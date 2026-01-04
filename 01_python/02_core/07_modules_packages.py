"""
Day 11: Python Core - Modules & Packages

This file introduces Python modules and packages.
Modules and packages allow us to organize code,
promote reusability, and build scalable projects.

이 파일은 파이썬의 모듈(Module)과 패키지(Package) 개념을 다룬다.
모듈과 패키지는 코드 구조화, 재사용성, 확장성을 위한 핵심 요소이다.
"""

# -------------------------------------------
# 1. What is a module?
# -------------------------------------------
# A module is simply a Python file (.py) containing variables,
# functions, or classes that can be reused in other files.

# 모듈은 변수, 함수, 클래스 등을 담고 있는 하나의 .py 파일이다.

# 예시 (같은 디렉토리에 math_utils.py가 있다고 가정):
# from math_utils import add, subtract


# -------------------------------------------
# 2. Importing modules
# -------------------------------------------

import math

print(math.sqrt(16))   # 4.0
print(math.pi)         # 3.141592...

# 한국어 설명:
# - import module_name 형태
# - module_name.function 형태로 접근


# -------------------------------------------
# 3. Import with alias
# -------------------------------------------

import math as m

print(m.sqrt(25))

# 한국어 설명:
# - alias(as)는 이름이 길거나 자주 사용할 때 유용


# -------------------------------------------
# 4. Import specific objects
# -------------------------------------------

from math import sqrt, pi

print(sqrt(36))
print(pi)

# 한국어 설명:
# - 필요한 함수/변수만 가져와서 사용
# - 네임스페이스 충돌에 주의


# -------------------------------------------
# 5. Built-in vs external modules
# -------------------------------------------

# Built-in modules (기본 제공)
import os
import sys
import datetime

print(os.getcwd())
print(sys.version)
print(datetime.date.today())

# External modules (외부 라이브러리)
# 예: numpy, pandas, requests
# pip install numpy
# import numpy as np


# -------------------------------------------
# 6. What is a package?
# -------------------------------------------
# A package is a directory that contains multiple modules.
# It usually includes an __init__.py file (Python < 3.3 필수).

# 패키지는 여러 모듈을 묶는 디렉토리 구조이다.
# 실무 프로젝트에서는 패키지 단위로 코드를 관리한다.


# -------------------------------------------
# 7. Package import example (conceptual)
# -------------------------------------------
# project/
# ├── utils/
# │   ├── __init__.py
# │   ├── preprocessing.py
# │   └── metrics.py
# └── main.py
#
# main.py:
# from utils.preprocessing import clean_data
# from utils.metrics import accuracy

# 한국어 설명:
# - 패키지는 계층 구조를 만든다
# - 분석/모델/유틸리티 분리에 매우 중요


# -------------------------------------------
# 8. __name__ == "__main__"
# -------------------------------------------

def main():
    print("This script is being run directly.")

if __name__ == "__main__":
    main()

# 한국어 설명:
# - 해당 파일을 직접 실행할 때만 main() 실행
# - import될 때는 실행되지 않음
# - 실무/연구 코드에서 표준 패턴


# -------------------------------------------
# 9. Best practices
# -------------------------------------------
# - 표준 라이브러리 먼저 import
# - 외부 라이브러리 다음
# - 로컬 모듈은 마지막
#
# - 모듈 이름은 소문자 + underscore
# - 패키지는 역할 단위로 분리


# -------------------------------------------
# Summary
# -------------------------------------------
# - Modules organize reusable code
# - Packages structure large projects
# - __name__ == "__main__" controls execution behavior
#
# 요약:
# - 모듈은 코드 재사용의 기본 단위
# - 패키지는 프로젝트 구조의 핵심
# - 실행 흐름 제어는 실무 필수 개념