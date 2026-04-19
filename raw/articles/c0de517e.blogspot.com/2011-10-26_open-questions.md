---
title: Open questions
url: https://c0de517e.blogspot.com/2011/10/open-questions.html
published: '2011-10-26'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

![]() |

[End of the virtual world](http://shotbyrobert.com/wordpress/?page_id=102)" by Robert OverwegWhat makes the graphics work? I've played the last three call of duty games on 360, with a projector and a 5.1 system. I found them to be amazing. Then I downloaded MW2 on steam, and the graphics looked mediocre.

Conversely, Mass Effect 2 seemed decent on 360 but way more awesome on PC.

Red Dead pushes less polygons and has more visual defects than Crysis but awed me in a way no other game of this generation did.

Battlefield 3 is a technical jewel but MW seemed to me to have a better atmosphere.

Why? Is my subjective judgment shared by others? Is my memory failing me and have my expectations shifted? Or there is also something technical behind these impressions?

MW textures on PC have the low-res quality of a bad port. Is this, coupled with the increase in resolution, the reason the game looks worse to me on PC, makes my brain "see" the polygons more? Or is it because its atmosphere is better suited for a projector and a couch? Or maybe it's because playing the game I was more immersed into it than when I just looked at the graphics on the PC.

Why was it the opposite for ME2? Is its art style, less reliant on gritty texture detail, making better use of the high resolution and antialiasing of the PC?

Why I enjoyed more ME2 single player graphics than BF3 ones? Are the graphics enhancing the gameplay, or is also the opposite true, game and story do affect the perception of the graphics?

Is it the aliasing that is killing BF? Or is the inability of deferred lighting to express the subtleness of light transport and materials the issue? Is our industry jumping on the deferred lighting approach too fast, without really understanding what it's losing form precomputed lighting?

What about the heavy bloom and flares that BF3 and Crysis2 use? How are they working? How do they alter the perception of the image?

From my experience I observed some patterns, but I don't really know much, I've also found very little research...

*Aliasing and other high frequency artifacts quickly tell your brain that it's looking at CG, they are very disturbing. Motionblur at 30fps looks more cinematic and packs more punch than 60fps without blur. We tolerate framerate problems way more if the game looks busy (i.e. A huge explosion) than if they are not connected with game actions. Colour is hard to get right, and ambient lighting and proper occlusion of lighting terms are important to represent volume, rendering the air (haze, fog, scattering, desaturation tricks etc) helps with scale. Crowd variety is achieved more with colour and behavior variation than texture and model. Specular lobes are everywhere, have always fresnel, and we can't recognize errors in the light directions in the specular but we use high-gloss highlights to evaluate shape. Bleeding dark edges (i.e. when dealing with subsampled effects) looks less questionable than having bright halos.*

There, I think I didn't miss anything, that's pretty much all I know, it fills a few lines of text. I think that's a big challenge for us, there are more studios that know how to do deferred lighting right and fast than there are studios that know what's important to create an immersive, beautiful game. We don't know what to focus on where, what devices are used for what, which artifacts are tolerable and which are disturbing.


We know the (sometimes) the physics but we have very little math to model the psychology. Yes, KSK fits skin specular well. But what parts of it are important? When does it break and breaks the perception of skin being skin? We need to make hacks, and physically reasonable hacks are fundamental in our line of business, physics are fundamental, but physiologically motivated hacks

This also affects all the "tuning" decisions, i.e. more

Moreover linking perception (vision) and psychology with rendering would give us more objective tools for art-direction, like what device is the best to convey in the general audience a given intent, what makes a sense of "scale" or of "fear" and so on...

We know the (sometimes) the physics but we have very little math to model the psychology. Yes, KSK fits skin specular well. But what parts of it are important? When does it break and breaks the perception of skin being skin? We need to make hacks, and physically reasonable hacks are fundamental in our line of business, physics are fundamental, but physiologically motivated hacks

[would be way better](http://cs.yale.edu/c2/images/uploads/HR18_1.pdf)!This also affects all the "tuning" decisions, i.e. more

[LOD](http://graphics.pixar.com/library/LOD2002/paper.pdf)[switching](http://webdocs.cs.ualberta.ca/~xingdong/papers/ISM06.pdf)but with better detail near the camera, or vice-versa?[Geometry or textures](http://cs.yale.edu/c2/images/uploads/HR12_2.pdf)? Bigger SSAO radius and more noise or the opposite and so on.Moreover linking perception (vision) and psychology with rendering would give us more objective tools for art-direction, like what device is the best to convey in the general audience a given intent, what makes a sense of "scale" or of "fear" and so on...

Rendering without knowing about perception is crazy, it's like if musicians knew more about sound waves and instruments than harmony and melody. And yet we often chose rendering techniques based on really faint leads about what is needed to look good. There is little research, and the little there is focuses on issues that seldom are directly applicable to modern videogame rendering techniques.

Even worse, we are just not starting to understand the basics, like



Videogame rendering today at its best it's a work of iteration, the more you can try and the better feedback you get, the more you inch towards this ill-defined target of visual splendor. But even artists and art-directors with a great eye for light and colour seldom have much experience about realtime CG artifacts and their impact on perception.



Shifting from art to science has to happen in order for our profession to evolve, we can't rely on art direction for technical problems, it's not only too error-prone but also very inefficient. Scientific studies can be shared and described exactly, while art direction remains subjective and does not result in a shared progress.



It of course not something that happens only in rendering (or presentation in general,

Even worse, we are just not starting to understand the basics, like

[color](http://filmicgames.com/archives/586)and normals, and not only in the industry but even in most publications you will find little regard towards even basic visual perception metrics.Videogame rendering today at its best it's a work of iteration, the more you can try and the better feedback you get, the more you inch towards this ill-defined target of visual splendor. But even artists and art-directors with a great eye for light and colour seldom have much experience about realtime CG artifacts and their impact on perception.

Shifting from art to science has to happen in order for our profession to evolve, we can't rely on art direction for technical problems, it's not only too error-prone but also very inefficient. Scientific studies can be shared and described exactly, while art direction remains subjective and does not result in a shared progress.

It of course not something that happens only in rendering (or presentation in general,

[animation, audio](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.60.2002&rep=rep1&type=pdf)), we even make games with very faint leads about what is needed to make fun. And that's why often you have studios investing big amounts of money, and staffed with great talents, producing results that are impressive but still fail, while only very few games really know how to be fun, and really know how to immerse players in their art...*More to come... Meanwhile you might want to read something (other than the links I've already scattered in the post):*

[Some](http://virtual.inesc.pt/cge02/pdfs/chalmers.pdf)[interesting](http://www.neurovr.org/emerging/volume5.html)[reads](http://www.crcpress.com/product/isbn/9781568814650)[here](http://www.physiologicalcomputing.net/?p=1698). Also[Holly Rushmeier](http://graphics.cs.yale.edu/holly/pres.html)'s work (some is linked in the post - from the website the EG2001 and EG2003 presentations are very neat)*Please comment if you know more resources on the topic. A question has been posted on Quora*

## 7 comments:

It falls down to the difference between fidelity and style... one is easier to achieve and the other is style...

No it doesn't

Very interesting "Gestalt-ian" breakdown of games. I'm surprised it is a surprise to me, but we're so focused in nailing down the specifics, that we sometimes forget the orchestration of the whole!




Now the question is... should the game detect the player's environment and tweak itself to portray as much as possible the mood it was originally going for... I'm thinking about: 30-60FPS, texture blurring, aliasing etc.

I noticed in Uncharted 2 for example that the cinematic sequences upped the ante on graphics, blur and such while gameplay tweaked the engine to be sharper and less on the post processing effects. I know this is an optimization as they're more stuff happening during gameplay (physics, AI and such), but it does make a difference in subconsciously triggering "passive" or "active" mode for the player. Now that I think about it, that's why we're sometimes caught off by surprise when a "non-gameplay" sequence goes into one directly!!!

More stuff to elaborate but got to get back to work! Nice article!

namar: I think there are two levels to this.




One, which I'm currently more interested in, pertains if you want the "immersion" (perception of "CG-ness"). We always aim to sell something that feels authentic (even if not realistic) and there are certain artifacts which matter more perceptually than others, have a bigger influence in breaking the immersion.

I think that carries over all technical decision we make, not only in rendering but also animation, sound, presentation in general, as there are many choices we routinely make without a strong understanding of what is "better".

We are just starting to understand "better" and "worse" in terms of physical models and approximations of them (i.e. this hack in this shader makes sense because the physical material behaves a bit like this) but we know almost nothing about what matters most to people (i.e. the diffuse here has to be modeled accurately because human vision is good at spotting errors in this context).

The second aspect regards the expression. What should we do to convey a given feeling or idea. This second one is more a matter of art-direction and I think we know already more about this than we do about the former.

What is still lacking is a scientific analysis of what some given devices do in the average player, but to be honest there is some work there, something is moving (i.e. psychopsychological analysis of videogames).

Atmosphere, immersion and music are my favorite things in entertainment media. But how can I take what you are talking seriously when you don't mention ME1. I can go to ME1 again and it's still better atmosphere-wise and there's no contest. ME2 had some good moments near the end but it truly felt like work to get there. Mind numbing battles compared to the great tactical stuff in ME1, that was so great I immediately called for same system to other games. Can't say same about ME2.




When I finished ME1 I rated it 8/10. ME2 was like 6/10.

I'd have given ME1 10/10 if it weren't for the parts of the game that were there just to pad out what the producers probably deemed not enough content. I'd rather have 1 hour of mind completely blown rather than 60 hours of "please can we get on with this" to get into the stage "wait for ME3.. and 4 and 5..." to get on with the plot.

I'd have rather finished the Reaper plot in single or at most two games and have the writers write NEW AND ORIGINAL stuff even if it happened in the same galaxy. Of course maybe it isn't going to be just as epic as the Reaper stuff but so what. There's lot of great sci-fi literature the games could draw on if they don't have writing talent available.

Actually ME2 was so forgettable and bland I can't even remember how it ended right now.


I remember stuff from ME1 much better. The last boss fight was bit lame but all the story delivery was *epic* vs ME2 *snore*.

"But how can I take what you are talking seriously when you don't mention ME1"... by understanding that I'm making examples (about visuals, not even storytelling) and that these are far from being the point I'm making.



But I will use my super powers of commenter divination and tell you straight: "go back to r/truegaming", this is not a gamers forum to circlejerk and write reviews of your favorite games, it's a rendering blog for rendering professionals or people passionate about it and I will delete any comment attempting at even starting to go in that direction.

Bye.

Post a Comment