import pytest

import assembly


@pytest.fixture(autouse=True)
def reset_globals():
    """매 테스트 실행 전 assembly 모듈의 전역 상태(q0~q4)를 0으로 리셋한다."""
    assembly.q0 = 0
    assembly.q1 = 0
    assembly.q2 = 0
    assembly.q3 = 0
    assembly.q4 = 0
    yield


def test_reset_globals_sets_all_state_to_zero():
    assert assembly.q0 == 0
    assert assembly.q1 == 0
    assert assembly.q2 == 0
    assert assembly.q3 == 0
    assert assembly.q4 == 0


def test_reset_globals_mutates_previous_state_before_next_test():
    # 이전 테스트 실행 중 상태를 임의로 오염시킨다.
    assembly.q0 = 99
    assembly.q1 = 99
    assembly.q2 = 99
    assembly.q3 = 99
    assembly.q4 = 99
    assert assembly.q0 == 99


def test_reset_globals_actually_resets_after_pollution():
    # 직전 테스트에서 오염시킨 상태가 fixture에 의해 리셋되었는지 확인한다.
    assert assembly.q0 == 0
    assert assembly.q1 == 0
    assert assembly.q2 == 0
    assert assembly.q3 == 0
    assert assembly.q4 == 0


@pytest.mark.parametrize(
    "q0, q1, q2, q3, expected",
    [
        # 1. Sedan + Continental 제동장치 조합 불가
        (assembly.SEDAN, assembly.GM, assembly.CONTINENTAL, assembly.BOSCH_S, False),
        # 2. SUV + TOYOTA 엔진 조합 불가
        (assembly.SUV, assembly.TOYOTA, assembly.MANDO, assembly.BOSCH_S, False),
        # 3. Truck + WIA 엔진 조합 불가
        (assembly.TRUCK, assembly.WIA, assembly.CONTINENTAL, assembly.BOSCH_S, False),
        # 4. Truck + MANDO 제동장치 조합 불가
        (assembly.TRUCK, assembly.GM, assembly.MANDO, assembly.BOSCH_S, False),
        # 5. Bosch 제동장치는 Bosch 조향장치와만 사용 가능
        (assembly.SEDAN, assembly.GM, assembly.BOSCH_B, assembly.MOBIS, False),
        # 정상 조합: 모든 제약 통과
        (assembly.SEDAN, assembly.GM, assembly.MANDO, assembly.BOSCH_S, True),
    ],
)
def test_is_valid_check(q0, q1, q2, q3, expected):
    assembly.q0 = q0
    assembly.q1 = q1
    assembly.q2 = q2
    assembly.q3 = q3

    assert assembly.is_valid_check() == expected


@pytest.mark.parametrize(
    "q0, q1, q2, q3, expected_output",
    [
        # 1. Sedan + Continental 제동장치 조합 불가
        (
            assembly.SEDAN,
            assembly.GM,
            assembly.CONTINENTAL,
            assembly.BOSCH_S,
            "FAIL\nSedan에는 Continental제동장치 사용 불가\n",
        ),
        # 2. SUV + TOYOTA 엔진 조합 불가
        (
            assembly.SUV,
            assembly.TOYOTA,
            assembly.MANDO,
            assembly.BOSCH_S,
            "FAIL\nSUV에는 TOYOTA엔진 사용 불가\n",
        ),
        # 3. Truck + WIA 엔진 조합 불가
        (
            assembly.TRUCK,
            assembly.WIA,
            assembly.CONTINENTAL,
            assembly.BOSCH_S,
            "FAIL\nTruck에는 WIA엔진 사용 불가\n",
        ),
        # 4. Truck + MANDO 제동장치 조합 불가
        (
            assembly.TRUCK,
            assembly.GM,
            assembly.MANDO,
            assembly.BOSCH_S,
            "FAIL\nTruck에는 Mando제동장치 사용 불가\n",
        ),
        # 5. Bosch 제동장치는 Bosch 조향장치와만 사용 가능
        (
            assembly.SEDAN,
            assembly.GM,
            assembly.BOSCH_B,
            assembly.MOBIS,
            "FAIL\nBosch제동장치에는 Bosch조향장치 이외 사용 불가\n",
        ),
        # 정상 조합: 모든 제약 통과
        (
            assembly.SEDAN,
            assembly.GM,
            assembly.MANDO,
            assembly.BOSCH_S,
            "PASS\n",
        ),
    ],
)
def test_produced_car(capsys, q0, q1, q2, q3, expected_output):
    assembly.q0 = q0
    assembly.q1 = q1
    assembly.q2 = q2
    assembly.q3 = q3

    assembly.test_produced_car()

    assert capsys.readouterr().out == expected_output


