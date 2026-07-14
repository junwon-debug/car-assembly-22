# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

"차량조립 KATA" 리팩토링 실습 프로젝트다. `assembly.py`에 이미 동작하는 절차지향식 코드가 작성되어 있고,
이를 유지보수하기 쉽고 안전하며 확장 가능한 구조로 리팩토링하는 것이 이 프로젝트의 목적이다
(자세한 배경과 요구사항은 `docs/프로젝트요구사항.md` 참고).

리팩토링 시 다음 기존 코드의 문제점을 개선 대상으로 삼는다:
- 절차지향식 코드로 유지보수가 어려운 구조 (전역 변수 `q0`~`q4`로 상태 관리, 매직 넘버 기반 분기)
- 안전하지 않은 문법 사용 (예: `except:` bare except)
- 확장성이 고려되지 않음 (차량 타입/부품이 늘어나면 `if/elif` 분기를 계속 추가해야 함)
- 유닛테스트 부재

## 실행

```bash
python assembly.py
```

가상환경은 `.venv`에 Python 3.14 기반으로 구성되어 있으며 `pytest`가 설치되어 있다 (아직 테스트 코드는 없음).

Windows에서 가상환경 활성화:
```powershell
.venv\Scripts\activate.ps1
```

## 테스트

`pytest`가 의존성으로 설치되어 있으므로 리팩토링 시 테스트 코드를 `pytest` 규칙(`test_*.py` 또는 `*_test.py`)에
맞춰 추가하고, 아래 명령으로 실행한다.

```bash
pytest                      # 전체 테스트 실행
pytest path/to/test_x.py::test_name   # 단일 테스트 실행
```

## 도메인 로직 (자동차 조립 규칙)

차량은 "타입 선택 → 부품 선택 → 완성 차량 검증" 순서로 조립된다.

- **차량 타입**: Sedan(세단), SUV, Truck — 향후 타입 추가 가능성을 염두에 두어야 함
- **부품**: 엔진(GM/TOYOTA/WIA, 그리고 테스트용 "고장난 엔진"), 제동장치(MANDO/CONTINENTAL/BOSCH), 조향장치(BOSCH/MOBIS)
- **호환성 제약 조건** (`is_valid_check()` / `test_produced_car()`에 중복 구현되어 있음):
  1. 제동장치로 Bosch를 사용하면 조향장치도 반드시 Bosch여야 한다 (타사 조향장치와 호환 불가)
  2. Continental은 Sedan용 제동장치를 만들지 않는다 → Sedan에 Continental 제동장치 사용 불가
  3. TOYOTA는 SUV용 엔진을 만들지 않는다 → SUV에 TOYOTA 엔진 사용 불가
  4. WIA는 Truck용 엔진을 만들지 않는다 → Truck에 WIA 엔진 사용 불가
  5. MANDO는 Truck용 제동장치를 만들지 않는다 → Truck에 MANDO 제동장치 사용 불가

이 제약 조건은 리팩토링 후에도 단일 지점(single source of truth)에서 판단하도록 만드는 것이 핵심 과제다 —
현재는 `is_valid_check()`(런타임 동작 차단용)와 `test_produced_car()`(테스트 결과 출력용)에 동일한 로직이
그대로 복제되어 있다.

## 현재 코드 구조 (리팩토링 전)

`assembly.py` 하나로 구성되어 있으며, 전역 변수 `q0`(차량 타입), `q1`(엔진), `q2`(제동장치), `q3`(조향장치)에
사용자 선택 상태를 저장하는 상태 머신 형태로 동작한다.

- `main()`: `step`(0~4) 값을 기준으로 한 단계 상태 머신으로 CLI 입력을 순환 처리
- `show_menu(step)` / `is_valid_range(step, ans)`: 단계별 메뉴 출력과 입력값 범위 검증
- `select_car_type/engine/brake/steering(a)`: 각각 해당 전역 변수(`q0`~`q3`)에 선택값 기록
- `is_valid_check()`: 조합 가능 여부 판정 (런타임 동작 차단용)
- `run_produced_car()` / `test_produced_car()`: 완성된 차량 실행 및 검증 결과 출력
