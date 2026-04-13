---
title: 果果的百岁照
url: https://tonybai.com/2010/09/23/one-hundred-days-photos-of-my-daughter/
published: '2010-09-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 果果的百岁照

"百岁照是一种民间传统，一种在小孩100天时候拍的照片，代表了人们对孩子的祈福，希望孩子能长命百岁。" — 百度百科

在[果果](http://tonybai.com/2010/06/10/celebrate-the-first-month-of-my-daughter/)103天的时候我和LP一起带着果果去拍了一套百岁照。拍摄的过程很“艰苦”^_^:从上午9点一直持续到下午3点，其间果果睡了三次，哭了若干次，不过结果还是不错的，这不今天我和LP把照片取了回来。和我们那一代相比，现在的小孩子幸福多了。在我LP的钱包里放着我的一张儿时的照片，那是我大概五个多月时照的，似乎也是我的第一张正式照片了，起码我目前为止能找到的最早的照片就是它了（小时候身体比较虚弱，百天的时候老妈也没抱着我去照相^_^）。照片是黑白的，布景很简陋，只有一张铺着桌布的桌子，我穿着一个小背心儿，趴在桌子上，抬起小脑瓜，然后摄影师给我记录下了那一瞬间！

现在的百岁照都是按套系的，和婚纱照一样，什么版权数量、服装套数、各种册子和我叫不上来名字的物件都需要和影楼一一敲定。不过这些我一概不懂，都是LP前期和影楼谈好的，我只是出钱出力^_^。

好了，该上照片了，每套衣服挑了一张：

![](http://filer.blogbus.com/40445/40445_1285219303k.jpg)


我LP的最爱

![](http://filer.blogbus.com/40445/40445_12852188688.jpg)


小家伙儿有些倦意了

![](http://filer.blogbus.com/40445/40445_1285218899r.jpg)


小马，拍照可这累啊！

![](http://filer.blogbus.com/40445/40445_12852189149.jpg)


看，那边有帅哥！

![](http://filer.blogbus.com/40445/40445_12852188850.jpg)


果果笑得最灿烂的一张，也是我的最爱！

原版照片Size都很大，这里利用[ImageMagick](http://www.imagemagick.org/script/index.php)提供的命令convert做了缩小处理：

for img in `ls *.JPG`; do convert -resize 50%x50% $img x-$img; done

这里作[爸爸](http://tonybai.com/2010/05/11/now-i-am-a-father/)的也许个愿：愿果果一生健康快乐，平安幸福！

果果倒不一定非得成龙成凤，做个快乐健康、人格健全、善良有爱心、对社会有贡献的普通人也没什么不好的^_^。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

宝宝很可爱，祝果果健康幸福！

果果爸爸是个搞技术的。

祝果果同学健康幸福！