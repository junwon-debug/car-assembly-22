import pytest

import domain


@pytest.fixture(autouse=True)
def reset_globals():
    """매 테스트 실행 전 domain 모듈의 전역 car 인스턴스를 새로 만들어 리셋한다."""
    domain.car = domain.Car()
    yield


def test_reset_car_fixture_provides_fresh_car_between_tests():
    # 이 테스트에서 전역 car 상태를 오염시킨다.
    domain.car.car_type = domain.CarType.SUV
    domain.car.engine = domain.Engine.TOYOTA
    domain.car.brake = domain.Brake.CONTINENTAL
    domain.car.steering = domain.Steering.MOBIS
    assert domain.car.car_type == domain.CarType.SUV

    # fixture가 재실행되며 새 Car 인스턴스를 만든 것처럼 검증한다.
    domain.car = domain.Car()
    assert domain.car.car_type is None
    assert domain.car.engine is None
    assert domain.car.brake is None
    assert domain.car.steering is None


@pytest.mark.parametrize(
    "q0, q1, q2, q3, expected",
    [
        # 1. Sedan + Continental 제동장치 조합 불가
        (domain.SEDAN, domain.GM, domain.CONTINENTAL, domain.BOSCH_S, False),
        # 2. SUV + TOYOTA 엔진 조합 불가
        (domain.SUV, domain.TOYOTA, domain.MANDO, domain.BOSCH_S, False),
        # 3. Truck + WIA 엔진 조합 불가
        (domain.TRUCK, domain.WIA, domain.CONTINENTAL, domain.BOSCH_S, False),
        # 4. Truck + MANDO 제동장치 조합 불가
        (domain.TRUCK, domain.GM, domain.MANDO, domain.BOSCH_S, False),
        # 5. Bosch 제동장치는 Bosch 조향장치와만 사용 가능
        (domain.SEDAN, domain.GM, domain.BOSCH_B, domain.MOBIS, False),
        # 정상 조합: 모든 제약 통과
        (domain.SEDAN, domain.GM, domain.MANDO, domain.BOSCH_S, True),
    ],
)
def test_is_valid_check(q0, q1, q2, q3, expected):
    domain.car.car_type = q0
    domain.car.engine = q1
    domain.car.brake = q2
    domain.car.steering = q3

    assert domain.is_valid_check() == expected


@pytest.mark.parametrize(
    "q0, q1, q2, q3, expected_output",
    [
        # 1. Sedan + Continental 제동장치 조합 불가
        (
            domain.SEDAN,
            domain.GM,
            domain.CONTINENTAL,
            domain.BOSCH_S,
            "FAIL\nSedan에는 Continental제동장치 사용 불가\n",
        ),
        # 2. SUV + TOYOTA 엔진 조합 불가
        (
            domain.SUV,
            domain.TOYOTA,
            domain.MANDO,
            domain.BOSCH_S,
            "FAIL\nSUV에는 TOYOTA엔진 사용 불가\n",
        ),
        # 3. Truck + WIA 엔진 조합 불가
        (
            domain.TRUCK,
            domain.WIA,
            domain.CONTINENTAL,
            domain.BOSCH_S,
            "FAIL\nTruck에는 WIA엔진 사용 불가\n",
        ),
        # 4. Truck + MANDO 제동장치 조합 불가
        (
            domain.TRUCK,
            domain.GM,
            domain.MANDO,
            domain.BOSCH_S,
            "FAIL\nTruck에는 Mando제동장치 사용 불가\n",
        ),
        # 5. Bosch 제동장치는 Bosch 조향장치와만 사용 가능
        (
            domain.SEDAN,
            domain.GM,
            domain.BOSCH_B,
            domain.MOBIS,
            "FAIL\nBosch제동장치에는 Bosch조향장치 이외 사용 불가\n",
        ),
        # 정상 조합: 모든 제약 통과
        (
            domain.SEDAN,
            domain.GM,
            domain.MANDO,
            domain.BOSCH_S,
            "PASS\n",
        ),
    ],
)
def test_produced_car(capsys, q0, q1, q2, q3, expected_output):
    domain.car.car_type = q0
    domain.car.engine = q1
    domain.car.brake = q2
    domain.car.steering = q3

    domain.test_produced_car()

    assert capsys.readouterr().out == expected_output


