# Advanced Python — Performance

이 디렉토리는 **Python 성능 분석과 최적화(Performance Optimization)**를 학습하기 위한 코드 모음이다.

Python 프로그램이 느려지는 이유는 대부분 다음 세 가지에서 발생한다.

1. 비효율적인 알고리즘
2. 불필요한 연산 반복
3. 과도한 메모리 사용

이 폴더에서는 다음과 같은 핵심 성능 개념을 실습한다.

- Time Complexity (시간복잡도)
- Profiling (성능 분석)
- Memory Optimization (메모리 최적화)

---

# 1. Time Complexity

시간복잡도(Time Complexity)는 **입력 데이터 크기가 증가할 때 실행 시간이 어떻게 증가하는지**를 설명하는 개념이다.

대표적인 Big-O 복잡도

| Complexity | 설명 |
|---|---|
| O(1) | constant time |
| O(log n) | logarithmic time |
| O(n) | linear time |
| O(n²) | quadratic time |

예시

```python
# O(1)
def get_first(data):
    return data[0]

# O(n)
def linear_search(data, target):
    for value in data:
        if value == target:
            return True
```
시간복잡도를 이해하는 것은 성능 최적화의 가장 중요한 출발점이다.

---

# 2. Profiling

Profiling은 코드에서 어떤 부분이 가장 많은 시간을 사용하는지 분석하는 과정이다.

Python에서는 보통 다음 도구를 사용한다.

#### perf_counter()

간단한 실행 시간 측정
```
from time import perf_counter

start = perf_counter()
my_function()
end = perf_counter()

print(end - start)
```

#### cProfile

함수 단위 성능 분석
```
import cProfile

cProfile.run("my_function()")
```

#### Profiling을 사용하면 다음 정보를 확인할 수 있다.
	•	함수 호출 횟수
	•	함수 실행 시간
	•	누적 실행 시간

이 정보를 통해 **병목(Bottleneck)**을 찾을 수 있다.

---
# 3. Memory Optimization

성능 문제는 CPU뿐 아니라 메모리 사용량에서도 발생한다.

특히 대용량 데이터 처리에서는 다음 패턴이 중요하다.

#### List (Eager Evaluation)
```
numbers = [i for i in range(1000000)]
```
모든 데이터를 한 번에 메모리에 저장한다.


#### Generator (Lazy Evaluation)
```
numbers = (i for i in range(1000000))
```

데이터를 필요할 때 하나씩 생성한다.

장점
	•	메모리 사용량 감소
	•	대용량 데이터 처리 가능

#### Chunk Processing

대용량 데이터를 나눠서 처리하는 방법
``` 
def chunked(data, size):
    for i in range(0, len(data), size):
        yield data[i:i+size]
```
이 방식은 다음과 같은 상황에서 자주 사용된다.
	•	로그 처리
	•	데이터 파이프라인
	•	ETL 작업
	•	머신러닝 데이터 전처리

---

# 4. Files in This Directory

| File | Description |
|---|---|
| 01_time_complexity_patterns.py | Big-O 시간복잡도 패턴 예제|
| 02_profiling_basics.py | perf_counter, cProfile 기반 성능 분석|
| 03_memory_optimization.py | generator, chunk processing 기반 메모리 최적화|

---

# 5. Run Examples

#### 프로젝트 루트에서 실행
```
cd study-languages
```

#### Time Complexity
```
python 01_python/06_advanced/01_performance/01_time_complexity_patterns.py
```

#### Profiling
```
python 01_python/06_advanced/01_performance/02_profiling_basics.py
```

#### Memory Optimization
```
python 01_python/06_advanced/01_performance/03_memory_optimization.py
```

---

# 6. Performance Optimization Principles

성능 최적화의 기본 원칙

1️⃣ 먼저 측정한다 (Measure first)
2️⃣ 병목을 찾는다 (Find the bottleneck)
3️⃣ 알고리즘을 개선한다 (Improve algorithm)
4️⃣ 필요할 때만 **미세 최적화(micro-optimization)**를 한다

많은 경우 다음이 가장 큰 성능 차이를 만든다.
	•	알고리즘 개선
	•	자료구조 선택
	•	불필요한 반복 제거

---

# Summary

Python 성능 최적화는 다음 세 가지 축으로 이루어진다.
```
Algorithm
   ↓
Profiling
   ↓
Memory Optimization
```

이 세 가지를 이해하면
	•	데이터 분석
	•	머신러닝
	•	백엔드 서비스
	•	대용량 데이터 처리

모든 분야에서 더 효율적인 Python 코드를 작성할 수 있다.