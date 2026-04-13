---
title: Simonschreibt.
url: https://simonschreibt.de/gat/zelda-the-bling-bling-offset/
author: Simon
published: '2018-05-05'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/4ba024f283a36bb8.png)


![](../../assets/4ba024f283a36bb8.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

![](../../assets/97c7abc15a9bccf8.gif)

Welcome! Today we’re going to talk about: **An apple**.

Actually, it’s not directly the apple, but the **bling-effect on the apple** (from [Zelda: Breath of the Wild](http://www.zelda.com/breath-of-the-wild/)) we’re interested in. Notice, that we still **do see** the effect even when the apple is **hidden** in high grass (**right** side of the video)!

Before I present you why all of this is **not** as easy-peasy as it may seem, let’s watch an example why such an effect can be **very** helpful to find an item in grass:

As you just saw, it can be hard to find items without a little help. In Sacred 2 we solved the problem by adding column-like effects which where **higher** than the surroundings:

Now that we know **why** such an effect is useful, let’s look at the effect in Zelda and the two major problems they had to deal with.



![](../../assets/25559e6a45508d0b.png)

The first problem: Our object could be **occluded** when put into high grass (and therefore the effect as well). But for some reason we do see the effect even **through** grass in the Zelda game:

That’s very cool. But, how did they do it?

I would have expected a behavior like below, where object and effect get occluded by the grass blades:

Let me quickly present three initial ideas for solutions which came into my mind:

![](../../assets/ebe450f92e093152.png)

![](../../assets/e766eecb05a53e2d.png)

My initial idea: Could that be a lens-flare? Lens-flares get drawn **on top** of everything (because they are a phenomenon occurring **within the camera** and therefore drawn **in front** of the whole scene). As long as no grass blade hides the effect, this would work…

![](../../assets/b46f0d305bf3ab30.png)


…but the lens-flare would disappear as soon as the effect gets occluded:

![](../../assets/6c10d6182116f0c3.png)

Another idea: Maybe they draw the effect **always on top** of the whole scene.

Hm…OK, bad idea. As you saw, if a totally different object (e.g. tree) is **in between** the camera and the object **with** effect, the latter would be drawn on top. That’s not so good.

![](../../assets/bb34c4f39e3605cb.png)

Could it be a very **special** grass-material? Where **only the effect** is allowed to be drawn on top but everything else is **not**?

Nothing of that is correct. It’s just a prove that I tend to think too complicated. The Zelda-developers did a very simple (but in my eyes genius) trick to overcome the problem. Are you ready? Here it is:

The **object** does **not** get modified but the **effect-position** gets moved **upwards** depending on the surrounding:

![](../../assets/cd4f678fb8054854.png)


Below you can see this in more detail: On the **left** the effect is **directly at** the apple (because the game detects somehow, that it lays on solid ground without grass), while on the **right** it’s slightly moved upward because the apple lays in **low grass**.

It gets more obvious when we look at really **high** grass. There, the effect is offset about a huge amount (look at the UI, it shows where the apple actually is, while the effect is way up in the air)!

Isn’t that amazingly simple? And it works so well! I never noticed that trick while just enjoying the game. Usually, while **running towards** an item, the UI-Hint for the “Pick up” appears **early enough** and then I press the button and just collect it. Do you notice the difference between the object-position and effect-position in this video?

Here I marked it to see it more easily:

Very. Well. Done! I really love this simple approach and I hope you liked it as well! Now, let’s look at the second problem.

![](../../assets/65f61a48ac553a9b.png)

Let’s look at the apple again. Do you notice something?

The question should be: What do you **not** notice? Usually when placing particles near to other surfaces you can see **clipping** happening.

Here I spawn a particle **on a sphere-surface** (the blue sphere-wireframe) which covers the volume of the apple. We see, that the particles **intersect** with the surface or are spawned **behind** the apple.

One idea to fix this could be to increase the spawn-area:

But now it floats in the air **beside** the apple and still appears sometimes **behind** the object.

So, how is it done in Zelda?

I got only one idea to fix this: **“Pivot Offset” (Unity**) or **“Camera Offset” (Unreal**). Here again our problem scenario: The Particles are spawned near the object and therefore do **clip/intersect** with the apple or appear **behind** it:

The same situation seen from the camera:

And here is the solution:

To prevent the particles from clipping, you can **offset** the particle towards the camera. Imagine a path from the particle-origin to the center of the camera and move the particle on this line:

The same situation seen from the camera:

This little trick avoids the clipping-problem and still keeps the particles **within the silhouette** of the object! It’s an amazing simple but effective solution.

One thing which can happen though: When the camera gets **inbetween** the offset particle and the object, the particles “disappear” since they are now behind the camera:

The offset is a powerful trick. Not only to prevent particles from clipping like below …

… but also to spawn particles **behind** an object (instead in front by) which gives the impression of an aura:

Just for comparison, here is the same thing **without** the offset:

And here is how you setup the camera/pivot-offset in…

**Unreal**

![](../../assets/e8b6232912728b60.png)


**Unity**

![](../../assets/17839d11c4539d14.png)


I hope you liked this little trick as well. There are no more ticks to show but some additional observations i made during investigating the topic.

![](../../assets/1e6697453d0cefbb.gif)

Here are the two little observations which might be interesting.

![](../../assets/e766eecb05a53e2d.png)

**Long Items**: Not every item in the game is round like an apple but every item has the bling-effect. Long weapons for example are an extreme case. Looking at them from the side works perfectly fine – note that the bling is only created **in the center area** of the weapon:

Looking at the weapon from **narrow angles** reveals that the offset **isn’t** big enough to push the bling-effect **in front** of the blade and therefore we can see intersections:

![](../../assets/6c10d6182116f0c3.png)

**Lens-flares**: In a cave I found these sparkling stones and you may think it’s made with **the same** tricks like before:

At first, I thought the same, especially after climbing on the rocks and seeing the blink-effect appear **in front** of Link. This is the offset, which pushes the effects nearer to the camera:

But then I saw that the effect is actually rendered **even on top** of the little flower which is very **near to the camera** and therefore far away from the rock (and its effects). **Remember**: The offset-trick should only be used for **small** distance to avoid, that the camera suddenly is **behind** the effect!

Here is a zoomed image where you see how the effect is rendered on top of the flower:

Remember, the other effect was rendered on top of its assigned object (e.g. the apple) but if there’s an independent object in front, the effect would be occluded. Here for instance we have Link is standing on front of the apple and the effect is never in front of Links leg:

That’s why I have the suspicion, that these effects are **real lens-flares**!

Thanks for reading, I hope you liked it and wish you a nice day!

Simon

![](../../assets/7b99d1f2e4be0953.gif)

Another way it may have been approached is by offsetting the vertices in the vertex shader along the camera vector which would make it render in front of the apple :)

It’s a very dirty trick but that is how I approached rendering boats in front of the water plane on my Technical Showcase: Dishonored project as you should be able to see here – https://www.youtube.com/watch?v=O-bdQMiK5_M

Ohhh! I have to add it to my article about the boats and water plane from assassins creed! I Love it! <3 Thanks!

I actually came up with such a dirty trick when studying that article! I tried a lot of things but working in Unreal was quite limiting, couldn’t offset the depth buffer towards the camera either because of conservative depth writes. But this way provided a really cheap and easy workaround.

Here’s the code in the UE4 material editor :) – https://imgur.com/a/RTzSKqj

Oh nice, thanks for sharing!

Hehe you are great investigator! :D

As a big fan of you, I want to translate your articles and introduce to people in my country. (Korea)

Would you permit this?

Of course, I’ll leave the original link of your article at the beginning. :)

Please give me positive answer! master!

Hi, unfortunately a lot of the videos on here are broken links now. Would be great to get them working again. Keep up the epic work!

Hey :) Which videos did not work for you?