# PLAN.md

`assembly.py` 리팩토링 계획. TDD(Red-Green-Refactor)로 진행하며, 현재 유닛테스트가 없으므로
**리팩토링에 앞서 기존 동작을 고정하는 특성화 테스트(characterization test)를 먼저 작성**한다.

## 진행 원칙

- 테스트가 없는 상태에서 구조를 먼저 바꾸지 않는다. 항상 "테스트로 현재 동작을 고정 → 리팩토링 → 테스트 통과 확인" 순서를 지킨다.
- 한 커밋에는 하나의 작은 변경만 담는다 (테스트 추가, 리팩토링 스텝 단위로 분리).
- 리팩토링 중 도메인 규칙([DOMAIN.md](DOMAIN.md))의 결과 값은 절대 바뀌면 안 된다 — 바뀐다면 리팩토링이 아니라 버그다.
- Phase는 순서대로 진행하며, 이전 Phase의 테스트가 모두 통과해야 다음 Phase로 넘어간다.

## Phase 1 — 유닛테스트 생성 (특성화 테스트)

리팩토링 대상 함수들의 현재 입출력을 pytest로 캡처해 안전망을 만든다.

- `is_valid_check()` / `test_produced_car()`: [DOMAIN.md](DOMAIN.md)의 제약 조건 5가지에 대해
  통과/실패 케이스를 각각 테스트 (동일 로직이 두 함수에 중복돼 있으므로 둘 다 커버)
- `select_car_type/engine/brake/steering(a)`: 각 전역 변수(`q0`~`q3`)에 올바른 값이 기록되는지
- `is_valid_range(step, ans)`: 각 step별 유효 범위 경계값(최소/최대/범위 밖) 테스트
- `run_produced_car()`: 정상 조합/고장난 엔진/불가능 조합일 때 출력 분기 확인 (stdout 캡처, `capsys` 활용)
- CLI 입출력(`main()`, `input()`, `time.sleep`)은 특성화 대상에서 제외 — 순수 로직 함수 위주로 테스트하고,
  Phase 3에서 로직과 I/O가 분리되면 그때 별도로 다룬다.

이 단계의 테스트는 전역 변수(`q0`~`q3`)에 직접 값을 세팅해야 하므로, 테스트마다 `setup`/`teardown`으로
전역 상태를 초기화한다 (Phase 2에서 상태가 캡슐화되면 이 테스트들도 자연히 정리됨).

## Phase 2 — 중복 제거 / 가독성 수준의 리팩토링

아키텍처를 바꾸지 않는 범위에서, Phase 1의 테스트를 통과시킨 채로 코드를 정리한다.

1. **매직 넘버 → Enum**: `SEDAN/SUV/TRUCK`, `GM/TOYOTA/WIA`, `MANDO/CONTINENTAL/BOSCH_B`, `BOSCH_S/MOBIS`를
   `enum.Enum`으로 전환
2. **전역 변수 제거**: `q0`~`q3`를 하나의 `Car`(또는 `CarBuild`) 데이터 클래스로 캡슐화
3. **중복 제약 로직 통합**: `is_valid_check()`와 `test_produced_car()`에 중복된 5가지 제약 조건 판정을
   하나의 공용 함수로 추출해 두 함수가 재사용하도록 변경 (아직 규칙을 객체화하지는 않음)
4. **안전하지 않은 문법 제거**: `except:` bare except를 `except ValueError:`로 명시
5. **불필요한 분기/중복 출력 코드 정리**: `select_*`, `run_produced_car()` 등의 반복되는 `if/elif` 출력 패턴 단순화

## Phase 3 — 아키텍처 수준의 리팩토링

Phase 2로 정리된 코드를 기반으로 구조 자체를 바꾼다.

1. **팩토리 메서드 패턴으로 전환**: 차량 타입(Sedan/SUV/Truck)마다 별도의 Factory 클래스(예: `SedanFactory`,
   `SuvFactory`, `TruckFactory`)를 두고, 공통 인터페이스(예: `CarFactory`)의 팩토리 메서드가 해당 타입 전용
   호환성 규칙과 부품 조합 생성을 담당하도록 함. 새 차량 타입이 추가되면 `if/elif` 분기를 늘리는 대신
   새 Factory 서브클래스만 추가하면 되도록 만드는 것이 목표
2. **CLI(I/O)와 도메인 로직 분리**: `main()`/`show_menu()`/`input()`/`time.sleep()` 등 화면 처리 코드와
   조립·검증 로직을 별도 모듈/함수로 분리해, 도메인 로직을 I/O 없이 단위 테스트 가능하게 만듦
3. **차량 타입/부품 확장성 검증**: 새 차량 타입이나 부품 하나를 추가하는 시나리오로 구조가 실제로
   확장 가능한지 확인 (필요 시 테스트 코드로 남김)

## 마무리

- 리팩토링 후 구조를 [CODE_STRUCTURE.md](CODE_STRUCTURE.md)에 반영
- Phase 3에서 나온 새 구조(Enum, 규칙 리스트 등)에 맞는 단위 테스트 추가 검토
- 커밋은 [../CLAUDE.md](../CLAUDE.md)의 커밋 컨벤션(`test:`, `refactor:` 등)을 따름
