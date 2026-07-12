import AppKit
import Foundation

let checker = NSSpellChecker.shared
let locale = Locale(identifier: "fr_FR")
let includeValidWords = CommandLine.arguments.contains("--all")

func withoutDiacritics(_ text: String) -> String {
    text.folding(options: [.diacriticInsensitive, .caseInsensitive], locale: locale)
        .lowercased(with: locale)
}

while let line = readLine() {
    let word = line.trimmingCharacters(in: .whitespacesAndNewlines)
    guard !word.isEmpty else { continue }

    let range = NSRange(location: 0, length: (word as NSString).length)
    var wordCount = 0
    let misspelled = checker.checkSpelling(
        of: word,
        startingAt: 0,
        language: "fr",
        wrap: false,
        inSpellDocumentWithTag: 0,
        wordCount: &wordCount
    )
    guard includeValidWords || misspelled.location != NSNotFound else { continue }

    let guesses = checker.guesses(
        forWordRange: range,
        in: word,
        language: "fr",
        inSpellDocumentWithTag: 0
    ) ?? []

    if let suggestion = guesses.first(where: {
        $0 != word && withoutDiacritics($0) == withoutDiacritics(word)
    }) {
        print("\(word)\t\(suggestion)")
    }
}
