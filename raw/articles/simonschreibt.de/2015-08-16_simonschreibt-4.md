---
title: Simonschreibt.
url: https://simonschreibt.de/gat/renderhell-book5/
author: Simon
published: '2015-08-16'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/d4520fa96ae94110.jpg)


Here I’ll shortly conclude what we learned so far:

Avoid small meshes

Check if small meshes are necessary or if you could connect several small to one big mesh. If you have small, talk to a graphic programmer to get infos about the polycount “sweet spot” (meshes below that triangle count aren’t rendered faster). So maybe yo want add some tris to make things round if you need to keep a small mesh. You should also care about multi materials. If you have one big mesh but with 5 sub-materials assigned, the big mesh is ripped apart during the rendering and this means you now have 5 small meshes again. Maybe an atlas texture could help?

Avoid too many materials

Speaking of materials: think about the material management. Sharing materials between assets might be possible if you plan ahead before the asset creation. Bigger atlas textures can help.

Debug Tools

Talk to your programmers if you can get ingame statistics so that you can assume how problematic your asset might be. Sometimes it’s hard to have the overview over complex assets. But if a tool can warn you, that this asset could be a potential performance problem, you might solve the problem before the asset is committed as final.

Ask the coder

As you see this topic is highly technical and very context dependent (hardware, engine, driver, game perspective…). So it might be a good idea to ask your programmer how assets should be setup. Or just wait, because if performance drops because of your assets, programmers will find your office and poke you until your optimized your stuff. :)

![](../../assets/ebe450f92e093152.png)

Wow, you read until here? You’re crazy! Thanks a lot! Let me now what you think. I hope you learned something. :)

**The End**

Hi Simon

Thanks, this was informative and fun to read. Will definitely recommend this series to new graphics programmers.

Thank you for the compliment! If you’ve any citique or the guys you recommend it to don’t understand something, let us know :)

Wow.The best thing I have read.Really good read for those interested in (me,me,me!!)graphics or anyone who is looking to know what’s going on under the hood(me,me,me!!) in the Simplest but best manner. Thanks a lot ,I will be going through this many times.

Good to hear! If there are any questions, I can forward them to Christoph :)

Wow, finally got to the end! Sorry for spamming but I wanted to leave my feedback:

The whole thing was great, like.. biblically great! you need to make sure this site NEVER goes down, even in the event of an apocalypse!

The only thing I would suggest (just to future-proof it), as more and more changes are made, and as new problems/solutions are found, this will get bigger and bigger. Maybe it’s worth making each book more like a book, by giving each “section” its own page or something. Just something to make it ease-of-use for people who want to refer to it regularly.

Anyway, it really helped. In fact this is a subject I’ve been stuck on for a LONG time, and you have made a huge difference!

Good to hear that you liked it :)

You won’t believe I but before Render Hell 2.0 the whole article was just one big thing. I separated the books with update 2.0 and I’m totally on your side that one part shouldn’t be too big. I always prefer to have a good overview. :)

Well to summarize your reply to my comment in book 2: I am a musician mainly, composer. But I do 3D art (weapons, creatures, environments), but I’ve always enjoyed the idea of programming. Not just for functionality but because i just like it! I don’t care if i’m writing a useful tool, or just a tool that allocates some crap into memory and juggles it around a little! It’s just nice to see all that stuff come together.

But yes I love to improve workflows and so on. I guess for me, I like to see how architecture and code can work together!

On that note I have some books to recommend:

Game Engine Architecture – by jason gregory, is amazing, it’s like a holy grail! I highly recommend it! (He is lead programmer for naughty dog)

Game Programming Patterns – Rob Nystrom. You know how many books are either 1 thing (AI, or networking, or graphics), and other books are “general engines”, and cover everything? well this book is the only that i have ever read, that covers the actual interactions between these subsystems. I learned how to write a basic render engine, how to manage memory etc, but i NEVER managed to put it into practise, but this book made a big difference!.

I would genuinly say, EVERY programmer should have a copy of each of those books.

Thanks for the recommendations!

Regarding workflows: I’m currently working on a new category which only goes about workflow improvement :) I hppe you’ll like it as soon as i release stuff there :)

真不错，我喜欢这种动画形式的

Great series, super clear explanation, i am as 3d artist understood all of the concepts very good. Thank you very much for this great work!

What is this? Where is the article?

Thanks for asking .. something really weird happened. Someone changed my article. Have to change my passwords asap!

Hi! great article! very informative and well researched.

I do have some fuzzy spots regarding texture resolution.

It is suggested to combine meshes into the same material, two questions arise:

– Does this suggestion apply even if the meshes aren’t in the same .fbx? Mesh A and Mesh B are imported into the engine as separate files, but then the same material is applied inside the engine. Is there any difference if a import them as one file? or it doesn’t matter?.

– In the pipeline we are creating the minimun texture resolution per asset that works well is 1K (let’s say for the Base Color), if we combine 4 of those assets into one material and pretend to keep the same resolution restriction, then we would have each asset with a 512×512 square of resolution assigned to it in the atlas, and some assets look bad. What’s the tradeoff of having one material assigned to 4 assets but with a 2K resolution texture set (or even greater if we, for example, group 16 assets into one atlas), it is still worth it to combine meshes into one material?

