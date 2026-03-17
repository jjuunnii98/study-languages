# Image vs Container

This file explains one of the most important beginner Docker concepts:

- What is an image?
- What is a container?
- How are they different?

Many beginners confuse these two ideas, but understanding the difference is essential.

---

# Docker Image

A Docker image is a **template**, **blueprint**, or **snapshot** used to create containers.

It contains everything needed to run an application, such as:

- operating system layers
- runtime environment
- dependencies
- application files
- default configuration

Examples of Docker images:

- `ubuntu`
- `nginx`
- `python`
- `mysql`

An image is **not running by itself**.

It is only a prepared package that can be used to create containers.

### 한국어 설명
Docker Image는 컨테이너를 만들기 위한 **설계도**다.  
실행 환경에 필요한 파일과 설정이 들어 있지만,
그 자체는 실행 중인 상태가 아니다.

즉:

```text
Image = 실행 전 템플릿
```

---

# Docker Container

A Docker container is a **running (or stopped) instance of an image**.

When you start an image with Docker, Docker creates a container from it.

Example:

```bash
docker run ubuntu
```

This means:

- use the `ubuntu` image
- create a container from it
- start running it

A container is the actual object you interact with.

### 한국어 설명
Container는 Image를 실제로 실행한 결과물이다.  
즉, 컨테이너는 이미지에서 만들어진 **실행 단위**라고 볼 수 있다.

```text
Container = 실행된 실제 인스턴스
```

---

# Simple Analogy

A useful beginner analogy is:

```text
Image = 붕어빵 틀
Container = 실제로 만들어진 붕어빵
```

Or:

```text
Image = class
Container = object
```

Or:

```text
Image = recipe
Container = cooked meal
```

### 한국어 설명
비유로 생각하면 이해가 쉽다.

- Image는 틀 / 설계도 / 레시피
- Container는 실제 결과물 / 실행 상태

이다.

---

# Image → Container Flow

A common Docker workflow looks like this:

```text
Docker Image
    ↓
docker run
    ↓
Docker Container
```

Example:

```bash
docker pull nginx
docker run -d nginx
```

Interpretation:

1. download the `nginx` image
2. create and run a container from that image

### 한국어 설명
이미지를 먼저 준비하고,
그 이미지를 바탕으로 컨테이너를 실행하는 구조다.

---

# Why the Difference Matters

Understanding the difference helps explain Docker commands correctly.

## `docker images`

This command shows:

- images stored on your machine

It does **not** show running applications.

## `docker ps`

This command shows:

- currently running containers

It does **not** show all images.

### 한국어 설명
초보자가 가장 자주 헷갈리는 부분은 여기다.

- `docker images` → 이미지 목록
- `docker ps` → 실행 중 컨테이너 목록

즉 서로 보는 대상이 다르다.

---

# Example Commands

## Check local images

```bash
docker images
```

Possible output:

```bash
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
ubuntu        latest    abc123456789   2 weeks ago    78MB
nginx         latest    def987654321   3 weeks ago    181MB
```

## Check running containers

```bash
docker ps
```

Possible output:

```bash
CONTAINER ID   IMAGE     COMMAND                  STATUS         PORTS                  NAMES
xyz123456789   nginx     "/docker-entrypoint…"   Up 2 minutes   0.0.0.0:8080->80/tcp  sharp_nginx
```

### 한국어 설명
위 예시를 보면:

- `docker images`에서는 ubuntu / nginx 같은 이미지가 보이고
- `docker ps`에서는 실제 실행 중인 nginx 컨테이너가 보인다.

---

# One Image, Multiple Containers

A single image can be used to create multiple containers.

Example:

```bash
docker run -d nginx
docker run -d nginx
```

This creates two separate containers from the same `nginx` image.

### 한국어 설명
하나의 이미지를 여러 번 실행하면
여러 개의 컨테이너를 만들 수 있다.

즉:

```text
1 image → many containers
```

이 가능하다.

---

# Containers Are More Dynamic

Images are usually stable templates.

Containers are more dynamic because they can be:

- running
- stopped
- restarted
- removed

That is why containers are treated as the "live" part of Docker.

### 한국어 설명
Image는 상대적으로 고정된 설계도이고,
Container는 실행되고 멈추고 삭제되는 **동적인 실행 단위**다.

---

# Beginner Mental Model

The easiest mental model is:

```text
Image = what can be run
Container = what is actually running
```

Or more precisely:

```text
Image = reusable template
Container = created instance
```

---

# Summary

Docker images and containers are related, but not the same.

```text
Image
→ template / blueprint / package

Container
→ running instance created from an image
```

You usually:

1. download or build an image
2. run a container from that image
3. inspect containers separately from images

This distinction is one of the most important foundations in Docker learning.