@pytest.mark.parametrize(
    "a, expected_output",
    [
        (domain.SEDAN, "차량 타입으로 Sedan을 선택하셨습니다.\n"),
        (domain.SUV, "차량 타입으로 SUV을 선택하셨습니다.\n"),
        (domain.TRUCK, "차량 타입으로 Truck을 선택하셨습니다.\n"),
    ],
)
def test_select_car_type(capsys, a, expected_output):
    domain.select_car_type(a)

    assert domain.car.car_type == a
    assert capsys.readouterr().out == expected_output


@pytest.mark.parametrize(
    "a, expected_output",
    [
        (domain.GM, "GM 엔진을 선택하셨습니다.\n"),
        (domain.TOYOTA, "TOYOTA 엔진을 선택하셨습니다.\n"),
        (domain.WIA, "WIA 엔진을 선택하셨습니다.\n"),
        (4, "고장난 엔진을 선택하셨습니다.\n"),
    ],
)
def test_select_engine(capsys, a, expected_output):
    domain.select_engine(a)

    assert domain.car.engine == a
    assert capsys.readouterr().out == expected_output


@pytest.mark.parametrize(
    "a, expected_output",
    [
        (domain.MANDO, "MANDO 제동장치를 선택하셨습니다.\n"),
        (domain.CONTINENTAL, "CONTINENTAL 제동장치를 선택하셨습니다.\n"),
        (domain.BOSCH_B, "BOSCH 제동장치를 선택하셨습니다.\n"),
    ],
)
def test_select_brake(capsys, a, expected_output):
    domain.select_brake(a)

    assert domain.car.brake == a
    assert capsys.readouterr().out == expected_output


@pytest.mark.parametrize(
    "a, expected_output",
    [
        (domain.BOSCH_S, "BOSCH 조향장치를 선택하셨습니다.\n"),
        (domain.MOBIS, "MOBIS 조향장치를 선택하셨습니다.\n"),
    ],
)
def test_select_steering(capsys, a, expected_output):
    domain.select_steering(a)

    assert domain.car.steering == a
    assert capsys.readouterr().out == expected_output


def test_run_produced_car_invalid_combination_only_shows_failure_message(capsys):
    """제약 위반 조합에서는 '자동차가 동작되지 않습니다'만 출력되고
    Car Type 등 필드 라인은 전혀 출력되지 않는다."""
    domain.car.car_type = domain.SEDAN
    domain.car.engine = domain.GM
    domain.car.brake = domain.CONTINENTAL
    domain.car.steering = domain.BOSCH_S

    domain.run_produced_car()

    out = capsys.readouterr().out
    assert out == "자동차가 동작되지 않습니다\n"
    assert "Car Type" not in out
    assert "Engine" not in out
    assert "Brake" not in out
    assert "Steering" not in out


def test_run_produced_car_valid_combination_with_broken_engine(capsys):
    """유효한 조합이더라도 엔진이 고장난 경우(q1=4)에는 is_valid_check를 통과한 뒤
    별도의 엔진 고장 체크에서 걸려 필드 라인 없이 고장 메시지만 출력된다."""
    domain.car.car_type = domain.SEDAN
    domain.car.engine = 4
    domain.car.brake = domain.MANDO
    domain.car.steering = domain.BOSCH_S

    domain.run_produced_car()

    out = capsys.readouterr().out
    assert out == "엔진이 고장나있습니다.\n자동차가 움직이지 않습니다.\n"
    assert "Car Type" not in out
    assert "Engine" not in out
    assert "Brake" not in out
    assert "Steering" not in out


def test_run_produced_car_fully_valid_combination_prints_all_fields_in_order(capsys):
    """완전히 정상적인 조합에서는 Car Type, Engine, Brake, Steering,
    동작 완료 메시지가 정확한 라벨과 순서로 출력된다."""
    domain.car.car_type = domain.SEDAN
    domain.car.engine = domain.GM
    domain.car.brake = domain.MANDO
    domain.car.steering = domain.BOSCH_S

    domain.run_produced_car()

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
            domain.SUV,
            domain.GM,
            domain.CONTINENTAL,
            domain.MOBIS,
            "Car Type : SUV\n"
            "Engine   : GM\n"
            "Brake    : Continental\n"
            "Steering : Mobis\n"
            "자동차가 동작됩니다.\n",
        ),
        # Truck 타입 + Bosch 제동장치(+Bosch 조향장치 필수 조합)
        (
            domain.TRUCK,
            domain.GM,
            domain.BOSCH_B,
            domain.BOSCH_S,
            "Car Type : Truck\n"
            "Engine   : GM\n"
            "Brake    : Bosch\n"
            "Steering : Bosch\n"
            "자동차가 동작됩니다.\n",
        ),
        # TOYOTA 엔진
        (
            domain.SEDAN,
            domain.TOYOTA,
            domain.MANDO,
            domain.BOSCH_S,
            "Car Type : Sedan\n"
            "Engine   : TOYOTA\n"
            "Brake    : Mando\n"
            "Steering : Bosch\n"
            "자동차가 동작됩니다.\n",
        ),
        # WIA 엔진 (SUV와 조합, Truck+WIA는 제약 위반이므로 회피)
        (
            domain.SUV,
            domain.WIA,
            domain.MANDO,
            domain.MOBIS,
            "Car Type : SUV\n"
            "Engine   : WIA\n"
            "Brake    : Mando\n"
            "Steering : Mobis\n"
            "자동차가 동작됩니다.\n",
        ),
    ],
)
def test_run_produced_car_field_labels(capsys, q0, q1, q2, q3, expected_output):
    domain.car.car_type = q0
    domain.car.engine = q1
    domain.car.brake = q2
    domain.car.steering = q3

    domain.run_produced_car()

    assert capsys.readouterr().out == expected_output


