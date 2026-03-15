# Docker Basics

This directory covers the **fundamental concepts and first commands of Docker**.

Docker is a tool that helps developers package applications together with their runtime environment,
so that software can run more consistently across different machines.

For beginners, Docker learning usually starts with three questions:

- What is Docker?
- Is Docker installed correctly on my machine?
- How do I run and inspect containers and images?

This module answers those questions step by step.

---

# 🎯 Learning Objectives

After completing this module, you should be able to:

- explain what Docker is in beginner-friendly terms
- understand the difference between an image and a container
- verify Docker installation on your machine
- run the `hello-world` test container
- inspect running and stopped containers
- inspect local Docker images
- use both Docker Desktop and terminal-based Docker workflows

---

# Why Docker Matters

In software development, code often depends on:

- language versions
- package versions
- operating system settings
- environment variables
- external tools

Even when the source code is the same, applications may fail on another machine because the environment is different.

Docker helps reduce that problem by packaging:

```text
application code
+ dependencies
+ runtime
+ environment settings
```

into a more reproducible setup.

### 한국어 설명
초보자가 가장 많이 겪는 문제 중 하나는  
“내 컴퓨터에서는 되는데 다른 컴퓨터에서는 안 되는 것”이다.

이 문제의 핵심 원인은 보통 **코드가 아니라 실행 환경 차이**다.  
Docker는 이 실행 환경을 함께 묶어서 더 일관되게 실행할 수 있게 도와준다.

---

# Core Concepts

## 1️⃣ Image

An image is a **template** or **blueprint**.

Examples:

- `ubuntu`
- `nginx`
- `python`
- `hello-world`

An image contains what is needed to run an application.

### 한국어 설명
Image는 컨테이너를 만들기 위한 설계도다.  
실행 환경 정보가 들어 있는 템플릿이라고 생각하면 된다.

---

## 2️⃣ Container

A container is a **running or stopped instance of an image**.

If:

```text
Image = blueprint
```

then:

```text
Container = actual instance created from that blueprint
```

### 한국어 설명
Container는 Image를 실제로 실행한 결과다.

즉:

- Image = 설계도
- Container = 실제 실행된 프로그램

이라고 이해하면 된다.

---

## 3️⃣ Docker Desktop vs Terminal

Docker can be used in two ways:

### Docker Desktop
A graphical interface where you can inspect:

- containers
- images
- status
- logs

### Terminal
A command-line interface where you can run commands such as:

```bash
docker --version
docker ps
docker images
docker run hello-world
```

### 한국어 설명
Docker Desktop은 GUI 방식이고,  
Mac 터미널은 명령어 방식이다.

둘 다 같은 Docker를 다루지만,
표현 방식만 다르다고 보면 된다.

---

# Files in This Module

| File | Purpose |
|------|---------|
| `01_what_is_docker.md` | Beginner-friendly introduction to Docker |
| `02_install_check.md` | Verify Docker installation and environment |
| `03_docker_run_hello_world.sh` | First Docker run example using `hello-world` |
| `04_docker_ps_images.md` | Inspect containers and images |

---

# 1️⃣ What is Docker?

File  
`01_what_is_docker.md`

This file introduces Docker from a beginner perspective.

Topics covered:

- what Docker is
- why Docker is useful
- image vs container
- Dockerfile concept
- why environment consistency matters

Beginner mental model:

```text
Code
  + Dependencies
  + Runtime
  + Environment
  = Dockerized Application
```

### 한국어 설명
이 문서는 Docker를 처음 접하는 사람이  
“도대체 Docker가 왜 필요한가?”를 이해하도록 돕는 입문 문서다.

---

# 2️⃣ Installation Check

File  
`02_install_check.md`

This file explains how to verify that Docker is installed correctly.

Typical commands:

```bash
docker --version
docker info
docker run hello-world
```

Success usually means:

- Docker CLI works
- Docker engine works
- image download works
- container execution works

### 한국어 설명
설치 확인 단계는 매우 중요하다.  
설치만 된 것이 아니라 **실제로 동작하는지** 확인해야 하기 때문이다.

---

# 3️⃣ First Container Run

File  
`03_docker_run_hello_world.sh`

This script demonstrates the most basic Docker test:

```bash
docker run hello-world
```

What happens:

1. Docker checks for the image locally
2. If missing, it downloads the image
3. It creates a container from the image
4. The container runs and prints a success message

This is the standard first test for Docker beginners.

### 한국어 설명
`hello-world`는 Docker 입문에서 가장 유명한 테스트 예제다.  
이 명령이 성공하면 Docker 환경이 정상적으로 작동한다고 볼 수 있다.

---

# 4️⃣ Inspecting Containers and Images

File  
`04_docker_ps_images.md`

This file explains how to inspect Docker state.

Key commands:

```bash
docker ps
docker ps -a
docker images
```

Meaning:

- `docker ps` → running containers
- `docker ps -a` → all containers
- `docker images` → local images

This helps beginners understand what Docker is doing on their machine.

### 한국어 설명
초보자는 image와 container를 자주 헷갈린다.  
이 문서는 실제 명령어를 통해 상태를 확인하면서 개념을 익히도록 설계되었다.

---

# Recommended Beginner Workflow

A practical learning flow for this module is:

```text
What is Docker?
      ↓
Check installation
      ↓
Run hello-world
      ↓
Inspect containers and images
```

This order matters because it builds understanding step by step:

1. concept
2. setup
3. execution
4. inspection

---

# Using Docker Desktop

After Docker Desktop is installed and opened, you can use:

## Containers Tab
To inspect:

- running containers
- stopped containers
- status
- start / stop actions
- delete actions

## Images Tab
To inspect:

- downloaded images
- image size
- tags
- removal actions

### 한국어 설명
Docker Desktop에서는 컨테이너와 이미지를 GUI로 볼 수 있다.  
터미널 명령어에 익숙하지 않은 초보자에게 매우 유용하다.

---

# Using Docker in Mac Terminal

Typical terminal commands on Mac:

```bash
docker --version
docker info
docker run hello-world
docker ps
docker ps -a
docker images
```

These commands help verify installation and inspect Docker resources directly.

### 한국어 설명
Mac 터미널에서는 위 명령어들만 익혀도 Docker 기초 실습을 충분히 진행할 수 있다.

---

# Practical Importance

Even at the beginner level, Docker is already useful for:

- backend development
- API testing
- environment setup
- local database practice
- Python / FastAPI application deployment practice

Docker becomes even more valuable when combined with:

- Python
- FastAPI
- MySQL
- Linux
- machine learning services

---

# Summary

This module introduces the first essential Docker concepts and commands:

```text
What is Docker?
→ Installation Check
→ hello-world Execution
→ Container / Image Inspection
```

By the end of this module, you should understand:

- what Docker is
- how Docker works at a basic level
- how to verify Docker installation
- how to inspect images and containers using both Docker Desktop and terminal commands