---
name: quiz-creator
description: "Generate exam-style practice quiz apps from source documents. Upload an exam guide/syllabus, ingest source docs, generate constraint-based trade-off questions by domain, run gap analysis, and build a local Python+HTML quiz app with domain sets, topic drill-down, answer shuffling, 3-retry, and progress tracking. Works for any certification exam."
---

# Quiz Creator

Generate exam-style practice quiz applications from authoritative source documents and an exam guide. Produces a self-contained Python + HTML app with domain-grouped question sets, task-balanced distribution, topic drill-down, randomized answer order, missed-question retry, and progress tracking.

**Works for any certification exam** — not just AWS. The exam guide drives everything.

## Prerequisites

1. **Exam guide or syllabus** (required) — PDF or markdown listing domains, tasks, and skills
2. **Source documents** (required) — official docs, whitepapers, course material, test-taker intel
3. **Obsidian vault** (recommended) — for organized source management, wikilinks, and study reference
4. **Firecrawl** (optional) — for scraping additional documentation

## Two Operating Modes

| Mode | What You Need | Best For |
|------|---------------|----------|
| **Minimal** | A folder with source docs + exam guide | Quick setup, single user |
| **Full (recommended)** | Obsidian vault with Sources/Wiki/Capture structure | Team use, ongoing study, cross-referencing |

In Minimal mode, questions are generated into a flat folder. In Full mode, questions go into the vault's `Generated-Questions/` directory with wikilinks to source documents.

## Configuration

```
EXAM_NAME: (e.g., "AWS AIP-C01", "CISSP", "CompTIA Security+")
QUIZ_DIR: (e.g., C:/Users/samue/repos/aip-c01-quiz)
EXAM_GUIDE_PATH: (e.g., Sources/Exam-Prep/ai-professional-01.md)
```

**For Obsidian Full mode, also set:**
```
VAULT_PATH: (e.g., C:/Users/samue/OneDrive/Obsidian/aws_learn_vault)
GENERATED_DIR: {VAULT_PATH}/Sources/Exam-Prep/Generated-Questions
SOURCE_DIR: {VAULT_PATH}/Sources
```

**For Minimal mode:**
```
SOURCE_DIR: (folder containing source documents)
GENERATED_DIR: (folder for generated question files)
```

## Subcommand Selection

| User invokes | Subcommand |
|---|---|
| `/quiz-creator setup <exam-guide-path>` | setup |
| `/quiz-creator generate <domain\|all> [count]` | generate |
| `/quiz-creator generate-topics` | generate-topics |
| `/quiz-creator gap-analysis` | gap-analysis |
| `/quiz-creator gap-fill [count]` | gap-fill |
| `/quiz-creator scrape <topic\|url>` | scrape |
| `/quiz-creator build` | build |
| `/quiz-creator status` | status |
| `/quiz-creator launch` | launch |
| `/quiz-creator` (no args) | Show available subcommands |

---

## /quiz-creator setup <exam-guide-path>

**This is Step 1. Run this before generating any questions.**

Parse an exam guide or syllabus to extract the complete skill map that drives question generation and gap analysis.

### Workflow

1. **Read the exam guide** at `<exam-guide-path>`:
   - If PDF, extract text first (pdfplumber or vision)
   - If markdown, read directly

2. **Extract the complete structure:**
   - All domains with exam weights (e.g., "Domain 1: FM Integration — 31%")
   - All tasks within each domain (e.g., "Task 1.1: Analyze requirements")
   - All skills within each task (e.g., "Skill 1.1.1: Create architectural designs")
   - Question types the exam uses (single, multi-select, ordering, matching)
   - Total scored questions and passing score

3. **Create a coverage map file** at `{GENERATED_DIR}/_coverage-map.md`:
   ```markdown
   # {EXAM_NAME} Coverage Map
   Generated: {date}
   
   ## Domain 1: {Name} ({weight}%)
   ### Task 1.1: {Description}
   - [ ] Skill 1.1.1: {Description} — GAP
   - [ ] Skill 1.1.2: {Description} — GAP
   ### Task 1.2: {Description}
   ...
   ```
   All skills start as GAP. They get updated to COVERED/PARTIAL as questions are generated.

