/*
Day 56 — Data Aggregation: Group By with reduce()

File
03_javascript/05_data_handling/03_data_aggregation/01_group_by_reduce.js

목표
JavaScript의 reduce()를 이용해서
SQL의 GROUP BY와 유사한 집계 로직을 구현한다.

핵심 주제
1) group by 기본 개념
2) count 집계
3) sum 집계
4) 평균 계산용 중간 구조 만들기
5) 실무형 데이터 집계 패턴

한국어 설명
JavaScript에는 SQL처럼 GROUP BY 문법이 없기 때문에,
배열 데이터를 그룹화하려면 reduce()를 자주 사용한다.

즉,

배열 데이터
→ key 기준으로 그룹핑
→ count / sum / average 등 계산

이 흐름을 직접 구현해야 한다.

이 패턴은
- API 응답 집계
- 대시보드 통계
- 로그 분석
- 매출 요약
등에서 매우 자주 사용된다.
*/


/* ============================================================
1) Example Dataset
============================================================ */

/*
예시: 주문 데이터
*/
const orders = [
  { id: 1, region: "Seoul", category: "Electronics", amount: 120000, status: "paid" },
  { id: 2, region: "Busan", category: "Food",        amount: 30000,  status: "paid" },
  { id: 3, region: "Seoul", category: "Food",        amount: 45000,  status: "cancelled" },
  { id: 4, region: "Seoul", category: "Electronics", amount: 80000,  status: "paid" },
  { id: 5, region: "Busan", category: "Food",        amount: 25000,  status: "paid" },
  { id: 6, region: "Incheon", category: "Beauty",    amount: 60000,  status: "paid" },
  { id: 7, region: "Seoul", category: "Beauty",      amount: 90000,  status: "paid" }
];

console.log("Original orders:", orders);


/* ============================================================
2) Basic Group By
============================================================ */

/*
region 기준으로 그룹핑

한국어 설명
- acc는 누적 객체(accumulator)
- order.region을 key로 사용
- 해당 key가 없으면 빈 배열 생성
- 해당 그룹 배열에 현재 order 추가
*/
const groupedByRegion = orders.reduce((acc, order) => {
  const key = order.region;

  if (!acc[key]) {
    acc[key] = [];
  }

  acc[key].push(order);
  return acc;
}, {});

console.log("Grouped by region:", groupedByRegion);


/* ============================================================
3) Count by Group
============================================================ */

/*
region별 주문 개수 세기

한국어 설명
- SQL로 치면 COUNT(*) GROUP BY region 과 유사
*/
const orderCountByRegion = orders.reduce((acc, order) => {
  const key = order.region;

  if (!acc[key]) {
    acc[key] = 0;
  }

  acc[key] += 1;
  return acc;
}, {});

console.log("Order count by region:", orderCountByRegion);


/* ============================================================
4) Sum by Group
============================================================ */

/*
region별 총 매출(amount) 합계

한국어 설명
- SQL의 SUM(amount) GROUP BY region 과 유사
*/
const revenueByRegion = orders.reduce((acc, order) => {
  const key = order.region;

  if (!acc[key]) {
    acc[key] = 0;
  }

  acc[key] += order.amount;
  return acc;
}, {});

console.log("Revenue by region:", revenueByRegion);


/* ============================================================
5) Count by Status
============================================================ */

/*
status별 주문 개수 집계
*/
const orderCountByStatus = orders.reduce((acc, order) => {
  const key = order.status;

  if (!acc[key]) {
    acc[key] = 0;
  }

  acc[key] += 1;
  return acc;
}, {});

console.log("Order count by status:", orderCountByStatus);


/* ============================================================
6) Sum by Category
============================================================ */

/*
category별 매출 합계
*/
const revenueByCategory = orders.reduce((acc, order) => {
  const key = order.category;

  if (!acc[key]) {
    acc[key] = 0;
  }

  acc[key] += order.amount;
  return acc;
}, {});

console.log("Revenue by category:", revenueByCategory);


/* ============================================================
7) Advanced Aggregation Object
============================================================ */

