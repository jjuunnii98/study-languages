"""
Day 8: Python Core - File I/O

This file covers file input/output (I/O) in Python.
File I/O is essential for loading data, saving results,
and building data processing pipelines.

이 파일은 파이썬의 파일 입출력(File I/O)을 다룬다.
파일 입출력은 데이터 로딩, 결과 저장,
그리고 분석 파이프라인 구축의 핵심 요소이다.
"""

# -------------------------------------------
# 1. Writing text files
# -------------------------------------------
# Use 'with' statement to safely handle files

file_path = "sample_text.txt"

with open(file_path, "w", encoding="utf-8") as f:
    f.write("Hello, Python File I/O!\n")
    f.write("This is a sample text file.\n")

# 한국어 설명:
# - "w" 모드: 파일 쓰기 (기존 파일이 있으면 덮어씀)
# - with 문을 사용하면 파일이 자동으로 닫힌다
# - encoding 지정은 한글/특수문자 처리에 중요


# -------------------------------------------
# 2. Reading text files
# -------------------------------------------

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

print(content)

# 한국어 설명:
# - "r" 모드: 파일 읽기
# - read(): 파일 전체를 문자열로 읽어온다


# -------------------------------------------
# 3. Reading line by line
# -------------------------------------------

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

# 한국어 설명:
# - 파일을 한 줄씩 순회(iteration) 가능
# - strip(): 줄 끝의 개행 문자 제거


# -------------------------------------------
# 4. Writing and reading lists
# -------------------------------------------

numbers = [1, 2, 3, 4, 5]
numbers_path = "numbers.txt"

with open(numbers_path, "w", encoding="utf-8") as f:
    for n in numbers:
        f.write(f"{n}\n")

with open(numbers_path, "r", encoding="utf-8") as f:
    loaded_numbers = [int(line.strip()) for line in f]

print(loaded_numbers)

# 한국어 설명:
# - 리스트 데이터를 파일로 저장할 때는
#   한 줄에 하나씩 쓰는 방식이 일반적
# - 다시 읽을 때는 타입 변환(int 등)이 필요


# -------------------------------------------
# 5. CSV file I/O
# -------------------------------------------
# Using the built-in csv module

import csv

csv_path = "sample_data.csv"

# Write CSV
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "score"])
    writer.writerow([1, "Alice", 90])
    writer.writerow([2, "Bob", 85])

# Read CSV
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

# 한국어 설명:
# - csv 모듈은 표 형태 데이터를 다룰 때 사용
# - DictReader를 사용하면 컬럼명을 key로 접근 가능


# -------------------------------------------
# 6. JSON file I/O
# -------------------------------------------

import json

data = {
    "project": "study-languages",
    "language": "Python",
    "level": "core",
    "day": 8
}

json_path = "config.json"

# Write JSON
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Read JSON
with open(json_path, "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

print(loaded_data)

# 한국어 설명:
# - JSON은 설정 파일, API 데이터 교환에 널리 사용
# - indent 옵션으로 가독성 향상
# - ensure_ascii=False → 한글 깨짐 방지


# -------------------------------------------
# 7. Common mistakes and best practices
# -------------------------------------------
# ❌ 파일을 직접 열고 닫는 방식
# f = open("file.txt")
# f.read()
# f.close()

# ✅ 권장 방식
# with open("file.txt") as f:
#     f.read()

# -------------------------------------------
# Summary
# -------------------------------------------
# - Use with-open pattern for safe file handling
# - Text, CSV, JSON are the most common formats
# - File I/O is foundational for data analysis pipelines
#
# 요약:
# - with 문으로 안전한 파일 처리
# - CSV/JSON은 실무에서 가장 많이 사용
# - 파일 입출력은 데이터 분석의 출발점