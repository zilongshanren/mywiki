---
title: Why I chose Hand Drawn Animations over Puppet Animations for Party Animals
url: https://www.gamedeveloper.com/art/why-i-chose-hand-drawn-animations-over-puppet-animations-for-party-animals
author: Ryan Sumo
published: '2014-05-10'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Why I chose Hand Drawn Animations over Puppet Animations for Party Animals

I outline why I chose hand drawn animation over puppet animation and do a quick tutorial of my animation process.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

# Spriter vs Photoshop


![](https://images-blogger-opensocial.googleusercontent.com/gadgets/proxy?url=http%3A%2F%2F1.bp.blogspot.com%2F-mxkQxTmZna0%2FU2yUZfOud5I%2FAAAAAAAABk0%2FbIEcduLhutI%2Fs1600%2Fspritermouse2.jpg&container=blogger&gadget=a&rewriteMime=image%2F*&width=1280&auto=webp&quality=80&disable=upscale)



I said I would experiment with the animation tool [Spriter](http://brashmonkey.com/) in a previous post to see if it would be a good fit for our game. I did, and I decided that as great as Spriter is, it just doesn't make sense for us to use it in our game. In my first few hours with Spriter it became clear to me that to create good animations with it would require a lot of skill and time. Otherwise they'd look exactly like their namesakes : puppets. Given the fact that I only really have a few animations I need to create for [Party Animals](http://blog.heypartyanimals.com/) the efficiency gained from doing puppet animations vastly decreases.


![](https://images-blogger-opensocial.googleusercontent.com/gadgets/proxy?url=http%3A%2F%2F4.bp.blogspot.com%2F-fhK8hngk5co%2FU23YNE51rxI%2FAAAAAAAABlY%2FEL_bLMioYRA%2Fs1600%2F2dtoolkit_partyanimals.jpg&container=blogger&gadget=a&rewriteMime=image%2F*&width=1280&auto=webp&quality=80&disable=upscale)



The way that [2D toolkit](http://www.unikronsoftware.com/2dtoolkit/) creates animations in Unity also helped to make my decision. 2Dtoolkit takes complete frames of animation then creates a texture atlas out of them that you can draw from when creating specific animations. This means that I wouldn't be able to manipulate the animations directly in Unity. Given that the required output for me was going to be the same anyway (ie full frames of animation), it just made more sense to stick with a software and process that I knew instead of taking the time to learn a new one. I would also have to use less software to get to the final product. If I were to use Spriter I'd first have to create the assets in PS, arrange and animate them in Spriter, and finally export them to Unity. Whereas now I'd do the first to steps in PS and export to Unity immediately after, bypassing Spriter entirely.


![](https://images-blogger-opensocial.googleusercontent.com/gadgets/proxy?url=http%3A%2F%2F1.bp.blogspot.com%2F-4qDD8SbKKro%2FU2yU3gP22zI%2FAAAAAAAABk8%2F-Mhp3GjJTQI%2Fs1600%2FPS_videotimeline.jpg&container=blogger&gadget=a&rewriteMime=image%2F*&width=1280&auto=webp&quality=80&disable=upscale)



I also experimented a little bit with Photoshop's timeline animation courtesy of this [video](http://vimeo.com/80851591) by Alex Grigg. While I learned a lot and am amazed at what you can do with PS in terms of animation, I once again came to the conclusion that trying to do it that way was just using a far too complicated too for a simple task. And so ironically after trying out all these different ways to animate our characters, I ended up going back to animating the only way I know how, which is frame by frame.


![](https://images-blogger-opensocial.googleusercontent.com/gadgets/proxy?url=http%3A%2F%2F2.bp.blogspot.com%2F-sVqaA1AJEVc%2FU2yV81zJExI%2FAAAAAAAABlI%2FqungweD1LYE%2Fs1600%2Fmousewalk_partyanimals.gif&container=blogger&gadget=a&rewriteMime=image%2F*&width=1280&auto=webp&quality=80&disable=upscale)




Here is the walk animation of our main character Mousey (yes, we still haven't given her a real name). This was relatively easy to do since I used a walk cycle guide. In the next few images I'll take you through the steps of how I made a hand drawn victory animation without a guide.

# Victory

![](https://images-blogger-opensocial.googleusercontent.com/gadgets/proxy?url=http%3A%2F%2F4.bp.blogspot.com%2F-XvQ0Kgue_YY%2FU23cqu_-0iI%2FAAAAAAAABlk%2FHXaB64gRwGI%2Fs1600%2Froughanim_partyanimals.gif&container=blogger&gadget=a&rewriteMime=image%2F*&width=1280&auto=webp&quality=80&disable=upscale)



Step 1 is to rough out the basic animation. I do this very small, since it's easier to capture the essence of the movement with smaller strokes. I've laid out the frames horizontally to show you how they look but typically I would draw each frame one on top of the other.


![](https://images-blogger-opensocial.googleusercontent.com/gadgets/proxy?url=http%3A%2F%2F2.bp.blogspot.com%2F-rGeqkC0AqXM%2FU23dfGgUjXI%2FAAAAAAAABmE%2FdKJJbNf4NY0%2Fs1600%2Froughanim2_partyanimals.jpg&container=blogger&gadget=a&rewriteMime=image%2F*&width=1280&auto=webp&quality=80&disable=upscale)



Step 2 is to enlarge the original rough animation then trace over it so that I have a larger version that I can use as a guide for the final animation. Drawing bigger will reveal flaws that were masked by the initial smaller animation, which I can fix here. As with concept art, the general rule is to try to fix things while they're being sketched instead of closer to the final product. You save yourself a lot of heartache that way.


![](https://images-blogger-opensocial.googleusercontent.com/gadgets/proxy?url=http%3A%2F%2F3.bp.blogspot.com%2F-nReo6htZeVM%2FU23cq5zau0I%2FAAAAAAAABlw%2F8PPlSIHVqUA%2Fs1600%2Fanimationlayers_partyanimals.jpg&container=blogger&gadget=a&rewriteMime=image%2F*&width=1280&auto=webp&quality=80&disable=upscale)



Step 3 is to take a pre made mouse model and arrange it according to the rough animation. I've separated each body part into layers so they're easier to work with, and I've drawn them in vector to make it more efficient to move around and reposition without any artifacting. I'm showing you my layers here as a guide.


![](https://images-blogger-opensocial.googleusercontent.com/gadgets/proxy?url=http%3A%2F%2F3.bp.blogspot.com%2F-E7LWJMXT1pc%2FU23eoMRbrlI%2FAAAAAAAABmQ%2Ffzmi7J9Q6gk%2Fs1600%2Ftimelineanimation_partyanimals.jpg&container=blogger&gadget=a&rewriteMime=image%2F*&width=1280&auto=webp&quality=80&disable=upscale)



Step 4 is to animate! Here's my animation timeline. As you can see it's relatively simple, just 5 frames. I hold frame 2 for just a fraction longer than the rest of the frames (except frame 1, which is the at rest frame) to show that the mouse is gathering her energy to jump. Frame 4 barely comes into frame and is only really there to smooth out the transition between frames 3 and 5. Frame 6 is a reused frame 2 as a landing frame. One of my issues with PS frame by frame animation is that the times you can hold the animations are so specific (0,0.1,0.2,0.5) so there's little leeway with timing the animations. I think that 2D toolkit gives you better control with that, but I've still to experiment further.


![](https://images-blogger-opensocial.googleusercontent.com/gadgets/proxy?url=http%3A%2F%2F1.bp.blogspot.com%2F-lV6KWOS4rI0%2FU23csdM-7OI%2FAAAAAAAABmA%2F0hkG5-iUy3Q%2Fs1600%2Fvictoryanimation_partyanimals.gif&container=blogger&gadget=a&rewriteMime=image%2F*&width=1280&auto=webp&quality=80&disable=upscale)



And here is the final animation!

# Final Thoughts

I didn't write this post to say that Spriter sucks and that frame by frame animation is better (I was very happy to support them by buying a Pro license, though they have demo that's free of charge). I'm really not an animation expert, and the truth is that each project requires specific animation tools. Ultimately if you already know how to do puppet animation then it's definitely much more efficient since no time would have to be taken to learn how to do it properly. But for me, it's frame by frame for now. As an aside here is an argument for [hand drawn animation](http://stoicstudio.com/animation-process/) and one for [puppet/modular animation](http://danfessler.com/blog/thoughts-on-modular-animation), in case anyone out there is still debating which method to use.


If anyone out there knows that I'm making a huge mistake here and can point out to me why what I'm doing is wrong, please don't hesitate to comment! If you think my frame by frame animation sucks and I could makes some changes to make it better I'd love to hear from you too.


This post was originally written for the [Party Animals Devlog.](http://blog.heypartyanimals.com/) Visit to find out more about the game.