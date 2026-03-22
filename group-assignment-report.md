# SamarthSchool: AI-Powered Benefits Navigator for Children with Special Abilities

## Group Assignment Report — Gen AI: Pre-Trained Models (Course 8919)

---

## Elevator Pitch

83.6% of eligible Indian families are unaware of disability welfare schemes their children qualify for, and 42% never apply simply because they don't know. SamarthSchool is a GraphRAG-powered benefits navigator that lets school administrators describe a child's situation in plain language and receive a personalized action plan — matching schemes, required documents, and application steps — in under 5 minutes and in any Indian language. By structuring 50+ government schemes into a machine-queryable Knowledge Graph paired with multilingual RAG, SamarthSchool turns an information asymmetry problem into a navigation problem — and makes every entitled benefit reachable.

---

## 1. Executive Summary

India has over 26.8 million persons with disabilities, yet 83.6% of eligible families are unaware of scholarship schemes available to them, and 42% never apply for government benefits because they don't know the benefits exist. For children with special abilities in schools, this means lost scholarships, unclaimed assistive devices, and missed educational support worth thousands of crores annually.

**SamarthSchool** is a RAG (Retrieval-Augmented Generation) and Knowledge Graph-powered application that lets school administrators find and access government benefits for children with special abilities from a natural language description of the child's needs. The system structures 50+ central and state-level disability schemes into a queryable Knowledge Graph, pairs it with a vector-based RAG pipeline for explanatory content, and responds in the user's preferred Indian language.

The product targets government and private schools, with a hybrid business model combining CSR/grant funding for initial deployment and B2G (Business-to-Government) procurement for scale. Year 1 development cost is estimated at INR 2.1-2.8 crore. With 500 schools by Year 3, the system would help unlock an estimated INR 11 crore in additional benefits for 7,500 children, cutting scheme identification time from hours to minutes.

---

## 2. Problem Definition

### 2.1 The problem in one sentence

Millions of Indian children with special abilities miss out on government benefits they are legally entitled to because schools and families simply don't know these benefits exist.

### 2.2 The disability landscape in India

There is a large gap between disability policy intent and ground reality in India. We use NFHS-5 (2019-21) prevalence data as our planning basis rather than Census 2011 figures because NFHS-5 uses a functional assessment methodology aligned with WHO standards and captures the expanded 21-category disability definition under RPwD Act 2016:

| Metric | Figure | Source |
|--------|--------|--------|
| Total persons with disabilities | 63.3 million (4.52% prevalence, NFHS-5) | NFHS-5 (2019-21) |
| Census 2011 estimate (narrow definition) | 26.8 million (2.21%), likely 2-3x undercounted | Census 2011 |
| Children with disabilities (estimated) | 18–20 million (NFHS-5 prevalence applied to ~450M children) | NFHS-5 extrapolation |
| CWSN enrolled in schools (Class I–XII) | 2.27 million | UDISE+ FY2022 |
| Children with disabilities never in school | 27% of age 5–19 | Census 2011 |
| Persons with disability certificate | Only 28.8% | NSS 76th Round (2018) |
| UDID cards generated vs. eligible | 11 million vs. 26.8 million+ | DEPwD, July 2024 |

The RPwD Act 2016 expanded recognized disability categories from 7 to 21 (including learning disabilities, autism spectrum conditions, and speech/language disabilities), yet many of these newer categories remain under-identified in schools.

### 2.3 The awareness gap

The problem is not a shortage of schemes. India has a large and growing portfolio of disability welfare programs. The problem is that these schemes never reach the children they were designed for:

- **83.6%** of eligible persons are unaware of scholarship schemes for students with disabilities (IJPMR Study, 2025)
- **94.3%** lack knowledge about income tax rebates for disabled persons
- **42%+** of eligible persons do not apply for government benefits because they are unaware the schemes exist (NILERD Study)
- **71.2%** of persons with disabilities lack a disability certificate, which is the prerequisite for accessing almost every central scheme

This is not a marginal problem. The Samagra Shiksha Abhiyan alone allocates Rs 3,500 per CWSN per year for aids, appliances, corrective surgeries, therapeutic services, and stipends. At 2.27 million enrolled CWSN, that is nearly Rs 800 crore in annual allocation. Much of it goes underutilized because schools don't know how to access it.

### 2.4 Why this problem is suited to Gen AI

The disability benefits landscape has several characteristics that make it well-suited to a Gen AI solution:

1. **Unstructured, fragmented information**: Benefits are scattered across 50+ schemes, multiple ministries (DEPwD, Ministry of Education, Ministry of Health, National Trust), 28 states + 8 UTs, and hundreds of PDFs, circulars, and gazette notifications in multiple languages.

2. **Complex eligibility matching**: Each scheme has distinct eligibility criteria involving disability type (21 categories), percentage (40%+ benchmark), age, income, domicile, gender, and institutional requirements. No single human can hold all these intersecting rules in memory.

3. **Natural language interaction need**: School administrators are not policy experts. They need to describe a child's situation in plain language ("We have a 10-year-old girl with hearing impairment in our government school in Tamil Nadu") and receive a personalized list of applicable benefits.

4. **Multilingual requirement**: India's 22 official languages mean that benefit information created in English/Hindi must be accessible to users across linguistic boundaries.

5. **Frequent updates**: Government schemes change through budget revisions, circulars, and amendments. A static database becomes stale within months; an AI pipeline with automated ingestion stays current.

Traditional approaches (static websites, PDF repositories, manual counseling) have failed to close this gap over the past decade. Why existing digital interventions have not worked:

- **MyScheme (myscheme.gov.in)**: India's own rule-based scheme eligibility checker exists and is free. Yet awareness remains below 20% for most schemes. MyScheme is generic (covers all welfare, not disability-specific), requires users to already know they should search, uses form-based UI rather than natural language, and does not integrate into school workflows. It solves the matching problem but not the discovery or guidance problem.
- **UDID Portal**: A registration system, not a navigator. It creates the disability ID but does not tell families what to do with it.
- **Haqdarshak**: A well-funded commercial platform (40M+ users) that helps citizens discover welfare schemes via field agents and app. However, it is not disability-specialized, lacks depth on eligibility criteria for the 21 RPwD categories, and its business model depends on per-transaction fees that may not align with school-level deployment.
- **NGO workshops**: Effective but not scalable. A disability rights workshop reaches 50–100 families; a digital platform reaches thousands.

