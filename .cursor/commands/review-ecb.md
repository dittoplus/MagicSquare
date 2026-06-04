# review-ecb — ECB·계약 정적 리뷰

MagicSquare_xx **ECB·입출력 계약** 위반만 검사한다. **코드 수정·자동 fix·테스트 추가 금지.**

한국어 응답. 헌법: `.cursorrules` · 오류 SSOT: `Report/02` §5.

---

## 필수 선언

**응답 첫 줄 (고정 형식):**

```text
Phase: review | Scope: src/|tests/|전체 | Track: Logic|UI|both
```

예: `Phase: review | Scope: src/ | Track: both`

---

## 절차

1. **범위 확인** — 사용자가 지정한 경로(없으면 `src/` + `tests/`). Read/Grep만 사용.
2. **5항목 점검** — 아래 체크리스트 순서대로 검색·읽기.
3. **위반 표 작성** — 발견된 항목만 행 추가. 없으면 `위반 없음`.
4. **우선순위 요약** — P0(아키텍처·계약 깨짐) / P1(스타일·SSOT 경미) 1~3줄.
5. **보고** — § 보고 형식. **수정 제안은 표의 Recommendation 열에만** (파일 편집 금지).

---

## 체크리스트 (5항목)

### 1. import 방향 (ECB)

| OK | 위반 |
|----|------|
| boundary → control → entity 호출 | entity가 `boundary`/`control` import |
| control → entity | control → boundary import |
| entity는 `entity` 패키지 내부·stdlib만 | boundary → entity **직접** import (control 우회) |

**검색 힌트:** `from boundary`, `from control`, `import boundary`, `import control` in `src/entity/` · `src/control/` import 역방향.

### 2. entity E001~E005

| OK | 위반 |
|----|------|
| entity는 순수 도메인(10선·합·좌표) | entity에서 `"E001"`~`"E005"` 반환·raise·dict `code` |
| E006 로직은 Result/enum 등 **코드 문자열 없이** | entity가 FR-01 입력 검증(E001~E004) 수행 |
| E001~E005 emit은 boundary/control | entity가 `{"code": ...}` 형태 오류 응답 생성 |

**검색 힌트:** `E001`, `E002`, … `E005`, `INVALID_SIZE`, `INVALID_ZERO` in `src/entity/`.

### 3. int[6] 1-index (출력 계약)

| OK | 위반 |
|----|------|
| 성공 시 `[r1,c1,n1,r2,c2,n2]` 길이 6 | 0-index 좌표를 성공 출력으로 반환 |
| r,c ∈ 1..4 | 길이 ≠ 6, tuple/str 혼용 |
| boundary/control에서 E005 검증 | entity가 API 응답 envelope 조립 |

**검색 힌트:** 반환 타입·docstring·테스트 assert의 좌표 값 `0`, `5` 사용.

### 4. MagicConstant SSOT

| OK | 위반 |
|----|------|
| `34`/`16`/`4`는 `entity/constants.py`(또는 SSOT 1곳)만 | `src/`·`tests/`에 마방진 `34`/`16` **리터럴** 산재 |
| 테스트·구현 모두 상수 import | 매직 넘버로 10선 합 비교 |

**검색 힌트:** `\b34\b`, `\b16\b` in `src/`, `tests/` (constants 모듈 제외).

### 5. Logic Track Domain Mock

| OK | 위반 |
|----|------|
| `tests/entity`, `tests/control` — **실구현** import | `MagicMock`/`patch`로 entity·domain 함수 대체 |
| boundary 테스트만 control/entity 스텁 | Logic 테스트에서 `validate_*` 등을 mock으로 통과 |
| fixture는 격자·상수 데이터만 | `@patch("entity...")` on Logic Track |

**검색 힌트:** `MagicMock`, `patch`, `monkeypatch.setattr` in `tests/entity/`, `tests/control/`.

---

## 보고 (위반 표)

위반이 **0건**이면:

```text
Phase: review | Scope: … | Track: …
결과: 위반 없음 (5항목 PASS)
```

위반이 **1건 이상**이면 표:

| P | Check | File:Line | 위반 내용 | Recommendation |
|---|-------|-----------|-----------|----------------|
| P0 | import 방향 | `src/entity/foo.py:3` | `from control import …` | control 호출 제거, entity 내부로 이동 |
| P0 | E001~E005 | … | … | boundary로 emit 이전 |
| P1 | MagicConstant | … | … | `entity.constants` import |

- **P0:** ECB 깨짐, entity E001~E005, Logic Domain Mock, 성공 출력 계약 오류
- **P1:** SSOT 리터럴, docstring·네이밍

**변경 파일:** 없음 (리뷰 only)

---

## 금지

| 금지 | 이유 |
|------|------|
| `src/`·`tests/` **수정** | 리뷰 Command |
| pytest 실행으로 “고치기” | Test Loop는 `/tdd-red`·GREEN |
| 자동 refactor·commit / push | 사용자 요청·별 Phase |
| 위반 없는데 임의 P2 지적 | 노이즈 |

---

## 참고

- Dual-Track: UI(`tests/boundary`) Mock **허용** — Logic Mock 위반과 구분.
- 10선 완전성(주·부대각)은 **동작 리뷰**; 본 Command는 **구조·계약** 위주.
