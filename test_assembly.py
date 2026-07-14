import pytest

import assembly


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


def test_main_handles_non_numeric_input_as_value_error_and_exits(monkeypatch, capsys):
    inputs = iter(["abc", "exit"])
    monkeypatch.setattr("builtins.input", lambda *_args: next(inputs))
    monkeypatch.setattr(assembly, "delay", lambda *_args: None)

    assembly.main()

    out = capsys.readouterr().out
    assert "ERROR :: 숫자만 입력 가능" in out
    assert "바이바이" in out
