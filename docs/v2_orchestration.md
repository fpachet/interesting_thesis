# V2 Orchestration Proposal

## Goal

Turn the current "one corpus -> one debate -> one final synthesis" pipeline into a research workflow that can:

- preserve every run instead of overwriting outputs
- let the user intervene interactively between steps
- chain several research questions over time
- accumulate reusable materials
- build an outline from those materials
- later support section-by-section drafting

The current pipeline remains the base engine for a single research question.

## Principle

V2 should add an orchestration layer above the existing pipeline, not replace it.

Current system:

- one theme
- one corpus
- one ordered list of roles
- several rounds
- one final synthesis

V2 system:

- one research program
- several research questions
- one or more runs per question
- user notes and forks between runs
- materials extracted from each run
- one outline built from validated materials
- later, one draft per section

## Where Orchestration Lives

The orchestration itself should not live in prompts and should not be hardcoded in Python.

It should be described declaratively at three distinct levels.

### 1. Workflow templates

Reusable research workflows, stored in:

```text
config/workflows/
```

Examples:

- `philosophical_question.json`
- `chapter_building.json`
- `literature_review.json`

These files describe the sequence of stages:

- which stages exist
- in what order they run
- which roles are used at each stage
- whether personas are allowed
- which artifacts each stage must produce
- which checkpoints are created

This is the generic orchestration layer of the framework.

### 2. Program instantiation

The project chooses and parameterizes those workflows in:

```text
research/program.json
research/questions/<id>.json
```

This layer answers:

- which workflow template is used for this project
- which workflow is used for each question
- which personas are available
- which sources are active
- which manuscript sections are targeted

This is the declarative orchestration of one concrete thesis project.

### 3. Runtime state

Execution state belongs in:

```text
memory/program_state.json
memory/runs/<run_id>.json
output/runs/<run_id>/checkpoints/
```

This layer records:

- current stage
- completed stages
- user notes
- selected materials
- resumable checkpoints

This is not the orchestration definition itself, but the current state of its execution.

### Short rule

In one sentence:

- templates define possible workflows
- `program.json` chooses and configures them
- `memory/` records where execution currently is

## Core Concepts

### Program

Top-level research object.

Contains:

- thesis title
- global theme
- list of questions
- available personas
- preferred output format
- target sections of the manuscript

### Question

A question is a bounded inquiry, not a whole thesis.

Examples:

- Is interestingness one concept or several regimes?
- Is readability a condition of interestingness or only one of its effects?
- Does the interesting solve a constrained problem, or does it displace the problem itself?

Each question has:

- `id`
- `title`
- `prompt`
- `depends_on`
- `personas`
- `source_paths`
- `target_sections`
- `status`

### Run

A run is one execution for one question.

Runs are immutable records. They should never be overwritten.

Each run has:

- `run_id`
- `question_id`
- `parent_run_id`
- `forked_from_checkpoint`
- `created_at`
- `status`
- `roles_snapshot`
- `input_snapshot`
- `user_notes`
- `artifacts`

### Checkpoint

A checkpoint is a resumable state inside a run.

Recommended checkpoints:

- after corpus digest
- after each round synthesis
- after final synthesis
- after material extraction

### Material Card

This is the missing layer between debate and writing.

A material card is a reusable thesis fragment extracted from a run.

Kinds:

- `definition`
- `distinction`
- `argument`
- `objection`
- `example`
- `counterexample`
- `transition`
- `paragraph`
- `bibliographic_note`

Each material card should contain:

- `id`
- `kind`
- `title`
- `body`
- `status` (`draft`, `promising`, `validated`, `rejected`)
- `source_run_id`
- `source_round`
- `source_roles`
- `source_documents`
- `source_personas`
- `target_sections`
- `tags`

### Outline Section

Section-level planning object.

Contains:

- `id`
- `title`
- `goal`
- `question_ids`
- `material_ids`
- `status`
- `draft_path`

## Recommended Directory Layout

```text
input/
  global/
  personas/
    descartes/
    simondon/
    bergson/
    husserl/

output/
  runs/
    2026-04-12_q00_baseline/
      config_snapshot.json
      corpus_digest.md
      rounds/
        round_01.md
        round_02.md
      final_synthesis.md
      materials.json
      checkpoints/
        digest.json
        round_01.json
        round_02.json
        final.json
    2026-04-13_q01_regimes_interet/
  exports/

research/
  program.json
  questions/
    q00_baseline.json
    q01_regimes_interet.json
    q02_lisibilite.json
  materials/
    m_0001.md
    m_0002.md
  outline/
    outline.json
  drafts/
    01_introduction.md
    02_cadre_conceptuel.md
    03_regimes_de_l_interessant.md

memory/
  program_state.json
  runs/
    2026-04-12_q00_baseline.json
    2026-04-13_q01_regimes_interet.json
```

