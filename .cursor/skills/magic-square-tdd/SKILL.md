---
name: magic-square-tdd
description: MagicSquare_xx Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. TDD RED/GREEN/REFACTOR, FR-04 10선 판정, entity/control/boundary, D-*/U-* 테스트, pytest Loop 요청 시 사용.
---

# magic-square-tdd

MagicSquare_xx **Dual-Track TDD + ECB** 절차 SSOT. 헌법은 `.cursorrules`, ID·오류 SSOT는 `Report/02`, 요구는 `docs/PRD.md`. D-* 목록은 [reference.md](reference.md).

응답은 **한국어**. 매 턴 첫 줄: `Phase: red|green|refactor | Layer: entity|control|boundary | Track: Logic|UI`.

---

## 언제 이 Skill을 켜는지

| 상황 | 적용 |
|------|------|
| 사용자가 TDD, RED/GREEN/REFACTOR, FR-04, 10선, 마방진 로직 구현·테스트를 요청 | ✅ **필수** |
| `tests/**/test_d_*`, `test_u_*` 작성·수정 | ✅ |
| `src/entity`, `src/control`, `src/boundary` 구현·리팩터 | ✅ |
| ECB import·Mock·E001~E007 계약 검토 | ✅ |
| Harness·문서만, Mom Test 인터뷰, git push만 | ❌ (본 Skill 불필요) |
| Command(`/tdd-red` 등) 없을 때 | 본 Skill이 **실행 절차** 역할 |

---

## Logic Track vs UI Track

| 항목 | **Logic Track** | **UI Track** |
|------|-----------------|--------------|
| Layer | entity, control | boundary |
| `src/` | `entity/`, `control/` | `boundary/` |
| `tests/` | `tests/entity/`, `tests/control/` | `tests/boundary/` |
| 테스트 ID | `D-*` | `U-*` |
| 파일명 | `test_d_*.py` | `test_u_*.py` |
| Mock | Domain/Entity **Mock 금지** — 실구현만 | Control/Entity **스텁 허용** |
| 대표 FR | FR-04 (10선=34), FR-02~05 (후속) | FR-01 (입력 계약) |

---

## ECB · Mock · E001~E007

### ECB (import·호출)

| 규칙 | 내용 |
|------|------|
| 호출 방향 | **boundary → control → entity** (단방향) |
| entity | `boundary`/`control` import **금지**; I/O 없음 |
| control | entity 조합; boundary 역import 금지 |
| boundary | FR-01 검증; 무효 입력 시 control/entity **미호출** |

### Mock

| Track | 허용 | 금지 |
|-------|------|------|
| Logic | pytest fixture로 **격자·상수**만 | `MagicMock`/`patch`로 entity·domain 함수 대체 |
| UI | control/entity **스텁** (호출 여부·반환값) | boundary 자체를 Mock으로 **통과 우회** |

### E001~E007 (Report/02 SSOT)

| Code | 담당 | Entity |
|------|------|--------|
| E001~E005 | Boundary emit | **처리·반환·매핑 금지** |
| E006 | Control 경유 (`NO_SOLUTION`) | 로직만; code emit은 control/boundary |
| E007 | Boundary (미완성 격자) | **금지** |

우선순위: E001 → E002 → E003 → E004 → Domain.

---

## RED (5~7단계)

1. **선언** — `Phase: red | Layer: … | Track: …`
2. **ID 확인** — [reference.md](reference.md) 또는 Report/02에서 `D-*`/`U-*` 1개 선택 (RED 우선: **D-04-02**)
3. **C2C** — Given(격자) / When(호출) / Then(기대) 한 줄 요약
4. **AAA 테스트** — `tests/{entity|control|boundary}/test_d_*.py` 또는 `test_u_*.py`; 함수 docstring에 **테스트 ID**
5. **`src/` 수정 금지** — import 대상은 미구현(`ImportError`) 또는 stub 없음 → **FAIL** 유도
6. **pytest 실행** — 대상 테스트만 (아래 Loop § RED)
7. **완료 보고** — FAIL 로그·Test ID·변경 파일 **`tests/`만**

**금지:** assert 완화, `skip`, `xfail`, Logic Track Domain Mock, GREEN 코드 선작성.

---

## GREEN (5~7단계)

