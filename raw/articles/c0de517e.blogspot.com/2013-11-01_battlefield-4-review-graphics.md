---
title: Battlefield 4 Review (graphics)
url: https://c0de517e.blogspot.com/2013/11/battlefield-4-review-graphics.html
published: '2013-11-01'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**UPDATE: I see this have been picked up by some gaming forums.**All fine if we take this not -too- seriously, the disclaimer below applies, these are some limited considerations and thoughts I had by putting few hours in the game while waiting for other stuff to finish and so on. I stand to the fact that some things are interesting to think about (beware, might even be technically wrong when I say they do this, could do that, I didn't use any hack to reverse-engineer the game) for people who make games. I see people saying "it's like digital foundry on steroids". No, DF spends weeks to do a really amazing job reversing what they can reverse accurately. I spent little time and had some unsubstantiated rendering thoughts, it's at best different. Anyhow, if it doesn't end up in a flamewar that lets me take this down, I might do it again for other games or publish other stuff I did in the past and kept private.*Maybe even do it seriously next time.*

So... This ain't gonna buy me any friends I guess. On the other hand I have to say I would be thrilled to see people tell me even the harshest things about my work, I've learned from a great artist who once told me to seek for people that would tear my drawings to pieces. Not that there is anything to tear in DICE's excellent game, just to say, please do dissect my work :)

Also, these are just some things that I've noticed in a few hours of single-player campaign, on my PC at Ultra. It's not comprehensive. It's biased by whatever happens in the first few hours of SP, by my mood the day I played in many other ways. It's not baked by Pix captures nor by any special knowledge, so it's probably

**ALL WRONG**I didn't take enough time to "reverse" anything.

I routinely survey games and their graphics, I consider it part of my job, but often I don't have much time for that. Worse still when the game is good and I end up actually you know, playing it, instead of just looking at rendering tech :)

I hope screenshots will survive blogspot's compression, also notice that most of them are downsized so don't pixel-peel, most images are equivalent to a supersampling AA version...

Ok, so. Let's go.

Frostbite is a great engine and I'm actually thrilled to see what all the various EA studios come up with it, truly can't wait. So as you will imagine and as everybody already will tell you, there is a lot of good stuff... That's why I'll start instead with three things that I think are -wrong-, then move to other observations:


**1) J.J.Abrams actually doesn't want his lens flares back****The good**: they work well, they are stable (seem even to fade behind occlusions), they are a mix of techniques I guess screenspace, art-authored particles and framebuffer readback to spawn more particles. They look very similar to Crytek ones, and they truly "blind" you.

**The bad**: they are fucking everywhere! BF3 did this, Crysis3 did this, please let this not spread to other games! It's a shame because they work well, and there are situations where you are blinded by lights that these could really help shape (even if they are cinematic flares, they don't try to replicate what happens with eyes), but they are always turned all the way up all the time and after a bit you'll want to rip your eyes out. It's a form of torture and a huge artistic sin.


[2) Everything has specular](http://filmicgames.com/archives/547). In your face! (a.k.a. Rise and Shine)Specular reflections seem to be turned always (well, very often) to 11. Now, while there are some situations where the intensity of it probably wouldn't be far off (i.e. really wet environments, pouring rain), we can't do perfect reflections yet.

**The good:**DICE guys being smart as they are do a number of interesting things, there are cubemap reflections but I think these are augmented with reflected "cards" or simple proxy geometry, I guess the latter only for planar reflections (rendered in a prepass, mirrored) but there's more to it, I think I've seen cards "fade" in and out and sometimes I think I've seen faint artifacts from a screenspace reflection method... Not sure, warrants more investigation

**The bad:**Specular aliasing everywhere, all forms of it (geometry, normalmaps, planar reflections), and I played on PC at very high-res, MSAA and post-AA filters.

From what I can see, analytic lights suffer mostly because textures even when looked up close have many discontinuities with the specular, I know that certain blending tricks help giving you detail, but seems overdone. Quite surprisingly as well, as we know by now many ways to circumvent texture/shader aliasing.

For planar reflections where aliasing is most offensive honestly it almost seems like if they did blur a bit the "cards" buffer (maybe I'm wrong and they don't have one...) it would solve a lot of issues. Still the effect should be applied sparingly, really in CG if you can't do it well, don't do it, sweep it under the rug. Planar reflections are a hack, they work only on some surfaces and this alone is an issue. Plus we can't really occlude too well sharp specular reflections, and occlusion is the key to believable lighting. In some levels, I just wish I had a multiplier I could tune down globally...

Lastly, specular seems always monochromatic, maybe I'm wrong, in real life it's often so, but I remember thinking for some materials to be wrong, could have been art or maybe to save on deferred GBuffer space...



**3) Faces**

