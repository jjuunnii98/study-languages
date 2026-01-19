# Python Object-Oriented Programming (OOP)

This module covers **Object-Oriented Programming in Python** from fundamentals
to practical, design-oriented patterns used in real-world systems.

The focus is not on syntax alone, but on:
- modeling real-world entities
- designing maintainable and extensible systems
- transitioning from research code to production-quality architecture

본 모듈은 Python의 객체지향 프로그래밍(OOP)을
기초 문법부터 실무 설계 관점까지 체계적으로 다룹니다.

“클래스를 쓸 줄 아는 수준”을 넘어,
**왜 OOP가 필요한지, 언제 쓰는지, 어떻게 설계해야 하는지**에 초점을 둡니다.

---

## 🎯 Learning Objectives

- Understand OOP as a design paradigm, not just a language feature
- Model domain concepts using classes and objects
- Apply encapsulation, inheritance, and composition appropriately
- Design data-centric and behavior-centric classes
- Use modern Python features (`dataclass`, `ABC`)
- Apply classic OOP design patterns in Pythonic ways

---

## 📂 Structure & Progress

Each file represents a focused OOP concept.
Files are completed incrementally with day-based commits.

각 파일은 하나의 핵심 객체지향 개념을 다루며,
Day 단위 학습 기록으로 순차적으로 완성되었습니다.

---

## ✅ Completed (Day 14–21)

### `01_classes_basics.py` (Day 14)
**Class fundamentals**
- Class and object concepts
- Attributes vs methods
- Instance creation and usage

클래스와 객체의 기본 구조를 이해하고,
객체지향 사고의 출발점을 다룹니다.

---

### `02_attributes_methods.py` (Day 15)
**Attributes and methods in depth**
- Instance attributes
- Method design
- Behavioral modeling

객체가 “무엇을 가지고 있고, 무엇을 할 수 있는지”를 명확히 분리합니다.

---

### `03_init_and_repr.py` (Day 15)
**Initialization and representation**
- `__init__` for controlled object creation
- `__repr__` for debugging and logging

객체의 생성과 표현을 책임 있게 설계하는 방법을 다룹니다.

---

### `04_inheritance.py` (Day 16)
**Inheritance and polymorphism**
- Base classes and subclasses
- Method overriding
- Polymorphic behavior

상속을 통해 공통 로직을 재사용하고,
다형성을 활용하는 방법을 학습합니다.

---

### `05_composition.py` (Day 17)
**Composition over inheritance**
- Object composition
- Dependency relationships
- Flexible system design

“상속보다 합성” 원칙을 실제 예제로 이해합니다.

---

### `06_encapsulation.py` (Day 18)
**Encapsulation and information hiding**
- Public vs protected vs private attributes
- Property (`@property`) usage
- Validation and controlled access

객체 내부 상태를 안전하게 보호하는 설계 방법을 다룹니다.

---

### `07_dataclass.py` (Day 19)
**Data-centric class design with dataclasses**
- `@dataclass` basics
- `default_factory`
- `__post_init__` validation
- Immutability with `frozen=True`
- Ordering and comparison
- `asdict`, `replace`

실무에서 가장 자주 쓰이는
“데이터 모델 클래스”를 현대적인 방식으로 설계합니다.

---

### `08_abc_interfaces.py` (Day 20)
**Abstract Base Classes & interfaces**
- `ABC` and `@abstractmethod`
- Interface-based design
- Polymorphism via contracts
- Decoupling implementations from usage

확장 가능하고 안정적인 시스템을 위한
인터페이스 중심 설계를 다룹니다.

---

### `09_oop_design_patterns.py` (Day 21)
**Practical OOP design patterns**
- Strategy pattern (interchangeable algorithms)
- Factory pattern (config-driven object creation)
- Template Method pattern (pipeline skeleton)
- Repository-like abstractions (data sources)

연구 코드와 제품 코드 모두에서 활용 가능한
객체지향 설계 패턴을 실전 예제로 통합합니다.

---

## 🧠 Why OOP Matters (Research & Product)

Object-Oriented Programming enables you to:
- model complex domains clearly
- manage growing codebases safely
- reuse and extend logic without breaking systems
- collaborate effectively in teams
- transition smoothly from experiments to production

객체지향은 단순한 프로그래밍 기법이 아니라,
**복잡한 문제를 구조적으로 사고하는 방법**입니다.

---

## 📌 학습 요약 (한국어)

- OOP는 문법이 아니라 설계 패러다임이다
- 클래스는 “데이터 + 행동”을 함께 모델링한다
- 캡슐화·상속·합성을 상황에 맞게 선택해야 한다
- dataclass와 ABC는 현대 Python OOP의 핵심 도구다
- 디자인 패턴은 복잡한 시스템을 단순화하는 언어다

---

## 🚧 Status

**Completed — Python OOP (Day 14–21)**

This module provides a solid foundation for:
- advanced libraries
- data analysis pipelines
- machine learning systems
- backend and service-oriented architectures

본 모듈은 Python 객체지향 학습을 완료했으며,
이후 라이브러리 활용 및 실전 시스템 설계로 확장됩니다.