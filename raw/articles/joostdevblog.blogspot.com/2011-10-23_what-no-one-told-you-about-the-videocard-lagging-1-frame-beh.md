---
title: 'What no one told you about the videocard: lagging 1 frame behind'
url: http://joostdevblog.blogspot.com/2011/10/what-no-one-told-you-about-videocard.html
author: Joost van Dongen
published: '2011-10-23'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)is a lot more complex than

[Swords & Soldiers](http://www.swordsandsoldiers.com)in every possible way, so we suddenly need to actually have a serious look at performance to get a good framerate on all platforms. Now while trying to optimise things, I found out that I had totally misunderstood an important part of how the videocard works.

I have read several books on programming real-time graphics (including the

*entire*OpenGL Red Book), yet somehow I have never read about this. So when I found out, I spoke to a couple of other experienced graphics programmers, and it turned out most didn't know this either. So I guess quite a few of my readers will find this interesting. For those who already knew about this:

*why didn't anyone tell me?!?!*;)

So what am I talking about? I always thought that the timing of a frame works like this:

![](../../assets/f81bbfcbcdc4b6a8.gif)

So as soon as you start sending render calls to the videocard, the videocard starts processing them. However, the videocard usually cannot process these calls as fast as it receives them, so when all the calls for a frame have been received, the CPU waits for the videocard to finish, and then proceeds with the next frame.

This scheme is quite nasty, since it contains two periods of waiting: both the GPU and the CPU wait for each other at some point, simply doing nothing in the meanwhile. This wastes performance.

So I have build some timers in Awesomenauts and I saw that indeed the CPU was spending a lot of time waiting for the GPU in calls to things like SDL_GL_SwapBuffers. I tested this in all versions of our engine, so on the Playstation 3, the Xbox 360 and the PC, and this happened on each platform.

So I implemented a multi-threading scheme to do the waiting in a separate thread, so that the next game frame can already be processed while we are still waiting for the GPU to finish the previous frame (this is actually a lot more complex than it sounds, but I will leave out the details for now).

And what happened? NOTHING! PC, PS3, Xbox360: none showed any framerate improvement! Argh! So I asked around to find out what I was doing wrong, and it turned out that the above scheme is entirely wrong. It is simply not how it works. This is how the scheme really works:

![](../../assets/fbba86c2c18175bc.gif)

So when you call D3DPresent or SDL_GL_SwapBuffers, the time spent there is not spent waiting for the

*current*frame, but waiting for the

*previous*frame. This is actually a really simple and smart solution to the waiting problem I mentioned above. As long as the GPU has more work to do than the CPU, it will never have to wait!

This explains why my optimisation didn't help: as this image shows, the GPU is constantly busy, so improving the framerate of the CPU using multi-threading is totally useless here.

An important thing to mention here is that I am

*not*talking about

*triple buffering*here. Triple buffering is a different subject and this scheme happens regardless of whether triple buffering is turned on or not (although for a good understanding of triple buffering, you would need to take this scheme into account as well).

Note that a side-effect of this scheme is that it introduces some extra input lag: user input (pressing a button to jump, for example) happens in the game state update, and the time between the game state update and the moment when it's results are shown on the screen increases because of this scheme. However, the framerate also increases a lot, so this is definitely a worthwhile trade-off.

Of course, if your game takes more time on the CPU than on the GPU, the GPU will still have to wait:

![](../../assets/8b4530e2fd19d3b3.gif)

Now my next question was: does it always work like this on all platforms? It turns out this varies. I asked around, and this is what I learned:

![](../../assets/78de1eb8e4c41c7b.gif)

While asking around, I also learned that in some cases on PC, the driver might decide not to wait at all. Someone on the Ogre forums posted

[here](http://www.ogre3d.org/forums/viewtopic.php?f=5&t=50486)that he had really long input long in his application. It turned out this was because the GPU was a lot more than 1 frame behind, because his CPU had so little work to do. So in his case, the scheme worked like this:

![](../../assets/cb0f62aef22a5bd7.gif)

However, I have never seen this happen myself, so I am not sure when this problem would occur. I have heard from a user that

[Proun](http://www.proun-game.com)sometimes has serious input lag when being run in Wine under Linux. I have not been able to test this myself, but I suspect this is the same problem.

However, this problem is limited by the size of the GPU command buffer: when the GPU is lagging too far behind, the entire buffer will be full of commands, so the CPU will not be able to push in any new ones, forcing the CPU to wait.

This can be solved using fences (an advanced feature of OpenGL and DirectX). Fences allow you to wait until the GPU has reached a certain point. You have to implement this yourself, but it makes absolutely certain that the GPU is never lagging more than 1 frame behind.

To conclude: keep this scheme in mind whenever you try to optimise your game, and be sure to first make sure whether the game is GPU or CPU bound. My fault while optimising Awesomenauts was that I was trying to optimise the CPU, while the bad framerate was being caused by the GPU. Always check your bottlenecks!

*PS. My*Proun Creator Disappointed With 'Pay What You Want' Results

[previous blogpost](http://joostdevblog.blogspot.com/2011/10/proun-is-big-success-pay-what-you-want.html)about the sales numbers of Proun resulted in some really painful comments online. I had tried to write a really positive blogpost about how happy I was with Proun's results, but[Gamasutra](http://www.gamasutra.com/view/news/37676/Proun_Creator_Disappointed_With_Pay_What_You_Want_Results.php)and several other large game sites summarised it simply as "*". Some sites and commenters also did some nasty misquotations on how I interpreted the sales data. Lots of people concluded that I am a whiner, and some even did some serious flaming about Proun and me. This is really painful for a game I made for the fun of making it, especially since I am really happy with how Proun did and tried to write a very positive blog post. Interesting how being misquoted can make people online hate me... Anyway, I cannot reach all those people and explain to them how happy I am with the reviews and income I got for Proun, so I guess I can only answer by trying to make more cool games! ^_^*

Interesting, I've never observed this behaviour myself (doesn't mean it's not true).





ReplyDeleteAnd I loved your last blog post. Could have been interpreted as whiney, but it was honest (takes much), and had massive impact (because of it being honest, and not a "it's all perfect" post).

Go on with the posts you do. They're all great. And if there was some whining in there, then because it just showed truth: Hard to make money in this industry. Anyone denying it is lying.

Continue the great work, I've learned a bunch, had fun so far with the games, all well here.

Now how about Proun on Windows Phone 7? :)

Wait... people actually said you were disappointed? I did not read your blog post like that at all. *confused*


ReplyDeleteOn topic: this is quite the interesting post. I too thought that the first chart is how it works.

Ah, I've always been wondering about this. I always thought the first chart was how it works as well. But it felt like such a waste. Glad it isn't.


ReplyDeleteThe GPU/CPU bottleneck thing makes a lot more sense now as well. :)

Interesting read, this reminds me of a setting in the control panel of NVIDIA for PC where the amount of pre-rendered CPU frames are adjustable.





ReplyDeleteFurthermore, I think processing input buffered is a general solution for synchronising 2 or more parties.

Think about the back-in-time rendering with network systems. Instead of processing new input from the network stream immediately, input is buffered. The buffer is read back in time (compared to client time) to ensure smooth moving entities.

The same principle also applies to video streaming.

Perhaps you see it as a different issue but in general is that

all what the GPU does. It buffers your commands and processes

them the next frame (while it fetches the commands for the next frame).This way it has one full CPU frame to process all the input but as a result you see everything 1 frame in the past, quite

the same as the network method or streaming data from internet.

regards, bk

Ow, wow, that setting in the Nvidia panel makes a lot of sense now! I never noticed that one before! It is 3 by default here on my PC, that is quite a high number. On 30fps, that means a potential added input lag of 100ms!

ReplyDeleteThinking about this I wonder if this is really so unexpected. Wont the graphics card have to wait for the scene to be described to it before it can actually even render the frame?

ReplyDelete@OmniMancer: It still does that in the very first scheme (the one that is incorrect): rendering starts right after the first rendercalls have been received.

ReplyDeleteHaving read both your wonderful post about sales and the gamasutra article, sadly I have to agree with them. Many things in the article they mentioned and the title itself "Proun is a success, pay what you want is not" clearly give an impression of disappointment with the model. But you did say in your article that you were happy with the sales anyway :)


ReplyDeleteMaybe they should have said this too.

Anyway great article here! I didn't know about this 1 frame lag either, and it was very interesting to read. I wonder how the vsync fits in this model? Maybe gpu and cpu are still working at full power, but buffers are swapped only at monitor rate?

I left VSync out of these schemes because they are complex enough already without VSync, but this is how it works:










ReplyDeleteIn the above schemes, VSync simply adds to the "render frame" block. So with VSync turned on, that takes longer.

Of course, waiting for VSync is in fact a form of waiting without doing anything useful, so VSync indeed introduces extra idling on the side of the GPU. And if the CPU is already waiting for the GPU to finish, then both would be idling while waiting for the VSync.

With double buffering, this is not solvable, because you cannot render the next frame yet: the front buffer is currently being shown and the back buffer is filled with the frame that is waiting to be shown, so there is nowhere to render the next frame until the VSync happens.

This is where triple buffering comes in: this allows you to start rendering the next frame to the third buffer.

So this suggests that triple buffering is a really good idea when doing VSync, but this is actually much less the case than you may think. The problem is that if you start earlier on the next frame, your wait for that frame simply increases. Say your GPU and CPU could run on 70fps, but the VSync caps it to 60fps. No matter how you put it, both the CPU and the GPU will have to wait at some point, simply because you are above your target 60fps already and rendering on 70fps is useless.

So is triple buffering useless then? No, it has one very specific use: if the rendering time of your frames varies, you can use triple buffering to even this out.

For example, say if one frame takes 14ms (70fps) and the next frame takes 18ms (56fps), then normally VSync would cap these two frames to respectively 17ms (60fps) and 33ms (30fps). With triple buffering, rendering the second frame could already start when the first frame is finished. These frames together take up 14+18=32ms. So with triple buffering, these two frames would remain at 60fps.

So as far as I know, triple buffering is only useful when you have VSync turned on, AND your framerate fluctuates a lot. If your framerate is constant, triple buffering has no benefits.

As far as I know, at least.

Thanks! So basically GPU/CPU both wait for a frame buffer update, but looks like it's a more complex matter than I thought.


ReplyDeleteAfter using Ogre3d for a while, I'm now learning from a lower level perspective with OpenGL/SDL and I was wondering how I'm supposed to achieve VSync. Since you mentioned SDL_GL_SwapBuffers maybe you're already experienced with it? :)

I read on a wiki that a way to achieve VSync is calling glFinish() after SDL_GL_SwapBuffers as glFinish causes a block until the next frame buffer update, but I'm not sure this is the right approach.

Whether both the CPU and GPU wait for VSync depends on the exact timings. Say we run at 60fps, which means 17ms per frame. If the CPU takes 16ms to process a frame, while the GPU takes only 13ms, then VSync will make the GPU wait an additional 4ms, while the CPU only waits an additional 1ms. It all depends on the exact timings.





ReplyDeleteDon't call glFinish! That will force you to the very first scheme in my post, since you always wait for the frame to finish. That scheme contains a lot of wasted waiting time.

Strangely, VSync is not a property of OpenGL or SDL. To enable VSync in Windows, call the function wglSwapIntervalEXT. You can search online for how to get access to that function.

If VSync is enabled, then SDL_GL_SwapBuffers handles it internally. You don't need to do anything yourself except enable it once using wglSwapIntervalEXT.

However, VSync can also be forced on or off by the user in the driver settings (like in the Nvidia Control Panel). By default your application has control, but you can never be sure that your VSync setting is actually used if the user has overriden it.

You're not the first, and you certainly won't be the last person to get paid out on by gamasutra readers because their 'journalists' like to only tell half their story. I don't believe a thing I read there any more, because you can almost guarantee they're misrepresenting the facts. AKA lying.


ReplyDeleteOn a more positive note, interesting stuff about the CPU/GPU. Will have to keep it in mind.

Thanks for your help Joost! :)



