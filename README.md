# 0311_db_project


1. 데이터 분석 (공통 컬럼 찾기)
2. 데이터 활용 기획 ( 데이터의 다양한 활용을 위한 기획 )

## 2-1.  1차 기획

1. 지연이 가장 많았던 항공사 - 예정출발시간 기준 
2. 국제선, 국내선 비율 
3. 각 공항과 계약된 항공사수
4. 비율비행취소여부에 따른 데이터 적재
5. 기간 내 항공사별 결항 횟수
6. 항공사별 지연시간 평균값
7.  출발은 지연되었으나 도착은 정시에 한 '회복 비행' 케이스


## 2-2. 2차 기획

01. 지연이 많았던 항공사 top5 (기간 1987.10 - 1989.12) - 도착지연시간 기준 (파이 차트)
필요한 컬럼 - 항공사코드(운반대.설명), 도착지연시간(0보다 큰 행의 갯수count)

02. 국제선, 국내선 비율 -  기간별 (파이 차트)
필요한 컬럼 - 년도, 월, 출발공항코드, 도착지공항코드

03. 각 공항을 이용하는 항공사 도출 (목록)
필요한 컬럼 - 항공사코드(운반대.설명), 출발공항코드, 도착지공항코드

04. 기간 내의 항공사별 결항 비율(비행취소여부에 따른 데이터 적재, 결항횟수/전체 운행 횟수)
필요한 컬럼 - 년도, 월, 항공사코드(운반대.설명), 비행취소여부

05. 실제경과시간과 예정경과시간의 갭을 토대로 항공사별 초과비행시간 평균값을 구할 수 있다. (바 차트)
필요한 컬럼 - 항공사코드, 실제경과시간, 예정경과시간 

06. 출발은 지연되었으나 도착은 정시에 한 '회복 비행' 케이스 비율- 항공사별(top 5) // (바 차트)
필요한 컬럼 - 항공사코드, 도착지연시간, 출발지연시간

## 2-3 최종 기획

01. 지연이 많았던 항공사 top5 (기간 1987.10 - 1989.12) - 도착지연시간 기준 (파이 차트)
컬럼 - 항공사코드(운반대.설명), 도착지연횟수

~~02. 국제선, 국내선 비율 -  기간별 (파이 차트)~~
~~필요한 컬럼 - 년도, 월, 출발공항코드, 도착지공항코드~~ - 데이터가 국내선으로 이루어졌기 때문에 국제선과 국내선의 구별이 필요 없다고 판단

02. 각 공항을 이용하는 항공사 도출 (목록)
컬럼 - 항공사코드(운반대.설명), 출발국가, 도착국가, 출발도시, 도착지도시

03. 기간 내의 항공사별 결항 비율(비행취소여부에 따른 데이터 적재, 결항횟수/전체 운행 횟수)
컬럼 - 년도, 월, 항공사코드(운반대.설명), 전체비행수, 실제비행수, 취소비행수, 실제비행비율, 취소비행비율

04. 실제경과시간과 예정경과시간의 갭을 토대로 항공사별 초과비행시간 평균값을 구할 수 있다. (바 차트)
컬럼 - 항공사코드, 실제경과시간, 예정경과시간

05. 출발은 지연되었으나 도착은 정시에 한 '회복 비행' 케이스 비율- 항공사별(top 5) // (바 차트)
컬럼 - 항공사코드, 도착지연시간, 출발지연시간

06. 항공사별 회복비행 비율 
컬럼 - 항공사명, 총지연횟수, 회복비행횟수, 회복비행비율


## 3-1 테이블 적재

### 1. data01 지연이 많았던 항공사 top5 (기간 1987.10 - 1989.12) - 도착지연시간 기준 (막대 차트)

```sql
INSERT INTO db_to_air.data01 (`항공사`, `도착지연횟수`)
SELECT 
    b.`설명` AS 항공사, 
    COUNT(a.`항공사코드`) AS 도착지연횟수
FROM 
    db_air.`비행` a
JOIN 
    db_air.`운반대` b ON a.`항공사코드` = b.`코드`
WHERE 
    a.`도착지연시간` REGEXP '^[0-9]+$' 
    AND CAST(a.`도착지연시간` AS UNSIGNED) > 0
GROUP BY 
    b.`설명`
ORDER BY
    도착지연횟수 DESC;
```

