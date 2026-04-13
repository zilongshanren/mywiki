---
title: Integrating Vector Data - Roads
url: https://outerra.blogspot.com/2010/05/integrating-vector-data-roads.html
author: Outerra
published: '2010-05-25'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[roads](http://outerra.blogspot.com/2009/06/roads.html)where the approach and algorithms for creating spline based roads were outlined. At that time it was just a concept of how it may work, with many unresolved issues.

In the past weeks I occupied myself with integrating the road system into the engine, making it more robust and powerful on the way. The road way points now contain additional information such as road type, width, marking style and more that will allow to make a variety of road types, also including forest roads with ruts, for example.

As you can see on the following screenshots, the roads are completely integrated into the terrain - no terrain poking through the road surface ever. The integration also modifies the surrounding terrain to make the embedment natural. Side of the road is initially smooth up to a specified border width (can be specified per road spline node), and after that the fractal roughness gradually takes on.

Depressions are filled and an embankment is created.

Routing the road through a rock or hill makes rocky slopes with defined steepness on the side(s).

More screenshots showing the creation process and the results, with varying level of detail.

The trees are automatically removed from the road surface and its border area, although sometimes you can see branches hanging over the road.

Splines allow for some mad road shapes but it still fits into the terrain :)

Terrain under the road is initially roughly prepared - gaps are filled and excess volume is cut out. This is being done at tile with resolution ~10m, so that fractal algorithm can refine it down naturally. Previously, when the road cut into a hill, the cut was unnaturally smooth. Now only the road border is smooth, gradually transitioning into a rougher fractal structure.

In the following screenshots you can see the process documented:

I. Placing the waypoints - this is currently being done as you move over the terrain pressing a build-road key, later a built-in editor will allow for better editing modes and options.

II. Rough terrain treatment - note this is actually hidden within the process, I've visualized it here just to show what effect it has on the terrain.

III. Finalizing the road

The engine has no problems with terrain resolution (as is apparently the case with many planetary engines), to the extent that asphalt can have actual thickness - I think it's 3cm now (~1.2inch).

Other notable features are

- vector data are automatically partitioned and indexed in quad-tree managing the terrain
- overlay dirt textures per road type
- roads can connect, additional helper code will be needed to adjust the spline points and their attributes so that the connection is smoother
- the same system is also used for terrain leveling, with or without pavement placing or with gravel surface etc.

Finally the process can be seen on the YouTube video. Original uploaded video was 500MB with good quality, but the recompression step on YouTube reduced it considerably.

The same system is used also for runways, here's a teaser screenshot for upcoming video where Angrypig tries to properly land at .. you can guess where this is from :-)

The corresponding discussion topic on Outerra Forums can be found

[here](http://www.outerra.com/forum/viewtopic.php?id=57)

See also the

[dirt roads](http://outerra.blogspot.com/2010/06/dirt-roads.html)

## 10 comments:

Lukla!


This looks wonderful, congratulations!

Wow, awesome! I could play years with this engine and it would never stop to be fun for me.






By the way, the runway looks a little rough on the end, it should probably be flatter.

Also, don't forget to post this news on ModDB, most people that are interested in this don't check your website much.

PS: Nejsou to Tatry? Mohl bych si udělat virtuální zájezd na Slovensko! :D

Yes it's Lukla :-)


The precision of source terrain data in these parts was not that good so the shapes could be better. Correspondingly the runway profile might not be exact as well. But the end is flat, the roughness is just an optical illusion.

Re:PS: Toto sú Himaláje a oblasti z Nepálu. Zvyčajne sme v Európe, ale teraz keď je tu ten prach z Islandu ... :-)

What I have won? Can I fly over there in Cessna? ;)


I know this airport from payware addon for Microsoft Flight Simulator, runway looks very similar. Good job guys.

will you be able to import openstreetmap data? http://www.openstreetmap.org/


its such a great and growing dataset. and completely open too

@Michal Puto: It will be possible to fly there in the demo, the airport will be included there by default. As well as possibility to place a generic airport anywhere else on flatter parts so you'll be able to place one somewhere down in Nepal.


@krz: Yes the OSM data can be imported one day, we've already inspected the formats it exports. We could use some additional attributes for polygon land classes for example, so we are also thinking about bi-directional data exchange with OSM.

Recently I took a look over roads in my home vicinity and I was wondering how much your roads looks like those in real.




RE:RE:PS: Nu, minul jsem jen o jeden světadíl. Mohlo to být horší :)

(To all who don't understand: I am sorry, but I can't stop :D )

Well except for the missing cracks, holes and asphalt patches, you mean :-)


But we are already thinking how to use fractals to ruin the smooth road surface to make it look a bit more realistic

Amazing, keep up the good work!



Hey, in the video I notice some kind of ambient occlusion in the deepest parts of the forest, how do you do that?

Saludos desde España :)

Thanks!

That ambient occlusion lookalike is actually derived from the output of function computing the probability that a tree grows at a particular place, that we are using to position the trees. In forests the probability is high so the ambient light is low; towards the forest edge the probability decreases and the light goes up.

Post a Comment