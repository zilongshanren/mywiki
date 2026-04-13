---
title: 使用wukong全文搜索引擎
url: https://tonybai.com/2016/12/06/an-intro-to-wukong-fulltext-search-engine/
published: '2016-12-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用wukong全文搜索引擎

近期项目中有一个全文索引和全文搜索的业务需求，组内同事在这方面都没啥经验，找一个满足我们需求的开源的[全文搜索引擎](https://en.wikipedia.org/wiki/Full-text_search)势在必行。我们这一期对全文搜索引擎的需求并不复杂，最主要的是引擎可以很好的支持中文分词、索引和搜索，并能快速实现功能。在全文搜索领域，基于[Apache lucene](https://lucene.apache.org/)的[ElasticSearch](https://github.com/elastic/elasticsearch)舍我其谁，其强大的分布式系统能力、对超大规模数据的支持、友好的Restful API以及近实时的搜索性能都是业内翘楚，并且其开发社区也是相当活跃，资料众多。但也正式由于其体量较大，我们并没有在本期项目中选择使用ElasticSearch，而是挑选了另外一个“fame”不是那么响亮的引擎：[wukong](https://github.com/huichen/wukong)。

### 一、wukong简介

wukong，是一款[golang](http://tonybai.com/tag/golang)实现的高性能、支持中文分词的全文搜索引擎。我个人觉得它最大的特点恰恰是不像ElasticSearch那样庞大和功能完备，而是可以以一个Library的形式快速集成到你的应用或服务中去，这可能也是在当前阶段选择它的最重要原因，当然其golang技术栈也是让我垂涎于它的另外一个原因:)。

第一次知道wukong，其实是在今年的[GopherChina大会](http://tonybai.com/2016/04/18/my-experience-of-gopherchina2016)上，其作者陈辉作为第一个演讲嘉宾在大会上分享了“[Go与人工智能](https://github.com/gopherchina/conference/blob/master/2016/1.1%20Go%20%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%20-%20%E9%99%88%E8%BE%89.pdf)”。在这个presentation中，chen hui详细讲解了wukong搜索引擎以及其他几个关联的开源项目，比如：[sego](https://github.com/huichen/sego)等。

在golang世界中，做full text search的可不止wukong一个。另外一个比较知名的是[bleve](https://github.com/blevesearch/bleve)，但默认情况下，bleve并不支持中文分词和搜索，需要[结合中文分词插件](http://yanyiwu.com/work/2016/04/04/bleve-gojieba.html)才能支持，比如：[gojieba](https://github.com/yanyiwu/gojieba)。

wukong基本上是陈辉一个人打造的项目，在陈辉在阿里任职期间，他将其用于阿里内部的一些项目中，但总体来说，wukong的应用还是很小众的，相关资料也不多，基本都集中在其[github站点](https://github.com/huichen/wukong)上。关于wukong源码的分析，倒是在国外站点上发现一篇：《[Code reading: wukong full-text search engine](https://ayende.com/blog/171745/code-reading-wukong-full-text-search-engine)》。

本文更多聚焦于应用wukong引擎，而不是来分析wukong代码。

### 二、全文索引和检索

#### 1、最简单的例子

我们先来看一个使用wukong引擎编写的最简单的例子：

```
//example1.go
package main
import (
"fmt"
"github.com/huichen/wukong/engine"
"github.com/huichen/wukong/types"
)
var (
searcher = engine.Engine{}
docId uint64
)
const (
text1 = `在苏黎世的FIFA颁奖典礼上，巴萨球星、阿根廷国家队队长梅西赢得了生涯第5个金球奖，继续创造足坛的新纪录`
text2 = `12月6日，网上出现照片显示国产第五代战斗机歼-20的尾翼已经涂上五位数部队编号`
)
func main() {
searcher.Init(types.EngineInitOptions{
IndexerInitOptions: &types.IndexerInitOptions{
IndexType: types.DocIdsIndex,
},
SegmenterDictionaries: "./dict/dictionary.txt",
StopTokenFile: "./dict/stop_tokens.txt",
})
defer searcher.Close()
docId++
searcher.IndexDocument(docId, types.DocumentIndexData{Content: text1}, false)
docId++
searcher.IndexDocument(docId, types.DocumentIndexData{Content: text2}, false)
searcher.FlushIndex()
fmt.Printf("%#v\n", searcher.Search(types.SearchRequest{Text: "巴萨 梅西"}))
fmt.Printf("%#v\n", searcher.Search(types.SearchRequest{Text: "战斗机 金球奖"}))
}
```


在这个例子中，我们创建的wukong engine索引了两个doc：text1和text2，建立好索引后，我们利用引擎进行关键词查询，我们来看看查询结果：

```
$go run example1.go
2016/12/06 21:40:04 载入sego词典 ./dict/dictionary.txt
2016/12/06 21:40:08 sego词典载入完毕
types.SearchResponse{Tokens:[]string{"巴萨", "梅西"}, Docs:[]types.ScoredDocument{types.ScoredDocument{DocId:0x1, Scores:[]float32{0}, TokenSnippetLocations:[]int(nil), TokenLocations:[][]int(nil)}}, Timeout:false, NumDocs:1}
types.SearchResponse{Tokens:[]string{"战斗机", "金球奖"}, Docs:[]types.ScoredDocument{}, Timeout:false, NumDocs:0}
```


可以看出当查询“巴萨 梅西”时，引擎正确匹配到了第一个文档(DocId:0×1)。而第二次查询关键词组合“战斗机 金球奖”则没有匹配到任何文档。从这个例子我们也可以看出，wukong引擎对关键词查询支持的是关键词的AND查询，只有文档中同时包含所有关键词，才能被匹配到。这也是目前wukong引擎唯一支持的一种关键词搜索组合模式。

wukong引擎的索引key是一个uint64值，我们需要保证该值的唯一性，否则将导致已创建的索引被override。

另外我们看到：在初始化IndexerInitOptions时，我们传入的IndexType是types.DocIdsIndex，这将指示engine在建立的索引和搜索结果中只保留匹配到的DocId信息，这将最小化wukong引擎对内存的占用。

如果在初始化EngineInitOptions时不给StopTokenFile赋值，那么当我们搜索”巴萨 梅西”时，引擎会将keywords分成三个关键词：”巴萨”、空格和”梅西”分别搜索并Merge结果：

```
$go run example1.go
2016/12/06 21:57:47 载入sego词典 ./dict/dictionary.txt
2016/12/06 21:57:51 sego词典载入完毕
types.SearchResponse{Tokens:[]string{"巴萨", " ", "梅西"}, Docs:[]types.ScoredDocument{}, Timeout:false, NumDocs:0}
types.SearchResponse{Tokens:[]string{"战斗机", " ", "金球奖"}, Docs:[]types.ScoredDocument{}, Timeout:false, NumDocs:0}
```


#### 2、FrequenciesIndex和LocationsIndex

wukong Engine的IndexType支持的另外两个类型是FrequenciesIndex和LocationsIndex，分别对应的是保留词频信息以及关键词在文档中出现的位置信息，这两类IndexType对内存的消耗量也是逐渐增大的，毕竟保留的信息是递增的：

当IndexType = FrequenciesIndex时：

```
$go run example1.go
2016/12/06 22:03:47 载入sego词典 ./dict/dictionary.txt
2016/12/06 22:03:51 sego词典载入完毕
types.SearchResponse{Tokens:[]string{"巴萨", "梅西"}, Docs:[]types.ScoredDocument{types.ScoredDocument{DocId:0x1, Scores:[]float32{3.0480049}, TokenSnippetLocations:[]int(nil), TokenLocations:[][]int(nil)}}, Timeout:false, NumDocs:1}
types.SearchResponse{Tokens:[]string{"战斗机", "金球奖"}, Docs:[]types.ScoredDocument{}, Timeout:false, NumDocs:0}
```


当IndexType = LocationsIndex时：

```
$go run example1.go
2016/12/06 22:04:31 载入sego词典 ./dict/dictionary.txt
2016/12/06 22:04:38 sego词典载入完毕
types.SearchResponse{Tokens:[]string{"巴萨", "梅西"}, Docs:[]types.ScoredDocument{types.ScoredDocument{DocId:0x1, Scores:[]float32{3.0480049}, TokenSnippetLocations:[]int{37, 76}, TokenLocations:[][]int{[]int{37}, []int{76}}}}, Timeout:false, NumDocs:1}
types.SearchResponse{Tokens:[]string{"战斗机", "金球奖"}, Docs:[]types.ScoredDocument{}, Timeout:false, NumDocs:0}
```


#### 3、分词对结果的影响

在前面，当不给StopTokenFile赋值时，我们初步看到了分词对搜索结果的影响。wukong的中文分词完全基于作者的另外一个开源项目[sego](https://github.com/huichen/sego)实现的。分词的准确程度直接影响着索引的建立和关键词的搜索结果。sego的词典和StopTokenFile来自于网络，如果你需要更加准确的分词结果，那么是需要你定期更新dictionary.txt和stop_tokens.txt。

举个例子，如果你的源文档内容为：”你们很感兴趣的 .NET Core 1.1 来了哦”，你的搜索关键词为：兴趣。按照我们的预期，应该可以搜索到这个源文档。但实际输出却是：

```
types.SearchResponse{Tokens:[]string{"兴趣"}, Docs:[]types.ScoredDocument{}, Timeout:false, NumDocs:0}
```


其原因就在于sego对”你们很感兴趣的 .NET Core 1.1 来了哦”这句话的分词结果是：

```
你们/r 很感兴趣/l 的/uj /x ./x net/x /x core/x /x 1/x ./x 1/x /x 来/v 了/ul 哦/zg
```


sego并没有将“兴趣”分出来，而是将“很感兴趣”四个字放在了一起，wukong引擎自然就不会单独为“兴趣”单独建立文档索引了，搜索不到也就能理解了。因此，sego可以被用来检验wukong引擎分词情况，这将有助于你了解wukong对文档索引的建立情况。

### 三、持久化索引和启动恢复

上面的例子中，wukong引擎建立的文档索引都是存放在内存中的，程序退出后，这些数据也就随之消失了。每次启动程序都要根据源文档重新建立索引显然是一个很不明智的想法。wukong支持将已建立的索引持久化到磁盘文件中，并在程序重启时从文件中间索引数据恢复出来，并在后续的关键词搜索时使用。wukong底层支持两种持久化引擎，一个是[boltdb](https://github.com/boltdb/bolt)，另外一个是[cznic/kv](https://github.com/cznic/kv)。默认采用boltdb。

我们来看一个持久化索引的例子(考虑文章size，省略一些代码)：

```
// example2_index_create.go
... ...
func main() {
searcher.Init(types.EngineInitOptions{
IndexerInitOptions: &types.IndexerInitOptions{
IndexType: types.DocIdsIndex,
},
UsePersistentStorage: true,
PersistentStorageFolder: "./index",
SegmenterDictionaries: "./dict/dictionary.txt",
StopTokenFile: "./dict/stop_tokens.txt",
})
defer searcher.Close()
os.MkdirAll("./index", 0777)
docId++
searcher.IndexDocument(docId, types.DocumentIndexData{Content: text1}, false)
docId++
searcher.IndexDocument(docId, types.DocumentIndexData{Content: text2}, false)
docId++
searcher.IndexDocument(docId, types.DocumentIndexData{Content: text3}, false)
searcher.FlushIndex()
log.Println("Created index number:", searcher.NumDocumentsIndexed())
}
```


这是一个创建持久化索引的源文件。可以看出：如果要持久化索引，只需在engine init时显式设置UsePersistentStorage为true，并设置PersistentStorageFolder，即索引持久化文件存放的路径。执行一下该源文件：

```
$go run example2_index_create.go
2016/12/06 22:41:49 载入sego词典 ./dict/dictionary.txt
2016/12/06 22:41:53 sego词典载入完毕
2016/12/06 22:41:53 Created index number: 3
```


执行后，我们会在./index路径下看到持久化后的索引数据文件：

```
$tree index
index
├── wukong.0
├── wukong.1
├── wukong.2
├── wukong.3
├── wukong.4
├── wukong.5
├── wukong.6
└── wukong.7
0 directories, 8 files
```


现在我们再建立一个程序，该程序从持久化的索引数据恢复索引到内存中，并针对搜索关键词给出搜索结果：

```
// example2_index_search.go
... ...
var (
searcher = engine.Engine{}
)
func main() {
searcher.Init(types.EngineInitOptions{
IndexerInitOptions: &types.IndexerInitOptions{
IndexType: types.DocIdsIndex,
},
UsePersistentStorage: true,
PersistentStorageFolder: "./index",
SegmenterDictionaries: "./dict/dictionary.txt",
StopTokenFile: "./dict/stop_tokens.txt",
})
defer searcher.Close()
searcher.FlushIndex()
log.Println("recover index number:", searcher.NumDocumentsIndexed())
fmt.Printf("%#v\n", searcher.Search(types.SearchRequest{Text: "巴萨 梅西"}))
}
```


执行这个程序：

```
$go run example2_index_search.go
2016/12/06 22:48:37 载入sego词典 ./dict/dictionary.txt
2016/12/06 22:48:41 sego词典载入完毕
2016/12/06 22:48:42 recover index number: 3
types.SearchResponse{Tokens:[]string{"巴萨", "梅西"}, Docs:[]types.ScoredDocument{types.ScoredDocument{DocId:0x1, Scores:[]float32{0}, TokenSnippetLocations:[]int(nil), TokenLocations:[][]int(nil)}}, Timeout:false, NumDocs:1}
```


该程序成功从前面已经建立好的程序中恢复了索引数据，并针对Search request给出了正确的搜索结果。

需要注意的是：boltdb采用了flock保证互斥访问底层文件数据的，因此当一个程序打开了boltdb，此时如果有另外一个程序尝试打开相同的boltdb，那么后者将阻塞在open boltdb的环节。

### 四、动态增加和删除索引

wukong引擎支持运行时动态增删索引，并实时影响搜索结果。

我们以上一节建立的持久化索引为基础，启动一个支持索引动态增加的程序：

```
//example3.go
func main() {
searcher.Init(types.EngineInitOptions{
IndexerInitOptions: &types.IndexerInitOptions{
IndexType: types.DocIdsIndex,
},
UsePersistentStorage: true,
PersistentStorageFolder: "./index",
PersistentStorageShards: 8,
SegmenterDictionaries: "./dict/dictionary.txt",
StopTokenFile: "./dict/stop_tokens.txt",
})
defer searcher.Close()
searcher.FlushIndex()
log.Println("recover index number:", searcher.NumDocumentsIndexed())
docId = searcher.NumDocumentsIndexed()
os.MkdirAll("./source", 0777)
go func() {
for {
var paths []string
//update index dynamically
time.Sleep(time.Second * 10)
var path = "./source"
err := filepath.Walk(path, func(path string, f os.FileInfo, err error) error {
if f == nil {
return err
}
if f.IsDir() {
return nil
}
fc, err := ioutil.ReadFile(path)
if err != nil {
fmt.Println("read file:", path, "error:", err)
}
docId++
fmt.Println("indexing file:", path, "... ...")
searcher.IndexDocument(docId, types.DocumentIndexData{Content: string(fc)}, true)
fmt.Println("indexed file:", path, " ok")
paths = append(paths, path)
return nil
})
if err != nil {
fmt.Printf("filepath.Walk() returned %v\n", err)
return
}
for _, p := range paths {
err := os.Remove(p)
if err != nil {
fmt.Println("remove file:", p, " error:", err)
continue
}
fmt.Println("remove file:", p, " ok!")
}
if len(paths) != 0 {
// 等待索引刷新完毕
fmt.Println("flush index....")
searcher.FlushIndex()
fmt.Println("flush index ok")
}
}
}()
for {
var s string
fmt.Println("Please input your search keywords:")
fmt.Scanf("%s", &s)
if s == "exit" {
break
}
fmt.Printf("%#v\n", searcher.Search(types.SearchRequest{Text: s}))
}
}
```


example3这个程序启动了一个goroutine，定期到source目录下读取要建立索引的源文档，并实时更新索引数据。main routine则等待用户输入关键词，并通过引擎搜索返回结果。我们来Run一下这个程序：

```
$go run example3.go
2016/12/06 23:07:17 载入sego词典 ./dict/dictionary.txt
2016/12/06 23:07:21 sego词典载入完毕
2016/12/06 23:07:21 recover index number: 3
Please input your search keywords:
梅西
types.SearchResponse{Tokens:[]string{"梅西"}, Docs:[]types.ScoredDocument{types.ScoredDocument{DocId:0x1, Scores:[]float32{0}, TokenSnippetLocations:[]int(nil), TokenLocations:[][]int(nil)}}, Timeout:false, NumDocs:1}
Please input your search keywords:
战斗机
types.SearchResponse{Tokens:[]string{"战斗机"}, Docs:[]types.ScoredDocument{types.ScoredDocument{DocId:0x2, Scores:[]float32{0}, TokenSnippetLocations:[]int(nil), TokenLocations:[][]int(nil)}}, Timeout:false, NumDocs:1}
Please input your search keywords:
```


可以看到：基于当前已经恢复的索引，我们可以正确搜索到”梅西”、”战斗机”等关键词所在的文档。

这时我们如果输入：“球王”，我们得到的搜索结果如下：

```
Please input your search keywords:
球王
types.SearchResponse{Tokens:[]string{"球王"}, Docs:[]types.ScoredDocument{}, Timeout:false, NumDocs:0}
```


没有任何文档得以匹配。

没关系，现在我们就来增加一个文档，里面包含球王等关键字。我们创建一个文档: soccerking.txt，内容为：

```
《球王马拉多纳》是一部讲述世界上被公认为现代足球坛上最伟大的传奇足球明星迭戈·马拉多纳的影片。他出身于清贫家庭，九岁展露过人才华，十一岁加入阿根廷足球青少年队，十六岁便成为阿根廷甲级联赛最年轻的>球员。1986年世界杯，他为阿根廷队射入足球史上最佳入球，并带领队伍勇夺金杯。他的一生充满争议、大起大落，球迷与人们对他的热爱却从未减少过，生命力旺盛的他多次从人生谷底重生。
```


将soccerking.txt移动到source目录中，片刻后，可以看到程序输出以下日志：

```
indexing file: source/soccerking.txt ... ...
indexed file: source/soccerking.txt ok
remove file: source/soccerking.txt ok!
flush index....
flush index ok
```


我们再尝试搜索”球王”、”马拉多纳”等关键词：

```
Please input your search keywords:
球王
types.SearchResponse{Tokens:[]string{"球王"}, Docs:[]types.ScoredDocument{types.ScoredDocument{DocId:0x4, Scores:[]float32{0}, TokenSnippetLocations:[]int(nil), TokenLocations:[][]int(nil)}}, Timeout:false, NumDocs:1}
Please input your search keywords:
马拉多纳
types.SearchResponse{Tokens:[]string{"马拉多纳"}, Docs:[]types.ScoredDocument{types.ScoredDocument{DocId:0x4, Scores:[]float32{0}, TokenSnippetLocations:[]int(nil), TokenLocations:[][]int(nil)}}, Timeout:false, NumDocs:1}
```


可以看到，这回engine正确搜索到了对应的Doc。

### 五、分布式索引和搜索

从前面的章节内容，我们大致了解了wukong的工作原理。wukong将索引存储于boltdb中，每个wukong instance独占一份数据，无法共享给其他wukong instance。当一个node上的内存空间不足以满足数据量需求时，需要将wukong引擎进行分布式部署以实现分布式索引和搜索。关于这点，wukong官方提供了一段方案描述：

```
分布式搜索的原理如下：
当文档数量较多无法在一台机器内存中索引时，可以将文档按照文本内容的hash值裂分(sharding)，不同块交由不同服务器索引。在查找时同一请求分发到所有裂分服务器上，然后将所有服务器返回的
结果归并重排序作为最终搜索结果输出。
为了保证裂分的均匀性，建议使用Go语言实现的Murmur3 hash函数:
https://github.com/huichen/murmur
按照上面的原理很容易用悟空引擎实现分布式搜索（每个裂分服务器运行一个悟空引擎），但这样的分布式系统多数是高度定制的，比如任务的调度依赖于分布式环境，有时需要添加额外层的服务器以
均衡负载
```


实质就是索引和搜索的分片处理。目前我们项目所在阶段尚不需这样一个分布式wukong，因此，这里也没有实战经验可供分享。

### 六、wukong引擎的局限

有了上面的内容介绍，你基本可以掌握和使用wukong引擎了。不过在选用wukong引擎之前，你务必要了解wukong引擎的一些局限：

1、开发不活跃，资料较少，社区较小

wukong引擎基本上是作者一个人的项目，社区参与度不高，资料很少。另外由于作者正在创业，[忙于造轮子](http://mp.weixin.qq.com/s?__biz=MjM5ODIzNDQ3Mw==&mid=2649966152&idx=1&sn=af685139039907fddcd73cab2b63f03f&chksm=beca364e89bdbf5854e3e517fc49577e3d322ef0bb1cc5a38ab47f5971f1149e18462a98e261&scene=2&srcid=0921VP415Bn6DTcmMLLWVqQ6&from=timeline&isappinstalled=0#wechat_redirect)^_^，因此wukong项目更新的频度不高。

2、缺少计划和愿景

似乎作者并没有持续将wukong引擎持续改进和发扬光大的想法和动力。Feature上也无增加。这点和bleve比起来就要差很多。

3、查询功能简单，仅支持关键词的AND查询

如果你要支持灵活多样的全文检索的查询方式，那么当前版本的wukong很可能不适合你。

4、搜索的准确度基于dictionary.txt的规模

前面说过，wukong的索引建立和搜索精确度一定程度上取决于分词引擎的分词精确性，这样dictionary.txt文件是否全面，就会成为影响搜索精确度的重要因素。

5、缺少将索引存储于关系DB中的插件支持

当前wukong引擎只能将索引持久化存储于文件中，尚无法和MySQL这样的数据库配合索引的存储和查询。

总之，wukong绝非一个完美的全文搜索引擎，是否选用，要看你所处的context。

### 七、小结

选用wukong引擎和我们的项目目前所处的context情况不无关系：我们需要快速实现出一个功能简单却可用的全文搜索服务。也许在后续版本中，对查询方式、数据规模有进一步要求时，就是可能考虑更换引擎的时刻了。bleve、elasticsearch到时候就都会被我们列为考虑对象了。

本文代码在可在[这里](https://github.com/bigwhite/experiments/tree/master/wukong)下载。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

沙发