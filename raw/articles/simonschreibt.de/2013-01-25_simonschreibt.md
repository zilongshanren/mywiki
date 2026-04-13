---
title: Simonschreibt.
url: https://simonschreibt.de/gat/assassins-creed-3-windows/
author: Simon
published: '2013-01-25'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This trick was mentioned by [Falk](http://www.fa-so.de/). He said, I have to check out the windows in Assassins Creed 3. So i asked around in the company and luckily Matthias, a great programmer & colleague at Egosoft, had the game as a PC version and even better, he already finished the game, which lets you achieve some cheats like “Always Night” or “Always Snow”. So we could easily capture the game at night, which is better for looking at the windows.

Let’s have a look. As you can see, it looks like there is a slightly lit room behind the window. I think if you look at it from near distance, the effect isn’t that strong anymore, but of course sufficient. This leads me to assumption, that there’s no real room behind the window.

Another colleague ([Alex](http://www.abalakin.de/)) of me suggested, it could be a cubemap with some parallax stuff in it. So at first i tested a standard cubemap with the Xoliul shader. Ok, it’s pretty clear that this doesn’t look like the cool parallax movement in AC3. I think it’s too fast.

![](../../assets/2f98d6a33157317d.gif)

[Neox](http://www.polyphobia.de/). As expected he dropped a hint immediately. He mentioned it could be [Interior Mapping](http://www.proun-game.com/Oogst3D/index.php?file=CODING/InteriorMapping/InteriorMapping.txt) or some cubemap parallax stuff. In fact, it’s not the Interior Mapping but i recommend reading the paper. It’s written in a way artists can understand and it’s very interesting!

Also I found this [article](http://seblagarde.wordpress.com/2012/09/29/image-based-lighting-approaches-and-parallax-corrected-cubemap/) about Image Based Lighting which seems to fit at least a bit.

![](../../assets/b10cde5ab507dfcf.png)


![](../../assets/b10cde5ab507dfcf.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

More important could be this [thread](http://forums.epicgames.com/threads/663154-Faking-depth-inside-a-material-%28inside-a-window-effect%29). It’s exactly about our issue and during [SynaGl0w](http://forums.epicgames.com/members/1327491-SynaGl0w) referred to a BumpOffset (which can be seen in UDK Material LT_Floors.BSP.Materials.M_LT_Floors_BSP_Grate_Pipe) the user [Kedhrin](http://forums.epicgames.com/members/1297044-Kedhrin) wrote a small [tutorial](http://forums.epicgames.com/threads/663154-Faking-depth-inside-a-material-%28inside-a-window-effect%29?p=26115029&viewfull=1#post26115029) about it.

I definitely had to ask [Marcel](http://www.marcelschaika.com/) also about his opinion. And i think we all got to a conclusion:

It seems that they use a standard cubemap but changed the “speed” of the moving plane to a slower amount, so it looks like the reflexion plane is behind the window. In my example (see above) the reflexion plane was moving too fast which looks like the reflexion is actually in front of the window glass.

**The second day**

I got some great feedback and also a good question. [Matty6666](http://www.polycount.com/forum/member.php?u=60136) asked how the windows look at day time. Because at night you see warm lit room interiors. I had no idea. So i asked my colleague Matthias again and he was so kind to boot the game up again.

“These foxes!” (In Germany we say that to smart people. “Du bist ein Fuchs!” == “You are a fox!”) At first i thought they do standard cubemapping at day time and to the “funky” cubemapping only at night time.

But then i saw, that they’re even foxier (superlative of being a fox). The use both: standard cubemapping *and* funky cubemapping at once. But of course, they change the texture. At day time you have colder colors inside. How awesome is that? When the outer light is warm, the inner light is cold. When the outer light is cold, the inner light is warm. This is art how i like it!

Hm darn! It’s not really well visible in the GIF files. So trust me: you can see a fast moving cubemap and a slow moving “interior” cubemap…

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[a long post about their interior mapping](https://blog.scssoft.com/2025/02/under-hood-parallax-interiors.html)! They made a ton of research and even a new tool so that the artists can easily define the UVs for all those windows.

there is a udk tutorial that covers this kinda thing. http://eat3d.com/materials. check out the 3rd image along (window parallax material). iv watched this tutorial and this seems to be the exact same thing even telling you about instancing and changing the color (yellow to blue in the video)

Thanks for the link! Hm…pretty pricy. But would be very interesting. The comment section speaks for itself :)

I have done this with footprints in snow and other things. You can basically modulate the uv’s of a material by the x and y component of your camera direction. The camera direction is in local space and then you can additionally control the amount by a float for increased parallax. I used a height map and multiplied that by the x and y component of the camera direction to create deep deer prints in snow for The Last of Us. You would only want to use a cubemap if you had say 3 windows and each window you wanted to show a different part of the room. The execution of that is a lot more complex though.

That sounds really interesting! How did you handle the “border” of the footstep? Any kind of occlusion mapping to “hide” the border which ins’t pointing at the camera? Do you have a video?

I didn’t play the game and the PS3 of my girlfriend is currently broken :( Would love to play the game and you gave me another reason to do it :) Besides of all the great feedback from magazines and colleagues.

I’ll be doing a post about it soon with examples of the shader and a breakdown. The material is alpha blended and projected onto the destination pixel in world space so basically a decal with parallax. The border just has a soft alpha to cut out the part where the cam dir is being multiplied by 0 due to the inverse height texture. That’s the rough idea. In UDK this technique is called bump offsetting I believe. People just don’t usually use a texture instead of a constant float.

Oh that sounds good! I would love to read your post as soon as it’s ready. Yeah i tried a bit around with Bump Offset in UDK in the “Lego – Studs”-Post, really interesting tech.

Thanks for sharing these details with us! :)

https://youtu.be/9vEfH9SJ9mY

Witcher is also using these tricks with parallax. Look at 32:20.

Super cool! Thanks for mentioning! <3