@pytest.mark.parametrize(
    "enum_member, alias",
    [
        (domain.CarType.SEDAN, domain.SEDAN),
        (domain.CarType.SUV, domain.SUV),
        (domain.CarType.TRUCK, domain.TRUCK),
        (domain.Engine.GM, domain.GM),
        (domain.Engine.TOYOTA, domain.TOYOTA),
        (domain.Engine.WIA, domain.WIA),
        (domain.Brake.MANDO, domain.MANDO),
        (domain.Brake.CONTINENTAL, domain.CONTINENTAL),
        (domain.Brake.BOSCH_B, domain.BOSCH_B),
        (domain.Steering.BOSCH_S, domain.BOSCH_S),
        (domain.Steering.MOBIS, domain.MOBIS),
    ],
)
def test_enum_alias_matches_legacy_constant(enum_member, alias):
    assert enum_member == alias


@pytest.mark.parametrize(
    "value, enum_class",
    [
        (domain.SEDAN, domain.CarType),
        (domain.SUV, domain.CarType),
        (domain.TRUCK, domain.CarType),
        (domain.GM, domain.Engine),
        (domain.TOYOTA, domain.Engine),
        (domain.WIA, domain.Engine),
        (domain.MANDO, domain.Brake),
        (domain.CONTINENTAL, domain.Brake),
        (domain.BOSCH_B, domain.Brake),
        (domain.BOSCH_S, domain.Steering),
        (domain.MOBIS, domain.Steering),
    ],
)
def test_legacy_constant_is_instance_of_enum(value, enum_class):
    assert isinstance(value, enum_class)


def test_produced_car_elif_priority_only_first_matching_condition_reported(capsys):
    """q0=TRUCK, q1=WIA, q2=MANDO 처럼 조건3(WIA엔진)과 조건4(Mando제동장치)가
    동시에 성립 가능한 조합에서, if/elif 체인 구조상 먼저 나오는 조건3의
    메시지만 출력되고 조건4의 메시지는 출력되지 않는다는 것을 특성화한다."""
    domain.car.car_type = domain.TRUCK
    domain.car.engine = domain.WIA
    domain.car.brake = domain.MANDO
    domain.car.steering = domain.BOSCH_S

    domain.test_produced_car()

    out = capsys.readouterr().out
    assert out == "FAIL\nTruck에는 WIA엔진 사용 불가\n"
    assert "Mando제동장치" not in out


def test_car_default_construction_has_all_none_fields():
    car = domain.Car()
    assert car.car_type is None
    assert car.engine is None
    assert car.brake is None
    assert car.steering is None


def test_car_construction_with_keyword_arguments_sets_fields():
    car = domain.Car(
        car_type=domain.CarType.SEDAN,
        engine=domain.Engine.GM,
        brake=domain.Brake.MANDO,
        steering=domain.Steering.BOSCH_S,
    )
    assert car.car_type == domain.CarType.SEDAN
    assert car.engine == domain.Engine.GM
    assert car.brake == domain.Brake.MANDO
    assert car.steering == domain.Steering.BOSCH_S


def test_car_fields_are_mutable_after_construction():
    car = domain.Car()
    car.car_type = domain.CarType.SUV
    assert car.car_type == domain.CarType.SUV