The difference comes down to framing. Existing solutions treat scheme awareness as a search problem ("find schemes matching criteria"). SamarthSchool treats it as a navigation problem ("given this child's situation, here is everything they are entitled to, how to apply, and what documents to prepare"), which requires the structured reasoning that a Knowledge Graph provides.

### 2.5 Success metrics

| Metric | Baseline (Current) | Target (Year 1) | Target (Year 3) |
|--------|-------------------|------------------|------------------|
| % of pilot schools aware of >10 applicable schemes | <15% | 80% | 95% |
| Benefits accessed per child per year | ~0.3 | 2.0 | 4.0 |
| Time to identify applicable schemes (per child) | 2–5 hours (manual research) | <5 minutes | <2 minutes |
| Scheme coverage in Knowledge Graph (central schemes) | 0% | 100% | 100% |
| Scheme coverage (state schemes, top 10 states) | 0% | 50% | 90% |
| User satisfaction (school administrators) | N/A | >4.0/5.0 | >4.5/5.0 |

---

## 3. Vision & Mission

**Vision**: An India where every child with special abilities receives every government benefit they are entitled to, accurately and in their own language.

**Mission**: Build an AI-powered benefits navigator that lets school administrators find and access disability welfare schemes for their students in under 5 minutes, replacing hours of manual research across fragmented government portals.

**Product Name**: **SamarthSchool** (समर्थ स्कूल). "Samarth" (समर्थ) means capable or empowered in Hindi — the name reflects the goal of empowering both schools and children with the information they need to claim their entitlements.

**What SamarthSchool is NOT**: It is not a disability registration portal (that is UDID), not a generic welfare scheme finder (that is MyScheme), and not a benefits-delivery platform. It is a disability-specific benefits *navigator* designed for school administrators — it bridges the gap between policy intent and ground-level awareness by combining structured Knowledge Graph reasoning with natural language access in Indian languages.

---

## 4. Gen AI solution design

### 4.1 Why RAG + Knowledge Graph (not RAG alone)

A standard RAG pipeline retrieves relevant text chunks and generates answers. For a benefits-awareness application, this is insufficient:

**Consider this query**: "I have a 12-year-old boy with 50% locomotor disability in a government school in Karnataka. Family income is Rs 1.5 lakh per year. What benefits is he eligible for?"

- **RAG alone** retrieves chunks mentioning some of these criteria but cannot systematically intersect all constraints (disability type + percentage + age + state + income + school type) across 50+ schemes. It may miss schemes or hallucinate eligibility.

- **RAG + Knowledge Graph** first runs a structured graph query filtering by disability_category=locomotor, percentage>=40, state=Karnataka OR all_india, income<=250000, age_range includes 12, and returns exact matching schemes. The RAG layer then provides natural-language explanations of each matched scheme, application process, and required documents.

This hybrid approach is called GraphRAG: structured reasoning via the Knowledge Graph, with natural-language generation via RAG on top.

### 4.2 Architecture overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA INGESTION LAYER                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ Web      │  │ PDF      │  │ Gazette  │  │ Manual Curation   │  │
│  │ Crawler  │  │ Parser   │  │ RSS      │  │ (scheme metadata) │  │
│  │ (Scrapy) │  │ (Docling │  │ Monitor  │  │                   │  │
│  │          │  │ + Surya) │  │          │  │                   │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬──────────┘  │
│       └──────────────┴──────────────┴────────────────┘              │
│                              │                                      │
│                    ┌─────────▼──────────┐                           │
│                    │  Processing        │                           │
│                    │  - Chunk (hybrid   │                           │
│                    │    semantic +      │                           │
│                    │    structural)     │                           │
│                    │  - Embed (bge-m3)  │                           │
│                    │  - Extract KG      │                           │
│                    │    triples (LLM)   │                           │
│                    └─────────┬──────────┘                           │
│                              │                                      │
│                    ┌─────────▼──────────┐                           │
│                    │  Version & Diff    │                           │
│                    │  (SHA-256 hash,    │                           │
│                    │   update changed   │                           │
│                    │   sections only)   │                           │
│                    └─────────┬──────────┘                           │
└──────────────────────────────┼──────────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   STORAGE LAYER     │
                    │  ┌───────────────┐  │
                    │  │ Qdrant        │  │
                    │  │ (vectors +    │  │
                    │  │  metadata)    │  │
                    │  └───────────────┘  │
                    │  ┌───────────────┐  │
                    │  │ Neo4j         │  │
                    │  │ (scheme graph │  │
                    │  │  + eligibility│  │
                    │  │  rules)       │  │
                    │  └───────────────┘  │
                    │  ┌───────────────┐  │
                    │  │ PostgreSQL    │  │
                    │  │ (user data,   │  │
                    │  │  audit logs)  │  │
                    │  └───────────────┘  │
                    └──────────┬──────────┘
                               │
