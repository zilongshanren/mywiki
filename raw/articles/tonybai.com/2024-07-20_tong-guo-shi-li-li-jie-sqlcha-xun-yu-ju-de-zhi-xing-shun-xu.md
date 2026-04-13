---
title: 通过实例理解SQL查询语句的执行顺序
url: https://tonybai.com/2024/07/20/sql-query-execution-order/
published: '2024-07-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解SQL查询语句的执行顺序

![](../../assets/bb9fa645867bdd77.png)


[本文永久链接](https://tonybai.com/2024/07/20/sql-query-execution-order) – https://tonybai.com/2024/07/20/sql-query-execution-order

SQL查询语句是关系数据库操作的核心。SQL查询语句有简有繁，简单的SQL查询语句，比如：

```
SELECT column1, column2
FROM table_name
WHERE condition;
```


对于这种查询语句，即便初学者也十分容易理解和掌握。但复杂的SQL查询语句，比如：

```
SELECT department, AVG(salary) AS avg_salary
FROM employee_table
WHERE department IN ('IT', 'HR', 'Finance')
GROUP BY department
HAVING AVG(salary) > (SELECT AVG(salary) FROM employee_table)
ORDER BY avg_salary DESC
LIMIT 3;
```


这种包含了SELECT、FROM、WHERE、GROUP BY、HAVING、ORDER BY和LIMIT等多个子句的复杂查询语句，即便是有多年开发经验的开发人员，**如果不清楚各个子句的执行顺序**，也很容易写错，并导致非预期的查询结果。

关于SQL查询语句的执行顺序，互联网上有很多类似下面这样的速查表式(cheetsheet)的图：

![](../../assets/32a2d5bec315fd1f.png)


这些图对理解SQL查询语句的执行顺序很有帮助。但对于初学者来说，如果再有一个配套的实例就更完美了。在这篇文章中，我就来为说明SQL查询语句的执行顺序补充一个实例，期望能帮助大家更好地学习和理解SQL查询语句的执行顺序。

## 1. 实例的Schema和初始数据

本文将使用两个表：departments 表和employees表来演示查询操作。以下是这两个表的创建和初始数据插入语句：

注：本文试验环境使用的是MySQL数据库，关于MySQL数据库的安装和运行方法，可以参考我之前的一篇文章《

[通过实例理解Go访问和操作数据库的几种方式]》。

```
DROP DATABASE IF EXISTS example_db;
CREATE DATABASE example_db;
use example_db;
CREATE TABLE departments (
dept_id INT PRIMARY KEY,
dept_name VARCHAR(255)
);
CREATE TABLE employees (
emp_id INT PRIMARY KEY,
name VARCHAR(255),
salary DECIMAL(10, 2),
dept_id INT,
FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
```


我们事先在表中预置一些初始数据：

```
INSERT INTO departments (dept_id, dept_name) VALUES
(1, 'HR'),
(2, 'Engineering'),
(3, 'Marketing');
INSERT INTO employees (emp_id, name, salary, dept_id) VALUES
(1, 'Alice', 60000, 1),
(2, 'Bob', 50000, 1),
(3, 'Carol', 70000, 2),
(4, 'Dave', 55000, 2),
(5, 'Eve', 40000, 3),
(6, 'Frank', 80000, 2),
(7, 'Grace', 45000, 3),
(8, 'Heidi', 75000, 2),
(9, 'Ivan', 48000, 1),
(10, 'Judy', 51000, 3);
```


到这里，试验环境和数据就就绪了！

## 2. SQL查询语句

接下来，我们来编写一个复杂一些的查询语句，作为本文要分析的目标：

```
SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM employees as e
JOIN departments as d ON e.dept_id = d.dept_id
WHERE e.salary > 10000
GROUP BY d.dept_name
HAVING AVG(e.salary) > 50000
ORDER BY avg_salary DESC
LIMIT 3;
```


这条SQL查询语句的功能大致是从employees和departments两个表中查询每个部门(dept)的平均工资。那么这条语句究竟是怎么做到这一点的呢？我们通过下面对SQL语句执行顺序的**step by step**分析来一看究竟。

## 3. SQL查询语句执行顺序

在编写SQL查询语句时，理解其执行顺序是至关重要的。因为，**SQL语句中各个子句的执行顺序与它们在语句中的出现顺序并不一致**，比如像本文前面那张图展示的那样，查询语句中最先出现的select子句这样的[投影操作](https://tonybai.com/2023/11/15/relational-algebra-and-sql-with-go-examples/)其实是在后面执行的。

通常情况下，就像上图中所示，SQL查询语句的执行顺序如下：

```
FROM和JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```


下面我们就基于上述实例，对执行顺序中的每个子句进行分析。首先来看一下FROM/JOIN。

### 3.1 FROM和JOIN

SQL查询语句中的FROM和JOIN子句是最先执行的：

```
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
```


它们为后续的其他子句提供了操作的对象数据集合。Join会先根据指定的连接条件(通常是等值条件，比如这里的e.dept_id = d.dept_id)来连接两个表，只有满足连接条件的行才会被保留在结果集中。From将从这个联结后的大表中查询满足条件的数据。

执行后的中间结果如下：

```
+--------+-------+----------+---------+-------------+
| emp_id | name | salary | dept_id | dept_name |
+--------+-------+----------+---------+-------------+
| 1 | Alice | 60000.00 | 1 | HR |
| 2 | Bob | 50000.00 | 1 | HR |
| 9 | Ivan | 48000.00 | 1 | HR |
| 3 | Carol | 70000.00 | 2 | Engineering |
| 4 | Dave | 55000.00 | 2 | Engineering |
| 6 | Frank | 80000.00 | 2 | Engineering |
| 8 | Heidi | 75000.00 | 2 | Engineering |
| 5 | Eve | 40000.00 | 3 | Marketing |
| 7 | Grace | 45000.00 | 3 | Marketing |
| 10 | Judy | 51000.00 | 3 | Marketing |
+--------+-------+----------+---------+-------------+
```


### 3.2 WHERE

接下来来到了WHERE。

WHERE子句的作用是对FROM和JOIN提供的数据集合进行筛选，只保留满足某些条件的记录(行)，它相当于对上面JOIN表后的中间结果的数据集合施加了一个过滤器，只有满足过滤条件（这里是salary > 10000）的记录才会进入下一个中间结果的数据集合中。这样也可以减少后续子句操作的数据量，提高查询效率。

具体到这个示例上，WHERE子句如下：

```
WHERE e.salary > 10000
```


由于上面中间结果中每位雇员的工资(salary)都大于10000，因此这一步过滤之后，实际得到的中间结果与上面的表格中的数据是一样的。

### 3.3 GROUP BY

接下来执行的是GROUP BY。

这里GROUP BY子句的作用是将上述查询的中间结果集按照指定的列(dept_name)进行分组。使用GROUP BY进行分组的前提是SELECT投影的列必须是可分组的列，比如这里的dept_name和dept_id。如果SELECT投影的列是不可分组的列，比如这里的emp_id、name等，查询语句就会报错！

在我们的实例中，使用的是dept_name对上述查询的中间结果集进行分组和聚合运算的：

```
GROUP BY d.dept_name
```


该子句会根据部门名称(dept_name)进行分组，计算每个组的平均工资(AVG(e.salary))的计算也是在这时执行的，以下是执行后的中间结果：

```
+---------+-------------+--------------+
| dept_id | dept_name | avg_salary |
+---------+-------------+--------------+
| 1 | HR | 52666.666667 |
| 2 | Engineering | 70000.000000 |
| 3 | Marketing | 45333.333333 |
+---------+-------------+--------------+
```


注：这里包含了可分组的字段dept_id。关于这个字段是否真实包含在中间结果中可能与各个数据库的实现有关。


### 3.4 HAVING

HAVING子句在数据分组之后起作用，用于过滤分组后的结果。这个与执行选择关系操作Where过滤在作用时机上有所不同，WHERE子句在数据被分组之前起作用，用于过滤原始数据。

本例应用的HAVING条件如下：

```
HAVING AVG(e.salary) > 50000
```


即过滤出平均工资超过50000的组。下面是HAVING子句作用后的中间结果：

```
+---------+-------------+--------------+
| dept_id | dept_name | avg_salary |
+---------+-------------+--------------+
| 1 | HR | 52666.666667 |
| 2 | Engineering | 70000.000000 |
+---------+-------------+--------------+
```


### 3.5 SELECT

SELECT是我们最熟悉的关系代数操作了，也叫投影，用于选择所需的列。

在本实例中，我们选择了dept_name和avg_salary：

```
SELECT d.dept_name, AVG(e.salary) AS avg_salary
```


该子句作用后的中间结果如下：

```
+-------------+--------------+
| dept_name | avg_salary |
+-------------+--------------+
| HR | 52666.666667 |
| Engineering | 70000.000000 |
+-------------+--------------+
```


### 3.6 ORDER BY

最后执行的是排序子句，对中间结果按特定字段的升序或降序进行排列，这里我们按平均工资降序排列：

```
ORDER BY avg_salary DESC
```


得到的中间结果如下：

```
+-------------+--------------+
| dept_name | avg_salary |
+-------------+--------------+
| Engineering | 70000.000000 |
| HR | 52666.666667 |
+-------------+--------------+
```


### 3.7 LIMIT

最后，LIMIT子句用于限制结果集的记录数量，这里限制输出3个：

```
LIMIT 3
```


由于上面的中间结果已经仅剩2条记录，因此上面的中间结果就是最终结果：

```
+-------------+--------------+
| dept_name | avg_salary |
+-------------+--------------+
| Engineering | 70000.000000 |
| HR | 52666.666667 |
+-------------+--------------+
```


## 4. 小结

在这篇文章中，我们通过实例，从FROM/JOIN开始，逐步分析了WHERE、GROUP BY、HAVING、SELECT、ORDER BY和LIMIT子句的执行顺序，并提供了中间结果的输出。这个实例的分步讲解可以让大家清晰地理解SQL查询语句的执行顺序，有助于大家更好地理解复杂的SQL查询语句，为编写复杂且高效的SQL查询语句打下坚实的基础。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论