This is the last thing I'll really bitch about. Characters aren't bad, animations are good too, but the shading is off, and again this is quite a surprise. Sometimes faces remind me of L.A.Noire weird low-frequency normalmaps. I wonder if that is indeed because of similar compression of acquired data, DICE has the tech and they used it in previous games... Anyhow, you can still blend that with detail maps driven by skin stretching or so, it's quite "common" tech nowadays. Also, specular. No, this time, the lack of it, which further causes the detail to be quite lacking, if only they had that they would be I think much better, as in general the SSS-ish effects are not bad and tastefully kept "in check" not going into "wax" looks. Looking at the ear edges, it seems a screenspace filter of some sort for SSS, but honestly it could be as well pre-integrated SSS. I don't love the over-bleeding in certain facial expression (normalmap wrinkles), eyes and lips are all "wrong" too. Now, mind you, especially in a deferred renderer doing skin, which is a fairly special material, is hard, but the lack of specular and detail is a mystery.

**Texture detail**

Now on some of the truly great stuff. On PC, details are amazing, especially textures and particles. Aliasing aside, materials are impressive, even more than Crysis 3 where everything had detail but mostly due to tiled detail textures used everywhere, especially I think to modify specular and give materials an unique microdetail. Here, I couldn't really see tiling, which means either they use very big textures or they do tiled details with some sort of distortion/blending tricks to hide it, or I'm not good at this :) Also material variation on the surfaces is great, you can't really see decals or layers, if they are doing them (which I'm sure they are) everything blends very, very well.

**Geometric detail**

Geometric detail is mostly due to having a lot of objects :) They don't seem to be doing tessellation, at least for displacement mapping, at all (which is not a bad choice), and I'm not sure if some surfaces do POM or not, honestly I'm not good at spotting that (especially certain techniques that don't simulate reliefs very well can be subtle).

Debris is everywhere, both authored in the level and due to destruction and particles. It's really great, things fly around all the time and it doesn't look unnatural. Also, no shimmer, no aliasing, small particles seem to be pre-blurred when depth of field is on (I think). It's actually easier (even if might not matter in a deferred, non baked renderer) to light correctly small instanced objects that large ones.

I couldn't see any particular shading trick applied to the vegetation (but I didn't look very hard, the levels I've played weren't very lush) but one thing it does great is that grass always bends out of the way and it's really hard to "clip" into it.

Destruction is everywhere and it seems mostly precomputed. At least in the campaign, some objects always shatter in the same way, while others shatter progressively, and other events seem scripted, like some cars always explode with a granade and some other never. All in all, it works great. Also the fact that there is always something that moves, cloth, paper, dust, foliage and so on really helps to sell the world as “living”, it’s really a perfect“touch”.

Lastly, I couldn't really see LODs crossfading or dissolving, small objects stay around long enough you won't notice they were gone, but that's also expected on PC on Ultra, I should try consoles...

**Lighting**

Pure deferred has its pros and cons, of course it's hard to bake much when things are always shattering and changing. Overall business as usual, does a good job with many lights on screen, and the analytic BRDF used seems quite "physically based".

They seem to use sparingly SSAO (Nvidia's HBAO I guess at ultra), really just a touch and with quite a huge radius, so you won't see "cartoon shading" silhouettes. It seems almost not randomized at all so you get sometimes the "stadium lights" effect (which I prefer to low-freq noise of some randomized AOs), if you look closely though sometimes there seems to be a 2x2 pattern that survives blurring. Blurring is detectable by the halos sometimes you get. There is a certain trade-off between large radius of occlusion and artifacts around characters, legs and so on, but most of the times it's not detectable so, good work there.

Honestly is great that we don't see SSAO-horrors like on Far Cry 3 or worse Deus Ex human revolution, but I wish sometimes it was used more, for "arealight" contact shadow kind of effects (bias it towards the sky! don't do radial SSAOs) and to shadows lights that are not dynamically shadowed, I wonder if they encode directional occlusion at all.

