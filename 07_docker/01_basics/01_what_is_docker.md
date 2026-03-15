# What is Docker?

## Docker in One Sentence

Docker is a tool that helps you **package an application and its environment together**
so it can run consistently across different machines.

In simple terms:

> Docker helps solve the problem of  
> “It works on my machine, but not on yours.”

---

## Why Do We Need Docker?

When building software, code often depends on many things:

- programming language version
- installed libraries
- operating system settings
- environment variables
- external tools

Even if the code is the same, the application may behave differently on another computer.

### Common beginner problem

You write an app on your laptop:

- it works on your laptop
- it fails on another laptop
- it fails again on the server

Why?

Because the **environment is different**.

Docker helps make the environment more consistent.

### 한국어 설명
초보자가 가장 많이 겪는 문제 중 하나는  
“내 컴퓨터에서는 되는데 다른 컴퓨터에서는 안 되는 것”이다.

이건 코드 문제라기보다 **실행 환경 차이** 때문인 경우가 많다.

Docker는 코드뿐 아니라 **실행 환경까지 같이 묶어서**  
다른 곳에서도 비슷하게 실행되도록 도와준다.

---

## Simple Analogy

Think of Docker like a **lunchbox**.

- code only → just ingredients
- Docker → ingredients + recipe + box + instructions together

This means someone else can open the same lunchbox
and get almost the same result.

### 한국어 설명
Docker를 도시락으로 생각하면 쉽다.

그냥 코드만 주는 것은 재료만 주는 것이고,  
Docker는 재료 + 조리법 + 용기까지 한 번에 주는 느낌이다.

---

## Core Concepts

### 1) Image

A Docker image is a **template** or **blueprint**.

It contains what is needed to run something.

Examples:

- Python runtime
- Node.js runtime
- MySQL setup
- application dependencies

### 한국어 설명
Image는 컨테이너를 만들기 위한 설계도 같은 것이다.  
실행에 필요한 환경 정보가 들어 있다.

---

### 2) Container

A container is a **running instance of an image**.

If image = blueprint  
then container = actual running app

### 한국어 설명
Container는 Image를 실제로 실행한 상태다.

즉,

- Image = 설계도
- Container = 실행 중인 실제 프로그램

이라고 이해하면 된다.

---

### 3) Dockerfile

A Dockerfile is a file that contains instructions
for building a Docker image.

Example instructions:

- start from Python image
- copy project files
- install dependencies
- run the app

### 한국어 설명
Dockerfile은 Docker 이미지를 만드는 방법을 적어둔 파일이다.  
즉, “이 환경을 어떻게 만들지”를 문서처럼 적는 것이다.

---

## What Problems Does Docker Solve?

Docker helps with:

- environment consistency
- easier deployment
- faster setup
- simpler testing
- cleaner local development

### Example

Without Docker:

- install Python manually
- install packages manually
- configure database manually
- fix version mismatch manually

With Docker:

- pull image
- run container
- use the same setup everywhere

### 한국어 설명
Docker가 있으면 설치 과정을 줄이고,  
같은 환경을 더 쉽게 재현할 수 있다.

---

## Where Is Docker Commonly Used?

Docker is widely used in:

- backend development
- web applications
- machine learning deployment
- data engineering pipelines
- API services
- cloud infrastructure

For example:

- FastAPI app in a container
- MySQL database in a container
- Jupyter notebook environment in a container

### 한국어 설명
특히 Python, FastAPI, MySQL, Linux와 함께 많이 쓰인다.  
즉, 데이터 분석/백엔드/ML 서비스화까지 연결되는 기술이다.

---

## Beginner Mental Model

A good beginner way to think about Docker is:

```text
Code
  + Dependencies
  + Runtime
  + Environment
  = Dockerized Application
```

That means Docker does not just run your code.

It runs your code **inside a prepared environment**.

---

## Important Distinction

Docker is **not** a virtual machine in the traditional sense.

It is lighter than a full VM and is designed for fast, repeatable application environments.

### 한국어 설명
Docker는 가상머신(VM)과 비슷해 보일 수 있지만 완전히 같지는 않다.  
초보자 단계에서는 “가벼운 실행 환경 패키징 도구” 정도로 이해해도 충분하다.

---

## First Beginner Goal

Before learning advanced Docker topics,
the first thing to understand is simply this:

> Docker lets you run applications in a reproducible environment.

That is the most important idea.

---

## Summary

Docker helps you:

- package applications
- include dependencies
- run software consistently
- reduce “works on my machine” problems

In one line:

```text
Docker = a tool for packaging and running software in a consistent environment
```

---

## Next Step

After understanding what Docker is,
the next beginner topics are usually:

- checking Docker installation
- running the first container
- understanding images vs containers
- basic Docker commands