---
title: Why big game studios (usually) use single main 3d software environment?
url: https://bartwronski.com/2014/02/25/why-big-game-studios-usually-use-single-main-3d-software-environment/
published: '2014-02-25'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

Couple days ago a friend from smaller gamedev company asked me very interesting question – why while smaller companies allow freelancers some freedom choosing 3d software, big and AAA companies usually force people to learn and use one 3d environment? Even if they don’t require prior knowledge, in job offers they often say they expect people to learn and become proficient in their use within first months? Why won’t managers just let everyone use his favourite software?

Well, the answer is simple.

*Productivity.*

But it’s not necessarily productivity to quickly deliver one asset (every artist will argue over which 3d soft is best for him – and probably will be right!), but productivity in terms of a big studio delivering optimal and great looking assets in huge amount and for a big game.

Let’s have a look at couple aspects of this kind of “productivity” – both on management and technical side.


### 1. Team, studio and asset organization.

Usually in bigger studios there are no “exclusive” assets that are touched only by a single person. This would add a big risk in the long run – what if someone quits the company? Gets sick before very important milestone/demo? Goes on parental leave? Has too much stuff to do and somebody has to help him?

Just imagine – how this could work if two artists that were about to share some work used different software for source data? Do you need to install and learn different software, or struggle with conversions where you could lose lots of important metadata and asset edition history?

How source data from various programs should be organized in source data repository?

To avoid such issues technical art directors force software used by the whole company and its version, art pipelines, source and target data folders structures etc. to help coordinate whole work on big team level.


### 2. Licensing.

Quite obvious one. 🙂 Bulk licenses for big teams are much cheaper than buying single licenses of various software. I just don’t want to imagine the nightmare of IT team having to buy and install everyone his favourite software + plugins…


### 3. Usage of temporary/intermediate files and asset management.

If you export to collada/obj/fbx it means having an additional file on disk. Should it be submitted to source repository? I think so (point 1 and being able to reimport it without external software). But having such additional file adds some complexity to usual resource management problem when tracking bugs – was this file exported/saved/submitted properly? Where does the version mismatch come from – wrong export or import? Again another layer of files adds another layer of potential problems.


### 4. Intermediate resources vs. live connection.

When I worked at CD Projekt Red, for a long time we used intermediate files to export from 3ds max to the game engine. But it meant simply a nightmare for an artist iterating and optimizing them. Let’s look at typical situation that happened quite often and was part of daily pipeline:

Asset is created, exported (click click click), imported (click click click), materials are setup in the engine (click click click), it is saved and placed on the scene. And ok, artist sees some bug/problem. He had to go through the same steps again (except for material setup – if he was lucky!) and verify again. Iteration times were extremely long and iteration itself was tedious and bug-prone – like sometimes on export materials could be reordered and had to be setup again!

I believe that artists should do art, not fight with the tools…

That’s why most of big studios create tools for live connection of 3d software and the engine – with auto import/export/scene refresh on key combination, single button click or save. It makes multiple steps taking potentially minutes not necessary – everything happens automatically in seconds!

This feature was always requested by artists and they loved it – however it is not an immediate thing to write. Multiple smaller companies don’t have enough tool programmers to manage to develop it… It takes some time, works with given version and I cannot imagine redoing such work for many 3d soft packages…


### 5. Technical problems with standard file formats and their 3d soft exporters.

Raise your hands if you never had any problems with smoothing groups being interpreted differently in various software packages, different object scales or coordinate spaces (left vs right-handed). Every software has its quirks and problems and you can easily fix them… but again it is much easier for just a single program.

Another sub-point here is “predictability” – senior artists know what to expect after importing asset from one kind of software and it is much easier to quickly fix such bugs than to try investigate and google them from scratch.


### 6. Special program features that generic files lack.

I’ll just describe an example texture pipeline using Photoshop.

