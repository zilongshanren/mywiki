---
title: 'Implementing a todo app, Part 1: The Backend'
url: https://www.4rknova.com/blog/2025/01/22/todo-app-backend
author: Nikolaos Papadopoulos
published: '2025-01-22'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Introduction

Full Stack Development refers to the process of designing, developing, and maintaining both the front-end (client-side) and back-end (server-side) of a web application. A full stack developer has expertise in working with multiple layers of web development, from user interfaces to databases and server-side logic using a wide range of languages and programming paradigms.

In this blog series, I will go over the development of a simple to-do application. Some familiarity with the technologies used is required in order to understand the code, therefore, I will provide references for further reading where applicable.

This first installment focuses on building the backend. The next chapter will cover the development of an Android app frontend.

The full code base is available in [this Github repository](https://github.com/4rknova/learning.full_stack/).

The server side architecture is simple. An API service implements a GraphQL interface for performing all supported data queries needed by the frontend. The actual data is stored in an SQL database running as a separate service.

# The API Service

The API service handles all data requests from the frontend(s) and is implemented in Go. I will use GraphQL to communicate with the database and perform data queries. Below is the code for the entry point of the service.

```
package main
import (
"github.com/99designs/gqlgen/graphql/handler"
"github.com/go-chi/chi/v5"
"github.com/go-chi/httplog/v2"
"log"
"log/slog"
"net/http"
"server/graph"
"server/internal/pkg/db/mysql"
"time"
)
const defaultPort = "4000"
func main() {
logger := httplog.NewLogger("logger", httplog.Options{
LogLevel: slog.LevelDebug,
Concise: true,
RequestHeaders: true,
MessageFieldName: "message",
TimeFieldFormat: time.RFC850,
Tags: map[string]string{
"version": "v1.0-81aa4244d9fc8076a",
"env": "dev",
},
})
port := defaultPort
router := chi.NewRouter()
router.Use(httplog.RequestLogger(logger))
database.InitDB()
defer func() {
err := database.CloseDB()
if err != nil {
log.Fatal("Error: ", err)
}
}()
database.Migrate()
log.Print("Starting server at port ", port)
server := handler.NewDefaultServer(
graph.NewExecutableSchema(graph.Config{Resolvers: &graph.Resolver{}})
)
router.Handle("/api", server)
log.Fatal(http.ListenAndServe(":"+port, router))
}
```


I also implement some needed database utilities that are used by the API service. Note the for loop in the *InitDB* function below which, serves as a crude way of dealing with connection issues during initialization. More specifically, it handles the scenario where our API service is initialized before the database service is ready to receive connections. The code will keep retrying to reach the database server at fixed intervals until a connection is established. The issue will become more apparent when we containerize the service.

You may also notice that I use a hostname instead of IP address for the database server. That hostname is defined when we create the database service container later on.

```
package database
import (
"database/sql"
"errors"
_ "github.com/go-sql-driver/mysql"
"github.com/golang-migrate/migrate"
"github.com/golang-migrate/migrate/database/mysql"
_ "github.com/golang-migrate/migrate/source/file"
"log"
"time"
)
var Db *sql.DB
func InitDB() {
log.Print("Initiating database connection..")
for {
var db, err = sql.Open("mysql",
"root:pass@tcp(todo_db:3306)/todo?parseTime=true"
)
if err != nil {
log.Print(err)
time.Sleep(5 * time.Second)
continue
}
if err = db.Ping(); err != nil {
log.Print(err)
continue
} else {
Db = db
break
}
}
}
func CloseDB() error {
log.Print("Closing database connection..")
return Db.Close()
}
func Migrate() {
log.Print("Performing database migration..")
if err := Db.Ping(); err != nil {
log.Fatal(err)
}
driver, _ := mysql.WithInstance(Db, &mysql.Config{})
m, _ := migrate.NewWithDatabaseInstance(
"file://internal/pkg/db/migrations/mysql",
"mysql",
driver,
)
if err := m.Up(); err != nil && !errors.Is(err, migrate.ErrNoChange) {
log.Fatal(err)
}
}
```


# The Database Schema

SQL migration scripts are scripts used to modify, update, or migrate a database schema and data from one version to another in a controlled and systematic way. They help developers and database administrators track changes over time, ensuring consistency across different environments such as development, testing, and production. The “migrate” call in the API server code will use the migration script below to initialize the SQL database during the first execution.

```
CREATE TABLE IF NOT EXISTS Users(
ID INT NOT NULL UNIQUE AUTO_INCREMENT,
Username VARCHAR (127) NOT NULL UNIQUE,
Password VARCHAR (127) NOT NULL,
PRIMARY KEY (ID)
);
CREATE TABLE IF NOT EXISTS Tasks(
ID INT NOT NULL UNIQUE AUTO_INCREMENT,
Text VARCHAR (255) ,
IsDone BOOLEAN,
UserID INT ,
FOREIGN KEY (UserID) REFERENCES Users(ID) ,
PRIMARY KEY (ID)
);%
```


# Defining the Database Queries

I will use GraphQL to define the API details and perform queries to the SQL database. The schema I provide below is very simple, but requires some basic familiarity with the GraphQL language and concepts. See the references section for more details on that [02].

An alternative approach would be to use a RESTful API. For more details on the differences between those two approaches see the links at the end of this post [03].

```
type Task {
id: ID!
text: String!
isDone: Boolean!
user: User!
}
type User {
id: ID!
name: String!
}
type Result {
isSuccessful: Boolean!
}
input NewTask {
text: String!
userId: String!
}
input UpdatedTask {
id: String!
isDone: Boolean!
}
type Query {
tasks: [Task!]!
}
type Mutation {
createTask(input: NewTask!): Task!
updateTask(input: UpdatedTask!): Result!
deleteTask(input: String!): Result!
}
```


The GraphQL queries will internally be resolved to a basic set of Create, Read, Update, and Delete (CRUD) operations. Those are implemented below.

```
package tasks
import (
"database/sql"
"log"
database "server/internal/pkg/db/mysql"
)
type User struct {
ID string `json:"id"`
Username string `json:"name"`
Password string `json:"password"`
}
type Task struct {
ID string
Text string
IsDone bool
User *users.User
}
func (task Task) Save() int64 {
stmt, err := database.Db.Prepare("INSERT INTO Tasks(Text,IsDone) VALUES(?,?)")
if err != nil {
log.Fatal(err)
}
res, err := stmt.Exec(task.Text, task.IsDone)
if err != nil {
log.Fatal(err)
}
id, err := res.LastInsertId()
if err != nil {
log.Fatal("Error:", err.Error())
}
return id
}
func (task Task) Update() bool {
stmt, err := database.Db.Prepare("UPDATE Tasks SET IsDone=? WHERE ID=?")
if err != nil {
log.Fatal(err)
}
res, err := stmt.Exec(task.IsDone, task.ID)
if err != nil {
log.Fatal(err)
}
count, err := res.RowsAffected()
if err != nil {
log.Fatal(err)
}
return count == 1
}
func (task Task) Delete() bool {
stmt, err := database.Db.Prepare("DELETE FROM Tasks WHERE ID=?")
if err != nil {
log.Fatal(err)
}
res, err := stmt.Exec(task.ID)
if err != nil {
log.Fatal(err)
}
count, err := res.RowsAffected()
if err != nil {
log.Fatal(err)
}
return count == 1
}
func GetAll() []Task {
stmt, err := database.Db.Prepare("SELECT ID, Text, IsDone FROM Tasks")
if err != nil {
log.Fatal(err)
}
defer func(stmt *sql.Stmt) {
err := stmt.Close()
if err != nil {
log.Fatal(err)
}
}(stmt)
rows, err := stmt.Query()
if err != nil {
log.Fatal(err)
}
defer func(rows *sql.Rows) {
err := rows.Close()
if err != nil {
log.Fatal(err)
}
}(rows)
var tasks []Task
for rows.Next() {
var task Task
err := rows.Scan(&task.ID, &task.Text, &task.IsDone)
if err != nil {
log.Fatal(err)
}
tasks = append(tasks, task)
}
if err = rows.Err(); err != nil {
log.Fatal(err)
}
return tasks
}
```


Finally, I use the GQLGen tool that will process the GraphQL schema and generate the glue code that calls the CRUD tasks implemented above. For details on using GQLGen see the references section at the end of this page [04]. After generating the code, the resolvers need to be implemented. Below you can see an example of what a resolver looks like. Review the

*schema.resolvers.go*file in the repository for the complete solution.

```
// CreateTask is the resolver for the createTask field.
func (r *mutationResolver) CreateTask(ctx context.Context,
input model.NewTask) (*model.Task, error) {
var task tasks.Task
log.Print("Creating new task: ", input, "..")
task.Text = input.Text
task.IsDone = false
TaskID := task.Save()
log.Print("Created new task with ID: ", TaskID)
return &model.Task{
ID: strconv.FormatInt(TaskID, 10),
Text: task.Text, IsDone: task.IsDone
}, nil
}
```


# The Deployment Environment

I use Docker to containerize and deploy the API and database services. More specifically the compose tool is used to simplify the process. Here’s how we setup the containers:

```
name: todo
services:
server:
container_name: todo_server
image: todo_server:latest
ports:
- 4000:4000
depends_on:
- mysql
mysql:
container_name: todo_db
image: mysql:latest
ports:
- 3306:3306
environment:
- MYSQL_ROOT_PASSWORD=pass
- MYSQL_DATABASE=todo
```


There are two containers involved. The MySQL container is prebuilt, while the API server container is created manually using the following Dockerfile.

```
# Stage 1: Build
FROM golang:1.23 AS build
ADD . /app
WORKDIR /app
RUN make build
# Stage 2: Image
FROM alpine:3.18
WORKDIR /app
COPY --from=build /app/server /app/
RUN mkdir -p /app/internal/pkg/db/migrations/mysql/
COPY --from=build /app/internal/pkg/db/migrations/mysql/ /app/internal/pkg/db/migrations/mysql/
ENTRYPOINT exec /app/server
```


Once all dependencies are pulled, starting the containers with docker-compose will produce an output similar to the following. Note that the API service will keep retrying to connect to the database until the MySQL server is up and running.

$ docker compose up [+] Running 2/2 ✔ Container todo_db Created 0.0s ✔ Container todo_server Created 0.0s Attaching to todo_db, todo_server todo_server | 2025/01/23 03:21:07 dial tcp 192.168.32.2:3306: connect: connection refused todo_server | 2025/01/23 02:00:12 Initiating database connection.. todo_server | 2025/01/23 02:00:12 Performing database migration.. todo_server | 2025/01/23 02:00:12 Starting server at port 4000

# Testing

A simple way to test the API backend is to issue our requests using curl. You can see an example of that implemented in a shell script below.

```
#!/bin/bash
# Tests performed:
# 1. Get all tasks
curl -X POST http://127.0.0.1:4000/api -H "Content-Type: application/json" \
-d '{"query": "query { tasks { id text isDone } }"}'
# 2. Create new task
curl -X POST http://127.0.0.1:4000/api -H "Content-Type: application/json" \
-d '{"query": "mutation { createTask(input:{text:\"AUTO GENERATED TEST TASK\" userId:\"1\"}) { id }}"}'
# 3. Delete a task
curl -X POST http://127.0.0.1:4000/api -H "Content-Type: application/json" \
-d '{"query": "mutation { deleteTask(input:\"1\") { isSuccessful }}"}'
# 4. Update a task
curl -X POST http://127.0.0.1:4000/api -H "Content-Type: application/json" \
-d '{"query": "mutation { updateTask(input:{ id:\"2\" isDone:true }) { isSuccessful }}"}'
```


While this testing method is not comprehensive, it allows for a quick first pass test of the API implementation. We’ll revisit the topic of testing and demonstrate how to use an appropriate framework to write test cases in another post.