┌──────────────────────────────┼──────────────────────────────────────┐
│                    QUERY LAYER                                      │
│                    ┌─────────▼──────────┐                           │
│                    │  Query Router      │                           │
│                    │  (classify intent: │                           │
│                    │   eligibility /    │                           │
│                    │   explanation /    │                           │
│                    │   process guide)   │                           │
│                    └─────────┬──────────┘                           │
│                              │                                      │
│              ┌───────────────┼───────────────┐                      │
│              ▼               ▼               ▼                      │
│      ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│      │ KG Query │    │ Vector   │    │ Hybrid   │                  │
│      │ (Cypher) │    │ Search   │    │ (both)   │                  │
│      │ Eligibi- │    │ Explana- │    │ Complex  │                  │
│      │ lity     │    │ tory     │    │ queries  │                  │
│      └────┬─────┘    └────┬─────┘    └────┬─────┘                  │
│           └───────────────┴───────────────┘                         │
│                           │                                         │
│                 ┌─────────▼──────────┐                              │
│                 │  Response          │                              │
│                 │  Generation        │                              │
│                 │  (Gemini 2.0 Flash │                              │
│                 │   / Qwen 2.5)      │                              │
│                 │  in user's lang    │                              │
│                 └─────────┬──────────┘                              │
│                           │                                         │
│                 ┌─────────▼──────────┐                              │
│                 │  Citation +        │                              │
│                 │  Confidence Score  │                              │
│                 │  + Disclaimer      │                              │
│                 └────────────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.3 Technology stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **PDF Parsing** | Docling (IBM, open-source) + Surya OCR (AI4Bharat) | Docling handles structured government PDFs with table extraction; Surya provides best-in-class OCR for Devanagari and 10+ Indian scripts |
| **Chunking** | Semantic + Structural Hybrid | Government documents follow section/clause hierarchy (2.1, 2.1.1); chunks target 512–768 tokens with metadata enrichment per chunk |
| **Embedding Model** | BAAI/bge-m3 (1024 dimensions) | Supports dense + sparse hybrid retrieval (critical for exact scheme name matching alongside semantic search); multilingual across Hindi, Tamil, Bengali, etc. |
| **Vector Database** | Qdrant (self-hosted) | First-class sparse vector support for bge-m3; payload-based metadata filtering (scheme_name, state, disability_category); runs on 4GB RAM |
| **Knowledge Graph DB** | Neo4j Community Edition 5.x (production target); Kùzu (MVP prototype) | Mature Cypher query language; natural fit for scheme→eligibility→disability entity relationships; AuraDB free tier for prototyping. MVP uses Kùzu for its embedded, zero-config design suitable for single-machine deployment |
| **LLM (Primary)** | Google Gemini 2.0 Flash (paid tier) | Good Hindi generation; lowest cost-per-token among frontier models (~$0.075/1M input); free tier for prototyping only, paid tier budgeted for production (see Section 6.2 unit economics) |
| **LLM (Complex Reasoning)** | Gemini 2.5 Pro / DeepSeek-R1 | Multi-step eligibility determination requiring intersection of 5+ criteria |
| **LLM (Self-hosted Fallback)** | Qwen 2.5 14B (quantized) | For fully offline/air-gapped deployments in schools without reliable internet |
| **Framework** | LlamaIndex (PropertyGraphIndex) | Native GraphRAG support; integrates Qdrant + Neo4j; clean ingestion pipeline for document updates |
| **Multilingual** | IndicTrans2 + IndicXlit (AI4Bharat) | Translation across 22 Indian languages; Romanized-to-Devanagari transliteration for users typing Hindi in English script |
| **Language Detection** | fastText lid.176 | Lightweight, supports 176 languages including all Indian languages |
| **Frontend** | React + Next.js (responsive, accessible) | WCAG 2.1 AA compliant; screen reader compatible; mobile-first for school administrators on phones |

### 4.4 Knowledge Graph schema

The Knowledge Graph models the structural relationships between schemes, eligibility criteria, disability categories, and benefits:

**Entities:**

| Entity | Key Properties |
|--------|---------------|
| `Scheme` | name, ministry, level (central/state), status, effective_date, budget_allocation |
| `EligibilityCriterion` | criterion_type (age/income/disability_%/domicile/gender), operator (>=, <=, in), value |
| `Benefit` | type (financial/assistive_device/scholarship/training), amount, frequency |
| `DisabilityCategory` | name (one of 21 per RPwD 2016), benchmark_percentage |
| `Document` | name, type (disability_certificate/income_cert/Aadhaar), issuing_authority |
| `ApplicationProcess` | mode (online/offline), portal_url, processing_time |
| `GovBody` | name, level, jurisdiction |

**Key Relationships:**

```
(Scheme)-[:HAS_ELIGIBILITY]->(EligibilityCriterion)
(Scheme)-[:PROVIDES]->(Benefit)
(Scheme)-[:REQUIRES_DOC]->(Document)
(Scheme)-[:ADMINISTERED_BY]->(GovBody)
(Scheme)-[:APPLICABLE_IN]->(State)
(EligibilityCriterion)-[:APPLIES_TO_CATEGORY]->(DisabilityCategory)
(Person)-[:HAS_DISABILITY]->(DisabilityCategory)
(Person)-[:RESIDES_IN]->(State)
```

**Sample Cypher Query** (for the Karnataka example above):

```cypher
MATCH (s:Scheme)-[:HAS_ELIGIBILITY]->(e:EligibilityCriterion),
      (s)-[:APPLICABLE_IN]->(st:State),
      (e)-[:APPLIES_TO_CATEGORY]->(d:DisabilityCategory)
WHERE d.name = 'Locomotor Disability'
  AND (st.name = 'Karnataka' OR st.name = 'All India')
  AND e.income_limit >= 150000
  AND e.min_disability_pct <= 50
  AND e.age_min <= 12 AND e.age_max >= 12
RETURN s.name, s.ministry, s.benefits
```

### 4.5 Multilingual pipeline

```
User Query (any language) → Language Detection (fastText)
    → [If non-English] Translate to English for KG query (IndicTrans2)
    → Keep original for vector search (bge-m3 cross-lingual)
    → KG Query (English Cypher) + Vector Search (original language)
    → Merge results
    → Generate response in user's detected language (Gemini Flash)
    → Include source citations and disclaimer
```

Design decisions worth noting:
- **Cross-lingual retrieval**: bge-m3 maps Hindi and English into the same embedding space, so a Hindi query retrieves English document chunks without explicit translation
- **Transliteration**: IndicXlit handles users typing Hindi in Roman script ("viklang pension yojana" → "विकलांग पेंशन योजना")
- **KG labels**: Stored in both English and Hindi for direct querying in either language

### 4.6 Data ingestion and update pipeline

Government schemes change through budget revisions, circulars, and amendments. The system maintains freshness through:

1. **Scheduled crawling**: Weekly scrapes of DEPwD, MyScheme, state portals; daily RSS monitoring of egazette.gov.in
2. **Change detection**: SHA-256 hash comparison; only re-process changed documents
3. **Versioned chunks**: Old versions retained with timestamps; queries always return current data
4. **Manual curation overlay**: Domain experts validate KG entries before they go live; incorrect eligibility criteria in the KG are worse than no system at all

### 4.7 Evaluation methodology

| Category | Metric | Target | Tool |
|----------|--------|--------|------|
| **Retrieval** | Recall@10 | >0.85 | RAGAS |
| **Retrieval** | Precision@5 | >0.70 | RAGAS |
| **Answer** | Faithfulness (no hallucination) | >0.90 | RAGAS faithfulness |
| **Answer** | Correctness | >0.85 | RAGAS + human eval |
| **Domain** | Eligibility Accuracy (50+ synthetic personas) | >90% | Custom test suite |
| **Domain** | Scheme Coverage (central schemes) | 100% | Manual audit |
| **Domain** | Harmful Misinformation Rate | <2% | Human audit (critical) |
| **Domain** | Language Parity (Hindi vs English) | <10% degradation | A/B evaluation |
| **UX** | Query-to-Answer Latency | p50 <3s, p95 <8s | Monitoring |
| **UX** | User Satisfaction | >4.0/5.0 | In-app survey |

