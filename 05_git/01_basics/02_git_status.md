# Git Status — Check Repository State

## What is `git status`?

`git status` shows the current state of your Git repository.

It tells you:

- which branch you are on
- which files are new
- which files are modified
- which files are staged
- whether your working tree is clean

In simple terms:

> `git status` = “What is happening in my project right now?”

---

## Why is it important?

When learning Git, many beginners get confused about:

- Did I change a file?
- Did Git detect it?
- Did I already stage it?
- Is it ready to commit?

`git status` answers all of these questions.

That is why it is one of the **most important beginner Git commands**.

### 한국어 설명
`git status`는 현재 Git 상태를 보여주는 명령어다.  
지금 내 파일이 수정되었는지, 아직 추적되지 않는지, commit 준비가 되었는지 확인할 수 있다.

즉, **Git에서 가장 자주 확인해야 하는 상태 점검 명령어**다.

---

## Basic Usage

```bash
git status
```

---

## Example 1 — Right after `git init`

```bash
mkdir git-practice
cd git-practice
git init
git status
```

Possible output:

```bash
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

### What this means

- `On branch main` → 현재 main 브랜치에 있음
- `No commits yet` → 아직 commit이 없음
- `nothing to commit` → 아직 추적 중인 파일이나 변경사항이 없음

### 한국어 설명
Git 저장소는 시작했지만, 아직 아무 파일도 추가하지 않았고 commit도 없는 상태다.

---

## Example 2 — New Untracked File

```bash
touch README.md
git status
```

Possible output:

```bash
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        README.md

nothing added to commit but untracked files present
```

### What this means

- `Untracked files` → Git이 아직 추적하지 않는 새 파일
- `README.md` → 새로 만든 파일
- 아직 `git add` 하지 않았기 때문에 commit 대상이 아님

### 한국어 설명
새 파일은 만들었지만 아직 Git이 “관리 대상으로 등록”하지 않은 상태다.  
이럴 때 `git add README.md`를 실행하면 된다.

---

## Example 3 — Staged File

```bash
git add README.md
git status
```

Possible output:

```bash
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md
```

### What this means

- `Changes to be committed` → commit 준비 완료
- `new file: README.md` → 새 파일이 staging area에 올라감

### 한국어 설명
이제 README.md는 commit 준비가 된 상태다.  
다음 단계는 보통 `git commit -m "message"` 이다.

---

## Example 4 — Modified File

```bash
echo "# My Project" >> README.md
git status
```

Possible output:

```bash
On branch main

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   README.md
```

### What this means

- `Changes not staged for commit` → 수정은 되었지만 아직 staging 안 됨
- `modified: README.md` → 기존 파일이 바뀜

### 한국어 설명
Git은 수정된 것을 감지했지만, 아직 `git add` 하지 않았기 때문에 commit 준비는 안 된 상태다.

---

## Typical Git State Flow

`git status`로 확인할 수 있는 흐름은 보통 이렇다.

```text
Untracked
   ↓ git add
Staged
   ↓ git commit
Committed
   ↓ file edit
Modified
   ↓ git add
Staged again
```

---

## Common Sections in `git status`

### 1) Untracked files
Files Git does not track yet.

```bash
Untracked files:
```

### 2) Changes not staged for commit
Modified files that Git sees, but you did not stage yet.

```bash
Changes not staged for commit:
```

### 3) Changes to be committed
Files ready to be included in the next commit.

```bash
Changes to be committed:
```

### 4) Working tree clean
Nothing changed.

```bash
nothing to commit, working tree clean
```

### 한국어 설명
초보자는 `git status` 출력에서  
이 네 가지 상태를 구분할 수 있으면 Git 흐름을 이해하기 훨씬 쉬워진다.

---

## Why beginners should use `git status` often

A very good beginner habit is:

```bash
git status
```

before and after important Git actions.

For example:

```bash
git status
git add .
git status
git commit -m "my commit"
git status
```

This helps you understand exactly what changed at each step.

### 한국어 설명
Git을 배울 때는 `git status`를 자주 실행하는 습관이 정말 중요하다.  
지금 내가 어떤 상태인지 확인하면서 배우면 Git 흐름이 훨씬 빨리 이해된다.

---

## Common Beginner Mistake

### Mistake:
Trying to commit without checking status first.

This may cause problems such as:

- forgetting to add files
- committing the wrong files
- missing important changes

### Better habit:
Always check:

```bash
git status
```

before commit.

---

## Summary

`git status` is the command that tells you what is happening inside your Git repository.

It helps you understand:

```text
What changed?
What is tracked?
What is staged?
What is ready to commit?
```

In beginner Git learning, this is one of the most important commands.

---

## Commands Summary

```bash
git init
git status
touch README.md
git status
git add README.md
git status
```

---

## Next Step

After `git status`, the natural next commands to learn are:

- `git add`
- `git commit`
- `git log`

These commands help you move from checking state to saving history.