4. **Output summary:**
   ```
   ══════════════════════════════════════
     Exam Guide Parsed
   ══════════════════════════════════════
     Exam:       {EXAM_NAME}
     Domains:    N (with weights)
     Tasks:      N
     Skills:     N
     Q Types:    single, multi-select, ordering
     Coverage:   {GENERATED_DIR}/_coverage-map.md
   ──────────────────────────────────────
     Next: ingest source docs, then
     /quiz-creator generate all
   ══════════════════════════════════════
   ```

---

## /quiz-creator generate <domain|all> [count]

Generate constraint-based trade-off questions for a specific domain or all domains.

### Arguments

- `<domain>`: Domain number (1-5) or `all`
- `[count]`: Questions per domain (default: 10, split ~70% single + ~25% multi-select + ~5% ordering)

### Workflow

1. **Read the coverage map** to understand which tasks/skills need questions

2. **Read the exam guide** for the specific domain's tasks and skills

3. **Identify source material:**
   - Scan `{SOURCE_DIR}/` for relevant documents
   - Read substantial portions to understand available content
   - If sources are thin, recommend scraping first

4. **Generate questions** following the constraint-based trade-off pattern:
   - Read `references/QUESTION-GENERATION-GUIDE.md` for the full methodology
   - Every question: realistic scenario + hard constraint + 4 plausible options
   - Two answers technically work, only one satisfies all constraints
   - Tag each question with `(Domain N)` and `(Task X.Y)` in the title
   - Detailed explanations for ALL options (4+ sentences each)
   - 70% single-answer, 25% multi-select, 5% ordering

5. **Write question file** to `{GENERATED_DIR}/`:
   - Single-domain: `domain-{N}-generated.md`
   - Category files: `{category}-questions.md`

6. **Update coverage map** — mark skills as COVERED for each question generated

7. **Output summary** with question count, domain, file path, and updated coverage %

---

## /quiz-creator generate-topics

Generate topic-focused question sets for drill-down practice.

### Workflow

1. **Analyze existing questions** to identify natural topic clusters:
   - RAG & Retrieval, Prompt Engineering, Agentic AI, Model Deployment, Streaming & APIs
   - Guardrails & Safety, Data Privacy, Governance, Cost Optimization, Monitoring, Evaluation

2. **For each topic with fewer than 5 questions**, generate additional questions from source material

3. **Tag questions with topic keywords** in titles and scenarios so the quiz app's keyword classifier can group them

4. **Write to** `{GENERATED_DIR}/topic-{name}-questions.md`

---

## /quiz-creator gap-analysis

Compare all generated questions against the exam guide's skill map and report coverage.

### Workflow

1. **Read the coverage map** from `{GENERATED_DIR}/_coverage-map.md`

2. **Read ALL question files** in `{GENERATED_DIR}/`

3. **For each skill in the exam guide:**
   - Search all questions for coverage (by task tag, keywords, or scenario content)
   - Mark as COVERED, PARTIAL, or GAP

4. **Calculate coverage:** COVERED / total skills

5. **Output report:**
   ```
   ══════════════════════════════════════
     Gap Analysis: {EXAM_NAME}
   ══════════════════════════════════════
     Total skills:    89
     Covered:         67 (75%)
     Partial:         16 (18%)
     Gap:              6 (7%)

     Critical Gaps (high-weight domains)
     ────────────────────────────────────
     1.1.3  Well-Architected GenAI Lens    D1 (31%)
     1.5.5  Query decomposition            D1 (31%)
     2.3.4  Edge deployment (Outposts)     D2 (26%)
     ...

     Recommendation: generate 15-20 gap-filling questions
     Run /quiz-creator gap-fill 20
   ══════════════════════════════════════
   ```

6. **Update the coverage map file** with current status

---

## /quiz-creator gap-fill [count]

Generate questions specifically targeting uncovered exam guide skills.