As far as scene lighting goes, I couldn't really see any dynamic GI going on (e.g. in the prison scene where there are large floodlights rotating around) and sometimes, especially in interior scenes it kind-of suffers from "deferred flatness", which is also a product I think of not having enough specular occlusion (i.e. on cubemap specular). If you can I'd say, always bake a good occlusion term, possibly directional, offline, or

**really invest in great directional SSAO or other methods, occlusion is fundamental**.

Sometimes, rarely I have to say, things fail more spectacularly than others and you can see a lot of environment/ambient lighting going wrong. This of course is not aided by the fact that often scenes are so shiny...

There appear to be linear (tube) lights, and they seem to have no specular (but might be that it was just an artistic choice), other than that it seems we still have point, spots and directional sun, which is a shame. I think any deferred renderer nowadays has to invest in more "exotic" lights, lights always come with some sort of "shaping" device and in real world you won't easily see a perfect "spot" with a perfect falloff, things are weird, broken, spill, focus and so on. Also, it's really hard to fake ambient lighting with points.

Sometimes there seems to be "scattering", but I think it's mostly due to either placed flares or tuning up the bloom to a very large radius (I might be totally wrong). Both methods work well, but it's not the lovely scatter The Order 1886 is showing us, especially the idea of using bloom means also that sometimes the light is very softly spilled indoors, but overall again, well enough. God rays from the sun are also well done. Sometimes it's possible to go through a door and see the fog on the other side disappear, probably it's due to these settings having "volumes" of tuning, hard to say and to spot. Underwater adds DOF and grain.

**Non occluded lights**

This I want to remark.

**If you don't have a source of occlusion for a given light or BRDF piece, prefer not have that part at all (or be subtle).**It is amazing how much difference it makes, I already wrote it, I'll do it again, occlusion is fundamental. Specular occlusion is fundamental. At least around silhouette edges, just "cast a ray".

**Other stuff**

I think it might have "

**thin wire**" AA of sorts on rods and small branches and so on. Not sure if it's there or I just want it to be there because I really think is a good idea. Seems though strange that a lot of rods don't shimmer much and often become exactly pixel sized. I don't know, I disabled AA, changed resolutions, still not sure. If it's there, it doesn't fade-to-alpha, so what I would do is to increase the diameter or wires to keep them pixel-sized until they're far enough they can quicky fade into not-existing.

**Sky**sometimes seems to be "tacked on" and too low-res. In most games sky seems fake. I'm not yet entirely sure why.

**Smoke**. Sometimes it seems almost to be accumulated/blurred in a separate buffer and then composited on top, I didn't spot any particularly fancy volumetric lighting either. It warrants more investigation. On ultra, I couldn't detect any artifact from subsampling particles, I guess that's not done or if it is, it's done very well (which is hard).

**Water**. On average great, worse if higher waves/interaction with objects. Sometimes just fucking AMAZING.

**DOF blur**is smart, I almost never see it "before the focal plane", which is ok, that is harder to do, and as I wrote, better to hide an effect than show artifacts. On ultra it's "sprite DOF" so I guess it uses compute and append buffers to create lists of particles. Which makes it surprising that the artists chose a "catadioptric lens" kind-of bokeh shape, which would be nice in "sampling" kind of DOFs (as you sample around a circle, not inside a disc) but seems unnecessary here. I guess it's there to make a "statement", kind of like the lens flares... We'll grow past these effects and start using them with taste as now we see done with SSAO (more often). On lower settings it goes towards a simple "blur based" DOF which unfortunately bleeds quite a bit :/

**Motion blur**, pretty standard stuff, doesn't bleed out of silhouettes it seems so nothing particularly fancy.

Final score: great!

Sometimes really unbelievably good. ~~I wish on PC it had a supersampling AA mode, as with proper supersampling some scenes are really amazing.~~ It does: resolution scale > 100%

## 17 comments:

Really an interesting read, very informative. I like this kind of thing, please do it more often :)

You said you are a rendering engineer and you stated many of the Frostbite engine cons.




So what engines have you worked on and since you already know these flaws are bad, show me your wonderful engine without those rendering artifacts?

Sorry, I hate people who state the obvious limitation of an engine but don't even have a better engine to back on.

What I mean is, your articles sound like "See all these silly flaws? I could easily create 100x better game engine than Frostbite, but I have not created one yet, maybe later..maybe."