## Interactive Workflow

The user should not need to relaunch everything from zero.

Recommended user actions:

1. create a question
2. start a run
3. read intermediate outputs
4. add a note
5. resume from the latest checkpoint
6. if needed, fork from an older checkpoint
7. extract materials
8. send validated materials to the outline

Two interaction modes are needed.

### Resume

Use when the user wants to influence only the remaining steps.

Example:

- after round 2, add note: "insist more on Simondon and provide musical examples"
- resume from checkpoint `round_02`
- only downstream steps are recomputed

### Fork

Use when the user wants to revise the logic of an earlier stage without destroying history.

Example:

- fork from checkpoint `digest`
- change the active personas
- launch a new run for the same question

This preserves the old run and makes comparison possible.

## CLI Proposal

The current command should continue to work for the single-question engine:

```bash
python -m interesting_thesis
```

Add a second layer of commands:

```bash
python -m interesting_thesis program init
python -m interesting_thesis question add
python -m interesting_thesis question list
python -m interesting_thesis run start --question q01_regimes_interet
python -m interesting_thesis run status --run 2026-04-13_q01_regimes_interet
python -m interesting_thesis run resume --run 2026-04-13_q01_regimes_interet --note "Ajouter des exemples musicaux et distinguer Husserl de Bergson."
python -m interesting_thesis run fork --run 2026-04-13_q01_regimes_interet --from-checkpoint round_02
python -m interesting_thesis materials extract --run 2026-04-13_q01_regimes_interet
python -m interesting_thesis materials list
python -m interesting_thesis outline build
python -m interesting_thesis draft render --section 02_cadre_conceptuel
```

## Minimal Data Files

### `research/program.json`

Defines:

- thesis metadata
- canonical list of personas
- global manuscript sections
- ordered question registry
- selected orchestration templates

### `research/questions/<id>.json`

Defines:

- local research question
- active personas
- source paths
- expected outputs
- target sections

### `output/runs/<run_id>/config_snapshot.json`

Freezes:

- prompts
- role order
- input paths
- theme
- model
- reasoning effort

This is important for reproducibility.

## Persona Design

Personas should be available as a library, but only a few should be active in each run.

Each persona should contain:

- `key`
- `name`
- `source_paths`
- `digest_path`
- `theses`
- `preferred_questions`
- `blind_spots`
- `prompt_file`

Important rule:

- keep 10 to 12 available personas if useful
- activate only 2 to 4 personas in a single run

## Example Workflow Template

The most useful first template is a bounded philosophical-question workflow:

1. problematization
2. theory dialogue
3. examples and counterexamples
4. local synthesis
5. material extraction

This template should live in `config/workflows/philosophical_question.json`.

Each question would then simply reference that template instead of redefining all stages manually.

## Recalculation Rules

### If the user adds a note during a run

- resume from the latest checkpoint
- recompute only downstream artifacts

### If the user changes a role prompt

- create a fork
- recompute from the first affected checkpoint

### If the user adds a new source document to a persona

- recompute that persona digest
- recompute only the questions using that persona

### If the user adds a new global document

- recompute global digest
- recompute affected questions

### If the user adds a new question

- no existing run is touched
- create a new run

## Thesis Workflow

V2 should support this sequence:

1. define the global theme
2. define the available personas
3. define a sequence of research questions
4. run debates question by question
5. extract material cards
6. validate selected materials
7. build the outline
8. render drafts section by section
9. export to LaTeX or PDF

This means the architecture should represent the stages of a thesis, but implementation should remain incremental.

## Suggested Implementation Order

### Phase 1

Low risk, immediate value:

- immutable run directories
- config snapshots
- checkpoints
- resume and fork semantics

### Phase 2

Research workflow:

- `program.json`
- question registry
- question-level runs
- material extraction

### Phase 3

Writing support:

- validated material store
- outline builder
- section drafts in Markdown

### Phase 4

Optional later layer:

- persona-specific corpora and digests
- LaTeX export
- bibliography hooks
- review mode for chapter revision

## Recommended First Deliverable

The first useful V2 should not try to automate the whole thesis.

It should deliver:

- versioned runs
- question registry
- resume and fork
- material cards
- outline builder

That is enough to move from isolated debates to a real research workflow.
