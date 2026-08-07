#!/usr/bin/env python3
"""Download and validate the direct PDFs in the personal-publications inventory."""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Result:
    pdf_url: str
    local_path: str
    status: str
    http_detail: str
    bytes: int = 0
    sha256: str = ""
    pages: str = ""


def validate_pdf(path: Path) -> tuple[bool, str]:
    try:
        with path.open("rb") as handle:
            header = handle.read(8)
    except OSError as exc:
        return False, str(exc)
    if not header.startswith(b"%PDF-"):
        return False, f"signature inattendue: {header!r}"
    check = subprocess.run(
        ["pdfinfo", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check.returncode != 0:
        return False, check.stderr.strip() or "pdfinfo a échoué"
    return True, check.stdout


def pdf_pages(pdfinfo_output: str) -> str:
    for line in pdfinfo_output.splitlines():
        if line.startswith("Pages:"):
            return line.partition(":")[2].strip()
    return ""


def checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(repo: Path, url: str, local_path: str) -> Result:
    target = repo / local_path
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        valid, detail = validate_pdf(target)
        if valid:
            return Result(
                url,
                local_path,
                "déjà présent",
                "",
                target.stat().st_size,
                checksum(target),
                pdf_pages(detail),
            )
        return Result(url, local_path, "fichier local invalide", detail)

    with tempfile.NamedTemporaryFile(
        prefix=f".{target.stem}-", suffix=".part", dir=target.parent, delete=False
    ) as handle:
        temporary = Path(handle.name)
    try:
        command = [
            "curl",
            "-L",
            "--fail",
            "--silent",
            "--show-error",
            "--retry",
            "2",
            "--connect-timeout",
            "20",
            "--max-time",
            "180",
            "--output",
            str(temporary),
            url,
        ]
        completed = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            return Result(url, local_path, "échec téléchargement", completed.stderr.strip())
        valid, detail = validate_pdf(temporary)
        if not valid:
            return Result(url, local_path, "contenu non PDF", detail)
        temporary.replace(target)
        return Result(
            url,
            local_path,
            "téléchargé",
            "",
            target.stat().st_size,
            checksum(target),
            pdf_pages(detail),
        )
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    with args.inventory.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    unique: dict[str, str] = {}
    for row in rows:
        if row["pdf_url"]:
            unique.setdefault(row["pdf_url"], row["local_target"])

    results: list[Result] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(fetch, args.repo.resolve(), url, target): url
            for url, target in unique.items()
        }
        total = len(futures)
        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            print(
                f"[{index:03d}/{total:03d}] {result.status}: {Path(result.local_path).name}",
                flush=True,
            )

    results.sort(key=lambda item: item.local_path.casefold())
    args.log.parent.mkdir(parents=True, exist_ok=True)
    with args.log.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(results[0])), delimiter="\t")
        writer.writeheader()
        for result in results:
            writer.writerow(asdict(result))

    failures = [result for result in results if result.status not in {"téléchargé", "déjà présent"}]
    print(f"Terminé: {len(results) - len(failures)}/{len(results)} PDF valides; {len(failures)} échecs")


if __name__ == "__main__":
    main()
