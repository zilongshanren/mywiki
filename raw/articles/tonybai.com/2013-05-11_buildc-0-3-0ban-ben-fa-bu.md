---
title: buildc 0.3.0版本发布
url: https://tonybai.com/2013/05/11/buildc-0-3-0-release/
published: '2013-05-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# buildc 0.3.0版本发布

自[buildc](http://tonybai.com/2011/12/08/buildc-a-building-assistant-tool-for-c-app/)正式在项目中应用以来，我们收到了许多同事针对[buildc](http://code.google.com/p/buildc)演进的意见和建议。其中确实有些易用性的问题是在最初设计时未考虑周全的，尤其是.buildc.rc中的配置，同事们对该文件的配置已经“怨声载道”了。

.buildc.rc是用来配置某开发者在开发过程中使用的第三方库所在subversion repository信息的，例如：

a_repository = ('SVN库地址', '本地缓存路径',

[

# 格式：[(“第三方库名称”, “库版本”, “特征库文件”), …]

('libevent', '2.0.10', 'lib/libevent.a'),

('instantclient', '10.2.0.5.0', 'lib/libnnz10.so'),

…

]

)

b_repository = ('SVN库地址', '本地缓存路径', [])

c_repository = ('SVN库地址', '本地缓存路径', [])

…

external_repositories = [

a_repository,

b_repository,

c_repository,

…

]

这里面需要维护最多、最频繁的就是各个repository中具备的第三方库名、版本号。开发者所开发的项目所依赖的第三方库信息发生变化，不仅仅需要修 改project下的buildc.cfg文件，还可能要修改.buildc.rc，大家维护起来确实体验不好，会多耗费一些工作量。

针对这个主要问题，我们决定对buildc进行一次较大范围的重构，重构后的版本定为[buildc 0.3.0版本](https://buildc.googlecode.com/files/buildc-0.3.0.tar.gz)。以下是buildc 0.3.0版本的主要改动点：

**一、简化.buildc.rc的配置，重新定义cache相关命令的语义**

0.3.0及以后版本的.buildc.rc只需配置repository的地址信息以及cache缓存的本地路径信息，无需再提供repository 里面具体的第三方库以及版本号信息了，这样一来，大多数情况下，project依赖的第三方库发生变更，都无需修改.buildc.rc了。

a_repository = ('SVN库地址', '本地缓存路径')

b_repository = ('SVN库地址', '本地缓存路径')

c_repository = ('SVN库地址', '本地缓存路径')

…

external_repositories = [

a_repository,

b_repository,

c_repository,

…

]

随之而变的是buildc cache相关命令的语义，0.3.0中cache相关命令的语义如下：

** buildc cache init *- 生成.buildc.repository，该文件是svn库的目录结构文件，相当于一份svn repository内部的地图，repository中存放的各种第三方库以及版本均在该文件中索引；如果该文件已经存在，命令执行的结果为：提示已存在。

** buildc cache upgrade* – 根据.buildc.rc的最新更新，重新生成.buildc.repository文件，并将该文件中所有lib本地的 Revision号置为none。该文件并不会执行本地cache的library的真实更新操作。

** buildc cache update* -

1. 如果.buildc.rc已经修改，但没有执行buildc cache upgrade，update会对比本地缓存库信息与对应的.repository文件中的同名lib信息，如果不一致，则提醒执行upgrade。

2. 如果.buildc.repository是新生成的，所有lib本地的Revision号均是none，则提示没有要更新的本地缓存库；

3. 如果某个项目已经download了自己依赖的库，那update将比对svn库中和本地库的revision差异，并下载最新库版本。并修改.buildc.repository中对应库的本地revision number。

* *buildc cache remove* – 将.buildc.repository中对应库的本地revision number都置为none，并删除本地缓存的库文件。

**二、重新定义config make的语义**

前面提到了，在执行buildc cache init时，buildc只是负责生成.repository文件，而并不真实执行库文件的下载和缓存。那何时真正下载呢？答案是在执行buildc config make时。这里颇有些“lazy evaluate”的味道，需要时再“download and cache it"。

* *buildc config make*

1. 如果.buildc.rc已经修改，但没有执行buildc cache upgrade，config make会对比本地缓存库信息与对应的.repository文件中的同名lib信息，如果不一致，则提醒执行upgrade。

2. 如果.buildc.rc是新生成的，或执行cache upgrade后的，config make会根据project对应的buildc.cfg中配置的第三方库，在.buildc.repository中查找是否存在（包括对应的版本 号），如果存在，则从subversion server端自动下载；否则提示出错。

3. 如果本地缓存中某个库文件不存在，buildc config make会检测到，并自动下载该库，并cache起来。

4. 如果subversion端某个库的svn revision号发生的更新，buildc config make会检测到，并下载最新的版本。

总之一切都是在buildc config make时来完成的，按需下载或更新，这样你甚至无需进行手工的library Cache维护。

**三、转向OO****范型**

实现buildc 0.3.0的小同事(wtz1989227@gmail.com)对OO情有独钟，因此在这个版本中，他将以前的结构化代码做了大幅度调整，并用OO的方 式进行了重构。按照wtz的思路，这次改造比较初级，OOD做得还不够充分，以后慢慢调整。实际代码中反映出来的情况也的确是这样。

**四、****buildc 0.2.3发布**

在将buildc 0.3.0代码merge到trunk之前，我创建了buildc-0.2的maintain branch，虽然理论上buildc 0.3.0在功能和配置方面与buildc 0.2.x版本是兼容的，但毕竟代码调整幅度较大。另外建议大家都转移到0.3.0这个最新版本上来，buildc-0.2分支顶多做一些bugfix， 不会再有新feature添加进去了。

昨天在发布buildc 0.3.0的同时，还发布了buildc-0.2的一个Bugfix版 – [buildc 0.2.3](https://buildc.googlecode.com/files/buildc-0.2.3.tar.gz)，该版本主要做了如下一些fix：

* 执行cache upgrade时增加对.buildc.rc中repository特征文件存在性的检查；

* 执行config make时增加对Make.rules文件是否为空的判断；

* 执行pack source时，添加VERSION文件，记录打包的上下文信息。

**五、其它**

考虑到[github](http://github.com)的活跃度远远高于[google code](http://code.google.com)，加上google code最近访问十分不稳定，因此之前就将[buildc](https://github.com/bigwhite/buildc)（还有[cbehave](https://github.com/bigwhite/cbehave)、[lcut](https://github.com/bigwhite/lcut)以及我的[实验代码库](https://github.com/bigwhite/experiments)）fork了一份到github上了，也攒攒 github上人气，因此这次buildc 0.2.3和buildc 0.3.0的代码还要发布到github上一次。git工具平时用的少，尤其是提交代码到github，这次算入门了。

* 代码远程提交

用git remote add一个github的remote repository后，就可以使用git push origin master将本地的commit推送到github上了。

* 打tag，并推送tag

— 查看Tag的git命令是git tag；

— 本地打tag，用这个命令： git tag -a v0.2.3 -m"0.2.3 released"；

— 推送Tag到remote repository：git push –tags origin master，不加–tags是无法推送tag的。

* branch操作

— 查看branch：git branch

— 创建branch：git branch buildc-0.2

— 推送branch：git push origin buildc-0.2

— 本地切换branch：git checkout buildc-0.2

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论