I hope i explained myself, specially the last question.

Thanks! great job.

Hi, thank you very much!

1. It depends on the engine. In Unity for example you can define an asset as “static” and when it has the same material/texture like others, then it’s automatically batched together. I didn’t test yet, but I assume Unreal does similar stuff. What I know for sure about Unreal is, that you can combine meshes within the engine – a new one is created, containing all materials (if there are many, then the new mesh has all of them assigned). Note: The mesh is split during rendering when several materials are assigned.

So the answer would be: Depends on your engine.

2. It appears weird to me that the minimum resolution is 1K … but anyway :D If all of your 4 (or 16) assets are on screen or near to eachother during the game, it’s great. If it would be single textures, all of them would be in the memory anyway (because you see all objects on screen) and therefore one big texture should work way better since you can even batch the meshes together (like described above). The problem is, that in reality, often meshes are not appearing together all the time. Or one of the meshes is used for example in a level, where the others are not. This means, if only one mesh is loaded, the whole atlas texture must be loaded which is a waste of memory in that case

So if you know exactly, that your assets will stay together and NEVER are used anywhere else, you can put stuff together in an atlas. But most likely you can’t keep such a promise over a game dev cycle. Also something important: Imagine one of the assets needs an Alpha channel but the other 3 objects do not. When putting all textures together into one atlas, you would have to create an “big” alpha channel for the whole atlas, even only one object makes use of it. This would be a big waste of texture memory. Also you have to keep in mind the mip mapping. Imagine one of your textures is pure white and another “patch” of the atlas is pure black. If your UVs of an object are too near at the border (where two atlas-sub-textures “meet”) you might see ugly color bleeding in the distance (due mip mapping). I had this and it’s ugly to resolve. Usually you would make sure that the UVs aren’t placed to near to the border of the atlas-sub-areas which wasted space. Also note, that with an atlas texture it’s not possible to use UV animations. If you would let the texture “slide” over the geometry (like you would do for an waterfall for example) you would slide the whole atlas over the object.

I hope this helped a little bit. Modern engines sometimes can “batch” textures into a big atlas automatically. It’s called mega texturing and basically a big chunk in the GPU memory is reserved and then filled with the single textures of all assets.

This might be an interesting article for you: http://www.casualdistractiongames.com/single-post/2017/01/07/UE4—Overview-of-Static-Mesh-Optimization-Options

“Merge Actors – A built-in tool that is no longer experimental. Merge actors will combine multiple static meshes into a single mesh. It can also merge materials into single texture atlases.”

Another question:

what about bleding materials?. For example, Unreal Engine does support a lot of blending options, what would be better from an optimization POV: to have two materials combined using a blending node inside another material, or two create one material that asks as inputs two of each textures and combines it directly inside of it?. It seems that the later option is the best, specially if we are doing blending using vertex info, because one material is (roughly) one draw call, instead of at least 2 drawcalls that are blended together. Did i get that right? any other thoutgh on blending, because it is insanely important for env art.

Thanks again!

I didn’t do tests in that regard but I feel like the latter option would be the way to go. I think I remember reading something (in the unreal documentation) the the “real” material blending costs a lot performance and shall be used with care. So I think you’re right but the only option to know for sure is doing some tests I would say :)

Another question popped up hahahaha

It’s usual practice to have a Master Material in Unreal Engine which then is instanced for. In our case it is needed that our Master Material to support some blending options for some 3D assets, but for other 3D assets there is no blending needed, actually, our project uses photogrammetry and we tested results with just a material with Albedo, Roughness and Normal simply plugged into it and it looks great for us.

The question is: what would be more efficient, to keep that Master Material for all the meshes, or create 2 masters, one that handles blending and one that is a lot simpler? it seems that having one material is more effective, but i want to take into account shader instructions to make a better judgement.

Thanks!

Good question which I have no clear answer for. Actually I’m asking that myself sometimes too. I read that naughty dog has one uber-material with a lot of switches because it’s easier to maintain. But note, that the do their shaders in code and not in a node-network like in Unreal – where the materials can get quiet messy over time which makes me prefer more, but simpler materials.

Not that if you do a static switch in Unreal, an material-instance is created anyway. So internally you create two separate materials but of course it’s sometimes nice to have only one material to maintain. I feel like one material for everything (skin, hair, environment, etc) is kind of .. big. But it sounds like your material wouldn’t go too crazy, when you’re just putting albedo/rough/normal to your objects and only the blend mode changes. In that case you can easily overwrite the blend mode within the material instance and you’re good to go :)

A wise dude one said: Performance is nothing you can calculate but only test. So … I guess do some tests and find out what’s better for your workflow and engine/pipeline. :)

just wanted to say thanks for putting these resources together, I will certainly be pointing other artists here for your entertaining and educational books :)

Thank you :)

Thanks you mach for your resources. (and more detailed links inside)

Impressive work!

Thank you for sharing that, it’s really great.

Plus de small animations makes the whole stuff easier to read and understand.

Well done

Thank you! I always try to make everything a bit mor comfy :)