@pytest.mark.parametrize(
    "a, expected_output",
    [
        (assembly.SEDAN, "차량 타입으로 Sedan을 선택하셨습니다.\n"),
        (assembly.SUV, "차량 타입으로 SUV을 선택하셨습니다.\n"),
        (assembly.TRUCK, "차량 타입으로 Truck을 선택하셨습니다.\n"),
    ],
)
def test_select_car_type(capsys, a, expected_output):
    assembly.select_car_type(a)

    assert assembly.q0 == a
    assert capsys.readouterr().out == expected_output


@pytest.mark.parametrize(
    "a, expected_output",
    [
        (assembly.GM, "GM 엔진을 선택하셨습니다.\n"),
        (assembly.TOYOTA, "TOYOTA 엔진을 선택하셨습니다.\n"),
        (assembly.WIA, "WIA 엔진을 선택하셨습니다.\n"),
        (4, "고장난 엔진을 선택하셨습니다.\n"),
    ],
)
def test_select_engine(capsys, a, expected_output):
    assembly.select_engine(a)

    assert assembly.q1 == a
    assert capsys.readouterr().out == expected_output


@pytest.mark.parametrize(
    "a, expected_output",
    [
        (assembly.MANDO, "MANDO 제동장치를 선택하셨습니다.\n"),
        (assembly.CONTINENTAL, "CONTINENTAL 제동장치를 선택하셨습니다.\n"),
        (assembly.BOSCH_B, "BOSCH 제동장치를 선택하셨습니다.\n"),
    ],
)
def test_select_brake(capsys, a, expected_output):
    assembly.select_brake(a)

    assert assembly.q2 == a
    assert capsys.readouterr().out == expected_output


@pytest.mark.parametrize(
    "a, expected_output",
    [
        (assembly.BOSCH_S, "BOSCH 조향장치를 선택하셨습니다.\n"),
        (assembly.MOBIS, "MOBIS 조향장치를 선택하셨습니다.\n"),
    ],
)
def test_select_steering(capsys, a, expected_output):
    assembly.select_steering(a)

    assert assembly.q3 == a
    assert capsys.readouterr().out == expected_output


@pytest.mark.parametrize(
    "step, ans, expected",
    [
        # step 0: 차량 타입 (1 ~ 3 범위만 유효, 0은 무효)
        (0, 1, True),
        (0, 3, True),
        (0, 0, False),
        (0, 4, False),
        # step 1: 엔진 (0 ~ 4 범위만 유효)
        (1, 0, True),
        (1, 4, True),
        (1, -1, False),
        (1, 5, False),
        # step 2: 제동장치 (0 ~ 3 범위만 유효)
        (2, 0, True),
        (2, 3, True),
        (2, -1, False),
        (2, 4, False),
        # step 3: 조향장치 (0 ~ 2 범위만 유효)
        (3, 0, True),
        (3, 2, True),
        (3, -1, False),
        (3, 3, False),
        # step 4: Run/Test 선택 (0 ~ 2 범위만 유효)
        (4, 0, True),
        (4, 2, True),
        (4, -1, False),
        (4, 3, False),
    ],
)
def test_is_valid_range(capsys, step, ans, expected):
    result = assembly.is_valid_range(step, ans)

    assert result == expected

    out = capsys.readouterr().out
    if expected:
        assert out == ""
    else:
        assert "ERROR" in out


def test_run_produced_car_invalid_combination_only_shows_failure_message(capsys):
    """제약 위반 조합에서는 '자동차가 동작되지 않습니다'만 출력되고
    Car Type 등 필드 라인은 전혀 출력되지 않는다."""
    assembly.q0 = assembly.SEDAN
    assembly.q1 = assembly.GM
    assembly.q2 = assembly.CONTINENTAL
    assembly.q3 = assembly.BOSCH_S

    assembly.run_produced_car()

    out = capsys.readouterr().out
    assert out == "자동차가 동작되지 않습니다\n"
    assert "Car Type" not in out
    assert "Engine" not in out
    assert "Brake" not in out
    assert "Steering" not in out


