# Domain → Source Document Mapping

Maps each AIP-C01 exam domain to the vault source documents that cover its topics. Use this to determine which sources to read when generating questions, and to identify coverage gaps.

## Domain 1: Foundation Model Integration, Data Management, and Compliance (31%)

### Primary Sources
| Source File | Topics Covered |
|---|---|
| `Sources/AWS-Gen-AI/aws-blog-genai-best-practices.md` | FM selection, RAG vs fine-tuning decision tree, prompt engineering (zero/few-shot, CoT, ReAct), agents overview |
| `Sources/AWS-Gen-AI/strategy-enterprise-ready-gen-ai-platform.md` | FM evaluation, Knowledge Bases, RAG architecture, vector storage, enterprise data layer |
| `Sources/AWS-Gen-AI/bedrock-knowledge-bases.md` | RAG, chunking strategies, vector stores, retrieval, RetrieveAndGenerate API |
| `Sources/AWS-Gen-AI/bedrock-prompt-management.md` | Prompt templates, versioning, approval workflows, governance |
| `Sources/Exam-Prep/ai-professional-01.md` (lines 195-320) | Tasks 1.1-1.6 skill definitions |

### Exam Tasks & Key Topics
- Task 1.1: Solution design, proof-of-concept, Well-Architected GenAI Lens
- Task 1.2: FM selection/evaluation, dynamic model switching (AppConfig), cross-region inference, fine-tuning (LoRA)
- Task 1.3: Data validation (Glue Data Quality), multimodal processing, JSON formatting
- Task 1.4: Vector stores (OpenSearch, Aurora pgvector, DynamoDB), metadata frameworks, sharding
- Task 1.5: Chunking, embeddings (Titan), hybrid search, reranking, MCP clients
- Task 1.6: Prompt management, guardrails governance, chain-of-thought, prompt flows

---

## Domain 2: Implementation and Integration (26%)

### Primary Sources
| Source File | Topics Covered |
|---|---|
| `Sources/AWS-Gen-AI/bedrock-agents.md` | Agents, action groups, tool use, orchestration, agent versioning |
| `Sources/AWS-Gen-AI/strategy-enterprise-ready-gen-ai-platform.md` | Enterprise integration, agents, API patterns, CI/CD |
| `Sources/AWS-Gen-AI/gen-ai-inference-architecture-and-best-practices-on-aws.md` | Deployment strategies (serverless/managed/self-managed), inference optimization |
| `Sources/AWS-Core/step-functions-workflows.md` | Standard vs Express workflows, orchestration patterns |
| `Sources/Exam-Prep/ai-professional-01.md` (lines 326-440) | Tasks 2.1-2.5 skill definitions |

### Exam Tasks & Key Topics
- Task 2.1: Agentic AI (Strands, Agent Squad, MCP), ReAct patterns, human-in-the-loop
- Task 2.2: Deployment (Lambda, Bedrock provisioned, SageMaker endpoints), container-based, model cascading
- Task 2.3: Enterprise integration (API Gateway, EventBridge), CI/CD (CodePipeline), GenAI gateway
- Task 2.4: FM APIs (streaming, async/SQS, rate limiting, X-Ray observability), intelligent routing
- Task 2.5: Amplify UI, Amazon Q Business/Developer, Prompt Flows, Strands orchestration

---

## Domain 3: AI Safety, Security, and Governance (20%)

### Primary Sources
| Source File | Topics Covered |
|---|---|
| `Sources/AWS-Gen-AI/bedrock-guardrails.md` | Content filtering, PII, denied topics, prompt attacks, grounding checks |
| `Sources/AWS-Gen-AI/strategy-enterprise-ready-gen-ai-platform.md` | Security controls, IAM, VPC endpoints, Lake Formation, responsible AI, governance |
| `Sources/Exam-Prep/Skill-Builder/skillbuilder-capture-02.md` | VPC endpoints, IAM, Lake Formation scenario |
| `Sources/Exam-Prep/Skill-Builder/skillbuilder-capture-03.md` | PII detection (Comprehend, Macie), S3 lifecycle |
| `Sources/Exam-Prep/ai-professional-01.md` (lines 439-510) | Tasks 3.1-3.4 skill definitions |

### Exam Tasks & Key Topics
- Task 3.1: Input/output safety (guardrails, content moderation), hallucination reduction, prompt injection defense
- Task 3.2: Data security (VPC endpoints, IAM, Lake Formation), PII (Comprehend, Macie), encryption
- Task 3.3: Compliance (model cards, Glue data lineage, CloudTrail audit), governance frameworks
- Task 3.4: Responsible AI (transparency, fairness, A/B testing for bias, automated compliance)

---

## Domain 4: Operational Efficiency and Optimization (12%)

### Primary Sources
| Source File | Topics Covered |
|---|---|
| `Sources/AWS-Gen-AI/gen-ai-inference-architecture-and-best-practices-on-aws.md` | Inference optimization (quantization, pruning, speculative decoding), auto-scaling, instance sizing, cost analysis |
| `Sources/AWS-Gen-AI/bedrock-cloudwatch-metrics.md` | CloudWatch metrics (InvocationLatency, TokenCount, Throttling), monitoring |
| `Sources/Exam-Prep/Skill-Builder/skillbuilder-capture-06.md` | ThrottlingException, provisioned throughput, exponential backoff |
| `Sources/AWS-Gen-AI/strategy-enterprise-ready-gen-ai-platform.md` | Cost optimization strategies, performance monitoring |
| `Sources/Exam-Prep/ai-professional-01.md` (lines 510-580) | Tasks 4.1-4.3 skill definitions |

### Exam Tasks & Key Topics
- Task 4.1: Token optimization, cost-capability tradeoffs, tiered model usage, caching (semantic, prompt, edge)
- Task 4.2: Latency optimization (streaming, parallel requests), retrieval performance, batch inference, parameter tuning
- Task 4.3: Observability (CloudWatch dashboards, business metrics), vector store monitoring, tool performance

---

## Domain 5: Testing, Validation, and Troubleshooting (11%)

### Primary Sources
| Source File | Topics Covered |
|---|---|
| `Sources/AWS-Gen-AI/bedrock-evaluation.md` | Automatic evaluation, human evaluation, LLM-as-judge, built-in metrics |
| `Sources/AWS-Gen-AI/bedrock-cloudwatch-metrics.md` | CloudWatch metrics, anomaly detection, performance benchmarks |
| `Sources/AWS-Core/xray-overview.md` | Distributed tracing, service maps, request analysis |
| `Sources/Exam-Prep/Skill-Builder/skillbuilder-capture-04.md` | FM evaluation framework (custom datasets, A/B testing, business metrics) |
| `Sources/Exam-Prep/Skill-Builder/skillbuilder-capture-06.md` | ThrottlingException troubleshooting, retry strategies |
| `Sources/Exam-Prep/ai-professional-01.md` (lines 583-620) | Tasks 5.1-5.2 skill definitions |

### Exam Tasks & Key Topics
- Task 5.1: Evaluation systems (relevance, accuracy, fluency), A/B testing, canary testing, user feedback, quality gates
- Task 5.2: Troubleshooting (CloudWatch Logs Insights, X-Ray tracing, golden datasets, hallucination detection, response drift)