~~2. data2 국제선, 국내선 비율 -  기간별 (파이 차트)~~ -- 제외

```sql
-- data02 국제선, 국내선 비율 - 기간별 (파이 차트) // 필요한 컬럼 - 년도, 월, 국내선, 국제선 

-- TRUNCATE db_to_air.data02;

-- INSERT INTO db_to_air.data02 (`년도`, `월`, `국내선`, `국제선`)
-- SELECT
--     a.`년도`,
--     a.`월`,
--     SUM(CASE WHEN ap_start.`국가` = ap_end.`국가` THEN 1 ELSE 0 END) AS 국내선,
--     SUM(CASE WHEN ap_start.`국가` <> ap_end.`국가` THEN 1 ELSE 0 END) AS 국제선
-- FROM
--     db_air.`비행` a
-- JOIN
--     db_air.`항공사` ap_start ON a.`출발공항코드` = ap_start.`항공사코드` 
-- JOIN
--     db_air.`항공사` ap_end ON a.`도착지공항코드` = ap_end.`항공사코드` 
-- GROUP BY 
--     a.`년도`,
--     a.`월`
-- ORDER BY
--     a.`년도`,
--     a.`월`;
```

### 3. data03
```sql
INSERT INTO db_to_air.`data03` 
(
SELECT DISTINCT v.`항공사코드`,h.`국가`,a.`국가`,h.`도시`,a.`도시` 
FROM db_air.`비행` v 
INNER JOIN db_air.항공사 h 
    ON v.출발공항코드 = h.항공사코드
    AND h.도시 != 'NA' 
INNER JOIN db_air.항공사 a 
    ON v.도착지공항코드 = a.항공사코드 
    AND a.도시 != 'NA'
);
```

### 4. data04 
    - 기간 내의 항공사별 결항 비율(비행취소여부에 따른 데이터 적재, 결항횟수/전체 운행 횟수) // 필요한 컬럼 
    - 년도, 월, 항공사(운반대.설명), 전체비행수, 실제비행수, 취소비행수, 실제비행비율, 취소비행비율
```sql
INSERT INTO db_to_air.data04  (`년도`, `월`, `항공사`, `전체비행수`, `실제비행수`, `취소비행수`, `실제비행비율`, `취소비행비율`)
SELECT
    a.`년도`,
    a.`월`,
    b.`설명` AS 항공사,
    COUNT(*) AS 전체비행수,
    SUM(CASE WHEN a.`비행취소여부` = 0 THEN 1 ELSE 0 END) AS 실제비행수,
    SUM(CASE WHEN a.`비행취소여부` = 1 THEN 1 ELSE 0 END) AS 취소비행수,
    ROUND(SUM(CASE WHEN a.`비행취소여부` = '0' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS 실제비행비율,
    ROUND(SUM(CASE WHEN a.`비행취소여부` = '1' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS 취소비행비율
FROM 
    db_air.`비행` a
JOIN
    db_air.`운반대` b ON a.`항공사코드` = b.`코드`
GROUP BY
    a.`년도`, a.`월`, b.`설명` 
ORDER BY
    a.`년도`, a.`월`, b.`설명`;
```

### 5. data05
```sql
SELECT h.`설명` AS `항공사명`, f.`실제경과시간`, f.`예정경과시간`
FROM db_air.`비행` AS f
JOIN db_air.`운반대` AS h
ON(f.`항공사코드` = h.`코드` )
;
```

### 6. data06
```sql
SELECT h.`설명` AS `항공사명`, f.`도착지연시간`, f.`출발지연시간`
FROM db_air.`비행` AS f
JOIN db_air.`운반대` AS h
ON(f.`항공사코드` = h.`코드` )
;
```


## 3-2 뷰 적재

