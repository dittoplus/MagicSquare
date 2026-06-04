# MagicSquare 4×4 (MagicSquare_1004)

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
| [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md) | Mom Test 문제 정의 · 추적성 |

---

## 범위 (요약)

**In scope:** 4×4 고정, 빈칸 정확히 2개, 10선 합 34, Python + pytest, Dual-Track TDD.

**Out of scope:** LMS 자동 채점, GUI/GridUI, N×N 일반화, 퍼즐 생성기.

**우선순위:** FR-04(10선 판정) → FR-02~03~05(빈칸 탐색·해 탐색).

---

## 프로젝트 구조 (예정)

```text
src/magicsquare/
  boundary/
  domain/          # validate_ten_lines (FR-04)
  control/
  entity/
tests/
  boundary/
  domain/
  e2e/
Report/
docs/
```

---

## 시작하기

> 코드·`pyproject.toml`은 아직 없습니다. FR-04 Domain Test Loop부터 추가할 예정입니다.

구현 시 권장 순서 ([PRD §8.3](docs/PRD.md)):

1. **RED** — 행·열만 맞고 대각선 틀린 격자가 통과하면 실패하는 테스트
2. **GREEN** — 10선 각각 합 34 검사
3. **REFACTOR** — 선 좌표 enumerate 추출 (behavior 불변)

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
