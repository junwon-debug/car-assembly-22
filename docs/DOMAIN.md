# DOMAIN.md

자동차 조립 도메인 규칙을 설명한다. 구현이 바뀌어도 이 규칙 자체는 잘 바뀌지 않는다.

## 조립 순서

차량은 "타입 선택 → 부품 선택 → 완성 차량 검증" 순서로 조립된다.

- **차량 타입**: Sedan(세단), SUV, Truck — 향후 타입 추가 가능성을 염두에 두어야 함
- **부품**: 엔진(GM/TOYOTA/WIA, 그리고 테스트용 "고장난 엔진"), 제동장치(MANDO/CONTINENTAL/BOSCH), 조향장치(BOSCH/MOBIS)

## 호환성 제약 조건

1. 제동장치로 Bosch를 사용하면 조향장치도 반드시 Bosch여야 한다 (타사 조향장치와 호환 불가)
2. Continental은 Sedan용 제동장치를 만들지 않는다 → Sedan에 Continental 제동장치 사용 불가
3. TOYOTA는 SUV용 엔진을 만들지 않는다 → SUV에 TOYOTA 엔진 사용 불가
4. WIA는 Truck용 엔진을 만들지 않는다 → Truck에 WIA 엔진 사용 불가
5. MANDO는 Truck용 제동장치를 만들지 않는다 → Truck에 MANDO 제동장치 사용 불가

이 제약 조건은 리팩토링 후에도 단일 지점(single source of truth)에서 판단하도록 만드는 것이 핵심 과제다 —
현재 구현(`assembly.py`)에서는 `is_valid_check()`(런타임 동작 차단용)와 `test_produced_car()`(테스트 결과
출력용)에 동일한 로직이 그대로 복제되어 있다. 구현 세부사항은 [docs/CODE_STRUCTURE.md](CODE_STRUCTURE.md) 참고.
