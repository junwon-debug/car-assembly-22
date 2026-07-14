# CODE_STRUCTURE.md

리팩토링(Phase 1~3) 완료 후의 코드 구조를 설명한다. 도메인 규칙 자체는 [docs/DOMAIN.md](DOMAIN.md) 참고.

## 파일 구성

CLI(I/O)와 도메인 로직이 두 파일로 분리되어 있다. 실행 진입점은 여전히 `python assembly.py`다.

- **`domain.py`**: I/O(대화형 `input()`/`time.sleep()`) 없이 단독으로 import 가능한 순수 도메인 로직
- **`assembly.py`**: CLI 화면 처리와 사용자 입력 루프. `import domain`으로 도메인 로직을 사용
- **`test_domain.py`** / **`test_assembly.py`** / **`test_extensibility.py`**: 각각 도메인 로직, CLI, 확장성
  시나리오를 검증하는 pytest 테스트

## domain.py

- `CarType` / `Engine` / `Brake` / `Steering`: 매직 넘버를 대체하는 `IntEnum`. 기존 코드와의 호환을 위해
  `SEDAN`, `GM`, `MANDO`, `BOSCH_S` 등 모듈 레벨 별칭도 함께 제공
- `Car`: 차량 조립 상태(`car_type`/`engine`/`brake`/`steering`)를 담는 `@dataclass`. 모듈 전역 `car` 인스턴스가
  현재 조립 중인 차량 하나를 표현한다 (과거 전역 변수 `q0~q3`를 대체)
- `CarFactory`(추상 베이스) / `SedanFactory` / `SuvFactory` / `TruckFactory`: 팩토리 메서드 패턴.
  - `create(engine, brake, steering) -> Car`: 완성된 `Car` 생성
  - `find_violation(car) -> Optional[str]`: 해당 타입 **전용** 호환성 규칙만 검사 (예: `SedanFactory`는
    Continental 제동장치 금지만 검사)
  - `validate(car) -> Optional[str]`: 타입 전용 규칙(`find_violation`)을 먼저 검사한 뒤, 모든 타입에 공통인
    Bosch 제동장치↔Bosch 조향장치 규칙을 검사 (베이스 클래스에 구현, 서브클래스는 오버라이드 불필요)
  - `CAR_FACTORIES` 딕셔너리 + `get_factory(car_type)`: `CarType` → Factory 인스턴스 조회. **새 차량 타입이
    추가되면 새 Factory 서브클래스를 만들고 이 딕셔너리에 한 줄만 추가하면 되며, 기존 코드의 if/elif 분기를
    수정할 필요가 없다** ([test_extensibility.py](../test_extensibility.py)로 검증됨)
- `select_car_type/engine/brake/steering(a)`: 전역 `car`의 필드에 값 세팅 + 안내 메시지 출력 (Enum→메시지
  딕셔너리 기반, if/elif 없음)
- `is_valid_check()` / `run_produced_car()` / `test_produced_car()`: `get_factory(car.car_type).validate(car)`를
  통해 조합 가능 여부를 판정하고 결과를 출력. 과거 두 함수에 중복돼 있던 5가지 제약 조건 로직은
  `CarFactory` 계층으로 단일화됨

## assembly.py

- `show_menu(step)` / `is_valid_range(step, ans)`: 단계별 메뉴 출력과 입력값 범위 검증
- `delay(ms)` / `clear()`: CLI 화면 갱신을 위한 보조 함수
- `main()`: `step`(0~4) 값을 기준으로 한 단계 상태 머신으로 CLI 입력을 순환 처리하며, 내부적으로
  `domain.select_*`/`domain.run_produced_car`/`domain.test_produced_car`를 호출. 숫자 변환 실패는
  `except ValueError:`로 명시적으로 처리 (bare `except:` 제거)
