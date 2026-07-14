# CODE_STRUCTURE.md

`assembly.py`의 현재(리팩토링 전) 코드 구조를 설명한다. 리팩토링이 진행되면서 자주 바뀔 내용이다.
도메인 규칙 자체는 [docs/DOMAIN.md](DOMAIN.md) 참고.

## 현재 구조

`assembly.py` 하나로 구성되어 있으며, 전역 변수 `q0`(차량 타입), `q1`(엔진), `q2`(제동장치), `q3`(조향장치)에
사용자 선택 상태를 저장하는 상태 머신 형태로 동작한다.

- `main()`: `step`(0~4) 값을 기준으로 한 단계 상태 머신으로 CLI 입력을 순환 처리
- `show_menu(step)` / `is_valid_range(step, ans)`: 단계별 메뉴 출력과 입력값 범위 검증
- `select_car_type/engine/brake/steering(a)`: 각각 해당 전역 변수(`q0`~`q3`)에 선택값 기록
- `is_valid_check()`: 조합 가능 여부 판정 (런타임 동작 차단용)
- `run_produced_car()` / `test_produced_car()`: 완성된 차량 실행 및 검증 결과 출력
