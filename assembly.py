import time
import sys
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

CLEAR_SCREEN = "\033[H\033[2J"


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

def delay(ms):
    t = ms / 1000.0
    time.sleep(t)

def clear():
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()

def show_menu(step):
    clear()
    if step == 0:
        print("        ______________")
        print("       /|            |")
        print("  ____/_|_____________|____")
        print(" |                      O  |")
        print(" '-(@)----------------(@)--'")
        print("===============================")
        print("어떤 차량 타입을 선택할까요?")
        print("1. Sedan")
        print("2. SUV")
        print("3. Truck")
    elif step == 1:
        print("어떤 엔진을 탑재할까요?")
        print("0. 뒤로가기")
        print("1. GM")
        print("2. TOYOTA")
        print("3. WIA")
        print("4. 고장난 엔진")
    elif step == 2:
        print("어떤 제동장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. MANDO")
        print("2. CONTINENTAL")
        print("3. BOSCH")
    elif step == 3:
        print("어떤 조향장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. BOSCH")
        print("2. MOBIS")
    elif step == 4:
        print("멋진 차량이 완성되었습니다.")
        print("0. 처음 화면으로 돌아가기")
        print("1. RUN")
        print("2. Test")
    print("===============================")

def is_valid_range(step, ans):
    if step == 0:
        if ans < 1 or ans > 3:
            print("ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능")
            return False
    if step == 1:
        if ans < 0 or ans > 4:
            print("ERROR :: 엔진은 1 ~ 4 범위만 선택 가능")
            return False
    if step == 2:
        if ans < 0 or ans > 3:
            print("ERROR :: 제동장치는 1 ~ 3 범위만 선택 가능")
            return False
    if step == 3:
        if ans < 0 or ans > 2:
            print("ERROR :: 조향장치는 1 ~ 2 범위만 선택 가능")
            return False
    if step == 4:
        if ans < 0 or ans > 2:
            print("ERROR :: Run 또는 Test 중 하나를 선택 필요")
            return False
    return True

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

def find_constraint_violation(target_car):
    if target_car.car_type == SEDAN and target_car.brake == CONTINENTAL:
        return "Sedan에는 Continental제동장치 사용 불가"
    if target_car.car_type == SUV and target_car.engine == TOYOTA:
        return "SUV에는 TOYOTA엔진 사용 불가"
    if target_car.car_type == TRUCK and target_car.engine == WIA:
        return "Truck에는 WIA엔진 사용 불가"
    if target_car.car_type == TRUCK and target_car.brake == MANDO:
        return "Truck에는 Mando제동장치 사용 불가"
    if target_car.brake == BOSCH_B and target_car.steering != BOSCH_S:
        return "Bosch제동장치에는 Bosch조향장치 이외 사용 불가"
    return None

def is_valid_check():
    return find_constraint_violation(car) is None

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
    violation = find_constraint_violation(car)
    if violation is None:
        print("PASS")
    else:
        print(f"FAIL\n{violation}")

def main():
    step = 0
    while True:
        show_menu(step)
        buf = input("INPUT > ").strip()

        if buf == "exit":
            print("바이바이")
            break

        try:
            ans = int(buf)
        except ValueError:
            print("ERROR :: 숫자만 입력 가능")
            delay(800)
            continue

        if not is_valid_range(step, ans):
            delay(800)
            continue

        if ans == 0:
            if step == 4:
                step = 0
            elif step > 0:
                step = step - 1
            continue

        if step == 0:
            select_car_type(ans)
            delay(800)
            step = 1
        elif step == 1:
            select_engine(ans)
            delay(800)
            step = 2
        elif step == 2:
            select_brake(ans)
            delay(800)
            step = 3
        elif step == 3:
            select_steering(ans)
            delay(800)
            step = 4
        elif step == 4:
            if ans == 1:
                run_produced_car()
                delay(2000)
            elif ans == 2:
                print("Test...")
                delay(1500)
                test_produced_car()
                delay(2000)

if __name__ == "__main__":
    main()