### Arguments

- `[count]`: Number of gap-filling questions (default: 20)

### Workflow

1. **Read the coverage map** — identify all GAP and PARTIAL skills

2. **Prioritize by domain weight** — fill high-weight domain gaps first

3. **For each gap**, generate one question:
   - Map the skill to available source material
   - Use the constraint-based trade-off pattern
   - Tag with the specific skill: `(Task X.Y)` or `(Domain N)`

4. **Write to** `{GENERATED_DIR}/gap-filling-questions.md`

5. **Re-run gap analysis** automatically and report updated coverage

---

## /quiz-creator scrape <topic|url>

Scrape documentation pages to add source material.

### Workflow

1. **Determine target:**
   - If URL: scrape directly
   - If topic name: search for the right documentation page
   - If domain number: scrape recommended gap-fill docs

2. **Scrape with Firecrawl:**
   ```bash
   firecrawl scrape "<url>" --only-main-content -o .firecrawl/{topic}.md
   ```

3. **Clean and add frontmatter:**
   ```yaml
   ---
   type: scraped-source
   source_url: "{url}"
   topic: "{description}"
   scraped: {date}
   ---
   ```

4. **Copy to source directory** (vault Sources/ or minimal mode folder)

5. **Output** the file path and suggest generating questions

---

## /quiz-creator build

Build or rebuild the quiz app with all current features.

### Workflow

1. **Create project directory** at `{QUIZ_DIR}/`

2. **Generate `quiz_server.py`** — Python stdlib HTTP server that:
   - Parses all markdown question files (single-question and multi-question formats)
   - Extracts domain from `(Domain N)` in titles or frontmatter
   - Extracts task from `(Task X.Y)` in titles or keyword classification
   - Auto-classifies untagged questions by keyword matching
   - Interleaves questions by task within each domain (round-robin for balanced sets)
   - Serves HTML and JSON API endpoints
   - Deduplicates questions by content hash
   - Auto-opens browser on startup

3. **Generate `quiz_app.html`** — Self-contained UI with:
   - **Start screen** with three sections:
     - **By Domain**: Sets of 15-20 questions per domain, task-balanced
     - **By Topic**: Drill-down by topic (RAG, Agents, Guardrails, etc.)
     - **Other Modes**: All, BenchPrep, Generated, Missed, Random 10, Shuffled
   - **Quiz screen**: Question display with randomized A-D order, domain-grouped sidebar
   - **Results screen**: Score, attempt history, per-domain breakdown, retry button
   - **Answer shuffling**: Options randomized each session, reshuffled on retry
   - **3-attempt retry**: Missed questions re-presented with new answer order, tracks improvement
   - **Keyboard shortcuts**: 1-5 select, Enter check/next, arrows navigate, F flag
   - **Progress persistence**: JSON file, resume across sessions

4. **Test:** `cd {QUIZ_DIR} && python quiz_server.py`

---

## /quiz-creator status

Show current state of the quiz system.

### Workflow

1. **Count questions** by domain, task, topic, and source file
2. **Show coverage** from the coverage map
3. **Report domain distribution** with set breakdowns

```
══════════════════════════════════════
  Quiz Creator Status: {EXAM_NAME}
══════════════════════════════════════
  Questions
  ────────────────────────────────────
  Domain 1: 55q [1.1:16, 1.2:9, 1.3:3, 1.4:4, 1.5:20, 1.6:3]
    Set 1 (19q): all 6 tasks covered
    Set 2 (18q): 4 tasks covered
    Set 3 (18q): 2 tasks covered
  Domain 2: 50q [2.1:17, 2.2:13, 2.3:11, 2.4:7, 2.5:2]
  ...
  Total: 202 questions

  Coverage: 83/89 skills (93%)
  Topics:  11 topic groups

  Quiz App: {QUIZ_DIR}/quiz_server.py
  Progress: exists (3 sessions recorded)
══════════════════════════════════════
```

---

## /quiz-creator launch

Stop any existing quiz server and launch a fresh one.

### Workflow

