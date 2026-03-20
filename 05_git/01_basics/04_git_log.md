# Git Log

## What is `git log`?

`git log` is used to view the commit history of a repository.

It shows:

- commit hash
- author
- date
- commit message

### 한국어 설명
`git log`는 Git 저장소의 **이전 commit 기록을 확인하는 명령어**다.

즉:

```text
"누가, 언제, 무엇을 변경했는지"
```

를 확인할 수 있다.

---

# 1️⃣ Basic Usage

```bash
git log
```

### Example Output

```text
commit a1b2c3d4e5f6...
Author: Junyeong Song
Date:   Tue Mar 10 14:00:00 2026

    feat: add Docker lifecycle script
```

### 한국어 설명
기본 `git log`는 commit을 최신순으로 보여준다.

---

# 2️⃣ One-line Summary

```bash
git log --oneline
```

### Example

```text
a1b2c3d feat: add Docker lifecycle script
b4c5d6e docs: update README
c7d8e9f fix: correct shell script error
```

### 한국어 설명
한 줄로 간단하게 commit을 확인할 때 사용한다.

👉 실무에서 가장 많이 사용하는 옵션

---

# 3️⃣ Limit Number of Commits

```bash
git log -n 5
```

또는

```bash
git log --oneline -n 5
```

### 한국어 설명
최근 commit 몇 개만 보고 싶을 때 사용한다.

---

# 4️⃣ Show Changes (diff)

```bash
git log -p
```

### 한국어 설명
각 commit에서 실제로 어떤 코드가 변경되었는지 보여준다.

👉 디버깅할 때 매우 중요

---

# 5️⃣ Show File-specific History

```bash
git log <file>
```

Example:

```bash
git log README.md
```

### 한국어 설명
특정 파일의 변경 이력만 보고 싶을 때 사용한다.

---

# 6️⃣ Pretty Format

```bash
git log --pretty=format:"%h - %an, %ar : %s"
```

### Example

```text
a1b2c3d - Junyeong, 2 hours ago : feat: add Docker script
```

### 한국어 설명
로그 출력 형식을 커스터마이징할 수 있다.

---

# 7️⃣ Graph View (branch visualization)

```bash
git log --oneline --graph --all
```

### Example

```text
* a1b2c3d (HEAD -> main) feat: add Docker script
* b4c5d6e docs: update README
* c7d8e9f fix: bug fix
```

### 한국어 설명
브랜치 구조를 시각적으로 확인할 수 있다.

👉 협업에서 매우 중요

---

# 8️⃣ Show Author Information

```bash
git log --author="Junyeong"
```

### 한국어 설명
특정 사람이 만든 commit만 필터링할 수 있다.

---

# 9️⃣ Show Commits by Date

```bash
git log --since="2026-03-01"
git log --until="2026-03-10"
```

### 한국어 설명
특정 기간의 commit만 조회할 수 있다.

---

# 🔟 Practical Examples

## Example 1: 최근 commit 확인

```bash
git log --oneline -n 10
```

---

## Example 2: 특정 파일 변경 이력

```bash
git log README.md
```

---

## Example 3: commit 내용까지 확인

```bash
git log -p -n 3
```

---

## Example 4: 브랜치 구조 확인

```bash
git log --oneline --graph --all
```

---

# 1️⃣1️⃣ Why `git log` is Important

- debugging (버그 추적)
- understanding history
- code review
- collaboration

### 한국어 설명
`git log`는 단순 기록 확인이 아니라:

```text
문제 추적 + 협업 이해 + 코드 분석
```

에 필수적인 도구다.

---

# 1️⃣2️⃣ Mental Model

Think of `git log` as:

```text
"Timeline of your project"
```

### 한국어 설명

```text
git log = 프로젝트의 시간 흐름
```

---

# 1️⃣3️⃣ Summary

## Basic

```bash
git log
git log --oneline
```

## Advanced

```bash
git log -p
git log <file>
git log --oneline --graph --all
```

---

# Final Takeaway

```text
git log is not just history.
It is your debugging tool, collaboration tool, and project timeline.
```

### 한국어 핵심 정리

```text
git log는 단순 기록이 아니라
프로젝트의 흐름을 이해하는 핵심 도구다.
```