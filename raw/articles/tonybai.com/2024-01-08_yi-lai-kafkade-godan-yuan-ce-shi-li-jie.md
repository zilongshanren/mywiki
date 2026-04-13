---
title: 依赖Kafka的Go单元测试例解
url: https://tonybai.com/2024/01/08/go-unit-testing-deps-on-kafka/
published: '2024-01-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 依赖Kafka的Go单元测试例解

![](../../assets/595ef0635f98ee36.png)


[本文永久链接](https://tonybai.com/2024/01/08/go-unit-testing-deps-on-kafka) – https://tonybai.com/2024/01/08/go-unit-testing-deps-on-kafka

[Kafka](https://kafka.apache.org)是Apache基金会开源的一个分布式事件流处理平台，是Java阵营(最初为Scala)中的一款杀手级应用，其提供的高可靠性、高吞吐量和低延迟的数据传输能力，让其到目前为止依旧是现代企业级应用系统以及云原生应用系统中使用的重要中间件。

在日常开发Go程序时，我们经常会遇到一些[依赖Kafka的代码](https://tonybai.com/2023/09/04/slog-in-action-file-logging-rotation-and-kafka-integration/)，如何对这些代码进行测试，尤其是单测是摆在Go开发者前面的一个现实问题！

有人说用mock，是个路子。但看过我的《[单测时尽量用fake object](https://tonybai.com/2023/04/20/provide-fake-object-for-external-collaborators/)》一文的童鞋估计已经走在了寻找kafka fake object的路上了！Kafka虽好，但身形硕大，不那么灵巧。找到一个合适的fake object不容易。在这篇文章中，我们就来聊聊如何测试那些依赖kafka的代码，再往本质一点说，就是和大家以找找那些合适的kafka fake object。

## 1. 寻找fake object的策略

在《[单测时尽量用fake object](https://tonybai.com/2023/04/20/provide-fake-object-for-external-collaborators/)》一文中，我们提到过，如果测试的依赖提供了tiny版本或某些简化版，我们可以直接使用这些版本作为fake object的候选，就像etcd提供了[用于测试的自身简化版的实现(embed)](https://github.com/etcd-io/etcd/blob/main/tests/integration/embed)那样。

但Kafka并没有提供tiny版本，我们也只能选择《[单测时尽量用fake object](https://tonybai.com/2023/04/20/provide-fake-object-for-external-collaborators/)》一文提到的另外一个策略，那就是**利用容器来充当fake object**，这是目前能搞到任意依赖的fake object的最简单路径了。也许以后[WASI(WebAssembly System Interface)](https://wasi.dev/)成熟了，让wasm脱离浏览器并可以在本地系统上飞起，到时候换用wasm也不迟。

下面我们就按照使用容器的策略来找一找适合的kafka container。

## 2. testcontainers-go

我们第一站就来到了[testcontainers-go](https://golang.testcontainers.org/)。testcontainers-go是一个Go语言开源项目，专门用于简化创建和清理基于容器的依赖项，常用于Go项目的单元测试、自动化集成或冒烟测试中。通过testcontainers-go提供的易于使用的API，开发人员能够以编程方式定义作为测试的一部分而运行的容器，并在测试完成时清理这些资源。

注：

[testcontainers]不仅提供Go API，它还覆盖了主流的编程语言，包括：Java、.NET、Python、Node.js、[Rust]等。

在几个月之前，[testcontainers-go](https://github.com/testcontainers/testcontainers-go/)项目还没有提供对Kafka的直接支持，我们需要自己使用testcontainers.GenericContainer来自定义并启动kafka容器。2023年9月，[以KRaft模式运行的Kafka容器才被首次引入testcontainers-go项目](https://github.com/testcontainers/testcontainers-go/pull/1610)。

目前testcontainers-go使用的kafka镜像版本是[confluentinc/confluent-local:7.5.0](https://hub.docker.com/r/confluentinc/confluent-local)。[Confluent](https://www.confluent.io)是在kafka背后的那家公司，基于kafka提供商业化支持。今年初，Confluent还收购了Immerok，将apache的另外一个明星项目Flink招致麾下。

[confluent-local](https://hub.docker.com/r/confluentinc/confluent-local)并不是一个流行的kafka镜像，它只是一个使用KRaft模式的零配置的、包含Confluent Community RestProxy的Apache Kafka，并且镜像是实验性的，仅应用于本地开发工作流，不应该用在支持生产工作负载。

生产中最常用的开源kafka镜像是[confluentinc/cp-kafka镜像](https://hub.docker.com/r/confluentinc/cp-kafka)，它是基于开源Kafka项目构建的，但在此基础上添加了一些额外的功能和工具，以提供更丰富的功能和更易于部署和管理的体验。cp-kafka镜像的版本号并非kafka的版本号，其对应关系需要cp-kafka镜像官网查询。

另外一个开发领域常用的kafka镜像是bitnami的kafka镜像。Bitnami是一个提供各种开源软件的预打包镜像和应用程序栈的公司。Bitnami Kafka镜像是基于开源Kafka项目构建的，是一个可用于快速部署和运行Kafka的Docker镜像。Bitnami Kafka镜像与其内部的Kakfa的版本号保持一致。

下面我们就来看看如何使用testcontainers-go的kafka来作为依赖kafka的Go单元测试用例的fake object。

这第一个测试示例改编自testcontainers-go/kafka module的example_test.go：

```
// testcontainers/kafka_setup/kafka_test.go
package main
import (
"context"
"fmt"
"testing"
"github.com/testcontainers/testcontainers-go/modules/kafka"
)
func TestKafkaSetup(t *testing.T) {
ctx := context.Background()
kafkaContainer, err := kafka.RunContainer(ctx, kafka.WithClusterID("test-cluster"))
if err != nil {
panic(err)
}
// Clean up the container
defer func() {
if err := kafkaContainer.Terminate(ctx); err != nil {
panic(err)
}
}()
state, err := kafkaContainer.State(ctx)
if err != nil {
panic(err)
}
if kafkaContainer.ClusterID != "test-cluster" {
t.Errorf("want test-cluster, actual %s", kafkaContainer.ClusterID)
}
if state.Running != true {
t.Errorf("want true, actual %t", state.Running)
}
brokers, _ := kafkaContainer.Brokers(ctx)
fmt.Printf("%q\n", brokers)
}
```


在这个例子中，我们直接调用kafka.RunContainer创建了一个名为test-cluster的kafka实例，如果没有通过WithImage向RunContainer传入自定义镜像，那么默认我们将启动一个confluentinc/confluent-local:7.5.0的容器（注意：随着时间变化，该默认容器镜像的版本也会随之改变）。

通过RunContainer返回的kafka.KafkaContainer我们可以获取到关于kafka容器的各种信息，比如上述代码中的ClusterID、kafka Broker地址信息等。有了这些信息，我们后续便可以与以容器形式启动的kafka建立连接并做数据的写入和读取操作了。

我们先来看这个测试的运行结果，与预期一致：

```
$ go test
2023/12/16 21:45:52 github.com/testcontainers/testcontainers-go - Connected to docker:
... ...
Resolved Docker Host: unix:///var/run/docker.sock
Resolved Docker Socket Path: /var/run/docker.sock
Test SessionID: 19e47867b733f4da4f430d78961771ae3a1cc66c5deca083b4f6359c6d4b2468
Test ProcessID: 41b9ef62-2617-4189-b23a-1bfa4c06dfec
2023/12/16 21:45:52 Creating container for image docker.io/testcontainers/ryuk:0.5.1
2023/12/16 21:45:53 Container created: 8f2240042c27
2023/12/16 21:45:53 Starting container: 8f2240042c27
2023/12/16 21:45:53 Container started: 8f2240042c27
2023/12/16 21:45:53 Waiting for container id 8f2240042c27 image: docker.io/testcontainers/ryuk:0.5.1. Waiting for: &{Port:8080/tcp timeout:<nil> PollInterval:100ms}
2023/12/16 21:45:53 Creating container for image confluentinc/confluent-local:7.5.0
2023/12/16 21:45:53 Container created: a39a495aed0b
2023/12/16 21:45:53 Starting container: a39a495aed0b
2023/12/16 21:45:53 Container started: a39a495aed0b
["localhost:1037"]
2023/12/16 21:45:58 Terminating container: a39a495aed0b
2023/12/16 21:45:58 Container terminated: a39a495aed0b
PASS
ok demo 6.236s
```


接下来，在上面用例的基础上，我们再来做一个Kafka连接以及数据读写测试：

```
// testcontainers/kafka_consumer_and_producer/kafka_test.go
package main
import (
"bytes"
"context"
"errors"
"net"
"strconv"
"testing"
"time"
"github.com/testcontainers/testcontainers-go/modules/kafka"
kc "github.com/segmentio/kafka-go" // kafka client
)
func createTopics(brokers []string, topics ...string) error {
// to create topics when auto.create.topics.enable='false'
conn, err := kc.Dial("tcp", brokers[0])
if err != nil {
return err
}
defer conn.Close()
controller, err := conn.Controller()
if err != nil {
return err
}
var controllerConn *kc.Conn
controllerConn, err = kc.Dial("tcp", net.JoinHostPort(controller.Host, strconv.Itoa(controller.Port)))
if err != nil {
return err
}
defer controllerConn.Close()
var topicConfigs []kc.TopicConfig
for _, topic := range topics {
topicConfig := kc.TopicConfig{
Topic: topic,
NumPartitions: 1,
ReplicationFactor: 1,
}
topicConfigs = append(topicConfigs, topicConfig)
}
err = controllerConn.CreateTopics(topicConfigs...)
if err != nil {
return err
}
return nil
}
func newWriter(brokers []string, topic string) *kc.Writer {
return &kc.Writer{
Addr: kc.TCP(brokers...),
Topic: topic,
Balancer: &kc.LeastBytes{},
AllowAutoTopicCreation: true,
RequiredAcks: 0,
}
}
func newReader(brokers []string, topic string) *kc.Reader {
return kc.NewReader(kc.ReaderConfig{
Brokers: brokers,
Topic: topic,
GroupID: "test-group",
MaxBytes: 10e6, // 10MB
})
}
func TestProducerAndConsumer(t *testing.T) {
ctx := context.Background()
kafkaContainer, err := kafka.RunContainer(ctx, kafka.WithClusterID("test-cluster"))
if err != nil {
t.Fatalf("want nil, actual %v\n", err)
}
// Clean up the container
defer func() {
if err := kafkaContainer.Terminate(ctx); err != nil {
t.Fatalf("want nil, actual %v\n", err)
}
}()
state, err := kafkaContainer.State(ctx)
if err != nil {
t.Fatalf("want nil, actual %v\n", err)
}
if state.Running != true {
t.Errorf("want true, actual %t", state.Running)
}
brokers, err := kafkaContainer.Brokers(ctx)
if err != nil {
t.Fatalf("want nil, actual %v\n", err)
}
topic := "test-topic"
w := newWriter(brokers, topic)
defer w.Close()
r := newReader(brokers, topic)
defer r.Close()
err = createTopics(brokers, topic)
if err != nil {
t.Fatalf("want nil, actual %v\n", err)
}
time.Sleep(5 * time.Second)
messages := []kc.Message{
{
Key: []byte("Key-A"),
Value: []byte("Value-A"),
},
{
Key: []byte("Key-B"),
Value: []byte("Value-B"),
},
{
Key: []byte("Key-C"),
Value: []byte("Value-C"),
},
{
Key: []byte("Key-D"),
Value: []byte("Value-D!"),
},
}
const retries = 3
for i := 0; i < retries; i++ {
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
// attempt to create topic prior to publishing the message
err = w.WriteMessages(ctx, messages...)
if errors.Is(err, kc.LeaderNotAvailable) || errors.Is(err, context.DeadlineExceeded) {
time.Sleep(time.Millisecond * 250)
continue
}
if err != nil {
t.Fatalf("want nil, actual %v\n", err)
}
break
}
var getMessages []kc.Message
for i := 0; i < len(messages); i++ {
m, err := r.ReadMessage(context.Background())
if err != nil {
t.Fatalf("want nil, actual %v\n", err)
}
getMessages = append(getMessages, m)
}
for i := 0; i < len(messages); i++ {
if !bytes.Equal(getMessages[i].Key, messages[i].Key) {
t.Errorf("want %s, actual %s\n", string(messages[i].Key), string(getMessages[i].Key))
}
if !bytes.Equal(getMessages[i].Value, messages[i].Value) {
t.Errorf("want %s, actual %s\n", string(messages[i].Value), string(getMessages[i].Value))
}
}
}
```


我们[使用segmentio/kafka-go这个客户端](https://tonybai.com/2022/03/28/the-comparison-of-the-go-community-leading-kakfa-clients)来实现kafka的读写。关于如何使用segmentio/kafka-go这个客户端，可以参考我之前写的《[Go社区主流Kafka客户端简要对比](https://tonybai.com/2022/03/28/the-comparison-of-the-go-community-leading-kakfa-clients)》。

这里我们在TestProducerAndConsumer这个用例中，先通过testcontainers-go的kafka.RunContainer启动一个Kakfa实例，然后创建了一个topic: “test-topic”。我们在写入消息前也可以不单独创建这个“test-topic”，Kafka默认启用topic自动创建，并且segmentio/kafka-go的高级API：Writer也支持AllowAutoTopicCreation的设置。不过topic的创建需要一些时间，如果要在首次写入消息时创建topic，此次写入可能会失败，需要retry。

向topic写入一条消息(实际上是一个批量Message，包括四个key-value pair)后，我们调用ReadMessage从上述topic中读取消息，并将读取的消息与写入的消息做比较。

注：近期

[发现kafka-go的一个可能导致内存暴涨的问题]，在kafka ack返回延迟变大的时候，可能触发该问题。

下面是执行该用例的输出结果：

```
$ go test
2023/12/17 17:43:54 github.com/testcontainers/testcontainers-go - Connected to docker:
Server Version: 24.0.7
API Version: 1.43
Operating System: CentOS Linux 7 (Core)
Total Memory: 30984 MB
Resolved Docker Host: unix:///var/run/docker.sock
Resolved Docker Socket Path: /var/run/docker.sock
Test SessionID: f76fe611c753aa4ef1456285503b0935a29795e7c0fab2ea2588029929215a08
Test ProcessID: 27f531ee-9b5f-4e4f-b5f0-468143871004
2023/12/17 17:43:54 Creating container for image docker.io/testcontainers/ryuk:0.5.1
2023/12/17 17:43:54 Container created: 577309098f4c
2023/12/17 17:43:54 Starting container: 577309098f4c
2023/12/17 17:43:54 Container started: 577309098f4c
2023/12/17 17:43:54 Waiting for container id 577309098f4c image: docker.io/testcontainers/ryuk:0.5.1. Waiting for: &{Port:8080/tcp timeout:<nil> PollInterval:100ms}
2023/12/17 17:43:54 Creating container for image confluentinc/confluent-local:7.5.0
2023/12/17 17:43:55 Container created: 1ee11e11742b
2023/12/17 17:43:55 Starting container: 1ee11e11742b
2023/12/17 17:43:55 Container started: 1ee11e11742b
2023/12/17 17:44:15 Terminating container: 1ee11e11742b
2023/12/17 17:44:15 Container terminated: 1ee11e11742b
PASS
ok demo 21.505s
```


我们看到默认情况下，testcontainer能满足与kafka交互的基本需求，并且testcontainer提供了一系列Option(WithXXX)可以对container进行定制，以满足一些扩展性的要求，但是这需要你对testcontainer提供的API有更全面的了解。

除了开箱即用的testcontainer之外，我们还可以使用另外一种方便的基于容器的技术：[docker-compose来定制和启停我们需要的kafka image](https://tonybai.com/2021/11/26/build-all-in-one-runtime-environment-with-docker-compose)。接下来，我们就来看看如何使用docker-compose建立fake kafka object。

## 3. 使用docker-compose建立fake kafka

### 3.1 一个基础的基于docker-compose的fake kafka实例模板

这次我们使用bitnami提供的kafka镜像，我们先建立一个“等价”于上面“testcontainers-go”提供的kafka module的kafka实例，下面是docker-compose.yml：

```
// docker-compose/bitnami/plaintext/docker-compose.yml
version: "2"
services:
kafka:
image: docker.io/bitnami/kafka:3.6
network_mode: "host"
volumes:
- "kafka_data:/bitnami"
environment:
# KRaft settings
- KAFKA_CFG_NODE_ID=0
- KAFKA_CFG_PROCESS_ROLES=controller,broker
- KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@localhost:9093
# Listeners
- KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
- KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://:9092
- KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
- KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
- KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
# borrow from testcontainer
- KAFKA_CFG_BROKER_ID=0
- KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR=1
- KAFKA_CFG_OFFSETS_TOPIC_NUM_PARTITIONS=1
- KAFKA_CFG_TRANSACTION_STATE_LOG_MIN_ISR=1
- KAFKA_CFG_GROUP_INITIAL_REBALANCE_DELAY_MS=0
- KAFKA_CFG_LOG_FLUSH_INTERVAL_MESSAGES=9223372036854775807
volumes:
kafka_data:
driver: local
```


我们看到其中一些配置“借鉴”了testcontainers-go的kafka module，我们启动一下该容器：

```
$ docker-compose up -d
[+] Running 2/2
✔ Volume "plaintext_kafka_data" Created 0.0s
✔ Container plaintext-kafka-1 Started 0.1s
```


依赖该容器的go测试代码与前面的TestProducerAndConsumer差不多，只是在开始处去掉了container的创建过程：

```
// docker-compose/bitnami/plaintext/kafka_test.go
func TestProducerAndConsumer(t *testing.T) {
brokers := []string{"localhost:9092"}
topic := "test-topic"
w := newWriter(brokers, topic)
defer w.Close()
r := newReader(brokers, topic)
defer r.Close()
err := createTopics(brokers, topic)
if err != nil {
t.Fatalf("want nil, actual %v\n", err)
}
time.Sleep(5 * time.Second)
... ...
}
```


运行该测试用例，我们看到预期的结果：

```
go test
write message ok Value-A
write message ok Value-B
write message ok Value-C
write message ok Value-D!
PASS
ok demo 15.143s
```


不过对于单元测试来说，显然我们不能手动来启动和停止kafka container，我们需要为每个用例填上setup和teardown，这样也能保证用例间的相互隔离，于是我们增加了一个docker_compose_helper.go文件，在这个文件中我们提供了一些帮助testcase启停kafka的helper函数：

```
// docker-compose/bitnami/plaintext/docker_compose_helper.go
package main
import (
"fmt"
"os/exec"
"strings"
"time"
)
// helpler function for operating docker container through docker-compose command
const (
defaultCmd = "docker-compose"
defaultCfgFile = "docker-compose.yml"
)
func execCliCommand(cmd string, opts ...string) ([]byte, error) {
cmds := cmd + " " + strings.Join(opts, " ")
fmt.Println("exec command:", cmds)
return exec.Command(cmd, opts...).CombinedOutput()
}
func execDockerComposeCommand(cmd string, cfgFile string, opts ...string) ([]byte, error) {
var allOpts = []string{"-f", cfgFile}
allOpts = append(allOpts, opts...)
return execCliCommand(cmd, allOpts...)
}
func UpKakfa(composeCfgFile string) ([]byte, error) {
b, err := execDockerComposeCommand(defaultCmd, composeCfgFile, "up", "-d")
if err != nil {
return nil, err
}
time.Sleep(10 * time.Second)
return b, nil
}
func UpDefaultKakfa() ([]byte, error) {
return UpKakfa(defaultCfgFile)
}
func DownKakfa(composeCfgFile string) ([]byte, error) {
b, err := execDockerComposeCommand(defaultCmd, composeCfgFile, "down", "-v")
if err != nil {
return nil, err
}
time.Sleep(10 * time.Second)
return b, nil
}
func DownDefaultKakfa() ([]byte, error) {
return DownKakfa(defaultCfgFile)
}
```


眼尖的童鞋可能看到：在UpKakfa和DownKafka函数中我们使用了硬编码的“time.Sleep”来等待10s，通常在镜像已经pull到本地后这是有效的，但却不是最精确地等待方式，[testcontainers-go/wait](https://pkg.go.dev/github.com/testcontainers/testcontainers-go@v0.26.0/wait)中提供了等待容器内程序启动完毕的多种策略，如果你想用更精确的等待方式，可以了解一下wait包。

基于helper函数，我们改造一下TestProducerAndConsumer用例：

```
// docker-compose/bitnami/plaintext/kafka_test.go
func TestProducerAndConsumer(t *testing.T) {
_, err := UpDefaultKakfa()
if err != nil {
t.Fatalf("want nil, actual %v\n", err)
}
t.Cleanup(func() {
DownDefaultKakfa()
})
... ...
}
```


我们在用例开始处通过UpDefaultKakfa使用docker-compose将kafka实例启动起来，然后[注册了Cleanup函数](https://tonybai.com/2020/03/08/some-changes-in-go-1-14/)，用于在test case执行结束后销毁kafka实例。

下面是新版用例的执行结果：

```
$ go test
exec command: docker-compose -f docker-compose.yml up -d
write message ok Value-A
write message ok Value-B
write message ok Value-C
write message ok Value-D!
exec command: docker-compose -f docker-compose.yml down -v
PASS
ok demo 36.402s
```


使用docker-compose的最大好处就是可以通过docker-compose.yml文件对要fake的object进行灵活的定制，这种定制与testcontainers-go的差别就是你无需去研究testcontiners-go的API。

下面是使用tls连接与kafka建立连接并实现读写的示例。

### 3.2 建立一个基于TLS连接的fake kafka实例

Kafka的配置复杂是有目共睹的，为了建立一个基于TLS连接，我也是花了不少时间做“试验”，尤其是listeners以及证书的配置，不下点苦功夫读文档还真是配不出来。

下面是一个基于bitnami/kafka镜像配置出来的基于TLS安全通道上的kafka实例：

```
// docker-compose/bitnami/tls/docker-compose.yml
# config doc: https://github.com/bitnami/containers/blob/main/bitnami/kafka/README.md
version: "2"
services:
kafka:
image: docker.io/bitnami/kafka:3.6
network_mode: "host"
#ports:
#- "9092:9092"
environment:
# KRaft settings
- KAFKA_CFG_NODE_ID=0
- KAFKA_CFG_PROCESS_ROLES=controller,broker
- KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@localhost:9094
# Listeners
- KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,SECURED://:9093,CONTROLLER://:9094
- KAFKA_CFG_ADVERTISED_LISTENERS=SECURED://:9093
- KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,SECURED:SSL,PLAINTEXT:PLAINTEXT
- KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
- KAFKA_CFG_INTER_BROKER_LISTENER_NAME=SECURED
# SSL settings
- KAFKA_TLS_TYPE=PEM
- KAFKA_TLS_CLIENT_AUTH=none
- KAFKA_CFG_SSL_ENDPOINT_IDENTIFICATION_ALGORITHM=
# borrow from testcontainer
- KAFKA_CFG_BROKER_ID=0
- KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR=1
- KAFKA_CFG_OFFSETS_TOPIC_NUM_PARTITIONS=1
- KAFKA_CFG_TRANSACTION_STATE_LOG_MIN_ISR=1
- KAFKA_CFG_GROUP_INITIAL_REBALANCE_DELAY_MS=0
- KAFKA_CFG_LOG_FLUSH_INTERVAL_MESSAGES=9223372036854775807
volumes:
# server.cert, server.key and ca.crt
- "kafka_data:/bitnami"
- "./kafka.keystore.pem:/opt/bitnami/kafka/config/certs/kafka.keystore.pem:ro"
- "./kafka.keystore.key:/opt/bitnami/kafka/config/certs/kafka.keystore.key:ro"
- "./kafka.truststore.pem:/opt/bitnami/kafka/config/certs/kafka.truststore.pem:ro"
volumes:
kafka_data:
driver: local
```


这里我们使用pem格式的证书和key，在上面配置中，volumes下面挂载的kafka.keystore.pem、kafka.keystore.key和kafka.truststore.pem分别对应了以前在Go中常用的名字：server-cert.pem(服务端证书), server-key.pem(服务端私钥)和ca-cert.pem(CA证书)。

这里整理了一个一键生成的脚本docker-compose/bitnami/tls/kafka-generate-cert.sh，我们执行该脚本生成所有需要的证书并放到指定位置(遇到命令行提示，只需要一路回车即可)：

```
$bash kafka-generate-cert.sh
.........++++++
.............................++++++
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:
State or Province Name (full name) []:
Locality Name (eg, city) [Default City]:
Organization Name (eg, company) [Default Company Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (eg, your name or your server's hostname) []:
Email Address []:
Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
Signature ok
subject=/C=XX/L=Default City/O=Default Company Ltd
Getting Private key
.....................++++++
.........++++++
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:
State or Province Name (full name) []:
Locality Name (eg, city) [Default City]:
Organization Name (eg, company) [Default Company Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (eg, your name or your server's hostname) []:
Email Address []:
Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
Signature ok
subject=/C=XX/L=Default City/O=Default Company Ltd
Getting CA Private Key
```


接下来，我们来改造用例，使之支持以tls方式建立到kakfa的连接：

```
//docker-compose/bitnami/tls/kafka_test.go
func createTopics(brokers []string, tlsConfig *tls.Config, topics ...string) error {
dialer := &kc.Dialer{
Timeout: 10 * time.Second,
DualStack: true,
TLS: tlsConfig,
}
conn, err := dialer.DialContext(context.Background(), "tcp", brokers[0])
if err != nil {
fmt.Println("creating topic: dialer dial error:", err)
return err
}
defer conn.Close()
fmt.Println("creating topic: dialer dial ok")
... ...
}
func newWriter(brokers []string, tlsConfig *tls.Config, topic string) *kc.Writer {
w := &kc.Writer{
Addr: kc.TCP(brokers...),
Topic: topic,
Balancer: &kc.LeastBytes{},
AllowAutoTopicCreation: true,
Async: true,
//RequiredAcks: 0,
Completion: func(messages []kc.Message, err error) {
for _, message := range messages {
if err != nil {
fmt.Println("write message fail", err)
} else {
fmt.Println("write message ok", string(message.Topic), string(message.Value))
}
}
},
}
if tlsConfig != nil {
w.Transport = &kc.Transport{
TLS: tlsConfig,
}
}
return w
}
func newReader(brokers []string, tlsConfig *tls.Config, topic string) *kc.Reader {
dialer := &kc.Dialer{
Timeout: 10 * time.Second,
DualStack: true,
TLS: tlsConfig,
}
return kc.NewReader(kc.ReaderConfig{
Dialer: dialer,
Brokers: brokers,
Topic: topic,
GroupID: "test-group",
MaxBytes: 10e6, // 10MB
})
}
func TestProducerAndConsumer(t *testing.T) {
var err error
_, err = UpDefaultKakfa()
if err != nil {
t.Fatalf("want nil, actual %v\n", err)
}
t.Cleanup(func() {
DownDefaultKakfa()
})
brokers := []string{"localhost:9093"}
topic := "test-topic"
tlsConfig, _ := newTLSConfig()
w := newWriter(brokers, tlsConfig, topic)
defer w.Close()
r := newReader(brokers, tlsConfig, topic)
defer r.Close()
err = createTopics(brokers, tlsConfig, topic)
if err != nil {
fmt.Printf("create topic error: %v, but it may not affect the later action, just ignore it\n", err)
}
time.Sleep(5 * time.Second)
... ...
}
func newTLSConfig() (*tls.Config, error) {
/*
// 加载 CA 证书
caCert, err := ioutil.ReadFile("/path/to/ca.crt")
if err != nil {
return nil, err
}
// 加载客户端证书和私钥
cert, err := tls.LoadX509KeyPair("/path/to/client.crt", "/path/to/client.key")
if err != nil {
return nil, err
}
// 创建 CertPool 并添加 CA 证书
caCertPool := x509.NewCertPool()
caCertPool.AppendCertsFromPEM(caCert)
*/
// 创建并返回 TLS 配置
return &tls.Config{
//RootCAs: caCertPool,
//Certificates: []tls.Certificate{cert},
InsecureSkipVerify: true,
}, nil
}
```


在上述代码中，我们按照segmentio/kafka-go为createTopics、newWriter和newReader都加上了tls.Config参数，此外在测试用例中，我们用newTLSConfig创建一个tls.Config的实例，在这里我们一切简化处理，采用InsecureSkipVerify=true的方式与kafka broker服务端进行握手，既不验证服务端证书，也不做双向认证(mutual TLS)。

下面是修改代码后的测试用例执行结果：

```
$ go test
exec command: docker-compose -f docker-compose.yml up -d
creating topic: dialer dial ok
creating topic: get controller ok
creating topic: dial control listener ok
create topic error: EOF, but it may not affect the later action, just ignore it
write message error: [3] Unknown Topic Or Partition: the request is for a topic or partition that does not exist on this broker
write message ok Value-A
write message ok Value-B
write message ok Value-C
write message ok Value-D!
exec command: docker-compose -f docker-compose.yml down -v
PASS
ok demo 38.473s
```


这里我们看到：createTopics虽然连接kafka的各个listener都ok，但调用topic创建时，返回EOF，但这的确不影响后续action的执行，不确定这是segmentio/kafka-go的问题，还是kafka实例的问题。另外首次写入消息时，也因为topic或partition未建立而失败，retry后消息正常写入。

通过这个例子我们看到，基于docker-compose建立fake object有着更广泛的灵活性，如果做好容器启动和停止的精准wait机制的话，我可能会更多选择这种方式。

## 4. 小结

本文介绍了如何在Go编程中进行依赖Kafka的单元测试，并探讨了寻找适合的Kafka fake object的策略。

对于Kafka这样的复杂系统来说，找到合适的fake object并不容易。因此，本文推荐使用容器作为fake object的策略，并分别介绍了使用testcontainers-go项目和使用docker-compose作为简化创建和清理基于容器的依赖项的工具。相对于刚刚加入testcontainers-go项目没多久的kafka module而言，使用docker-compose自定义fake object更加灵活一些。但无论哪种方法，开发人员都需要对kafka的配置有一个较为整体和深入的理解。

文中主要聚焦使用testcontainers-go和docker-compose建立fake kafka的过程，而用例并没有建立明确的sut(被测目标)，比如针对某个函数的白盒单元测试。

文本涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/unit-testing-deps-on-kafka)下载。

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2024年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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