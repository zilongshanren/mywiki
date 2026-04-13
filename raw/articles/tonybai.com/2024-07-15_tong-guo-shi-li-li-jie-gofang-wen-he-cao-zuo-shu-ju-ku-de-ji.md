---
title: 通过实例理解Go访问和操作数据库的几种方式
url: https://tonybai.com/2024/07/15/understand-the-ways-to-access-databases-in-go/
published: '2024-07-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解Go访问和操作数据库的几种方式

![](../../assets/c2739705795cd12e.png)


[本文永久链接](https://tonybai.com/2024/07/15/understand-the-ways-to-access-databases-in-go) – https://tonybai.com/2024/07/15/understand-the-ways-to-access-databases-in-go

关系数据库操作是Go应用开发中的重要一环，尤其是Go Web应用、微服务等。作为Gopher，我们需要了解几种主流的数据库访问和操作方法，以便在项目中做出适当的选择。

我个人在日常开发中较少涉及CRUD类应用，因此使用Go访问和操作数据库的机会并不多，在这方面也算是有一些“短板”。通过在这篇文章中对数据库访问方式进行全面的梳理，我也算是补全一下技能树，同时也能为读者小伙伴提供一些参考。

我搜集了目前Go社区的主流数据库访问和操作方式，大致有如下几种：

- 使用Go标准库database/sql+特定数据库的driver，外加像
[sqlx](https://github.com/jmoiron/sqlx)这种无缝兼容的功能增强包 - 使用对象关系映射ORM，如
[GORM](https://github.com/go-gorm/gorm)等 - 使用代码生成+ ORM方式，如
[sqlc](https://github.com/sqlc-dev/sqlc)、Fackbook开源的[Ent](https://github.com/ent/ent)等。

在这篇文章中，我会建立一个简单的关系数据库实例，并用一个简单的学校院系选课关系模型作为示例，分别用上述几种方法实现数据库访问以及CRUD操作，并对比各种方式的操作性能。通过对比，你可以了解每种方法的特点。希望这些例子能帮助各位读者在实际项目中更好地处理数据库操作。

## 1. 建立示例数据库和数据库模式(schema)

为了便于后续代码示例的讲解和实现，我们先来建立示例数据库并定义数据库模式。

### 1.1 基于容器启动MySQL数据库服务

在本文中，我们选择关系数据库界的主流代表[MySQL数据库](https://www.mysql.com/)。基于容器，我们可以很方便地启动MySQL数据库服务：

```
$docker pull mysql:latest
$docker run -d --name mysql-db -v /path/to/host/mysqldata:/var/lib/mysql -p 4407:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql:latest
```


由于做了volume挂载，MySQL容器内部的数据文件将会存储在主机的/path/to/host/mysqldata目录下，即使容器被删除或重新创建，数据文件也不会丢失。你可以根据实际情况替换/path/to/host/mysqldata为你想要存储MySQL数据的主机目录路径。

如果容器启动成功，我们可以通过容器内的mysql client工具连接到MySQL数据库中：

```
$docker exec -it mysql-db mysql -uroot -p
Enter password:
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.2.0 MySQL Community Server - GPL
Copyright (c) 2000, 2023, Oracle and/or its affiliates.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql>
```


我们在MySQL中创建example_db数据库供后面的数据库建表和数据操作使用：

```
mysql> CREATE DATABASE example_db;
Query OK, 1 row affected (0.01 sec)
mysql> SHOW DATABASES;
+--------------------+
| Database |
+--------------------+
| example_db |
| information_schema |
| mysql |
| performance_schema |
| sys |
+--------------------+
5 rows in set (0.01 sec)
```


### 1.2 建立数据库模式

接下来，我将借用并简化[《Database System Concepts,7th》](https://book.douban.com/subject/35501216/)一书中提供的示例数据库的Schema，创建本文后续代码示例使用的数据库表。简化后的Schema将涵盖常见的CRUD操作需求，同时保证数据库结构清晰易懂。下面是简化后的数据模式对应的E-R图(基于在线https://dbdiagram.io/工具生成，dbml源文件在database-access/schema.dbml)：

![](../../assets/a0feff126b6fa615.png)


这个Schema包括department(院系表)、instructor(教师表)、course(课程信息表)、student(学生信息表)和enrollment(学生选课信息)。下面是建表语句：

```
// database-access/schema.sql
DROP DATABASE IF EXISTS example_db;
CREATE DATABASE example_db;
CREATE TABLE department (
dept_id INT AUTO_INCREMENT,
name VARCHAR(50) NOT NULL,
PRIMARY KEY (dept_id)
);
CREATE TABLE instructor (
instr_id INT AUTO_INCREMENT,
name VARCHAR(50) NOT NULL,
dept_id INT,
PRIMARY KEY (instr_id),
FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);
CREATE TABLE course (
course_id INT AUTO_INCREMENT,
title VARCHAR(100) NOT NULL,
dept_id INT,
PRIMARY KEY (course_id),
FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);
CREATE TABLE student (
student_id INT AUTO_INCREMENT,
name VARCHAR(50) NOT NULL,
dept_id INT,
PRIMARY KEY (student_id),
FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);
CREATE TABLE enrollment (
student_id INT,
course_id INT,
semester VARCHAR(6),
year INT,
PRIMARY KEY (student_id, course_id, semester, year),
FOREIGN KEY (student_id) REFERENCES student(student_id),
FOREIGN KEY (course_id) REFERENCES course(course_id)
);
```


通过mysql client工具执行上述语句后，我们就完成了表的创建：

```
mysql> show tables;
+----------------------+
| Tables_in_example_db |
+----------------------+
| course |
| department |
| enrollment |
| instructor |
| student |
+----------------------+
5 rows in set (0.00 sec)
```


不过在开始使用Go语言来访问并操作这些数据表之前，我们先定义一些基本的数据库表操作的示例，后续每种Go访问和操作数据库的方式都会基于这些示例并实现这些示例中的操作。

## 2. 定义数据库表操作示例

### 2.1 插入数据（Create）

向department表中插入数据：

```
INSERT INTO department (name) VALUES ('Computer Science');
INSERT INTO department (name) VALUES ('Mathematics');
```


向instructor表中插入数据：

```
INSERT INTO instructor (name, dept_id) VALUES ('John Doe', 1);
INSERT INTO instructor (name, dept_id) VALUES ('Jane Smith', 2);
```


向course表中插入数据：

```
INSERT INTO course (title, dept_id) VALUES ('Database Systems', 1);
INSERT INTO course (title, dept_id) VALUES ('Calculus', 2);
```


向student表中插入数据：

```
INSERT INTO student (name, dept_id) VALUES ('Alice', 1);
INSERT INTO student (name, dept_id) VALUES ('Bob', 2);
```


向enrollment表中插入数据：

```
INSERT INTO enrollment (student_id, course_id, semester, year) VALUES (1, 1, 'Fall', 2024);
INSERT INTO enrollment (student_id, course_id, semester, year) VALUES (2, 2, 'Fall', 2024);
```


### 2.2 查询数据（Retrieve）

查询所有学生的信息：

```
SELECT * FROM student;
```


查询某个院系的课程信息：

```
SELECT * FROM course WHERE dept_id = 1;
```


查询某个学生的选课信息：

```
SELECT * FROM enrollment WHERE student_id = 1;
```


### 2.3 更新数据（Update）

更新某个学生的姓名：

```
UPDATE student SET name = 'Alice Johnson' WHERE student_id = 1;
```


更新某个课程的标题：

```
UPDATE course SET title = 'Advanced Database Systems' WHERE course_id = 1;
```


### 2.4 删除数据（Delete）

删除某个学生的选课记录：

```
DELETE FROM enrollment WHERE student_id = 1 AND course_id = 1 AND semester = 'Fall' AND year = 2024;
```


删除某个课程：

```
DELETE FROM course WHERE course_id = 1;
```


通过上述定义的这些示例操作，我们可以对数据库进行基本的增删改查操作。接下来，我们就来正式介绍Go访问和操作数据库的几种主流方式，并分别用这些方式来实现上述示例的CRUD操作。

我们先来看一下基于Go标准库的数据库访问和操作方式。

## 3. 采用Go标准库的数据库访问方式

Go标准库中提供了一个database/sql包，它定义了一些接口和方法，用于访问关系数据库。这个包提供了一个抽象层，可以与各种不同的关系数据库驱动程序进行交互。比如database/sql包定义了一些接口，如DB、Conn、Stmt等，用于表示数据库连接、语句执行等操作。数据库驱动包需要实现这些接口，并提供了具体的数据库交互逻辑。

Go应用使用database/sql包时，应用首先需要导入数据库驱动程序，然后使用sql.Open函数连接到数据库。这个函数返回一个*sql.DB对象，代表数据库连接。之后，Go应用便可以使用DB对象执行各种SQL操作,如DB.Query、DB.Exec等。这些函数会调用驱动程序中实现的具体方法来与数据库交互。 对于对于复杂的数据库查询操作，Go应用还可以使用DB对象创建*sql.Stmt对象，后者表示预编译好的SQL语句，这样可以提高操作性能。

总的来说，database/sql包提供了一个标准化的接口，让应用程序可以方便地访问不同的关系数据库，而不需要关心底层的实现细节。这使得Go程序可以跨数据库平台运行。

下面我们就基于[go-sql-driver/mysql](https://tonybai.com/github.com/go-sql-driver/mysql)提供的MySQL驱动来实现对MySQL中示例表的各种操作。

### 3.1 初始化数据库连接

我们首先需要在代码中初始化数据库连接。以下是初始化代码示例：

```
// database-access/stdlib/main.go
package main
import (
"database/sql"
"fmt"
_ "github.com/go-sql-driver/mysql" // 注册mysql driver
"log"
)
func main() {
dsn := "root:123456@tcp(127.0.0.1:4407)/example_db"
db, err := sql.Open("mysql", dsn)
if err != nil {
log.Fatal(err)
}
defer db.Close()
// 测试数据库连接
if err := db.Ping(); err != nil {
log.Fatal(err)
}
fmt.Println("Connected to the database successfully!")
}
```


拿到数据库实例(*sql.DB对象)后，我们便可以基于该实例对数据库表进行各种操作了！接下来，我们逐一看一下。

### 3.2 插入数据（Create）

以下是通过Go标准库database/sql包方式插入数据的代码示例：

```
func insertData(db *sql.DB) {
// 插入department数据
_, err := db.Exec("INSERT INTO department (name) VALUES ('Computer Science'), ('Mathematics')")
if err != nil {
log.Fatal(err)
}
// 插入instructor数据
_, err = db.Exec("INSERT INTO instructor (name, dept_id) VALUES ('John Doe', 1), ('Jane Smith', 2)")
if err != nil {
log.Fatal(err)
}
// 插入course数据
_, err = db.Exec("INSERT INTO course (title, dept_id) VALUES ('Database Systems', 1), ('Calculus', 2)")
if err != nil {
log.Fatal(err)
}
// 插入student数据
_, err = db.Exec("INSERT INTO student (name, dept_id) VALUES ('Alice', 1), ('Bob', 2)")
if err != nil {
log.Fatal(err)
}
// 插入enrollment数据
_, err = db.Exec("INSERT INTO enrollment (student_id, course_id, semester, year) VALUES (1, 1, 'Fall', 2024), (2, 2, 'Fall', 2024)")
if err != nil {
log.Fatal(err)
}
fmt.Println("Data inserted successfully!")
}
```


### 3.3 查询数据（Retrieve）

以下是查询数据的代码示例：

```
func queryData(db *sql.DB) {
// 查询所有学生的信息
rows, err := db.Query("SELECT * FROM student")
if err != nil {
log.Fatal(err)
}
defer rows.Close()
for rows.Next() {
var studentID int
var name string
var deptID int
err := rows.Scan(&studentID, &name, &deptID)
if err != nil {
log.Fatal(err)
}
fmt.Printf("Student ID: %d, Name: %s, Department ID: %d\n", studentID, name, deptID)
}
// 查询某个院系的课程信息
rows, err = db.Query("SELECT * FROM course WHERE dept_id = ?", 1)
if err != nil {
log.Fatal(err)
}
defer rows.Close()
for rows.Next() {
var courseID int
var title string
var deptID int
err := rows.Scan(&courseID, &title, &deptID)
if err != nil {
log.Fatal(err)
}
fmt.Printf("Course ID: %d, Title: %s, Department ID: %d\n", courseID, title, deptID)
}
// 查询某个学生的选课信息
rows, err = db.Query("SELECT * FROM enrollment WHERE student_id = ?", 1)
if err != nil {
log.Fatal(err)
}
defer rows.Close()
for rows.Next() {
var studentID int
var courseID int
var semester string
var year int
err := rows.Scan(&studentID, &courseID, &semester, &year)
if err != nil {
log.Fatal(err)
}
fmt.Printf("Student ID: %d, Course ID: %d, Semester: %s, Year: %d\n", studentID, courseID, semester, year)
}
}
```


### 3.4 更新数据（Update）

以下是更新数据的代码示例：

```
func updateData(db *sql.DB) {
// 更新某个学生的姓名
_, err := db.Exec("UPDATE student SET name = 'Alice Johnson' WHERE student_id = ?", 1)
if err != nil {
log.Fatal(err)
}
// 更新某个课程的标题
_, err = db.Exec("UPDATE course SET title = 'Advanced Database Systems' WHERE course_id = ?", 1)
if err != nil {
log.Fatal(err)
}
fmt.Println("Data updated successfully!")
}
```


### 3.5 删除数据（Delete）

以下是删除数据的代码示例：

```
func deleteData(db *sql.DB) {
// 删除某个学生的选课记录
_, err := db.Exec("DELETE FROM enrollment WHERE student_id = ? AND course_id = ? AND semester = ? AND year = ?", 1, 1, "Fall", 2024)
if err != nil {
log.Fatal(err)
}
// 删除某个课程
_, err = db.Exec("DELETE FROM course WHERE course_id = ?", 1)
if err != nil {
log.Fatal(err)
}
fmt.Println("Data deleted successfully!")
}
```


注：上述示例的完整代码可以参见database-access/stdlib/main.go。


通过上述代码示例，我们展示了如何使用Go标准库和MySQL驱动程序来进行数据库连接和基本的CRUD操作。我们看到直接使用Go标准库的database/sql包来访问和操作数据库确实是比较基础和原始的方式，基本上是手动拼接SQL语句和处理结果，这种方式确实比较低级和繁琐。

sqlx包在一定程度上提升了Go标准库访问数据库的体验，并完全兼容database/sql包的接口，接下来，我们就来看看如何使用database/sql的扩展库sqlx来访问和操作数据库。

### 3.6 使用sqlx扩展库访问MySQL数据库

[sqlx](https://github.com/jmoiron/sqlx)是一个扩展库，它在Go的标准database/sql库之上提供了一系列扩展。sqlx版本的sql.DB、sql.TX、sql.Stmt等所有接口都保留了底层接口不变，这意味着它们的接口是标准库接口的超集，这使得我们可以无缝地将现有使用database/sql的代码集成到sqlx中。sqlx的主要扩展功能包括：

- 将查询结果中的行数据直接解析到结构体(支持嵌入式结构体)、map和切片中，无需手工解析；
- 支持命名参数查询（Named queries），包括预编译语句(prepared statement)；
- 提供一些常用的辅助函数，如Get、Select方法可以快速从查询结果转换为结构体/切片。

sqlx在保持database/sql接口不变的情况下，提供了许多额外的功能和便利性，使得在Go中访问关系型数据库变得更加简单高效。下面是使用sqlx实现的上面示例操作的完整代码：

```
// database-access/sqlx/main.go
package main
import (
"fmt"
"log"
_ "github.com/go-sql-driver/mysql"
"github.com/jmoiron/sqlx"
)
func main() {
dsn := "root:123456@tcp(127.0.0.1:4407)/example_db"
db, err := sqlx.Connect("mysql", dsn)
if err != nil {
log.Fatal(err)
}
defer db.Close()
fmt.Println("Connected to the database successfully!")
insertData(db)
queryData(db)
updateData(db)
queryData(db) // 查看更新后的数据
deleteData(db)
queryData(db) // 查看删除后的数据
}
func insertData(db *sqlx.DB) {
// 插入department数据
_, err := db.NamedExec(`INSERT INTO department (name) VALUES (:name)`, []map[string]interface{}{
{"name": "Computer Science"},
{"name": "Mathematics"},
})
if err != nil {
log.Fatal(err)
}
// 插入instructor数据
_, err = db.NamedExec(`INSERT INTO instructor (name, dept_id) VALUES (:name, :dept_id)`, []map[string]interface{}{
{"name": "John Doe", "dept_id": 1},
{"name": "Jane Smith", "dept_id": 2},
})
if err != nil {
log.Fatal(err)
}
// 插入course数据
_, err = db.NamedExec(`INSERT INTO course (title, dept_id) VALUES (:title, :dept_id)`, []map[string]interface{}{
{"title": "Database Systems", "dept_id": 1},
{"title": "Calculus", "dept_id": 2},
})
if err != nil {
log.Fatal(err)
}
// 插入student数据
_, err = db.NamedExec(`INSERT INTO student (name, dept_id) VALUES (:name, :dept_id)`, []map[string]interface{}{
{"name": "Alice", "dept_id": 1},
{"name": "Bob", "dept_id": 2},
})
if err != nil {
log.Fatal(err)
}
// 插入enrollment数据
_, err = db.NamedExec(`INSERT INTO enrollment (student_id, course_id, semester, year) VALUES (:student_id, :course_id, :semester, :year)`, []map[string]interface{}{
{"student_id": 1, "course_id": 1, "semester": "Fall", "year": 2024},
{"student_id": 2, "course_id": 2, "semester": "Fall", "year": 2024},
})
if err != nil {
log.Fatal(err)
}
fmt.Println("Data inserted successfully!")
}
type Student struct {
StudentID int `db:"student_id"`
Name string `db:"name"`
DeptID int `db:"dept_id"`
}
type Course struct {
CourseID int `db:"course_id"`
Title string `db:"title"`
DeptID int `db:"dept_id"`
}
type Enrollment struct {
StudentID int `db:"student_id"`
CourseID int `db:"course_id"`
Semester string `db:"semester"`
Year int `db:"year"`
}
func queryData(db *sqlx.DB) {
// 查询所有学生的信息
var students []Student
err := db.Select(&students, "SELECT * FROM student")
if err != nil {
log.Fatal(err)
}
for _, student := range students {
fmt.Printf("Student ID: %d, Name: %s, Department ID: %d\n", student.StudentID, student.Name, student.DeptID)
}
// 查询某个院系的课程信息
var courses []Course
err = db.Select(&courses, "SELECT * FROM course WHERE dept_id = ?", 1)
if err != nil {
log.Fatal(err)
}
for _, course := range courses {
fmt.Printf("Course ID: %d, Title: %s, Department ID: %d\n", course.CourseID, course.Title, course.DeptID)
}
// 查询某个学生的选课信息
var enrollments []Enrollment
err = db.Select(&enrollments, "SELECT * FROM enrollment WHERE student_id = ?", 1)
if err != nil {
log.Fatal(err)
}
for _, enrollment := range enrollments {
fmt.Printf("Student ID: %d, Course ID: %d, Semester: %s, Year: %d\n", enrollment.StudentID, enrollment.CourseID, enrollment.Semester, enrollment.Year)
}
}
func updateData(db *sqlx.DB) {
// 更新某个学生的姓名
_, err := db.NamedExec("UPDATE student SET name = :name WHERE student_id = :student_id", map[string]interface{}{
"name": "Alice Johnson",
"student_id": 1,
})
if err != nil {
log.Fatal(err)
}
// 更新某个课程的标题
_, err = db.NamedExec("UPDATE course SET title = :title WHERE course_id = :course_id", map[string]interface{}{
"title": "Advanced Database Systems",
"course_id": 1,
})
if err != nil {
log.Fatal(err)
}
fmt.Println("Data updated successfully!")
}
func deleteData(db *sqlx.DB) {
// 删除某个学生的选课记录
_, err := db.NamedExec("DELETE FROM enrollment WHERE student_id = :student_id AND course_id = :course_id AND semester = :semester AND year = :year", map[string]interface{}{
"student_id": 1,
"course_id": 1,
"semester": "Fall",
"year": 2024,
})
if err != nil {
log.Fatal(err)
}
// 删除某个课程
_, err = db.NamedExec("DELETE FROM course WHERE course_id = :course_id", map[string]interface{}{
"course_id": 1,
})
if err != nil {
log.Fatal(err)
}
fmt.Println("Data deleted successfully!")
}
```


我们看到：相较于直接使用database/sql，sqlx的named query/exec和直接将结果写入结构体/map/slices的确非常方便！ 代码也显得更加简洁、易读。

不过要说方便和易读，对象关系映射(ORM)方式说自己第二，没人敢说是第一。下面我们就来看看在Go中访问和操作数据库最常使用的方式：ORM方式。

## 4. 使用ORM库访问数据库

ORM（Object-Relational Mapping）是一种通过对象方式来操作数据库的方法，它将数据库中的表映射为程序中的对象，使开发者可以使用面向对象的方式操作数据库。使用ORM库可以简化数据库操作，提高开发效率，同时也能减少手写SQL带来的错误风险。

Go社区有几个很受欢迎的ORM库，比如gorm、[xorm](https://gitea.com/xorm/xorm)等。接下来我将以最常用的Go ORM库GORM来说明一下如何使用ORM访问和操作数据库。

GORM是一个功能强大的Go ORM库，它提供了丰富的特性，如自动迁移(migrate)、关联、钩子、事务、复合主键等。GORM支持多种数据库，包括MySQL、PostgreSQL、SQLite等。

和采用原生database/sql的方式不同，使用ORM方式访问数据库，我们首先先要定义表对应的对象，即创建对象模型。

### 4.1 创建对象模型

下面的各个结构体类型对应的就是示例中各个表，gorm通过struct field tag来将结构体字段与表的列字段对应在一起：

```
// database-access/gorm/main.go
type Department struct {
ID uint `gorm:"primaryKey"`
Name string `gorm:"size:100;not null"`
}
type Instructor struct {
ID uint `gorm:"primaryKey"`
Name string `gorm:"size:100;not null"`
DeptID uint
Dept Department `gorm:"foreignKey:DeptID"`
}
type Course struct {
ID uint `gorm:"primaryKey"`
Title string `gorm:"size:100;not null"`
DeptID uint
Dept Department `gorm:"foreignKey:DeptID"`
}
type Student struct {
ID uint `gorm:"primaryKey"`
Name string `gorm:"size:100;not null"`
DeptID uint
Dept Department `gorm:"foreignKey:DeptID"`
}
type Enrollment struct {
ID uint `gorm:"primaryKey"`
StudentID uint
CourseID uint
Semester string `gorm:"size:50;not null"`
Year int `gorm:"not null"`
Student Student `gorm:"foreignKey:StudentID"`
Course Course `gorm:"foreignKey:CourseID"`
CreatedAt time.Time
UpdatedAt time.Time
}
```


### 4.2 CRUD操作示例

下面就是基于上面定义的ORM模型进行CRUD操作的示例代码：

```
// database-access/gorm/main.go
func main() {
dsn := "root:123456@tcp(127.0.0.1:4407)/example_db?charset=utf8mb4&parseTime=True&loc=Local"
db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
NamingStrategy: schema.NamingStrategy{
SingularTable: true,
},
})
if err != nil {
log.Fatal(err)
}
// 自动迁移模式
db.AutoMigrate(&Department{}, &Instructor{}, &Course{}, &Student{}, &Enrollment{})
// 执行CRUD操作
createData(db)
queryData(db)
updateData(db)
deleteData(db)
}
func createData(db *gorm.DB) {
// 创建院系
cs := Department{Name: "Computer Science"}
math := Department{Name: "Mathematics"}
db.Create(&cs)
db.Create(&math)
// 创建教师
db.Create(&Instructor{Name: "John Doe", DeptID: cs.ID})
db.Create(&Instructor{Name: "Jane Smith", DeptID: math.ID})
// 创建课程
db.Create(&Course{Title: "Database Systems", DeptID: cs.ID})
db.Create(&Course{Title: "Calculus", DeptID: math.ID})
// 创建学生
db.Create(&Student{Name: "Alice", DeptID: cs.ID})
db.Create(&Student{Name: "Bob", DeptID: math.ID})
// 学生选课
db.Create(&Enrollment{StudentID: 1, CourseID: 1, Semester: "Fall", Year: 2024})
db.Create(&Enrollment{StudentID: 2, CourseID: 2, Semester: "Fall", Year: 2024})
}
func queryData(db *gorm.DB) {
// 查询所有学生
var students []Student
db.Find(&students)
for _, student := range students {
log.Printf("Student ID: %d, Name: %s, Department ID: %d\n", student.ID, student.Name, student.DeptID)
}
// 查询某个院系的课程
var courses []Course
db.Where("dept_id = ?", 1).Find(&courses)
for _, course := range courses {
log.Printf("Course ID: %d, Title: %s, Department ID: %d\n", course.ID, course.Title, course.DeptID)
}
// 查询某个学生的选课信息
var enrollments []Enrollment
db.Where("student_id = ?", 1).Find(&enrollments)
for _, enrollment := range enrollments {
log.Printf("Student ID: %d, Course ID: %d, Semester: %s, Year: %d\n", enrollment.StudentID, enrollment.CourseID, enrollment.Semester, enrollment.Year)
}
}
func updateData(db *gorm.DB) {
// 更新学生姓名
db.Model(&Student{}).Where("id = ?", 1).Update("name", "Alice Johnson")
// 更新课程标题
db.Model(&Course{}).Where("id = ?", 1).Update("title", "Advanced Database Systems")
}
func deleteData(db *gorm.DB) {
// 删除选课记录
db.Where("course_id = ?", 1).Delete(&Enrollment{})
// 删除课程
db.Where("id = ?", 1).Delete(&Course{})
}
```


我们看到GORM提供了大量的便捷方法，可以大幅度简化SQL操作。例如，插入记录只需调用Create方法，而不需要手写SQL语句。GORM还提供了多种钩子函数（如BeforeCreate, AfterCreate, BeforeUpdate, AfterUpdate等），可以在特定操作前后执行自定义逻辑。这对于实现复杂业务逻辑非常有帮助。示例里没有使用钩子函数，大家可以自行试验。

日常使用数据库，查询操作占比最大，GORM的查询构造器允许开发人员使用链式方法调用来构造复杂的查询条件，例如，我们可以使用Where, Or, Order, Limit, Offset等方法来构建查询。

GORM还提供了AutoMigrate方法，可以根据模型结构自动创建或更新数据库表，这在开发环境中十分实用，减少了手动管理数据库结构的复杂性。

此外，GORM支持一对一、一对多和多对多等多种关联关系，并且可以通过简单的模型定义和方法调用来操作这些关系。就像例子中那样，我们可以通过定义foreignKey来自动管理外键约束。

总之，ORM方式的数据库访问和操作大幅降低了开发人员使用数据库的复杂性，提高了生产效率。不过由于引入了一层新的抽象，在表数据量较大的情况下，ORM方式的性能相对于原生SQL要低一些，这个我们在后面的对比各种方式的性能一节会再说。

Go开发人员在使用数据库时，往往希望能够在以下几个方面达到平衡：

- 性能

Go标准库的database/sql包提供了直接操作SQL语句的方式，可以发挥底层数据库引擎的性能优势。相比之下，ORM库在一定程度上会增加性能开销。

- 开发体验

ORM 库能够提供更高级的抽象和自动化，简化了许多数据库操作的样板代码，使得开发体验更加友好，生产力也相对较高。

- 类型安全

ORM库通常能够提供更好的类型安全性，减少手动拼接SQL语句时出错的风险。

简单来说，就是我们希望“既要..，也要…，还要…”，于是便有了以代码生成方式访问和操作数据库的代表sqlc。接下来我们就来看看如何sqlc是如何用代码生成方式来访问和操作数据库的。

## 5. 使用代码生成方式访问数据库

sqlc是一个强大的工具，它可以将针对数据库的操作，比如SQL查询等，直接生成类型安全的Go代码。它不仅保留了SQL的灵活性和可读性，同时也提供了编译时的类型检查，可以避免手写SQL代码中的错误。

### 5.1 安装sqlc

和上面的两种方式不同，使用sqlc，我们需要首先安装sqlc [cmdline工具](https://tonybai.com/2023/03/25/the-guide-of-developing-cli-program-in-go)，这个工具用来基于sqlc定义的一套SQL [dsl语法](https://tonybai.com/2022/05/24/an-example-of-implement-dsl-using-antlr-and-go-part1)生成相应的Go代码。

通过下面命令可以实现sqlc工具的安装：

```
$go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest
```


安装后，输入下面命令验证一下sqlc的安装结果，如果输出下面内容，则说明安装ok了：

```
$sqlc -h
Usage:
sqlc [command]
Available Commands:
compile Statically check SQL for syntax and type errors
completion Generate the autocompletion script for the specified shell
createdb Create an ephemeral database
diff Compare the generated files to the existing files
generate Generate source code from SQL
help Help about any command
init Create an empty sqlc.yaml settings file
push Push the schema, queries, and configuration for this project
verify Verify schema, queries, and configuration for this project
version Print the sqlc version number
vet Vet examines queries
Flags:
-f, --file string specify an alternate config file (default: sqlc.yaml)
-h, --help help for sqlc
--no-remote disable remote execution (default: false)
--remote enable remote execution (default: false)
Use "sqlc [command] --help" for more information about a command.
```


### 5.2 初始化和配置sqlc项目

下面是sqlc的代码生成上的输入与输出示意图：

![](../../assets/f9e454d107cfa510.png)


我们看到要生成Go代码，我们需要提供三个输入文件，其中sqlc.yaml是sqlc项目的主配置文件，它是个[yaml格式文件](https://tonybai.com/2019/02/25/introduction-to-yaml-creating-a-kubernetes-deployment/)，在我们这个示例中，它的内容如下：

```
// database-access/sqlc/sqlc.yaml
version: "2"
sql:
- name: "db"
engine: "mysql"
queries: "queries.sql"
schema: "schema.sql"
gen:
go:
package: "db"
out: "db"
```


这个文件可以使用sqlc init生成一个模板，然后再向其中填写具体内容。上述sqlc.yaml的内容不难理解，其中engine表示生成的代码将用于与MySQL交互，schema是数据库模式文件，queries.sql中定义了与数据库的所有交互语句，而在gen段中，package是输出的代码的包名，而out则是输出到哪个目录下。

接下来，我们再来看看schema.sql和queries.sql。

### 5.3 创建数据库模式和查询文件

schema.sql文件的内容与我们

```
-- schema.sql
CREATE TABLE department (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL
);
CREATE TABLE instructor (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
dept_id INT,
FOREIGN KEY (dept_id) REFERENCES department(id)
);
CREATE TABLE course (
id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(100) NOT NULL,
dept_id INT,
FOREIGN KEY (dept_id) REFERENCES department(id)
);
CREATE TABLE student (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
dept_id INT,
FOREIGN KEY (dept_id) REFERENCES department(id)
);
CREATE TABLE enrollment (
student_id INT,
course_id INT,
semester VARCHAR(50) NOT NULL,
year INT NOT NULL,
PRIMARY KEY (student_id, course_id, semester, year),
FOREIGN KEY (student_id) REFERENCES student(id),
FOREIGN KEY (course_id) REFERENCES course(id)
);
```


没错，这就是一些建表语句，后续sqlc执行生成命令时会参考这些表以及约束。queries.sql则是我们要使用的数据库dml语句：

```
-- name: CreateDepartment :execresult
INSERT INTO department (
name
) VALUES (
?
);
-- name: GetDepartments :many
SELECT id, name FROM department;
-- name: CreateInstructor :execresult
INSERT INTO instructor (
name, dept_id
) VALUES (
?, ?
);
-- name: GetInstructors :many
SELECT id, name, dept_id FROM instructor;
-- name: CreateCourse :execresult
INSERT INTO course (
title, dept_id
) VALUES (
?, ?
);
-- name: GetCoursesByDept :many
SELECT id, title, dept_id FROM course WHERE dept_id = ?;
-- name: CreateStudent :execresult
INSERT INTO student (
name, dept_id
) VALUES (
?, ?
);
-- name: GetStudents :many
SELECT id, name, dept_id FROM student;
-- name: EnrollStudent :execresult
INSERT INTO enrollment (
student_id, course_id, semester, year
) VALUES (
?, ?, ?, ?
);
-- name: GetEnrollmentByStudent :many
SELECT student_id, course_id, semester, year FROM enrollment WHERE student_id = ?;
-- name: UpdateStudentName :exec
UPDATE student SET name = ?
WHERE id = ?;
-- name: UpdateCourseTitle :exec
UPDATE course SET title = ?
WHERE id = ?;
-- name: DeleteStudent :exec
DELETE FROM student
WHERE id = ?;
-- name: DeleteCourse :exec
DELETE FROM course
WHERE id = ?;
-- name: DeleteEnrollmentByCourseID :exec
DELETE FROM enrollment
WHERE course_id = ?;
```


务必注意：针对不同的数据库，queries.sql中使用的语法**有所不同**，关于queries.sql的DSL语法形式的详细内容，可参考[sqlc docs](https://docs.sqlc.dev/en/latest/index.html)。

### 5.4 生成代码

在项目sqlc根目录下运行下面sqlc命令可以在指定的db目录下生成包名为db的Go代码：

```
$sqlc generate
$tree db
db
├── db.go
├── models.go
└── queries.sql.go
```


其中queries.sql.go是对应queries.sql中所有dml操作的方法。下面摘录queries.sql.go的代码片段：

```
// Code generated by sqlc. DO NOT EDIT.
// versions:
// sqlc v1.26.0
// source: queries.sql
package db
import (
"context"
"database/sql"
)
const createCourse = `-- name: CreateCourse :execresult
INSERT INTO course (
title, dept_id
) VALUES (
?, ?
)
`
type CreateCourseParams struct {
Title string
DeptID sql.NullInt32
}
func (q *Queries) CreateCourse(ctx context.Context, arg CreateCourseParams) (sql.Result, error) {
return q.db.ExecContext(ctx, createCourse, arg.Title, arg.DeptID)
}
const createDepartment = `-- name: CreateDepartment :execresult
INSERT INTO department (
name
) VALUES (
?
)
`
func (q *Queries) CreateDepartment(ctx context.Context, name string) (sql.Result, error) {
return q.db.ExecContext(ctx, createDepartment, name)
}
... ...
```


我们看到，queries.sql中的操作都以Queries类型的方法形式存在，在后面的使用过程中，我们可以体会这种方式带来的编码时的便利。

### 5.5 使用生成的代码访问和操作数据库

下面是使用生成的Go代码进行数据库操作的示例，我们需要先初始化数据库连接并创建Queries实例，然后基于创建的Queries实例的方法进行数据库表操作：

```
// database-access/sqlc/main.go
package main
import (
"context"
"database/sql"
"fmt"
"log"
"demo/db"
_ "github.com/go-sql-driver/mysql"
)
func main() {
dsn := "root:123456@tcp(127.0.0.1:4407)/example_db"
conn, err := sql.Open("mysql", dsn)
if err != nil {
log.Fatal(err)
}
defer conn.Close()
queries := db.New(conn)
// 执行CRUD操作
createData(queries)
queryData(queries)
updateData(queries)
deleteData(queries)
}
func createData(queries *db.Queries) {
ctx := context.Background()
// 创建部门
_, err := queries.CreateDepartment(ctx, "Computer Science")
if err != nil {
log.Fatal(err)
}
_, err = queries.CreateDepartment(ctx, "Mathematics")
if err != nil {
log.Fatal(err)
}
// 创建教师
_, err = queries.CreateInstructor(ctx, db.CreateInstructorParams{Name: "John Doe", DeptID: sql.NullInt32{1, true}})
if err != nil {
log.Fatal(err)
}
_, err = queries.CreateInstructor(ctx, db.CreateInstructorParams{Name: "Jane Smith", DeptID: sql.NullInt32{2, true}})
if err != nil {
log.Fatal(err)
}
// 创建课程
_, err = queries.CreateCourse(ctx, db.CreateCourseParams{Title: "Database Systems", DeptID: sql.NullInt32{1, true}})
if err != nil {
log.Fatal(err)
}
_, err = queries.CreateCourse(ctx, db.CreateCourseParams{Title: "Calculus", DeptID: sql.NullInt32{2, true}})
if err != nil {
log.Fatal(err)
}
// 创建学生
_, err = queries.CreateStudent(ctx, db.CreateStudentParams{Name: "Alice", DeptID: sql.NullInt32{1, true}})
if err != nil {
log.Fatal(err)
}
_, err = queries.CreateStudent(ctx, db.CreateStudentParams{Name: "Bob", DeptID: sql.NullInt32{2, true}})
if err != nil {
log.Fatal(err)
}
// 学生选课
_, err = queries.EnrollStudent(ctx, db.EnrollStudentParams{StudentID: sql.NullInt32{1, true}, CourseID: sql.NullInt32{1, true}, Semester: "Fall", Year: 2024})
if err != nil {
log.Fatal(err)
}
_, err = queries.EnrollStudent(ctx, db.EnrollStudentParams{StudentID: sql.NullInt32{2, true}, CourseID: sql.NullInt32{2, true}, Semester: "Fall", Year: 2024})
if err != nil {
log.Fatal(err)
}
}
func queryData(queries *db.Queries) {
ctx := context.Background()
// 查询所有学生
students, err := queries.GetStudents(ctx)
if err != nil {
log.Fatal(err)
}
for _, student := range students {
fmt.Printf("Student ID: %d, Name: %s, Department ID: %d\n", student.ID, student.Name, student.DeptID.Int32)
}
// 查询某个部门的课程
courses, err := queries.GetCoursesByDept(ctx, sql.NullInt32{1, true})
if err != nil {
log.Fatal(err)
}
for _, course := range courses {
fmt.Printf("Course ID: %d, Title: %s, Department ID: %d\n", course.ID, course.Title, course.DeptID.Int32)
}
// 查询某个学生的选课信息
enrollments, err := queries.GetEnrollmentByStudent(ctx, sql.NullInt32{1, true})
if err != nil {
log.Fatal(err)
}
for _, enrollment := range enrollments {
fmt.Printf("Student ID: %d, Course ID: %d, Semester: %s, Year: %d\n", enrollment.StudentID.Int32, enrollment.CourseID.Int32, enrollment.Semester, enrollment.Year)
}
}
func updateData(queries *db.Queries) {
ctx := context.Background()
// 更新学生姓名
err := queries.UpdateStudentName(ctx, db.UpdateStudentNameParams{ID: 1, Name: "Alice Johnson"})
if err != nil {
log.Fatal(err)
}
// 更新课程标题
err = queries.UpdateCourseTitle(ctx, db.UpdateCourseTitleParams{ID: 1, Title: "Advanced Database Systems"})
if err != nil {
log.Fatal(err)
}
}
func deleteData(queries *db.Queries) {
ctx := context.Background()
// 删除选课记录
err := queries.DeleteEnrollmentByCourseID(ctx, sql.NullInt32{1, true})
if err != nil {
log.Fatal(err)
}
// 删除课程
err = queries.DeleteCourse(ctx, 1)
if err != nil {
log.Fatal(err)
}
// 删除学生
err = queries.DeleteStudent(ctx, 1)
if err != nil {
log.Fatal(err)
}
}
```


通过上述示例，我们可以看到sqlc在生成类型安全的Go代码方面非常高效，它结合了SQL查询的灵活性和Go语言的类型安全特性，使得数据库操作更加直观和可靠。不过，学习sqlc的DSL还是需要一点时间的，也有一个小小的门槛。

除了sqlc，Facebook开源的entgo是一个同时基于代码生成以及ORM进行数据库操作的方式。和sqlc一样，entgo在前期需要一定的额外学习成本。下面我们来看看使用entgo如何访问和操作数据库。

### 5.6. 使用entgo操作数据库

Ent是Facebook开源的一个实体框架，它使用Schema作为强类型的Go代码生成数据模型和查询方法。Ent提供了类型安全的API、自动化的迁移、GraphQL支持等特性。

#### 5.6.1 安装Ent

和sqlc一样，由于需要代码生成，我们需要先安装ent的命令行工具：

```
$go install entgo.io/ent/cmd/ent@latest
```


使用下面命令可以验证ent安装是否ok：

```
$ent -h
Usage:
ent [command]
Available Commands:
completion Generate the autocompletion script for the specified shell
describe print a description of the graph schema
generate generate go code for the schema directory
help Help about any command
new initialize a new environment with zero or more schemas
Flags:
-h, --help help for ent
Use "ent [command] --help" for more information about a command.
```


接下来，和sqlc一样，我们需要使用ent的DSL来定义schema，和sqlc不同，ent使用Go语法来定义schema。

#### 5.6.2 定义Schema

使用Ent需要先定义Schema，我们建立一个schema目录，将所有schema相关的Go定义文件都放入目录中：

```
$tree schema
schema
├── course.go
├── department.go
├── enrollment.go
├── instructor.go
└── student.go
```


schema目录下的每个文件都是一个entity的定义，以department.go为例：

```
// database-access/ent/schema/department.go
package schema
import (
"entgo.io/ent"
"entgo.io/ent/schema/edge"
"entgo.io/ent/schema/field"
)
// Department holds the schema definition for the Department entity.
type Department struct {
ent.Schema
}
// Fields of the Department.
func (Department) Fields() []ent.Field {
return []ent.Field{
field.String("name").NotEmpty(),
}
}
// Edges of the Department.
func (Department) Edges() []ent.Edge {
return []ent.Edge{
edge.To("instructors", Instructor.Type),
edge.To("courses", Course.Type),
edge.To("students", Student.Type),
}
}
```


我们看到结构体类型Department对应表department，department与其他表之间的关系使用ent.Edge表示，这样就建立了与其他表的关系。有了Schema定义后，我们就可以来生成代码了。

#### 5.6.3 生成代码

我们在database-access/ent目录下执行下面命令：

```
$ent generate demo/schema --target ent
```


ent会基于demo/schema包生成相应代码(这里go module为demo)，即在ent目录下生成包名为ent的代码：

```
$tree -L 1 -F ./ent
./ent
├── client.go
├── course/
├── course.go
├── course_create.go
├── course_delete.go
├── course_query.go
├── course_update.go
├── department/
├── department.go
├── department_create.go
├── department_delete.go
├── department_query.go
├── department_update.go
├── enrollment/
├── enrollment.go
├── enrollment_create.go
├── enrollment_delete.go
├── enrollment_query.go
├── enrollment_update.go
├── ent.go
├── enttest/
├── hook/
├── instructor/
├── instructor.go
├── instructor_create.go
├── instructor_delete.go
├── instructor_query.go
├── instructor_update.go
├── migrate/
├── mutation.go
├── predicate/
├── runtime/
├── runtime.go
├── student/
├── student.go
├── student_create.go
├── student_delete.go
├── student_query.go
├── student_update.go
└── tx.go
```


我们看到，ent为每个entity，比如department都生成了一组文件，包括增删改查。接下来，我们就来使用ent生成的代码来操作数据库！

#### 5.6.4 使用生成的代码操作数据库

下面是使用ent生成的代码操作数据库的示例代码：

```
// database-access/ent/main.go
package main
import (
"context"
"log"
"demo/ent"
"demo/ent/course"
"demo/ent/department"
"demo/ent/enrollment"
"demo/ent/student"
_ "github.com/go-sql-driver/mysql"
)
func main() {
client, err := ent.Open("mysql", "root:123456@tcp(127.0.0.1:4407)/example_db?parseTime=True")
if err != nil {
log.Fatalf("failed opening connection to mysql: %v", err)
}
defer client.Close()
ctx := context.Background()
// Run the automatic migration tool to create all schema resources.
if err := client.Schema.Create(ctx); err != nil {
log.Fatalf("failed creating schema resources: %v", err)
}
// 执行CRUD操作
createData(ctx, client)
queryData(ctx, client)
updateData(ctx, client)
deleteData(ctx, client)
}
func createData(ctx context.Context, client *ent.Client) {
// 创建部门
cs, err := client.Department.Create().SetName("Computer Science").Save(ctx)
if err != nil {
log.Fatal(err)
}
math, err := client.Department.Create().SetName("Mathematics").Save(ctx)
if err != nil {
log.Fatal(err)
}
// 创建教师
_, err = client.Instructor.Create().SetName("John Doe").SetDepartment(cs).Save(ctx)
if err != nil {
log.Fatal(err)
}
_, err = client.Instructor.Create().SetName("Jane Smith").SetDepartment(math).Save(ctx)
if err != nil {
log.Fatal(err)
}
// 创建课程
dbCourse, err := client.Course.Create().SetTitle("Database Systems").SetDepartment(cs).Save(ctx)
if err != nil {
log.Fatal(err)
}
calcCourse, err := client.Course.Create().SetTitle("Calculus").SetDepartment(math).Save(ctx)
if err != nil {
log.Fatal(err)
}
// 创建学生
alice, err := client.Student.Create().SetName("Alice").SetDepartment(cs).Save(ctx)
if err != nil {
log.Fatal(err)
}
bob, err := client.Student.Create().SetName("Bob").SetDepartment(math).Save(ctx)
if err != nil {
log.Fatal(err)
}
// 学生选课
_, err = client.Enrollment.Create().SetStudent(alice).SetCourse(dbCourse).SetSemester("Fall").SetYear(2024).Save(ctx)
if err != nil {
log.Fatal(err)
}
_, err = client.Enrollment.Create().SetStudent(bob).SetCourse(calcCourse).SetSemester("Fall").SetYear(2024).Save(ctx)
if err != nil {
log.Fatal(err)
}
}
func queryData(ctx context.Context, client *ent.Client) {
// 查询所有学生
//students, err := client.Student.Query().All(ctx)
students, err := client.Student.Query().WithDepartment().All(ctx)
if err != nil {
log.Fatal(err)
}
for _, stu := range students {
log.Printf("Student ID: %d, Name: %s, Department ID: %d\n", stu.ID, stu.Name, stu.Edges.Department.ID)
}
// 查询某个部门的课程
courses, err := client.Course.Query().WithDepartment().Where(course.HasDepartmentWith(department.ID(1))).All(ctx)
if err != nil {
log.Fatal(err)
}
for _, course := range courses {
log.Printf("Course ID: %d, Title: %s, Department ID: %d\n", course.ID, course.Title, course.Edges.Department.ID)
}
// 查询某个学生的选课信息
enrollments, err := client.Enrollment.Query().WithStudent().WithCourse().Where(enrollment.HasStudentWith(student.ID(1))).All(ctx)
if err != nil {
log.Fatal(err)
}
for _, enrollment := range enrollments {
log.Printf("Student ID: %d, Course ID: %d, Semester: %s, Year: %d\n", enrollment.Edges.Student.ID,
enrollment.Edges.Course.ID, enrollment.Semester, enrollment.Year)
}
}
func updateData(ctx context.Context, client *ent.Client) {
// 更新学生姓名
_, err := client.Student.UpdateOneID(1).SetName("Alice Johnson").Save(ctx)
if err != nil {
log.Fatal(err)
}
// 更新课程标题
_, err = client.Course.UpdateOneID(1).SetTitle("Advanced Database Systems").Save(ctx)
if err != nil {
log.Fatal(err)
}
}
func deleteData(ctx context.Context, client *ent.Client) {
// 删除选课记录
_, err := client.Enrollment.Delete().Where(enrollment.HasCourseWith(course.ID(1))).Exec(ctx)
if err != nil {
log.Fatal(err)
}
// 删除课程
err = client.Course.DeleteOneID(1).Exec(ctx)
if err != nil {
log.Fatal(err)
}
// 删除学生
err = client.Student.DeleteOneID(1).Exec(ctx)
if err != nil {
log.Fatal(err)
}
}
```


通过以上示例可以看到，使用GORM和Ent都可以大大简化数据库操作，并提供了类型安全的API和自动化的迁移支持，使得开发更加高效和可靠。

到这里我们已经见识到了三类数据库访问和操作的方式，那么究竟那种适合我们呢？我们接下来做一个简单的对比。

## 6. 不同数据库访问方式的对比

在前面的小节中，我们介绍了三种主要的数据库访问方式：Go标准库、ORM库（GORM），以及代码生成工具（sqlc和ent）。在本节中，我们将基于前面示例中的表现，对这些方式进行一个简单的对比，以帮助开发者在实际项目中做出最佳选择。

以下是整理的关于Go不同数据库访问方式优缺点的表格：

![](../../assets/a539290e6d1d40a0.png)


这张表格总结了不同数据库访问方式的优缺点，帮助读者选择最适合其项目需求的方式。

关于各种数据库访问方式的性能对比，做起来还是稍麻烦的，之前goland博客曾发表过一篇[有关go标准库 vs. gorm vs. sqlx. vs. sqlc的压测的文章](https://blog.jetbrains.com/zh-hans/go/2023/06/30/database-sql-gorm-sqlx-sqlc/)，大家可以参考其中的结论，即Go标准库、sqlc由于是原生sql操作，所以性能最佳；sqlx略有扩展，性能次之；gorm在小数据量的情况下，性能是很快的，但性能会随着数据量的增加而下降很多。

综合，以上对比与性能情况，这里也给出一些选择建议：

- 如果性能是首要考虑，且不介意手写SQL查询，推荐使用Go标准库 (database/sql)。
- 如果需要更多的功能和一些简化的开发体验，可以选择sqlx。
- 如果需要高级的ORM特性和简化开发过程，GORM和Ent都是不错的选择，但需要注意性能开销。
- 如果希望在保持性能的同时获得类型安全和编译时检查，sqlc是一个非常好的选择。

## 7. 小结

本文详细介绍了在Go语言中访问和操作数据库的几种主流方式。

我们首先搭建了一个基于MySQL数据库的示例环境，并定义了一个简单的学校院系选课关系模型作为数据库模式。然后，我们分别使用以下三种方法实现了对该数据库的CRUD操作：

-
使用Go标准库database/sql加上特定数据库的driver，并配合像sqlx这样的功能增强包。这种方式灵活性高，可完全控制SQL语句，但需要编写较多样板代码。

-
使用ORM工具GORM，这种方式可以将数据库操作抽象为对象关系映射，降低开发难度，但功能可能无法完全满足需求，性能也会在数据量增大的情况下有较大下降。

-
使用代码生成 + ORM 的方式，如sqlc和Ent。这种方式将SQL语句编译为Go代码或直接用Go代码表述schema，既可以获得类似ORM的便利，又可以自定义SQL语句。不过这种方式有相对高一些的学习门槛，比如要熟练掌握sqlc的DSL语法才能写出满足要求的数据库操作语句。


最后，我们还简单对比了这三种方法的优劣，希望可以帮助大家选择出适合自身项目的数据库访问方式。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/blob/master/database-access)下载 – https://github.com/bigwhite/experiments/blob/master/database-access

本文中的部分源码由OpenAI的GPT-4o生成。

## 8. 参考资料

- 比较database/sql、GORM、sqlx 和 sqlc – https://blog.jetbrains.com/zh-hans/go/2023/06/30/database-sql-gorm-sqlx-sqlc/
- https://github.com/rexfordnyrk/go-db-comparison/
- https://www.reddit.com/r/golang/comments/130kxaw/comparing_databasesql_gorm_sqlx_and_sqlc/
- sqlc介绍 – https://conroy.org/introducing-sqlc

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

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论