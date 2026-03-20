# Git Basics

This directory covers the fundamental Git commands and concepts required for version control in real-world development workflows.

Git is not just a backup tool.  
It is a system for tracking changes, organizing development history, and collaborating with confidence.

This module focuses on the most essential beginner commands:

- `git init`
- `git status`
- `git add`
- `git commit`
- `git log`

---

## 🎯 Learning Objectives

After completing this module, you should be able to:

- explain what Git is and why it matters
- initialize a local Git repository
- inspect repository state with `git status`
- stage changes with `git add`
- save version history with `git commit`
- inspect commit history with `git log`
- understand the relationship between the working directory, staging area, and repository history

---

## Why Git Matters

In software development, files change constantly.

Without version control, it becomes difficult to answer questions such as:

- What changed?
- When did it change?
- Why did it change?
- Can I go back to an older version?
- Which files are ready to be saved into project history?

Git solves these problems by recording the evolution of a project over time.

### 한국어 설명
Git은 단순히 파일을 저장하는 도구가 아니다.  
프로젝트의 변경 이력을 관리하고, 실수를 복구하고, 협업을 가능하게 만드는 핵심 도구다.

즉 Git을 이해하면:

- 코드 변경 이력 관리
- 버그 추적
- 이전 버전 복원
- 협업 흐름 이해

가 가능해진다.

---

## Core Git Workflow

A basic Git workflow looks like this:

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

## Git은 보통 아래 3단계로 이해하면 된다.(이 구조를 이해하는 것이 Git의 핵심이다.)
	
    1.	Working Directory: 실제 파일을 수정하는 공간
	
    2.	Staging Area: 다음 commit에 포함할 변경사항을 골라두는 공간
	
    3.	Repository History: commit이 실제로 저장된 버전 기록

---

## Module Structure

| File | Description|
|------|--------|
| 01_git_init.md | Initialize a Git repository and understand repository creation|
| 02_git_status.md | Inspect tracked, untracked, staged, and unstaged changes|
| 03_git_add_commit.md | Stage changes and save them into commit history|
| 04_git_log.md | Explore commit history and inspect past changes|

---

## 1️⃣ git init

File: 01_git_init.md

This command creates a new Git repository in the current directory.

```
git init
```

What it does
	•	creates a .git directory
	•	starts version control tracking
	•	turns a normal folder into a Git repository

## 한국어 설명

```git init은 현재 폴더를 Git 저장소로 바꾸는 명령어다. 

즉 Git을 사용할 준비를 시작하는 단계다.
```

---

## 2️⃣ git status

File: 02_git_status.md

This command shows the current state of the repository.

```
git status
```

What it shows
	•	untracked files
	•	modified files
	•	staged files
	•	branch status

## 한국어 설명

```
git status는 Git에서 가장 자주 사용하는 확인 명령어다.

현재 무엇이 변경되었는지, 무엇이 staging 되었는지, 무엇이 아직 추적되지 않는지 알려준다.
```

---

## 3️⃣ git add and git commit

File: 03_git_add_commit.md

These two commands form the core save workflow.

#### Stage changes
```
git add <file>
```

#### Commit staged changes
```
git commit -m "message"
```

#### Why both matter
	•	git add selects changes
	•	git commit records selected changes into history

## 한국어 설명
```
많은 초보자가 git add와 git commit을 하나로 생각하지만, 실제로는 다르다.
	•	git add = 이번 commit에 넣을 변경사항 선택
	•	git commit = 선택한 내용을 기록으로 저장

즉, Git은 선택 후 저장 구조다.
```

---

## 4️⃣ git log

File: 04_git_log.md

This command shows commit history.

```
git log
```

#### Common practical forms:
```
git log --oneline
git log --oneline -n 5
git log --oneline --graph --all
```

#### Why it matters
	•	inspect history
	•	debug past changes
	•	understand project evolution
	•	review commit messages

## 한국어 설명
```
git log는 과거 commit 기록을 확인하는 명령어다.
단순히 예전 기록을 보는 것을 넘어서, 버그를 추적하고 프로젝트 흐름을 이해하는 데 매우 중요하다.
```

---

## Recommended Beginner Workflow

A practical learning order for this directory is:
```
git init
   ↓
git status
   ↓
git add
   ↓
git commit
   ↓
git log
```
This order is important because it mirrors how Git is actually used in daily work.


## Example End-to-End Flow
```
git init
git status
git add README.md
git commit -m "docs: add initial README"
git log --oneline
```

## 한국어 설명
```
이 흐름은 Git의 가장 기본적인 사용 예시다.
	1.	저장소 생성
	2.	상태 확인
	3.	변경사항 staging
	4.	commit으로 저장
	5.	log로 기록 확인

이 다섯 단계를 반복하면서 Git을 사용하게 된다.
```

---

## Good Habits to Build Early

#### 1. Check status often
```
git status
```

#### 2. Write meaningful commit messages
```
git commit -m "feat: add Docker lifecycle practice script"
```

#### 3. Keep commits focused

A single commit should represent one logical change.

## 한국어 설명
```
Git을 잘 쓰는 사람은 단순히 명령어를 많이 아는 사람이 아니라,
작고 의미 있는 commit을 남기고, 자주 상태를 확인하고, 기록을 깔끔하게 유지하는 사람이다.
```

---

## Practical Importance for Portfolio Development

For a GitHub portfolio, Git basics matter because they show:
	•	consistency
	•	organization
	•	development discipline
	•	ability to manage changes systematically

A well-maintained Git history makes a project look more professional.

## 한국어 설명
```
GitHub 포트폴리오에서는 코드 자체뿐만 아니라 Git 사용 방식도 중요하다.

특히:
	•	commit 메시지 품질
	•	구조적인 작업 흐름
	•	변경 이력의 명확성

은 프로젝트의 완성도를 높여준다.
```

---

## Summary

This module introduces the foundational Git workflow:
```
git init
→ create repository

git status
→ inspect repository state

git add
→ stage changes

git commit
→ save changes to history

git log
→ inspect history
```
Together, these commands form the minimum Git skill set required for software development, data projects, and portfolio building.

---

## Final Takeaway
```
Git basics are not optional.
They are the foundation of professional development workflow.

Git 기초는 단순 명령어 암기가 아니라, 개발 기록을 구조적으로 관리하는 기본기다.
```