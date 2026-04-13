---
title: 使用Filebeat输送Docker容器的日志
url: https://tonybai.com/2016/03/25/ship-docker-container-log-with-filebeat/
published: '2016-03-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Filebeat输送Docker容器的日志

今天我们来说说[Docker](https://www.docker.com/)容器日志。

### 一、容器日志输出的旧疾及能力演进

[Docker](http://tonybai.com/tag/docker)容器在默认情况下会将打印到stdout、stderr的 日志数据存储在本地磁盘上，默认位置为/var/lib/docker/containers/{ContainerId} /{ContainerId}-json.log。在老版本Docker中，这种日志记录方式经常被诟病，诸如：日志大小无限制、无法 Rotate（轮转）、无日志基本管理能力以及性能糟糕等。针对这些旧疾，Docker一直试图在演进中完善和解决。

记忆中好像是在Docker 1.8版本中，Docker增加了对json-file型（默认）log driver的rotate功能，我们可通过max-size和max-file两个–log-opt来配置。比如：我们启动一个nginx容器，采用 json-file日志引擎，每个log文件限制最大为1k，轮转的日志个数为5个：

```
$docker run -d --log-driver=json-file --log-opt max-size=1k --log-opt max-file=5 --name webserver -p 9988:80 nginx
50f100e7ea4d5b4931f144f9eac12b6a05e56579583d7a0322b250004b68ae72
$ sudo ls -l /var/lib/docker/containers/50f100e7ea4d5b4931f144f9eac12b6a05e56579583d7a0322b250004b68ae72
总用量 44
-rw-r--r-- 1 root root 226 3月 24 14:39 50f100e7ea4d5b4931f144f9eac12b6a05e56579583d7a0322b250004b68ae72-json.log
-rw-r--r-- 1 root root 1129 3月 24 14:39 50f100e7ea4d5b4931f144f9eac12b6a05e56579583d7a0322b250004b68ae72-json.log.1
-rw-r--r-- 1 root root 1130 3月 24 14:39 50f100e7ea4d5b4931f144f9eac12b6a05e56579583d7a0322b250004b68ae72-json.log.2
-rw-r--r-- 1 root root 1129 3月 24 14:39 50f100e7ea4d5b4931f144f9eac12b6a05e56579583d7a0322b250004b68ae72-json.log.3
-rw-r--r-- 1 root root 1129 3月 24 14:39 50f100e7ea4d5b4931f144f9eac12b6a05e56579583d7a0322b250004b68ae72-json.log.4
... ...
```


有了rotate，我们就不必担心某个container的日志暴涨而将同host的其他container拖死了。不过对于日志的管理目前也仅仅演进到如此，很多需求还得依靠第三方工具和方案来解决。

另外当前Docker容器日志的写入性能依旧糟糕，如果对此敏感，可以用volume机制来解决，即 关闭容器内应用的标准输出、错误（–log-driver=none），直接将日志写到某mounted volume中的某个文件中。下面是bare metal裸机原生写日志文件、volume方式写日志文件以及docker默认写json文件的性能简单对比：

我们用dd这个小工具，以go1.6.linux-amd64.tar.gz这个 85MB的文件作为输入，结果如下：（环境ubuntu 12.04 docker 1.9.1）

```
1、bare metal
dd if=~/.bin/go1.6.linux-amd64.tar.gz of=./go.bin
记录了165623+1 的读入
记录了165623+1 的写出
84799480字节(85 MB)已复制，0.426716 秒，199 MB/秒
2、通过挂在本地volume
$ docker run --rm -it -v /home1/tonybai/testdd/volume:/testdd ubuntu:14.04 dd if=/testdd/go1.6.linux-amd64.tar.gz of=/testdd/go.bin
165623+1 records in
165623+1 records out
84799480 bytes (85 MB) copied, 0.3753 s, 226 MB/s
3、docker default
$docker run -v /home1/tonybai/testdd/volume:/testdd ubuntu:14.04 dd if=/testdd/go1.6.linux-amd64.tar.gz 2>&1 1>/dev/null
165623+1 records in
165623+1 records out
84799480 bytes (85 MB) copied, 5.97732 s, 14.2 MB/s
$ sudo ls -lh /var/lib/docker/containers/d4b5e6aae3968f68e5081414ad95c6308fa91808b44b415a03040403af5a4713/ d4b5e6aae3968f68e5081414ad95c6308fa91808b44b415a03040403af5a4713-json.log
-rw------- 1 root root 331M 3月 24 18:05 /var/lib/docker/containers/d4b5e6aae3968f68e5081414ad95c6308fa91808b44b415a03040403af5a4713/ d4b5e6aae3968f68e5081414ad95c6308fa91808b44b415a03040403af5a4713-json.log
```


可以看出，默认情况下，Docker写入json的速度是挂载volume方式的十分之一还低。主要原因是Docker容器的标准输出、 标准错误都会被Docker Daemon接管，并由Daemon写入json log文件，因此Daemon就成为了日志写入的瓶颈。

### 二、容器日志的集中管理

日志的管理需求由来已久，无论是传统遗留系统，还是互联网应用或服务，日志在运维和运营中的作用不可小觑。尤其是现在被普遍采用的集中日志管理实践，对Docker的日志管理提出了新的要求。上面提到随着Docker的演进，Docker的logging已有所改善，增加了多种[log driver](https://docs.docker.com/engine/reference/run/#logging-drivers-log-driver)的支持（比如syslog、fluentd等），为容器日志的集中管理方案提供了多样性。

目前国内很多企业采用ELK方案（当然ELK方案不仅仅局限于Docker了），即[ElasticSearch](https://www.elastic.co/products/elasticsearch) + [Logstash](https://www.elastic.co/products/logstash) + [Kibana](https://www.elastic.co/products/kibana)，Logstash负责从各个节点收集、过滤、分析和处理日志，ElasticSearch负责存储、索引和查找日志；Kibana负责以图形化界面展示日志处理结果。但Docker Container如何做本地日志管理、如何将本地最新的日志输送给Logstash没有标准方案，你可以用[fluentd agent](http://www.fluentd.org/)也可以使用[logspout](https://github.com/gliderlabs/logspout)。ELK方案中也有自己的用于客户端节点日志输送的工具，以前称为logstash-forwarder：

```
node1 (logstash-forwarder) ------>
node2 (logstash-forwarder) ------> logstash server --> ElasticSearch
node3 (logstash-forwarder) ------>
```


现在Elastic.co使用[beats](https://www.elastic.co/products/beats)系列产品替代logstash-forwarder，针对日志输送这块，对应的beats产品是[filebeat](https://www.elastic.co/products/beats/filebeat)，使用filebeat后，前面的集中日志方案结构就变成了：

```
node1 (filebeat) ------>
node2 (filebeat) ------> [logstash server] --> ElasticSearch
node3 (filebeat) ------>
```


我们看到logstash server是一个可选的中间环节，使用filebeat后，你可以将client node上的最新日志直接发送给ElasticSearch，而无需经过logstash这一环节。当然如果你对源日志有过滤、清洗、分析等需求时，logstash依旧是你的得力助手。这里我们暂不用logstash，而是直接将日志发给ElasticSearch做存储和索引。

### 三、使用Filebeat输出容器日志的步骤

测试环境示意图如下：（ubuntu 14.04 + docker 1.9.1)

```
node1 (10.10.126.101 nginx container + filebeat) ------> server 10.10.105.71 (ElasticSearch + kibana)
```


这里的所有程序均以容器形式安装和运行。

#### 1、安装elasticsearch和kibana

elasticsearch和kibana都有官方Docker image。

安装elasticsearch：

```
$ docker pull elasticsearch
Using default tag: latest
latest: Pulling from library/elasticsearch
...
```


执行env，查看版本：

```
$ docker exec elasticsearch env
... ...
ELASTICSEARCH_MAJOR=2.2
ELASTICSEARCH_VERSION=2.2.1
ELASTICSEARCH_REPO_BASE=http://packages.elasticsearch.org/elasticsearch/2.x/debian
... ...
```


安装kibana：

```
$ docker pull kibana
Using default tag: latest
latest: Pulling from library/kibana
... ...
```


我们查看一下当前images列表：

```
REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE
elasticsearch latest c6b6bed19c45 8 days ago 347.1 MB
kibana latest d2c9c3cfc682 12 days ago 295.4 MB
... ...
```


#### 2、启动es和kibana，验证服务启动ok

启动ES:

```
$ sudo mkdir -p /data/elasticsearch
$ docker run -d --name elasticsearch -p 9200:9200 -v /data/elasticsearch:/usr/share/elasticsearch/data elasticsearch
4288b4db18af8575961faf940a1dc634fe30857bb184fb45611136b7bd3ffb7d
```


查看服务启动情况：

```
$ docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
4288b4db18af elasticsearch "/docker-entrypoint.s" 21 seconds ago Up 10 seconds 0.0.0.0:9200->9200/tcp, 9300/tcp elasticsearch
```


启动日志如下：

```
$ docker logs elasticsearch
[2016-03-24 11:00:29,289][INFO ][node ] [Katherine Reynolds] version[2.2.1], pid[1], build[d045fc2/2016-03-09T09:38:54Z]
[2016-03-24 11:00:29,291][INFO ][node ] [Katherine Reynolds] initializing ...
[2016-03-24 11:00:29,863][INFO ][plugins ] [Katherine Reynolds] modules [lang-expression, lang-groovy], plugins [], sites []
[2016-03-24 11:00:29,894][INFO ][env ] [Katherine Reynolds] using [1] data paths, mounts [[/usr/share/elasticsearch/data (/dev/disk/by-uuid/f577c0bc-665b-431b-96e0-e3536dc11469)]], net usable_space [114.5gb], net total_space [130.4gb], spins? [possibly], types [ext4]
[2016-03-24 11:00:29,894][INFO ][env ] [Katherine Reynolds] heap size [990.7mb], compressed ordinary object pointers [true]
[2016-03-24 11:00:31,881][INFO ][node ] [Katherine Reynolds] initialized
[2016-03-24 11:00:31,881][INFO ][node ] [Katherine Reynolds] starting ...
[2016-03-24 11:00:31,993][INFO ][transport ] [Katherine Reynolds] publish_address {172.17.0.1:9300}, bound_addresses {[::]:9300}
[2016-03-24 11:00:32,004][INFO ][discovery ] [Katherine Reynolds] elasticsearch/D7hV_RcHQa275Xc7if1Kkg
[2016-03-24 11:00:35,058][INFO ][cluster.service ] [Katherine Reynolds] new_master {Katherine Reynolds}{D7hV_RcHQa275Xc7if1Kkg}{172.17.0.1}{172.17.0.1:9300}, reason: zen-disco-join(elected_as_master, [0] joins received)
[2016-03-24 11:00:35,075][INFO ][http ] [Katherine Reynolds] publish_address {172.17.0.1:9200}, bound_addresses {[::]:9200}
[2016-03-24 11:00:35,076][INFO ][node ] [Katherine Reynolds] started
[2016-03-24 11:00:35,144][INFO ][gateway ] [Katherine Reynolds] recovered [0] indices into cluster_state
```


启动kibana：

启动kibana容器需要提供一个环境变量参数，即ES的服务地址和端口：

```
$docker run -d --name kibana -e ELASTICSEARCH_URL="http://10.10.105.72:9200" -p 5601:5601 kibana
```


要验证kibana是否启动ok，可以通过浏览器打开：http://10.10.105.72:5601，如果web页面正常显示，并且http://10.10.105.72:5601/status页面中有”Status: Green”字样，说明Kibana启动ok了。

#### 3、安装和配置filebeat

在安装filebeat前，我们先启动一个测试用webserver，部署在10.10.126.101上，用于产生日志数据：

```
$ docker run -d --log-driver=json-file --log-opt max-size=1k --log-opt max-file=5 --name webserver -p 9988:80 nginx
50f100e7ea4d5b4931f144f9eac12b6a05e56579583d7a0322b250004b68ae72
```


Filebeat没有官方image版本，docker hub上star数量最多的是prima/filebeat这个库中的image，我们就打算使用这个了，pull过程这里就不赘述了：

```
$docker run --rm prima/filebeat env
... ...
FILEBEAT_VERSION=1.1.2
... ...
```


可以看到这个库中的filebeat image使用的filebeat版本是最新的。

我们接下来来看run：

```
$ docker run --rm prima/filebeat
Loading config file error: Failed to read /filebeat.yml: open /filebeat.yml: no such file or directory. Exiting.
```


看来Filebeat需要做一些配置，我们得来查看一下Filebeat的[官方manual](https://www.elastic.co/guide/en/beats/filebeat/1.1/index.html)。

Filebeat需要一个filebeat.yml配置文件，用于配置log来源以及log输送的目的地，我们参考manual给出一个适合我们的配置：

```
filebeat:
# List of prospectors to fetch data.
prospectors:
# Each - is a prospector. Below are the prospector specific configurations
-
# Paths that should be crawled and fetched. Glob based paths.
# For each file found under this path, a harvester is started.
paths:
- "/var/lib/docker/containers/*/*.log"
#- c:\programdata\elasticsearch\logs\*
# Type of the files. Based on this the way the file is read is decided.
# The different types cannot be mixed in one prospector
#
# Possible options are:
# * log: Reads every line of the log file (default)
# * stdin: Reads the standard in
input_type: log
# Configure what outputs to use when sending the data collected by the beat.
# Multiple outputs may be used.
output:
### Elasticsearch as output
elasticsearch:
# Array of hosts to connect to.
hosts: ["10.10.105.72:9200"]
```


我们采集/var/lib/docker/containers/*/*.log，即filebeat所在节点的所有容器的日志。输出的位置是我们ElasticSearch的服务地址，这里我们直接将log输送给ES，而不通过Logstash中转。

再启动之前，我们还需要向ES提交一个filebeat index template，以便让Es知道filebeat输出的日志数据都包含哪些属性和字段。[filebeat.template.json](https://github.com/elastic/beats/blob/master/filebeat/etc/filebeat.template.json)这个模板文件不用我们编写，filebeat官方提供，我们可以[在github.com上找到它](https://github.com/elastic/beats/blob/master/filebeat/etc/filebeat.template.json)。

加载这个模板到ES:

```
$ curl -XPUT 'http://10.10.105.72:9200/_template/filebeat?pretty' -d@/home1/tonybai/filebeat.template.json
{
"acknowledged" : true
}
```


如果看到curl的返回结果是true，那么说明加载ok了。

接下来，我们启动filebeat容器：

```
$ docker run -d --name filebeat -v /home1/tonybai/filebeat.yml:/filebeat.yml prima/filebeat
f93497ea816e5c4015e69376f98e791ca02b91a20145ee1366e4c15f6a706c10
```


我们到Kibana中看看是否能收到容器的日志。使用Kibana时，需要添加一个新的index pattern。按照manual中的要求，对于filebeat输送的日志，我们的index name or pattern应该填写为：”filebeat-*“，不过我在kibana中添加default index ：filebeat-* 一直失败，下面那个按钮一直是灰色的，并提示：“Unable to fetch mapping. Do you have indices matching the pattern”。

在filebeat的forum中找寻问题答案，有人提示：看看ElasticSearch中是否有filebeat传输来的日志。于是查看ElasticSearch日志以及通过ElasticSearch提供的API做了一番查询，发现filebeat根本没有日志传输过来。

回过头仔细想来，wow，居然没给filebeat容器挂在/var/lib/docker/containers目录，那么filebeat就没有权限访问容器日志，自然不会有日志传输到ES了，下面的输出也证实了这一点：

```
$ docker exec filebeat ls /var/lib/docker/containers
ls: cannot access /var/lib/docker/containers: No such file or directory
```


于是修改filebeat启动参数：

```
$docker run -d --name filebeat -v /home1/tonybai/filebeat.yml:/filebeat.yml -v /var/lib/docker/containers:/var/lib/docker/containers prima/filebeat
```


一段时间后，我们就可以在Kibana上成功创建filebeat-* index pattern并看到filebeat输送过来的日志了。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

抱歉，暂停评论。