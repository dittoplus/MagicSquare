# RED 단계 TODO (Dual-Track TDD)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_xx |
| 작성일 | 2026-06-04 |
| 단계 | **RED** — 실패 테스트 먼저 (`src/` 수정 금지) |
| SSOT | [`PRD.md`](PRD.md), [`Report/02`](../Report/02.MagicSquare_Session3_CursorDesign_Report.md) |
| 절차 | `.cursor/commands/tdd-red.md`, `.cursor/skills/magic-square-tdd/` |

**완료 기준:** 해당 Test ID에 대해 `pytest` **FAIL** (미구현 `ImportError` / `AssertionError` / `pytest.fail()`). assert 완화·`skip`·`xfail` 금지.

**Fixture (고정):**

- **G0** — 완전 채워진 4×4 격자 (10선 판정용)
- **G1** — 부분 격자: 빈칸 `(2,2)`, `(3,3)` · 누락 수 `{7, 10}` (1-index 행·열)

---

## Track A — Boundary (UI Track)

배치: `tests/boundary/test_u_*.py` · Control/Entity **스텁 허용** · 무효 입력 시 Domain **미호출**

### 입력 검증 (FR-01)

- [ ] **U-IN-01** — `grid=None` → `code` `E003` / `INVALID_NULL` *(설계표; Report/02에 null 전용 코드 미정의 시 SSOT 보강)*
  - Given: `grid=None`
  - Then: `{"code": "E003", ...}` 또는 PRD 동치 `INVALID_*`
  - Expected RED: `ModuleNotFoundError` (boundary 미구현)
- [ ] **U-IN-02** — `grid=3×4` → `E001` / `INVALID_SIZE`
  - Given: 3행×4열 격자
  - Then: `INVALID_SIZE`, Domain 미호출
  - Expected RED: `AssertionError`
- [ ] **U-IN-03** — 빈칸 0개 → `E002` / `INVALID_BLANKS` *(PRD: `INVALID_ZERO_COUNT` — 빈칸 ≠ 2)*
  - Given: `0`인 칸이 2개가 아닌 격자
  - Then: 빈칸 개수 오류, Domain 미호출
  - Expected RED: `AssertionError`

### 출력·흐름

- [ ] **U-OUT-01** — 유효 입력 **G1** → `len(result)==6`
  - Given: G1 (FR-01 통과 격자)
  - Then: 성공 시 `int[6]` — `[r1,c1,n1,r2,c2,n2]` (1-index)
  - Expected RED: `pytest.fail()` (RED 명시)
- [ ] **U-FLOW-02** — `grid=None` → `execute()` **0회** 호출
  - Given: `grid=None`
  - Then: control orchestration 미호출 (Mock/스텁 검증)
  - Expected RED: `pytest.fail()` (RED 명시)

---

## Track B — Logic (Domain Track)

배치: `tests/entity/`, `tests/control/` · `test_d_*.py` · **Domain Mock 금지**

### FR-02~03·05 (솔버·좌표·누락 수)

- [x] **D-LOC-01** — `find_blank_coords()` · **G1** → `[(2,2),(3,3)]` · **GREEN PASS** (Golden Master G1)
  - Invariant: **I6** row-major
  - ~~Expected RED: `ImportError` / `AssertionError`~~
- [ ] **D-MIS-01** — `find_not_exist_nums()` · **G1** → `[7, 10]` 오름차순
  - Invariant: **I7**, **I11**
  - Expected RED: `ImportError` / `AssertionError`
- [ ] **D-VAL-01** — `is_magic_square()` · **G0** 완전 격자 → `True`
  - Invariant: **I1~I5**
  - Expected RED: `ImportError` / `AssertionError`
- [ ] **D-SOL-01** — `solution()` · **G1** Step A 성공
  - Invariant: **I8**
  - Expected RED: `ImportError` / `AssertionError`

### FR-04 — 10선 완성 판정 (초안 1차 · RED 우선)

대상 API: `validate_ten_lines()` (PRD §6) — `is_magic_square()`와 동일 축

- [ ] **D-04-02** — 행·열만 34, **부대각 `/` ≠ 34** → `False` (**RED 우선**)
  - Mom Test: SC-1, SC-3
  - Expected RED: `AssertionError` (잘못된 `True` 또는 미구현)
- [ ] **D-04-03** — 주대각만 검사하는 구현과 **동치 거부**
  - Mom Test: SC-1
  - Expected RED: `AssertionError`

### FR-04 — GREEN 대기 (RED 이후)

- [ ] **D-04-01** — 10선 모두 34 → `True` (GREEN)
- [ ] **D-04-04** — 동일 격자 2회 → 동일 결과 (GREEN)

---

## 공통 작업 (RED 착수 전·후)

- [x] `tests/conftest.py`에 **G1** fixture 정의 *(G0: 후속)*
- [ ] 각 테스트 함수 docstring에 **Test ID** (`U-*` / `D-*`) 명시
- [ ] RED 완료 후 `python -m pytest <대상 파일> -q` → **FAIL** 로그 보관
- [ ] Boundary 오류 `INVALID_NULL` vs Report **E003**(`INVALID_ZERO_COUNT`) — 필요 시 PRD·Report SSOT 정합

---

## 추적

| 문서 | 역할 |
|------|------|
| [`PRD.md`](PRD.md) | FR · AC · 오류 `code` |
| [`Report/02`](../Report/02.MagicSquare_Session3_CursorDesign_Report.md) | E001~E007 · D-* SSOT |
| [`README.md`](../README.md) | Dual-Track 개요 |

**상태:** Harness 골격만 존재 — 위 항목 테스트 본문 **미작성** (`Report/02` Test Loop ❌).
