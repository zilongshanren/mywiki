---
title: Hello, Apollo
url: https://tonybai.com/2017/08/15/hello-apollo/
published: '2017-08-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Hello, Apollo

要说目前哪个技术领域投资最火热，莫过于[人工智能](https://en.wikipedia.org/wiki/Artificial_intelligence)。而人工智能领域中最火的(或者说之一)肯定要算上自动驾驶。自动驾驶的概念不是什么新鲜的玩意了，只是随着近两年这一波人工智能的大热，自动驾驶又被推到了风口浪尖。各大汽车厂商、互联网公司也都跃跃欲试，准备给汽车这一“历经百年的黄金平台”做一次新的“赋能”。

今年7月5日，国内搜索引擎No.1企业[百度](https://www.baidu.com)在其首届百度AI开发者大会上发布了[Apollo自动驾驶开放平台](http://apollo.auto/)，同时百度也对外宣布baidu正式从互联网公司转型为一家人工智能公司。作为“错过了移动互联网时代”的典型公司代表，百度这次押宝人工智能，我觉得也是战略上迫不得已的选择：在现有现金牛“搜索广告业务”还能带来大量利润的时候，为抓住未来那头现金牛而进行的努力。而[Apollo自动驾驶平台](https://github.com/apolloauto)恰是百度人工智能战略的重要组成部分。

[Apollo](https://en.wikipedia.org/wiki/Apollo)，阿波罗是古希腊神话中的光明之神，这个名字在西方文化中“自带光环”。提到Apollo，很多人还会想到半个多世纪前美国著名的“登月计划”。百度将其自动驾驶平台命名为Apollo，我猜测是有“借势之意”，即期望Apollo这个项目能在百度众多人工智能业务中拥有美好光明的前景。

作为技术人员，我们不能像一般媒体人员那样根据官方提供的“说辞”做宽泛的介绍，我们要与Apoll亲密接触，看看Apollo究竟是什么，究竟能做什么。这里就和大家一起来Say Hello to Apollo。

## 一、自动驾驶汽车- “百年黄金平台”的新时代赋能

在正式入门Apollo之前，还要说点“废话”。在接触Apollo之前，我从未认真思考过“汽车”这个平台，这次算是“顿悟”，虽然也算不上深刻。就我看来，汽车 是一个不可多得的“黄金平台”。作为一个平台，汽车已经有了上百年的历史，见证了人类科学技术的发展，是跨学科之集大成者。这百年多时间，任何新的、先进的民用技术都会赋能在汽车工业上。以一个长不足5米，重量不超过2t的一般家用乘用车为例，我们在其上面能看到先进的能源技术、材料技术、化工技术、电子技术、通讯技术以及精密的机械原件和组装技术等，可以说汽车为各个公司的创造力提供了展示的舞台。

就普通老百姓的衣食住行而言，汽车也是史无前例的高频使用典范，且是最直接、最贴近普通百姓生活的，这些都是飞机、火车等无法媲美的（如果非要选一个，那只有智能终端能与汽车媲美了，尤其是在集成度方面）。即便是到了科幻片中的漫天跑飞行器的时候，汽车也可能依旧是短距离交通的首选。当然届时的汽车很可能与我们此时的汽车大不相同了。随着时代的进步，汽车也在演化，日新月异的新技术、新材料、新能源对汽车的进一步赋能，因此汽车依旧是朝阳产业，这也是国际资本依旧积极群雄逐鹿汽车工业发展的根本原因了。比如：通过新能源方式赋能汽车的[特斯拉](https://www.tesla.com/)、通过无人驾驶技术赋能的Google的[waymo](https://waymo.com/)等。当然，不仅是从技术方面，从商业模式方面也有围绕着汽车这一平台创新的经典案例，典型的比如：[uber](https://www.uber.com/)、[滴滴](http://www.didichuxing.com/)等的高效出行以及近期日渐升温的共享汽车出行。

可以说，各大公司都在从自身优势出发，考虑如何为汽车这一百年黄金平台赋能。从这一点出发，我们就能大致理解百度Apollo的出现了：它是baidu结合自身的技术优势和数据优势拥抱汽车工业、为汽车做新时代赋能而迈出的重要一步。

## 二、Apollo的技术架构

Apollo是一套完整的自动驾驶技术方案，官方架构原图的截图较为模糊，这里自己画了一个简单的四层结构，每层内的模块暂未画出，因为不是本次入门的重点：

![img{512x368}](../../assets/726d33e929ea429e.png)


按照上图，apollo自动驾驶分成四层技术栈，从下到上分别为：

### 1、Reference Vehicle Platform(参考车辆平台)

自动驾驶最终都要落地到车上，因此apollo抽象了一个”参考车辆平台”层，通过电子化的方式控制车辆的行驶行为。

Note: 在开发者大会上，百度展示了由美国创业公司AutonomouStuff基于Apollo 1.0开放平台改装而成的循迹自动驾驶车，这辆车是一辆美系的

[林肯MKZ]。也就是说当前发布的Apollo适配林肯MKZ是没有问题的。但这款中型车对于普通开发者来说门槛算是稍高了。如果百度能拿出一款大众系、丰田系或至少也应该是一个本田系这样的车型，那对自动驾驶领域的开发者或者说爱好者来说，才是福利。相比而言，著名黑客[George Hotz]创立的自动驾驶技术公司[comma.ai]为其[openpilot]初始选用的车型则是Honda系的思域和CR-V，滥大街的车型，容易搞到，且低成本搞到，也容易改装。

### 2、Reference Hardware Platform（参考硬件平台）

这一层为自动驾驶汽车提供计算、感知、交互的硬件能力，包括计算单元(车载处理器设备)、GPS/IMU(惯性测量设备)、摄像头、激光雷达、声波雷达、HMI(人机接口)等。在发布的Apollo 1.0版本中，开放的硬件能力包括：计算单元、GPS/IMU(惯性测量设备)以及HMI。

### 3、Apollo open software Platform (开放软件平台）

这一层是百度Apollo 1.0开放的核心部分，见下图(蓝色的代表在apollo 1.0.0中已经开放的能力)：

![img{512x368}](../../assets/591fdb18be41cfa0.png)


从图中看到，这一层还可以分为三个子层，从下至上分别是：

- apollo kernel层

这一层是运行于硬件上面的OS，对于自动驾驶这种实时性要求特别强的领域，这里显然只能是[RTOS（实时操作系统）](https://en.wikipedia.org/wiki/Real-time_operating_system)。Apollo 1.0开放的源码中包含一个”[Apollo Kernel](https://github.com/ApolloAuto/apollo-kernel)“的项目，在这个项目下汇集着可以满足实时性需求的OS kernel。当然目前还仅有一个选择：[realtime linux kernel](https://github.com/ApolloAuto/apollo-kernel/tree/master/linux)。这是apollo基于Linux Kernel 4.4.32+realtime patch定制的一款专用linux内核。

- apollo platform层

在Kernel层的上面就是apollo的runtime framework了，提供platform级的支撑。Apollo 1.0同样也创建了一个专用项目：[apollo-platform](https://github.com/ApolloAuto/apollo-platform)，用于汇集满足apollo平台级支撑需求的platform。当前该项目下也仅提供了一种选择：[Apollo ROS](https://github.com/ApolloAuto/apollo-platform/tree/master/ros)，是基于[ROS1](http://tonybai.com/2017/08/01/hello-ros/)的Indigo版二次开发后的定制版[ROS](http://www.ros.org/)。Apollo ROS基于自动驾驶需求出发，对ROS1主要做了三方面改进：

-
为优化自动驾驶大量使用传感器引发很大的传输带宽需求， Apollo ROS改变基于socket的网络传输模式，大量采用共享内存的node间通信机制，减少传输中的数据拷贝，显著提升传输效率, 尤其是在满足一对多的传输场景下效果明显;

-
从鲁棒性出发，使用

[RTPS](https://en.wikipedia.org/wiki/RTPS)(Real-Time Publish Subscribe)服务发现协议实现完全的P2P网络拓扑，避免原ROS的以Master作为拓扑网络的中心的单点故障问题； -
使用protobuf替代原ROSmessage，提供很好的向后兼容，避免接口升级后，不同版本的模块难以兼容的问题。


其实第二点改进也是[ROS2](https://github.com/ros2/ros2/wiki)正在做的事情。关于Apollo ROS的详尽变化，可以参考前不久百度工程师的一个分享：[《Apollo代码开放框架—ROS 探索与实践》](https://mp.weixin.qq.com/s?__biz=MjM5MDE2NDU2MA==&mid=2654478221&idx=1&sn=53f5df1d719a4350a21d4e14d2e9e2f1&chksm=bd844cb28af3c5a4be0088f45b64bc80fa6f925edc2a35f9879a2638eded403bc3c4dd43022d&mpshare=1&scene=1&srcid=0802kZzer6lJe1ibMfyV9qD6&key=e1f08144dbefae2c8d5ad76bcf36a77cf0de18c05558a90d3a24c07246c613dac07d3feccf80d471856043f716c3b296aa89f2031a16dc4cb31e4351946f3c2833f7c80d131c73535d923e64f57f0df8&ascene=0&uin=MTYwMzM0NjYyMQ%3D%3D&devicetype=iMac+MacBookAir6%2C2+OSX+OSX+10.9.2+build(13C64)&version=11020201&pass_ticket=1ng4jRt2K0HxdxmyMlg58QAreBeJxJtx0gW67mmJjxAfSELvD3t27wQBjq5zittf)。

- apollo modules层

在这一层是apollo的功能modules，当前似乎依旧是基于ROS的package开发的，在github.com/ApolloAuto/apollo/modules/common/apollo_app.cc你大致能看出来一个ROS Package的开发模板。这一层提供诸如：规划(planning)、洞察(perception）、控制（control）、预测(prediction)、决策（decision)、定位等诸多功能。但Apollo 1.0仅仅开放了Control、Localization和HMI三个module，因为这三块足以构成Apollo 1.0提供的封闭场地循迹驾驶体系了。

### 4、Cloud Services(云端服务)

Apollo 1.0还开放了云端数据平台，以及唤醒万物的[DuerOS](http://dueros.baidu.com/)能力。DuerOS也是Baidu人工智能战略的重要棋子，似乎也是目前Baidu在AI方面最为成熟的、应用最广的产品。当然这一层还包括仿真、高精度地图等服务，不过目前尚未开放。

## 三、上手Apollo

买不起林肯MKZ的童鞋也不要担心，Apollo 1.0提供了一个本地仿真工具，给你一个与Apollo亲密接触的途径，让你可以在PC上肆无忌惮地玩耍，毕竟Apollo 1.0仅提供封闭场地的寻迹能力，相对简单。

我们的重点是Apollo open software Platform这一层，而这一层中，我们不关心apollo kernel，只关心Apollo ROS和三个已经开放的apollo modules。

### 1、下载release版本

截至目前为止，Apollo仅发布了一个版本：[apollo-v1.0.0](https://github.com/ApolloAuto/apollo/releases/tag/v1.0.0)，我们可以从github上将其下载到本地：

```
# wget -c https://github.com/ApolloAuto/apollo/archive/v1.0.0.tar.gz
# tar zxvf v1.0.0.tar.gz
# cd apollo-1.0.0
# ls -F
apollo_docker.sh* apollo.doxygen apollo.sh* AUTHORS.md BUILD CPPLINT.cfg
docker/ docs/ LICENSE modules/ README.md scripts/ third_party/ tools/ WORKSPACE
```


注意：我的实验环境为ubuntu 16.04.1 amd64。


### 2、本地源码构建

对于基于Apollo这个framework的开发者，Apollo官方强烈建议直接采用官方预定义好的专用docker环境(for dev)。对于爱折腾的我而言，必须要在本地做一次源码构建，即使这个体验是糟糕的，甚至最终是失败的^0^。源码构建的命令很简单，一行即可：

```
# cd apollo-1.0.0
# bash apollo.sh build
```


在这个过程中，我遇到了两个错误：

- bazel不存在

Apollo的构建依赖google出品的[bazel构建工具](https://bazel.build/)，我个人对bazel并没有什么研究，这里先装上再说：

```
# echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list
deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8
# curl https://bazel.build/bazel-release.pub.gpg | apt-key add -
% Total % Received % Xferd Average Speed Time Time Time Current
Dload Upload Total Spent Left Speed
100 3157 100 3157 0 0 3202 0 --:--:-- --:--:-- --:--:-- 3201
OK
# apt-get update && apt-get install bazel
```


- third_party/ros/setup.bash: No such file or directory

apollo的编译要依赖ros，但apollo并没有自带ros。我们需要到apollo platform那个项目中去下载Apollo ROS：

```
# wget -c https://github.com/ApolloAuto/apollo-platform/releases/download/1.0.0/ros-indigo-apollo-1.0.0.x86_64.tar.gz
# tar zxvf ros-indigo-apollo-1.0.0.x86_64.tar.gz
# cd ros
# ls -F
bin/ BUILD env.sh* etc/ include/ lib/ setup.bash setup.sh _setup_util.py* setup.zsh share/
```


将下载的ros目录copy到apollo-1.0.0/third_party下，并chmod +x third_party/ros/setup.bash。

我们再次执行bash apollo.sh build，这次执行前面的error和warning基本都消失了，apollo.sh脚本开始下载依赖包并编译：

```
# bash apollo.sh build
ROS_DISTRO was set to 'kinetic' before. Please make sure that the environment does not mix paths from different distributions.
[WARNING] ESD CAN library supplied by ESD Electronics does not exit.
[WARNING] If you need ESD CAN, please refer to third_party/can_card_library/esd_can/README.md
.
____Loading package: modules/common/util/testing
____Loading package: @com_github_grpc_grpc//
____Loading package: @google_styleguide//
____Loading package: @glog//
____Loading package: @eigen//
____Loading package: @gtest//
____Loading package: @civetweb//
____Loading package: @com_github_google_protobuf//
____Loading package: @websocketpp//
____Loading package: @curlpp//
Building on x86_64, with targets:
//tools/platforms:x86_64
//tools/platforms:aarch64
//modules/prediction:prediction
//modules/prediction:prediction_lib
... ...
//modules/common:log
//modules/canbus/proto:canbus_proto.pb
//:x86_64
//:arm64
WARNING: Running Bazel server needs to be killed, because the startup options are different.
INFO: Downloading https://github.com/google/boringssl/archive/master-with-bazel.zip via codeload.github.com: 2,750,374 bytes
INFO: Cloning https://github.com/madler/zlib: Receiving objects (3309 / 5016)
INFO: Downloading https://github.com/google/boringssl/archive/master-with-bazel.zip via codeload.github.com: 2,773,664 bytes
INFO: Cloning https://github.com/madler/zlib: Receiving objects (3314 / 5016)
INFO: Downloading https://github.com/google/boringssl/archive/master-with-bazel.zip via codeload.github.com: 2,795,584 bytes
INFO: Downloading https://github.com/google/boringssl/archive/master-with-bazel.zip via codeload.github.com: 13,504,198 bytes
INFO: Downloading https://github.com/google/boringssl/archive/master-with-bazel.zip via codeload.github.com: 13,522,008 bytes
INFO: Found 190 targets...
[34 / 41] Compiling external/com_github_google_protobuf/src/google/protobuf/compiler/java/java_message_lite.cc [for host]
[41 / 48] Compiling external/com_github_google_protobuf/src/google/protobuf/compiler/command_line_interface.cc [for host]
[157 / 163] Compiling external/com_github_google_protobuf/src/google/protobuf/compiler/javanano/javanano_enum.cc [for host]
[752 / 756] Compiling external/com_github_grpc_grpc/src/core/ext/client_config/resolver_result.c
ERROR: /root/test/apolloauto/apollo-1.0.0/modules/canbus/BUILD:32:1: Linking of rule '//modules/canbus:canbus' failed: gcc failed: error executing command /usr/bin/gcc -o bazel-out/local-dbg/bin/modules/canbus/canbus '-Wl,-rpath,$ORIGIN/../../_solib_k8/_U_S_Sthird_Uparty_Sros_Cros_Ucommon___Uthird_Uparty_Sros_Slib' ... (remaining 8 argument(s) skipped): com.google.devtools.build.lib.shell.BadExitStatusException: Process exited with status 1.
modules/canbus/main.cc:21: error: undefined reference to 'ros::init(int&, char**, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned int)'
third_party/ros/include/ros/publisher.h:107: error: undefined reference to 'ros::console::initializeLogLocation(ros::console::LogLocation*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, ros::console::levels::Level)'
... ...
collect2: error: ld returned 1 exit status
INFO: Elapsed time: 578.172s, Critical Path: 26.62s
============================
[ERROR] Build failed!
[INFO] Took 597.189 seconds
============================
```


经过漫长的等待后，还是以失败告终。并且C++的错误输出分析起来真是好痛苦，于是暂时放弃本地源码编译。

### 3、pre-specified Docker dev环境

既然apollo已经为我们准备好了pre-specified Docker dev环境，我们不妨用一下，下载和启动该环境可以用下面命令：

```
# cd apollo-1.0.0
# bash docker/scripts/dev_start.sh
```


apolloauto/apollo:dev-latest这个image超级庞大，大约有7个G左右，所以你需要耐心等待一会儿了。docker运行起来后，我们在另外一个terminal windows下可以执行下面命令切入到该docker容器内部：

```
# bash docker/scripts/dev_into.sh
root@myhost: /apollo#
```


在dev container中，我们可以来编译一下apollo源码：

```
root@myhost:/apollo# bash apollo.sh build
... ...
Copyright (c) 2017 Various License Holders. All Rights Reserved
Apollo software is built on top of various other open source software packages,
a complete list of licenses are located at https://github.com/ApolloAuto/apollo/blob/master/third_party/ACKNOWLEDGEMENT.txt
You agree to the terms of all the License Agreements.
Type 'y' or 'Y' to agree to the license agreement above, or type any other key to exit
y[WARNING] ESD CAN library supplied by ESD Electronics does not exit.
[WARNING] If you need ESD CAN, please refer to third_party/can_card_library/esd_can/README.md
____Loading package: modules/monitor/common
____Loading package: modules/common/adapters
____Loading package: modules/dreamview/conf
____Loading package: modules/control/integration_tests
____Loading package: @google_styleguide//
____Loading package: @com_github_google_protobuf//
... ...
[502 / 1,099] Compiling external/com_github_grpc_grpc/src/core/ext/transport/chttp2/transport/hpack_encoder.c
[914 / 1,524] Compiling external/com_github_grpc_grpc/src/core/ext/census/tracing.c
[1,304 / 1,527] Linking modules/canbus/vehicle/libmessage_manager_base.a
INFO: Elapsed time: 371.151s, Critical Path: 260.93s
============================
[ OK ] Build passed!
[INFO] Took 401.521 seconds
============================
```


由于dev环境中相关的依赖已经就绪，因此无需过多干预，在漫长的一段等待后，我们看到编译ok了。

### 4、运行apollo demo

在dev enviroment中或apollo:release-latest中，我们都可以运行apollo的一个寻迹小车的demo。以apollo:release-latest image环境为例：

```
// 启动基于apollo:release-latest image的apollo container（image size大约为3G，耐心等待下载）：
# cd apollo-1.0.0/
# bash docker/scripts/release_start.sh
//切入到容器中去
# bash docker/scripts/release_into.sh
root@myhost:/apollo#
```


在容器中启动HMI(human-machine interface)：

```
root@myhost:/apollo# bash scripts/hmi.sh
Start roscore...
HMI ros node service running at localhost:8887
HMI running at http://localhost:8887
root@myhostr:/apollo# rosnode list
/hmi_ros_node_service
/rosout
```


可以看到，hmi.sh脚本启动了roscore(ros master节点和相关服务）以及hmi的service，我们打开浏览器，输入：http://host_ip:8887即可看到如下场景：

![img{512x368}](../../assets/1fbf997171469808.png)


在容器内继续执行如下命令，回放小车的轨迹数据：

```
# rosbag play -l ./docs/demo_guide/demo.bag
[ INFO] [1502809442.462789096]: Opening ./docs/demo_guide/demo.bag
Waiting 0.2 seconds after advertising topics... done.
Hit space to toggle paused, or 's' to step.
[RUNNING] Bag Time: 1497125289.756657 Duration: 20.614178 / 41.613536
[RUNNING] Bag Time: 1497125289.896669 Duration: 20.754189 / 41.613536
... ...
```


我们打开hmi页面上的Debug开关，点击右上角的”Dreamview”按钮，稍后片刻，你就会在新打开的页面上看到小车仿真寻迹行驶的场景了：

![img{512x368}](../../assets/eb52ee75df12b34b.png)


最初实验时，由于没有在阿里云的防火墙打开8888端口，导致dreamview的websocket建立连接失败，

[dreamview页面始终无法显示出小车]。后经与apollo team的[ycool]在线联调才发现这个问题。这个问题的解决方法也已更新到Apollo的[FAQ]中了。

## 四、小结

Baidu为apollo项目做了一个4年的规划（见下面的roadmap），并计划在2020年实现全路网自动驾驶，这个说法似乎有意避开了自动驾驶的级别，这个2020目标到底是L4呢还是L5呢？不过无论是L4还是L5，这个目标都十分有挑战啊。

![img{512x368}](../../assets/6a1bd00301d588ec.png)


个人觉得：未来的L4、L5级别的自动驾驶一定不光光是依靠车辆自身的设备与算法，还要与道路基础设施相配合去实现。甚至是依赖车与车之间的通信才能做到全天候、全路况的自动驾驶。apollo虽然迈出了第一步，但任重道远，让我们拭目以待吧！

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论