---
title: Depth of field blur in Proun
url: http://joostdevblog.blogspot.com/2010/09/depth-of-field-blur-in-proun.html
author: Joost van Dongen
published: '2010-09-12'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Proun](http://www.proun-game.com)may not look like it with it's abstract graphics, but there is a whole lot of subtle technology working together to create the distinct visual style of the game. Perhaps the most obvious is the depth of field blur, and since I used a different technique then what is used in most games, let's have a look at that.

Depth of field blur is the effect that certain objects in an image are in focus, while others are blurred. It is used a lot in film and photography to create pretty images and to focus the viewer's attention on certain parts of an image. In Proun, the depth of field blur has two goals: one is that it makes the game look a lot better, and the other is that it helps the user to focus on the objects that are important, i.e. the ones close to the vehicle.

Since Proun has an abstract art style, judging the size and thus distance of objects is difficult. In a normal game, if you see a person, you know how large that person is compared to yourself and based on that, you also know how far away that person is. But how large is a cube in Proun compared to your own sphere? The depth of field blur greatly helps to solve this problem.

![](../../assets/ad1b91e5c6ccde37.jpg)

For a couple of years now, real-time depth of field blur has been used a lot in games. One game was way ahead of its time, though: Outcast already did it in 1999 (as that awesome game did lots of things years before anyone else).

![](../../assets/12869df4c1de6ac3.jpg)

Precise depth of field blur takes a lot of time to calculate, so as with almost everything, games have to do some kind of estimate that looks good enough. The most used solution is quite simple: first a sharp render of the scene is made, then this is copied and heavily blurred, and finally the sharp image and the blurred image are combined based on the distance to the camera.

The problem here is that most objects are slightly blurred, so something halfway between two images. Taking an average of a heavily blurred image and a sharp one is not the same as doing a smaller blur, as you can see in this image:

![](../../assets/f45aff3d11e1ddbf.jpg)

So, what would be much better, is if we could change the size of the blur based on how sharp an object should be. Ati proposed this in a paper of their's called

[Advanced Depth Of Field](http://developer.amd.com/media/gpu_assets/Scheuermann_DepthOfField.pdf). Their solution is simple: for each pixel, we take an average of a lot of samples of the vicinity, and the distance of these samples is based on the distance of the object, since that determines how sharp the object should be. This means that for slightly blurred objects, we really do a smaller blur. This works really well and allows for a much better blur. The drawback here is that this is a lot more expensive to render, so this can really only be used if you are willing to spend a lot of performance on depth of field blur.

Another problem that is addressed by ATI's paper is that sharp objects in the foreground should not leak over the background. Almost all modern games have this problem and it adds an unwanted glow around sharp objects, which makes the image look a bit washed. Even the incredibly beautiful cutscenes of Starcraft II have this problem, as you can see here:

![](../../assets/d126bd0df6853178.jpg)

One problem with ATI's technique is that it is difficult to do a lot of samples. If the blur would have been the same on the entire image, you could first do a horizontal blur and then a vertical blur. If you do 9 samples horizontally and then 9 samples vertically, then with just 18 samples in total, the result looks the same as if you would have done 81 samples in one step. Splitting horizontal and vertical is not possible with ATI's technique, so to get the same smooth blur, we would need to really do 81 samples per pixel. Way too much for good performance!

Since doing that many samples is a problem, I tried applying a noise to the samples to hide this problem. Although this work technically, it looks bad with Proun's stylised art style. Many games today use noise to hide that they don't do enough samples in something, but these games contain lots of details in the image already, so the noise does not stand out that much. In Proun however, there are hardly any small details in the image to hide the noise, so the noise becomes very visible. Therefore I removed the noise and accepted that Proun's depth of field blur looks slightly less smooth.

![](../../assets/318df5a94c0efc62.jpg)

In the end, the depth of field blur eats 90% of the total performance in Proun. Since the rest of the game is really simple to render and because depth of field blur is so important for the visual style of the game, I don't mind about that. To compensate, I did add several graphics settings: on Very High, you get 64 samples per pixel, on High 32, on Medium 16 and on Very Low there is no depth of field blur at all. Hopefully older computers are still able to run the game this way.

*(For those interested in checking the actual shader code: if you install Proun, you can see the depth of field blur shaders in the file "DofPostEffect.cg".)*

As a result of using this technique, the depth of field blur in Proun looks really smooth and precise. Nice! :)

can i modify this ?


ReplyDeletei m using exotic resolutions to play and everything looks foggy :(

It requires some modding, but it is actually not too difficult to change the size of the blur in Proun. You can find a description of how to do this here:


ReplyDeletehttp://www.ronimo-games.com/forum/viewtopic.php?f=7&t=1119