---
title: weed-fs使用简介
url: https://tonybai.com/2015/08/22/intro-of-using-weedfs/
published: '2015-08-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# weed-fs使用简介

[weed-fs](https://github.com/chrislusf/seaweedfs)，全名Seaweed-fs，是一种用[golang](http://tonybai.com/tag/golang)实现的简单且高可用的分布式文件系统。该系统的目标有二：

- 存储billions of files

- serve the files fast

weed-fs起初是为了搞一个基于Fackbook的[Haystack论文](http://www.usenix.org/event/osdi10/tech/full_papers/Beaver.pdf)的实现，Haystack旨在优化Fackbook内部图片存储和获取。后在这个基 础上，weed-fs作者又增加了若干feature，形成了目前的weed-fs。

这里并不打算深入分析weed-fs源码，仅仅是从黑盒角度介绍weed-fs的使用，发掘weed-fs的功能、长处和不足。

**一、weed-fs集群简介**

weed-fs集群的拓扑(Topology)由DataCenter、Rack(机架)、Machine(或叫Node)组成。最初版本的weed-fs应该可以通 过配置文件来描述整个集群的拓扑结构，配置文件采用xml格式，官方给出的样例如下：

<Configuration>

<Topology>

<DataCenter name="dc1">

<Rack name="rack1">

<Ip>192.168.1.1</Ip>

</Rack>

</DataCenter>

<DataCenter name="dc2">

<Rack name="rack1">

<Ip>192.168.1.2</Ip>

</Rack>

<Rack name="rack2">

<Ip>192.168.1.3</Ip>

<Ip>192.168.1.4</Ip>

</Rack>

</DataCenter>

</Topology>

</Configuration>

但目前的版本中，该配置文件在help说明中被置为“Deprecating!”了：

$weed master -help

…

-conf="/etc/weedfs/weedfs.conf": Deprecating! xml configuration file

…

0.70版本的weed-fs在Master中维护集群拓扑，master会根据master与master、volume与master的连接 情况实时合成拓扑结构了。

weed-fs自身可以在两种模式下运行，一种是Master，另外一种则是Volume。集群的维护以及强一致性的保证由master们保 证，master间通过[raft协议](https://en.wikipedia.org/wiki/Raft_(computer_science))实现强一致性。Volume是实际管理和存储数据的运行实例。数据的可靠性则可以通过weed-fs提供的 replication机制保证。

weed-fs提供了若干种replication策略(rack – 机架，一个逻辑上的概念)：

000 no replication, just one copy

001 replicate once on the same rack

010 replicate once on a different rack in the same data center

100 replicate once on a different data center

200 replicate twice on two other different data center

110 replicate once on a different rack, and once on a different data center

选择数据更可靠的策略，则会带来一些性能上的代价，这始终是一个权衡的问题。

更多的细节以及Scaling、数据迁移等方面，下面将逐一说明。

**二、weed-fs集群的启动**

为了实验方便，我们定义了一个weed-fs集群拓扑：

三个master:

master1 – localhost:9333

master2 – localhost:9334

master3 – localhost:9335

replication策略：100(即在另外一个不同的datacenter中复制一份)

三个volume:

volume1 – localhost:8081 dc1

volume2 – localhost:8082 dc1

volume3 – localhost:8083 dc2

集群启动首先启动master们，启动顺序: master1、master2、master3：

master1:

$ weed -v=3 master -port=9333 -mdir=./m1 -peers=localhost:9333,localhost:9334,localhost:9335 -defaultReplication=100

I0820 14:37:17 07606 file_util.go:20] Folder ./m1 Permission: -rwxrwxr-x

I0820 14:37:17 07606 topology.go:86] Using default configurations.

I0820 14:37:17 07606 master_server.go:59] Volume Size Limit is 30000 MB

I0820 14:37:17 07606 master.go:69] Start Seaweed Master 0.70 beta at 0.0.0.0:9333

I0820 14:37:17 07606 raft_server.go:50] Starting RaftServer with IP:localhost:9333:

I0820 14:37:17 07606 raft_server.go:74] Joining cluster: localhost:9333,localhost:9334,localhost:9335

I0820 14:37:17 07606 raft_server.go:134] Attempting to connect to: [http://localhost:9334/cluster/join](http://localhost:9334/cluster/join)

I0820 14:37:17 07606 raft_server.go:139] Post returned error: Post [http://localhost:9334/cluster/join](http://localhost:9334/cluster/join): dial tcp 127.0.0.1:9334: connection refused

I0820 14:37:17 07606 raft_server.go:134] Attempting to connect to: [http://localhost:9335/cluster/join](http://localhost:9335/cluster/join)

I0820 14:37:17 07606 raft_server.go:139] Post returned error: Post [http://localhost:9335/cluster/join](http://localhost:9335/cluster/join): dial tcp 127.0.0.1:9335: connection refused

I0820 14:37:17 07606 raft_server.go:78] No existing server found. Starting as leader in the new cluster.

I0820 14:37:17 07606 master_server.go:93] **[ localhost:9333 ] I am the leader!**

I0820 14:37:52 07606 raft_server_handlers.go:16] Processing incoming join. Current Leader localhost:9333 Self localhost:9333 Peers map[]

I0820 14:37:52 07606 raft_server_handlers.go:20] Command:{"name":"localhost:9334","connectionString":["http://localhost:9334"](http://localhost:9334)}

I0820 14:37:52 07606 raft_server_handlers.go:27] join command from Name localhost:9334 Connection [http://localhost:9334](http://localhost:9334)

I0820 14:38:02 07606 raft_server_handlers.go:16] Processing incoming join. Current Leader localhost:9333 Self localhost:9333 Peers map[localhost:9334:0xc20800f730]

I0820 14:38:02 07606 raft_server_handlers.go:20] Command:{"name":"localhost:9335","connectionString":["http://localhost:9335"](http://localhost:9335)}

I0820 14:38:02 07606 raft_server_handlers.go:27] join command from Name localhost:9335 Connection [http://localhost:9335](http://localhost:9335)

master2:

$ weed -v=3 master -port=9334 -mdir=./m2 -peers=localhost:9333,localhost:9334,localhost:9335 -defaultReplication=100

I0820 14:37:52 07616 file_util.go:20] Folder ./m2 Permission: -rwxrwxr-x

I0820 14:37:52 07616 topology.go:86] Using default configurations.

I0820 14:37:52 07616 master_server.go:59] Volume Size Limit is 30000 MB

I0820 14:37:52 07616 master.go:69] Start Seaweed Master 0.70 beta at 0.0.0.0:9334

I0820 14:37:52 07616 raft_server.go:50] Starting RaftServer with IP:localhost:9334:

I0820 14:37:52 07616 raft_server.go:74] Joining cluster: localhost:9333,localhost:9334,localhost:9335