### 1. 공항별_항공사_목록 (data03)

```sql
CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `db_to_air`.`공항별_항공사_목록` AS
SELECT
    `d`.`출발도시` AS `공항`,
    `u`.`설명` AS `항공사명`,
    `d`.`항공사코드` AS `항공사코드`
FROM
    (`db_to_air`.`data03` `d`
JOIN `db_air`.`운반대` `u` ON
    (`d`.`항공사코드` = `u`.`코드`))
GROUP BY
    `d`.`출발도시`,
    `d`.`항공사코드`
UNION
SELECT
    `d`.`도착지도시` AS `공항`,
    `u`.`설명` AS `항공사명`,
    `d`.`항공사코드` AS `항공사코드`
FROM
    (`db_to_air`.`data03` `d`
JOIN `db_air`.`운반대` `u` ON
    (`d`.`항공사코드` = `u`.`코드`))
GROUP by
    `d`.`도착지도시`,
    `d`.`항공사코드`
ORDER by
    1,
    2;
```

### 2. 실운행_공항_목록 (data03)

```sql
CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `db_to_air`.`실운행_공항_목록` AS
SELECT
    `공항별_항공사_목록`.`공항` AS `공항`
FROM
    `db_to_air`.`공항별_항공사_목록`
GROUP BY
    `공항별_항공사_목록`.`공항`;
```

### 3. 취소비행비율_분기별_항공사_top5 (data04)

```sql
CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `db_to_air`.`취소비행비율_분기별_항공사_top5` AS
select
    `sub`.`년도` AS `년도`,
    `sub`.`분기` AS `분기`,
    `sub`.`항공사` AS `항공사`,
    `sub`.`전체비행수` AS `전체비행수`,
    `sub`.`실제비행비율` AS `실제비행비율`,
    `sub`.`취소비행비율` AS `취소비행비율`
from
    (
    select
        `db_to_air`.`data04`.`년도` AS `년도`,
        case
            when `db_to_air`.`data04`.`월` between 1 and 3 then '1분기'
            when `db_to_air`.`data04`.`월` between 4 and 6 then '2분기'
            when `db_to_air`.`data04`.`월` between 7 and 9 then '3분기'
            when `db_to_air`.`data04`.`월` between 10 and 12 then '4분기'
        end AS `분기`,
        `db_to_air`.`data04`.`항공사` AS `항공사`,
        sum(cast(`db_to_air`.`data04`.`전체비행수` as unsigned)) AS `전체비행수`,
        round(avg(cast(`db_to_air`.`data04`.`실제비행비율` as double)), 2) AS `실제비행비율`,
        round(avg(cast(`db_to_air`.`data04`.`취소비행비율` as double)), 2) AS `취소비행비율`,
        rank() over ( partition by `db_to_air`.`data04`.`년도`,
        case
            when `db_to_air`.`data04`.`월` between 1 and 3 then '1분기'
            when `db_to_air`.`data04`.`월` between 4 and 6 then '2분기'
            when `db_to_air`.`data04`.`월` between 7 and 9 then '3분기'
            when `db_to_air`.`data04`.`월` between 10 and 12 then '4분기'
        end
    order by
        sum(cast(`db_to_air`.`data04`.`전체비행수` as unsigned)) desc) AS `rnk`
    from
        `db_to_air`.`data04`
    group by
        1,
        2,
        3) `sub`
where
    `sub`.`rnk` <= 5
order by
    `sub`.`년도`,
    `sub`.`분기`,
    `sub`.`전체비행수` desc;
```

