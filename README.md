# MagicSquare 4×4 (MagicSquare_xx)

부분적으로 비어 있는 **4×4 Magic Square**(빈칸 2개, `0` / `1..16`, **10개 선 합 34**)를 다루는 **Python TDD** 학습 프로젝트입니다.

요구사항은 **Mom Test**로 도출한 문제 정의에서 출발하며, 단일 기준 문서는 [`docs/PRD.md`](docs/PRD.md)입니다.

---

## 왜 이 프로젝트인가 (Mom Test)

**진짜 문제:** 빈칸 2개 4×4 과제에서 **10개 선(행·열·대각) 합 34**를 빠짐없이 확인하지 못한 채 “끝났다”고 판단해, **약 20분**을 다시 쓰게 된다.

**주제:** 부분 마방진을 “완성”으로 볼 때, **10개 선을 빠짐없이·재현 가능하게** 판별할 수 있어야 한다.

| | |
|---|---|
| **표면(하지 않음)** | “대각선까지 검증해 주는 **프로그램**” |
| **1차 구현 초점** | **FR-04** — 10선 합 34 **완성 판정** (Domain) |

상세 인터뷰·R-G-I-O·성공 기준: [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md)

---

## Dual-Track TDD

| 트랙 | 역할 |
|------|------|
| **Domain** | 마방진 수학 — 10선 합 34 판정, *(후속)* 해 탐색 |
| **Boundary** | 입력 검증(FR-01), `code`/`message` 계약 — 무효 입력 시 Domain **미호출** |

GUI·LMS·웹은 **Out of Scope** ([PRD §2.2](docs/PRD.md)).

---

## 문서

| 문서 | 내용 |
|------|------|
| [`docs/PRD.md`](docs/PRD.md) | FR · AC · 테스트 · 범위 **단일 기준** |
| [`docs/TODO-RED.md`](docs/TODO-RED.md) | RED 단계 Test ID · Given/Then · 상세 SSOT |
| [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md) | Mom Test 문제 정의 · 추적성 |

---

## 범위 (요약)

**In scope:** 4×4 고정, 빈칸 정확히 2개, 10선 합 34, Python + pytest, Dual-Track TDD.

**Out of scope:** LMS 자동 채점, GUI/GridUI, N×N 일반화, 퍼즐 생성기.

**우선순위:** FR-04(10선 판정) → FR-02~03~05(빈칸 탐색·해 탐색).

---

## 프로젝트 구조

```text
pyproject.toml
src/{entity,control,boundary}/
tests/{entity,control,boundary}/
Report/
docs/
```

---

## RED 단계 체크리스트

상세 Given/Then·오류 코드는 [`docs/TODO-RED.md`](docs/TODO-RED.md) 참고.  
**완료 기준:** 각 Test ID에 `pytest` **FAIL** (`src/` 수정 없이 `tests/`만). Fixture: **G0**(완전 격자), **G1**(빈칸 `(2,2)`, `(3,3)` · 누락 `{7,10}`).

### 공통

- [ ] `tests/conftest.py`에 **G0**, **G1** fixture 정의
- [ ] 각 테스트 docstring에 **Test ID** (`U-*` / `D-*`) 명시
- [ ] RED 후 `python -m pytest <대상> -q` → **FAIL** 로그 보관
- [ ] `INVALID_NULL` vs Report **E003** — 필요 시 PRD·Report SSOT 정합

### Track A — Boundary (`tests/boundary/test_u_*.py`)

- [ ] **U-IN-01** — `grid=None` → `E003` / `INVALID_NULL`
- [ ] **U-IN-02** — `grid=3×4` → `E001` / `INVALID_SIZE`
- [ ] **U-IN-03** — 빈칸 0개 → `E002` / `INVALID_BLANKS` (PRD: `INVALID_ZERO_COUNT`)
- [ ] **U-OUT-01** — 유효 입력 **G1** → `len(result)==6`
- [ ] **U-FLOW-02** — `grid=None` → `execute()` **0회** (Domain 미호출)

### Track B — Logic (`tests/entity/`, `tests/control/` · `test_d_*.py`)

**FR-02~05 · 솔버**

- [x] **D-LOC-01** — `find_blank_coords()` · G1 → `[(2,2),(3,3)]` (I6) · **GREEN**
- [ ] **D-MIS-01** — `find_not_exist_nums()` · G1 → `[7, 10]` (I7, I11)
- [ ] **D-VAL-01** — `is_magic_square()` · G0 → `True` (I1~I5)
- [ ] **D-SOL-01** — `solution()` · G1 Step A 성공 (I8)

**FR-04 · 10선 판정** (`validate_ten_lines` — RED 우선)

- [ ] **D-04-02** — 행·열만 34, 부대각 `/` ≠ 34 → `False` (**RED 우선**)
- [ ] **D-04-03** — 주대각만 검사와 동치 거부 (SC-1)

**FR-04 · GREEN 대기** (RED 이후)

- [ ] **D-04-01** — 10선 모두 34 → `True`
- [ ] **D-04-04** — 동일 격자 2회 → 동일 결과

---

## 시작하기

Harness(`pyproject.toml`, ECB `src/`·`tests/` 골격)는 준비됨. **테스트 본문은 미작성.**

TDD 순서 ([PRD §8.3](docs/PRD.md)):

1. **RED** — 위 체크리스트 (`D-04-02` 우선)
2. **GREEN** — 10선 각각 합 34 검사
3. **REFACTOR** — 선 좌표 enumerate 추출 (behavior 불변)

```powershell
pip install -e ".[dev]"
python -m pytest tests/entity/test_d_04_02.py -q
```

---

## Mom Test → PRD 추적

| Mom Test | PRD |
|----------|-----|
| “대각선 **하나를 빼먹어서**” | SC-1 → AC-04, AC-05 |
| “행·열·대각선 합 맞췄는데” | SC-2 → AC-04 |
| “**20분** 날렸다” | SC-3 → 회귀·재현 테스트 |

---

## 라이선스

교육·연습용 프로젝트. 라이선스는 추후 명시.
