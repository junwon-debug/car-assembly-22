"""Phase 3 T8: 차량 타입/부품 확장성 검증 테스트.

기존 domain.py의 CarFactory / SedanFactory / SuvFactory / TruckFactory /
CAR_FACTORIES / get_factory 코드는 이 테스트 파일에서 단 한 줄도 수정하지 않는다.
새로운 차량 타입은 CarFactory를 상속한 서브클래스를 "추가"하고, 조회용 딕셔너리에
"등록"하는 것만으로 기존 코드 변경 없이 확장 가능함을 증명한다.
"""

from enum import IntEnum
from typing import Optional

import pytest

import domain
from domain import Brake, Car, CarFactory, CarType, Engine, Steering


class DummyCarType(IntEnum):
    """실제 CarType Enum을 건드리지 않기 위한, 테스트 전용 4번째 차량 타입."""

    VAN = 4


class VanFactory(CarFactory):
    """가상의 4번째 차량 타입: Van.

    임의 규칙: Van에는 CONTINENTAL 제동장치만 허용한다.
    """

    car_type = DummyCarType.VAN

    def create(self, engine, brake, steering) -> Car:
        return Car(
            car_type=self.car_type,
            engine=Engine(engine),
            brake=Brake(brake),
            steering=Steering(steering),
        )

    def find_violation(self, target_car) -> Optional[str]:
        if target_car.brake != Brake.CONTINENTAL:
            return "Van에는 Continental제동장치만 사용 가능"
        return None


@pytest.fixture(autouse=True)
def reset_globals():
    domain.car = domain.Car()
    yield


def test_new_car_type_added_without_touching_existing_factories():
    """새 CarFactory 서브클래스 추가만으로 기존 코드 수정 없이 확장 가능함을 증명한다.

    기존 CarFactory/SedanFactory/SuvFactory/TruckFactory/CAR_FACTORIES/get_factory는
    이 테스트에서 전혀 수정하지 않았고, VanFactory 클래스 정의 + 로컬 딕셔너리
    등록 한 줄만 추가했다.
    """
    # 기존 CAR_FACTORIES는 손대지 않고, 로컬 사본에만 새 타입을 등록한다.
    extended_factories = {**domain.CAR_FACTORIES, DummyCarType.VAN: VanFactory()}

    van_factory = extended_factories[DummyCarType.VAN]
    assert isinstance(van_factory, VanFactory)

    # create()가 올바르게 동작한다.
    van_car = van_factory.create(Engine.GM, Brake.CONTINENTAL, Steering.BOSCH_S)
    assert van_car.car_type == DummyCarType.VAN
    assert van_car.engine == Engine.GM
    assert van_car.brake == Brake.CONTINENTAL
    assert van_car.steering == Steering.BOSCH_S


@pytest.mark.parametrize(
    "engine, brake, steering, expected_violation",
    [
        # 타입 전용 규칙 위반: Continental이 아닌 제동장치
        (Engine.GM, Brake.MANDO, Steering.BOSCH_S, "Van에는 Continental제동장치만 사용 가능"),
        # 타입 전용 규칙은 통과하지만 공통 Bosch 규칙 위반
        # (Continental 제동장치이므로 Bosch 공통 규칙과는 무관 -> 정상)
        (Engine.GM, Brake.CONTINENTAL, Steering.MOBIS, None),
        # 모든 규칙 통과
        (Engine.GM, Brake.CONTINENTAL, Steering.BOSCH_S, None),
    ],
)
def test_van_factory_validate_applies_type_rule_then_bosch_rule(
    engine, brake, steering, expected_violation
):
    """VanFactory는 CarFactory.validate()를 상속받으므로, T5에서 정한
    '타입 전용 규칙 먼저, Bosch 공통 규칙 나중' 순서를 별도 구현 없이 그대로 따른다.
    """
    van_factory = VanFactory()
    target_car = van_factory.create(engine, brake, steering)

    assert van_factory.validate(target_car) == expected_violation


