# Git Add and Commit

## What are `git add` and `git commit`?

These are two of the most important Git commands.

They are used to save your work into Git history, but they do **different jobs**.

- `git add` → prepares changes for commit
- `git commit` → saves the prepared changes into history

### 한국어 설명
많은 초보자가 `git add`와 `git commit`을 하나의 동작처럼 생각하지만, 실제로는 역할이 다르다.

- `git add` = 커밋할 변경사항을 선택해서 staging area에 올리는 단계
- `git commit` = staging area에 올라간 내용을 Git 히스토리에 저장하는 단계

즉 Git은 **바로 저장하지 않고, 먼저 고른 뒤 저장하는 구조**다.

---

# Core Git Workflow

A simple Git workflow looks like this:

```text
Working Directory
    ↓
git add
    ↓
Staging Area
    ↓
git commit
    ↓
Repository History
```

### 한국어 설명
Git은 보통 아래 3단계로 생각하면 된다.

1. **Working Directory**
   - 실제 파일을 수정하는 공간

2. **Staging Area**
   - 이번 commit에 넣을 변경사항을 골라두는 공간

3. **Repository History**
   - commit이 실제로 저장된 기록

---

# 1️⃣ `git add`

## What does it do?

```bash
git add <file>
```

This command moves changes from the working directory into the staging area.

Example:

```bash
git add README.md
```

This means:

- you modified `README.md`
- you want Git to include it in the next commit

### 한국어 설명
`git add`는 “저장”이 아니라 **이번 commit에 포함할 변경사항을 선택하는 동작**이다.

즉:

```text
"이 파일을 다음 commit에 넣겠다"
```

라고 Git에게 알려주는 단계다.

---

## Add one file

```bash
git add README.md
```

### 한국어 설명
특정 파일 하나만 staging할 때 사용한다.

---

## Add multiple files

```bash
git add file1.py file2.py README.md
```

### 한국어 설명
여러 파일을 한 번에 staging할 수 있다.

---

## Add everything

```bash
git add .
```

### 한국어 설명
현재 디렉토리 기준으로 변경된 파일들을 한 번에 staging한다.

주의:
- 삭제된 파일까지 모두 반영하려면 `git add -A`가 더 명확할 때가 있다.

---

## Add all changes including deletions

```bash
git add -A
```

### 한국어 설명
새 파일, 수정된 파일, 삭제된 파일까지 모두 staging한다.

리포지토리 구조를 크게 바꾸거나 reset할 때 매우 유용하다.

---

# 2️⃣ `git commit`

## What does it do?

```bash
git commit -m "your message"
```

This command saves the staged changes into Git history.

Example:

```bash
git commit -m "docs: update README with project overview"
```

### 한국어 설명
`git commit`은 staging area에 올려둔 변경사항을 **Git의 기록으로 저장**하는 동작이다.

즉 commit 이후에는:

- 변경사항이 하나의 버전으로 남고
- 나중에 다시 돌아가거나 비교할 수 있고
- GitHub에 push할 수도 있다

---

# 3️⃣ Why are add and commit separate?

Git separates these two commands on purpose.

This allows you to:

- choose only some files
- review changes before saving
- create cleaner commit history

### 한국어 설명
Git이 `add`와 `commit`을 분리한 이유는 **더 정교하게 버전 관리를 하게 하기 위해서**다.

예를 들어:

- 파일 5개 수정했지만
- 그중 2개만 먼저 저장하고 싶을 수 있다

이럴 때 `git add`로 필요한 것만 올리고,  
그 다음 `git commit`으로 깔끔한 기록을 만들 수 있다.

---

# 4️⃣ Basic Example

Suppose you edited a Python file and a README file.

## Step 1: Check status

```bash
git status
```

Possible output:

```bash
modified: script.py
modified: README.md
```

## Step 2: Stage files

```bash
git add script.py README.md
```

## Step 3: Commit staged changes

```bash
git commit -m "feat: add script improvements and update README"
```

### 한국어 설명
가장 기본적인 흐름은:

```text
git status
→ git add
→ git commit
```

이다.

---

# 5️⃣ Recommended Commit Message Style

A good commit message should be:

- specific
- concise
- meaningful

## Good examples

```bash
git commit -m "feat: add vector operations example in R"
git commit -m "docs: update Docker basics README"
git commit -m "refactor: reorganize analysis project structure"
git commit -m "fix: correct path handling in shell script"
```

## Poor examples

```bash
git commit -m "update"
git commit -m "fix"
git commit -m "change"
```

### 한국어 설명
좋은 commit message는 **무엇을 왜 바꿨는지**가 드러나야 한다.

너처럼 GitHub 포트폴리오를 만드는 경우에는 특히 중요하다.

---

# 6️⃣ Common Patterns

## Pattern A — Single file change

```bash
git add README.md
git commit -m "docs: improve README explanation"
```

## Pattern B — Multiple related files

```bash
git add src/model.py tests/test_model.py
git commit -m "feat: add baseline model and test coverage"
```

## Pattern C — Large structural change

```bash
git add -A
git commit -m "refactor: rebuild repository structure for practical analysis workflows"
```

### 한국어 설명
리포지토리 구조를 크게 바꾸는 경우에는 `git add -A`가 특히 중요하다.  
삭제된 파일까지 정확히 반영할 수 있기 때문이다.

---

# 7️⃣ How to inspect what is staged

Use:

```bash
git status
```

This will show:

- staged changes
- unstaged changes
- untracked files

### 한국어 설명
`git add`를 하고 나서도 바로 commit하지 말고,  
`git status`로 무엇이 staging되었는지 확인하는 습관이 중요하다.

---

# 8️⃣ Important Distinction

## `git add` does not save history

`git add` only stages changes.

## `git commit` saves history

`git commit` creates a new Git snapshot in the repository history.

### 한국어 설명
아주 중요:

- `git add`만 하면 아직 저장된 것이 아님
- `git commit`까지 해야 기록으로 남는다

즉, **add는 준비 / commit은 저장**이다.

---

# 9️⃣ Practical Mental Model

Think of Git like this:

```text
Working Directory = editing desk
Staging Area      = selected files for saving
Commit            = permanent snapshot in history
```

### 한국어 설명
비유로 이해하면:

- Working Directory = 작업 책상
- Staging Area = 이번에 저장할 문서만 골라 놓은 폴더
- Commit = 정식 보관함에 넣은 기록

---

# 🔟 Summary

## `git add`

```bash
git add <file>
git add .
git add -A
```

Used for:

- selecting changes
- preparing the next commit

## `git commit`

```bash
git commit -m "message"
```

Used for:

- saving staged changes into Git history

---

# Final Takeaway

A clean Git workflow is:

```bash
git status
git add ...
git commit -m "meaningful message"
```

### 한국어 핵심 정리

```text
git add    = commit할 변경사항 선택
git commit = 선택된 변경사항 저장
```

이 흐름을 정확히 이해하면 Git을 훨씬 더 깔끔하고 실무적으로 사용할 수 있다.