ReplyDeleteI see. That's the usual programmer/user battle, where the programmer wants to offer setting customization on his own, and user wants things to work as driver settings.

It turned out that newer versions of SDL (1.2) have some methods to handle VSync: SDL_GL_SetAttribute(SDL_GL_SWAP_CONTROL,0) -> Vsync disabled.

I wish good luck to your team for awesomenauts! I really envy you for being able to program on consoles. That must be really cool ;)

Thanks Joost, great post as always, very helpful and informative.



ReplyDeleteAs for the press over your financial post, I wouldn't be too effected. I discovered you from the same articles, and read your full blog post, and in fact continued to read your entire archive, so have a good idea of what you are about. Anyone who cares enough will read your blog post too, so they are only fooling the casual browser.

Keep blogging!

Joost, just ignore those haters. I've spread the word to most of my friends and family about Proun, and their reaction was nothing but positive. And I ask for everyone else to do the same because it's a great game, and its creator deserves it.

ReplyDeleteThanks for the nice words, folks! :)

ReplyDeleteThe Present(vsync) call doesn't wait vsync, but put command to buffer instead. The CPU wait when all backbuffers is busy. You can increase amount of backbuffers and it helps to hide any drops. But if CPU works very fast, you will wait at last buffered frame (at Present). Vsync use another thread for presenting.

ReplyDeleteInteresting to read this article when the catalyst linux driver (13.4) causes a noticeable input lag with awesomenauts - unless vsync forces the cpu to wait at least for 1/60s.

ReplyDelete