The evaluation process uses a gold-standard test set of 200+ query-answer pairs validated by disability rights advocates, supplemented with 500+ real-world queries collected during pilot. Automated RAGAS evaluation runs on every KG/document update, and human audit is conducted quarterly.

MyScheme's rule-based matching is the baseline. If human disability counselors achieve ~80% accuracy on complex multi-criteria eligibility (field studies show counselors frequently miss obscure schemes or apply wrong income thresholds), the 90% target represents an improvement that must be validated empirically during MVP, not assumed.

### 4.8 Failure modes and mitigation

| Failure Mode | Impact | Mitigation |
|---|---|---|
| **KG has no match** (rare disability, new scheme not yet ingested) | User gets empty result; loses trust | Fall back to RAG-only search with explicit disclaimer: "No exact match found in our database. Here are potentially relevant schemes. Please verify with your DDRC." |
| **LLM hallucinates a scheme** (claims eligibility for non-existent or wrong scheme) | Family wastes time, documents, money; false hope | Every response is grounded in KG results, not free LLM generation. If a scheme isn't in the KG, it cannot appear in the response. RAG answers carry source citations and confidence scores. |
| **OCR misparses a PDF** (wrong income threshold, wrong disability percentage) | Incorrect eligibility determination | Dual-validation: automated parsing + mandatory human expert review before KG entries go live. No automatically-parsed data enters the KG without human sign-off. |
| **Stale data** (scheme modified but KG not updated) | Outdated information presented as current | Every response includes "Data last verified: [date]" timestamp. Chunks older than 6 months trigger review alerts. Users can flag outdated information. |
| **LLM routing error** (eligibility query sent to RAG instead of KG) | Less accurate results | Intent classification confidence threshold: if <0.8, route to hybrid (both KG + RAG) rather than risk misrouting. |

For eligibility determinations, the system is advisory, not authoritative. Every response includes: *"This is an AI-generated recommendation based on our database as of [date]. Please verify eligibility with your local DDRC or the official scheme portal before applying. SamarthSchool does not make official eligibility determinations."*

### 4.9 Ethical considerations

**Algorithmic bias**: The system could systematically under-identify eligibility for disability categories that are harder to describe in natural language (e.g., intellectual disabilities, specific learning disabilities). To mitigate this, evaluation includes a fairness audit across all 21 RPwD categories with per-category accuracy targets.

**Consent and agency**: School administrators querying on behalf of children raises questions about data agency. The system stores no child-level PII by default. Queries are stateless: the administrator enters details, gets results, and nothing is retained. If a school opts into tracking for analytics, verifiable parental consent is required per DPDP Act Section 9.

**Digital divide risk**: Schools with low digital literacy, the ones that most need this tool, may be least likely to adopt it. The WhatsApp interface (Phase 3) lowers the technology barrier. Pilot design explicitly includes rural government schools, not just urban private schools.

**Dependency risk**: If the product shuts down, schools that relied on it lose access. The Knowledge Graph data is designed to be exportable, and the open API (Phase 4) ensures the data layer is not locked into the product.

**Data sensitivity**: Disability type, income, and location of children is sensitive data even in aggregate. No PII is stored at rest; queries are processed in-memory and discarded. Audit logs retain query patterns for quality improvement but not child-identifying details.

### 4.10 Knowledge Graph construction and validation

Building the KG is the highest-risk, highest-effort component. Government eligibility rules use complex conditional language ("eligible if the applicant belongs to SC/ST category AND has a disability certificate AND family income does not exceed Rs 2.5 lakh per annum OR Rs 3.5 lakh in case of OBC category"). Automated triple extraction from such text is error-prone.

The initial KG for 50+ central schemes is manually curated, not auto-extracted. A domain expert (disability rights specialist) structures each scheme's eligibility criteria, benefits, and documents directly into the Neo4j schema. LLM-based extraction is used only for draft generation that the domain expert then validates.

For ongoing maintenance, each scheme entry has an "owner" (the domain expert responsible for keeping it current). Scheme changes detected by the crawling pipeline generate alerts for the owner to review and update. The cost of this ongoing KG maintenance is budgeted at INR 8-12 lakh per year (Section 6.2).

**Validation protocol**: Before any KG entry goes live:
1. Automated consistency check (eligibility criteria completeness, valid disability category references)
2. Cross-reference against official scheme document (source URL linked to every KG node)
3. Domain expert sign-off
4. Test with 5+ synthetic personas per scheme to verify correct matching

### 4.11 Human-in-the-loop workflow

SamarthSchool is designed as an advisory system, not an autonomous one. Human judgment is embedded at three levels:

**Level 1 — Knowledge Graph Construction (pre-query)**
Every scheme entry is validated by a disability domain expert before going live. LLM-assisted extraction produces draft KG triples from government documents, but no triple enters the production graph without human sign-off (see validation protocol above). This is the highest-stakes human review: an incorrect eligibility rule in the KG is worse than having no system at all, because it creates false confidence.

**Level 2 — Query Review (during use)**
School administrators review the AI-generated recommendations before taking any action. The system presents matching schemes with citations and confidence scores, but explicitly labels every response as advisory: *"This is an AI-generated recommendation. Please verify with your local DDRC or official scheme portal before applying."* The administrator decides which schemes to pursue, gathers documents, and initiates applications. SamarthSchool does not auto-fill forms or submit applications on behalf of users — that would carry regulatory and liability risk.

**Level 3 — Feedback and Quality Improvement (post-query)**
Administrators can flag responses as incorrect, outdated, or incomplete via an in-app feedback mechanism. Flagged responses trigger alerts to the domain expert for review and KG correction. This creates a continuous improvement loop: real-world usage reveals gaps in the Knowledge Graph that synthetic testing alone cannot catch. Quarterly audits review a random sample of queries and responses to measure accuracy trends and identify systematic issues (e.g., an entire category of state schemes being missed).

This three-level human-in-the-loop design ensures that the system augments human expertise rather than replacing it. The key principle: SamarthSchool makes the administrator's job faster, not unnecessary.

---

## 5. Product roadmap

### 5.1 Phased development plan

#### Phase 1: MVP (Months 0–3)

**Objective**: Prove that GraphRAG can accurately match children to eligible schemes.

