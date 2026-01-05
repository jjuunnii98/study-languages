"""
Day 13: Python OOP - Class Basics

This file introduces the basic concept of classes in Python.
Classes are blueprints for creating objects that bundle
data (attributes) and behavior (methods).

이 파일은 파이썬 객체지향 프로그래밍(OOP)의 출발점으로,
클래스(Class)의 기본 개념을 다룬다.
클래스는 데이터(속성)와 동작(메서드)을 함께 묶는 설계 단위이다.
"""

# -------------------------------------------------
# 1. Why Classes?
# -------------------------------------------------
# Before OOP, data and functions are often separated.
# OOP groups related data and behavior together.

# OOP 이전:
# name = "Junyeong"
# age = 27
# def greet(name): ...

# OOP 이후:
# Person(name, age).greet()


# -------------------------------------------------
# 2. Defining a simple class
# -------------------------------------------------

class Person:
    """
    A simple Person class.

    한국어 설명:
    - Person은 사람이라는 개념을 표현하는 클래스
    - 객체(object)는 이 클래스를 기반으로 생성된다
    """

    def greet(self):
        return "Hello!"


# -------------------------------------------------
# 3. Creating objects (instances)
# -------------------------------------------------

p1 = Person()
p2 = Person()

print(p1.greet())
print(p2.greet())

# 한국어 설명:
# - p1, p2는 Person 클래스의 인스턴스(instance)
# - 같은 클래스에서 여러 객체를 생성할 수 있다


# -------------------------------------------------
# 4. Understanding `self`
# -------------------------------------------------
# self refers to the current object itself.

class Animal:
    def speak(self):
        return "Animal sound"


a = Animal()
print(a.speak())

# 한국어 설명:
# - self는 객체 자기 자신을 가리킨다
# - 메서드를 호출하면 Python이 자동으로 self를 전달한다
#   a.speak()  →  Animal.speak(a)


# -------------------------------------------------
# 5. Adding attributes dynamically
# -------------------------------------------------
# Python allows adding attributes at runtime (not always recommended)

p1.name = "Junyeong"
p1.age = 27

print(p1.name, p1.age)

# 한국어 설명:
# - 파이썬은 동적 언어이므로 실행 중 속성 추가 가능
# - 하지만 일반적으로는 __init__에서 속성을 정의하는 것이 안전
#   (다음 파일에서 다룰 예정)


# -------------------------------------------------
# 6. Class vs Object
# -------------------------------------------------

print(type(Person))  # <class 'type'>
print(type(p1))      # <class '__main__.Person'>

# 한국어 설명:
# - Person은 클래스
# - p1은 Person 클래스로부터 만들어진 객체
# - 클래스는 설계도, 객체는 실제 인스턴스


# -------------------------------------------------
# Summary
# -------------------------------------------------
"""
Day 13 요약

- 클래스는 객체를 만들기 위한 설계도
- 객체는 클래스의 인스턴스
- self는 객체 자신을 가리키는 참조
- 클래스는 데이터와 행동을 함께 묶는다

다음 단계:
- __init__과 속성 초기화
- 객체의 상태(state)를 안전하게 관리하는 방법
"""