Usually typical pipeline for textures is creating them in “some” software, saving in TGA or similar format and importing it in the engine. It was acceptable and relatively easy (although suffers from problems described in 3,4,5) in old school pipelines when you needed just albedo + normal maps + sometimes gloss / specularity maps. But with PBR and tons of different important surface parameters it gets nightmarish – for single texture set you need to edit and export/import 4-5 texture maps, need to make sure they are swizzled properly and proper channel corresponds to target physical value. What if technical artists decide to change packing? Remove/add some channel? You need to reimport and edit all your textures…

So pipeline that works in many bigger studios uses ability of PSD files to have layers. You can have your PBR properties on different layers, packed and swizzled automatically on save. You don’t need to think what was in the alpha for given material type (“was it alpha test or translucency?”). Couple textures are stored inside the engine as a single texture pack, not tons of files with names like “tree_bark_sc” when you can easily forget (or not know) what does s or c stand for. You can use again the live connection and option to hide/show layers to compare 2 texture versions within seconds. It really helps debugging some assets and I love it myself when I have to do some technical art or want to check something. Another benefit is that if technical directors decide to change texture packing you don’t need to worry, on next save/import you won’t accidentally break the data.

Finally, you don’t need to lose any data when saving your source files – you have both non-compressed non-flattened data as well as lack of intermediate files.

Why not store all this intermediate and source data directly in the editor/engine? Answer is simple – storage size. Source data takes tons of terabytes and you don’t want your whole team including LDs and programmers to sync on all of that.


### 7. Additional tools and pipelines created by technical artists.

Almost no big company uses “vanilla” pure 3d software without any tools and plugins. Technical artists and 3d/tool programmers create plugins that enhance the productivity a lot – for example automatize vertex painting for some physics/vertex shader animation properties of vertices, automatize layer blending or help simplify some very common operations. Because of existence of those plugins it is sometimes problematic to even switch to a new software version – but to have their authors rewrite them for a different software or multiple products… It needs really strong justification. 🙂


### 8. Common export/import steps.

I think this point quite overlaps with 3-7, but it is quite important one – usually “pure” assets require some post steps inside the engine to make them skinned, assign proper materials or have as part of some other mesh/template – and to make artist job easier, programmers write special tools/plugins. It is much easier to automate this tedious work if you have only one pipeline and one 3d program to support.


### 9. Special game art features handling.

LODs. Rigging. Skinning. Exporting animations. Impostors. Billboards.

All of this is very technical kind of art and is very software dependent. Companies write whole sets of plugins and tools to simplify it and they often are written by technical artists as plugins for 3d software.


### 10. Handling in-editor/in-game materials.

Again overlap with 7, but also important – definitely artists should be able to see their assets properly in 3d software (it both helps them and also saves time on iterating), with all the masking of layers, alpha testing and even lighting. It all changes per material type, so you need to support in-game materials in your 3d soft (or the other way around). It is tricky to implement even for one environment (both automated shader export/import or writing custom viewport renderer are “big” tasks) and almost impossible for multiple ones.


### 11. Potentially editing whole game in 3ds max / Maya / Blender.

Controversial and “hardcore” one. I remember a presentation from Guerrilla Games – Siggraph 2011 I think – about how they use Maya as their whole game editor for everyone – from env artists and lighters to LDs. From talking with various friends at other studios it seems that while it is not the most common practice, still multiple studios are using it and are happy with it. I don’t want to comment it right now (worth a separate post I guess), I see lots of advantages and disadvantages, but just mention it as an option – definitely interesting and tempting one. :>


### Summary

There are multiple reasons behind big studios using single art pipeline and one dominating 3d software. It is not the matter of which one technical directors prefer, or is it easiest to create asset of type X – but simply organizing work of whole studio depends on it. It means creating tools for potentially hundreds of people, buying licences and setting up network infrastructure to handle huge source assets.

If you are either beginning or experienced – but used to only one program – artist, I have only one advice for you – be flexible. 🙂 Learn different ways of doing assets, various new tools, different pipelines and approaches. I guarantee you that you will be a great addition to any AAA team and will feel great in any studio working environment or pipeline – no matter if for given task you will have to use 3ds max/Maya/Blender/Houdini or Speedtree modeller.