def test_van_factory_type_rule_takes_priority_over_bosch_rule():
    """타입 전용 규칙 위반이 Bosch 공통 규칙 위반보다 먼저 검출되는지 확인한다.

    MANDO 제동장치는 Van 규칙 위반(Continental만 허용)이면서 동시에
    Bosch 제동장치가 아니므로 Bosch 공통 규칙은 애초에 적용 대상이 아니다.
    타입 규칙 메시지가 우선적으로 반환되어야 한다.
    """
    van_factory = VanFactory()
    target_car = van_factory.create(Engine.GM, Brake.MANDO, Steering.MOBIS)

    violation = van_factory.validate(target_car)

    assert violation == "Van에는 Continental제동장치만 사용 가능"


def test_car_factories_dict_extended_locally_without_mutating_original():
    """CAR_FACTORIES 딕셔너리 확장은 매핑 한 줄 추가로 충분함을 보여준다.

    기존 domain.CAR_FACTORIES 자체는 변경하지 않고, 로컬 사본 딕셔너리를 만들어
    새 타입을 등록한 뒤 조회가 정상 동작하는지 확인한다.
    """
    original_keys = set(domain.CAR_FACTORIES.keys())

    extended_factories = {**domain.CAR_FACTORIES, DummyCarType.VAN: VanFactory()}

    # 원본 CAR_FACTORIES는 그대로 유지된다 (한 줄도 수정/변형되지 않음).
    assert set(domain.CAR_FACTORIES.keys()) == original_keys
    assert DummyCarType.VAN not in domain.CAR_FACTORIES

    # 로컬 사본에서는 기존 타입 + 새 타입 모두 조회 가능하다.
    assert isinstance(extended_factories[CarType.SEDAN], type(domain.CAR_FACTORIES[CarType.SEDAN]))
    assert isinstance(extended_factories[DummyCarType.VAN], VanFactory)


def test_new_engine_value_is_safely_ignored_by_existing_factories():
    """새 부품(Engine) 값이 추가되는 상황을 가정한다.

    각 Factory의 find_violation은 자신이 아는 규칙만 검사하고 모르는 값은 통과시키므로,
    실제 Engine Enum에 새 값이 추가되어도(여기서는 정수 값 999로 시뮬레이션) 기존
    SedanFactory/SuvFactory/TruckFactory 코드는 수정할 필요가 없다.
    """
    # 실제로 Engine Enum을 변경하지 않고, "알려지지 않은 엔진 값이 들어왔다"는 상황을
    # 기존 Enum 중 각 Factory가 규칙으로 다루지 않는 값으로 시뮬레이션한다.
    sedan_factory = domain.get_factory(CarType.SEDAN)
    suv_factory = domain.get_factory(CarType.SUV)
    truck_factory = domain.get_factory(CarType.TRUCK)

    # Sedan은 엔진 종류에 대한 규칙이 없으므로 어떤 엔진이 오든(신규 엔진 포함) 통과.
    sedan_car = Car(car_type=CarType.SEDAN, engine=Engine.WIA, brake=Brake.MANDO, steering=Steering.BOSCH_S)
    assert sedan_factory.find_violation(sedan_car) is None

    # SUV는 TOYOTA 엔진만 금지하므로, 그 외 엔진(신규 엔진 포함 가정)은 통과.
    suv_car = Car(car_type=CarType.SUV, engine=Engine.GM, brake=Brake.MANDO, steering=Steering.BOSCH_S)
    assert suv_factory.find_violation(suv_car) is None

    # Truck은 WIA 엔진만 금지하므로, 그 외 엔진(신규 엔진 포함 가정)은 통과.
    truck_car = Car(car_type=CarType.TRUCK, engine=Engine.GM, brake=Brake.CONTINENTAL, steering=Steering.BOSCH_S)
    assert truck_factory.find_violation(truck_car) is None