class TestCarFactory:
    def test_car_factory_cannot_be_instantiated_directly(self):
        with pytest.raises(TypeError):
            domain.CarFactory()

    def test_subclass_missing_create_cannot_be_instantiated(self):
        class _MissingCreateFactory(domain.CarFactory):
            car_type = domain.CarType.SEDAN

            def find_violation(self, target_car):
                return None

        with pytest.raises(TypeError):
            _MissingCreateFactory()

    def test_subclass_missing_find_violation_cannot_be_instantiated(self):
        class _MissingFindViolationFactory(domain.CarFactory):
            car_type = domain.CarType.SEDAN

            def create(self, engine, brake, steering):
                return domain.Car()

        with pytest.raises(TypeError):
            _MissingFindViolationFactory()

    def test_fully_implemented_subclass_can_be_instantiated(self):
        class _AlwaysValidFactory(domain.CarFactory):
            car_type = domain.CarType.SEDAN

            def create(self, engine, brake, steering):
                return domain.Car(
                    car_type=self.car_type,
                    engine=domain.Engine(engine),
                    brake=domain.Brake(brake),
                    steering=domain.Steering(steering),
                )

            def find_violation(self, target_car):
                return None

        factory = _AlwaysValidFactory()
        assert isinstance(factory, domain.CarFactory)

    def test_validate_detects_common_bosch_brake_rule_violation(self):
        class _AlwaysValidFactory(domain.CarFactory):
            car_type = domain.CarType.SEDAN

            def create(self, engine, brake, steering):
                return domain.Car(
                    car_type=self.car_type,
                    engine=domain.Engine(engine),
                    brake=domain.Brake(brake),
                    steering=domain.Steering(steering),
                )

            def find_violation(self, target_car):
                return None

        factory = _AlwaysValidFactory()
        bad_car = domain.Car(
            car_type=domain.CarType.SEDAN,
            engine=domain.Engine.GM,
            brake=domain.Brake.BOSCH_B,
            steering=domain.Steering.MOBIS,
        )
        assert factory.validate(bad_car) == "Bosch제동장치에는 Bosch조향장치 이외 사용 불가"

    def test_validate_passes_for_valid_bosch_combination(self):
        class _AlwaysValidFactory(domain.CarFactory):
            car_type = domain.CarType.SEDAN

            def create(self, engine, brake, steering):
                return domain.Car(
                    car_type=self.car_type,
                    engine=domain.Engine(engine),
                    brake=domain.Brake(brake),
                    steering=domain.Steering(steering),
                )

            def find_violation(self, target_car):
                return None

        factory = _AlwaysValidFactory()
        good_car = domain.Car(
            car_type=domain.CarType.SEDAN,
            engine=domain.Engine.GM,
            brake=domain.Brake.BOSCH_B,
            steering=domain.Steering.BOSCH_S,
        )
        assert factory.validate(good_car) is None


class TestSedanFactory:
    def test_find_violation_detects_continental_brake(self):
        factory = domain.SedanFactory()
        bad_car = domain.Car(
            car_type=domain.CarType.SEDAN,
            engine=domain.Engine.GM,
            brake=domain.Brake.CONTINENTAL,
            steering=domain.Steering.BOSCH_S,
        )
        assert factory.find_violation(bad_car) == "Sedan에는 Continental제동장치 사용 불가"

    def test_find_violation_passes_for_valid_brake(self):
        factory = domain.SedanFactory()
        good_car = domain.Car(
            car_type=domain.CarType.SEDAN,
            engine=domain.Engine.GM,
            brake=domain.Brake.MANDO,
            steering=domain.Steering.BOSCH_S,
        )
        assert factory.find_violation(good_car) is None

    def test_validate_detects_common_bosch_brake_rule_violation(self):
        factory = domain.SedanFactory()
        bad_car = domain.Car(
            car_type=domain.CarType.SEDAN,
            engine=domain.Engine.GM,
            brake=domain.Brake.BOSCH_B,
            steering=domain.Steering.MOBIS,
        )
        assert factory.validate(bad_car) == "Bosch제동장치에는 Bosch조향장치 이외 사용 불가"

    def test_create_returns_car_with_expected_fields(self):
        factory = domain.SedanFactory()
        result = factory.create(domain.Engine.GM, domain.Brake.MANDO, domain.Steering.BOSCH_S)

        assert result == domain.Car(
            car_type=domain.CarType.SEDAN,
            engine=domain.Engine.GM,
            brake=domain.Brake.MANDO,
            steering=domain.Steering.BOSCH_S,
        )


