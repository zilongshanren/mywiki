---
title: Simonschreibt.
url: https://simonschreibt.de/gat/diablo-3-wings-of-angels/
author: Simon
published: '2016-02-11'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/dc94241187e3af43.png)


![](../../assets/dc94241187e3af43.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

I really like the design of Tyrael in the Diablo games and I **LOVE** the design and animation of his wings:

Not only in the great cutscene but also directly in [Diablo II](http://eu.blizzard.com/en-gb/games/d2/) it was possible to admire them:

![](../../assets/ebe450f92e093152.png)

When Blizzard announced [Diablo III](http://us.battle.net/d3/en/) I was very very very interested how they would realize those wings in a 3D engine. Let’s look at how it turned out:

Wow…this looks amazing!

But how is it done? Sure, they could use an animated texture and map it to a plane but that would cost a lot texture memory. Using skinned geometry (like I did below as example) might be a possibility but would cost many bones.

![](../../assets/45d9a372616a61cb.png)


However it’s made: there are several problems to solve:

- The starting point of the wing must be fixed
- You need a nice wavy movement
- The wing should get thinner towards the tip

I looked at their assets and to be honest at first I had no idea how they made such beautiful wings out of these “simple” textures:

![](../../assets/ebe450f92e093152.png)

**Important:**I’m just

**assuming**here and I

**don’t really know**if my thoughts are correct!

![](../../assets/c6011d07578ff048.png)


OK, it’s easy to understand that you get a nice wavy movement by using a sine wave texture and moving it along a plane. **BUT** the starting point **moves up and down** and as I just mentioned: we need a **fixed** point:

By looking at the in-game geometry I could see the trick: They deformed the plane so that the up-down-movement gets reduced on one side. Adding some subdivisions avoids that the texture stretches in a weird way like you can see on the **left**:

This is good enough because the area where the wings connect is pretty big and allows at least **a bit** movement. This avoids that the wings look disconnected when the sine curve is at its minimum/maximum:

By the way: The additional subdivisions let you add more deformation which can result in better and more interesting looking curve movement (faster/stretched at the beginning, slower/compressed at the end):

![](../../assets/ebe450f92e093152.png)

![](../../assets/32b3ee38e59ad30d.png)


Now we need to get rid of the opaque blue areas and here the texture’s alpha channel comes into play:

Applying this gives us a nice animated wing “string”. It’s interesting to see that these plasma-like “fringes” seem to have a bit of life already:

The only problem is that you can see the hard cut on the right side of the plane where the wave texture ends very abrupt (the left side isn’t a problem because there it connects to the angel’s armor which hides the harsh cut).

![](../../assets/90da8880300f4521.png)


But this problem can be solved by using a second texture as mask (see below). Another idea is to use **vertex color** as transparency mask but of course a texture mask gives more control with details.

To the right you can see how the applied mask improves the wing experience. Very interesting: the transparency in addition with the slightly squashed geometry makes the end of the wing look **thinner** which was one of the three mentioned problem zones!

![](../../assets/f8d3893e0280026a.png)


Now we can duplicate the plane several times to make the wings look like in the Diablo game. And to get some variation we can offset the UVs of the planes a bit:

But as you can see this produces several problems. We’ll talk about some solutions below:

![](../../assets/08db70efe631e4e5.png)


One problem is that the texture tiles/wraps and therefore “starts again” when the UV shell is reaching over the 0-1 border.

This can be solved by setting the texture tiling mode to : **Clamp**.

Clamping basically means that the border values of the texture are repeated forever instead of the whole texture (like it happens when you tile/wrap it):

![](../../assets/727d5256fb73daa7.png)


To avoid the last problem with the harsh cut at the right side (see above) you can stretch your UVs so that it aligns with the mask again:

![](../../assets/fdf5a7294b0e19b2.png)


Another solution I really like is using one UV set for the wave texture and **another** one just for the mask (without any offsets in the UV shells). I don’t know if they did this in the game because I couldn’t find such a 2nd UV set in the assets.

By using a 2nd UV set you don’t get any problem which we talked about above **but** clamping the mask texture might come in handy anyway even if the UV shells don’t overlap the 0-1-area some pixel bleeding might happen:

![](../../assets/35ac419e60190b05.png)


However you solved the problems, if you now don’t use boring planes like in my examples but pimp it up a bit then you end up with a beautiful geometry like this which is used in the game:

The curved surfaces add volume and even if it looks a bit complicated you should remember that it’s “just” made of subdivided and deformed planes:

As you can see there are some planes **without** subdivisions which actually **do** suffer from some “weird” texture stretching (like explained at the beginning of the article) but this gets very well hidden by all that other movement going on.

And these planes seem to use a different texture for the masking (I named it “Mask 2”). But I might be wrong here.

If you’re interested in seeing the UVs, here you go:

![](../../assets/c219b5f609e22e53.png)


If we apply our material to this wonderful geometry (and push the intensity a bit) it looks really similar to what you can see in-game:

Do you remember the “Pattern” texture (mentioned at the beginning of the article)?

I wasn’t sure how it’s used in the material but [luos_83](https://twitter.com/Luos_83) suggested it could be multiplied with the mask texture which looks very reasonable:

This adds a nice additional detail to the whole effect:

Here’s my final material. But as I said: It’s only an assumption!

![](../../assets/12c937279e483ec0.png)

![](../../assets/9d664484d0b2d2ec.png)


Again I’m totally in love with how Blizzards artist combine several “simple” steps to create something stunning. Only one thing I **don’t like** that much: When the characters move, the wings follow immediatelly without [secondary motion](https://en.wikipedia.org/wiki/Secondary_animation):

Not a major issue but got handled later – in a different BLizzard game: [Heroes of the Storm](http://eu.battle.net/heroes/en/) improved the wings in that regard:

You can admire the dynamic wings in the menu as well as directly in the game:

The textures look similar to what was used in [Diablo III](http://us.battle.net/d3/en/) but in addition to the wave texture they actually transform the geometry!

Here you can see the wings in the main menu:

And here you can see how the geometry gets transformed:

In my eyes these wings are a great example how game development works: We constantly have to overcome problems which look intimidating at first but can be beaten by using several small and creative solutions.

Thanks for reading and I hope you like what saw. Have a nice day! :)

![](../../assets/ba0680151067ebbc.png)

How awesome is that? **Jill Harrington**, the creator of the wings for Diablo III, said hello and revealed some more details for us:

“The second, darker mask texture is to modulate the bloom amount. Without it, the wings were still too bright at the tips. It also tints the bloom a bit.”


“Those little planes that aren’t subdivided are just there to fill in the wing base a bit without adding too many polys. The not-so-great texture artifacts don’t show in the whole wing, I think!”


“There actually is a small amount of secondary motion in the wings on NPC angels. They have a rig with a handful of joints controlled by limited ragdoll. When they were created, we couldn’t set a gravity that wasn’t either “up” or “down”, so stronger physics would have basically made droopy broken wings and killed the illusion.”


Of course the amount of overdraw with all those layered planes with soft alpha makes me wince, but they never caused a performance hit so they got to stay that way!


Thanks a lot Jill for sharing all those information with us! :)


![](../../assets/ba0680151067ebbc.png)

[Zeratu](https://twitter.com/ZeratuJiang) took some time to write a post about giving a wing-mesh dynamic secondary motion in Unity! He even shares his project files. Awesome! Thank you so much!

[Link to the Article.](https://zhuanlan.zhihu.com/p/30524160)

[Link to the Project Files.](http://link.zhihu.com/?target=https%3A//github.com/Zeratu/NiYongYuanCaiBuDao/tree/master/WingsRevo) (he also linked to them at the bottom of his article!)


![](../../assets/4546bf239667c7c5.gif)

![](../../assets/ba0680151067ebbc.png)

Wow, nice breakdown. Another very well explained technique on your Blog. Keep it up, it’s awesome and very helpful for people like me who are getting into FX stuff :)

Thank you! Yeah I’ve noticed that it’s easy to find tutorials for “normal” game art but VFX is still an issue when it comes to tutorials…or do you know good resources for that?

I feel the same way. There are few good resources for VFX out there. So much easier to learn amazing environment art techniques because of all the stuff that is out there to learn from. VFX is like: “There are a million amazing techniques used in the latest games, but nobody ever explains them to you. So go figure them out by yourself!” :D I’m happy I found a site where you try to break down a VFX technique once in a while.

Feel free to drop some links to vfx resources. :) I just twittered a talk about vfx in d3 which is one of my favorites: https://twitter.com/simonschreibt/status/697879894651510785

I found some Tutorials on Youtube from different people. I’m working with UE4 so I looked for UDK and UE4 tuts.

I got some from people I don’t know where there working, for example this guys:

https://www.youtube.com/channel/UCA-sP_G8gDY0V9YOOpK7V1g

https://www.youtube.com/watch?v=G9vKSqRzhGQ

Of course, Epic’s introducing to Cascade and particles is a good start

https://www.youtube.com/playlist?list=PLZlv_N0_O1gYDLyB3LVfjYIcbBe8NqR8t

But there’re also some twitch streams which were done by the Epic Games customer relation department, so some Senior VFX artist show their techniques (didn’t watch all of them by now)…one is missing, can’t find it. Hopefully I can dig this out my browsing history.

http://www.twitch.tv/unrealengine/v/16480921

http://www.twitch.tv/unrealengine/v/13926101

http://www.twitch.tv/unrealengine/v/12749804

https://www.youtube.com/watch?v=dtuLOxSkciA

And i found this Blog also:

http://valdism.blogspot.de/2014/04/vfx-tips-making-smoke-textures.html

Found it!!!!

https://www.youtube.com/watch?v=YZ3TIqwqOWY

Wow that’s a very cool list! I already knew the Unreal Introduction which is really great but the others are awesome too! Thanks for sharing! :)

gooooood job bro , u help me a lot , sharing is the best thing in the world!

Just discovered your tutorials, this is wicked stuff, and you dissect it in such depth and provide those short video snippets so that nothing is missing… like I said, really great stuff, I’ll retweet it for sure.

Thanks man! Saw you on twitter, nice nickname ;)

Thanks for such great content, Simon. So glad that i found this blog :)

Can you tell me the name of the tool you used to show Tyrael’s wings geometry and textures in game, please? Or is this done by modifying game assets?

Thank you for the kind words :) I’ll write you a mail.

I would like to know also. Is there some general application that works for most games or did you use some Blizzard/Diablo-specific software?

Sometimes you can find modding tools but sometimes it’s better to use tools like for example Intel GPA.

Really great insight. I always wondered how Tyraels wings work in HotS :D

Do you think the secondary motion is done with bones? or inside the shader?

That’s a good question..to be honest I’ve no idea. Maybe an IK-Bonechain which get’s deformed dynamically? I’d expect that it’s similar to the [Viper in Starcraft II](http://us.battle.net/sc2/en/game/unit/viper) which dot an dynamic tail at some time.

Was wondering about the same thing, the rest is pretty much straight forward but i could have used something like this secondary motion in the past. I would die to know if there’s a reasonable shader based approach.

And again a really nice breakdown btw. So props to you simon!

I could imagine that you can apply a sine curve into a vertex shader but that the shader reacts to the players movement…no idea. We should ask a shader-pro. Or someone could apply for a job at Blizzard, crawl through their documentation and tell us :D

first: your articles are great keep it up!

to the dicussion: my guess is that they are simple ribbon emitters with initial velocity or maybe not an emitter but using verlet constraints to keep the ribbon geometry in place. since there is not uv maped mesh this would be much easier than transforming bones (like jiggle bones in the source engine)

PS: also interested in what you used to get the wings geometry. i know how to get the textures but only them

PPS: can you make middle mouse clicks on links work? ;)

I’ll write you a mail regarding the programs but what problem do you have with the middle mouse button? When I click a link it opens in a new tab (Chrome Browser). How does your browser behave?

thanks a lot.

the middle mouse problem seems to only affect the comment section (opens new tab but the original one loads the page as well)

Oh…that’s interesting. Never tested that. Thanks for the hint!

Thank you for this article. You’ve must have spend a ton of time to discover and compile all of this know-how.

It tooks some time yes, but only a fragment of what I’ve spent for example into the Render Hell article. :) So it’s fine and with all this nice feedback it was totally worth it. :)