You sound like a mad 12 year old Dice fanboy. You can criticize their tech the way you want, you just need eyes and a brain. This guy obviously knows his stuff, it was a great read to me. I'm glad to have his insight, even though I don't know who he is.

Agreed that we could use that kind of posts more often.


Shame to see so much retarded hate :<

There's no hate, just observation; nothing is perfect and complaining about imperfection as this piece does in part, warrants examination of the author's credentials.





Some of the observations are down simply to taste and there is no authority when it comes to preference.

I would like to know what engine and effects implemented in what game are superior and better done and how the author's credentials give his opinion any more gravitas than anyone else.

After all, half of his observations are based on guess work, an other half on his opinion of what is worthy graphics of a best in class developer - its seems basic to enquire of his abilities and output without being accused of hate.

That accusation is frankly infantile.

For a post with no hate, it came off as extremely knee-jerk accusatory. It's possible to criticize without condemning and his article hardly read of condemnation.




Whether or not a better engine exists is largely irrelevant. Noting imperfections in an existing engine is far from an attack.

Further, from what I gathered, he seldom stated limitations of the engine. It often ran more along the lines of pointing out questionable decisions regarding implementations of the engine's capabilities.

You'd do better to argue his points than to call into question his credentials.

Its quite clear that you would rather value a random person's opinions without a care as to their credentials... I mean, what relevance is that?




Anyone can come up with a theory, an opinion. A professional opinion however is obviously worth more. It moves it from the realm of opinion, to assessment and critical evaluation which this piece aspires to be. Credentials asserting ability and profession are standard criteria if you want observations to be taken seriously. Any professional in any field would understand this.

But its clear you don't understand this basic point, its worthless arguing with you. You probably value evolution and creationism equally - after all, its all opinions to you isn't it?

Move along, nothing to see here.

Ok, fair enough, I don't mind the comments (and I'm not one to mind the tone) so allow me to explain.







"your article sound like..." - Maybe, I honestly dedicate only a bit to the blog and I don't re-read my articles (often) so they come out the way the come out. Here I was a bit upset by the first levels by some of the artifacts. There are also some levels that are quite perfect, it's mostly in the artist's hands, there are some things that are technically improvable but the main thing is that if an effect is not perfect artists should just avoid it.

"show me your wonderful..." - The guys at DICE are amazing, I know many of them personally and I'm not in any way trying to prove that "my stuff" is better than theirs (and by the way, these days engines are made by many people so unless you're Carmack, even if your game looks better than another, hardly you can brag as a personal victory). On the other hand, this logic is flawed and please don't ever perpetuate it. I bet that if I don't know, a plumber in your house leaves all the walls leaking you are entitled to criticize him and if he says "ok, so show me a better plumbing job you've done" you would hit him with a baseball bat. So...