def test_run_produced_car_valid_combination_with_broken_engine(capsys):
    """유효한 조합이더라도 엔진이 고장난 경우(q1=4)에는 is_valid_check를 통과한 뒤
    별도의 엔진 고장 체크에서 걸려 필드 라인 없이 고장 메시지만 출력된다."""
    assembly.q0 = assembly.SEDAN
    assembly.q1 = 4
    assembly.q2 = assembly.MANDO
    assembly.q3 = assembly.BOSCH_S

    assembly.run_produced_car()

    out = capsys.readouterr().out
    assert out == "엔진이 고장나있습니다.\n자동차가 움직이지 않습니다.\n"
    assert "Car Type" not in out
    assert "Engine" not in out
    assert "Brake" not in out
    assert "Steering" not in out


def test_run_produced_car_fully_valid_combination_prints_all_fields_in_order(capsys):
    """완전히 정상적인 조합에서는 Car Type, Engine, Brake, Steering,
    동작 완료 메시지가 정확한 라벨과 순서로 출력된다."""
    assembly.q0 = assembly.SEDAN
    assembly.q1 = assembly.GM
    assembly.q2 = assembly.MANDO
    assembly.q3 = assembly.BOSCH_S

    assembly.run_produced_car()

    out = capsys.readouterr().out
    assert out == (
        "Car Type : Sedan\n"
        "Engine   : GM\n"
        "Brake    : Mando\n"
        "Steering : Bosch\n"
        "자동차가 동작됩니다.\n"
    )


@pytest.mark.parametrize(
    "q0, q1, q2, q3, expected_output",
    [
        # SUV 타입 + Continental 제동장치 + Mobis 조향장치
        (
            assembly.SUV,
            assembly.GM,
            assembly.CONTINENTAL,
            assembly.MOBIS,
            "Car Type : SUV\n"
            "Engine   : GM\n"
            "Brake    : Continental\n"
            "Steering : Mobis\n"
            "자동차가 동작됩니다.\n",
        ),
        # Truck 타입 + Bosch 제동장치(+Bosch 조향장치 필수 조합)
        (
            assembly.TRUCK,
            assembly.GM,
            assembly.BOSCH_B,
            assembly.BOSCH_S,
            "Car Type : Truck\n"
            "Engine   : GM\n"
            "Brake    : Bosch\n"
            "Steering : Bosch\n"
            "자동차가 동작됩니다.\n",
        ),
        # TOYOTA 엔진
        (
            assembly.SEDAN,
            assembly.TOYOTA,
            assembly.MANDO,
            assembly.BOSCH_S,
            "Car Type : Sedan\n"
            "Engine   : TOYOTA\n"
            "Brake    : Mando\n"
            "Steering : Bosch\n"
            "자동차가 동작됩니다.\n",
        ),
        # WIA 엔진 (SUV와 조합, Truck+WIA는 제약 위반이므로 회피)
        (
            assembly.SUV,
            assembly.WIA,
            assembly.MANDO,
            assembly.MOBIS,
            "Car Type : SUV\n"
            "Engine   : WIA\n"
            "Brake    : Mando\n"
            "Steering : Mobis\n"
            "자동차가 동작됩니다.\n",
        ),
    ],
)
def test_run_produced_car_field_labels(capsys, q0, q1, q2, q3, expected_output):
    assembly.q0 = q0
    assembly.q1 = q1
    assembly.q2 = q2
    assembly.q3 = q3

    assembly.run_produced_car()

    assert capsys.readouterr().out == expected_output


def test_produced_car_elif_priority_only_first_matching_condition_reported(capsys):
    """q0=TRUCK, q1=WIA, q2=MANDO 처럼 조건3(WIA엔진)과 조건4(Mando제동장치)가
    동시에 성립 가능한 조합에서, if/elif 체인 구조상 먼저 나오는 조건3의
    메시지만 출력되고 조건4의 메시지는 출력되지 않는다는 것을 특성화한다."""
    assembly.q0 = assembly.TRUCK
    assembly.q1 = assembly.WIA
    assembly.q2 = assembly.MANDO
    assembly.q3 = assembly.BOSCH_S

    assembly.test_produced_car()

    out = capsys.readouterr().out
    assert out == "FAIL\nTruck에는 WIA엔진 사용 불가\n"
    assert "Mando제동장치" not in out