I0820 14:37:52 07616 raft_server.go:134] Attempting to connect to: [http://localhost:9333/cluster/join](http://localhost:9333/cluster/join)

I0820 14:37:52 07616 raft_server.go:179] Post returned status: 200

master3:

$ weed -v=3 master -port=9335 -mdir=./m3 -peers=localhost:9333,localhost:9334,localhost:9335 -defaultReplication=100

I0820 14:38:02 07626 file_util.go:20] Folder ./m3 Permission: -rwxrwxr-x

I0820 14:38:02 07626 topology.go:86] Using default configurations.

I0820 14:38:02 07626 master_server.go:59] Volume Size Limit is 30000 MB

I0820 14:38:02 07626 master.go:69] Start Seaweed Master 0.70 beta at 0.0.0.0:9335

I0820 14:38:02 07626 raft_server.go:50] Starting RaftServer with IP:localhost:9335:

I0820 14:38:02 07626 raft_server.go:74] Joining cluster: localhost:9333,localhost:9334,localhost:9335

I0820 14:38:02 07626 raft_server.go:134] Attempting to connect to: [http://localhost:9333/cluster/join](http://localhost:9333/cluster/join)

I0820 14:38:03 07626 raft_server.go:179] Post returned status: 200

master1启动后，发现其他两个peer master尚未启动，于是将自己选为leader。master2、master3启动后，加入到以master1为leader的 master集群。

接下来我们来启动volume servers：

volume1:

$ weed -v=3 volume -port=8081 -dir=./v1 -mserver=localhost:9333 -dataCenter=dc1

I0820 14:44:29 07642 file_util.go:20] Folder ./v1 Permission: -rwxrwxr-x

I0820 14:44:29 07642 store.go:225] Store started on dir: ./v1 with 0 volumes max 7

I0820 14:44:29 07642 volume.go:136] Start Seaweed volume server 0.70 beta at 0.0.0.0:8081

I0820 14:44:29 07642 volume_server.go:70] Volume server bootstraps with master localhost:9333

I0820 14:44:29 07642 list_masters.go:18] list masters result :{"IsLeader":true,"Leader":"localhost:9333","Peers":["localhost:9334","localhost:9335"]}

I0820 14:44:29 07642 store.go:65] current master nodes is nodes:[localhost:9334 localhost:9335 localhost:9333 localhost:9333], lastNode:3

volume server的启动大致相同，volume2和volume3的输出日志这里就不详细列出了。

volume2:

$weed -v=3 volume -port=8082 -dir=./v2 -mserver=localhost:9334 -dataCenter=dc1

volume3:

$weed -v=3 volume -port=8083 -dir=./v3 -mserver=localhost:9335 -dataCenter=dc2

三个volume server启动后，我们在leader master(9333)上能看到如下日志：

I0820 14:44:29 07606 node.go:208] topo adds child dc1

I0820 14:44:29 07606 node.go:208] topo:dc1 adds child **DefaultRack**

I0820 14:44:29 07606 node.go:208] topo:dc1:DefaultRack adds child 127.0.0.1:8081

I0820 14:47:09 07606 node.go:208] topo:dc1:DefaultRack adds child 127.0.0.1:8082

I0820 14:47:21 07606 node.go:208] topo adds child dc2

I0820 14:47:21 07606 node.go:208] topo:dc2 adds child DefaultRack

I0820 14:47:21 07606 node.go:208] topo:dc2:DefaultRack adds child 127.0.0.1:8083

至此，整个weed-fs集群已经启动了。初始启动后的master会在-mdir下建立一些目录和文件：

$ ls m1

conf log snapshot

但volume在-dir下没有做任何操作，volume server会在第一次写入数据时建立相应的.idx文件和.dat文件。

**三、****基本操作：存储、获取和删除文件**

创建一个hello.txt文件，内容为"hello weed-fs!"，用于我们测试weed-fs的基本操作。weed-fs提供了HTTP REST API接口，我们可以很方便的使用其基本功能(这里客户端使用curl)。

**1、存储**

我们来将hello.txt文件存储在weed-fs文件系统中，我们通过master提供的submit API接口来完成这一操作：

$ curl -F [file=@hello.txt](mailto:file=@hello.txt) [http://localhost:9333/submit](http://localhost:9333/submit)

{"fid":"6,01fc4a422c","fileName":"hello.txt","fileUrl":"127.0.0.1:8082/6,01fc4a422c","size":39}

我们看到master给我们返回了一行json数据，其中:

fid是一个逗号分隔的字符串，按照repository中文档的说明，这个字符串应该由volume id, key uint64和cookie code构成。其中逗号前面的6就是volume id, 01fc4a422c则是key和cookie组成的串。fid是文件hello.txt在集群中的唯一ID。后续查看、获取以及删除该文件数据都需要使 用这个fid。

fileUrl是该文件在weed-fs中的一个访问地址(非唯一哦)，这里是127.0.0.1:8082/6,01fc4a422c，可以看出weed-fs在volume server2上存储了一份hello.txt的数据。

这一存储操作引发了物理volume的创建，我们可以看到volume server的-dir下发生了变化，多了很多.idx和.dat文 件：

$ ls v1 v2 v3

v1:

3.dat 3.idx 4.dat 4.idx 5.dat 5.idx

v2:

1.dat 1.idx 2.dat 2.idx 6.dat 6.idx

v3:

1.dat 1.idx 2.dat 2.idx 3.dat 3.idx 4.dat 4.idx 5.dat 5.idx 6.dat 6.idx

并且这个创建过程是在master leader的控制之下的：

I0820 15:06:02 07606 volume_growth.go:204] Created Volume 3 on topo:dc1:DefaultRack:127.0.0.1:8081

I0820 15:06:02 07606 volume_growth.go:204] Created Volume 3 on topo:dc2:DefaultRack:127.0.0.1:8083

我们从文件的size可以看出，hello.txt文件被存储在了v2和v3下的id为6的卷(6.dat和6.idx)中：

v2:

-rw-r–r– 1 tonybai tonybai 104 8月20 15:06 6.dat

-rw-r–r– 1 tonybai tonybai 16 8月20 15:06 6.idx

v3:

-rw-r–r– 1 tonybai tonybai 104 8月20 15:06 6.dat

-rw-r–r– 1 tonybai tonybai 16 8月20 15:06 6.idx

v2和v3中的6.dat是一模一样的，6.idx也是一样的（后续在做数据迁移时，这点极其重要）。

**2、****获取**

前面提到master给我们返回了一个fid:6,01fc4a422c以及fileUrl":"127.0.0.1:8082/6,01fc4a422c"。

通过这个fileUrl，我们可以获取到hello.txt的数据：

