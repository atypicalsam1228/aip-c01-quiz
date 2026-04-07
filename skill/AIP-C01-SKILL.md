---
name: aip-c01-quiz
description: "Pre-configured AIP-C01 (AWS Certified Generative AI Developer Professional) quiz manager. 202 questions, 93% exam guide coverage, Obsidian vault integration. Generate new questions, run gap analysis, launch the quiz app. Use when the user invokes /aip-c01-quiz or asks about their AIP-C01 exam prep, quiz, or practice questions."
---

# AIP-C01 Quiz Manager

Pre-configured instance of the `/quiz-creator` skill for the **AWS Certified Generative AI Developer Professional (AIP-C01)** exam. All paths, domains, sources, and 202 questions are already set up.

For the general-purpose quiz creation workflow, see `/quiz-creator`.

## Configuration (Pre-Set)

```
EXAM_NAME: AWS Certified Generative AI Developer Professional (AIP-C01)
QUIZ_DIR: C:/Users/samue/repos/aip-c01-quiz
VAULT_PATH: C:/Users/samue/OneDrive/Obsidian/aws_learn_vault
GENERATED_DIR: C:/Users/samue/OneDrive/Obsidian/aws_learn_vault/Sources/Exam-Prep/Generated-Questions
SOURCE_DIR: C:/Users/samue/OneDrive/Obsidian/aws_learn_vault/Sources
EXAM_GUIDE_PATH: C:/Users/samue/OneDrive/Obsidian/aws_learn_vault/Sources/Exam-Prep/ai-professional-01.md
GIT_CMD: git --git-dir=C:/Users/samue/repos/aws_learn_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/aws_learn_vault
```

## Subcommands

| Command | Description |
|---------|-------------|
| `/aip-c01-quiz status` | Show question counts, domain/task distribution, coverage % |
| `/aip-c01-quiz generate <domain\|all> [count]` | Generate new AIP-C01 questions for a domain |
| `/aip-c01-quiz gap-analysis` | Compare questions against all 89 exam guide skills |
| `/aip-c01-quiz gap-fill [count]` | Generate questions for uncovered skills |
| `/aip-c01-quiz launch` | Kill existing server, start quiz at localhost:8765 |
| `/aip-c01-quiz` (no args) | Show subcommands |

All subcommands follow the workflows defined in `/quiz-creator` SKILL.md — this skill just pre-fills the configuration.

## Current Stats

| Domain | Weight | Questions | Tasks | Sets |
|--------|--------|-----------|-------|------|
| D1: FM Integration, Data, Compliance | 31% | 55 | 6 tasks | 3 (19/18/18) |
| D2: Implementation & Integration | 26% | 50 | 5 tasks | 3 (17/17/16) |
| D3: Safety, Security, Governance | 20% | 45 | 4 tasks | 3 (15/15/15) |
| D4: Operational Efficiency | 12% | 31 | 3 tasks | 2 (16/15) |
| D5: Testing & Troubleshooting | 11% | 21 | 2 tasks | 1 (21) |
| **Total** | | **202** | **20 tasks** | **12 sets** |

**Exam guide coverage: 83/89 skills (93%)**

## Question Files

```
Sources/Exam-Prep/Generated-Questions/
├── domain-1-generated.md          # 10 — revised with ANN, chunking, prompt caching
├── domain-2-generated.md          # 10 — revised with Agent Squad, model cascading, SSE
├── domain-3-generated.md          # 10 — revised with OWASP, Comprehend Medical, Audit Manager
├── domain-4-generated.md          # 10 — revised with ADOT, Inference Recommender
├── domain-5-generated.md          # 10 — revised with golden datasets, semantic drift
├── trade-off-questions.md         # 25 — Reddit test-taker informed
├── domain-3-safety-governance.md  # 10 — Guardrails, PII, bias deep-dive
├── agentic-ai-questions.md        #  8 — AgentCore, Strands, MCP
├── service-differentiation.md     # 10 — Bedrock vs SageMaker, etc.
├── skillbuilder-extracted-questions.md  # 33 — from AWS Skill Builder
├── screencapture-tradeoff-questions.md  # 30 — ANN, chunking, circuit breakers
└── gap-filling-questions.md       # 20 — targeting uncovered exam guide skills
```

Plus 14 BenchPrep practice sets + 2 bonus sets in `Practice-Questions/` and `Bonus-Questions/`.

## Exam Domains Reference

### Domain 1 (31%) — 6 Tasks, 25 Skills
- Task 1.1: Analyze requirements and design GenAI solutions
- Task 1.2: Select and configure FMs
- Task 1.3: Data validation and processing pipelines
- Task 1.4: Vector store solutions
- Task 1.5: Retrieval mechanisms (RAG)
- Task 1.6: Prompt engineering strategies and governance

### Domain 2 (26%) — 5 Tasks, 22 Skills
- Task 2.1: Agentic AI and tool integrations
- Task 2.2: Model deployment strategies
- Task 2.3: Enterprise integration architectures
- Task 2.4: FM API integrations
- Task 2.5: Application integration and development tools

### Domain 3 (20%) — 4 Tasks, 14 Skills
- Task 3.1: Input and output safety controls
- Task 3.2: Data security and privacy controls
- Task 3.3: AI governance and compliance
- Task 3.4: Responsible AI principles

### Domain 4 (12%) — 3 Tasks, 14 Skills
- Task 4.1: Cost optimization and resource efficiency
- Task 4.2: Application performance optimization
- Task 4.3: Monitoring systems

### Domain 5 (11%) — 2 Tasks, 14 Skills
- Task 5.1: Evaluation systems
- Task 5.2: Troubleshoot GenAI applications

## Source Documents

See `references/DOMAIN-SOURCE-MAP.md` for the complete mapping of source documents to exam domains.

Key sources:
- Official AIP-C01 exam guide (33 pages)
- 5 Domain NotebookLM research files
- Reddit test-taker intelligence (5 threads)
- 41 Skill Builder screencapture extractions
- AWS whitepapers (inference architecture, enterprise strategy, best practices)
- Bedrock service docs (agents, guardrails, knowledge bases, evaluation, prompt management)

## Related Skills

| Skill | Relationship |
|---|---|
| `/quiz-creator` | General-purpose quiz creation (this skill inherits from it) |
| `/aws-vault` | Manages the Obsidian vault with sources and wiki articles |
| `/firecrawl` | Scrape additional AWS documentation |
| `/notebooklm` | Analyze sources to find testable concepts |
| `/guided-learning` | Teach weak areas identified by quiz results |

## Git Workflow

```bash
# Commit vault changes (questions, sources)
git --git-dir=C:/Users/samue/repos/aws_learn_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/aws_learn_vault add -A
git --git-dir=C:/Users/samue/repos/aws_learn_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/aws_learn_vault commit -m "description"

# Commit quiz app changes
cd C:/Users/samue/repos/aip-c01-quiz && git add -A && git commit -m "description"
```
