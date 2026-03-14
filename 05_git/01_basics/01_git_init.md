# Git Init — Start a Git Repository

## What is `git init`?

`git init` is the command that starts Git version control in a directory.

It tells Git:

> “From now on, I want this folder to be tracked as a Git repository.”

In simple terms:

- before `git init` → just a normal folder
- after `git init` → a Git-managed project folder

---

## Why is it important?

Before learning `git add`, `git commit`, or `git push`,
you first need to turn your folder into a **Git repository**.

That is exactly what `git init` does.

Without `git init`, Git does not know that your project should be tracked.

---

## What happens when you run `git init`?

When you run:

```bash
git init
```

Git creates a hidden folder called:

```bash
.git
```

This `.git` directory stores all metadata needed for version control.

It contains information such as:

- commit history
- branches
- Git configuration for the repository
- tracked file states

### 한국어 설명
`git init`을 실행하면 현재 폴더 안에 숨김 폴더인 `.git` 이 생성된다.  
이 폴더는 Git이 버전 관리에 필요한 정보를 저장하는 핵심 공간이다.

즉, **일반 폴더를 Git 저장소(repository)로 바꾸는 작업**이라고 이해하면 된다.

---

## Basic Example

### 1) Create a new project folder

```bash
mkdir my-first-project
cd my-first-project
```

### 2) Initialize Git

```bash
git init
```

### 3) Check repository status

```bash
git status
```

You may see output like:

```bash
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

### 한국어 설명
이 상태는 Git 저장소는 만들어졌지만,  
아직 commit한 기록이 없고 추적 중인 파일도 없다는 뜻이다.

---

## Example Workflow

```bash
mkdir git-practice
cd git-practice
git init
touch README.md
git status
```

### What this means

- `mkdir git-practice` → 새 폴더 생성
- `cd git-practice` → 그 폴더로 이동
- `git init` → Git 관리 시작
- `touch README.md` → 빈 파일 생성
- `git status` → 현재 Git 상태 확인

---

## Why `git status` matters after `git init`

After initialization, the next most important command is:

```bash
git status
```

This tells you:

- which files are new
- which files are modified
- which files are staged
- whether commits exist yet

### 한국어 설명
`git status`는 Git 학습 초반에 가장 자주 쓰는 명령어다.  
현재 상태를 보여주기 때문에 **습관적으로 자주 확인하는 것이 중요**하다.

---

## Important Note

Running `git init` does **not** automatically save files.

It only prepares the folder for Git tracking.

To actually save file history, you still need:

```bash
git add .
git commit -m "your message"
```

### 한국어 설명
많은 초보자가 `git init`만 하면 저장된다고 오해하는데,  
실제로는 **버전 관리 시작만 한 것**이다.  
이력을 남기려면 반드시 `git add` 와 `git commit` 이 필요하다.

---

## Typical Beginner Mistake

### Mistake:
Running `git init` in the wrong directory.

Example:

```bash
cd ~
git init
```

This would initialize Git in your home directory, which is usually not what you want.

### Better practice:
Always check your location first.

```bash
pwd
ls
```

Then initialize Git only in the intended project folder.

### 한국어 설명
`git init`은 **현재 위치한 폴더 기준으로 실행**되기 때문에  
반드시 `pwd`로 현재 경로를 확인하고 실행하는 습관이 좋다.

---

## Summary

`git init` is the first step in Git.

It means:

```text
Normal Folder
   ↓
git init
   ↓
Git Repository
```

Once initialized, you can start tracking changes using Git commands.

---

## Commands Summary

```bash
mkdir my-project
cd my-project
git init
git status
```

---

## Next Step

After `git init`, the natural next commands to learn are:

- `git status`
- `git add`
- `git commit`

These commands turn Git from “enabled” into “actually useful”.