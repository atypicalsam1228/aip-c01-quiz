# Question Generation Guide

How to generate high-quality exam practice questions from source documents. This guide is exam-agnostic — it works for any certification, course, or assessment.

---

## 1. Before You Start — Exam Guide Analysis

**This is Step 1. Do not skip it.**

An exam guide or syllabus is the blueprint for what gets tested. Without it, you're guessing.

1. **Read the exam guide completely** — understand the scope, weights, and question types
2. **Extract every domain, task, and skill** into a structured list:
   ```
   Domain 1: Topic Name (31%)
     Task 1.1: Task description
       Skill 1.1.1: Specific skill
       Skill 1.1.2: Specific skill
     Task 1.2: Task description
       ...
   ```
3. **Note exam weights** — Domain 1 at 31% should have ~31% of your questions
4. **Identify question types** — single-answer, multi-select, ordering, matching
5. **Create a coverage tracking table** — you'll mark each skill as COVERED, PARTIAL, or GAP after generating questions

**If no exam guide exists**, create one from course objectives, textbook chapter headings, or learning outcomes. The structure matters more than the source.

---

## 2. Source Document Strategy

### What Makes a Good Source
- **Official documentation** — service docs, developer guides, user manuals
- **Whitepapers and best practices** — architecture guides, design patterns
- **Exam prep courses** — Skill Builder, Udemy, A Cloud Guru (screencapture the slides/questions)
- **Test-taker intelligence** — Reddit threads, forum posts from people who took the exam
- **Practice question sets** — official and third-party (extract and reformat)

### What NOT to Use
- LLM-generated content without verification — it may contain hallucinations
- Outdated documentation — check publication dates
- Blog posts without citations — prefer primary sources

### How Much Source Material
- **Minimum**: 3-5 substantive documents per domain
- **Recommended**: 10+ documents per domain including official docs, course material, and test-taker intel
- **Test-taker intel is gold** — it reveals question patterns, heavily tested topics, and difficulty calibration

### Ingesting Sources
- **PDFs**: Extract with pdfplumber (text-based) or vision API (screenshot PDFs)
- **Web pages**: Scrape with Firecrawl or defuddle for clean markdown
- **Screencaptures**: Extract via vision, preserve questions and answer choices exactly
- **Store in Obsidian vault** (recommended) or a flat folder structure (minimal mode)

---

## 3. Question Design Principles

### The Constraint-Based Trade-Off Pattern

This is THE dominant pattern for professional-level certification exams. Master it.

**Structure:**
```
Scenario (2-3 paragraphs):
  - Company/developer facing a real problem
  - Specific technical context (services, scale, data)
  - At least ONE hard constraint (latency SLA, cost ceiling, compliance req, data residency, team capability)

Question stem:
  "Which solution meets these requirements with the LEAST operational overhead?"
  "Which approach is MOST cost-effective while meeting the latency requirement?"

Options (4-5):
  A. Viable approach — but violates the constraint
  B. Correct approach — satisfies ALL requirements including the constraint
  C. Overengineered approach — works but adds unnecessary complexity
  D. Wrong service — real service used in wrong context
```

**Key principles:**
- **Two answers should technically work** — but only one satisfies all constraints
- **Test WHY, not WHAT** — don't test "What does Service X do?" Test "When do you choose X over Y given these constraints?"
- **Service justification** — the question forces defending one choice over another
- **Include the constraint in the scenario, not the question stem** — the learner must identify it

### Question Stem Patterns
- "Which solution meets these requirements with the LEAST operational overhead?"
- "Which approach is MOST cost-effective?"
- "What makes this solution possible?" (not "most efficient")
- "Which combination provides the MOST comprehensive protection?"
- "Which TWO steps should the team implement?" (multi-select)

### Plausible Distractors
Wrong answers must be real services/features used in wrong contexts:
- Right service, wrong use case (using Kendra for RAG instead of Knowledge Bases)
- Right concept, wrong implementation (manual instead of managed)
- Overengineered solution (custom Lambda pipeline when a managed service exists)
- Correct for a different constraint (cost-optimized when the constraint is latency)

**Never** use obviously fake or absurd answer choices.

---

## 4. Question Format Specification

### Obsidian Callout Syntax (Required)

```markdown
## Question 1

> [!question] Question — Descriptive Title (Domain N)
> Scenario paragraph 1...
>
> Scenario paragraph 2 with the constraint...
>
> Which solution meets these requirements?
>
> **A.** First option text
>
> **B.** Second option text
>
> **C.** Third option text
>
> **D.** Fourth option text

> [!example]- Answer: B
> **Correct Answer:** B
>
> **A. Incorrect.** Detailed explanation of why this doesn't work (4+ sentences).
> Cite specific source docs. Explain which constraint it violates.
>
> **B. Correct.** Detailed explanation of why this is right (4+ sentences).
> Cite specific source docs. Explain how it satisfies all constraints.
>
> **C. Incorrect.** Detailed explanation...
>
> **D. Incorrect.** Detailed explanation...
```

### Multi-Select Format

```markdown
> Which TWO steps should the team implement? (Select TWO.)
>
> **A.** through **E.**

> [!example]- Answer: B, D
```

### Ordering Format

```markdown
> Select and order each step. (Select and order FIVE.)
>
> - Step item 1
> - Step item 2
> ...
>
> **Step 1:** Correct first step
> **Step 2:** Correct second step
```

### Frontmatter

```yaml
---
type: generated-questions
category: descriptive-category-name
domain: 1
domain_name: "Domain Name"
question_count: 10
sources:
  - "[[Sources/path/to/source1]]"
  - "[[Sources/path/to/source2]]"
generated: YYYY-MM-DD
---
```

