# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

"차량조립 KATA" 리팩토링 실습 프로젝트다. `assembly.py`에 이미 동작하는 절차지향식 코드가 작성되어 있고,
이를 유지보수하기 쉽고 안전하며 확장 가능한 구조로 리팩토링하는 것이 이 프로젝트의 목적이다
(자세한 배경과 요구사항은 `docs/프로젝트요구사항.md` 참고).

리팩토링 시 다음 기존 코드의 문제점을 개선 대상으로 삼는다:
- 절차지향식 코드로 유지보수가 어려운 구조 (전역 변수 `q0`~`q4`로 상태 관리, 매직 넘버 기반 분기)
- 안전하지 않은 문법 사용 (예: `except:` bare except)
- 확장성이 고려되지 않음 (차량 타입/부품이 늘어나면 `if/elif` 분기를 계속 추가해야 함)
- 유닛테스트 부재

## 실행

```bash
python assembly.py
```

가상환경은 `.venv`에 Python 3.14 기반으로 구성되어 있으며 `pytest`가 설치되어 있다 (아직 테스트 코드는 없음).

## 테스트

`pytest`가 의존성으로 설치되어 있으므로 리팩토링 시 테스트 코드를 `pytest` 규칙(`test_*.py` 또는 `*_test.py`)에
맞춰 추가하고, 아래 명령으로 실행한다.

```bash
pytest                      # 전체 테스트 실행
pytest path/to/test_x.py::test_name   # 단일 테스트 실행
```

## 커밋 컨벤션

`type: 한글 설명` 형식을 따른다 (예: `docs: 요구사항 문서 추가`, `docs: CLAUDE.md 초안 생성`).

- `feat`: 새 기능 추가
- `fix`: 버그 수정
- `refactor`: 동작 변경 없는 구조 개선
- `test`: 테스트 추가/수정
- `docs`: 문서 추가/수정
- `chore`: 그 외 잡다한 작업 (설정, 의존성 등)

## 상세 문서

- 도메인 로직(자동차 조립 규칙): [docs/DOMAIN.md](docs/DOMAIN.md)
- 현재 코드 구조: [docs/CODE_STRUCTURE.md](docs/CODE_STRUCTURE.md)
