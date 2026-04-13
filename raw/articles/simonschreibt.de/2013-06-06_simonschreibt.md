---
title: Simonschreibt.
url: https://simonschreibt.de/gat/dungeon-keeper-2-walls/
author: Simon
published: '2013-06-06'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Deep in the dungeons of my brain was something waiting to come out. The last impulse to bring it into the daylight was given to me through Dr. [Fj](http://florianjonas.blogspot.de/). He mentioned the walls of [Dungeon Keeper 2](http://en.wikipedia.org/wiki/Dungeon_Keeper_2) and made me think and write about it.

**S t r u c t u r e**

![](../../assets/dcdd5c759a696f8a.gif)

![](../../assets/4698979b4730957e.gif)

Let’s start easy: The game makes you build and underground empire and for that you have to “cut” the ground earth on a cube basis (like [Minecraft](https://minecraft.net/)).

I wondered if these cube geometries are already existing (standing side by side) or if the whole ground geometry is one big block and modified in real time. The answer can be seen if you activate a wireframe

mode:

There are no cubes standing side by side! It’s “solid mass” where the needed intersections are cut into. You can also notice how the whole polygon topology changes at the cut area

**S i l h o u e t t e**

![](../../assets/bab6d8bcd9a484c2.gif)

One point which fascinated me since i saw the game the first time is shown here. The image consists of 3 frames: **1.** Screenshot **2.** Overpaint (silhouette following original form) and **3.** Overpaint (straighten to show how boring it *could* look).

The overpainted wall structure shows some nice geometry variation. If you think about a wall, you may think that it should be straight. But wouldn’t this look a bit boring (at least for a comicish style)? I wondered how this is done, because the

geometry/topology of the wall/ground changes – depending on the type of the wall and size of the room (more about this later).

It seems that there’s some kind of realtime transformation going on. Sure, the wall parts *could* be stored in several versions and stick together by code. But 2 clues lead me to a different suggestion.

- Most times i can’t see repeating patterns.
- A possibility to see the original geometry was given to me. This is the result:

![](../../assets/8d1d375da982ea34.jpg)

![](../../assets/b06d5cbf414bb367.gif)

These are the original geometries of the “training room” walls. As you see, the meshes *aren’t* deformed. Just straight lines – except a small alcove (lower right) and a shield (low centered). This is you it looks in the game:

I hope you can recognize the meshes and see, that *they’re* deformed (at least a bit). This leads me to the consideration that the artists had a “relaxed” job by *not* creating x variations of the same asset in different deformation states. Instead, the coders invested some brain power to add a consistent “noise modifier” (to speak in 3Ds max talk).

![](../../assets/b930a7419466cb42.gif)

And this deformation not only moves the vertices *a bit*, instead the impact can be pretty drastically like you can see if you let your workers dig a column of earth:**V a r i a n c e**

![](../../assets/e68b64d14d6e2746.gif)

Besides the nice deformation, i really like how dynamic the different wall parts are placed. The different tiles are sorted depending on the size of the room. Here i built a training room for the goblins and you can see how the wall “react” to the placement of more and more training tiles:**D a m a g e**

![](../../assets/acaf6647ab5a1d0b.gif)

Another nice detail: before walls are destroyed, they get different textures for the damage state:**E d g e**

![](../../assets/c9f1dc6e8516c8c2.gif)

Last but not least: I really like that they not only textured the wall but also the top of the wall! It’s nothing fancy but i like the sense of detail.**E n d**

You reached the end of the article. I thank you for reading and visiting my blog. I would be happy to hear your opinion about it!

If you wanna know, how to extract the meshes of DK2 or read some words of thank, just continue reading.

**T u t o r i a l (3Ds Max)**

It took me long time to find the tools and a workflow to extract the DK2 meshes and show them in 3Ds Max. Here’s the workflow:

- Install Dungeon Keeper 2 (e.g.
[GoG Version](http://www.gog.com/gamecard/dungeon_keeper_2)) - Download DK2WADTOOL
[here](https://simont.de/projects/simonschreibt_content/gat037/backup/)(original link is dead) - Run the DK2WADTOOL and select a WAD file from your game directory e.g. …\DungeonKeeper2\data\Meshes.WAD
- Download the 010 Editor Trial
[here](http://www.sweetscape.com/download/download_010editor.html) - Download the necessary scripts
[here](http://www.simont.de/downloads/dk2_010.rar)(Thx to[Hoenir](http://durchschuss.funpic.de/index.php?cat=games&site=dk2models)!!) and extract them RAR archive - Start the 010 Editor
- Open one of the KMF mesh files from the …\DungeonKeeper2\data\Meshes directory (created by the DK2WADTOOL) via “File > Open File”
- Open the template (Dungeon Keeper 2 KMF.bt) which you extracted from Hoenirs RAR archive via “Template > Open Template”
- Run the Template via “Template > Run Template” and select the opened template there
- Open the template (Keeper 2 Vert Extrahierungsskript.1sc) which you extracted from Hoenirs RAR archive via “Script > Open Scripts”
- Run the Script via “Script > Run Script” and select the script there
- A new tab with a new file should be created which should look like the following. Copy the whole file content into the clipboard.fn create = (

temp = mesh numverts:9 numfaces:8

setVert temp 1 [0.000000,0.500000,-1.000000]

… - Open 3Ds Max
- “Max Script > New Script”
- Paste the script code here
- In the script window press “Tools > Evaluate All”
- Done! A new objects is generated which should show you the mesh. It’s pretty small – zoom in!

**T h ♥ n k s**

This took me longer than every other article and i needed more help than ever. Without these great people it wouldn’t have been possible to collect all the information. But the greatest thing of this project is to get in contact with other people and so i want to say thanks to:

** FJ** because he mentioned the issue and gave me the last impulse to start writing.

**Elshad** for finding out, that the that the DXRipper wireframe mode works even if it doesn’t show the usual interface.

**Tomasz Lis** for providing DK2 tools on a [website](http://keeper.lubie.org/index.php) and answering all my questions.

[ Trass3r](http://keeperklan.com/members/182-Trass3r) for giving me hope. I found his code snippets which let me hope that there’s a solution.

** Hoenir** for being part of the decryption of the DK2 file format, answering all my questions and most important: handing me out the template and script for the 010 editor. Without these it isn’t possible to have a look on the original meshes of the game.

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

Interesting that you digged SO deep into it! I already though you do some magic on the graphics card with a tool to go wireframe… However: Since there was modified terrain already in Magic Carpet I was not so blown away by the possibilities in DK. Although its nicely done! (love the “edge decals”)

Exactly. Surely it wasn’t the next tech level for the gaming industry but i really like the will for detail. I mean the gameplay wouldn’t suffer from straight walls but i really like the look of the game even today :)

p.s. it was horrible. almost no tool worked with it, no mod tool could show the wireframe and i gave almost up.

p.p.s you’re a fast reader :D the article is online just 5 minutes!

To me it is, similar to Blizzard games, the amount of polish made this game stand out a lot. It is comparable to Evil Genius (http://cdn.steampowered.com/v/gfx/apps/3720/0000008902.1920×1080.jpg?t=1270602382), however the graphics style has so much more “love” in it. DK really used to be and still is one of my favorite games of all times. Sometimes I wish I had some minions I could slap around for increased motivation xD

That’s right. It’s interesting that also the first game (DK1) had such nice walls. But i only saw that on screenshots since i never played it.

Man I wanted to know this for so long, great job!

You look at the game and you can see that it’s something special about it, just just don’t know why (well until now that is…)

Thanks for the article and keep them coming!

(PS. could you change the language on your blog to English? Kind of hard to guess which is the “post” button)

Thanks for your comment :) I changed the blog language – i hope it’s working! Thanks for the hint!

I followed your link for the WAD tool, but all the website says is that you have to search the web for it. I tried to search the web, but all links I’ve found are dead.

Am I overlooking something?

I updated the link in the article with a direct download. Please use VirusTotal.com before you execute the file.

Great article, so glad to see other people just as interested in this. The minor bit of chaos in the coordinates of the wall models is termed wibble in the editor, alongside lean – its randomness factor has yet to be revealed, but I’m persistent.

If you’re particularly interested in the texture format as well (to get your nicely loaded models into 3ds max with something more than just shading), I posted a mechanism for decompressing those in the keeper klan forums.

http://keeperklan.com/threads/220-DK2-texture-format/page5

I’m undertaking a much more ambitious project of trying to reproduce the engine, and have had miles of success, but just as many miles to go :)

1. Thanks for your comment! Really happy to hear you liked it.

2. It’s just unbelievable that there’s a active community around this game after these years. And it’s a shame that no tools or help were released…i mean even the whole Quake3 (and Doom3?) engine is open source :D

3. I think i already saw your thread because i was spying the forum for every information i could find for the article. But my understanding in these things is limited, because i’m just an artist :D For me it was enough to see that the geometry isn’t modified in the bas meshes, but i think it’s awesome that you made this extractor.

4. Wow that sounds like a crazy project. And in the end your engine would be able to read the original data?

awsome, i never thought i would find a article like that.

Its exactly the information i needed.

Can you only tell me, wich version Max you´re using?

I´m using the Max2012 x64 version and wenn i run the script im only getting planes.

Is this a bug of the version or did you have any similar problem?

cheers

Luke

Hi Luke! Thx, i’m happy that i could help you :)

Max2010 64x! But the script i pretty simple so it might be that the problem is somewhere else…maybe the planes are something different and the actual model is really small in the scene. Or you should try another model. It took me also a long time to find the correct ones. :)

Just being curouis: Why do you need it?

Hi. I have problem with this tutorial. I can’t convert kmf to obj becouse i have error in point 9. Please help me.

Hm it worked for me when i was doing the article. I see two ways for you: 1. Send me the file so i can check if i get the error too 2. (better) Get in contact with Hoenir (the autor of the template) because he helped me too when i needed assistance

My name is Robin Green and I worked on navigation tech at Bullfrog along with head of R&D Ian Shaw. Ian was the master of the Incremental Delaunay Triangulation system that allowed us to dig out mazes (and the underlying map-and-crowd-nav system was used on both DK2 and Theme Park World)

Notice how the diagonals in adjacent squares flip from top-left/bottom-right to top-right/bottom-left? That’s the key to incremental delaunay, knowing when to split and when to flip.

Oh that’s very nice that you comment here! :) It’s hard to get in contact with Devs especially when a company isn’t there any more – a shame by the way :,(

I’ll link to the “Incremental Delaunay” wikipedia article and if you don’t mind mention your comment in the post. It’s always a honor if a dev of the game i cover gets in contact with us. :) But basically you guys added the new geometry (e.g. some wall-parts), cut the original geometry exactly where the new walls cut the old surface?

Oh and a reader of the blog had a question about the lighting in DK2…maybe he’ll write a comment too and ask some questions :)

Hi Robin,

The lights in the DK2 look so dynamic, it is really impressive for an old game like that.

Can you tell us a little about how the light / shadows are calculated in DK2?

Hi,

thanks for the information. We are currently hacking through all of the DK II resources. We already can display the static models. Extract WADs etc etc. All thanks to the community (I can just code, not hack in to formats :) )! If you can offer any help or are just curious, please visit our GITHUB page. I’m currently struggling with animations…

Code is available at:

https://github.com/tonihele/OpenDungeonKeeper

Hehe, i think all of my knowledge is written into that article. But when i did my research i also struggled a lot – there’s not much documentation. Are you guys writing down all your results?

Yeah, many resources were thankfully restored by Wayback Machine. And there is a semi-active guru (werkt) in the KeeperKlan forums. Though it seems to be offline at the moment. And he has already written a nice documentation about the KMF models, including the animations etc. And cracked the texture format, yet I would like to get my hands on the complete decompression code.

I don’t think we are going to document it much. The native JAVA (separate from the 3D engine) code exists there for all to see and copy. And it is all in one place, starting from extraction of WADs to extracting models/sounds/cursors etc.

YouTube proof:

http://youtu.be/xaf4mNnWUcQ

WoW! I Would have needed this for my article when i was looking for the wall-models :) In was a pain in the apple to get hands on those :)

A year has passed, I thought I’d drop in and update our status:

https://youtu.be/pOKXlO-n114

No variations on the meshes yet.

Thanks for the update! Looks great!

This is an awesome tutorial.

I’ve been trying to do this myself and came across your tutorial, I tried to follow your instructions but when running the script I get an error

*ERROR Line 17: Variable ‘mesh’ is undefined.

I’m working on some dk2 papercrafts and dungeon keeper related pages, to have the original game models would be awesome, is there any way you could send them to me in obj or some other 3d format other than the original kmf? or give me some insight into how to et past the ‘mesh’ is undefined problem?

I’d be more than happy to post your progress on my pages and credit to you for the models of course.

Hi Matt,

did you find a solution to the problem? Maybe you can send me your KMF and I can try it as well? Unfortunately I was also just trying around and don’t have a deep understanding of the systems. In any case, feel free to send me a KMF and maybe we can find the problem together.

Sorry for taking so long to get back to you, lifein general has kept me busy on other projects. I could never get it to work or found a solution for the errors, tried it on different operating systems, 3d bbit and 64 bit, win 10, win 7, heck i even tried vista and xp but same problem.

How would i send you the KMF files? if you could convert them and send them back i would be very grateful.

Just adding, I also get this, and cannot convert the KMF files

Me too, error after error, Could anyone just upload those models? I’m just an artist, even though I could write some code, but this is too much for me..

Updated scripts to convert to .obj are here: https://gist.github.com/Trass3r/914222adb44941e8013d1aa77bc7deba

wow, super cool! thanks for posting <3

The link of “DK2WADTOOL” is invalid, I searched it all over the internet and can’t found one, Could anyone upload one? Or any one who had already extracted the models of DK2, just upload the models?

I updated the link. I still had all data on my HDD and uploaded everything into this backup folder: https://simont.de/projects/simonschreibt_content/gat037/backup/