class TestSuvFactory:
    def test_find_violation_detects_toyota_engine(self):
        factory = domain.SuvFactory()
        bad_car = domain.Car(
            car_type=domain.CarType.SUV,
            engine=domain.Engine.TOYOTA,
            brake=domain.Brake.MANDO,
            steering=domain.Steering.BOSCH_S,
        )
        assert factory.find_violation(bad_car) == "SUV에는 TOYOTA엔진 사용 불가"

    def test_find_violation_passes_for_valid_engine(self):
        factory = domain.SuvFactory()
        good_car = domain.Car(
            car_type=domain.CarType.SUV,
            engine=domain.Engine.GM,
            brake=domain.Brake.MANDO,
            steering=domain.Steering.BOSCH_S,
        )
        assert factory.find_violation(good_car) is None

    def test_create_returns_car_with_expected_fields(self):
        factory = domain.SuvFactory()
        result = factory.create(domain.Engine.GM, domain.Brake.MANDO, domain.Steering.BOSCH_S)

        assert result == domain.Car(
            car_type=domain.CarType.SUV,
            engine=domain.Engine.GM,
            brake=domain.Brake.MANDO,
            steering=domain.Steering.BOSCH_S,
        )

    def test_validate_priority_type_specific_violation_reported_before_bosch_rule(self):
        """엔진(TOYOTA)과 Bosch 조향 불일치가 동시에 위반되는 조합에서는
        타입 전용 규칙(TOYOTA엔진)이 먼저 보고되고, Bosch 공통 규칙 메시지는 나오지 않는다."""
        factory = domain.SuvFactory()
        car = domain.Car(
            car_type=domain.CarType.SUV,
            engine=domain.Engine.TOYOTA,
            brake=domain.Brake.BOSCH_B,
            steering=domain.Steering.MOBIS,
        )
        assert factory.validate(car) == "SUV에는 TOYOTA엔진 사용 불가"


class TestTruckFactory:
    def test_find_violation_detects_wia_engine(self):
        factory = domain.TruckFactory()
        bad_car = domain.Car(
            car_type=domain.CarType.TRUCK,
            engine=domain.Engine.WIA,
            brake=domain.Brake.CONTINENTAL,
            steering=domain.Steering.BOSCH_S,
        )
        assert factory.find_violation(bad_car) == "Truck에는 WIA엔진 사용 불가"

    def test_find_violation_detects_mando_brake(self):
        factory = domain.TruckFactory()
        bad_car = domain.Car(
            car_type=domain.CarType.TRUCK,
            engine=domain.Engine.GM,
            brake=domain.Brake.MANDO,
            steering=domain.Steering.BOSCH_S,
        )
        assert factory.find_violation(bad_car) == "Truck에는 Mando제동장치 사용 불가"

    def test_find_violation_passes_for_valid_combination(self):
        factory = domain.TruckFactory()
        good_car = domain.Car(
            car_type=domain.CarType.TRUCK,
            engine=domain.Engine.GM,
            brake=domain.Brake.CONTINENTAL,
            steering=domain.Steering.BOSCH_S,
        )
        assert factory.find_violation(good_car) is None

    def test_find_violation_priority_only_first_matching_condition_reported(self):
        """WIA엔진(조건1)과 Mando제동장치(조건2)가 동시에 위반될 때 WIA엔진 메시지만 반환된다."""
        factory = domain.TruckFactory()
        target_car = domain.Car(
            car_type=domain.CarType.TRUCK,
            engine=domain.Engine.WIA,
            brake=domain.Brake.MANDO,
            steering=domain.Steering.BOSCH_S,
        )
        assert factory.find_violation(target_car) == "Truck에는 WIA엔진 사용 불가"

    def test_create_returns_car_with_expected_fields(self):
        factory = domain.TruckFactory()
        result = factory.create(domain.Engine.GM, domain.Brake.CONTINENTAL, domain.Steering.BOSCH_S)

        assert result == domain.Car(
            car_type=domain.CarType.TRUCK,
            engine=domain.Engine.GM,
            brake=domain.Brake.CONTINENTAL,
            steering=domain.Steering.BOSCH_S,
        )


class TestGetFactory:
    def test_sedan_type_returns_sedan_factory(self):
        factory = domain.get_factory(domain.CarType.SEDAN)
        assert isinstance(factory, domain.SedanFactory)

    def test_suv_type_returns_suv_factory(self):
        factory = domain.get_factory(domain.CarType.SUV)
        assert isinstance(factory, domain.SuvFactory)

    def test_truck_type_returns_truck_factory(self):
        factory = domain.get_factory(domain.CarType.TRUCK)
        assert isinstance(factory, domain.TruckFactory)

    def test_unknown_type_raises_key_error(self):
        with pytest.raises(KeyError):
            domain.get_factory(999)
