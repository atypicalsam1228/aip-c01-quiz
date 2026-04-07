"""
AIP-C01 Practice Quiz Server
Parses Obsidian markdown question files and serves a local quiz app.
No dependencies beyond Python stdlib.
"""

import http.server
import json
import re
import hashlib
import webbrowser
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────

VAULT_PATH = Path("C:/Users/samue/OneDrive/Obsidian/aws_learn_vault")
PRACTICE_DIR = VAULT_PATH / "Sources/Exam-Prep/Practice-Questions"
BONUS_DIR = VAULT_PATH / "Sources/Exam-Prep/Bonus-Questions"
GENERATED_DIR = VAULT_PATH / "Sources/Exam-Prep/Generated-Questions"
APP_DIR = Path(__file__).parent
HTML_FILE = APP_DIR / "quiz_app.html"
PROGRESS_FILE = APP_DIR / "progress.json"
PORT = 8765

DOMAIN_NAMES = {
    1: "Foundation Model Integration, Data Management, and Compliance",
    2: "Implementation and Integration",
    3: "AI Safety, Security, and Governance",
    4: "Operational Efficiency and Optimization",
    5: "Testing, Validation, and Troubleshooting",
}

# ── Markdown Parser ───────────────────────────────────────────────────────────


def strip_frontmatter(text):
    """Remove YAML frontmatter between --- markers."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].strip()
    return text


def extract_callout_block(text, callout_type):
    """Extract lines belonging to a specific callout block.
    Returns (header_line, body_lines, remaining_text).
    Stops when it hits a new callout header [!...] or leaves the > block.
    """
    lines = text.split("\n")
    header = None
    body = []
    start_idx = None
    end_idx = len(lines)

    for i, line in enumerate(lines):
        stripped = line.strip()
        if header is None:
            if f"[!{callout_type}]" in stripped:
                header = stripped
                start_idx = i
        else:
            # Stop if we hit a new callout header
            if re.search(r">\s*\[!", stripped) and i > start_idx:
                end_idx = i
                break
            # Callout body: lines starting with > (possibly empty >)
            if stripped.startswith(">") or stripped == "":
                body.append(stripped)
            else:
                end_idx = i
                break

    remaining = "\n".join(lines[end_idx:])
    return header, body, remaining


def parse_question_block(header, body_lines):
    """Parse a [!question] callout into title, body text, question type, and options."""
    # Extract title from header — handle em dash, en dash, hyphen, or missing title
    title_match = re.search(r"Question\s*[—–\-]\s*(.+)", header)
    if title_match:
        title = title_match.group(1).strip()
    else:
        # No title in header — use first sentence of body as title
        title = None  # will be set from body below

    body_parts = []
    options = []
    ordering_items = []
    correct_order = []

    for line in body_lines:
        # Strip leading > and whitespace
        content = re.sub(r"^>\s?", "", line)

        # Check for option lines: **A.** text
        opt_match = re.match(r"\*\*([A-E])\.\*\*\s*(.*)", content)
        if opt_match:
            options.append({
                "letter": opt_match.group(1),
                "text": opt_match.group(2).strip()
            })
            continue

        # Check for ordering list items: - Step text
        order_item_match = re.match(r"^-\s+(.+)", content)
        if order_item_match and not options:
            ordering_items.append(order_item_match.group(1).strip())
            continue

        # Check for Step N: answer lines (may have text or be empty)
        step_match = re.match(r"\*\*Step\s+(\d+):\*\*\s*(.*)", content)
        if step_match:
            step_text = step_match.group(2).strip()
            if step_text:
                correct_order.append(step_text)
            continue

        body_parts.append(content)

    body_text = "\n".join(body_parts).strip()

    # Generate title from body if not in header
    if title is None:
        # Use the last question sentence (usually "Which solution..." or "Which approach...")
        for line in reversed(body_text.split("\n")):
            line = line.strip()
            if line and line.endswith("?"):
                # Shorten to something reasonable
                title = line[:80].rstrip("?") if len(line) > 80 else line.rstrip("?")
                break
        if title is None:
            title = body_text[:60].split(".")[0]

    # Determine question type
    if "Select and order" in body_text or ordering_items:
        q_type = "ordering"
        select_count = len(ordering_items) if ordering_items else 5
    elif re.search(r"\(Select\s+(TWO|THREE|FOUR)\.\)", body_text):
        q_type = "multi-select"
        count_map = {"TWO": 2, "THREE": 3, "FOUR": 4}
        count_match = re.search(r"\(Select\s+(TWO|THREE|FOUR)\.\)", body_text)
        select_count = count_map.get(count_match.group(1), 2)
    else:
        q_type = "single"
        select_count = 1

    return {
        "title": title,
        "type": q_type,
        "select_count": select_count,
        "body": body_text,
        "options": options,
        "ordering_items": ordering_items if ordering_items else None,
        "correct_order": correct_order if correct_order else None,
    }


def parse_answer_block_practice(header, body_lines):
    """Parse a practice-style [!example]- Answer: X block."""
    # Extract correct answers from header
    answer_match = re.search(r"Answer:\s*(.+)", header)
    correct_answers = []
    if answer_match:
        ans_text = answer_match.group(1).strip()
        if "Correct" in ans_text:
            # Ordering question — correct order is in the question block
            pass
        else:
            correct_answers = [a.strip() for a in ans_text.split(",")]

    explanations = parse_explanations(body_lines)
    return correct_answers, explanations


def parse_answer_block_bonus(body_lines):
    """Parse a bonus-style [!example] Answer Explanations block."""
    explanations = parse_explanations(body_lines)
    # Extract correct answers by scanning for "Correct." in explanations
    correct_answers = [
        letter for letter, exp in explanations.items() if exp["correct"]
    ]
    return correct_answers, explanations


def parse_explanations(body_lines):
    """Parse per-option explanations from answer callout body lines."""
    explanations = {}
    current_letter = None
    current_text = []
    current_correct = False

    for line in body_lines:
        content = re.sub(r"^>\s?", "", line)

        # Skip "Your Answer:" / "Correct Answer:" metadata lines
        if content.startswith("**Your Answer:**") or content.startswith("**Correct Answer:**"):
            continue

        # Check for option explanation header: **A. Incorrect.** or **A. Correct.**
        # Also handle bonus format: **A. Full option text here**\nCorrect./Incorrect.
        exp_match = re.match(r"\*\*([A-E])\.\s*(Correct|Incorrect)\.\*\*\s*(.*)", content)
        if exp_match:
            # Save previous
            if current_letter:
                explanations[current_letter] = {
                    "correct": current_correct,
                    "text": "\n".join(current_text).strip()
                }
            current_letter = exp_match.group(1)
            current_correct = exp_match.group(2) == "Correct"
            current_text = [exp_match.group(3)] if exp_match.group(3) else []
            continue

        # Bonus format: **A. Full option text here**
        bonus_header = re.match(r"\*\*([A-E])\.\s+(.+?)\*\*\s*$", content)
        if bonus_header:
            if current_letter:
                explanations[current_letter] = {
                    "correct": current_correct,
                    "text": "\n".join(current_text).strip()
                }
            current_letter = bonus_header.group(1)
            current_correct = False
            current_text = []
            continue

        # Check if this line starts with Correct./Incorrect. (bonus format)
        if current_letter and current_text == []:
            correctness_match = re.match(r"^(Correct|Incorrect)\.\s*(.*)", content)
            if correctness_match:
                current_correct = correctness_match.group(1) == "Correct"
                if correctness_match.group(2):
                    current_text.append(correctness_match.group(2))
                continue

        if current_letter:
            current_text.append(content)

    # Save last option
    if current_letter:
        explanations[current_letter] = {
            "correct": current_correct,
            "text": "\n".join(current_text).strip()
        }

    return explanations


def parse_question_file(filepath):
    """Parse a single question markdown file into a structured dict."""
    text = filepath.read_text(encoding="utf-8")
    text = strip_frontmatter(text)

    # Determine set type from path
    q_set = "bonus" if "Bonus" in str(filepath) else "practice"

    # Extract ID from filename
    name = filepath.stem
    num_match = re.search(r"(\d+)", name)
    q_id = f"{q_set}-{num_match.group(1)}" if num_match else name

    # Parse question block
    q_header, q_body, remaining = extract_callout_block(text, "question")
    if not q_header:
        return None

    question_data = parse_question_block(q_header, q_body)

    # Parse answer block
    a_header, a_body, _ = extract_callout_block(remaining, "example")
    if not a_header:
        return None

    # Determine format: practice ([!example]-) vs bonus ([!example] Answer)
    if "[!example]-" in a_header or "[!example]- " in a_header:
        correct_answers, explanations = parse_answer_block_practice(a_header, a_body)
    else:
        correct_answers, explanations = parse_answer_block_bonus(a_body)

    # For ordering questions, extract correct order from explanation if not in question
    if question_data["type"] == "ordering":
        correct_answers = []  # Not letter-based
        if not question_data["correct_order"] and a_body:
            # Parse ordering from explanation text using ordinal markers
            explanation_text = "\n".join(re.sub(r"^>\s?", "", l) for l in a_body)
            ordinals = ["First", "Second", "Third", "Fourth", "Finally"]
            items = question_data["ordering_items"] or []
            extracted_order = []
            for ordinal in ordinals:
                # Match "First, you must ..." paragraph and find best matching item
                match = re.search(
                    rf"{ordinal},?\s+you must\s+(.+?)(?:\.\s|\.$)",
                    explanation_text
                )
                if match:
                    phrase = match.group(1).strip().lower()
                    # Score each item by word overlap
                    best_item = None
                    best_score = 0
                    for item in items:
                        if item in extracted_order:
                            continue
                        item_words = set(item.lower().split())
                        phrase_words = set(phrase.split())
                        score = len(item_words & phrase_words)
                        if score > best_score:
                            best_score = score
                            best_item = item
                    if best_item:
                        extracted_order.append(best_item)
            if len(extracted_order) == len(items):
                question_data["correct_order"] = extracted_order
            elif extracted_order:
                # Partial match — append remaining items
                for item in items:
                    if item not in extracted_order:
                        extracted_order.append(item)
                question_data["correct_order"] = extracted_order

    return {
        "id": q_id,
        "source_file": filepath.name,
        "title": question_data["title"],
        "type": question_data["type"],
        "select_count": question_data["select_count"],
        "body": question_data["body"],
        "options": question_data["options"],
        "ordering_items": question_data["ordering_items"],
        "correct_answers": correct_answers,
        "correct_order": question_data["correct_order"],
        "explanations": explanations,
        "set": q_set,
    }


def extract_frontmatter(text):
    """Extract YAML frontmatter as a dict of simple key-value pairs."""
    fm = {}
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            for line in text[3:end].split("\n"):
                line = line.strip()
                if ":" in line and not line.startswith("-"):
                    key, _, val = line.partition(":")
                    val = val.strip().strip('"').strip("'")
                    fm[key.strip()] = val
    return fm


def extract_domain_from_title(title):
    """Extract domain number from '(Domain N)' in question title."""
    m = re.search(r"\(Domain\s+(\d)\)", title)
    return int(m.group(1)) if m else None


def extract_task_from_title(title):
    """Extract task number from '(Task X.Y)' in question title."""
    m = re.search(r"\(Task\s+(\d+\.\d+)\)", title)
    return m.group(1) if m else None


# Task keyword classifiers per domain
TASK_KEYWORDS = {
    # Domain 1
    "1.1": ["architect", "design", "poc", "proof of concept", "well-architected", "genai lens", "business require"],
    "1.2": ["model select", "foundation model", "cross-region", "circuit breaker", "fine-tun", "lora", "adapter", "model registry", "appconfig", "model switch"],
    "1.3": ["data valid", "data process", "pipeline", "glue data", "data wrangler", "multimodal", "transcribe", "format input", "json format", "data quality"],
    "1.4": ["vector store", "vector database", "opensearch", "pgvector", "neptune", "s3 vectors", "metadata framework", "sharding", "index optim", "incremental update"],
    "1.5": ["retrieval", "rag", "chunking", "chunk", "embedding", "semantic search", "hybrid search", "reranker", "knowledge base", "query expansion", "query decompos"],
    "1.6": ["prompt engineer", "prompt manage", "prompt flow", "prompt template", "prompt cach", "chain-of-thought", "few-shot", "zero-shot", "prompt govern"],
    # Domain 2
    "2.1": ["agent", "agentcore", "strands", "mcp", "action group", "react pattern", "tool integrat", "human-in-the-loop", "multi-agent", "agent squad"],
    "2.2": ["deploy", "provisioned throughput", "sagemaker endpoint", "container", "gpu", "model cascad", "model loading", "inference endpoint", "on-demand"],
    "2.3": ["enterprise", "ci/cd", "codepipeline", "codebuild", "event-driven", "eventbridge", "legacy system", "outpost", "wavelength", "edge deploy"],
    "2.4": ["api integrat", "invoke model", "converse api", "streaming", "websocket", "server-sent", "exponential backoff", "rate limit", "throttl", "model routing"],
    "2.5": ["amplify", "amazon q developer", "amazon q business", "openapi", "prompt flow", "crm", "developer product"],
    # Domain 3
    "3.1": ["content safety", "guardrail", "harmful", "toxicity", "hallucination", "grounding", "defense-in-depth", "prompt injection", "jailbreak", "adversarial"],
    "3.2": ["vpc endpoint", "privatelink", "iam polic", "lake formation", "pii", "phi", "macie", "data mask", "anonymiz", "encryption", "kms", "data privacy"],
    "3.3": ["model card", "data lineage", "cloudtrail", "audit", "governance board", "compliance framework", "audit manager", "model registry", "soc 2", "hipaa"],
    "3.4": ["responsible ai", "fairness", "bias", "clarify", "transparent", "explainab", "shap", "confidence metric"],
    # Domain 4
    "4.1": ["cost optim", "token efficien", "tiered model", "cost-capability", "caching", "semantic cach", "prompt cach", "batch", "provisioned throughput"],
    "4.2": ["latency", "parallel request", "streaming", "auto-scal", "quantiz", "temperature", "top-k", "top-p", "performance optim", "inference optim"],
    "4.3": ["cloudwatch", "monitoring", "observab", "dashboard", "x-ray", "model invocation log", "anomaly detect", "golden dataset", "vector store monitor"],
    # Domain 5
    "5.1": ["evaluat", "llm-as-a-judge", "a/b test", "rouge", "bleu", "bertscore", "human feedback", "quality gate", "regression test", "agent performance", "task completion"],
    "5.2": ["troubleshoot", "context window overflow", "debug", "error log", "chunking issue", "retrieval issue", "prompt maintenance", "drift monitor"],
}


def classify_task(domain, body, title=""):
    """Classify a question into a task based on keywords."""
    text = (title + " " + body).lower()
    prefix = str(domain) + "."
    best_task = None
    best_score = 0
    for task_id, keywords in TASK_KEYWORDS.items():
        if not task_id.startswith(prefix):
            continue
        score = sum(1 for k in keywords if k in text)
        if score > best_score:
            best_score = score
            best_task = task_id
    return best_task or f"{domain}.1"


def classify_domain(body, title=""):
    """Classify a question into a domain based on keywords in body and title."""
    text = (title + " " + body).lower()

    # Domain 3 signals (check first — governance/security terms overlap with others)
    d3 = ["guardrail", "pii", "phi", "hipaa", "gdpr", "soc 2", "compliance",
           "governance", "bias", "fairness", "audit", "macie", "clarify",
           "model card", "lineage", "prompt injection", "jailbreak", "waf",
           "vpc endpoint", "privatelink", "iam polic", "encryption", "kms",
           "responsible ai", "toxicity", "content filter"]
    if sum(1 for k in d3 if k in text) >= 2:
        return 3

    # Domain 5 signals
    d5 = ["evaluat", "hallucin", "golden dataset", "rouge", "bleu", "bertscore",
           "llm-as-a-judge", "llm as a judge", "a/b test", "regression test",
           "troubleshoot", "debug", "drift detect", "model monitor",
           "quality gate", "x-ray", "xray", "tracing"]
    if sum(1 for k in d5 if k in text) >= 2:
        return 5

    # Domain 4 signals
    d4 = ["cost optim", "token optim", "latency optim", "caching", "semantic cach",
           "provisioned throughput", "batch inference", "auto-scal", "autoscal",
           "quantiz", "int8", "int4", "spot instance", "savings plan",
           "cloudwatch metric", "cloudwatch alarm", "dashboard", "monitor",
           "token usage", "resource utiliz", "capacity plan"]
    if sum(1 for k in d4 if k in text) >= 2:
        return 4

    # Domain 2 signals
    d2 = ["agent", "agentcore", "strands", "mcp", "action group", "lambda",
           "step function", "api gateway", "streaming", "websocket",
           "invoke model", "converse api", "deploy", "endpoint",
           "ci/cd", "codepipeline", "amplify", "amazon q",
           "event-driven", "eventbridge", "orchestrat"]
    if sum(1 for k in d2 if k in text) >= 2:
        return 2

    # Domain 1 signals (default for FM/RAG/data topics)
    d1 = ["foundation model", "rag", "retrieval", "knowledge base", "vector",
           "embedding", "chunking", "opensearch", "pgvector", "aurora",
           "fine-tun", "prompt engineer", "model select", "bedrock",
           "data valid", "data quality", "glue", "cross-region inference"]
    if sum(1 for k in d1 if k in text) >= 2:
        return 1

    return 1  # Default to Domain 1


def parse_generated_file(filepath):
    """Parse a multi-question generated file into a list of question dicts.
    Handles both single-domain files (domain in frontmatter) and multi-domain
    files (domain in question titles via '(Domain N)' pattern).
    """
    text = filepath.read_text(encoding="utf-8")
    fm = extract_frontmatter(text)
    file_domain = int(fm.get("domain", 0))
    file_domain_name = fm.get("domain_name", DOMAIN_NAMES.get(file_domain, ""))
    file_category = fm.get("category", "")

    text = strip_frontmatter(text)

    # Split on ## Question N headers
    chunks = re.split(r"(?=^## Question \d+)", text, flags=re.MULTILINE)
    chunks = [c.strip() for c in chunks if c.strip() and c.strip().startswith("## Question")]

    questions = []
    for i, chunk in enumerate(chunks, 1):
        q_header, q_body, remaining = extract_callout_block(chunk, "question")
        if not q_header:
            print(f"Warning: no question block in {filepath.name} Q{i}")
            continue

        question_data = parse_question_block(q_header, q_body)

        a_header, a_body, _ = extract_callout_block(remaining, "example")
        if not a_header:
            print(f"Warning: no answer block in {filepath.name} Q{i}")
            continue

        correct_answers, explanations = parse_answer_block_practice(a_header, a_body)

        title = question_data["title"]

        # Extract domain: from title tag first, then frontmatter, then classify
        domain = extract_domain_from_title(title)
        if domain is None:
            domain = file_domain if file_domain else classify_domain(question_data["body"], title)
        domain_name = DOMAIN_NAMES.get(domain, file_domain_name)

        # Extract task: from title tag first, then classify by keywords
        task = extract_task_from_title(title)
        if task is None:
            task = classify_task(domain, question_data["body"], title)

        # Strip "(Domain N)" and "(Task X.Y)" from title
        title = re.sub(r"\s*\(Domain\s+\d\)\s*", "", title)
        title = re.sub(r"\s*\(Task\s+\d+\.\d+\)\s*$", "", title)

        # Build ID prefix from category or domain
        prefix = file_category[:6] if file_category else f"d{domain}"
        questions.append({
            "id": f"{prefix}-{i:02d}",
            "source_file": filepath.name,
            "title": title,
            "type": question_data["type"],
            "select_count": question_data["select_count"],
            "body": question_data["body"],
            "options": question_data["options"],
            "ordering_items": question_data["ordering_items"],
            "correct_answers": correct_answers,
            "correct_order": question_data["correct_order"],
            "explanations": explanations,
            "set": "generated",
            "domain": domain,
            "domain_name": domain_name,
            "task": task,
        })

    return questions


def parse_all_questions():
    """Parse all question files, deduplicate, and return sorted list."""
    questions = []
    seen_hashes = set()

    # Single-question files (practice + bonus)
    dirs = [
        (PRACTICE_DIR, "exam-practice-set-*.md"),
        (BONUS_DIR, "exam-bonus-set-*.md"),
    ]

    for directory, pattern in dirs:
        if not directory.exists():
            print(f"Warning: {directory} not found")
            continue
        for filepath in sorted(directory.glob(pattern)):
            q = parse_question_file(filepath)
            if q is None:
                print(f"Warning: could not parse {filepath.name}")
                continue

            # Deduplicate by body hash
            body_hash = hashlib.md5(q["body"][:200].encode()).hexdigest()
            if body_hash in seen_hashes:
                print(f"Skipping duplicate: {filepath.name}")
                continue
            seen_hashes.add(body_hash)

            # Add domain fields (null for BenchPrep questions)
            q["domain"] = None
            q["domain_name"] = None
            questions.append(q)

    # Multi-question generated files — load ALL .md files except _index.md
    if GENERATED_DIR.exists():
        for filepath in sorted(GENERATED_DIR.glob("*.md")):
            if filepath.name == "_index.md":
                continue
            gen_questions = parse_generated_file(filepath)
            added = 0
            for q in gen_questions:
                body_hash = hashlib.md5(q["body"][:200].encode()).hexdigest()
                if body_hash in seen_hashes:
                    continue
                seen_hashes.add(body_hash)
                questions.append(q)
                added += 1
            if gen_questions:
                domains_found = sorted(set(q["domain"] for q in gen_questions if q["domain"]))
                print(f"  {filepath.name}: {added} questions (Domains {domains_found})")

    # Classify BenchPrep questions that have domain=None, and add task to all
    for q in questions:
        if q["domain"] is None:
            q["domain"] = classify_domain(q["body"], q.get("title", ""))
            q["domain_name"] = DOMAIN_NAMES.get(q["domain"], "Unknown")
        if "task" not in q or q.get("task") is None:
            q["task"] = classify_task(q["domain"], q["body"], q.get("title", ""))

    # Interleave questions by task within each domain for balanced sets
    questions = interleave_by_task(questions)

    return questions


def interleave_by_task(questions):
    """Reorder questions so tasks are interleaved within each domain.
    Non-domain questions (domain=None) are appended at the end.
    """
    from collections import defaultdict

    # Group by domain, then by task within domain
    domain_tasks = defaultdict(lambda: defaultdict(list))
    non_domain = []
    for q in questions:
        d = q.get("domain")
        if d is None:
            non_domain.append(q)
        else:
            domain_tasks[d][q.get("task", f"{d}.1")].append(q)

    result = []
    for d in sorted(domain_tasks.keys()):
        tasks = domain_tasks[d]
        task_ids = sorted(tasks.keys())
        # Round-robin across tasks
        task_queues = {t: list(qs) for t, qs in tasks.items()}
        while any(task_queues.values()):
            for t in task_ids:
                if task_queues[t]:
                    result.append(task_queues[t].pop(0))

    result.extend(non_domain)
    return result


# ── HTTP Server ────────────────────────────────────────────────────────────────

QUESTIONS = []


class QuizHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.serve_file(HTML_FILE, "text/html")
        elif self.path.startswith("/api/questions"):
            self.send_json(QUESTIONS)
        elif self.path == "/api/progress":
            if PROGRESS_FILE.exists():
                data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
            else:
                data = {}
            self.send_json(data)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/api/progress":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            PROGRESS_FILE.write_text(body.decode("utf-8"), encoding="utf-8")
            self.send_json({"ok": True})
        else:
            self.send_error(404)

    def serve_file(self, path, content_type):
        try:
            data = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_error(404, f"File not found: {path}")

    def send_json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Quieter logging
        pass


def main():
    global QUESTIONS
    QUESTIONS = parse_all_questions()

    practice_count = sum(1 for q in QUESTIONS if q["set"] == "practice")
    bonus_count = sum(1 for q in QUESTIONS if q["set"] == "bonus")
    generated_count = sum(1 for q in QUESTIONS if q["set"] == "generated")
    print(f"\nLoaded {len(QUESTIONS)} questions ({practice_count} practice, {bonus_count} bonus, {generated_count} generated)")

    # Show domain and task breakdown
    print("\nDomain breakdown:")
    for d in range(1, 6):
        dqs = [q for q in QUESTIONS if q.get("domain") == d]
        tasks = {}
        for q in dqs:
            t = q.get("task", "?")
            tasks[t] = tasks.get(t, 0) + 1
        task_str = ", ".join(f"{t}:{c}" for t, c in sorted(tasks.items()))
        print(f"  Domain {d}: {len(dqs)} questions [{task_str}]")
    unclassified = [q for q in QUESTIONS if q.get("domain") is None]
    if unclassified:
        print(f"  Unclassified: {len(unclassified)} questions")

    server = http.server.HTTPServer(("127.0.0.1", PORT), QuizHandler)
    url = f"http://localhost:{PORT}"
    print(f"\nQuiz running at {url}")
    print("Press Ctrl+C to stop\n")
    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
