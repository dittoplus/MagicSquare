# D-* Logic Track 테스트 ID (SSOT)

출처: `Report/02` §6 · `docs/PRD.md` §8.2. 파일 `tests/**/test_d_*.py`, docstring에 ID 필수.

| ID | 시나리오 | Phase |
|----|----------|-------|
| **D-04-01** | 10선 모두 34 → `True` | GREEN |
| **D-04-02** | 행·열만 34, 부대각 ≠ 34 → `False` | **RED 우선** |
| **D-04-03** | 주대각만 확인한 케이스와 동치 거부 | RED |
| **D-04-04** | 동일 격자 2회 → 동일 결과 | GREEN |

후속 Logic ID는 Report/02·PRD 갱신 후 본表에 추가.
