"""
Day 16: Inheritance (OOP)

This file introduces inheritance in Python.
Inheritance allows a class to reuse and extend
the behavior of another class.

본 파일은 Python의 상속(Inheritance)을 다룬다.
상속은 기존 클래스의 속성과 메서드를 재사용하면서,
기능을 확장하거나 특수화할 수 있게 해준다.
"""

# --------------------------------------------------
# 1. Basic Inheritance
# --------------------------------------------------
# A base class (parent class)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def describe(self):
        return f"Name: {self.name}, Age: {self.age}"


# A derived class (child class)
class Student(Person):
    def __init__(self, name, age, major):
        # Call the parent class constructor
        super().__init__(name, age)
        self.major = major

    def describe(self):
        # Override parent method
        return f"Name: {self.name}, Age: {self.age}, Major: {self.major}"


student = Student("Junyeong", 27, "Data Science")
print(student.describe())


# --------------------------------------------------
# 2. Why super() Matters
# --------------------------------------------------
# super() ensures that the parent class is properly initialized.
# This is especially important when multiple classes share logic.

# super()는 부모 클래스의 초기화 로직을 안전하게 호출한다.
# 상속 구조가 복잡해질수록 반드시 필요하다.


# --------------------------------------------------
# 3. Inheritance Without Overriding
# --------------------------------------------------
# Child class can inherit behavior without redefining methods.

class Researcher(Person):
    def research_field(self):
        return "Machine Learning"


researcher = Researcher("Alice", 30)
print(researcher.describe())
print(researcher.research_field())


# --------------------------------------------------
# 4. Practical Example: ML-Oriented Design
# --------------------------------------------------
# Base model class

class BaseModel:
    def fit(self, X, y):
        raise NotImplementedError("fit() must be implemented in subclasses")

    def predict(self, X):
        raise NotImplementedError("predict() must be implemented in subclasses")


# Derived model class
class LogisticRegressionModel(BaseModel):
    def fit(self, X, y):
        print("Fitting Logistic Regression model")

    def predict(self, X):
        print("Predicting with Logistic Regression")
        return [0] * len(X)


model = LogisticRegressionModel()
model.fit([1, 2, 3], [0, 1, 0])
print(model.predict([1, 2]))


# --------------------------------------------------
# 5. Key Takeaways
# --------------------------------------------------
# - Inheritance promotes code reuse
# - Child classes can override or extend parent behavior
# - super() is essential for safe initialization
# - Abstract-like base classes help enforce interfaces
# - In ML and data pipelines, inheritance improves structure