# v3.18 Table 5-3A / 5-3B Final Strategy

## Decision summary

The main paper should use the **severe-failure subset** for Table 5-3A:

- Main Table 5-3A: `results/final/text_to_pandas_severe_failure_error_type_summary_f1_lt_05.csv`
- Unit of analysis: Text-to-Pandas Agent severe failure cases, **F1 < 0.5, n = 40**
- Rationale: the diagnostic categories are rule-based post-hoc labels; using near-complete failures improves classification reliability and avoids over-interpreting partial-success cases.

The broader low-performance analysis remains available as supplementary diagnostics:

- `logs/text_to_pandas_low_performance_diagnostics/primary_error_type_summary_f1_lt_07.csv`
- `logs/text_to_pandas_low_performance_diagnostics/error_flag_summary_f1_lt_07.csv`
- `logs/text_to_pandas_low_performance_diagnostics/case_details_f1_lt_07.csv`

These files cover **F1 < 0.7, n = 53**, but are not used as the main paper table.

## Paper Table 5-3A recommended title

**Text-to-Pandas Agent의 severe failure 사례(F1<0.5, n=40)에 대한 주 오류 유형**

## Paper Table 5-3A

| 주 오류 유형          |   Count |   비율(%) | 해석                                                                           |
|:----------------------|--------:|----------:|:-------------------------------------------------------------------------------|
| 조건 해석 오류        |      19 |      47.5 | 자연어 조건을 query plan filter로 변환하는 과정에서 조건 누락 또는 오해석 발생 |
| 테이블·컬럼 선택 오류 |      11 |      27.5 | df_base/df_subj 선택 또는 예산·기관·사업명 컬럼 grounding 실패                 |
| 기관명·약어 해석 오류 |      10 |      25   | NIA, IITP, 부처 약칭 등 기관명 alias 해석 실패                                 |

### Required table note

표 5-3A는 Text-to-Pandas Agent의 전체 문항 중 severe failure에 해당하는 F1<0.5 사례 40건을 대상으로 주 오류 유형을 분류한 것이다. F1<0.7에 해당하는 전체 저성능 사례는 53건이나, 0.5≤F1<0.7에 해당하는 부분 성공 사례는 후보 일부 누락, 출력 형식 차이, 복합 원인 등이 혼재하므로 본문 표에서는 제외하고 보조 진단 파일로 제공하였다.

## Paper Table 5-3B source

Source file: `results/final/evaluation_mode_summary_5methods_perturbed_v1.csv`

| method                        |   exact_value |   exact_set |   any_3_from_candidate_set |
|:------------------------------|--------------:|------------:|---------------------------:|
| XLSX Template Executor v4     |         50    |       87.18 |                      65.31 |
| RDF Template SPARQL v3        |         50    |       64.1  |                      59.52 |
| Text-to-Pandas Agent          |         11.11 |       58.97 |                      65.07 |
| Plain Text Vector RAG         |          0    |       49.49 |                      39.61 |
| JSON Serialization Vector RAG |          0    |       31.28 |                      15.6  |

## Four interpretation guardrails

1. 본 연구의 비교는 end-to-end 자연어 질의응답 시스템의 단순 성능 순위가 아니라, 동일한 예산설명서 데이터가 서로 다른 표현 형식으로 제공될 때 LLM Agent가 활용할 수 있는 질의 가능성과 준상한 성능을 비교한 것이다.
2. Plain Text Vector RAG의 낮은 집계 성능은 RAG 일반의 절대적 한계가 아니라, 본 실험에서 사용한 계산 도구와 구조화 질의 도구가 없는 plain text baseline의 한계로 해석해야 한다.
3. Text-to-Pandas Agent는 자연어 질문을 구조화 query plan으로 자동 변환하는 현실적 Agent baseline이며, XLSX Template Executor와의 차이는 자연어→구조화 질의 변환 단계에서 발생하는 성능 손실을 보여준다.
4. JSON Serialization Vector RAG의 낮은 성능은 JSON 표현 자체의 한계가 아니라, 계층 구조를 명시적 질의 연산으로 활용하지 않고 직렬화된 텍스트로 검색한 방식의 한계를 보여준다.
