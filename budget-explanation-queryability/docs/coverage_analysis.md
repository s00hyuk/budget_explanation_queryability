# Cross-Ministry Reusability / Coverage Notes

This package includes the final 5-method perturbed benchmark outputs. The paper also reports a cross-ministry, cross-domain reuse check for the Budget Explanation Domain Ontology (BEDO). The coverage table should be interpreted as an automatic extraction-based detection rate, not as proof that a section is absent from the source HWP/HWPX document.

Recommended wording for the paper:

> The cross-ministry coverage rate indicates whether each BEDO core item was detected under the automatic HWP/HWPX parsing criteria. A non-detected item may reflect variation in section heading or table extraction quality rather than actual absence from the original budget document.

Core reusable components:

| BEDO component | Expected interpretation |
|---|---|
| Project title | Common budget project identifier |
| Project code information | Account/fund, ministry, field, sector, program, unit program, detailed project code |
| Support type and rate | Direct, investment, contribution, subsidy, loan, national subsidy rate |
| Budget/expenditure summary table | Year-to-year budget comparison table |
| Purpose/content | Descriptive purpose and policy content |
| Legal basis and history | Statutory basis and project history |
| Implementation structure | Implementing method, agency, beneficiary, subsidy/contribution details |

