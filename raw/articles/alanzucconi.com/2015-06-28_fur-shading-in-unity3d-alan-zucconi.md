---
title: Fur shading in Unity3D - Alan Zucconi
url: https://www.alanzucconi.com/2015/06/28/fur-shading-in-unity3d/
author: Alan Zucconi
published: '2015-06-28'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

## 💖 Support this blog

## Comments

### 18 responses to “Fur shading in Unity3D”

-
![Strakh avatar](../../assets/dd1b081c27f69afe.jpg)

Do I have to wait until the payment clears for it to work on here? It says pending in my patron account info, but I am subscribed and it says I have access to everything on your patron. The refresh button doesn’t seem to do anything after I click allow.

-
![Alan Zucconi avatar](../../assets/98460c412545b8dd.png)

I’m replying to this on Patreon!


-
-
![Mingtong avatar](../../assets/d4389719b8ff3f2f.jpg)

Hello Alan! I’ve joined your Patreon member for this fur shader. But seems only part1 and part2 are available?? How could I get access to the rest 4 parts? Thank you very much!!

-
![Alan Zucconi avatar](../../assets/98460c412545b8dd.png)

The fur shading tutorial was actually one of my very first ones (as you can see it dates back to 2015! 👴). As such it is not as polished as some of the most recent ones!

In fact, I did forget to update the links! If you visit the page now, all of the links should be now working (and a few typos have been corrected as well!). The fur shading article was originally part of “A Gentle Introduction to Shaders”, but was later taken out because it was too technical. All of the other bits, however, are accessible!

I hope this helps!


-
-
![Melvin avatar](../../assets/04ead1f40cfc810e.png)

Hi! I’m struggling to get the shader to work. I keep getting the error “Surface shader vertex function ‘vertexProgram’ not found at line 41”. This error is repeated for line 49 as well.

I’m definitely new to programming shaders, so I apologize for the trouble!

-
![Melvin avatar](../../assets/04ead1f40cfc810e.png)

So I took a programming tutorial between my previous post and now. I solved my issue by 1) downgrading from URP to the default rendering pipeline 2) changing the name of the vert function in FurHelpers.cginc to vertexProgram and 3) changing the last line of code in the FurHelpers.cginc file


to: o.Alpha *= saturate(alpha);

from: o.Alpha *= alpha;

This clamped the oversaturated output Alpha to display a value only between 0 and 1, which I found to solve the problem.I couldn’t figure out how to add the code from the section “Final fur thickness”. No matter what I did, the interpolation function seemed to do nothing.

I may have been expecting too much from this shader/tutorial, but I think there are other free alternatives online that are better and easier to follow.

-
![Alan Zucconi avatar](../../assets/98460c412545b8dd.png)

Hi Melvin, I’ve just seen this comment!


This was one of my first tutorials, written back in 2015.

I am sorry to hear a few things did not work straight away in the most recent version of Unity. I upgrade the tutorials periodically (and I sadly spend a lot of time doing it!) with so many recent changes to the rendering pipelines, it is hard to keep up!I hope you will find some of the newer shader tutorials much easier to follow!

-
![Melvin avatar](../../assets/04ead1f40cfc810e.png)

Oops! So sorry, Alan Zucconi, I wish I could edit my previous comment! I reread it and I certainly did not mean to come off as petty or spread misinformation.

I definitely wanted to add/change some things on my previous comment:

1) I could not find alternate fur tutorials that were better, clearer, or free in any regard. This is most likely the best tutorial given the cost and yielded effect. Albeit, it’s a bit hard to follow. For shader novices like me, I definitely would recommend taking/following a shader course/series or reading Alan Zucconi’s previous shader tutorials before attempting this section.


2) I also wanted to post my texture and result to show this tutorial is definitely still relevant even on the most recent version of Unity. (My texture isn’t great, it’s a little too dark, but it’s okay)texture: https://bit.ly/FurTexture


result: http://bit.ly/FurResultI still couldn’t figure out how to implement the code from the section “Final fur thickness” but the result I got is still decent.

Again, sorry! I wish I could redact the last sentence from my previous message. Anyways, thanks for the tutorial!


-

-

-
-
Hi there. I’m sorry, but I have no idea what I’m doing. All I wanted was to apply fur to a sphere to get grass effect (seen on brackeys shrinking planet). So, my first question is:


Lines 42 and 50 in FurShader.shader – “vertexProgram” is it that the “vert” function in that helpers file?

Second:

What kind of texture should I use, I mean, I put some texture I tried to build with gimp and I’m not even close to the results I want.

Again, sorry if those are stupid questions, but I’m really lost.-
By the way, I’m getting the same results as Thomas, all the model is extruding, here’s an example: https://imgur.com/a/vQPhe4q

-
![Alan Zucconi avatar](../../assets/98460c412545b8dd.png)

Hi Matheus!


I think the problem here is that perhaps you are only doing ONE PASS.

So you are only extruding the material only once!To get the grass effect, you need to extrude it many times, at small incremental intervals, to give the effect of depth.


-

-
-
Hi Alan, I ran into a couple of issue with this fur shader, all the scripts are pretty much the same as yours. But when I increase the Fur Length property the entire model extend outward which looks nothing like the fur in your final result

Is it because of my texture? I basically used the fur mask texture in your post, but both the mask and the fur texture behave the same

-
![Alan Zucconi avatar](../../assets/98460c412545b8dd.png)

Hi Thomas, unfortunately I don’t think this is enough information to know what’s going on! 🙁


-
-
Hi,


i support you on Patreon, but i can’t see this post.

the password given on the drive doesn’t seems to work. 🙁Thanks for your work.

-
![Alan Zucconi avatar](../../assets/98460c412545b8dd.png)

Hey!

Sorry about that… I’m restructuring my pages, so that document is not so up to date anymore! You can find the password here: https://www.patreon.com/posts/preview-for-13182976 ! 🙂 I hope that helps!


-
-
Hey, I just supported you on Patreon. Is the password to the tutorials will be given for me on email, or how am I supposed to get access for the rest of tutorials ?:-)

Thanks a lot for your hard work!

-
![Alan Zucconi avatar](../../assets/98460c412545b8dd.png)

Hey Marek!


You should be able to access the posts on Patreon that are marked as “[PREVIEW]” in the title! They have the password for the posts! :p

-
-
[…] the basic tutorial about shaders. More posts will follow, with more advanced techniques such as fur shading, heatmaps, water shading and volumetric explosions. Many of these posts are already available on […]


## Leave a Reply Cancel reply