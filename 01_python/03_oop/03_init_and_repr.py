"""
Day 15: __init__ and __repr__ (OOP)

This file introduces two fundamental special methods in Python classes:
- __init__: constructor method for object initialization
- __repr__: official string representation of an object

Understanding these methods is essential for writing
clean, debuggable, and professional object-oriented code.
"""

# --------------------------------------------------
# 1. Basic __init__ Method
# --------------------------------------------------
# __init__ is called automatically when a new object is created.
# It initializes the object's attributes.

class User:
    def __init__(self, name, age):
        # Instance attributes
        self.name = name
        self.age = age

# Create an object (instance) of User
user1 = User("Junyeong", 27)
print(user1.name)
print(user1.age)


# --------------------------------------------------
# 2. Why __repr__ Matters
# --------------------------------------------------
# Without __repr__, printing an object shows a memory address,
# which is not useful for debugging or logging.

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

product = Product("Laptop", 1500)
print(product)  # Default behavior (not informative)


# --------------------------------------------------
# 3. Implementing __repr__
# --------------------------------------------------
# __repr__ should return a string that clearly describes the object.
# Ideally, it should be unambiguous and helpful for developers.

class ProductWithRepr:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price})"

product2 = ProductWithRepr("Laptop", 1500)
print(product2)


# --------------------------------------------------
# 4. __repr__ vs __str__ (Conceptual)
# --------------------------------------------------
# __repr__: developer-facing, debugging-oriented
# __str__: user-facing, human-readable (introduced later)

# In practice:
# - __repr__ is used in the interpreter, logs, and debugging
# - __str__ is used in print() if defined

# If __str__ is not defined, Python falls back to __repr__


# --------------------------------------------------
# 5. Practical Example: Data-Oriented Class
# --------------------------------------------------
# A well-designed __repr__ is extremely useful
# when working with data analysis or modeling pipelines.

class ExperimentResult:
    def __init__(self, model_name, accuracy, dataset):
        self.model_name = model_name
        self.accuracy = accuracy
        self.dataset = dataset

    def __repr__(self):
        return (
            f"ExperimentResult("
            f"model_name='{self.model_name}', "
            f"accuracy={self.accuracy:.3f}, "
            f"dataset='{self.dataset}'"
            f")"
        )

result = ExperimentResult("LogisticRegression", 0.87321, "Titanic")
print(result)


# --------------------------------------------------
# 6. Summary
# --------------------------------------------------
# - __init__ defines how an object is created and initialized
# - __repr__ defines how an object is represented for developers
# - A good __repr__ improves debugging, logging, and readability
# - These methods are foundational for professional OOP design