1. **선언** — `Phase: green | Layer: … | Track: …`
2. **대상** — RED에서 FAIL 난 **동일 Test ID**만 통과시키는 **최소** 구현
3. **Layer 준수** — FR-04는 `entity`; orchestration은 `control`; E001~E005는 `boundary`만
4. **MagicConstant SSOT** — `34`/`16`/`4` 리터럴 금지 → `entity/constants.py` 등 단일 모듈
5. **10선 완전성** — 4행+4열+주대각(`\`)+부대각(`/`) **전부** 검사 (Mom Test SC-1)
6. **pytest 실행** — 해당 테스트 → **PASS** (Loop § GREEN)
7. **완료 보고** — PASS 로그·변경 `src/`·`tests/` 경로·ECB 위반 없음

**금지:** RED 테스트 삭제·완화, 다른 ID 일괄 GREEN, entity에서 E001~E005 반환.

---

## REFACTOR (5~7단계)

1. **선언** — `Phase: refactor | Layer: … | Track: …`
2. **전제** — 해당 Track **전체** 테스트 이미 GREEN
3. **범위** — 구조 개선만 (선 좌표 enumerate, 중복 제거, 이름 정리)
4. **Behavior 동일** — 공개 API·테스트 기대값 **불변**
5. **ECB·SSOT 유지** — import 방향·상수 위치 퇴행 금지
6. **pytest 실행** — Track 또는 전체 (Loop § REFACTOR)
7. **완료 보고** — diff 요약·회귀 없음·SC/Mom Test 추적 유지

**금지:** 기능 추가, assert 변경, REFACTOR 중 RED 테스트 깨진 채 진행.

---

## Test/Review Loop — pytest 실행 시점

프로젝트 루트, `pip install -e ".[dev]"` 후:

| Phase | 언제 | 명령 | 통과 기준 |
|-------|------|------|-----------|
| **Harness 점검** | Harness·디렉터리만 변경 | `python -m pytest --collect-only -q` | 수집 OK (0 tests 허용) |
| **RED** | 테스트 추가·수정 직후 | `python -m pytest tests/entity/test_d_04_02.py -q` *(또는 해당 파일)* | **FAIL** (미구현·잘못된 통과) |
| **RED 검증** | FAIL 확인 후 보고 | 동일 명령 재실행 | 여전히 FAIL (우연 PASS 의심 시) |
| **GREEN** | `src/` 최소 구현 후 | `python -m pytest tests/entity/test_d_04_02.py -q` | **PASS** |
| **GREEN 회귀** | entity/control 변경 후 | `python -m pytest tests/entity tests/control -q` | Logic Track **전부 PASS** |
| **UI GREEN** | boundary 작업 후 | `python -m pytest tests/boundary -q` | UI Track PASS |
| **REFACTOR** | 구조 변경 후 | `python -m pytest -q` | **전체 PASS** |
| **Review** | ECB·계약 점검 요청 시 | 위 전체 + import 방향·E001~E005 entity 검색 | 위반 0건 |

Track 격리: Logic 작업 중 `tests/boundary` 실패는 **UI 미착수**면 별도 이슈로 분리.

---

## 10선 체크리스트 (FR-04 · Mom Test)

완성 판정·테스트 격자 설계 시 **10개 선** 모두 합 34:

- 행 R1~R4, 열 C1~C4, 주대각 `\`, 부대각 `/`
- **SC-1:** 대각선 **1개만** 검사하는 구현·테스트 → RED
- **SC-2:** 10선 빠짐없이 판정
- **SC-3:** 동일 입력 → 동일 출력 (D-04-04)

---

## 완료 보고 항목 (매 Phase 종료)

```text
Phase: … | Layer: … | Track: …
Test ID: D-… / U-…
pytest: [명령] → [PASS|FAIL] (핵심 1줄)
변경 파일: …
ECB: [위반 없음 / P0 목록]
E001~E007: [해당 없음 / boundary만 emit 확인]
다음: [RED|GREEN|REFACTOR] + ID
```

git commit/push는 **사용자 요청 시만**.

---

## 참고

- D-* ID 전체: [reference.md](reference.md)
- 오류·ID SSOT: `Report/02.MagicSquare_Session3_CursorDesign_Report.md`