/*
region별 여러 통계 한번에 집계

한국어 설명
한 그룹에 대해:
- count
- totalAmount
를 동시에 저장
*/
const summaryByRegion = orders.reduce((acc, order) => {
  const key = order.region;

  if (!acc[key]) {
    acc[key] = {
      count: 0,
      totalAmount: 0
    };
  }

  acc[key].count += 1;
  acc[key].totalAmount += order.amount;

  return acc;
}, {});

console.log("Summary by region:", summaryByRegion);


/* ============================================================
8) Average Calculation
============================================================ */

/*
region별 평균 주문 금액 계산

한국어 설명
평균은 보통:
- count
- sum
을 먼저 만든 뒤
마지막에 sum / count 로 계산한다.
*/
const averageAmountByRegion = Object.fromEntries(
  Object.entries(summaryByRegion).map(([region, stats]) => {
    return [
      region,
      Number((stats.totalAmount / stats.count).toFixed(2))
    ];
  })
);

console.log("Average amount by region:", averageAmountByRegion);


/* ============================================================
9) Filter + Group By
============================================================ */

/*
paid 상태의 주문만 대상으로 region별 매출 집계
*/
const paidRevenueByRegion = orders
  .filter((order) => order.status === "paid")
  .reduce((acc, order) => {
    const key = order.region;

    if (!acc[key]) {
      acc[key] = 0;
    }

    acc[key] += order.amount;
    return acc;
  }, {});

console.log("Paid revenue by region:", paidRevenueByRegion);


/* ============================================================
10) Nested Group Summary
============================================================ */

/*
region 안에서 category별 매출 집계

한국어 설명
중첩 객체를 사용하면
2단계 group by 처럼 만들 수 있다.
*/
const nestedRevenue = orders.reduce((acc, order) => {
  const regionKey = order.region;
  const categoryKey = order.category;

  if (!acc[regionKey]) {
    acc[regionKey] = {};
  }

  if (!acc[regionKey][categoryKey]) {
    acc[regionKey][categoryKey] = 0;
  }

  acc[regionKey][categoryKey] += order.amount;

  return acc;
}, {});

console.log("Nested revenue by region and category:", nestedRevenue);


/* ============================================================
11) Reusable Group By Helper
============================================================ */

/*
재사용 가능한 count 집계 helper

한국어 설명
keySelector를 함수로 받아서
원하는 기준으로 count 집계를 수행
*/
function groupCountBy(array, keySelector) {
  return array.reduce((acc, item) => {
    const key = keySelector(item);

    if (!acc[key]) {
      acc[key] = 0;
    }

    acc[key] += 1;
    return acc;
  }, {});
}

const countByCategory = groupCountBy(orders, (order) => order.category);
console.log("Count by category (helper):", countByCategory);


/* ============================================================
12) Reusable Sum Helper
============================================================ */

/*
재사용 가능한 sum 집계 helper
*/
function groupSumBy(array, keySelector, valueSelector) {
  return array.reduce((acc, item) => {
    const key = keySelector(item);
    const value = valueSelector(item);

    if (!acc[key]) {
      acc[key] = 0;
    }

    acc[key] += value;
    return acc;
  }, {});
}

const paidRevenueByCategory = groupSumBy(
  orders.filter((order) => order.status === "paid"),
  (order) => order.category,
  (order) => order.amount
);

console.log("Paid revenue by category (helper):", paidRevenueByCategory);


/* ============================================================
13) Convert Aggregation Object to Rows
============================================================ */

/*
집계 결과를 표 형태로 바꾸기

한국어 설명
대시보드나 테이블 UI에서 보여주기 좋게
객체를 배열로 변환
*/
const regionSummaryRows = Object.entries(summaryByRegion).map(([region, stats]) => {
  return {
    region: region,
    count: stats.count,
    totalAmount: stats.totalAmount,
    averageAmount: Number((stats.totalAmount / stats.count).toFixed(2))
  };
});

console.log("Region summary rows:", regionSummaryRows);


/* ============================================================
14) Summary
============================================================ */

/*
정리

reduce() 기반 group by 패턴:

1. 초기값은 보통 {}
2. key를 계산
3. 그룹이 없으면 초기화
4. count / sum / stats 누적
5. 필요하면 마지막에 Object.entries()로 후처리

실무 활용:
- 주문 집계
- 상태별 통계
- 카테고리별 매출
- 지역별 사용자 수
- 로그 이벤트 요약
*/

console.log("Summary complete.");