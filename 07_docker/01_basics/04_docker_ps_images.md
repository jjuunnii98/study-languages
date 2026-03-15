# Docker PS and Images

## What are `docker ps` and `docker images`?

These are two of the most important beginner Docker commands.

They help you answer two basic questions:

- What containers exist?
- What images exist?

In simple terms:

- `docker ps` → shows containers
- `docker images` → shows images

---

## Before learning the commands, remember this:

### Image
An image is a **template** or **blueprint**.

Examples:

- `ubuntu`
- `python`
- `nginx`
- `hello-world`

### Container
A container is a **running or stopped instance of an image**.

That means:

```text
Image = blueprint
Container = actual running (or stopped) object created from the image
```

### 한국어 설명
초보자는 image와 container를 자주 헷갈린다.

쉽게 생각하면:

- Image = 설계도
- Container = 실제 실행 결과

이다.

---

# 1️⃣ `docker ps`

## What does it do?

```bash
docker ps
```

This command shows **currently running containers**.

It usually includes:

- container ID
- image name
- command
- created time
- status
- port mapping
- container name

### Example

```bash
docker ps
```

Possible output:

```bash
CONTAINER ID   IMAGE     COMMAND                  STATUS         PORTS                  NAMES
abc123456789   nginx     "/docker-entrypoint…"   Up 2 minutes   0.0.0.0:8080->80/tcp  upbeat_nginx
```

### What this means

- a container based on the `nginx` image is running
- it is active now
- port `8080` on your Mac is connected to port `80` in the container

### 한국어 설명
`docker ps`는 **현재 실행 중인 컨테이너만** 보여준다.  
즉 지금 살아 있는 Docker 프로세스를 확인하는 명령어다.

---

# 2️⃣ `docker ps -a`

## What does it do?

```bash
docker ps -a
```

This command shows **all containers**:

- running containers
- stopped containers
- exited containers

### Why is this useful?

Some containers stop immediately after finishing their job.

For example:

```bash
docker run hello-world
```

This container prints a message and exits.
So it may **not** appear in `docker ps`,
but it **will** appear in `docker ps -a`.

### Example

```bash
docker ps -a
```

Possible output:

```bash
CONTAINER ID   IMAGE         COMMAND    STATUS                     NAMES
xyz987654321   hello-world   "/hello"   Exited (0) 2 minutes ago   nostalgic_test
```

### 한국어 설명
초보자는 `docker ps`에서 아무것도 안 보여서  
“컨테이너가 안 만들어졌나?” 하고 오해할 수 있다.

하지만 `hello-world`처럼 실행 후 바로 끝나는 컨테이너는  
`docker ps -a` 에서 확인해야 한다.

---

# 3️⃣ `docker images`

## What does it do?

```bash
docker images
```

This command shows **images stored on your machine**.

It usually includes:

- repository name
- tag
- image ID
- created time
- image size

### Example

```bash
docker images
```

Possible output:

```bash
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    abc123456789   2 weeks ago    13.3kB
ubuntu        latest    def987654321   3 weeks ago    78MB
```

### What this means

- `hello-world` image exists locally
- `ubuntu` image also exists locally
- these images can be used to create new containers

### 한국어 설명
`docker images`는 **내 컴퓨터에 저장된 이미지 목록**을 보여준다.  
즉 “어떤 설계도(image)를 내려받아 놓았는가?”를 확인하는 명령어다.

---

# 4️⃣ Docker Desktop에서 확인하는 방법

Docker Desktop을 실행하면
터미널 명령어를 GUI에서도 확인할 수 있다.

## Containers 확인

Docker Desktop 열기  
→ **Containers** 탭 클릭

여기서 볼 수 있는 것:

- 실행 중인 컨테이너
- 종료된 컨테이너
- 상태(Status)
- 삭제(Delete)
- 시작(Start)
- 중지(Stop)

### 한국어 설명
이 화면은 `docker ps` 와 `docker ps -a` 를 GUI로 보는 느낌이다.

---

## Images 확인

Docker Desktop 열기  
→ **Images** 탭 클릭

여기서 볼 수 있는 것:

- 이미지 이름
- 태그(tag)
- 크기(size)
- 삭제 버튼

### 한국어 설명
이 화면은 `docker images` 를 GUI로 보는 느낌이다.

---

# 5️⃣ Mac 터미널에서 확인하는 방법

On Mac terminal, use the following commands:

```bash
docker ps
docker ps -a
docker images
```

Typical beginner flow:

```bash
docker run hello-world
docker ps
docker ps -a
docker images
```

### Expected interpretation

- `docker ps` → may not show `hello-world`
- `docker ps -a` → shows `hello-world` container
- `docker images` → shows `hello-world` image

---

# 6️⃣ Beginner Mental Model

A simple way to think about it:

```text
docker images
→ What blueprints do I have?

docker ps
→ What is currently running?

docker ps -a
→ What has existed, including stopped containers?
```

---

# 7️⃣ Why These Commands Matter

These commands are essential because they let you inspect Docker state.

They help you understand:

- which containers are active
- which containers finished
- which images are available locally
- what Docker is doing on your machine

Without these commands, Docker feels like a black box.

---

# 8️⃣ Summary

These three commands are core beginner Docker commands:

```bash
docker ps
docker ps -a
docker images
```

Use them to check:

```text
running containers
all containers
local images
```

They are the foundation for understanding how Docker works.

---

# Commands Summary

```bash
docker ps
docker ps -a
docker images
```

---

# Next Step

After learning these commands, the next natural topics are:

- `docker stop`
- `docker rm`
- `docker rmi`
- `docker pull`
- `docker run -it`