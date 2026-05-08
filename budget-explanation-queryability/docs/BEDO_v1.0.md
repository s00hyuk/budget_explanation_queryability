# Budget Explanation Domain Ontology (BEDO) v1.0

## 1. Purpose

BEDO is a lightweight domain ontology for representing Korean government budget explanation documents (`예산설명서`) as RDF graphs. It is designed for AI-friendly querying — specifically for SPARQL-based template execution over a structured representation of fiscal projects, their administrative classification, implementing agencies, and budget figures.

BEDO is an **RDFS-level** ontology (no OWL reasoning) to keep query execution lightweight and avoid reasoning overhead in template-based pipelines.

**Namespace** (placeholder, replace with actual IRI):
```
@prefix : <http://example.org/bedo/v1.0#> .
```

---

## 2. Classes (8 core classes)

| Class | Description | Example |
|---|---|---|
| `:Project` | An individual fiscal project | `AI·SW중심대학` |
| `:Ministry` | The supervising central government ministry | `과학기술 정보통신부` |
| `:Field` | Top-level administrative classification | `과학기술` |
| `:Sector` | Sub-classification under a Field | `정보통신` |
| `:Program` | A budget program (groups projects) | `SW산업진흥` |
| `:UnitProgram` | A unit-program under a Program | `SW융합인력양성` |
| `:Agency` | The implementing agency | `정보통신기획평가원` |
| `:SupportType` | Support form (categorical) | `직접`, `출연`, `보조`, `출자`, `융자` |

---

## 3. Object Properties (7)

| Property | Domain → Range | Meaning |
|---|---|---|
| `:hasSupervisor` | `Project → Ministry` | the supervising ministry of a project |
| `:implementedBy` | `Project → Agency` | the implementing agency |
| `:belongsToField` | `Project → Field` | field-level classification |
| `:belongsToSector` | `Project → Sector` | sector-level classification |
| `:underProgram` | `Project → Program` | program membership |
| `:underUnitProgram` | `Project → UnitProgram` | unit-program membership |
| `:hasSupportType` | `Project → SupportType` | support-form classification |

---

## 4. Data Properties (7)

| Property | Domain → Range | Meaning |
|---|---|---|
| `:hasBudget2026` | `Project → xsd:decimal` | 2026 confirmed budget (백만원) |
| `:hasBudget2025` | `Project → xsd:decimal` | 2025 budget (백만원) |
| `:budgetChange` | `Project → xsd:decimal` | year-over-year change |
| `:isNew` | `Project → xsd:boolean` | new-project flag |
| `:isContinued` | `Project → xsd:boolean` | continuing-project flag |
| `:projectName` | `Project → xsd:string` | project name |
| `:projectCode` | `Project → xsd:string` | project ID code |

---

## 5. Why a domain-specific ontology?

Existing public-data vocabularies (DCAT, schema.org, FOAF) describe **dataset metadata** and **organizations / persons / web resources** in general. They do not capture the domain structure of Korean government budget projects:

- The supervising-ministry vs. implementing-agency distinction (BEDO splits `:Ministry` and `:Agency`)
- The Korean budget classification hierarchy (`Field → Sector → Program → UnitProgram → Project`)
- Categorical support types (`직접 / 출자 / 출연 / 보조 / 융자`)
- Year-over-year budget change semantics

BEDO is therefore **complementary to** general-purpose LOD vocabularies rather than competing with them. Future extensions could publish BEDO-instance graphs as 5-star LOD by linking `:Ministry` and `:Agency` to existing organization vocabularies.

---

## 6. Range of generalization

The BEDO classes and properties were derived by analyzing 533 AI-related fiscal projects from Korea's 2026 budget. We additionally verified that the same template structure recurs across other policy domains by sampling budget explanation documents from 9 different ministries and committees (paper §3.5):

| Core schema component | Coverage (n=9 sample documents) |
|---|---|
| 사업 코드 정보 (project code, account, division, etc.) | 9/9 (100%) |
| 프로그램·단위·세부사업 체계 (program hierarchy) | 9/9 (100%) |
| 사업 지원 형태 (support types) | 9/9 (100%) |
| 소관/담당/시행주체 정보 (supervisor / implementing agency) | 9/9 (100%) |
| 예산·지출계획 총괄표 (budget summary) | 9/9 (100%) |
| 사업목적·내용 (purpose & content) | 8/9 (88.9%) |
| 사업근거 및 추진경위 (legal basis & history) | 8/9 (88.9%) |

This indicates that BEDO is not an ad-hoc schema fitted to AI-domain projects but a **reusable domain schema** grounded in the recurring structure of the Korean government's standard budget explanation template across ministries and policy areas.

---

## 7. File

The instance graph at `data/budget_graph_v2.ttl` contains 533 `:Project` instances along with the corresponding `:Agency`, `:UnitProgram`, `:Sector`, `:Ministry`, `:Field`, and `:SupportType` resources.
