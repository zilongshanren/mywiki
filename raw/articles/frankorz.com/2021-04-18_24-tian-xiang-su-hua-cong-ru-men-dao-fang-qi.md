---
title: 24 天像素画从入门到放弃
url: http://frankorz.com/2021/04/18/learn-pixel-art/
author: 文章作者 猫冬
published: '2021-04-18'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

前不久十分厌学，想着是不是学废了，就想找到其他的东西学学，于是有一天周日尝试了同时入门 Blender 和 像素画。

建模其实和 Unity 用初始模型搭积木差不多，入门也还好。但是自己从小就是对美术绝缘，只有初中的时候会和其他同龄人一样照着漫画书瞎画。后来就直到现在，因此开始画像素画的时候还是十分不适应，感觉每一个点都是为无用艺术界添砖加瓦。

后来决定画像素画的契机是听[播客](https://gulugulufm.github.io/podcasts/2/)介绍到一个码农姐姐为了做游戏[坚持 100 天画像素画](https://www.douban.com/note/773573673/)，于是少年那颗不知天高地厚的心怦然地燃烧起来。

教练！我想学画画！

## 兴起

作为一个资深松鼠症患者，Steam 里早已经躺着不知道什么时候打折入手的像素画神器 “Asprite”，我原本以为一辈子再也不会下载它，这就是命运的安排吧。

很多软件能画像素画，毕竟像素画就只是由点构成的，不过好的工具能事半功倍。用习惯 PS 的美术朋友可能会选择继续用 PS 改笔触画像素画，对于我来说，功能太多的软件反而会打压我的一时兴起的兴趣，于是我跟着 [Aseprite！超方便的像素画软件初学者教程](https://www.bilibili.com/video/BV1Ax411x7Ss) 花半小时大概清楚 Aseprite 有的功能。

Aseprite 是收费的，在 [Github 开源](https://github.com/aseprite/aseprite) ，如果你想自己编译，可以参考 [[GUIDE] How to build Aseprite from source. (Aseprite free & legal)](https://www.reddit.com/r/PixelArt/comments/i387m1/guide_how_to_build_aseprite_from_source_aseprite/) 。我是在 Steam 上买的，现在看了看是 70 元，买了 Win、Mac、Linus 都能用，不需要自己分开编译，更新也会更方便些。

自己一开始跟着 Youtube 博主的视频教程入门，其中有前面 Aseprite 初学者教程的作者 [MortMort](https://www.youtube.com/channel/UCsn9MzwyPKeCE6MEGtMU4gg)、开了 [Pixel 101 系列教程](https://www.youtube.com/watch?v=51u9ZgrEThg&list=PLmac3HPrav-9UWt-ahViIZxpyQxJ2wPSH)的 [Pixel Pete](https://www.youtube.com/c/PeterMilko/featured) 等。

我喜欢看视频教程入门的原因有几点：

- 我想看他们是怎么开始构思一幅画的（像素画的型）
- 画像素画的过程（先画什么后画什么，颜色如何选择）
- 对软件的使用，如何适当地使用软件的功能更快地画出你想要的画。
- 了解像素画独有的技巧，如：像素抖动等

一开始我看的是 Pixel 101 的前几个教程，Pixel Pete 在像素极其有限的情况下很快就能画出不同的物品，让我知道精准控制地像素就能通过不同颜色影响画在人们脑海中的想象。

因此我对像素画的理解就是：易入门、精准控制少量颜色和少量像素、费时少易出货，需要的基础也比原画板绘少非常多。

由于我当前工作室的游戏就是像素风格，因此问了几位原画同事，都说像素画是最简单的，他们一开始有原画基础，临摹下像素画的画法，很快就都能上手画像素画了。

于是我决定开始 100 天像素画挑战，每天花一个小时左右鼠绘像素画。

## 学习

第一天开始画之后，我发现很多问题：

- 一个像素能表现的东西是有限的，我要决定这个像素应该表现成什么，从而决定是什么颜色。
- 像素画的分辨率十分低，阴影过渡和线条可能会非常生硬，画太多又会有色块现象。
- 像素画中颜色的数量要有限制，阴影可以用两到三个颜色过渡，太多颜色会很乱。

于是找了本书 [《Make Your Own Pixel Art》](https://nostarch.com/pixelart) 参考，这本书面对的是没绘画基础的新手，用的软件也是 Aseprite。这本书讲的非常详细，我印象最深的就是我需要先学会画出不同基本模型的光照，例如圆柱、正方体等，这些形状和光照会画之后，再将它们组合起来，创造出自己的物品或角色。

对于调色板的颜色，可以在 [Lospec](https://lospec.com/palette-list) 中选一些经典的颜色，这样我们暂时不用考虑颜色的对比、饱和度挑选等，先限制自己在调色板中用色，后期学颜色理论（Color Theory）了再自己配色。

下面是第三天时做的书中的练习，给出一个角色的剪影，我来上色。

![第三天](../../assets/00eff0e31438a558.png)


第五天我尝试画自己的角色，画布是 $ 64 × 64 $ ，主题是太空。其中用到刚学的像素抖动，星星的表示，不过有些光影的地方还是错的。

![](../../assets/3d01006bc07eaaa4.png)


于是每天画画，时不时尝试不同风格的像素画，中途还尝试了下画动画帧。每天也会用 [Eagle](https://eagle.cool/) 收集一下参考用的素材，这个软件看动画帧也非常方便。

![Eagle](../../assets/ec08e7e6a2c36aa0.png)


挑战途中，我还找了一些素材参考，其中十分有用的是风农翻译的蔚蓝主美 [Pedra Medeiros](https://www.patreon.com/saint11) 的一系列像素画教程：[saint11像素宝典](https://space.bilibili.com/7647261/article) 和 [JKLLIN](https://jkllin.zcool.com.cn/) 的[像素画学习系列](https://www.zcool.com.cn/work/ZNDM5MTM4MDA=.html)。像素宝典里面还教了很多游戏中很有用的动画帧画法，比如攻击时的准备帧、不同风格如光魔法和黑暗魔法的表现等。

如果还想深入，我十分推荐 [Michael Azzi](https://michafrar.com/) 写的 [Pixel Logic](https://pixellogicbook.com/) 这本书，B 站的物暗先生[汉化](https://www.bilibili.com/read/cv8026953/)过。这本书里面介绍了很多像素画的专有概念，还引用了很多像素游戏作为参考，如果想做一个像素游戏，你能从中获益很多。

我还经常逛逛 Twitter 的像素画标签，如：[pixelart](https://twitter.com/hashtag/pixelart)、[ドット絵](https://twitter.com/hashtag/%E3%83%89%E3%83%83%E3%83%88%E7%B5%B5)等，Artstation 的 [Pixel Art 画](https://www.artstation.com/search?q=pixel%20art&sort_by=relevance)，还有 Deviant Art 的 [Pixel Art 主题](https://www.deviantart.com/topic/pixel-art)。找到参考的同时，还能进一步找到自己**喜欢的风格**，这样可以跟着画的作者进一步了解这种风格的像素画画法。

## 放弃

直到第 24 天我决定放弃，其实还是时间的问题，回到家自己的时间也就两三个小时，有时候纠结一下颜色和参考，一堆时间就过去了，我希望把时间更多地重新放在技术上。

当然这 24 天我也是收获了不少，对像素画有了基本的了解，对颜色也开始有了那么点概念。工作中做游戏系统原型的时候都能不等美术资源，自己随便画图凑合用了 hhh。游戏开发者在学像素画的时候，也能请教下工作室中的美术，以后说不定还能靠着自己的像素画做独立开发，一箭双雕！

大家在一开始画的时候从小图画起，$ 16 × 16 $ 到 $ 64 × 64 $ 的画布就已经足够了，这样的画布也不需要绘画板，鼠绘就足够了，我相信画到一定程度，就会知道自己需不要一个绘画板了。

## 最后

本文作为学习过程的记录，希望能给读者激起学像素画的兴趣，避免走一些弯路。博主学像素画也是为了点一下独立开发的技能，虽然画的不怎么样，至少不怕画画了！

如果你对我 24 天的像素画感兴趣，可以点击下方按钮，或者博客右上角的相对应的标签查看。