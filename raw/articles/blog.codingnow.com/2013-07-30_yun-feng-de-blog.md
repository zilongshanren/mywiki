---
title: 云风的 BLOG
url: https://blog.codingnow.com/2013/07/
published: '2013-07-30'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 给 skynet 添加 mongo driver

前段时间 [实现了 mongo 的 lua driver](http://blog.codingnow.com/2013/06/lua_mongo.html) ，做了一些基础工作后，由于工作比较忙就放下了。

这几天有同学告诉我他们在用这个了，并找到了一处 bug 。我还真是受宠若惊啊。一咬牙决定把这个东东整合到 skynet 中去。

本来觉得挺简单，做起来后发现必须把 lua-mongo 里的 socket 部分剥离开，才能替换成 [skynet 的 socket 库](http://blog.codingnow.com/2013/06/skynet_socket.html) 。

这个分离工作花了我一天的时间，结果虽然会损失一点性能，但是 mongo 的底层协议解析模块就可以独立出来。

和 skynet 的整合工作在做完这个步骤后，要轻松的多了。只需要把 socket 模块替换成 skynet 提供的即可。

注意：我们的项目暂时还没有使用 MongoDB ，所以我只实现了最基本的 mongo driver 的特性。需要有兴趣的同学帮我完善，或者，等我们的项目开始用 mongo 的话，总有一天我会自己把这些工作做完的。

有兴趣的同学可以直接 pull request 到 [lua-mongo](https://github.com/cloudwu/lua-mongo) ，我会整合新功能，并合并到 skynet 中。

目前最希望完成的是短线自动重连， replica set ，以及 write concern 这三项特性。它们应该都可以在 lua 层完成。