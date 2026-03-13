# SQL for ML — Label Generation

This module covers **label generation patterns in SQL** for machine learning workflows.

In machine learning, features alone are not enough.
A predictive model also needs a clearly defined **target variable (label)**.

This directory focuses on how to generate labels directly in SQL using
well-defined business logic and time-aware rules.

Typical examples include:

- purchase within 30 days
- churn within 60 days
- readmission within 90 days
- time until event occurs

---

# 🎯 Learning Objectives

After completing this module, you should be able to:

- define binary labels using SQL
- separate observation windows from prediction windows
- generate time-to-event labels for survival-style problems
- understand censoring in time-based label construction
- avoid leakage when creating labels

---

# Why Label Generation Matters

A machine learning problem is defined not only by its features,
but also by its **target definition**.

Poorly defined labels lead to:

- unclear prediction objectives
- inconsistent training datasets
- misleading evaluation results
- hidden data leakage

In practice, label generation is often one of the most important parts of
the ML pipeline.

---

# Module Structure

| File | Purpose |
|------|------|
| `01_binary_label.sql` | Generate a binary classification label |
| `02_time_to_event_label.sql` | Generate event indicator + time-to-event label |

---

# 1️⃣ Binary Label Generation

File  
`01_binary_label.sql`

This file demonstrates how to create a **binary label (0/1)** using SQL.

Example business question:

> Will a customer make a purchase within 30 days after the anchor date?

Typical output:

- `1` → event occurs within the prediction window
- `0` → event does not occur within the prediction window

Key concepts covered:

- anchor date
- prediction window
- binary event indicator
- label table creation
- class balance check

Example logic:

```text
anchor_date
    ↓
look for future event within 30 days
    ↓
if event exists → 1
else → 0
``` 

This is the foundation of many classification problems such as:
	•	churn prediction
	•	purchase prediction
	•	conversion prediction
	•	default prediction

# 2️⃣ Time-to-Event Label Generation

File
02_time_to_event_label.sql

This file demonstrates how to create time-to-event labels.

Instead of only predicting whether an event happens,
we also record how long it takes until the event occurs.

Typical output:
	•	event_indicator
	•	1 = event observed
	•	0 = censored
	•	event_time_days
	•	days until first event
	•	or censoring horizon if no event is observed

Example business question:

How many days does it take until a customer makes the first purchase after the anchor date?

Key concepts covered:
	•	first event after anchor date
	•	event time calculation
	•	censoring
	•	fixed observation horizon
	•	distribution checks

Example logic:

``` 
anchor_date
    ↓
search future events within 90 days
    ↓
if first event exists:
    event_indicator = 1
    event_time_days = days until event
else:
    event_indicator = 0
    event_time_days = 90
``` 

This pattern is especially important for:
	•	survival analysis
	•	healthcare outcome modeling
	•	risk modeling
	•	customer lifetime / churn timing analysis

---
# Observation Window vs Prediction Window

A critical concept in label generation is the separation of time periods.

```
Past / Observation Window
    ↓
anchor_date
    ↓
Future / Prediction Window
``` 

	•	Observation Window
	•	used for feature generation
	•	includes historical data only
	•	Prediction Window
	•	used for label generation
	•	includes future event outcomes

This separation is essential for building valid ML datasets.

---
## Leakage Awareness

A common mistake in ML pipelines is data leakage.

For example, when predicting future purchase:

❌ Invalid feature examples:
	•	number of purchases after anchor date
	•	spending after anchor date
	•	future last activity date

These use information from the future and contaminate the training data.

Correct principle:

```
before anchor_date  → features
after anchor_date   → labels only
```

This module is designed to reinforce that rule.

---
## Practical Workflow

A typical SQL for ML pipeline looks like this:

```
Raw Tables
    ↓
Feature Engineering
    ↓
Label Generation
    ↓
Feature Table + Label Table
    ↓
Training Dataset
```
This module covers the label generation stage of that pipeline.

---
## Why SQL is Useful for Label Generation

SQL is often the best place to generate labels because it offers:
	•	direct access to event history
	•	reproducible logic
	•	scalable processing on large datasets
	•	easy integration with feature marts / training tables

Instead of manually constructing labels in notebooks,
SQL-based label generation produces a cleaner and more auditable workflow.

---
## Practical Importance

These label generation patterns are commonly used in:
	•	customer churn prediction
	•	purchase propensity modeling
	•	fraud / default event modeling
	•	healthcare time-to-event research
	•	retention and risk analytics

Understanding label generation is essential because:
	•	label definition determines the prediction problem
	•	time boundaries determine dataset validity
	•	leakage prevention determines model trustworthiness

---
# Summary

This module introduces two core label generation patterns in SQL:

``` 
Binary Label
→ event happens or not

Time-to-Event Label
→ whether the event happens
→ and how long it takes
``` 

Together, these patterns form the foundation for
classification and survival-style machine learning datasets.