Last, but most important. I try to see things with a critical eye (well when I'm not just playing games) in order to see anything I can "steal" but also all lessons I can learn in terms of avoiding certain stuff that some people did already and I found problematic. In fact I was planning a follow up article focusing specifically on "lessons learned".

"Reversing" a game is fun, I remember the thrill when some artists started to peek in the first Crysis and found the AO stuff, which then we (engineered) correctly "solved" as a screenspace method and tried to replicate before Crytek published their stuff. Fun times, good learnings, I did a much more in-depth job for example when Crysis 3 came out and so on...

I do this for all major titles (an excuse to buy and play more games "for work") and sometimes (rarely, don't have time and there are no big secrets anyways) even more in-depth, but I never have published these results (well, externally at least) exactly because I don't really want people to think I'm going against this or that, which is quite stupid. This time I changed my mind because I thought it was just interesting enough to do so, as everybody will undoubtedly look at BF4 as a quality target.

I knew that I was at risk of getting some shit because of this decision but I also knew that most people in the industry, even DICE guys wouldn't mind. The truth is that if I really wanted to "damage" them it would have been better not to write anything. If I see things that in my mind are improvable, well, this gets people to think and maybe improve them, that's why I personally always love critiques (different from insults). If I operated as a true competitor, I would get from this what I needed in terms of learning and not show anybody...

Hope it's clear. DICE rocks. BF4 is fun and is my fav. multiplayer FPS game. I love EA (and worked for them for years). Peace out and maybe if I don't get too much hate (not that I did so far) I'll publish more :)

Oh for my "credentials", I don't like to talk about the games I made and the companies I've worked with on my blog exactly because I don't want people to think not of what I say but of who I am and think I'm motivated by this or that hate or so. Truth is we're all friends, at least, renderers love to chat about rendering :)


On the other hand, google is powerful and you can find out ;)

Ad-hominem















Subtextual ad-hominem, though this paragraph warrants discussion

Ad-hominem, red herring, false analogy

And grammatical failings galore, all while neglecting to address the greater body of the reply. Am I to take you for a professional? Fine.

To the point: We've both read a Blogger article by a person claiming to be a rendering engineer. Were this something more than a relatively light read addressing the technical aspects of some known issues with Battlefield's artistic direction and the Frostbite engine, I'd perhaps be more inclined to request some proof of authority on the matter. It is not. It's an opinion piece on subjective analysis that you are welcome disagree with. You can, as I have, read the rest of his articles if you hope to glean some idea of his level of familiarity with the subject. I suspect, however, that you don't

actuallycare about his credentials.Additionally, this

"

So what engines have you worked on and since you already know these flaws are bad, show me your wonderful engine without those rendering artifacts?"is a childish argument and

anotherinformal fallacy. There were ways of politely expressing that you had concerns about the author's authority to critique Dice's game, but instead you chose to discredit, not his article, but his authority to write it. There's nothing wrong with that, per se, but it does make you look like a butthurt asshole.Furthermore, this

"

Sorry, I hate people who state the obvious limitation of an engine but don't even have a better engine to back on."is so far from a valid argument that I don't even know where to begin. If I were to point out some inherent problems with combustion engines, would it be reasonable to demand I show you a type of engine without those flaws? No, that's ridiculous. You could demand proof of my authority to speak on the matter, but I think everyone would be happier if you simply addressed my statements and, if applicable, refuted them. The way you carried yourself in your initial post, however, seemed less like a scholarly disagreement on fundamentals and more a personal offense taken. We

knowthere are shortcomings and identifying them is a service to the community as a whole, whether or not we can actually remedy them right now.Finally, this

"

What I mean is, your articles sound like "See all these silly flaws? I could easily create 100x better game engine than Frostbite, but I have not created one yet, maybe later..maybe."is drawing a conclusion that is completely unstated and unimplied in the article. Another goddamn informal fallacy. Did you actually read the piece?

Please, stop talking about professionalism.

Great analysis, thanks for posting this article.

"Specular occlusion is fundamental. At least around silhouette edges, just "cast a ray"."




Could you expand a bit on that? Are you talking about marching a ray, a la screen space reflections, to occlude cubemap reflections, or something else?

"surprising that the artists chose a "catadioptric lens" kind-of bokeh shape, which would be nice in "sampling" kind of DOFs (as you sample around a circle, not inside a disc) but seems unnecessary here. I guess it's there to make a "statement", kind of like the lens flares..."

I'm not sure. The bokeh is not quite as sharp as a catadioptric lens. On the other hand, that is the kind of bokeh my eye creates looking through the LED on my monitor to infinity (not sure if I'm a freak), so maybe they were going for a physiological effect, rather than cinematic. Or you might be right, and the artist was just lost, which happens all the time.

Occlusion: Yes, you can do it in SS, just walk along the ray and step down mipmaps to approx a "cone sampling". Or in other ways i.e. if you have an occlusion SVO...


Catadioptric: I think the shape is that one, anyone it's unpleasant no matter what. I think it's not supersharp just because probably they use subsampled buffers for large sprites (it's a common technique) to reduce fillrate

The Anonymous comments on here deserve to just be deleted.




As a fellow gfx programmer, reading each others insights/guesses into how new techniques work, and also critiquing how the state-of-the-art can still be improved, is extremely important and makes for very interesting reading.

On the other hand, fanboi BS comments, that completely miss the point and the definition of the word "critique" are in absolutely no way interesting.

-----

On topic -- I'm doing SS ray-marching along several jittered reflection rays (based on roughness) and storing distance and distance^2 to a buffer, which is then blurred. When calculating specular for lights without shadow-maps, I use this data to perform a kind of SS-VSM (and yep, to mask out cube-maps).

Really an interesting read, very informative thanks a lot

Great analysis, thanks for posting this article.

Post a Comment