Hey Simon,

A lot of the effect is explained in this GDC talk, in fact it’s a truly brilliant insight into the VFX of Diablo.

For example areas of interest for me are the BlendAdd method and the tex1 * tex2 * 2 which are used extensively in all their effects to not only make then stand out but also to create effects which look far more sophisticated than they actually are.

Link to talk here: (I could type for hours, but obviously this guy nails it)

http://www.gdcvault.com/play/1017660/Technical-Artist-Bootcamp-The-VFX

I LOVE this talk! It’s one of the best talks I ever saw!

omg,it is a amazing video that is so clear ! it is my pleasure to meet u simon!,

iam a newbee in 3d game vfx ,but i am into it so much!

would u give me some web address that u think is good for me to learn those stuff?

and blizzard game’s texture where can i get?just give me some clue!

sorry about my english and so much ask ^^

great to hear that you like my videos :) i hope you’ll like future ones too :) regarding your questions:

i’m sure you already know that google/youtube is full of awesome tutorials. i think the next step is to have a good community. i’m mostly visiting polycount.com where you can find tons of awesome people which can help when you’ve questions. also you should checkout the polycount WIKI which is a goldmine containing tipps and tutorials – you could spend days reading through it. :D

but the most important 1st step is to have a goal. when i started with 3D i didn’t have a goal and therefore didn’t make progress. so it’s good if you set yourself a goal like for example making a hat for team fortress 2, a skin for dota 2, some small mod or create an artwork of your favorite character/environment. but maybe i underestimated you and you already know what you want to make – which would be awesome!

