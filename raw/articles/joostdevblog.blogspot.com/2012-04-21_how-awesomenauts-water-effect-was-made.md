---
title: How Awesomenauts' water effect was made
url: http://joostdevblog.blogspot.com/2012/04/i-had-lot-of-fun-writing-water-shader.html
author: Joost van Dongen
published: '2012-04-21'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com/), especially since it allowed me to use all kinds of small and subtle tricks to get exactly the right effect. Using shaders creatively to get precisely the right look is one of the things I enjoy most, but it is not a very common pleasure when developing 2D games. So I sneaked in this water effect during a weekend just because I really wanted to make it. Before I implemented this water, our artists weren't really convinced by the necessity of creating it at that point, but once they saw it, they were really happy with the look. :)

![](../../assets/62f07e57f07fc886.jpg)

There is nothing ground-breaking here, but I am quite happy with the specific combination of little tricks I used to get the best water effect for Awesomenauts, so here is a little graphical overview of how I made it!

![](../../assets/dfde9f6ca93b1985.jpg)

![](../../assets/5c4cd7b389f6f9f1.jpg)

![](../../assets/dae998620bfaec42.jpg)

![](../../assets/0d6196c864a5bd88.jpg)

(Raytracing like this in a shader is actually very similar to what I did during the research for my Master's thesis at Utrecht University. My

[Interior Mapping](http://interiormapping.oogst3d.net/)and

[volume rendering](http://www.proun-game.com/Oogst3D/index.php?file=CODING/Volumes/Volumes.txt)shaders use the same kind of concept in 3D.)

![](../../assets/694e9328bc642f69.jpg)

![](../../assets/46c1a52aaa4889ca.jpg)

![](../../assets/857250d0b0d11a96.jpg)

(Here's a link to my earlier blogpost about

[depth of field blur](http://joostdevblog.blogspot.com/2012/04/depth-of-field-blur-swiss-army-knife.html).

![](../../assets/da09a2d0e8bd9b0f.jpg)

![](../../assets/6a01d5ffd0d19b0b.jpg)

![](../../assets/200336bbb9b28ee3.jpg)

![](../../assets/72223f066b1e61de.jpg)

![](../../assets/e2814638c65b6c52.jpg)

You can see the water in action for yourself when

[Awesomenauts](http://www.awesomenauts.com/)launches on May 2nd for XBLA and PSN! Creating Awesomenauts took a long time and it has been a really big game for us to develop, but we are really happy with how the game turned out, so I can't wait to finally see whether people will actually like and play it massively!

Very nice!

ReplyDeleteI really love it, a really thorough and in depth review including a few stages I wouldn't have realized were necessary until you detailed them.


ReplyDeleteI think my favorite bit is that you did this at the weekend, on your own time. Not only did you tactfully and quietly push it to the point where your team mates could share your vision, but you also did it because you love your product. This is really awesome, particularly at this end stage development, where nobody could blame you for just wanting to get it finished and out of the door. I think that pride and passion for your own game is what makes the independent developer and this will be a huge driving factor for the success of awesomenauts. I am hopeful for a successful release :)