| Deliverable | Details |
|-------------|---------|
| Knowledge Graph (Central schemes) | All 50+ central government disability schemes structured in Neo4j |
| RAG pipeline (English + Hindi) | Docling parsing → bge-m3 embeddings → Qdrant → Gemini Flash generation |
| Basic web interface | Simple form: enter child details → get matching schemes with explanations |
| Evaluation suite | 200+ test personas; RAGAS automated evaluation; >85% eligibility accuracy |
| Pilot deployment | 5 schools in 1 city (mix of government and private) |

**Tech stack**: LlamaIndex + Neo4j AuraDB Free + Qdrant (single node) + Gemini Flash free tier

**Risk**: Government PDF parsing accuracy for scanned documents
**Mitigation**: Use Surya OCR + manual verification for initial corpus; build correction feedback loop

#### Phase 2: Beta (Months 3–6)

**Objective**: Add state-level schemes and multilingual support; expand pilot.

| Deliverable | Details |
|-------------|---------|
| State schemes (top 5 states) | Maharashtra, Karnataka, Tamil Nadu, Delhi, Rajasthan |
| Multilingual support | Hindi, Tamil, Kannada, Marathi (via IndicTrans2 + Gemini Flash) |
| Application guidance module | Step-by-step instructions for each scheme: required documents, portal URLs, process |
| Document checklist generator | Based on matched schemes, generate personalized document preparation list |
| Expanded pilot | 25 schools across 3 cities |
| User feedback loop | In-app feedback → retraining pipeline; flag incorrect/outdated information |

**Risk**: State-level scheme data is inconsistent and poorly digitized
**Mitigation**: Partner with state-level disability NGOs for data curation; use RTI requests for missing data

#### Phase 3: v1.0 Production (Months 6–12)

**Objective**: Production-grade deployment with compliance, accessibility, and analytics.

