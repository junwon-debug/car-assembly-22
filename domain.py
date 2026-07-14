from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional


class CarType(IntEnum):
    SEDAN = 1
    SUV = 2
    TRUCK = 3


class Engine(IntEnum):
    GM = 1
    TOYOTA = 2
    WIA = 3
    BROKEN = 4


class Brake(IntEnum):
    MANDO = 1
    CONTINENTAL = 2
    BOSCH_B = 3


class Steering(IntEnum):
    BOSCH_S = 1
    MOBIS = 2


SEDAN = CarType.SEDAN
SUV = CarType.SUV
TRUCK = CarType.TRUCK

GM = Engine.GM
TOYOTA = Engine.TOYOTA
WIA = Engine.WIA

MANDO = Brake.MANDO
CONTINENTAL = Brake.CONTINENTAL
BOSCH_B = Brake.BOSCH_B

BOSCH_S = Steering.BOSCH_S
MOBIS = Steering.MOBIS


@dataclass
class Car:
    car_type: Optional[CarType] = None
    engine: Optional[Engine] = None
    brake: Optional[Brake] = None
    steering: Optional[Steering] = None


car = Car()


class CarFactory(ABC):
    """차량 타입별 생성 + 해당 타입 전용 호환성 검증을 전담하는 팩토리 인터페이스."""

    car_type: CarType

    @abstractmethod
    def create(self, engine, brake, steering) -> Car:
        ...

    @abstractmethod
    def find_violation(self, target_car) -> Optional[str]:
        """이 차량 타입 전용 호환성 규칙만 검사. 위반 시 메시지, 통과 시 None."""
        ...

    def validate(self, target_car) -> Optional[str]:
        """타입 전용 규칙(find_violation)을 먼저 검사한 뒤, 공통 규칙(Bosch 제동장치는 Bosch 조향장치와만 호환)을 검사."""
        violation = self.find_violation(target_car)
        if violation is not None:
            return violation
        if target_car.brake == Brake.BOSCH_B and target_car.steering != Steering.BOSCH_S:
            return "Bosch제동장치에는 Bosch조향장치 이외 사용 불가"
        return None


class SedanFactory(CarFactory):
    car_type = CarType.SEDAN

    def create(self, engine, brake, steering) -> Car:
        return Car(car_type=self.car_type, engine=Engine(engine), brake=Brake(brake), steering=Steering(steering))

    def find_violation(self, target_car) -> Optional[str]:
        if target_car.brake == Brake.CONTINENTAL:
            return "Sedan에는 Continental제동장치 사용 불가"
        return None


class SuvFactory(CarFactory):
    car_type = CarType.SUV

    def create(self, engine, brake, steering) -> Car:
        return Car(car_type=self.car_type, engine=Engine(engine), brake=Brake(brake), steering=Steering(steering))

    def find_violation(self, target_car) -> Optional[str]:
        if target_car.engine == Engine.TOYOTA:
            return "SUV에는 TOYOTA엔진 사용 불가"
        return None


class TruckFactory(CarFactory):
    car_type = CarType.TRUCK

    def create(self, engine, brake, steering) -> Car:
        return Car(car_type=self.car_type, engine=Engine(engine), brake=Brake(brake), steering=Steering(steering))

    def find_violation(self, target_car) -> Optional[str]:
        if target_car.engine == Engine.WIA:
            return "Truck에는 WIA엔진 사용 불가"
        if target_car.brake == Brake.MANDO:
            return "Truck에는 Mando제동장치 사용 불가"
        return None


CAR_FACTORIES = {
    CarType.SEDAN: SedanFactory(),
    CarType.SUV: SuvFactory(),
    CarType.TRUCK: TruckFactory(),
}


def get_factory(car_type: CarType) -> CarFactory:
    """CarType Enum 값으로부터 알맞은 CarFactory 인스턴스를 조회한다."""
    return CAR_FACTORIES[car_type]


CAR_TYPE_SELECT_MESSAGES = {
    CarType.SEDAN: "차량 타입으로 Sedan을 선택하셨습니다.",
    CarType.SUV: "차량 타입으로 SUV을 선택하셨습니다.",
    CarType.TRUCK: "차량 타입으로 Truck을 선택하셨습니다.",
}

ENGINE_SELECT_MESSAGES = {
    Engine.GM: "GM 엔진을 선택하셨습니다.",
    Engine.TOYOTA: "TOYOTA 엔진을 선택하셨습니다.",
    Engine.WIA: "WIA 엔진을 선택하셨습니다.",
    Engine.BROKEN: "고장난 엔진을 선택하셨습니다.",
}

BRAKE_SELECT_MESSAGES = {
    Brake.MANDO: "MANDO 제동장치를 선택하셨습니다.",
    Brake.CONTINENTAL: "CONTINENTAL 제동장치를 선택하셨습니다.",
    Brake.BOSCH_B: "BOSCH 제동장치를 선택하셨습니다.",
}

STEERING_SELECT_MESSAGES = {
    Steering.BOSCH_S: "BOSCH 조향장치를 선택하셨습니다.",
    Steering.MOBIS: "MOBIS 조향장치를 선택하셨습니다.",
}

CAR_TYPE_LABELS = {CarType.SEDAN: "Sedan", CarType.SUV: "SUV", CarType.TRUCK: "Truck"}
ENGINE_LABELS = {Engine.GM: "GM", Engine.TOYOTA: "TOYOTA", Engine.WIA: "WIA"}
BRAKE_LABELS = {Brake.MANDO: "Mando", Brake.CONTINENTAL: "Continental", Brake.BOSCH_B: "Bosch"}
STEERING_LABELS = {Steering.BOSCH_S: "Bosch", Steering.MOBIS: "Mobis"}


def select_car_type(a):
    car.car_type = CarType(a)
    message = CAR_TYPE_SELECT_MESSAGES.get(car.car_type)
    if message:
        print(message)


def select_engine(a):
    car.engine = Engine(a)
    message = ENGINE_SELECT_MESSAGES.get(car.engine)
    if message:
        print(message)


def select_brake(a):
    car.brake = Brake(a)
    message = BRAKE_SELECT_MESSAGES.get(car.brake)
    if message:
        print(message)


def select_steering(a):
    car.steering = Steering(a)
    message = STEERING_SELECT_MESSAGES.get(car.steering)
    if message:
        print(message)


def is_valid_check():
    return get_factory(car.car_type).validate(car) is None


def run_produced_car():
    if not is_valid_check():
        print("자동차가 동작되지 않습니다")
        return
    if car.engine == Engine.BROKEN:
        print("엔진이 고장나있습니다.")
        print("자동차가 움직이지 않습니다.")
        return

    car_type_label = CAR_TYPE_LABELS.get(car.car_type)
    if car_type_label:
        print(f"Car Type : {car_type_label}")

    engine_label = ENGINE_LABELS.get(car.engine)
    if engine_label:
        print(f"Engine   : {engine_label}")

    brake_label = BRAKE_LABELS.get(car.brake)
    if brake_label:
        print(f"Brake    : {brake_label}")

    steering_label = STEERING_LABELS.get(car.steering)
    if steering_label:
        print(f"Steering : {steering_label}")

    print("자동차가 동작됩니다.")


def test_produced_car():
    violation = get_factory(car.car_type).validate(car)
    if violation is None:
        print("PASS")
    else:
        print(f"FAIL\n{violation}")
