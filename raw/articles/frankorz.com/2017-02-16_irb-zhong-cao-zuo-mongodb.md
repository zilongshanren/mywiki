---
title: IRB 中操作 MongoDB
url: http://frankorz.com/2017/02/16/mongodb_operate_in_irb/
author: 文章作者 猫冬
published: '2017-02-16'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

又在 Coursera 里面选了门课坑自己


最近又学了很多东西，其中记不住的做笔记记下来，这篇文章是为 Ruby on Rails 运用 MongoDB 做准备。

## 基础命令

Mac 下安装 MongoDB 可以参考 [Mac下使用brew安装mongodb](http://hcysun.me/2015/11/21/Mac%E4%B8%8B%E4%BD%BF%E7%94%A8brew%E5%AE%89%E8%A3%85mongodb/)。

启动数据库

进入命令行模式

### 导入 MongoDB 提供的示例数据

[ 示例数据下载
](http://media.mongodb.org/zips.json)
在 json 文件所在的文件夹下导入数据库。

1
| % mongoimport --db test --collection zips --drop --file zips.json
|

### irb Shell 中的一些基础操作

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
| irb require 'mongo' => true Mongo::Client.new('mongodb://localhost:27017') db = D, [2017-02-16T00:06:03.651134 D, [2017-02-16T00:06:03.651314 D, [2017-02-16T00:06:03.654477 D, [2017-02-16T00:06:03.654581 D, [2017-02-16T00:06:03.654674 => #<Mongo::Client:0x70333621287660 cluster=localhost:27017> 'test') db = db.use( => #<Mongo::Client:0x70333622110940 cluster=localhost:27017>
=> "test"
D, [2017-02-16T11:11:07.299786 D, [2017-02-16T11:11:07.326259 => ["zips"] :zips].find.first db[ D, [2017-02-16T11:12:51.044213 D, [2017-02-16T11:12:51.059517 => {"_id"=>"01001", "city"=>"AGAWAM", "loc"=>[-72.622739, 42.070206], "pop"=>15338, "state"=>"MA"}
|

Win 系统下可以用 `system('cls')`

命令来清空 irb shell

Mac OS X 和 Linux 系统可以用 Ctrl + L 来清空屏幕

### 精简输出

1 2 3 4
| 2.3.3 :008 > Mongo::Logger.logger.level = ::Logger::INFO => 1 2.3.3 :009 > db[:zips].find.first => {"_id"=>"01001", "city"=>"AGAWAM", "loc"=>[-72.622739, 42.070206], "pop"=>15338, "state"=>"MA"}
|

## Create and Read

介绍 CRUD 增查改删操作的前两步操作

### "C"reate

- Select a collection on the client and call
`insert_one`

or `insert_many`

`insert_one`

: insert **one** document to collection
`insert_many`

: insert **multiple** documents to the collection

#### insert_one

1
| db[:zips].insert_one(:_id => "100",:city => "city01", :loc => [ -76.05922700000001, 39.564894], :pop => 4678,:state => "MD")
|

用 find 和 count 来搜索数据

1
| db[:zips].find(:city => "city01").count
|

插入一项数据，并且测试该项数据的存在

1 2 3 4 5 6
| :zips].insert_one(:_id => "100",:city => "city01", :loc => [ -76.05922700000001, 39.564894], :pop => 4678,:state => "MD") db[ => #<Mongo::Operation::Result:70333617635280 documents=[{"n"=>1, "ok"=>1.0}]> 2.3.3 :011 > db[:zips].find(:city => "city01").count => 1 :zips].find(:city => "city01").to_a db[ => [{"_id"=>"100", "city"=>"city01", "loc"=>[-76.059227, 39.564894], "pop"=>4678, "state"=>"MD"}]
|

#### insert_many

1 2 3 4 5 6 7 8
| db[:zips].insert_many([ { :_id => "200", :city => "city02", :loc => [ -74.05922700000001, 37.564894 ], :pop => 2000, :state => "CA" }, { :_id => "201", :city => "city03", :loc => [ -75.05922700000001, 35.564894 ], :pop => 3000, :state => "CA" } ])
|

同时插入多项数据

1 2 3 4 5 6 7 8 9 10 11 12 13
| :zips].insert_many([ db[ 2.3.3 :014 > { :_id => "200", :city => "city02", 2.3.3 :015 > :loc => [ -74.05922700000001, 37.564894 ], 2.3.3 :016 > :pop => 2000, :state => "CA" }, 2.3.3 :017 > { :_id => "201", :city => "city03", 2.3.3 :018 > :loc => [ -75.05922700000001, 35.564894 ], 2.3.3 :019 > :pop => 3000, :state => "CA" }
=> #<Mongo::BulkWrite::Result:0x007fefa58136d8 @results={"n_inserted"=>2, "n"=>2, "inserted_ids"=>["200", "201"]}> 2.3.3 :021 > db[:zips].find("city" => "city02").to_a => [{"_id"=>"200", "city"=>"city02", "loc"=>[-74.059227, 37.564894], "pop"=>2000, "state"=>"CA"}] :zips].find("city" => "city03").to_a db[ => [{"_id"=>"201", "city"=>"city03", "loc"=>[-75.059227, 35.564894], "pop"=>3000, "state"=>"CA"}]
|

### "R"ead

- find command
- find – returns a
**cursor** object – allows us to **iterate** over the selected document(s)
- Can be used with
**query** criteria

1 2 3 4 5 6 7 8 9
| db[:zips].find(:city => "BALTIMORE")
db[:zips].find.first db[:zips].find(:state => "MD").first
db[:zips].find(:state => "NY", :city => "GERMANTOWN").count
db[:zips].find.distinct(:state)
|

使用 pp (pretty-printing) 来美化命令行的输出，并且找到符合条件的第一项

1 2 3 4 5 6 7 8 9
| require 'pp' => true :zips].find(:state => "NY", :city => "GERMANTOWN").first pp db[ {"_id"=>"12526", "city"=>"GERMANTOWN", "loc"=>[-73.862451, 42.1219], "pop"=>4061, "state"=>"NY"} => {"_id"=>"12526", "city"=>"GERMANTOWN", "loc"=>[-73.862451, 42.1219], "pop"=>4061, "state"=>"NY"}
|

#### Cursor Iterations

print all

1
| db[:zips].find().each { |r| puts r }
|

pretty printing

1 2
| require 'pp' db[:zips].find().each { |r| pp r }
|

#### Projection

**Limits** the fields to return from all matching documents
- We can
**specify** inclusion or exclusion.
- _id is automatically included by default.
- true or 1: inclusive
- false or 0: exclusive

限制返回项的输出，例如只输出 `state`

属性，`_id`

是默认输出的，我们也可以取消输出 `_id`

项。

1 2 3 4
| :zips].find({:state => "MD"}).projection(state:true).first db[ => {"_id"=>"20331", "state"=>"MD"} :zips].find({:state => "MD"}).projection(state:true, _id:false).first db[ => {"state"=>"MD"}
|

## Paging

- Paging is accomplished with skip and limit
`skip(n)`

- tells mongodb that it should skip ‘n’ results
`limit(n)`

- instructs mongodb that it should limit the result length to ‘n’ results

### limit

限制搜索只有三项输出

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
| :zips].find.limit(3).each{ |r| pp r} db[ {"_id"=>"01001", "city"=>"AGAWAM", "loc"=>[-72.622739, 42.070206], "pop"=>15338, "state"=>"MA"} {"_id"=>"01002", "city"=>"CUSHMAN", "loc"=>[-72.51565, 42.377017], "pop"=>36963, "state"=>"MA"} {"_id"=>"01005", "city"=>"BARRE", "loc"=>[-72.108354, 42.409698], "pop"=>4546, "state"=>"MA"} => #<Enumerator: #<Mongo::Cursor:0x70333637935980 @view=#<Mongo::Collection::View:0x70333616708020 namespace='test.zips' @filter={} @options={"limit"=>3}>>:each>
|

### skip

跳过前三项，显示后三项

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
| :zips].find.skip(3).limit(3).each { |r| pp r} db[ {"_id"=>"01007", "city"=>"BELCHERTOWN", "loc"=>[-72.410953, 42.275103], "pop"=>10579, "state"=>"MA"} {"_id"=>"01008", "city"=>"BLANDFORD", "loc"=>[-72.936114, 42.182949], "pop"=>1240, "state"=>"MA"} {"_id"=>"01010", "city"=>"BRIMFIELD", "loc"=>[-72.188455, 42.116543], "pop"=>3706, "state"=>"MA"} => #<Enumerator: #<Mongo::Cursor:0x70333639364960 @view=#<Mongo::Collection::View:0x70333639398700 namespace='test.zips' @filter={} @options={"skip"=>3, "limit"=>3}>>:each>
|

### Sort

sort - Specifies the order in which the query returns matching documents.

`{ field: value }`


1 for Ascending, -1 for Descending.

搜索后以城市名升序输出，若改为`{:city => -1 }`

则为逆序输出。

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
| :zips].find.limit(3).sort({:city => 1 }).each { |r| pp r} db[ {"_id"=>"42601", "city"=>"AARON", "loc"=>[-85.199114, 36.812827], "pop"=>270, "state"=>"KY"} {"_id"=>"16820", "city"=>"AARONSBURG", "loc"=>[-77.387977, 40.876944], "pop"=>100, "state"=>"PA"} {"_id"=>"31794", "city"=>"ABAC", "loc"=>[-83.498867, 31.451722], "pop"=>27906, "state"=>"GA"} => #<Enumerator: #<Mongo::Cursor:0x70333639793460 @view=#<Mongo::Collection::View:0x70333626982300 namespace='test.zips' @filter={} @options={"limit"=>3, "sort"=>{"city"=>1}}>>:each>
|

## Advanced Find

Find By Criteria

- ‘lt’ & ‘gt’
- Evaluations
- Regex
- Exists
- Not
- Type

### lt and gt

lt -> less than

gt -> great than

找到城市名比「P」小的，且比「B」大的三项

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
| :zips].find(:city => {:$lt => 'P', :$gt => 'B'}).limit(3).to_a.each { |r| pp r};nil db[ {"_id"=>"01002", "city"=>"CUSHMAN", "loc"=>[-72.51565, 42.377017], "pop"=>36963, "state"=>"MA"} {"_id"=>"01005", "city"=>"BARRE", "loc"=>[-72.108354, 42.409698], "pop"=>4546, "state"=>"MA"} {"_id"=>"01007", "city"=>"BELCHERTOWN", "loc"=>[-72.410953, 42.275103], "pop"=>10579, "state"=>"MA"} => nil
|

小 Tips：

我们已经用 pp 来格式化输出了，可以在语句结尾加`;nil`

来精简额外的输出，如上所示。

### Regex

Regex – supports regular expression capabilities for pattern matching **strings** in queries.

用正则表达式匹配城市名含有 X 的项

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
| :zips].find(:city => {:$regex => 'X'}).limit(3).each {|r| pp r};nil db[ {"_id"=>"01240", "city"=>"LENOX", "loc"=>[-73.271322, 42.364241], "pop"=>5001, "state"=>"MA"} {"_id"=>"01537", "city"=>"NORTH OXFORD", "loc"=>[-71.885953, 42.16549], "pop"=>3031, "state"=>"MA"} {"_id"=>"01540", "city"=>"OXFORD", "loc"=>[-71.868677, 42.11285], "pop"=>9557, "state"=>"MA"} => nil
|

`X&`

:Displays cities ending with X

`^X`

:Displays cities starting with X

`^[A- E]`

:Displays cities that match the regex (A to E)

### $exist

Will check to see of the document exists when the boolean is **true**

mongo 中的 documents 可能会没有一些 values，我们可以用`$exist`

来找出存在相关 values 的项。

找出 `:city`

属性不为空的三项

1 2 3 4 5
| :zips].find(:city => {:$exists => true}).projection({:_id => false}).limit(3).to_a.each {|r| pp r} db[ {"city"=>"AGAWAM", "loc"=>[-72.622739, 42.070206], "pop"=>15338, "state"=>"MA"} {"city"=>"CUSHMAN", "loc"=>[-72.51565, 42.377017], "pop"=>36963, "state"=>"MA"} {"city"=>"BARRE", "loc"=>[-72.108354, 42.409698], "pop"=>4546, "state"=>"MA"} => [{"city"=>"AGAWAM", "loc"=>[-72.622739, 42.070206], "pop"=>15338, "state"=>"MA"}, {"city"=>"CUSHMAN", "loc"=>[-72.51565, 42.377017], "pop"=>36963, "state"=>"MA"}, {"city"=>"BARRE", "loc"=>[-72.108354, 42.409698], "pop"=>4546, "state"=>"MA"}]
|

### $not

`$not`

performs a logical NOT operation

Selects the documents that do not match the

找到 :pop 属性不大于9500的项

1 2 3 4 5 6 7 8 9 10 11
| :zips].find(:pop =>{'$not' => {'$gt' => 9500}}).projection({_id:false}).limit(3).to_a.each {|r| pp r};nil db[ {"city"=>"BARRE", "loc"=>[-72.108354, 42.409698], "pop"=>4546, "state"=>"MA"} {"city"=>"BLANDFORD", "loc"=>[-72.936114, 42.182949], "pop"=>1240, "state"=>"MA"} {"city"=>"BRIMFIELD", "loc"=>[-72.188455, 42.116543], "pop"=>3706, "state"=>"MA"} => nil
|

### $type

`$type`

- selects the documents where the value of the field is an instance of the specified numeric BSON type.

简而言之，`$type`

的作用就是验证相关属性的类型。这在我们不知道数据类型的时候很好用，我们可以在 [BSON Types](https://docs.mongodb.com/manual/reference/bson-types/) 页面中查看各数字代表着什么，例如 1 代表 Double 类型，2 代表 String 类型。

在下面示例中，`:state`

属性应是 String 类型，所以 `:&type => 2`

会有结果。`:&type => 1`

没有结果，是因为 `:state`

不是 Double 类型。

1 2 3 4
| :zips].find({:state=> {:$type => 2}}).first db[ => {"_id"=>"01001", "city"=>"AGAWAM", "loc"=>[-72.622739, 42.070206], "pop"=>15338, "state"=>"MA"} :zips].find({:state=> {:$type => 1}}).first db[ => nil
|

## Replace, Update and Delete

介绍 Replace 和 CRUD 的后两项操作

- replace_one
- update_one
- update_many
- delete_one
- delete_many
- upsert

### Replace

#### replace_one

replace_one – **Replace** a document in the collection according to the **specified parameters**.

替换`:_id => "101"`

项的所有信息

1 2 3 4 5 6
| :zips].insert_one(:_id => "101", :city => "citytemp", :loc => [ -76.05922700000001, 39.564894 ], :pop => 4678, :state => "MD" ) db[ => #<Mongo::Operation::Result:70126374694180 documents=[{"n"=>1, "ok"=>1.0}]> 2.3.3 :018 > db[:zips].find(:_id =>"101").replace_one(:_id => "101", :city => "city02", :loc => [ -78.22, 36.22 ], :pop => 2000, :state => "MD" ) => #<Mongo::Operation::Result:70126384942080 documents=[{"n"=>1, "nModified"=>1, "ok"=>1.0}]> 2.3.3 :019 > db[:zips].find(:_id => "101").to_a => [{"_id"=>"101", "city"=>"city02", "loc"=>[-78.22, 36.22], "pop"=>2000, "state"=>"MD"}]
|

### "U"pdate

#### update_one

update_one – **Update** a **single** document in the collection according to the **specified arguments**.

只更新单项中的属性，例如改城市名或同时更改多个属性

1 2 3 4 5 6 7 8
| :zips].find(:_id => "101").update_one(:$set => {:city => "name2"}) db[ => #<Mongo::Operation::Result:70126374531300 documents=[{"n"=>1, "nModified"=>1, "ok"=>1.0}]> 2.3.3 :023 > db[:zips].find(:_id => "101").to_a => [{"_id"=>"101", "city"=>"name2", "loc"=>[-78.22, 36.22], "pop"=>2000, "state"=>"MD"}] :zips].find(:_id => "101").update_one(:$set => {:city => "name3", :loc => [ 11.11, 11.11 ]}) db[ => #<Mongo::Operation::Result:70126373842240 documents=[{"n"=>1, "nModified"=>1, "ok"=>1.0}]> 2.3.3 :025 > db[:zips].find(:_id => "101").to_a => [{"_id"=>"101", "city"=>"name3", "loc"=>[11.11, 11.11], "pop"=>2000, "state"=>"XX"}]
|

#### update_many

update_many – **Updates single or multiple** documents in the collection according to the **specified arguments**.

更新多项属性，例如把所有州名为`MD`

的项中的州名更改为`XX`


1 2 3 4 5 6 7 8
| :zips].find(:state => 'MD').count db[ => 422 :zips].find(:state => 'MD').update_many(:$set => {:state => 'XX'}) db[ => #<Mongo::Operation::Result:70126374300980 documents=[{"n"=>422, "nModified"=>422, "ok"=>1.0}]> 2.3.3 :028 > db[:zips].find(:state => 'MD').count => 0 :zips].find(:state => 'XX').count db[ => 422
|

### "D"elete

#### delete_one

delete_one – will **delete** a **single** document in the collection according to the **specified arguments**.

删除之前添加的城市名为 `name3`

的项

1 2 3 4 5 6
| :zips].find(:city => 'name3').count db[ => 1 :zips].find(:city => 'name3').delete_one() db[ => #<Mongo::Operation::Result:70293222869840 documents=[{"n"=>1, "ok"=>1.0}]> 2.3.3 :007 > db[:zips].find(:city => 'name3').count => 0
|

#### delete_many

delete_many – **deletes single or multiple** documents in the collection according to the **specified arguments**.

删除所有州名为`XX`

的项

1 2 3 4 5 6
| :zips].find(:state => 'XX' ).count db[ => 421 :zips].find(:state => 'XX' ).delete_many() db[ => #<Mongo::Operation::Result:70293222986380 documents=[{"n"=>421, "ok"=>1.0}]> 2.3.3 :011 > db[:zips].find(:state => 'XX' ).count => 0
|

### upsert

If upsert is **true** and **no** document matches the query criteria, update() inserts a **single** document.

如果把 upsert （更新插入）设为 true，即使没有找到相关的项（条件不满足），也会执行 `update_one`

来创建一个项

1 2 3 4 5 6 7 8 9 10 11 12
| :zips].find(:city => "ODENVILLE1").count db[ => 0 :zips].find(:city => "ODENVILLE2").count db[ => 0 :zips].find(:city =>"ODENVILLE1").update_one({:$set => {:city => "ODENVILLE2"}}, :upsert => true) db[ => #<Mongo::Operation::Result:70293217700720 documents=[{"n"=>1, "nModified"=>0, "upserted"=>[{"index"=>0, "_id"=>BSON::ObjectId('58a5746b62b11bdc607226a8')}], "ok"=>1.0}]> 2.3.3 :017 > db[:zips].find(:city => "ODENVILLE1").count => 0 :zips].find(:city => "ODENVILLE2").count db[ => 1 :zips].find(:city => "ODENVILLE2").to_a db[ => [{"_id"=>BSON::ObjectId('58a5746b62b11bdc607226a8'), "city"=>"ODENVILLE2"}]
|