### 4. 취소비행비율_연도별_항공사_top5 (data04)
```sql
CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `db_to_air`.`취소비행비율_연도별_항공사_top5` AS
select
    `sub`.`년도` AS `년도`,
    `sub`.`항공사` AS `항공사`,
    `sub`.`전체비행수` AS `전체비행수`,
    `sub`.`실제비행비율` AS `실제비행비율`,
    `sub`.`취소비행비율` AS `취소비행비율`
from
    (
    select
        `db_to_air`.`data04`.`년도` AS `년도`,
        `db_to_air`.`data04`.`항공사` AS `항공사`,
        sum(cast(`db_to_air`.`data04`.`전체비행수` as unsigned)) AS `전체비행수`,
        round(avg(cast(`db_to_air`.`data04`.`실제비행비율` as double)), 2) AS `실제비행비율`,
        round(avg(cast(`db_to_air`.`data04`.`취소비행비율` as double)), 2) AS `취소비행비율`,
        rank() over ( partition by `db_to_air`.`data04`.`년도`
    order by
        sum(cast(`db_to_air`.`data04`.`전체비행수` as unsigned)) desc) AS `rnk`
    from
        `db_to_air`.`data04`
    group by
        1,
        2) `sub`
where
    `sub`.`rnk` <= 5
order by
    `sub`.`년도`,
    `sub`.`전체비행수` desc;
```

### 5. 취소비행비율_월별_항공사_top5 (data04)

```sql
CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `db_to_air`.`취소비행비율_월별_항공사_top5` AS
select
    `sub`.`년도` AS `년도`,
    `sub`.`월` AS `월`,
    `sub`.`항공사` AS `항공사`,
    `sub`.`전체비행수` AS `전체비행수`,
    `sub`.`실제비행비율` AS `실제비행비율`,
    `sub`.`취소비행비율` AS `취소비행비율`
from
    (
    select
        `db_to_air`.`data04`.`년도` AS `년도`,
        `db_to_air`.`data04`.`월` AS `월`,
        `db_to_air`.`data04`.`항공사` AS `항공사`,
        `db_to_air`.`data04`.`전체비행수` AS `전체비행수`,
        `db_to_air`.`data04`.`실제비행수` AS `실제비행수`,
        `db_to_air`.`data04`.`취소비행수` AS `취소비행수`,
        `db_to_air`.`data04`.`실제비행비율` AS `실제비행비율`,
        `db_to_air`.`data04`.`취소비행비율` AS `취소비행비율`,
        rank() over ( partition by `db_to_air`.`data04`.`년도`,
        `db_to_air`.`data04`.`월`
    order by
        cast(`db_to_air`.`data04`.`전체비행수` as unsigned) desc) AS `rnk`
    from
        `db_to_air`.`data04`) `sub`
where
    `sub`.`rnk` <= 5
order by
    `sub`.`년도`,
    `sub`.`월`,
    cast(`sub`.`전체비행수` as unsigned) desc;
```

### 6. 항공사별_초과비행시간 (data05)

```sql
CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `db_to_air`.`항공사별_초과비행시간` AS
select
    `db_to_air`.`data05`.`항공사명` AS `항공사명`,
    round(avg(`db_to_air`.`data05`.`실제경과시간` - `db_to_air`.`data05`.`예정경과시간`), 2) AS `평균초과비행시간`
from
    `db_to_air`.`data05`
where
    `db_to_air`.`data05`.`실제경과시간` - `db_to_air`.`data05`.`예정경과시간` > 0
group by
    `db_to_air`.`data05`.`항공사명`;
```

### 7. 항공사별_회복비행비율 (data06)

```sql
CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `db_to_air`.`항공사별_회복비행비율` AS
select
    `sub`.`항공사명` AS `항공사명`,
    `sub`.`총지연횟수` AS `총지연횟수`,
    `sub`.`회복비행횟수` AS `회복비행횟수`,
    round(`sub`.`회복비행횟수` / `sub`.`총지연횟수`, 2) AS `회복비행비율`
from
    (
select
    `db_to_air`.`data06`.`항공사명` AS `항공사명`,
    count(case when `db_to_air`.`data06`.`출발지연시간` > 0 then 1 end) AS `총지연횟수`,
    count(case when `db_to_air`.`data06`.`출발지연시간` > 0 and `db_to_air`.`data06`.`도착지연시간` <= 0 then 1 end) AS `회복비행횟수`
from
    `db_to_air`.`data06`
group by
    `db_to_air`.`data06`.`항공사명`) `sub`;
```