regarding the textures from blizzard there’re ways to get them but wouldn’t it be way more useful if you try to create them by your own? i mean, that would be a wonderful goal, wouldn’t it? :)

Hi, is it possible to do these wings in CryEngine 5 ?

I’m very certain it is. Why not give it a try? ;) And make sure to share your results with us! :)

Hi,

I started to make test in CryEngine 3 but I have some issue because the countours of the plane are visible, my mask doesn’t seem to work.

I have only 1 material with 1 UV set.I don’t find the option in CryEngine to make the mask texture clamp (extent option in Blender).

I used a decal option to make the mask (opacity texture) in CryEngine but I am not sure it’s the right way to do this.Also I had to make the option to increase emittance but that maybe the reason why it’s too bright.

https://media.giphy.com/media/IGBQm3tBR4I48/giphy.gif

Hi Simon,

For Tyrael Heroes of the Storm wings, I don’t see how the Wings mask is used ?

The texture can’t scroll and repeat itself and if it was static it wouldn’t have this effect.

Any idea how it’s used if it’s used at all ?

Thank you

Hi! :) As far as I see, the mask is static and does NOT move. But the other 3 textures you see in the image are used to scroll along the surface and masked out by this one big wing-mask to give everything a nice shape. But you’re right, this mask can not be used for scrolling since it doesn’t repeat – but the other textures can and serve as 2nd layer which are masked by the static mask. :)

I made those wings inspired from the Tyrael Wings for Grim Dawn :

https://media.giphy.com/media/M9Om3XBUswOdnteqzW/giphy.gif

Super cool! As soon as I have time I’ll add them to the post as update :)

Hey! Perhaps someone could give me a lead on how to do that wave texture, please?

I do have experience doing tileable textures, but I had never done a Wavy line (with energy around) tileable, I’m lost on how to do this..could anyone give me a lead? :(

Sure, you can create tileable textures in Photoshop (https://www.youtube.com/watch?v=FR3Z0zr1RaY) or you can use a tool like Substance Designer which automatically tries to keep everything tileable.

Great job on this. As far as I can tell, you got this entirely right. And I can tell a lot. ;)

thanks for your comment! good to hear that i’ve got it right <3