For multi-domain files, omit `domain` from frontmatter and tag each question title with `(Domain N)`.

---

## 5. Question Types and Mix

| Type | Percentage | Format |
|------|-----------|--------|
| Single-answer | 70% | 4 options (A-D), one correct |
| Multi-select | 25% | 5 options (A-E), "Select TWO" or "Select THREE" |
| Ordering | 5% | 5 items to order sequentially |

- State the selection count explicitly: "(Select TWO.)" not "(Select all that apply.)"
- Multi-select questions should have exactly 2-3 correct answers, not 4
- Ordering questions should have 4-5 steps with clear sequential logic

---

## 6. Domain and Task Tagging

**Every question MUST include a domain tag:**
```
> [!question] Question — Title (Domain 1)
```

**Every question SHOULD include a task tag when the source mapping is clear:**
```
> [!question] Question — Title (Task 1.2)
```

Tags enable:
- **Task-balanced sets** — questions interleaved by task so each set covers all tasks
- **Gap analysis** — compare questions against exam guide skills
- **Coverage tracking** — ensure no domain/task is over- or under-represented
- **Topic classification** — keyword-based grouping for drill-down mode

Questions without explicit tags get auto-classified by keyword matching — but explicit tags are more accurate.

---

## 7. Complexity Calibration

Match the difficulty to the target exam level:

### Professional / Specialty Level
- Multi-service architectures (3+ services per scenario)
- Constraint trade-offs requiring architectural judgment
- 3-4 paragraph scenarios with embedded constraints
- "When and why" questions, not "what does it do"
- Test-taker intel: "harder than expected", "trade-off questions dominate"

### Associate Level
- Service feature knowledge with application context
- Simpler scenarios (2 paragraphs)
- "Which service best fits this use case?"
- Some trade-offs but with clearer correct answers

### Foundational / Practitioner Level
- Concept understanding and definitions
- 1-paragraph scenarios or direct questions
- "What is the primary purpose of Service X?"
- Clear correct answer, obviously wrong distractors

### Calibrating with Test-Taker Intel
Search Reddit, forums, and study groups for posts from people who took the exam:
- What topics were heavily tested?
- What question patterns did they see?
- What surprised them about the difficulty?
- What study resources actually helped?

This intel is invaluable for calibrating question complexity and focus areas.

---

## 8. Gap Analysis Process

After generating your initial question set:

1. **List ALL skills from the exam guide** (every skill under every task)
2. **For each skill, search your questions** for coverage:
   - **COVERED** — at least one question directly tests this skill
   - **PARTIAL** — questions touch the topic but don't test the specific skill
   - **GAP** — no question tests this skill
3. **Calculate coverage percentage**: COVERED / total skills
4. **Target: 90%+ skill coverage** before considering the question bank complete
5. **Generate gap-filling questions** — one question per GAP skill, prioritized by domain weight
6. **Re-run analysis** to verify coverage improvement

### Priority Order for Gap Filling
1. Skills in high-weight domains (if Domain 1 = 31%, fill its gaps first)
2. Skills that test-taker intel says are heavily examined
3. Skills involving specific services called out in the exam guide
4. Skills in low-weight domains (fill last)

---

## 9. Answer Randomization Considerations

The quiz app shuffles answer positions (A-D) each session. This means:

- **Don't make the correct answer always the longest option** — vary lengths
- **Don't always put the correct answer in position B** — the shuffle handles this, but don't create patterns
- **Each option should be roughly the same detail level** — if A is one sentence and B is a paragraph, the length signals the answer
- **On retry, answers are reshuffled** — learners can't memorize "it was the third option"
- **Write each option to stand alone** — don't use "All of the above" or "None of the above"

---

## 10. Review Checklist

Before finalizing a question set, verify:

- [ ] Every question has a realistic business scenario (not abstract or theoretical)
- [ ] Every question has at least one hard constraint that determines the answer
- [ ] All 4+ options are plausible (no obvious throwaway answers)
- [ ] Explanations cover ALL options with 4+ sentences each
- [ ] Explanations explain WHY wrong answers fail, not just that they're wrong
- [ ] Domain tags `(Domain N)` are present in every question title
- [ ] Task tags `(Task X.Y)` are present where the mapping is clear
- [ ] No duplicate scenarios across question files
- [ ] Question distribution roughly matches exam domain weights
- [ ] Gap analysis shows 90%+ skill coverage
- [ ] Question types match the exam format (70/25/5 split or as specified)
- [ ] Source documents are cited in explanations where applicable
- [ ] Questions test "when and why" not "what does it do"
- [ ] Multi-select questions explicitly state the count: "(Select TWO.)"

---

## Example: End-to-End Workflow

```
1. User uploads exam guide: /quiz-creator setup exam-guide.pdf
   → Agent extracts 5 domains, 20 tasks, 89 skills
   → Creates coverage map with all 89 skills marked as GAP

2. User ingests source documents into vault Sources/
   → 40+ documents across official docs, courses, test-taker intel

3. User generates questions: /quiz-creator generate all 10
   → Agent reads sources, generates 50 questions (10 per domain)
   → Tags each with domain and task
   → Coverage: 67/89 skills (75%)

4. User runs gap analysis: /quiz-creator gap-analysis
   → 22 skills still uncovered
   → Recommends 20 gap-filling questions

5. User fills gaps: /quiz-creator gap-fill 20
   → 20 targeted questions for uncovered skills
   → Coverage: 83/89 skills (93%)

6. User builds and launches: /quiz-creator build && /quiz-creator launch
   → Quiz app at http://localhost:8765
   → 70 questions in domain sets of 15-20
   → Task-balanced, answer-shuffled, 3-retry
```
