---
title: 关系代数、SQL语句和Go语言示例
url: https://tonybai.com/2023/11/15/relational-algebra-and-sql-with-go-examples/
published: '2023-11-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 关系代数、SQL语句和Go语言示例

![](../../assets/a83e481891a7fa2b.png)


[本文永久链接](https://tonybai.com/2023/11/15/relational-algebra-and-sql-with-go-examples) – https://tonybai.com/2023/11/15/relational-algebra-and-sql-with-go-examples

近些年，数据库领域发展日新月异，除传统的关系型数据库外，还出现了许多新型的数据库，比如：以HBase、Cassandra、MongoDB为代表的NoSQL数据库，以InfluxDB、TDEngine为代表的[时序数据](https://tonybai.com/2023/05/28/understand-time-series-of-tsdb/)库，以Neo4J、Dgraph为代表的图数据库，以Redis、Memcached等为代表的内存数据库，以Milvus为代表的向量数据库，以CockroachDB、TiDB为代表的HTAP融合数据库以及云原生数据库等。各类型数据库都有自己的优势，开发者可以根据应用场景选择最合适的数据库。

不过，关系型数据库依旧是当今最流行的数据库管理系统，广泛应用于企业应用，也是大多数数应用开发人员日常接触最多的一种数据库类型。关系型数据库通过关系模型和关系代数的理论基础，实现了对关系数据的高效组织和操作。但许多开发人员在使用SQL进行数据库开发时，往往感到关系代数晦涩难懂，对SQL语句的语义理解不透彻，这给数据库应用开发带来了困难。

在这篇文章中，我们就来研究一下关系模型和关系代数，探究其与SQL语句的对应关系，并用Go语言代码示例实现相关查询，期望能帮助读者增进对关系数据库的理解，减轻数据库开发痛点，提高数据库应用能力。

## 1. 关系模型(Relational Model)

20世纪70年代，IBM研究员E.F. Codd在“A Relational Model of Data for Large Shared Data Banks”这篇论文中提出了关系模型的概念。随后，E.F.Codd又陆续发表了多篇文章，用数学理论奠定了关系数据库的基础，为关系数据库建立了一个数据模型 —— **关系数据模型**。

关系模型基于谓词逻辑和集合论，有严格的数学基础，提供了高级别的数据抽象层次，并不规定数据存取的具体过程，而是交由DBMS(数据库管理系统)自己实现。

关系模型之所以成为DBMS领域的主流模型，正是由于其非常简单(相较于更早的网络模型(network model)和层次模型(hierarchical model))，下面是关系模型中定义的一些概念：

- 关系(Relation)

E.F.Codd的论文对关系(Relation)的定义是这样的：“这里的关系是指公认的数学意义上的关系。给定集合S1, S2, … ,Sn（不一定互不相关），如果 R是由n元组(n-tuples)组成的集合，其中每个元组的第一个元素来自S1，第二个元素来自S2，以此类推，那么R就是这n个集合(S1~Sn)上的一个关系”。

不用你说，我也知道这段文字太过抽象！下面我尽力用一个图来呈现一下Relation的含义：

![](../../assets/335cf53fda5c2ec9.png)


我们看到，关系(Relation)是一个集合，实质上是一个“二维表格结构”，把上图中不属于R中的元组去掉，看起来可能更清晰一些：

![](../../assets/82e4fe66f5fe8e0d.png)


这个结构中的每一行就是1个n元组(n-tuples)，列则是S1到Sn，一共n个列。n元组中的数据依次分别来自S1、S2、…Sn。

- 元组(Tuple)

关系(Relation)这个“二维表格结构”中的每一个n元组，即每一行，被称作元组(Tuple)。

- 属性(Attribute)

关系(Relation)这个“二维表格结构”中的每一列(Sn)被称作一个属性(Attribute)。

- 域(Domain)

属性可能取值的范围被称为该属性的域，以图中属性S3为例，S3-e1、S3-e2一直到S3-ek都在该属性的域中，显然{S3-e1, S3-e2, …, S3-ek}这个集合是属性S3的域的一个子集。有个特殊的值null是所有域的一个成员，它一般表示值为”unknown”。

论文在定义关系模型时，还定义了一些模型的额外特征，比如：

- 元组的顺序是不重要的；
- 所有的元组(行)是不同的；
- … …

有了关系模型的定义，接下来就可以在模型基础上定义以关系操作对象的运算了，这种运算的集合就构成了**关系代数**。

## 2. 关系代数（Relational Algebra）

关系代数由一系列操作组成，这些操作将一个或两个关系作为输入，并产生一个新的关系作为结果。概括来说就是关系代数的运算通过输入有限数量的关系进行运算，运算结果仍为关系。

关系代数定义了一些基本关系运算和扩展关系运算，其中基本关系运算包括：

- 选择（Selection）
- 投影（Projection）
- 笛卡儿积（Cartesian Product）
- 连接（Join）
- 除（Division）
- 关系并（Union）
- 关系差（Difference）

扩展运算包括：

- 关系交（Intersection）
- 重命名（Rename）
- … …

注：关于关系代数的基本关系运算与扩展关系运算的定义在不同书籍里或资料里有所不同。比如在《数据库查询优化器的艺术》一书中，作者认为：关系代数（Relational Algebra）是在集合代数基础上发展起来的，其数据的操作可分为传统的集合运算和专门的关系运算两类。传统的集合运算包括并（Union）、差（Difference）、交（Intersection）和笛卡儿积（Cartesion Product），专门的关系运算包括选择（Select）、投影（Project）、连接（Join）和除（Division）。关系代数中五个基本的操作并（Union）、差（Difference）、笛卡儿积（Cartesion Product）、选择（Select）和投影（Project）组成了关系代数完备的操作集。


关系代数中的一些操作（如选择、投影和重命名操作）被称为一元操作(unary operation)，因为它们只对一个关系进行操作。其他操作，如关系并、笛卡尔积和关系差，则是对一对关系进行操作，因此称为二元操作(binary operation)：

![](../../assets/d3ee3e60559b7d2d.png)


到这里，我们知道了关系模型的概念定义以及基于关系的代数运算都有哪些。那么关系模型、代数运算与我们日常的关系数据库以及我们使用的SQL语句的对应关系是什么呢？接下来我们就逐一说明一下。

## 3. 关系模型与关系数据库实现的对应关系

讲到这里，其实大家心里或多或少都有个数了，关系模型与关系数据库实现中概念的对应关系十分明显：

- 关系型数据库中的表(table)对应关系模型中的关系(relation)；
- 关系型数据库中的表的记录行(row)对应关系模型中的元组(triple)；
- 关系型数据库中的表的列(column)对应关系模型中的属性(attribute)；
- 关系型数据库中的表的列数据类型(column type)对应关系模型中的属性的域(domain)。

当然关系型数据库与关系模型还有一些对应关系不是本文重点，比如：

- 关系模型中的关系完整性约束（如实体完整性、参照完整性等）对应于关系数据库中的约束（如主键约束、外键约束等）。
- 关系模型中的范式理论（如第一范式、第二范式等）对应于关系数据库中的数据规范化过程。

我们下面要关注的一个最重要的对应就是**关系模型中的关系代数运算对应于关系数据库中的查询操作**，我们可以使用SQL语句来实现关系模型中的运算，这也是下面我们要重点说明的内容，通过了解SQL语句背后实现的关系代数运算的本质，将可以帮助我们更好地理解关系模型，对后续数据库设计以及数据操作的高效性都大有裨益。

## 4. 关系代数与SQL的对应关系

终于来到最重要的内容了，其实就是通过SQL如何实现关系代数的操作，这也是作为应用开发人员最最关心的内容。

### 4.1 预先定义的关系

为了便于后续的说明，这里我们预先定义一些关系(表)，它们将用在后续说明各个关系运算符的示例中，这些表见下图：

![](../../assets/c256208a1d57d45c.png)


这里包含一个学生表(Students)、一个课程清单表(Courses)以及两年年度的选课表：CourseSelection2022和CourseSelection2023(注：这里不讨论表设计的合理性)。

文中使用[sqlite](http://sqlite.org)做为数据库管理系统(DBMS)的代表，主要是为了简单，SQL标准的兼容性也不错。下面的Go代码用于创建上图中的表并插入样例数据：

```
// relational-algebra-examples/create_database/main.go
package main
import (
"database/sql"
"fmt"
_ "modernc.org/sqlite"
)
func createTable(db *sql.DB, sqlStmt string) error {
stmt, err := db.Prepare(sqlStmt)
if err != nil {
fmt.Println("prepare statement error:", err)
return err
}
_, err = stmt.Exec()
if err != nil {
fmt.Println("exec prepared statement error:", err)
return err
}
return nil
}
func createTables(db *sql.DB) error {
// 创建Students表
err := createTable(db, `CREATE TABLE IF NOT EXISTS Students (
Sno INTEGER PRIMARY KEY,
Sname TEXT,
Gender TEXT,
Age INTEGER
)`)
if err != nil {
fmt.Println("create table Students error:", err)
return err
}
// 创建Courses表
err = createTable(db, `CREATE TABLE IF NOT EXISTS Courses (
Cno INTEGER PRIMARY KEY,
Cname TEXT,
Credit INTEGER
)`)
if err != nil {
fmt.Println("create table Courses error:", err)
return err
}
// 2022选课表
err = createTable(db, `CREATE TABLE CourseSelection2022 (
Sno INTEGER,
Cno INTEGER,
Score INTEGER,
PRIMARY KEY (Sno, Cno),
FOREIGN KEY (Sno) REFERENCES Students(Sno),
FOREIGN KEY (Cno) REFERENCES Courses(Cno)
)`)
if err != nil {
fmt.Println("create table CourseSelection2022 error:", err)
return err
}
// 2023选课表
err = createTable(db, `CREATE TABLE CourseSelection2023 (
Sno INTEGER,
Cno INTEGER,
Score INTEGER,
PRIMARY KEY (Sno, Cno),
FOREIGN KEY (Sno) REFERENCES Students(Sno),
FOREIGN KEY (Cno) REFERENCES Courses(Cno)
)`)
if err != nil {
fmt.Println("create table CourseSelection2023 error:", err)
return err
}
return nil
}
func checkErr(err error) {
if err != nil {
panic(err)
}
}
func insertData(db *sql.DB) {
// 向Students表插入数据
stmt, err := db.Prepare("INSERT INTO Students VALUES (?, ?, ?, ?)")
checkErr(err)
_, err = stmt.Exec(1001, "张三", "M", 20)
checkErr(err)
_, err = stmt.Exec(1002, "李四", "F", 18)
checkErr(err)
_, err = stmt.Exec(1003, "王五", "M", 19)
checkErr(err)
// 向Courses表插入数据
stmt, err = db.Prepare("INSERT INTO Courses VALUES (?, ?, ?)")
checkErr(err)
_, err = stmt.Exec(1, "数据库", 4)
checkErr(err)
_, err = stmt.Exec(2, "数学", 2)
checkErr(err)
_, err = stmt.Exec(3, "英语", 3)
checkErr(err)
// 插入2022选课数据
stmt, _ = db.Prepare("INSERT INTO CourseSelection2022 VALUES (?, ?, ?)")
_, err = stmt.Exec(1001, 1, 85)
checkErr(err)
_, err = stmt.Exec(1001, 2, 80)
checkErr(err)
_, err = stmt.Exec(1002, 1, 83)
checkErr(err)
_, err = stmt.Exec(1003, 1, 76)
checkErr(err)
// ...
// 插入2023选课数据
stmt, _ = db.Prepare("INSERT INTO CourseSelection2023 VALUES (?, ?, ?)")
stmt.Exec(1001, 3, 75)
checkErr(err)
stmt.Exec(1002, 2, 81)
checkErr(err)
stmt.Exec(1003, 3, 86)
checkErr(err)
}
func main() {
db, err := sql.Open("sqlite", "../test.db")
defer db.Close()
if err != nil {
fmt.Println("open test.db error:", err)
return
}
err = createTables(db)
if err != nil {
fmt.Println("create table error:", err)
return
}
insertData(db)
}
```


这里我们使用了[cznic大神](https://gitlab.com/cznic)实现并开源的modernc.org/sqlite，这是一个纯Go的sqlite3数据库driver。Go社区另一个广泛使用的sqlite3的driver库为[go-sqlite3](https://github.com/mattn/go-sqlite3)，只不过go-sqlite3是使用cgo对sqlite3 C库的封装。

执行上面go代码，便可以建立一个名为test.db的sqlite数据库，我们通过sqlite官方的[命令行工具(cli)](https://tonybai.com/2023/03/25/the-guide-of-developing-cli-program-in-go)也可以与该数据库文件交互(这里我们使用的是容器版cli)，比如：

```
$docker pull nouchka/sqlite3
// cd到test.db文件路径下
$docker run -v {test.db文件所在目录的绝对路径}:/root/db -it nouchka/sqlite3
SQLite version 3.40.1 2022-12-28 14:03:47
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open ./test.db
sqlite> .databases
main: /root/db/test.db r/w
sqlite> .tables
CourseSelection2022 Courses
CourseSelection2023 Students
sqlite>
```


接下来，我们就先从关系代数运算中最容易理解的一元运算符开始说起。

### 4.2. 选择（Selection)

“选择”是一元关系运算，它的运算符为σ，语义如下：

```
R' = σ[p](R) = {t | t∈R ∩ p(t) = true } // 这里用[p]表示数学符号的下标
```


其中R为关系，t为元组，p是谓词(predicate)表达式的组合，可以由一个或多个谓词表达式构成。

这个语义相对好理解一些：它对R的操作结果依然是关系R’，即一个新元组集合，这个元组集合中的元组来自R，但必须满足p(t) = true的条件。说直白一些，就是**选择满足给定条件的元组**。下面是一个“选择”操作的示意图：

![](../../assets/b9cbb5d96101ffa8.png)


我们可以用下面最常见的SQL语句实现对单一关系(表)的选择运算：

```
SELECT * FROM R WHERE p(t) = true;
```


对应Go示例的代码片段如下：

```
// relational-algebra-examples/query/main.go
func doSelection(db *sql.DB) {
rows, _ := db.Query("SELECT * FROM CourseSelection2022 where score >= 80") // p(t)为score >= 80
var selections []CourseSelection
for rows.Next() {
var s CourseSelection
rows.Scan(&s.Sno, &s.Cno, &s.Score)
selections = append(selections, s)
}
fmt.Println(selections)
}
```


输出结果为：

```
[{1001 1 85} {1001 2 80} {1002 1 83}]
```


### 4.3 投影（Projection）

“投影”也是一元关系运算，它的运算符为∏，语义如下：

```
R' = ∏[A1,A2,...,An](R) = {t[A1,A2,...,An]| t∈R } // 这里A1,A2,...,An表示从R中取出的列名
```


显然和“选择”通过谓词表达式选元组不同，“投影”选择一个关系中的指定列(A1,A2,…,An)，即选择需要的属性。下面是其运算过程的示意图：

![](../../assets/e4d4b27a1bdda00d.png)


“投影”对应的SQL语句也是我们最熟悉的语句：

```
SELECT A1, A2, ..., An FROM R;
```


对应Go示例的代码片段如下：

```
// relational-algebra-examples/query/main.go
func doProjection(db *sql.DB) {
rows, _ := db.Query("SELECT Sno, Sname FROM Students") // A1 = Sno, A2 = Sname
var students []Student
for rows.Next() {
var s Student
rows.Scan(&s.Sno, &s.Sname)
students = append(students, s)
}
fmt.Println(students)
}
```


输出结果为：

```
[{1001 张三 0} {1002 李四 0} {1003 王五 0}]
```


不过要注意的是：取消某些关系列后可能出现重复行，违反了关系的定义(关系是一个元组的集合)，因此必须检查并去除结果关系中重复的元组。

### 4.4 运算符的组合（Composition）

关系运算的输入是关系，结果也是一个关系，因此我们可以将关系运算符组合成一个更复杂的关系运算符表达式来实现更复杂的运算。比如将上面的两个一元关系运算符组合在一起“先选元组，再选属性”：

```
R' = ∏[A1,A2,...,An](σ[p](R))
```


其运算过程如下图所示：

![](../../assets/4e4d7c42f6337645.png)


上述运算符组合对应的SQL语句如下：

```
SELECT A1, A2, ..., An FROM R where p(t) = true;
```


对应Go示例的代码片段如下：

```
// relational-algebra-examples/query/main.go
func doCompositionOperation(db *sql.DB) {
rows, _ := db.Query("SELECT Sno, Sname FROM Students where age >= 20")
var students []Student
for rows.Next() {
var s Student
rows.Scan(&s.Sno, &s.Sname)
students = append(students, s)
}
fmt.Println(students)
}
```


输出结果为：

```
[{1001 张三 0}]
```


无论是选择运算还是投影运算，亦或是组合之后的运算，理解起来都相对容易，因为只涉及一个“关系”。接下来我们就看一下涉及两个关系的二元运算符，我们先来看看**集合运算**。

### 4.5 关系交（Intersection）

如果没有记错，我们是在高中学习的集合代数。那时定义两个集合的交集运算是这样的：

```
对于集合A和B，其交运算(Intersction)为：
A ∩ B = { x | x ∈ A且 x ∈ B}
```


用一个一维空间的数的集合的例子来说，就是当A = {1, 2, 3, 4, 5}，B = { 3, 5, 6, 9}时，A ∩ B = {3, 5}。我们通常用维恩图来示意集合运算：

![](../../assets/fe8ecd1aaea5b58f.png)


在关系模型中，元组是一维集合，关系是元组的集合，即是一个二维集合，那么基于关系的交运算就要有一个前提：那就是**参与运算的两个关系的属性必须是兼容的**。

两个关系的属性兼容需满足以下条件：

- 属性数量相同

两个关系中的属性数量必须相同。

- 属性类型相同或可转换

两个关系中对应位置的属性类型必须相同或可以通过类型转换进行兼容。例如，一个关系中的属性类型是整数，而另一个关系中的属性类型是浮点数，这种情况下属性类型是兼容的，因为整数可以隐式转换为浮点数。

- 属性名称可以不同

两个关系中对应位置的属性名称可以不同，只要它们的属性类型兼容即可。属性名称的不同不会影响属性兼容性。

在关系模型中，两个关系的属性兼容性是判断两个关系是否可以进行某些操作(包括集合操作)的重要条件之一。

回到集合运算，如果两个关系的属性不兼容，则这两个关系无法进行集合运算，比如Students表和Courses表的属性个数不同，如果对它们进行关系交运算，会导致报错：

```
SELECT * FROM Students INTERSECT SELECT * FROM Courses;
Parse error: SELECTs to the left and right of INTERSECT do not have the same number of result columns
```


介绍完集合运算的前提后，我们再来看关系交运算，其语义入下：

```
R' = R1 ∩ R2
```


即两个关系R1和R2在属性兼容的前提下进行关系交运算的结果为返回两个关系中相同的元组。

关系交运算对应的SQL语句如下：

```
SELECT * FROM R1 INTERSECT SELECT * FROM R2;
```


对应Go示例的代码片段如下：

```
// relational-algebra-examples/query/main.go
func doIntersection(db *sql.DB) {
rows, _ := db.Query("SELECT * FROM CourseSelection2022 INTERSECT SELECT * FROM CourseSelection2023")
var selections []CourseSelection
for rows.Next() {
var s CourseSelection
rows.Scan(&s.Sno, &s.Cno, &s.Score)
selections = append(selections, s)
}
fmt.Println(selections)
}
```


由于CourseSelection2022和CourseSelection2023这两个关系没有相同元组，所以上述Go程序输出的结果为空。

### 4.6 关系并（Union）

和关系交一样，两个关系进行关系并运算的前提也是属性兼容。关系并运算的语义如下：

```
R' = R1 ∪ R2
```


即两个关系R1和R2在属性兼容的前提下进行关系并运算的结果为返回两个关系中的所有元组，但要去除重复元组。

关系并对应的SQL语句如下：

```
SELECT * FROM R1 UNION SELECT * FROM R2;
```


对应Go示例的代码片段如下：

```
// relational-algebra-examples/query/main.go
func doUnion(db *sql.DB) {
rows, _ := db.Query("SELECT * FROM CourseSelection2022 UNION SELECT * FROM CourseSelection2023")
var selections []CourseSelection
for rows.Next() {
var s CourseSelection
rows.Scan(&s.Sno, &s.Cno, &s.Score)
selections = append(selections, s)
}
fmt.Println(selections)
}
```


CourseSelection2022和CourseSelection2023这两个关系没有重复元组，所有关系并运算后得到的结果关系中包含了这两个关系的全部元组，上述程序的输出结果为：

```
[{1001 1 85} {1001 2 80} {1001 3 75} {1002 1 83} {1002 2 81} {1003 1 76} {1003 3 86}]
```


### 4.7 关系差（Difference）

在集合代数中，对于集合A和B，其差运算为：

```
A - B = { x | x ∈ A且 x ∉ B}
```


即从A集合中排除掉B集合中的元素。

在关系模型中，关系差运算即是从一个关系中排除另一个关系中的元组，其语义如下：

```
R' = R1-R2={t|t∈R1 ∩ t∉R2} // t为关系中的元组
```


在SQL中，我们可以用NOT IN实现：

```
SELECT * FROM R1 WHERE A1 NOT IN (SELECT A1 FROM R2 WHERE 条件)
```


下面是对应的Go语言代码片段：

```
// relational-algebra-examples/query/main.go
func doDifference(db *sql.DB) {
rows, _ := db.Query("SELECT * FROM CourseSelection2022 WHERE Cno NOT IN (SELECT Cno FROM CourseSelection2023)")
var selections []CourseSelection
for rows.Next() {
var s CourseSelection
rows.Scan(&s.Sno, &s.Cno, &s.Score)
selections = append(selections, s)
}
fmt.Println(selections)
}
```


这段示例的含义是选出CourseSelection2022的元组，但去掉Cno值在CourseSelection2023出现过的元组。下面是运行结果：

```
[{1001 1 85} {1002 1 83} {1003 1 76}]
```


注意：关系差运算的前提也是两个关系的属性兼容。

最后看看略复杂的二元运算符：笛卡尔积和连接。

### 4.8 笛卡尔积(Cartesian-product)

在关系代数中，关系积，即笛卡尔积（Cartesian Product）这种运算(也被称为关系叉乘)用于取两个关系的所有可能的组合。它的数学语义可以描述为：给定关系R1和R2，它们的笛卡尔积结果是一个新的关系，其中的元组由R1中的每个元组与R2中的每个元组的组合构成。

在SQL中，笛卡尔积可以通过使用CROSS JOIN关键字来实现：

```
SELECT * FROM R1 CROSS JOIN R2;
```


也可以通过下面SQL语句来实现：

```
SELECT R1.*, R1.* FROM R1, R2;
```


对应的Go代码片段如下：

// relational-algebra-examples/query/main.go

```
// StudentCourse结果
type StudentCourse struct {
Sno int
Sname string
Gender string
Age int
Cno int
Cname string
Credit int
}
func doCartesianProduct(db *sql.DB) {
rows, _ := db.Query("SELECT * FROM Students CROSS JOIN Courses")
// rows, _ := db.Query("SELECT Students.*, Courses.* FROM Students, Courses")
var selections []StudentCourse
for rows.Next() {
var s StudentCourse
rows.Scan(&s.Sno, &s.Sname, &s.Gender, &s.Age, &s.Cno, &s.Cname, &s.Credit)
selections = append(selections, s)
}
fmt.Println(len(selections))
fmt.Println(selections)
}
```


示例的运行结果如下：

```
9
[{1001 张三 M 20 1 数据库 4} {1001 张三 M 20 2 数学 2} {1001 张三 M 20 3 英语 3} {1002 李四 F 18 1 数据库 4} {1002 李四 F 18 2 数学 2} {1002 李四 F 18 3 英语 3} {1003 王五 M 19 1 数据库 4} {1003 王五 M 19 2 数学 2} {1003 王五 M 19 3 英语 3}]
```


我们看到对Students和Courses两个关系(表)进行笛卡尔积运算后，结果包含了Students中的每个元组与Courses中的每个元组进行组合的结果(3×3=9个)。

需要注意的是，由于笛卡尔积可能导致非常大的结果集，因此在实际使用中应谨慎使用，并且通常需要与其他运算符和条件结合使用，以限制结果的大小和提高查询效率。通常我们会用连接来达到这些目的。

### 4.9 连接(Join)

连接(Join)运算(⋈)是从两个关系的笛卡儿积中选取属性间满足一定条件的元组形成一个新的关系，即将笛卡尔积和选择(selection)运算合并达到一个操作中。从这个角度来看，**笛卡尔积可以视为一种无条件的连接**。

连接代数运算符是关系代数中很有用的关系代数运算符，也是日常经常使用的运算符，它有很多种不同的子类别，下面我们分别看看各种子类型的语义、SQL语句以及对应的Go代码示例。

#### 4.9.1 等值连接（Equijoin）

等值连接是通过比较两个关系(表)之间的属性值是否相等来进行连接的操作。连接条件使用等号（=）来比较属性值的相等性。

我们直接看Go示例：

```
// relational-algebra-examples/query/main.go
func dumpOperationResult(operation string, rows *sql.Rows) {
cols, _ := rows.Columns()
w := tabwriter.NewWriter(os.Stdout, 0, 2, 1, ' ', 0)
defer w.Flush()
w.Write([]byte(strings.Join(cols, "\t")))
w.Write([]byte("\n"))
row := make([][]byte, len(cols))
rowPtr := make([]any, len(cols))
for i := range row {
rowPtr[i] = &row[i]
}
fmt.Printf("\n%s operation:\n", operation)
for rows.Next() {
rows.Scan(rowPtr...)
w.Write(bytes.Join(row, []byte("\t")))
w.Write([]byte("\n"))
}
}
func doEquijoin(db *sql.DB) {
rows, _ := db.Query("SELECT * FROM CourseSelection2022 JOIN Students ON CourseSelection2022.Sno = Students.Sno")
dumpOperationResult("Equijoin", rows)
}
```


这个示例使用等值连接将CourseSelection2022表和Students表连接起来，连接条件是CourseSelection2022.Sno = Students.Sno，即学生编号相等，返回的结果将包含CourseSelection2022和Students两个表中满足连接条件的元组。

我们看看程序运行的输出结果：

```
Equijoin operation:
Sno Cno Score Sno Sname Gender Age
1001 1 85 1001 张三 M 20
1001 2 80 1001 张三 M 20
1002 1 83 1002 李四 F 18
1003 1 76 1003 王五 M 19
```


在这个结果中，我们看到一个“奇怪”的情况，那就是出现了两个Sno属性。在等值连接中，如果连接的两个表中存在相同名称的属性（例如这里两个表中都有名为”Sno”的属性），那么在连接结果中会出现两个相同名称的属性。

这是因为等值连接会将两个表中具有相同连接条件的属性进行匹配，并将匹配成功的元组进行组合。由于两个表中都有名为”Sno”的属性，因此连接结果中会保留这两个属性，以显示连接操作前后的对应关系。

为了区分来自不同表的相同属性名，通常在连接结果中会使用表别名或表名作为前缀，以区分它们的来源。这样可以确保结果中的属性名称是唯一的，避免歧义。 例如，如果在等值连接中连接了名为”CourseSelection2022″的表和名为”Students”的表，并且两个表中都有名为”Sno”的属性，那么连接结果中可能会出现类似于”CourseSelection2022.Sno”和”Students.Sno”的属性名称，以明确它们的来源。

需要注意的是，数据库管理系统的具体实现和查询工具的设置可能会影响连接结果中属性的显示方式，但通常会采用类似的方式来区分相同属性名的来源。

#### 4.9.2 自然连接（Natural Join）

自然连接是基于两个表中具有相同属性名的属性进行连接的操作，重点在于**它会自动匹配具有相同属性名的属性，并根据这些属性的相等性进行连接，而无需手工指定**。

我们来看自然连接的Go示例：

```
// relational-algebra-examples/query/main.go
func doNaturaljoin(db *sql.DB) {
rows, _ := db.Query("SELECT * FROM CourseSelection2022 NATURAL JOIN Students")
dumpOperationResult("Naturaljoin", rows)
}
```


这个示例使用自然连接将CourseSelection2022表和Students表连接起来，自然连接会自动基于两个表中所有具有相同属性名的属性进行连接，返回的结果将包含CourseSelection2022和Students两个表中所有满足连接条件的元组，并**自动消除重复属性**，这是与等值连接的一个明显的区别。

我们看看程序运行的输出结果：

```
Naturaljoin operation:
Sno Cno Score Sname Gender Age
1001 1 85 张三 M 20
1001 2 80 张三 M 20
1002 1 83 李四 F 18
1003 1 76 王五 M 19
```


如果两个表(比如R1和R2)有一个以上的属性名相同，比如2个(比如：A1和A2)，那就会自动针对这两个属性名(一起)在两个表中进行等值连接：只有R2.A1 = R1.A1且R2.A2 = R1.A2时，才将元组连接并放入结果关系中。

#### 4.9.3 θ连接（Theta Join）

θ连接是一种通用的连接操作，它使用比等号更一般化的连接条件进行连接。连接条件可以使用除了等号之外的比较运算符（如大于、小于、不等于等）来比较两个表之间的属性。

我们来看θ连接的Go示例：

```
// relational-algebra-examples/query/main.go
func doThetajoin(db *sql.DB) {
rows, _ := db.Query(`SELECT *
FROM CourseSelection2022
JOIN Students ON CourseSelection2022.Sno > Students.Sno`)
dumpOperationResult("Thetajoin", rows)
}
```


这个示例使用Join将CourseSelection2022表和Students表连接起来，连接条件是CourseSelection2022.Sno > Students.Sno，即学生编号大于学生表中的学生编号，返回的结果将包含CourseSelection2022和`Students两个表中满足连接条件的元组。

```
Thetajoin operation:
Sno Cno Score Sno Sname Gender Age
1002 1 83 1001 张三 M 20
1003 1 76 1001 张三 M 20
1003 1 76 1002 李四 F 18
```


这个结果的生成过程大致如下：

- 先看CourseSelection2022表的第一个元组，其Sno为1001，该Sno不大于Students表中的任一个Sno；
- 再看CourseSelection2022表的第二个元组，其Sno为1002，该Sno仅大于Students表中的Sno为1001的那一个元组，于是将CourseSelection2022表的第二个元组和Students表中第一个元组连接起来作为结果表中的第一个元组；
- 最后看CourseSelection2022表的第三个元组，其Sno为1003，该Sno大于Students表中的Sno为1001和1002的元组，于是将CourseSelection2022表的第三个元组分别和Students表中第一个和第二个元组连接起来作为结果表中的第二个和第三个元组。

#### 4.9.4 半连接（Semi Join）

半连接是一种特殊的连接操作，它返回满足连接条件的左侧关系中的元组，并且只返回右侧关系中与之匹配的属性。半连接通常用于判断两个关系中是否存在匹配的元组，而不需要返回右侧关系的详细信息。

我们来看半连接的Go示例：

```
// relational-algebra-examples/query/main.go
func doSemijoin(db *sql.DB) {
rows, _ := db.Query(`SELECT *
FROM Students
WHERE EXISTS (
SELECT *
FROM CourseSelection2022
WHERE Students.Sno = CourseSelection2022.Sno
)`)
dumpOperationResult("Semijoin", rows)
}
```


这个示例使用半连接操作，以Students表为左侧关系，CourseSelection2022表为右侧关系。它使用子查询来判断左侧关系中是否存在满足连接条件的元组，即Students.Sno = CourseSelection2022.Sno。它返回的结果将只包含满足连接条件的Students表中的元组。

下面是程序输出的结果：

```
Semijoin operation:
Sno Sname Gender Age
1001 张三 M 20
1002 李四 F 18
1003 王五 M 19
```


半连接返回的结果关系中只包含左关系中的行，其中每一行只返回一次，即使在右关系中有多个匹配项。

#### 4.9.5 反连接（Anti Join）

反连接是半连接的补集操作，它返回左侧关系中不存在满足连接条件的元组。反连接通常用于查找在左侧关系中存在而在右侧关系中不存在的元组。

我们来看反连接的Go示例：

```
// relational-algebra-examples/query/main.go
func doAntijoin(db *sql.DB) {
rows, _ := db.Query(`SELECT *
FROM Students
WHERE NOT EXISTS (
SELECT *
FROM CourseSelection2022
WHERE Students.Sno = CourseSelection2022.Sno
)`)
dumpOperationResult("Antijoin", rows)
}
```


这个示例使用反连接操作，以Students表为左侧关系，CourseSelection2022表为右侧关系，并使用NOT EXISTS子查询来判断左侧关系中不存在满足连接条件的元组，即Students.Sno = CourseSelection2022.Sno。返回的结果将只包含左侧关系Students表中不存在连接条件的元组。

```
Antijoin operation:
Sno Sname Gender Age
```


我们看到输出的元组集合为空。

#### 4.9.6 左(外)连接（Left Outer Join）

左外连接是将左侧关系中的所有元组与满足连接条件的右侧关系中的元组进行连接，并返回所有左侧关系的元组。如果右侧关系中没有与左侧关系匹配的元组，对应的属性值将为NULL。

我们来看左(外)连接的Go示例：

```
// relational-algebra-examples/query/main.go
func doLeftjoin(db *sql.DB) {
rows, _ := db.Query(`SELECT *
FROM Students
LEFT JOIN CourseSelection2022 ON Students.Sno = CourseSelection2022.Sno`)
dumpOperationResult("Leftjoin", rows)
}
```


这个示例使用左外连接将Students表和CourseSelection2022表连接起来，其连接条件是Students.Sno = CourseSelection2022.Sno，即学生编号相等。示例的返回结果将**包含Students表中的所有元组**，并将满足连接条件的CourseSelection2022表中的元组加入结果中。如果没有匹配的元组，右侧关系中的属性值将为NULL。

`

下面是程序输出的结果：

```
Leftjoin operation:
Sno Sname Gender Age Sno Cno Score
1001 张三 M 20 1001 1 85
1001 张三 M 20 1001 2 80
1002 李四 F 18 1002 1 83
1003 王五 M 19 1003 1 76
```


#### 4.9.7 右(外)连接（Right Outer Join）

右外连接是将右侧关系中的所有元组与满足连接条件的左侧关系中的元组进行连接，并返回所有右侧关系的元组。如果左侧关系中没有与右侧关系匹配的元组，对应的属性值将为NULL。

我们来看右(外)连接的Go示例：

```
// relational-algebra-examples/query/main.go
func doRightjoin(db *sql.DB) {
rows, _ := db.Query(`SELECT *
FROM Students
RIGHT JOIN CourseSelection2022 ON Students.Sno = CourseSelection2022.Sno`)
dumpOperationResult("Rightjoin", rows)
}
```


这个示例使用右外连接将Students表和CourseSelection2022表连接起来，它的连接条件是Students.Sno = CourseSelection2022.Sno，即学生编号相等。返回的结果将**包含CourseSelection2022表中的所有元组**，并将满足连接条件的Students表中的元组加入结果中。如果没有匹配的元组，左侧关系中的属性值将为NULL。

下面是程序输出的结果：

```
Rightjoin operation:
Sno Sname Gender Age Sno Cno Score
1001 张三 M 20 1001 1 85
1001 张三 M 20 1001 2 80
1002 李四 F 18 1002 1 83
1003 王五 M 19 1003 1 76
```


#### 4.9.8 全连接（Full Outer Join）

全连接是将左侧关系和右侧关系中的所有元组进行连接，并返回所有满足连接条件的元组。如果左侧关系或右侧关系中没有与对方匹配的元组，对应的属性值将为NULL。

我们来看全连接的Go示例：

```
// relational-algebra-examples/query/main.go
func doFulljoin(db *sql.DB) {
rows, _ := db.Query(`SELECT *
FROM Students
FULL JOIN CourseSelection2022 ON Students.Sno = CourseSelection2022.Sno`)
dumpOperationResult("Fulljoin", rows)
}
```


这个示例使用全连接将Students表和CourseSelection2022表连接起来，连接条件是Students.Sno = CourseSelection2022.Sno，即学生编号相等。示例返回的结果将包含Students表和CourseSelection2022表中的所有元组，并将满足连接条件的元组进行组合。如果没有匹配的元组，对应关系中的属性值将为NULL。

下面是程序输出的结果：

```
Fulljoin operation:
Sno Sname Gender Age Sno Cno Score
1001 张三 M 20 1001 1 85
1001 张三 M 20 1001 2 80
1002 李四 F 18 1002 1 83
1003 王五 M 19 1003 1 76
```


以上就是本文要介绍的连接类型，这些连接类型提供了在关系数据库中操作和组合表数据的灵活性，可以根据特定的需求选择合适的连接方式来获取所需的结果。

## 5. 小结

本文系统地介绍和讲解了关系数据库中的关系代数运算，包括选择、投影、连接、交、并、积等，以及关系代数的SQL实现，并给出了Go语言示例。

关系模型是关系数据库的理论基础，关系代数通过对关系的运算来表达查询，因此关系代数也构成了SQL查询语言的理论基础。理解关系代数与SQL的对应关系，可以更好地使用SQL语言操作关系型数据库。

本文算是关系数据库的**入门文章**，既能让数据库初学者快速掌握关系代数，也能让有基础的读者回顾并深入理解概念内涵。通过阅读学习，能帮助读者把关系代数运用到实际数据库应用中，解决查询优化等问题。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/relational-algebra-examples)下载。

注：由于环境所限，本文所有示例均是在sqlite3上进行的。


## 6. 参考资料

[《Database System Concepts》](https://book.douban.com/subject/30345517/)– https://book.douban.com/subject/30345517/[《openGauss数据库核心技术》](https://book.douban.com/subject/35137626/)– https://book.douban.com/subject/35137626/[《云原生数据库：原理与实践》](https://book.douban.com/subject/35631506/)– https://book.douban.com/subject/35631506/[《数据库查询优化器的艺术》](https://book.douban.com/subject/25815707/)– https://book.douban.com/subject/25815707/[Introduction of Relational Algebra in DBMS](https://www.geeksforgeeks.org/introduction-of-relational-algebra-in-dbms/)– https://www.geeksforgeeks.org/introduction-of-relational-algebra-in-dbms/[15 SQLite3 SQL Commands Explained with Examples](https://www.thegeekstuff.com/2012/09/sqlite-command-examples/)– https://www.thegeekstuff.com/2012/09/sqlite-command-examples/

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论