# Docker Install Check

## Why Check the Installation?

Installing Docker is only the first step.

Before using Docker for real projects, you should confirm:

- Docker is installed
- the Docker engine is running
- the terminal recognizes Docker commands
- containers can actually start on your machine

In simple terms:

> “Docker install check” means  
> making sure Docker is not only installed, but actually usable.

### 한국어 설명
Docker를 설치했다고 해서 바로 다 끝난 것은 아니다.  
실제로 명령어가 동작하는지, Docker 엔진이 켜져 있는지,
테스트 컨테이너가 실행되는지 확인해야 한다.

---

## Step 1 — Check Docker Version

Run this command in your terminal:

```bash
docker --version
```

Possible output:

```bash
Docker version 27.0.3, build abcdefg
```

### What this means

If a version number appears, Docker is installed and the command is recognized.

If you see an error like:

```bash
command not found: docker
```

then Docker is either:

- not installed
- not added to your PATH
- not available in your current shell environment

### 한국어 설명
`docker --version`은 가장 기본적인 설치 확인 명령어다.  
버전이 나오면 설치 자체는 된 것이다.

---

## Step 2 — Check Detailed Docker Info

Run:

```bash
docker info
```

This command shows detailed information about your Docker environment.

Possible output includes:

- number of containers
- number of images
- storage driver
- operating system info
- server status

### Important note

If Docker is installed but not running,
you may see an error such as:

```bash
Cannot connect to the Docker daemon
```

This usually means Docker Desktop is not started yet.

### 한국어 설명
`docker info`는 Docker가 실제로 동작 중인지 확인할 때 매우 유용하다.  
설치는 되었지만 엔진이 꺼져 있으면 에러가 날 수 있다.

---

## Step 3 — Check Docker Desktop (Mac / Windows)

If you are using Docker Desktop:

- make sure Docker Desktop is open
- wait until Docker is fully started
- then run `docker info` again

Typical beginner mistake:

- Docker installed
- but Docker Desktop not running

### 한국어 설명
Mac이나 Windows에서는 Docker Desktop을 실행해야
Docker 엔진이 실제로 동작하는 경우가 많다.

즉 설치만 해놓고 앱을 켜지 않으면
명령어가 제대로 안 될 수 있다.

---

## Step 4 — Run a Test Container

A very common first test is:

```bash
docker run hello-world
```

### What this does

Docker will:

1. check whether the `hello-world` image exists locally
2. download it if necessary
3. start a small test container
4. print a success message

Expected output:

```text
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### 한국어 설명
이 명령어는 Docker가 실제로 이미지를 가져오고,
컨테이너를 실행할 수 있는지 확인하는 가장 기본적인 테스트다.

즉,
설치 확인의 마지막 단계라고 생각하면 된다.

---

## Step 5 — Check Images

After running `hello-world`, check the downloaded image:

```bash
docker images
```

Possible output:

```bash
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    abc123456789   2 weeks ago    13.3kB
```

### What this means

This shows which Docker images exist on your machine.

### 한국어 설명
`docker images`는 내 컴퓨터에 저장된 Docker 이미지 목록을 보여준다.

---

## Step 6 — Check Containers

You can also inspect containers.

### Running containers only

```bash
docker ps
```

### All containers including stopped ones

```bash
docker ps -a
```

Possible output:

```bash
CONTAINER ID   IMAGE         COMMAND    STATUS
abc123         hello-world   "/hello"   Exited (0)
```

### What this means

The `hello-world` container usually exits immediately after printing its message,
so it may appear in `docker ps -a` rather than `docker ps`.

### 한국어 설명
컨테이너는 항상 계속 실행되는 것이 아니다.  
`hello-world`는 메시지를 출력하고 바로 종료되므로
보통 `docker ps -a` 에서 확인할 수 있다.

---

## Typical Beginner Installation Check Flow

A common beginner flow looks like this:

```bash
docker --version
docker info
docker run hello-world
docker images
docker ps -a
```

This confirms:

- Docker command works
- Docker engine works
- images can be downloaded
- containers can run

---

## Common Problems

### 1) `command not found: docker`

Possible reasons:

- Docker not installed
- terminal session not refreshed
- PATH issue

### 2) `Cannot connect to the Docker daemon`

Possible reasons:

- Docker Desktop not running
- Docker engine not started

### 3) `permission denied`

Possible on Linux systems if Docker permissions are not configured.

### 한국어 설명
초보자는 설치 에러를 자주 겪는데,
가장 흔한 원인은:

- 설치 안 됨
- Docker Desktop 안 켜짐
- 권한 문제

이다.

---

## Minimum Success Criteria

You can consider Docker installation successful if all of these work:

```bash
docker --version
docker info
docker run hello-world
```

If these commands succeed, your Docker environment is ready for beginner practice.

---

## Summary

Docker install check means confirming that:

```text
Docker is installed
   ↓
Docker engine is running
   ↓
Docker commands work
   ↓
A test container can run successfully
```

The most important beginner test is:

```bash
docker run hello-world
```

If that works, Docker is ready to use.

---

## Commands Summary

```bash
docker --version
docker info
docker run hello-world
docker images
docker ps
docker ps -a
```

---

## Next Step

After confirming Docker works correctly,
the next beginner topics are usually:

- image vs container
- basic lifecycle commands
- `docker pull`
- `docker run`
- `docker stop`
- `docker rm`