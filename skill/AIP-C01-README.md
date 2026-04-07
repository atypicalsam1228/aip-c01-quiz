# AIP-C01 Quiz Manager

Pre-configured quiz skill for the AWS Certified Generative AI Developer Professional (AIP-C01) exam. Built on the general `/quiz-creator` skill with all paths, sources, and 202 questions already set up.

## Quick Start

```bash
/aip-c01-quiz launch          # Start the quiz app
/aip-c01-quiz status          # See question counts and coverage
/aip-c01-quiz generate 1 5    # Generate 5 more Domain 1 questions
/aip-c01-quiz gap-analysis    # Check exam guide coverage
```

## What's Included

- **202 questions** across 5 domains (93% exam guide skill coverage)
- **40+ ingested source documents** — AWS docs, whitepapers, Skill Builder, Reddit intel
- **Pre-configured vault** at `~/OneDrive/Obsidian/aws_learn_vault`
- **Quiz app** at `~/repos/aip-c01-quiz` (Python + HTML, zero dependencies)

## Relationship to /quiz-creator

This skill inherits from `/quiz-creator` (the general-purpose quiz builder). All subcommands follow the same workflows — this skill just pre-fills the AIP-C01 configuration so you don't have to set up paths, domains, or source mappings.

To create a quiz for a different exam, use `/quiz-creator` directly.
