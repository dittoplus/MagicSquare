# TDD RED — 실패 테스트 먼저

MagicSquare_xx **Dual-Track TDD — RED 단계만**. GREEN/REFACTOR·`src/` 구현은 **하지 않는다**.

한국어 응답. SSOT: `.cursorrules`, `docs/PRD.md`, `Report/02`, D-* 목록 `.cursor/skills/magic-square-tdd/reference.md`.

---

## 필수 선언

**응답 첫 줄 (고정 형식):**

```text
Phase: red | Layer: entity|control|boundary | Track: Logic|UI
```

예: `Phase: red | Layer: entity | Track: Logic`

---

## 절차 (ID 확인 → AAA 테스트 → pytest FAIL)

1. **Test ID 확인**
   - Logic: `D-*` — `tests/entity/`, `tests/control/` · `test_d_*.py`
   - UI: `U-*` — `tests/boundary/` · `test_u_*.py` (FR-01)
   - 출처: `reference.md` 또는 `Report/02` §6; 없으면 `docs/PRD.md` §8.2
   - RED 우선 ID: **D-04-02** (행·열 OK, 부대각 `/` ≠ 34 → `False` 기대)

2. **C2C 한 줄** — Given(격자) / When(함수·API) / Then(기대)

3. **AAA 테스트 작성** — `tests/{entity|control|boundary}/test_d_*.py` 또는 `test_u_*.py`
   - **Arrange:** 4×4 격자 fixture (Mom Test: 대각선 누락 케이스 포함)
   - **Act:** import 대상 호출 (미구현 → `ImportError`도 RED 성공)
   - **Assert:** 기대 결과 **한 가지** — 완화·삭제 금지
   - 함수 docstring에 **Test ID** (예: `D-04-02`)

4. **`src/` 수정 금지** — RED는 `tests/`만 변경

5. **pytest 실행** — 아래 예시로 **FAIL** 확인 (미구현·잘못된 PASS 모두 RED 성공)

6. **보고** — § 보고

---

## pytest 예시 (bash)

프로젝트 루트, `pip install -e ".[dev]"` 후:

```bash
# 단일 테스트 (권장)
python -m pytest tests/entity/test_d_04_02.py::test_d_04_02_anti_diagonal_not_34 -q

# 파일 전체
python -m pytest tests/entity/test_d_04_02.py -q

# ID 키워드
python -m pytest tests/entity -k "d_04_02" -q
```

**RED 통과 기준:** exit code ≠ 0 — `FAILED`, `ImportError`, `AssertionError` (GREEN 코드 없이 실패).

---

## 보고

```text
Phase: red | Layer: … | Track: …
Test ID: D-… / U-…
pytest: [실행 명령] → FAIL
FAIL 요약: [1~2줄 — AssertionError / ImportError / unexpected pass]
변경 파일: tests/… (tests/만)
다음: GREEN — 동일 Test ID
```

---

## 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN 단계 |
| Logic Track **Domain/Entity Mock** (`patch`, `MagicMock` on domain) | Dual-Track — 실구현만 |
| assert 완화·삭제·`skip`·`xfail` | RED 우회 |
| RED 없이 GREEN 구현 | TDD 순서 |
| git commit / push | 사용자 요청 시만 |