| Deliverable | Details |
|-------------|---------|
| State schemes (top 10 states) | Cover 80%+ of India's school-age PwD population |
| DPDP Act compliance | Parental consent mechanism; data minimization; no profiling of children |
| WCAG 2.1 AA + GIGW 3.0 | Full accessibility compliance; screen reader support; keyboard navigation |
| Analytics dashboard | Per-school: schemes discovered, applications initiated, benefits accessed |
| Offline mode | District-hub deployment: Qwen 2.5 14B on a district education office server (not individual school hardware); schools connect via local network or pre-cached responses |
| WhatsApp integration | Chatbot interface via WhatsApp Business API (India's most-used messaging app) |
| Deployment | 100+ schools across 5 states |

**Risk**: DPDP Act compliance for children's data (penalty up to INR 150 crore)
**Mitigation**: Privacy-by-design architecture; hire data protection consultant; minimize PII storage

#### Phase 4: Scale (Years 1–3)

**Objective**: National scale via government procurement; sustainability.

| Deliverable | Details |
|-------------|---------|
| All 28 states + 8 UTs | Complete national scheme coverage |
| B2G integration | Integrate with UDID portal, Samagra Shiksha MIS, state education department systems |
| Agentic workflows (exploratory) | Application status tracking and document reminders. Note: auto-filling government forms carries regulatory and liability risk and requires a separate feasibility assessment before implementation |
| CSR/NGO partnership portal | Dashboard for CSR funders to track impact metrics |
| Knowledge Graph API | Open API for researchers, NGOs, and other applications to query the scheme graph |
| Bhashini integration | Use India's national language translation platform for 22-language support |
| Target | 10,000+ schools; 500,000+ children served |

**Risk**: Government procurement cycles (12–24 months)
**Mitigation**: Parallel CSR funding track; build evidence base during pilot for procurement justification

### 5.2 Roadmap timeline

```
Month:  0    3    6    9    12        24        36
        |----|----|----|----|---------|---------|
        MVP   Beta  v1.0 Prod        Scale

        5     25   100  schools      10,000+
        schools                       schools

        Central  +5 States  +10 States  All India
        Schemes

        EN+HI   +4 langs   +GIGW     22 langs
                             compliance
```

### 5.3 Adoption strategy

The question we need to answer: why would schools adopt this when MyScheme exists for free?

1. **Go through existing relationships, not cold outreach**: Partner with Samagra Shiksha Abhiyan's existing CWSN coordinator network. Every district has a CWSN coordinator under Samagra Shiksha whose explicit job is to ensure children with disabilities access entitlements. SamarthSchool becomes their tool, not the school administrator's burden. This works because CWSN coordinators are already measured on benefit uptake.

2. **NGO amplification**: Disability rights NGOs (Samarthanam Trust, CBM India, Sense International India) already conduct school outreach programs. SamarthSchool becomes a tool they use during school visits rather than a standalone product schools must discover on their own.

3. **Demonstrated value in pilot**: The 5-school MVP is designed to generate before/after evidence. "Before SamarthSchool, this school's 20 CWSN accessed 6 total benefits; after, they accessed 38." That kind of evidence is what makes the case for scaling.

4. **WhatsApp-first interface**: India has 500M+ WhatsApp users. A WhatsApp chatbot eliminates the app installation barrier. A CWSN coordinator can query on behalf of multiple schools from their phone.

5. **Why SamarthSchool over MyScheme**: MyScheme requires the user to know which category to search, answer 15+ form fields, and interpret results. SamarthSchool lets you describe the child's situation in natural language and get a complete action plan. That user experience difference is what drives adoption.

### 5.4 Team composition

| Role | Count | Phase | Key Skills |
|------|-------|-------|------------|
| ML Engineer (RAG/KG specialist) | 2 | All | LlamaIndex, Neo4j, embedding models, RAG evaluation |
| Full-Stack Developer | 1 | All | Next.js, WCAG accessibility, WhatsApp API integration |
| Disability Domain Expert | 1 | All | Indian disability law, scheme knowledge, NGO network |
| Policy Researcher / KG Curator | 1 | All | Government document analysis, KG data entry and validation |
| Product Manager | 1 | Phase 2+ | User research, pilot management, government relationship building |
| DevOps / Infrastructure | 0.5 (part-time) | Phase 2+ | Qdrant, Neo4j, cloud deployment, monitoring |

---

## 6. ROI Analysis

### 6.1 Assumptions used

| Assumption | Value | Basis |
|-----------|-------|-------|
| Pilot schools (Year 1) | 50 | Conservative target for v1.0 (reduced from 100 to reflect realistic onboarding capacity) |
| CWSN per school (average) | 15 | UDISE+ data: ~2.27M CWSN across ~1.5M schools |
| Benefits accessed per child currently | 0.3 per year | Based on 28.8% certification rate and awareness data |
| Benefits accessed with SamarthSchool | 2.0 per year | Conservative target; MVP data will validate |
| Average monetary value per benefit accessed | Rs 3,200 per year | **Derived weighted average** (see breakdown below) |
| Schools (Year 2) | 200 | NGO partner expansion + early B2G pilots |
| Schools (Year 3) | 500 | B2G contracts in 2-3 states (conservative; government procurement takes 12-24 months) |

The benefit value of Rs 3,200 is derived from actual scheme amounts, not asserted:

| Benefit Type | Annual Value | Likelihood of Access | Weighted Value |
|---|---|---|---|
| Samagra Shiksha per-child allocation | Rs 3,500 | High (school-initiated) | Rs 2,800 |
| Pre-Matric Scholarship (day scholar) | Rs 6,000 + Rs 1,000 books | Medium (requires NSP application) | Rs 2,800 |
| ADIP assistive devices | Rs 15,000 (once per 3 years = Rs 5,000/yr amortized) | Low (camp-based, limited slots) | Rs 1,000 |
| Niramaya Health Insurance | Rs 250–500 premium for Rs 1 lakh cover | Low (very obscure) | Rs 200 |
| State-specific scholarships | Rs 2,000–7,000 | Medium | Rs 2,000 |
| **Weighted average per benefit accessed** | | | **~Rs 3,200** |

A note on what "benefits accessed" means here: the family has been informed of eligibility and guided through the application process. It does not mean the government has disbursed funds, since disbursement timelines are outside the system's control. The ROI measures the value of benefits *applied for with correct documentation*, not benefits received.

### 6.2 Cost structure (3-year projection)

| Cost Category | Year 1 | Year 2 | Year 3 |
|--------------|--------|--------|--------|
| **Development Team** (5.5 FTEs, see Section 5.4) | INR 1.8 Cr ($216K) | INR 2.0 Cr ($240K) | INR 2.0 Cr ($240K) |
| **LLM API Costs** | INR 3 L ($3.6K) | INR 8 L ($9.6K) | INR 20 L ($24K) |
| **Infrastructure** (Qdrant, Neo4j, PostgreSQL, hosting) | INR 8 L ($9.6K) | INR 15 L ($18K) | INR 25 L ($30K) |
| **Knowledge Base Maintenance** (domain expert time) | INR 8 L ($10K) | INR 10 L ($12K) | INR 12 L ($15K) |
| **Compliance & Audit** (DPDP, GIGW, accessibility) | INR 5 L ($6K) | INR 3 L ($4K) | INR 3 L ($4K) |
| **WhatsApp Business API** | INR 0 | INR 2 L ($2.4K) | INR 5 L ($6K) |
| **Travel & Pilot Operations** | INR 5 L ($6K) | INR 8 L ($10K) | INR 10 L ($12K) |
| **Total Cost** | **INR 2.09 Cr ($251K)** | **INR 2.46 Cr ($296K)** | **INR 2.75 Cr ($331K)** |

Per-query unit economics (Year 1 estimates):
- LLM tokens per query: ~2,000 (input: 1,500 context + prompt; output: 500 response)
- Embedding cost per query: negligible (self-hosted bge-m3)
- Neo4j query: negligible (self-hosted, sub-millisecond)
- Gemini 2.0 Flash paid tier: ~$0.075/1M input tokens, $0.30/1M output tokens
- **Cost per query: ~Rs 0.25 ($0.003)**
- At 50 schools × 10 queries/day × 250 days = 125,000 queries/year = INR 31,250 in LLM costs (well within budget)

Salary assumptions (market rates for Bangalore/Delhi NCR, 2026):
- ML Engineer (3-5 yrs): INR 30-40 LPA
- Full-Stack Developer: INR 20-28 LPA
- Domain Expert (disability policy): INR 12-18 LPA
- Policy Researcher/KG Curator: INR 10-15 LPA
- Product Manager: INR 22-30 LPA

### 6.3 Social impact ROI

| Impact Metric | Year 1 | Year 2 | Year 3 |
|--------------|--------|--------|--------|
| Schools served | 50 | 200 | 500 |
| Children impacted | 750 | 3,000 | 7,500 |
| Additional benefits accessed per child | 1.7 | 2.0 | 2.5 |
| Total additional benefit applications | 1,275 | 6,000 | 18,750 |
| Estimated value of benefits applied for | INR 41 L | INR 1.92 Cr | INR 6.0 Cr |
| **Social ROI** (value applied for ÷ cost) | **0.20x** | **0.78x** | **2.2x** |

Year 1 social ROI below 1.0x is expected because the investment goes toward building the platform and KG, not maximizing throughput. The system becomes ROI-positive in social terms by mid-Year 3. These numbers use the conservative benefit value (Rs 3,200) and assume not all applications result in disbursement.

### 6.4 Financial revenue model

| Revenue Stream | Year 1 | Year 2 | Year 3 |
|---------------|--------|--------|--------|
| CSR grants (pilot funding) | INR 1.5 Cr | INR 1.0 Cr | INR 0.5 Cr |
| B2G contracts (state education depts) | INR 0 | INR 0 | INR 1.0 Cr |
| NGO/Development org grants (UNICEF, World Bank) | INR 0 | INR 50 L | INR 50 L |
| Impact investment (Series Seed) | INR 0 | INR 1.5 Cr | INR 0 |
| **Total Revenue/Funding** | **INR 1.5 Cr** | **INR 3.0 Cr** | **INR 2.0 Cr** |
| **Net Position** | **-INR 59 L** | **+INR 54 L** | **-INR 75 L** |

Potential CSR partners, based on their existing disability/education programs:
- Tata Trusts / TCS Foundation: Long-standing education programs; INR 800+ Cr annual CSR; disability is a Schedule VII activity
- Infosys Foundation: Education and rural development focus; typical grant INR 50L–2Cr
- Wipro Foundation / Wipro Cares: Inclusive education programs with NGO partners

CSR grants require 3-6 months of relationship building and proposal development, so Year 1 CSR of INR 1.5 Cr is achievable only if fundraising begins before development. The net-negative position in Years 1 and 3 means the product needs sustained impact investment. It is not self-sustaining on revenue alone within 3 years, which is typical for social impact ventures.

### 6.5 Break-even analysis

- Break-even is not achieved within 3 years on revenue alone. Cumulative deficit: ~INR 80 lakh.
- The path to sustainability runs through B2G contracts (target: Year 3-4 with 2-3 state education departments at INR 50L-1Cr each).
- If B2G is delayed, CSR funding renewal (typical cycle: 3-year grants) plus development grants from UNICEF/World Bank disability programs provide a 5-year runway.
- The make-or-break milestone is MVP pilot evidence. The 5-school before/after data must be compelling enough to secure Year 2 impact investment. Without it, the project does not survive past Year 1.

### 6.6 Sensitivity analysis

| Scenario | Schools (Y3) | Benefits/Child | Revenue (Y3) | Net Position (Y3) |
|----------|-------------|---------------|---------------|-------------------|
| **Pessimistic** (50% adoption, no B2G) | 250 | 1.5 | INR 1.0 Cr | -INR 1.75 Cr |
| **Base case** | 500 | 2.5 | INR 2.0 Cr | -INR 0.75 Cr |
| **Optimistic** (B2G in Year 2, strong CSR) | 1,000 | 3.0 | INR 4.0 Cr | +INR 1.25 Cr |

The pessimistic scenario is survivable with continued CSR/grant funding but requires cost reduction (smaller team, reduced scope). The optimistic scenario achieves profitability. The base case requires external funding for 4-5 years, which is consistent with social venture norms. Haqdarshak, for comparison, operated on grant/impact funding for 5+ years before reaching financial sustainability.

### 6.7 Comparison to status quo

| Metric | Without SamarthSchool | With SamarthSchool |
|--------|----------------------|-------------------|
| Time to identify schemes per child | 2–5 hours (manual research across portals) | <5 minutes |
| Schemes identified per search | 2–3 (commonly known ones only) | 8–12 (including obscure schemes like Niramaya, Top Class Education) |
| Accuracy of eligibility matching | Variable (human counselor: ~80%, depends on expertise) | >90% target (KG-verified; to be validated in MVP) |
| Language accessibility | English/Hindi only | 4+ Indian languages (Year 1), 10+ (Year 2) |
| Update frequency | Annual (if at all) | Weekly (automated crawling + manual KG validation) |
| Cost per child served | Rs 500–1,000 (counselor time) | Rs 50–100 (marginal cost at scale) |

---

## 7. Competitive landscape and unique aspects

### 7.1 Existing solutions and their gaps

| Solution | What It Does | What It Lacks |
|----------|-------------|---------------|
| **MyScheme (myscheme.gov.in)** | Rule-based scheme eligibility checker | No AI; no multilingual NL interface; generic (not disability-focused); no school context |
| **UDID Portal** | Disability identification and registration | Not a benefits navigator; users must already know schemes exist |
| **Haqdarshak** | Welfare scheme discovery for citizens (40M+ users, deep government partnerships, field agent model) | Generic across all welfare; not disability-specialized; eligibility matching lacks depth for 21 RPwD categories; per-transaction fee model may not align with school budgets; no Knowledge Graph for structured reasoning |
| **Sugamya Bharat App** | Accessibility auditing | Physical accessibility focus; not benefits navigation |
| **State Disability Portals** | State-specific scheme information | Fragmented; no cross-state search; no AI; often outdated |
| **NGO Listings** | Static scheme listings | Not personalized; no eligibility matching; not updated |

None of the existing solutions combine a disability-specific Knowledge Graph, AI-powered personalized eligibility matching, multilingual natural language interface, and school-administrator-centric design. That gap is what SamarthSchool targets.

### 7.2 What makes SamarthSchool different

#### Novel domain application (patent potential)

The underlying techniques (GraphRAG, multilingual embeddings, Knowledge Graphs) are established; GraphRAG was published by Microsoft Research in 2024. The novelty is in the specific domain application and the structured Knowledge Graph of Indian disability schemes, which does not exist in any machine-queryable form today. Specifically:

- **First structured, machine-queryable ontology of Indian disability welfare schemes**: Encoding 50+ schemes with eligibility rules as graph-traversable entities is a novel dataset contribution
- **Hybrid query routing for policy eligibility**: Classifying user intent to route between structured graph queries (eligibility) and unstructured vector search (explanatory content), tuned for Indian government policy language
- **Cross-lingual eligibility matching for low-resource Indian languages**: Using multilingual embeddings for retrieval while maintaining an English-language KG for structured queries, with transliteration handling for Romanized Hindi input

A provisional patent could cover the specific method of "structured eligibility determination for Indian government welfare schemes using a Knowledge Graph with hybrid natural-language query routing," though enforceability would be narrow given the prior art in GraphRAG.

#### Publishable research

The methodology is suitable for publication at venues focused on AI for social impact:

- **AAAI/AI4SG Workshop** (AI for Social Good): Closing the disability benefits awareness gap using GraphRAG
- **ICTD** (Information and Communication Technologies and Development): Technology for welfare scheme access in developing countries
- **ACM DEV** (Computing and Sustainable Societies): Multilingual AI systems for government service navigation
- **CHI Late-Breaking Work**: Designing AI-powered government service navigation for accessibility-first users

Key publishable contributions:
1. A benchmark dataset of Indian disability scheme eligibility queries with ground-truth answers
2. Evaluation of GraphRAG vs. pure RAG for multi-constraint eligibility matching
3. Multilingual RAG performance across 10+ Indian languages for government documents

#### VC/Impact investor presentability

SamarthSchool falls across three high-interest impact investing themes:

1. **Disability inclusion**, explicitly listed as an emerging theme by India Impact Investors Council
2. **GovTech/Civic Tech**, with $4.96 billion deployed in Indian impact enterprises in 2024
3. **EdTech**, a $3.6-12.1 billion market growing at 27% CAGR

Relevant investors: AssisTech Foundation (disability-specific accelerator), Aavishkaar Capital, Omidyar Network India, Villgro. India's Social Stock Exchange (SSE) provides an additional listing pathway.

The CSR funding pool is large: INR 29,987 crore (~$3.6B) in FY 2023-24, with 44% going to education, disability, and livelihood programs.

### 7.3 Data and IP moat

The main competitive moat is the Knowledge Graph itself: a structured, validated, continuously-updated representation of 50+ disability schemes with machine-queryable eligibility rules. Building this requires:

- Domain expertise in Indian disability law and policy
- Partnerships with disability rights organizations for validation
- State-level data curation across 28 states
- Continuous monitoring and update infrastructure

This is not easy to replicate. The KG gets more valuable over time as it accumulates historical scheme data, usage patterns, and validation from domain experts.

---

## 8. Conclusion

India allocates thousands of crores annually for children with disabilities through 50+ schemes, yet 83.6% of eligible families don't know these schemes exist, and 42% never apply. This is not a technology gap or a policy gap. It is an information asymmetry gap.

SamarthSchool's GraphRAG architecture combines Neo4j's structured eligibility reasoning with Qdrant's semantic retrieval and Gemini's multilingual generation. The Knowledge Graph enables deterministic eligibility matching across 21 disability categories and 50+ schemes. The RAG layer makes results readable and actionable in the user's language. The failure modes are identified and mitigated through advisory disclaimers, human-validated KG entries, and stateless queries that store no child PII.

The path to scale is realistic but not easy. Government procurement takes 12-24 months, CSR funding requires sustained relationship-building, and the Knowledge Graph needs continuous curation. Our sensitivity analysis shows the project needs external funding for 4-5 years, which is in line with how social ventures typically operate.

Whether a small team with the right architecture and partnerships can close a gap that decades of government portals and NGO outreach have not is ultimately an empirical question. The MVP pilot with 5 schools will answer it. If those schools show a measurable increase in benefits accessed, the evidence base is there for everything else: B2G procurement, impact investment, national scale.

---

## Appendix: Course Concepts Applied

This table maps key Gen AI course concepts (Course 8919: Pre-Trained Models) to their specific application in SamarthSchool:

| Course Concept | SamarthSchool Application |
|---------------|--------------------------|
| **Retrieval-Augmented Generation (RAG)** | Core architecture: Qdrant vector store retrieves scheme document chunks to ground Gemini 2.0 Flash responses with citations. Prevents hallucination of non-existent schemes. |
| **Embeddings** | BAAI/bge-m3 (1024-dim, multilingual) encodes scheme documents and user queries into shared embedding space. Dense+sparse hybrid enables both semantic and exact keyword matching. |
| **Knowledge Graphs** | Neo4j stores 50+ schemes as structured entities with eligibility rules. Cypher queries perform deterministic multi-criteria matching (disability type × % × age × income × state) that pure RAG cannot. |
| **Prompt Engineering** | Query router classifies user intent (eligibility/explanation/process) using structured prompts. Response generation prompts enforce citation inclusion, advisory disclaimers, and language-appropriate output. |
| **Evaluation (RAGAS)** | Automated evaluation pipeline using Recall@10, Precision@5, Faithfulness, and Correctness metrics. 200+ gold-standard test personas validated by domain experts. |
| **Pre-Trained Models** | Gemini 2.0 Flash (primary LLM), bge-m3 (embedding), fastText lid.176 (language detection), IndicTrans2 (translation) — all pre-trained models adapted to domain via RAG rather than fine-tuning. |
| **Fine-Tuning (considered, deferred)** | Fine-tuning Gemini or Qwen on disability policy language is a Phase 3 consideration. Current approach uses RAG + KG grounding, which is more controllable and auditable for policy-sensitive outputs. |
| **Agents (exploratory)** | Phase 4 roadmap includes agentic workflows for application status tracking and document reminders, with explicit scope limits on auto-filling government forms (regulatory risk). |
| **Multilingual NLP** | Cross-lingual retrieval (bge-m3), translation (IndicTrans2), transliteration (IndicXlit for Romanized Hindi), and language detection (fastText) form a complete multilingual pipeline for 22 Indian languages. |
| **Human-in-the-Loop** | Three-level design: domain expert validates KG entries, school administrator reviews AI recommendations, feedback loop enables continuous improvement (Section 4.11). |

---

## References

1. Census of India 2011 — Data on Disability. Ministry of Home Affairs, Government of India.
2. National Family Health Survey-5 (NFHS-5), 2019-21 — Disability Prevalence. International Institute for Population Sciences.
3. NSS 76th Round (2018) — Persons with Disabilities in India. National Statistical Office.
4. UDISE+ FY2022 — Flash Statistics on CWSN Enrollment. Ministry of Education.
5. "Awareness of Unique Disability Identification Card and Associated Benefits." Indian Journal of Physical Medicine & Rehabilitation, 2025.
6. NILERD Study on UDID Coverage and Benefit Access. National Institute of Labour Economics Research and Development.
7. Rights of Persons with Disabilities Act, 2016. The Gazette of India, December 2016.
8. Samagra Shiksha Abhiyan — Framework for Implementation, Inclusive Education Component. Ministry of Education.
9. DEPwD Scholarship Schemes — Pre-Matric, Post-Matric, Top Class Education. Department of Empowerment of Persons with Disabilities.
10. ADIP Scheme Guidelines. Department of Empowerment of Persons with Disabilities.
11. Niramaya Health Insurance Scheme. National Trust, Ministry of Social Justice & Empowerment.
12. Digital Personal Data Protection Act, 2023 — Section 9 (Children's Data). Government of India.
13. GIGW 3.0 — Guidelines for Indian Government Websites and Apps. Ministry of Electronics & IT.
14. "India's Budget for People with Disabilities is Generous but Remains Underutilised." Scroll.in, 2025.
15. "Undercounting Disability in India." IndiaSpend, 2024.
16. India Impact Investors Council — Annual Report 2024.
17. UNESCO State of Education Report 2019: Children with Disabilities. UNESCO New Delhi.
18. "Graph RAG: Unlocking LLM Discovery on Narrative Private Data." Microsoft Research, 2024.
19. "Retrieval-Augmented Generation for AI-Generated Content: A Survey." Gao et al., 2024.
20. AI4Bharat — IndicTrans2 and IndicXlit Documentation. IIT Madras.
21. India EdTech Market Analysis. IMARC Group, 2025.
22. CSR Spending in India FY 2023-24 — Sector-Wise Allocation. Protean eGov Technologies.
23. AssisTech Foundation — Assistive Technology Ecosystem Report, 2025.
24. Maharashtra PwD Welfare Department — Schemes and Programmes.
25. Karnataka Department for Empowerment of Differently Abled — Scheme Listings.
26. Tamil Nadu State Scholarship Portal — Schemes for Differently Abled.
27. Delhi State Legal Services Authority — CWSN Scheme Compilation.
28. "Does Having a Disability Certificate Ensure Benefits?" Economic & Political Weekly, 2026.
29. RAGAS (Retrieval Augmented Generation Assessment) — Documentation. Explodinggradients, 2024.
30. Haqdarshak — Platform Overview. haqdarshak.com.
