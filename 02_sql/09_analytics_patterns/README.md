# SQL Analytics Patterns (09)

This directory contains **advanced analytics design patterns**
implemented purely in SQL.

It focuses on translating business questions into
structured, reproducible analytical workflows.

본 디렉토리는 SQL을 활용한  
**고급 분석 패턴(Advanced Analytics Patterns)**을 다룹니다.

단순 쿼리 작성이 아니라,  
비즈니스 질문을 → 분석 구조 → 지표 설계 → 의사결정 연결  
까지 이어지는 전체 분석 흐름을 설계합니다.

---

# 🎯 Core Objective

To move from:

Raw Tables  
→ Analytical Definitions  
→ Aggregation Logic  
→ Decision-Ready Metrics

---

# 📂 Module Structure

This section is organized into practical analytics domains:

1. Cohort Analysis
2. Retention Analysis
3. Funnel Analysis
4. Time Series Analysis
5. Segmentation

Each module builds reusable SQL patterns
that can be adapted to real production datasets.

---

# 01️⃣ Cohort Analysis (Day 23–25)

**Goal:**  
Understand how groups of users behave over time
based on their initial cohort.

### Files
- `01_define_cohort.sql`
- `02_cohort_size.sql`
- `03_retention_by_cohort.sql`

### Key Concepts
- Cohort month definition
- Month offset calculation
- Cohort-based retention tracking

---

# 02️⃣ Retention Analysis (Day 26–28)

**Goal:**  
Measure how many users remain active
after their first interaction.

### Files
- `01_define_retention.sql`
- `02_retention_matrix.sql`
- `03_retention_rate.sql`

### Key Concepts
- Retention event modeling
- Retention matrix design
- Retention rate KPI calculation

---

# 03️⃣ Funnel Analysis (Day 29–31)

**Goal:**  
Understand user drop-off between steps.

### Files
- `01_define_funnel_events.sql`
- `02_step_counts.sql`
- `03_conversion_rates.sql`

### Key Concepts
- Step-based event modeling
- Funnel step counts
- Conversion rate calculation
- Drop-off identification

---

# 04️⃣ Time Series Analysis (Day 32–34)

**Goal:**  
Analyze metrics over time
and detect trends or changes.

### Files
- `01_time_bucket_aggregation.sql`
- `02_moving_average.sql`
- `03_period_over_period.sql`

### Key Concepts
- Time bucketing
- Rolling window averages
- Period-over-period growth
- Trend analysis

---

# 05️⃣ Segmentation (Day 35–37)

**Goal:**  
Compare behavioral and revenue metrics
across user groups.

### Files
- `01_segment_definition.sql`
- `02_segment_metrics.sql`
- `03_segment_comparison.sql`

### Key Concepts
- Rule-based segmentation
- Segment-level KPI aggregation
- Share / Lift / Rank comparison

---

# 🧠 Architectural Perspective

These modules follow a unified analytical structure:

```text
Event / User Tables
        ↓
Behavior Modeling
        ↓
Aggregation Logic
        ↓
KPI Standardization
        ↓
Decision-Ready Output