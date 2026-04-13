---
title: Simonschreibt.
url: https://simonschreibt.de/gat/diablo-3-the-sacred-spiderweb/
author: Simon
published: '2016-01-14'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/3900fdd8a1823a54.png)


![](../../assets/3900fdd8a1823a54.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

![](../../assets/8bb68259a587be7b.png)


For me one of the hardest things while doing art is learning **What makes things look good?** For example: It is easy to notice, that the **left** sphere is missing a shadow to be “grounded” in the scene:

![](../../assets/346a98ec33c5de66.png)


Now we’ve light and shadow in the scene and this means there’s nothing to improve, isn’t it? Not quite. The problem is that further improvements are more subtle but still add a lot to the quality.

Only if you learn about indirect lighting and soft shadows you are able to update the sphere like below (shadow fades and is soft, the lower part of the sphere receives a bit reflected light from the ground):

![](../../assets/740add2501463f49.png)


What I want to state is, that it’s often hard to say **WHY** something looks good or does not. Often you achieve big difference even if the tweaks itself are less remarkable than going from no-shadow to sphere-with-shadow.

Additionally many of these elements are hard to spot but easy to miss – if you don’t know about them already.

One way of getting the details right is using references ([I described one method here](http://simonschreibt.de/wft/delayed-reference-method)). But today I wanna talk about a situation where I **did not** get it right **even WITH references**.

![](../../assets/9d09bcbf32cf0fe8.png)


While working on [Sacred 2](http://www.sacred2.com) I saw some spiderwebs in the game which looked like this:

Just by counting the fact, this is a perfect spiderweb, right? It has the structure of a spiderweb, the strings “hang” really nice, the color isn’t out of place … so why did I think that it could be improved (but of course had no idea how)?

Even a **quick** Google-Search for “spiderweb” **didn’t** help me. The first results show spiderwebs how (I guess) everyone would imagine them and they look very similar to the ones in the Sacred game:

![](../../assets/7366fb6faea92950.png)


That’s why I didn’t have any improvement-idea and forgot about the issue until I played Diablo 3. I saw **their** spiderwebs and it opened my eyes:

Later I saw spiderwebs in a Batman which even **move**:

Sometimes you have to step back to see the whole picture and it couldn’t be more true here. If you don’t watch a spiderweb in closeup (like I did) …

… but step back it might look more like this (OK this example is a bit extreme but I hope you understand my point):

With all these examples we can state that the Sacred 2 web has problems in the following areas:

**Scale:**It looks like a tiny web which was scaled up a lot. Even by supposing it was built by a HUGE spider it could be expected to have a different and more detailed structure.**Softness**: Diablo and Batman use soft-alpha (see below) to make their webs vail-like while the Sacred web is pretty harsh.**Movement**: The slow and wavy movement in the web of the Batman game adds the final touch.

Now we know what we want to achieve which is a very important goal. But especially for us game developers it’s difficult because even if we know what we need, the technology must be capable of simulating or at least faking it (e.g. global illumination, reflections, translucency …) – and we’ve to be aware of which technique is best suited for what we want to achieve.

![](../../assets/e40af0aadea9a88f.png)


I can’t remember why but for some reason we used a “hard” alpha-channel (alpha1, alphaTest) for the spiderwebs in Sacred 2 which didn’t allow smooth transparencies.

Here’s again the great Batman-Example how it **could** have looked:

But to be honest, back in the days I didn’t even think about suggesting a soft-alpha/alpha8. I just didn’t have the eye for seeing what’s missing, for knowing what technology would be necessary and I didn’t make a step back (and searched longer for references showing spiderwebs from a certain distance) to see that there’s something wrong with the scale.

The Diablo spiderwebs where eye-opening to me and the Batman games spiced it up even more. Here are more examples for moving webs:

Isn’t that beautiful?

It wasn’t really a “trick” but I hope you liked it anyway. :) Maybe you’ll find it useful if you have to do spiderwebs in the future or you can understand/appreciate the problems we artists sometimes have.

Have a nice day!

![](../../assets/ba0680151067ebbc.png)

[loginatu](https://www.youtube.com/user/loginatu2)mentioned that spiderwebs may catch a lot of dust and send this example:

“The Sacred version is not necessarily bad, spider web and specially aged ones gather dust over time and they get that old, heavy look, especially in caves or old enclosed spaces”

Also I like the [comment of reddit user mylon](https://www.reddit.com/r/gamedev/comments/40z3dd/i_wrote_about_spiderwebs_in_games_and_the/cyyvtqb) because it gives a very interesting view on the topic:

“[…] You see this a lot in other media where the portrayal seems poor but it’s done to convey meaning rather than be accurate. Is this for the best? I don’t really think so but sometimes it works. Good example is hacking in movies. It’s always mashing keys to make lines appear on a console or windows pop up. […]”

![](../../assets/ba0680151067ebbc.png)

Perhaps not a “real trick”, but, especially for a “not a real artist” like myself, this sort of insight is invaluable!

I think that the technique of “stepping back for better perspective” is one of the most important skills for any creative – be they artist or developer. And yet it can be very difficult one to apply in practice. So often the time when we need to step back for a wider look to solve our problem is exactly when we’re so consumed with focus that we don’t even think to do so.

Happy to hear that you find it useful! :) Oh yes you’re right. Maybe it’s not the hard thing to step back but to know WHEN you have to step back. :D Did you watch the movie oder read the article?

Both, actually.

I *really* appreciate having both options!

For most things, I prefer reading, as I can move forward quickly, go back and review, etc. Plus, I often read in situations where watching a video would be inappropriate.

That said, I’ve been trying to use more videos for learning art skills.

Good to hear, thank you for your feedback! :)

I’m so happy to see more stuff from you Simon :)

Your blog is a huge inspiration and help for my bachelor thesis game!

Vielen Dank dafür ;)

Happy that it helps :) What is your bachelor about?

I’m studying mediadesign in Hanover and I’m making a prototype for a 3rd person tower defense game.

Prototype as in “i won’t be able to finish all features till deadline” ;)

I’ll send you a link when i’m done if you like.

Nice, for a year I was in Hannover every 2nd weekend. Nice city! Love the “Maschsee”! Of course send me the link! Looking forward what you’re doing :)

Fun article, thank you. I remember that area in Diablo 3 and just how amazingly volumetric (?) the spider webs were.

Yeah they look really great! Like them a lot :)

I wasn’t sure what to expect. I mean – spider webs? But after watching I was surprised again by how you manege to give us, the viewers, insides in to the artistic side of games.

Happy that you liked the video. Yeah, sometimes in small areas lays unexpected complexity :D

I feel like you could take the moving/animated cloth texture trick from deus ex and apply it to a web and get a similar effect.