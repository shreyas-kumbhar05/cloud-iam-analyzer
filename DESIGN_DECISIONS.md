# Design Decisions

| Decision | Alternatives considered | Chosen | Reason |
|---|---|---|---|
| Overall pipeline architecture | Monolithic script vs. modular pipeline | Modular pipeline with a normalized intermediate schema | Separates provider-specific parsing from provider-independent security analysis, allowing future formats and rules to be added without changing existing stages |

### Pipeline

```text
Input Policy
    ↓
Parser
    ↓
NormalizedPolicy
    ↓
Rule Engine
    ↓
Finding
    ↓
Risk Engine
    ↓
Report