$ curl [http://127.0.0.1:8082/6,01fc4a422c](http://127.0.0.1:8082/6,01fc4a422c)

hello weed-fs!

根据我们的replication策略，hello.txt应该还存储在v3下，我们换成8083这个volume，应该也可以得到 hello.txt数据：

$ curl [http://127.0.0.1:8083/6,01fc4a422c](http://127.0.0.1:8083/6,01fc4a422c)

hello weed-fs!

如果我们通过volume1 (8081)查，应该得不到数据：

$ curl [http://127.0.0.1:8081/6,01fc4a422c](http://127.0.0.1:8081/6,01fc4a422c)

<a href=["http://127.0.0.1:8082/6,01fc4a422c"](http://127.0.0.1:8082/6,01fc4a422c)>Moved Permanently</a>.

这里似乎是重定向了。我们给curl加上重定向处理选项再试一次：

$ curl -L [http://127.0.0.1:8081/6,01fc4a422c](http://127.0.0.1:8081/6,01fc4a422c)

hello weed-fs!

居然也能得到相应数据，从volume1的日志来看，volume1也能获取到hello.txt的正确地址，并将返回重定向请求，这样curl 就能从正确的machine上获取数据了。

如果我们通过master来获取hello.txt数据，会是什么结果呢？

$ curl -L [http://127.0.0.1:9335/6,01fc4a422c](http://127.0.0.1:9335/6,01fc4a422c)

hello weed-fs!

同样master返回重定向地址，curl从volume节点获取到正确数据。我们看看master是如何返回重定向地址的？

$ curl [http://127.0.0.1:9335/6,01fc4a422c](http://127.0.0.1:9335/6,01fc4a422c)

<a href=["http://127.0.0.1:8082/6,01fc4a422c"](http://127.0.0.1:8082/6,01fc4a422c)>Moved Permanently</a>.

$ curl [http://127.0.0.1:9335/6,01fc4a422c](http://127.0.0.1:9335/6,01fc4a422c)

<a href=["http://127.0.0.1:8083/6,01fc4a422c"](http://127.0.0.1:8083/6,01fc4a422c)>Moved Permanently</a>.

可以看到master会自动均衡负载，轮询式的返回8082和8083。0.70版本以前，通过非leader master是无法得到正确结果的，只能通过leader master得到，0.70版本fix了这个问题。

**3、删除**

通过fileUrl地址直接删除hello.txt：

$ curl -X DELETE [http://127.0.0.1:8082/6,01fc4a422c](http://127.0.0.1:8082/6,01fc4a422c)

{"size":39}

操作成功后，我们再来get一下hello.txt:

$ curl -i [http://127.0.0.1:8082/6,01fc4a422c](http://127.0.0.1:8082/6,01fc4a422c)

HTTP/1.1 **404 Not Found**

Date: Thu, 20 Aug 2015 08:13:28 GMT

Content-Length: 0

Content-Type: text/plain; charset=utf-8

$ curl -i -L [http://127.0.0.1:9335/6,01fc4a422c](http://127.0.0.1:9335/6,01fc4a422c)

HTTP/1.1 301 Moved Permanently

Content-Length: 69

Content-Type: text/html; charset=utf-8

Date: Thu, 20 Aug 2015 08:13:56 GMT

Location: [http://127.0.0.1:8082/6,01fc4a422c](http://127.0.0.1:8082/6,01fc4a422c)

HTTP/1.1 **404 Not Found**

Date: Thu, 20 Aug 2015 08:13:56 GMT

Content-Length: 0

Content-Type: text/plain; charset=utf-8

可以看出，无论是直接通过volume还是间接通过master都无法获取到hello.txt了，hello.txt被成功删除了。

不过删除hello.txt后，volume server下的数据文件的size却并没有随之减小，别担心，这就是weed-fs的处理方法，这些数据删除后遗留下来的空洞需要手工清除（对数据文件 进行手工紧缩）：

$ curl ["http://localhost:9335/vol/vacuum"](http://localhost:9335/vol/vacuum)

{"Topology":{"DataCenters":[{"Free":8,"Id":"dc1","Max":14,"Racks":[{"DataNodes":[{"Free":4,"Max":7,"PublicUrl":"127.0.0.1:8081","Url":"127.0.0.1:8081","Volumes":3},{"Free":4,"Max":7,"PublicUrl":"127.0.0.1:8082","Url":"127.0.0.1:8082","Volumes":3}],”Free”:8,”Id”:”DefaultRack”,”Max”:14}]},{“Free”:1,”Id”:”dc2″,”Max”:7,”Racks”:[{"DataNodes":[{"Free":1,"Max":7,"PublicUrl":"127.0.0.1:8083","Url":"127.0.0.1:8083","Volumes":6}],”Free”:1,”Id”:”DefaultRack”,”Max”:7}]}],”Free”:9,”Max”:21,”layouts”:[{"collection":"","replication":"100","ttl":"","writables":[1,2,3,4,5,6]}]},"Version":"0.70 beta"}

紧缩后，你再查看v1, v2, v3下的文件size，真的变小了。

**四、一致性****（consistency）**

在分布式系统中，“一致性”是永恒的难题。weed-fs支持replication，其多副本的数据一致性需要保证。

weed-fs理论上采用了是一种“强一致性”的策略，即：

存储文件时，当多个副本都存储成功后，才会返回成功；任何一个副本存储失败，此次存储操作则返回失败。

删除文件时，当所有副本都删除成功后，才返回成功；任何一个副本删除失败，则此次删除操作返回失败。

我们来验证一下weed-fs是否做到了以上两点：

**1、存储的一致性保证**

我们先将volume3停掉(即dc2)，这样在replication 策略为100时，向weed-fs存储hello.txt时会发生如下结果：

$ curl -F [file=@hello.txt](mailto:file=@hello.txt) [http://localhost:9333/submit](http://localhost:9333/submit)

{"error":"Cannot grow volume group! Not enough data node found!"}

master根据100策略，需要在dc2选择一个volume存储hello.txt的副本，但dc2所有machine都down掉了，因此 没有存储空间，于是master认为此次操作无法继续进行，返回失败。这点符合存储一致性的要求。

**2、删除****的一致性保证**

恢复dc2，将hello.txt存入：

$ curl -F [file=@hello.txt](mailto:file=@hello.txt) [http://localhost:9333/submit](http://localhost:9333/submit)

{"fid":"6,04dce94a72","fileName":"hello.txt","fileUrl":"127.0.0.1:8082/6,04dce94a72","size":39}

再次停掉dc2，之后尝试删除hello.txt（通过master删除)：

$ curl -L -X DELETE [http://127.0.0.1:9333/6,04dce94a72](http://127.0.0.1:9333/6,04dce94a72)

{"error":"Deletion Failed."}

虽然返回的是delete failed，但从8082上的日志来看，似乎8082已经将hello.txt删除了：

I0820 17:32:20 07653 volume_server_handlers_write.go:53] deleting Cookie:3706276466, Id:4, Size:0, DataSize:0, Name: , Mime:

我们再从8082获取一下hello.txt：

$ curl [http://127.0.0.1:8082/6,04dce94a72](http://127.0.0.1:8082/6,04dce94a72)

结果是什么也没有返回。

从8082日志来看：

I0820 17:33:24 07653 volume_server_handlers_read.go:53] read error: File Entry Not Found. Needle 70 Memory 0 /6,04dce94a72

hello.txt的确被删除了！

这时将dc2(8083)重新启动！我们尝试从8083获取hello.txt：

$ curl [http://127.0.0.1:8083/6,04dce94a72](http://127.0.0.1:8083/6,04dce94a72)

hello weed-fs!

8083上的hello.txt依旧存在，可以被读取。

再试试通过master来获取hello.txt：

$ curl -L [http://127.0.0.1:9333/6,04dce94a72](http://127.0.0.1:9333/6,04dce94a72)

$ curl -L [http://127.0.0.1:9333/6,04dce94a72](http://127.0.0.1:9333/6,04dce94a72)

hello weed-fs!

结果是有时能返回hello.txt内容，有时不行。显然这是与master的自动负载均衡有关，返回8082这个重定向地址，则curl无法得 到结果；但若返回8083这个重定向地址，我们就可以得到hello.txt的内容。

这样来看，目前weed-fs的删除操作还无法保证强一致性。weed-fs github.com上已有若干issues(#172，#179，#182)是关于这个问题的。在大数据量(TB、PB级别)的情况下，这种不一致性最 大的问题是导致storage leak，即空间被占用而无法回收，volume将被逐个逐渐占满，期待后续的解决方案吧。

**五、目录支持**

weed-fs还支持像传统文件系统那样，将文件放在目录下管理，并通过文件路径对文件进行存储、获取和删除操作。weed-fs对目录的支持是 通过另外一个server实现的：filer server。也就是说如果想拥有对目录的支持，则必须启动一个(或若干个) filer server，并且所有的操作都要通过filer server进行。

$ weed filer -port=8888 -dir=./f1 -master=localhost:9333 -defaultReplicaPlacement=100

I0820 22:09:40 08238 file_util.go:20] Folder ./f1 Permission: -rwxrwxr-x

I0820 22:09:40 08238 filer.go:88] Start Seaweed Filer 0.70 beta at port 8888

**1、存储**

$curl -F ["filename=@hello.txt"](mailto:filename=@hello.txt) ["http://localhost:8888/foo/"](http://localhost:8888/foo/)

{"name":"hello.txt","size":39}

**2、获取**

$ curl [http://localhost:8888/foo/hello.txt](http://localhost:8888/foo/hello.txt)

hello weed-fs!

**3、查询目录文件列表**

$ curl ["http://localhost:8888/foo/?pretty=y"](http://localhost:8888/foo/?pretty=y)

{

"Directory": "/foo/",

"Files": [

{

"name": "hello.txt",

"fid": "6,067281a126"

}

],

"Subdirectories": null

}

**4、删除**

$ curl -X DELETE [http://localhost:8888/foo/hello.txt](http://localhost:8888/foo/hello.txt)

{"error":""}

再尝试获取hello.txt：

$curl [http://localhost:8888/foo/hello.txt](http://localhost:8888/foo/hello.txt)

返回空。hello.txt已被删除。

**5、****多****filer server**

weed filer server是单点，我们再来启动一个filer server。

$ weed filer -port=8889 -dir=./f2 -master=localhost:9333 -defaultReplicaPlacement=100

I0821 13:47:52 08973 file_util.go:20] Folder ./f2 Permission: -rwxrwxr-x

I0821 13:47:52 08973 filer.go:88] Start Seaweed Filer 0.70 beta at port 8889

两个filer节点间是否有协调呢？我们来测试一下：我们从8888存储一个文件，然后从8889获取这个文件：

$ curl -F ["filename=@hello.txt"](mailto:filename=@hello.txt) ["http://localhost:8888/foo/"](http://localhost:8888/foo/)

{"name":"hello.txt","size":39}

$ curl [http://localhost:8888/foo/hello.txt](http://localhost:8888/foo/hello.txt)

hello weed-fs!

$ curl [http://localhost:8889/foo/hello.txt](http://localhost:8889/foo/hello.txt)

空

从测试结果来看，二者各自独立工作，并没有任何联系，也就是说没有共享“文件full path”到"fid"的索引关系。默认情况下 filer server都是工作在standalone模式下的。

weed-fs官方给出了filer的集群方案，即使用[redis](http://redis.io)或Cassandra作为后端，在多个filer节点间共享“文件full path”到"fid"的索引关系。

我们启动一个redis-server(2.8.21)，监听在默认的6379端口。用下面命令重启两个filer server节点：

$ weed filer -port=8888 -dir=./f1 -master=localhost:9333 -defaultReplicaPlacement=100 -redis.server=localhost:6379

$ weed filer -port=8889 -dir=./f2 -master=localhost:9333 -defaultReplicaPlacement=100 -redis.server=localhost:6379

重复一下上面的测试步骤：

$ curl -F ["filename=@hello.txt"](mailto:filename=@hello.txt) ["http://localhost:8888/foo/"](http://localhost:8888/foo/)

{"name":"hello.txt","size":39}

$ curl [http://localhost:8889/foo/hello.txt](http://localhost:8889/foo/hello.txt)

hello weed-fs!

可以看到从8888存储的文件，可以被从8889获取到。

我们删除这个文件：

$ curl -X DELETE [http://localhost:8889/foo/hello.txt](http://localhost:8889/foo/hello.txt)

{"error":"Invalid fileId "}

提示error，但实际上文件已经被删除了！这块可能是个小bug(#183)。

虽然filer是集群了，但其后端的redis依旧是单点，如果考虑高可靠性，redis显然也要做好集群。

**六、****Collection**

Collection，顾名思义是“集合”，在weed-fs中，它指的是物理volume的集合。前面我们在存储文件时并没有指定 collection，因此weed-fs采用默认collection(空)。如果我们指定集合，结果会是什么样子呢？

$ curl -F [file=@hello.txt](mailto:file=@hello.txt) ["http://localhost:9333/submit?collection=picture"](http://localhost:9333/submit?collection=picture)

{"fid":"7,0c4f5dc90f","fileName":"hello.txt","fileUrl":"127.0.0.1:8083/7,0c4f5dc90f","size":39}

$ ls v1 v2 v3

v1:

3.dat 3.idx 4.dat 4.idx 5.dat 5.idx picture_7.dat picture_7.idx

v2:

1.dat 1.idx 2.dat 2.idx 6.dat 6.idx

v3:

1.dat 1.idx 2.dat 2.idx 3.dat 3.idx 4.dat 4.idx 5.dat 5.idx 6.dat 6.idx picture_7.dat picture_7.idx

可以看出volume server在自己的-dir下面建立了一个collection名字为prefix的idx和dat文件，上述例子中hello.txt被分配到 8081和8083两个volume server上，因此这两个volume server各自建立了picture_7.dat和picture_7.idx。以picture为前缀的idx和dat文件只是用来存放存储在 collection=picture的文件数据，其他数据要么存储在默认collection中，要么存储在其他名字的collection 中。

collection就好比为Windows下位驱动器存储卷起名。比如C:叫"系统盘"，D叫“程序盘”，E叫“数据盘”。这里各个 volume server下的picture_7.dat和picture_7.idx被起名为picture卷。如果还有video collection，那么它可能由各个volume server下的video_8.dat和video_8.idx。

不过由于默认情况下，weed volume的默认-max="7"，因此在实验环境下每个volume server最多在-dir下建立7个物理卷(七对.idx和.dat)。如果此时我还想建立video卷会怎么样呢？

$ curl -F [file=@hello.txt](mailto:file=@hello.txt) ["http://localhost:9333/submit?collection=video"](http://localhost:9333/submit?collection=video)

{"error":"Cannot grow volume group! Not enough data node found!"}

volume server们返回失败结果，提示无法再扩展volume了。这时你需要重启各个volume server，将-max值改大，比如100。

比如：$weed -v=3 volume -port=8083 -dir=./v3 -mserver=localhost:9335 -dataCenter=dc2 -max=100

重启后，我们再来建立video collection:

$ curl -F [file=@hello.txt](mailto:file=@hello.txt) ["http://localhost:9333/submit?collection=video"](http://localhost:9333/submit?collection=video)

{"fid":"11,0ee98ca54d","fileName":"hello.txt","fileUrl":"127.0.0.1:8083/11,0ee98ca54d","size":39}

$ ls v1 v2 v3

v1:

3.dat 4.dat 5.dat picture_7.dat video_10.dat video_11.dat video_12.dat video_13.dat video_9.dat

3.idx 4.idx 5.idx picture_7.idx video_10.idx video_11.idx video_12.idx video_13.idx video_9.idx

v2:

1.dat 1.idx 2.dat 2.idx 6.dat 6.idx video_8.dat video_8.idx

v3:

1.dat 2.dat 3.dat 4.dat 5.dat 6.dat picture_7.dat video_10.dat video_11.dat video_12.dat video_13.dat video_8.dat video_9.dat

1.idx 2.idx 3.idx 4.idx 5.idx 6.idx picture_7.idx video_10.idx video_11.idx video_12.idx video_13.idx video_8.idx video_9.idx

可以看到每个datacenter的volume server一次分配了6个volume作为video collection的存储卷。

**七、伸缩(Scaling****)**

对于分布式系统来说，Scaling是不得不考虑的问题，也是极为常见的操作。

**1、伸（scale up)**

weed-fs对“伸"的支持是很好的，我们分角色说。

【master】

master间采用的是raft协议，增加一个master，对于集群来说是最最基本的操作：

$weed -v=3 master -port=9336 -mdir=./m4 -peers=localhost:9333,localhost:9334,localhost:9335,localhost:9336 -defaultReplication=100

I0821 15:45:47 12398 file_util.go:20] Folder ./m4 Permission: -rwxrwxr-x

I0821 15:45:47 12398 topology.go:86] Using default configurations.

I0821 15:45:47 12398 master_server.go:59] Volume Size Limit is 30000 MB

I0821 15:45:47 12398 master.go:69] Start Seaweed Master 0.70 beta at 0.0.0.0:9336

I0821 15:45:47 12398 raft_server.go:50] Starting RaftServer with IP:localhost:9336:

I0821 15:45:47 12398 raft_server.go:74] Joining cluster: localhost:9333,localhost:9334,localhost:9335,localhost:9336

I0821 15:45:48 12398 raft_server.go:134] Attempting to connect to: [http://localhost:9333/cluster/join](http://localhost:9333/cluster/join)

I0821 15:45:49 12398 raft_server.go:179] Post returned status: 200

新master节点启动后，会通过raft协议自动加入到以9333为leader的master集群中。

【volume】

和master一样，volume本身就是靠master管理的，volume server之间没有什么联系，增加一个volume server要做的就是启动一个新的volume server就好了：

$ weed -v=3 volume -port=8084 -dir=./v4 -mserver=localhost:9335 -dataCenter=dc2

I0821 15:48:21 12412 file_util.go:20] Folder ./v4 Permission: -rwxrwxr-x

I0821 15:48:21 12412 store.go:225] Store started on dir: ./v4 with 0 volumes max 7

I0821 15:48:21 12412 volume.go:136] Start Seaweed volume server 0.70 beta at 0.0.0.0:8084

I0821 15:48:21 12412 volume_server.go:70] Volume server bootstraps with master localhost:9335

I0821 15:48:22 12412 list_masters.go:18] list masters result :

I0821 15:48:22 12412 list_masters.go:18] list masters result :{"IsLeader":true,"Leader":"localhost:9333","Peers":["localhost:9334","localhost:9335","localhost:9336"]}

I0821 15:48:22 12412 store.go:65] current master nodes is nodes:[localhost:9334 localhost:9335 localhost:9336 localhost:9333 localhost:9333], lastNode:4

I0821 15:48:22 12412 volume_server.go:82] Volume Server Connected with master at localhost:9333

新volume server节点启动后，同样会自动加入集群，后续master就会自动在其上存储数据了。

【filer】

前面已经谈到了，无论是standalone模式，还是distributed模式，filter都可以随意增减，这里就不再重复赘述了。

**2、缩(scale down)**

master的缩是极其简单的，只需将相应节点shutdown即可；如果master是leader，则其他master会检测到leader shutdown，并自动重新选出新leader。不过在leader选举的过程中，整个集群的服务将短暂停止，直到leader选出。

filer在standalone模式下，谈伸缩是毫无意义的；对于distributed模式下，filter节点和master节点缩的方法 一致，shutdown即可。

唯一的麻烦就是volume节点，因为数据存储在volume节点下，我们不能简单的停掉volume，我们需要考虑在不同 replication策略下是否可以做数据迁移，如何做数据迁移。这就是下一节我们要详细描述的。

**八、****数据迁移**

下面我们就来探讨一下weed-fs的volume数据迁移问题。

**1、000复制策略下的数据迁移**

为方便测试，我简化一下实验环境（一个master+3个volume）：

master:

$ weed -v=3 master -port=9333 -mdir=./m1 -defaultReplication=000

volume:

$ weed -v=3 volume -port=8081 -dir=./v1 -mserver=localhost:9333 -dataCenter=dc1

$ weed -v=3 volume -port=8082 -dir=./v2 -mserver=localhost:9333 -dataCenter=dc1

$ weed -v=3 volume -port=8083 -dir=./v3 -mserver=localhost:9333 -dataCenter=dc1

和之前一样，启动后，v1，v2，v3目录下面是空的，卷的创建要等到第一份数据存入时。000策略就是没有副本的策略，你存储的文件在 weed-fs中只有一份数据。

我们上传一份文件：

$ curl -F [filename=@hello1.txt](mailto:filename=@hello1.txt) ["http://localhost:9333/submit"](http://localhost:9333/submit)

{"fid":"1,01655ab58e","fileName":"hello1.txt","fileUrl":"127.0.0.1:8081/1,01655ab58e","size":40}

$ ll v1 v2 v3

v1:

-rw-r–r– 1 tonybai tonybai 104 8 21 21:31 1.dat

-rw-r–r– 1 tonybai tonybai 16 8 21 21:31 1.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 21:31 4.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:31 4.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 21:31 7.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:31 7.idx

v2:

-rw-r–r– 1 tonybai tonybai 8 8 21 21:31 2.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:31 2.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 21:31 3.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:31 3.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 21:31 6.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:31 6.idx

v3:

-rw-r–r– 1 tonybai tonybai 8 8 21 21:31 5.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:31 5.idx

可以看到hello1.txt被存储在v1下，同时可以看出不同的物理卷分别存放在不同节点下（由于不需要do replication）。

在这种情况(000)下，如果要将v1数据迁移到v2或v3中，只需将v1停掉，将v1下的文件mv到v2或v3中，重启volume server2或volume server3即可。

**2、001复制策略下的数据迁移**

001复制策略是weed-fs默认的复制策略，weed-fs会为每个文件在同Rack下复制一个副本。我们还利用上面的环境，不过需要停掉 weed-fs，清空目录下的文件，重启后使用，别忘了-defaultReplication=001。

我们连续存储三个文件：

$ curl -F [filename=@hello1.txt](mailto:filename=@hello1.txt) ["http://localhost:9333/submit"](http://localhost:9333/submit)

{"fid":"2,01ea84980d","fileName":"hello1.txt","fileUrl":"127.0.0.1:8082/2,01ea84980d","size":40}

$ curl -F [filename=@hello2.txt](mailto:filename=@hello2.txt) ["http://localhost:9333/submit"](http://localhost:9333/submit)

{"fid":"1,027883baa8","fileName":"hello2.txt","fileUrl":"127.0.0.1:8083/1,027883baa8","size":40}

$ curl -F [filename=@hello3.txt](mailto:filename=@hello3.txt) ["http://localhost:9333/submit"](http://localhost:9333/submit)

{"fid":"6,03220f577e","fileName":"hello3.txt","fileUrl":"127.0.0.1:8081/6,03220f577e","size":40}

可以看出三个文件分别被存储在vol2, vol1和vol6中，我们查看一下v1, v2, v3中的文件情况：

$ ll v1 v2 v3

v1:

-rw-r–r– 1 tonybai tonybai 104 8 21 22:00 1.dat

-rw-r–r– 1 tonybai tonybai 16 8 21 22:00 1.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 21:56 3.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:56 3.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 21:56 4.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:56 4.idx

-rw-r–r– 1 tonybai tonybai 104 8 21 22:02 6.dat

-rw-r–r– 1 tonybai tonybai 16 8 21 22:02 6.idx

v2:

-rw-r–r– 1 tonybai tonybai 104 8 21 21:56 2.dat

-rw-r–r– 1 tonybai tonybai 16 8 21 21:56 2.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 21:56 5.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:56 5.idx

v3:

-rw-r–r– 1 tonybai tonybai 104 8 21 22:00 1.dat

-rw-r–r– 1 tonybai tonybai 16 8 21 22:00 1.idx

-rw-r–r– 1 tonybai tonybai 104 8 21 21:56 2.dat

-rw-r–r– 1 tonybai tonybai 16 8 21 21:56 2.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 21:56 3.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:56 3.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 21:56 4.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:56 4.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 21:56 5.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 21:56 5.idx

-rw-r–r– 1 tonybai tonybai 104 8 21 22:02 6.dat

-rw-r–r– 1 tonybai tonybai 16 8 21 22:02 6.idx

假设我们现在要shutdown v3，将v3数据迁移到其他volume server，我们有3种做法：

1) 不迁移

2) 将v3下的所有文件mv到v2或v1中

3) 将v3下的所有文件先后覆盖到v1和v2中

我们来逐个分析每种做法的后果：

**1) 不迁移**

001策略下，每份数据有两个copy，v3中的数据其他两个v1+v2总是有的，因此即便不迁移，v1+v2中也会有一份数据copy。你可以 测试一下当shutdown volume3后：

$ curl -L ["http://localhost:9333/2,01ea84980d"](http://localhost:9333/2,01ea84980d)

hello weed-fs1!

$ curl -L ["http://localhost:9333/1,027883baa8"](http://localhost:9333/1,027883baa8)

hello weed-fs2!

$ curl -L ["http://localhost:9333/6,03220f577e"](http://localhost:9333/6,03220f577e)

hello weed-fs3!

针对每一份文件，你都可以多get几次，都会得到正确的结果。但此时的不足也很明显，那就是存量数据不再拥有另外一份备份。

**2) ****将v3下的所有文件mv到v2或v1中**

还是根据001策略，将v3数据mv到v2或v1中，结果会是什么呢，这里就以v3 mv到 v1举例：


- 对于v1和v3都有的卷id，比如1，两者的文件1.idx和1.dat是一模一样的。这是001策略决定的。但一旦迁移后，**系统中的数据就由2份变 成1份了**。

- 对于v1有，而v3没有的，那自然不必说了。

- 对于v1没有，而v3有的，mv过去就成为了v1的数据。

为此，这种做法依旧不够完美。

**3）将v****3下的所有文件覆盖到v1和v2中**

结合上面的方法，只有此种迁移方式才能保证迁移后，系统中的数据不丢失，且每个都是按照001策略所说的2份，这才是正确的方法。

我们来测试一下：

– 停掉volume3；

– 停掉volume1，将v3下的文件copy到v1下，启动volume1

– 停掉volume2，将v3下的文件copy到v2下，启动volume2

$ curl ["http://localhost:9333/6,03220f577e"](http://localhost:9333/6,03220f577e)

<a href=["http://127.0.0.1:8081/6,03220f577e"](http://127.0.0.1:8081/6,03220f577e)>Moved Permanently</a>.

$ curl ["http://localhost:9333/6,03220f577e"](http://localhost:9333/6,03220f577e)

<a href=["http://127.0.0.1:8082/6,03220f577e"](http://127.0.0.1:8082/6,03220f577e)>Moved Permanently</a>.

可以看到，master返回了重定向地址8081和8082，说明8083迁移到8082上的数据也生效了。

**3、100复制策略下的数据迁移**

测试环境稍作变化：

master:

$ weed -v=3 master -port=9333 -mdir=./m1 -defaultReplication=100

volume:

$ weed -v=3 volume -port=8081 -dir=./v1 -mserver=localhost:9333 -dataCenter=dc1

$ weed -v=3 volume -port=8082 -dir=./v2 -mserver=localhost:9333 -dataCenter=dc1

$ weed -v=3 volume -port=8083 -dir=./v3 -mserver=localhost:9333 -dataCenter=**dc****2**

和之前一样，我们上传三份文件：

$ curl -F [filename=@hello1.txt](mailto:filename=@hello1.txt) ["http://localhost:9333/submit"](http://localhost:9333/submit)

{"fid":"4,01d937dd30","fileName":"hello1.txt","fileUrl":"127.0.0.1:8083/4,01d937dd30","size":40}

$ curl -F [filename=@hello2.txt](mailto:filename=@hello2.txt) ["http://localhost:9333/submit"](http://localhost:9333/submit)

{"fid":"2,025efbef14","fileName":"hello2.txt","fileUrl":"127.0.0.1:8082/2,025efbef14","size":40}

$ curl -F [filename=@hello3.txt](mailto:filename=@hello3.txt) ["http://localhost:9333/submit"](http://localhost:9333/submit)

{"fid":"2,03be936488","fileName":"hello3.txt","fileUrl":"127.0.0.1:8082/2,03be936488","size":40}

$ ll v1 v2 v3

-rw-r–r– 1 tonybai tonybai 8 8 21 22:58 3.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 22:58 3.idx

-rw-r–r– 1 tonybai tonybai 104 8 21 22:58 4.dat

-rw-r–r– 1 tonybai tonybai 16 8 21 22:58 4.idx

v2:

-rw-r–r– 1 tonybai tonybai 8 8 21 22:58 1.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 22:58 1.idx

-rw-r–r– 1 tonybai tonybai 200 8 21 22:59 2.dat

-rw-r–r– 1 tonybai tonybai 32 8 21 22:59 2.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 22:58 5.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 22:58 5.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 22:58 6.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 22:58 6.idx

v3:

-rw-r–r– 1 tonybai tonybai 8 8 21 22:58 1.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 22:58 1.idx

-rw-r–r– 1 tonybai tonybai 200 8 21 22:59 2.dat

-rw-r–r– 1 tonybai tonybai 32 8 21 22:59 2.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 22:58 3.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 22:58 3.idx

-rw-r–r– 1 tonybai tonybai 104 8 21 22:58 4.dat

-rw-r–r– 1 tonybai tonybai 16 8 21 22:58 4.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 22:58 5.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 22:58 5.idx

-rw-r–r– 1 tonybai tonybai 8 8 21 22:58 6.dat

-rw-r–r– 1 tonybai tonybai 0 8 21 22:58 6.idx

由于100策略是在不同DataCenter中各保持一份copy，因此数据的迁移不应该在数据中心间进行，而同一数据中心内的迁移又回归到了 “000”策略的情形。

其他策略的分析方式也是如此，这里就不长篇大论了。

**九、Benchmark**

在HP ProLiant DL380 G4, Intel(R) Xeon(TM) CPU 3.60GHz 4核，6G内存的机器(非SSD硬盘)上，执行benchmark test:

$ weed benchmark -server=localhost:9333

This is SeaweedFS version 0.70 beta linux amd64

———— Writing Benchmark ———-

Concurrency Level: 16

Time taken for tests: 831.583 seconds

Complete requests: 1048576

Failed requests: 0

Total transferred: 1106794545 bytes

Requests per second: 1260.94 [#/sec]

Transfer rate: 1299.75 [Kbytes/sec]

Connection Times (ms)

min avg max std

Total: 2.2 12.5 1118.4 9.3

Percentage of the requests served within a certain time (ms)

50% 11.4 ms

66% 13.3 ms

75% 14.8 ms

80% 15.9 ms

90% 19.2 ms

95% 22.6 ms

98% 27.4 ms

99% 31.2 ms

100% 1118.4 ms

———— Randomly Reading Benchmark ———-

Concurrency Level: 16

Time taken for tests: 151.480 seconds

Complete requests: 1048576

Failed requests: 0

Total transferred: 1106791113 bytes

Requests per second: 6922.22 [#/sec]

Transfer rate: 7135.28 [Kbytes/sec]

Connection Times (ms)

min avg max std

Total: 0.1 2.2 116.7 3.9

Percentage of the requests served within a certain time (ms)

50% 1.6 ms

66% 2.1 ms

75% 2.5 ms

80% 2.8 ms

90% 3.7 ms

95% 4.8 ms

98% 7.4 ms

99% 11.1 ms

100% 116.7 ms

这个似乎比作者在mac笔记本(SSD)上性能还要差些，当然此次我们用的策略是100，并且这个服务器上还运行着其他程序。但即便如此，感觉weed-fs还是有较大优化的空间的。

作者在官网上将weed-fs与其他分布式文件系统如[Ceph](http://ceph.io)，hdfs等做了简要对比，强调了weed-fs相对于其他分布式文件系统的优点。

**十、其它**

weed-fs使用google glog，因此所有log的级别设置以及log定向的方法均与glog一致。

weed-fs提供了backup命令，用来在同机上备份volume server上的数据。

weed-fs没有提供官方client包，但在wiki上列出多种[第三方client包（](https://github.com/chrislusf/seaweedfs/wiki/Client-Libraries)各种语言），就Go client包来看，似乎还没有特别理想的。

weed-fs目前还没有web console，只能通过命令行进行操作。

使用weed-fs时，别忘了将open files no limit调大，否则可能会导致volume server crash。

**十一、小结**

weed-fs为想寻找开源分布式文件系统的朋友们提供了一个新选择。尤其是在存储大量小图片时，weed-fs自身就是基于haystack这一优化图 片存储的论文的。另外weed-fs使用起来的确十分简单，分分钟就可以建立起一个分布式系统，部署容易，几乎不需要什么配置。但weed-fs目前最大 的问题似乎是没有重量级的使用案例，自身也还有不少不足，但希望通过这篇文章能让更多人认识weed-fs，并使用weed-fs，帮助改善weed-fs吧。

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

总结很好

比如上传一个文本文件后能修改这个文件吗？

据我了解，至今weedfs也没有提供修改已上传的文件数据的接口啊，因此无法修改。可以先删除，再传新的。

weedfs从核心原理来看，就不是为了修改数据而存在的。更适合一次写入，大量读取，比如：小图片文件等。

看完你写的教程，真想使用weedfs，但心里还有几个疑惑：

1）fid能自己生成，然后存进去吗？

2）一个volume服务器，一次只能创建7个dat文件吗？这7个dat文件存满了，weedfs又创建7个新的 .dat 文件吗？

3）启动volume服务器时的参数，-volumeSizeLimitMB=1G，这个参数意思是这个volume服务器只能存1G的数据，还是 但个 .dat 文件的存储量？

1) fid似乎不能自己生成，只能由weedfs server生成；

2) 官方文档说法：By default, SeaweedFS grows the volumes automatically. For example, for no-replication volumes, there will be concurrently 7 writable volumes allocated.

3) volumeSizeLimitMB我没有用过，但似乎是volume的size limit。可以看看代码。

weedfs使用要慎重，尤其是在生产环境，毕竟是涉及到数据的事情。毕竟作者的更新不那么快，似乎精力有限。出现问题，如果你自己无法解决，指望作者快速响应可能很难。

谢谢你的回复和建议

反复看了你写的weedfs教程，自己琢磨了好一会，对于volume server的2个参数的概念一直没弄明白？

1）-dataCenter

2）-rank

增加这两个参数的作用是什么？

-dataCenter 直译过来还好理解，如果要加 -rank 这个参数的话，起什么作用？（在博文中你对 Collection 的概念，打的比喻就很好理解）

希望博主看到后能回复一下。

datacenter和rack(机架，注意: 不是rank哦)都是部署拓扑的概念。引入这两个概念主要是考虑到数据的安全性。Weedfs是一个分布式文件系统，分布以volume为基本单元，每一份上传到weedfs cluster上的数据都会根据master中设定的replication type来决定这份数据有多少份”副本”以及副本如何分布。而datacenter和rack作为要素也是要参与到如何分布的，也就是说决定如何分布的要素有三个：{replicationtype, datacenter, rack}。这些概念是直接映射到现实中你的weedfs cluster的部署拓扑的。datacenter和rack都可以一一映射到现实世界中的某个数据中心以及某个数据中心中的某个机架的。

哦，谢谢，有点明白了。

在用weedfs做实验的时候，想到一个问题，关于volume服务的，一个 volume server 最多能存 30G 的数据，默认分配 7 个 .dat 文件。

在不指定 collection 的前提下，这个 volume server 就只有 7 个 .dat 文件，且每个.dat 能存 4.3G 的数据。

4.3G的数据备份如果用 rsync的话要校验好久的。

要是能把一个 volume server 分成100个 .dat 小文件，一个.dat文件307MB，rsync备份也快哦。

想请教你是怎么做的，把大文件拆分几个小文件备份。

我使用的就是默认的启动配置。对数据也没有单独进行备份。使用的是默认的001，两个副本。因此无法给你建议。如果要deep into weedfs，只能去看代码了。

诶是这样吗，不是一个volume server可以有多个volumes，一个volume最多32g这样？英语不太好，理解的就这个意思。。。

嗯，我的理解：如果某个node上执行了weed volume -port=xx -dir=yy 这样的命令，启动了一个weedfs volume server实例，这个实例就是一个volume server。一个volume server的-dir路径下面是真实存储数据的文件。默认每个volume server实例最多在-dir下建立7个物理volume，即七对.idx和.dat，一对.idx和.dat构成一个物理volume。

不会golang，只能慢慢去摸索了，目前我想这样去拆分 .dat 文件，使用 collection=id%14，如果有3个 volume server 那么就能分配300个 .dat 文件，昨天实验了下，这300个 .dat 文件也不是平均分配到3个 volume server 上。

昨天还实验了一个 mount 命令，挂载的是一个本地的 filer，要是挂一个公网的 weed filer server ，不知道挂上后这个网络连接是不是一直保持的。

我还没用过weed mount。go语言很简单，一周左右就就可以把语法啥的基本学完了。

curl “http://localhost:8888/mydata/?pretty=y”时不应该显示的是目录下的文件列表吗，我测试时显示的时目录下的最后一个文件的内容，是为什么

按照官方文档，应该返回是一个包含文件列表的json。如果你的环境确实存在这样的问题，建议到github上去提一个issue。

我想问一下，我如果通过filer进行upload，那么master的replication的政策同样会保证文件的多副本吗？我目前的测试就是如果通过filer上传，会给你返回一个文件的被存储的到的url，然后这个url里面是对应的被存到的volume server，如果这个volume server 挂了，那么其他的volume server是无法找到这个file 的。。是这样吗？ 那么通过filer进行upload的话，副本应该怎么保证呢？

副本机制肯定是有的。如果通过filter upload file，如果保证filter高可用，官方wiki有段话：“When filer is used directly to upload and download files, in addition to file meta data, the filer also need to process the file content during read and write. So it’s a good idea to add multiple filer servers. Having an nginx server in front of the filer servers to load balance the requests would be a good idea.”

在使用filer的时候，当把文件目录里的文件都删除了，想要的文件夹也删掉，这个有没有好的解决方法？因为项目有好多层目录结构，似乎好像只能删除文件。

curl -H “Accept；application/json” “http://localhost:8888/data/?pretty=y”获取数据时，可不可以获取最新保存的几条数据，好像这样的方式获取的是从头开始算的数据，请问怎样可以从后面开始算起获取？

实现你的需求，好像只能通过filer API实现，详情可以看看 官方文档：https://github.com/chrislusf/seaweedfs/wiki/Filer-Server-API 中的“List files under a directory”一节。

weed-fs可以配置日志(log)的输出位置吗？比如输出到一个文件中？

开发测试环境下，可以重定向log到某个文件中。生产环境下，如果是物理二进制程序部署，可以编写systemd unit文件在os init时拉起weedfs服务，并通过journalctl查看输出日志；如果是以容器形式运行，那么weedfs的日志直接打印到stdout上，然后就要看容器日志如何收集了。

您在第十点其他说的open files no limit调大是什么意思？是在哪里调？

open files no limit 是进程可以打开的最大文件描述符数量。有soft limit和hard limit两个值。你可以google一下如何调整。

我是通过filer文件目录来保存小图片，但是发送过去保存时–地址假设是http://123.123.123.123/img/,但是输出了错误信息Post http:///dir/assign: http: no Host in request URL”，为什么会出现这样的问题呢？但是容器重启就正常了。

没碰到过这个问题，建议到weedfs github上填issue。

经过几年的发展，还是无法在生产环境中使用吗？

weedfs 在2018年11月5日发布的1.00版本，想必作者主观上觉得weedfs已经成熟了，虽然没有在release notes中明说。其实早在这之前就有很多人将weedfs用于生产环境了，但究竟填过多少坑就不得而知了。将开源项目用于生产环境，即便是该项目版本进化到3.x.x也是需要勇气和魄力的，并且做好采坑的准备。

我想问一下不同的局域网启动volume是默认共用一个机架和数据中心呢还是不同的机架和数据中心？

我理解这里的机架和数据中心都是逻辑的，是需要你自己的定义的。

您有没有一个完整的官方api文档，github上很不明确

抱歉，我手里没有类似文档。