1. Kill any existing process on port 8765
2. Launch: `cd {QUIZ_DIR} && python quiz_server.py`
3. Report URL: `http://localhost:8765`

---

## Question Format Rules

### Callout format (must match for parser compatibility)

```markdown
> [!question] Question — Title (Domain N)
> Scenario text...
>
> **A.** Option text
> **B.** Option text
> **C.** Option text
> **D.** Option text

> [!example]- Answer: B
> **A. Incorrect.** Explanation...
> **B. Correct.** Explanation...
> **C. Incorrect.** Explanation...
> **D. Incorrect.** Explanation...
```

### Tagging

- `(Domain N)` — required in every question title for domain classification
- `(Task X.Y)` — recommended for task-balanced distribution
- Questions without tags get auto-classified by keyword matching

### File naming

- Domain files: `domain-{N}-generated.md`
- Category files: `{category}-questions.md`
- All files in `{GENERATED_DIR}/`, one `## Question N` per question

### Frontmatter

```yaml
---
type: generated-questions
category: category-name
domain: N (optional — for single-domain files)
question_count: N
sources:
  - "[[Sources/path/to/source]]"
generated: YYYY-MM-DD
---
```

---

## Question JSON Structure

The parser produces this per question:

```json
{
  "id": "d1-01",
  "source_file": "domain-1-generated.md",
  "title": "Descriptive Title",
  "type": "single|multi-select|ordering",
  "select_count": 1,
  "body": "Scenario text...",
  "options": [{"letter": "A", "text": "..."}],
  "correct_answers": ["B"],
  "correct_order": null,
  "explanations": {"A": {"correct": false, "text": "..."}},
  "set": "generated",
  "domain": 1,
  "domain_name": "Domain Name",
  "task": "1.2"
}
```

---

## Quiz App Features Summary

| Feature | Description |
|---------|-------------|
| Domain sets | 15-20 questions per set, ~30 min sessions |
| Task-balanced | Round-robin interleaving across tasks within each domain |
| Topic drill-down | Focus on RAG, Agents, Guardrails, Cost, etc. |
| Answer shuffle | A-D positions randomized each session |
| 3-attempt retry | Missed questions re-presented with reshuffled answers |
| Attempt history | Track improvement across retries |
| Multiple modes | Domain, topic, all, missed, random, shuffle, source-filtered |
| Domain sidebar | Expandable sections with per-domain scores |
| Keyboard shortcuts | 1-5 select, Enter check/next, arrows, F flag |
| Progress tracking | JSON persistence across sessions |
| Zero dependencies | Python stdlib only |

---

## Coverage Tracking

The coverage map at `{GENERATED_DIR}/_coverage-map.md` is the source of truth for exam coverage. It gets updated by:

- `/quiz-creator setup` — creates the map with all skills as GAP
- `/quiz-creator generate` — marks skills as COVERED when questions are generated
- `/quiz-creator gap-analysis` — re-scans all questions and updates the map
- `/quiz-creator gap-fill` — closes gaps and updates the map

**Target: 90%+ skill coverage before the question bank is considered complete.**

---

## Related Skills

| Skill | Relationship |
|---|---|
| `/aws-vault` | Manages the Obsidian vault where sources and questions live |
| `/firecrawl` | Scrapes documentation pages for source material |
| `/notebooklm` | Analyze source docs to identify testable concepts per domain |
| `/web-research` | Research topics online before generating questions |
| `/yt-research` | Find video content and transcripts for additional source material |
| `/guided-learning` | Teach concepts that quiz results reveal as weak areas |

## Git Workflow

After any changes, remind the user:

```
Commit quiz app changes:
  cd {QUIZ_DIR}
  git add -A && git commit -m "description"
```

If using an Obsidian vault with a bare repo:
```
Commit vault changes:
  git --git-dir={GIT_DIR} --work-tree={VAULT_PATH} add -A
  git --git-dir={GIT_DIR} --work-tree={VAULT_PATH} commit -m "description"
```

Do NOT auto-commit. The user decides when to snapshot.
