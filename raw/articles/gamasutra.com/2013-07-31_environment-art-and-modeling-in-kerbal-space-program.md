---
title: Environment art and modeling in Kerbal Space Program
url: https://www.gamedeveloper.com/art/environment-art-and-modeling-in-kerbal-space-program
author: Artyom Zuev
published: '2013-07-31'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Environment art and modeling in Kerbal Space Program

An inside look at the modelling work behind Kerbal Space Program's structures.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![](../../assets/7ac912ecda0db0d1.png)


Hi there. I'm a content developer at Squad, working on the the Kerbal Space Program, and I figured it could be interesting to write a blog about my process.

The most obvious thing to start with would be the new space center we have added in the 0.21 update. It would be an opportunity to tell you about some weird workflows I use and to talk in detail about style choices specific to this game.

Replacing the objects that were used in that scene up to this point was something that was much needed to be done, as the old meshes were essentially placeholders and had a host of problems. Let's detail them first.

Oh, well. First and foremost I have to warn this would be a long read and a huge page to load as I have no restraint or sense of what's appropriate for a dev blog. I'd also like to apologize for perhaps oversimplifying things that could be obvious to fellow artists. Sorry about that.

The Issues

Let's recount the issues that were present in the old content.

First, the polycount. While old buildings were seemingly simple in their shape, they were modeled using some techniques like boolean extrusions which did not work out too well for their polycount.

Second, the material count, and subsequently, the amount of textures old models were using was problematic. Now that isn't nice. Why? There are things called draw calls, which are portions of information sent from the CPU to your GPU describing what to render. And the thing is, what you're seeing in any given frame isn't being sent to the GPU in one chunk. There is a multitude of factors that break everything into hundreds and potentially thousands of separate calls. If you want to render a textureless cube without lighting, that can be done with just one draw call. If you want to use a diffuse texture under simple ambient light, it would be two drawcalls: one for the geometry and texturing, and one for shading. Want to use a normal map? That's another two heavy draw calls. Want to use transparency? Add another one. Should the object cast shadows and receive shadows? Add two more! Now, guess what happens if an object is using 20 materials? The amount of draw calls adds up extremely quickly then, and your CPU can only send so much and your GPU can only receive so many before things start to slow down. Old buildings were using a multitude of materials: for example, the old Vehicle Assembly Building (VAB) interior used 16 materials (which wasn't even noticeable from surface resolution or material variety).

Third, the object count. Each model has to be drawn separately. For example. having a building consisting of five models, is better than having a building consisting of half a hundred (I'm leaving it to you to imagine how draw calls are multiplied in that case). Well, the old VAB interior was consisting of dozens of separate models, and some other objects were no better off.

Then, the visual style. Aforementioned wouldn't be as much of a problem if those buildings looked rad, but alas. Here are some issues with them:

Buildings were using vastly disproportionate elements, like glass industrial lamps on the VAB clocking three meters across, randomly scaled doors and 10 meter-high observation windows.

Elements lacking function added just for the sake of filling space with something, in the vain of "greeble" used to cover surfaces of sci-fi ships.

Unsatisfying overall quality from an architectural standpoint: problems with composition and color, lack of consistent elements like window and door systems, lack of ventilation, questionable structure, surfaces lacking contrast between high and low frequency detail.


![](../../assets/88e188c3f2405cc9.jpg)

![](../../assets/19ffd943f95e3675.jpg)

![](../../assets/d6ee0d45e8817323.jpg)


^ As a side note: most of the images there and from now on are clickable thumbnails that will lead you to high-res originals. Click them.

And finally, the quality of texturing. Uh-oh.

First, there was an extremely inconsistent texel density (which means that texture resolution varied wildly across the surfaces, with crystal-clear high-resolution metal seen right next to a muddy concrete stretched across hundreds of meters). Ideally, you should get exactly the same texture resolution per surface area everywhere: 512x512 per 8x8 meters, for example (that translates to 2x2m for 128x128 textures and so forth): that hugely helps to make everything look more consistent, and makes MIP mapping behave nicer. Sometimes it's unavoidable, like with the terrain system that's forced to operate on enormous scale, but there is no excuse not to make building models consistent in themselves.

Second, the quality of textures. Normal maps, if used, were hastily generated by an automatic filter with poor results. Diffuse textures contained puzzling detail. I vividly remember, for example, a photo of some small electric control panel stretched onto the whole height of an old launch tower, or strange green boxes each VAB "shelf" was stuffed with, with dials so large a kerbal could fit into them! Some stuff evidently used non-proportional transformations. No attempt was made to build a consistent color palette that works together in interiors, each texture was created without referencing others, which leads to a chaotic, unpleasant color set without any nice contrasts for the eye. Not a single specular map was used.


That's all I can remember off the bat. Now, I should say I'm not trying to bash the developer who originally did these models (and has long left the team), as making so much content was still a hard and long job that provided KSP with valuable placeholders to ride with for a long time. Stuff like that only deserves bashing and shaming if we as developers are convinced that nothing can be wrong and nothing should be changed. Thankfully that's not the case, and replacing those objects was long planned for. So it needed to happen. Now, how can you go about it?

Decisions, decisions

Okay, so now we know what needs to be fixed. What should I make, then? First building I needed to make was the new VAB (Vehicle (Vertical) Assembly Building). But a “place where tall stuff is being built” is an awfully generic description, so I needed ideas.

The old VAB gave me a hint. It loosely reminded me of something real, but I wasn't sure what that was. I Googled "VAB", and sure enough, found the original iconic NASA building from Cape Canaveral. The old VAB took the idea of door design from it, but not much else. What were some additional references beyond one of the most iconic buildings in the history of space programs? Well, there are some other things. Maybe the VAB should be more sci-fi looking? Or maybe it should be a ramshackle hut built from wood, scrap and duct tape, because it would be "so kerbal"? Or maybe the red-grey-white "style" of old buildings should be faithfully followed? Well, I don't think so, and let me build the case why.

Style of the old buildings. Well, two things about it. First of all, there already exists an established art style within KSP, and it has nothing to do with old buildings: the style of stock parts. It is defined by a few things. First, it is depicting modern pieces of technology like engines and electric equipment, built fairly competently and cleanly, with slight exaggeration of proportions. Second, it usually ignores too small high-frequency detail in favor of nice bulky minimal shapes. Third, it favors hand-painted detail and solid fills instead of gritty photo-sourced textures, and is using a particular color palette of grays, browns and whites, with occasional accents in other colors. It's a very consistent style, and it works well, fitting the characters and the world together. Now, the old buildings have nothing to do with it, actively clashing with the aforementioned things. They are using gritty photo-sourced textures one second and enormously stretched abstract fills another. They are using colors completely disconnected from the parts and don't have hand-painted detail. Most importantly, they are anything but sensible modern-age buildings. I have already explained a bit earlier all the flaws their style has, making it fairly bad choice if you want the game to be beautiful and consistent. With that I allowed myself to completely ignore the style of all old buildings and not reference a single thing from them. Onward to the next candidate!

Sci-fi! I have a history with sci-fi themed mods for the game, so something like [B9 Aerospace](http://forum.kerbalspaceprogram.com/showthread.php/25241-0-21-B9-Aerospace-Pack-R3-3-New-pods-IVAs-engines-fuselages-structures) themed hangar with faceted chrome walls, futuristic architecture and surgical lighting was somewhat expected from me. But no, thanks. The parts in the stock game are very obviously depicting a different technological era, so something that is consistent with them must be made. Modern era architecture is a very interesting place anyway, with tons of styles, interesting structural solutions and lots of fancy props you can use. So nope, no sci-fi, at least not until (and if) we get tech levels implemented. Tech levels could go both ways though, maybe I'll make a tiny garage-like VAB where your first rocket is made, as it makes little sense to have a NASA-scale facility in the beginning. But that's far into the future. So, next one.

It’s not Kerbal? *shrug* For some reason some people like to think Kerbals are sloppy engineers only capable of producing inherently broken designs held together by duct tape. To them, proposing something prim and proper like a NASA VAB could be built by Kerbals is ridiculous. Well, I disagree. Take a good look at the parts: at the [LV-N engine](http://wiki.kerbalspaceprogram.com/wiki/LV-N_Atomic_Rocket_Engine), at the [3-man pod](http://wiki.kerbalspaceprogram.com/wiki/Mk1-2_Command_Pod), at the landing legs, at the [ion engine](http://wiki.kerbalspaceprogram.com/wiki/PB-Ion_Electric_Propulsion_System). Those are cleanly executed pieces of impressive technology. Kerbals are indifferent to safety precautions and are very excited about explosions, yes, but they make an impression of extremely capable and very competent engineers. Sure, we know they probably turned a construction crane into a vomit carousel or raced on bulldozers in the process, but I don't doubt for one second they can build buildings similar to real ones, and I don't think it would be out of character for them. Plenty of other stuff like engines is fairly close to how our human rockets look. It's unfair to mistake Kerbals for orks from a “Certain Universe With 40k In The Name,” or to expect them to build sloppy duct-taped huts.

Overall, I'm convinced the obsession with disasters and perception of Kerbals as worthless engineers only caring about explosions is destructive for the game. KSP deserves much more than being a glorified disaster simulator where rockets falling apart and crews being killed is the prime entertainment and the only expected result. The achievements of players who strive to be successful, who create beautiful, well-engineered, reliable designs, should never be devalued, and the opinion that going to space is impossibly hard deserves to be crushed and disproved over and over again. Kerbals are capable engineers and it's up to the player to utilize their technology well.

This same mindset is harming the game in many other areas as well. The bugs of the physics system aren't there because we thought they would be fun and don't deserve to be defended as some players surprisingly do. The achievements of reaching orbit, landing on another body or even establishing a permanent base somewhere should not be perceived as something impossibly hard and unreachable for anyone but hardcore players. Everything is possible if you are willing to learn and there is no reason to restrict yourself to playing a disaster simulator with rocket cars or insta-exploding space planes. Justifying that to yourself by creating a certain mental image of Kerbal engineers competency might make the game better for you but I’m striving for a greater Kerbal good.

Now, I'm not opposed to having fun at all. For instance, I have nothing against the KSP trailers made by our Pixar-tier magician Daniel Rosas which often depict Kerbals ignoring safety and having good fun. Part of the charm of KSP is the opportunity to take enormous risks, ignore established paradigms and experiment freely, which can often lead to great successes and interesting stories to tell. That is not clashing in the slightest with the fact that you have nice, cleanly made, technologically impressive spacecraft parts available to you, or well-built buildings to assemble your creations in - all without any sign of duct tape, rust or sloppy welding. So, basically, I feel objects in the game should continue to be clean and well-built to be consistent with the existing art style, and I'm convinced reinforcing the widespread opinion of Kerbals being incompetent is very harmful for the game. So there you have it.

So, we are left with the realization that using a real reference for the VAB is a good choice. Though, replicating it precisely isn't really a good way. So I have paid close attention to the existing art style of KSP that is most exhibited in the spacecraft parts that are available, and created a building inspired by the NASA VAB with some important differences in mind:

No gritty photo-textures: Every texture is painted manually and lacks rough noisy definition, instead relying on exaggerated highlights, seams and solid color fills.

No overwhelming high-frequency detail like wires and overpopulated rooftops: I have only left clean, clearly defined props like bulky HVAC systems.

Proportions were changed to fit for Kerbals, with door sizes, floor & window heights and ladders created accordingly.

More dense, self-sufficient composition: A real VAB is surrounded with dozens of buildings. I have condensed it into a solid structure that looks better as a defined element of a space center.

Doors: The original VAB could hold 4 rockets assembled simultaneously. In KSP, we only need one. But why cut the remaining 3/4th of space? So I give all volume inside of the tower to one giant assembly hall, with the door of the fitting size sitting on one side.

Symmetry is boring. Why leave the doors on both sides? So I have replaced one side with a giant window that allows us to spice the variety up and make the lighting in the interior very interesting.


So, with reference chosen, execution style set and with new ideas in mind, VAB modeling started. We finally get to click onto more pictures too.

Building the building

![](../../assets/56e83192e6985a05.jpg)


So, first, you need to decide whether to make an interior or exterior model first. As the VAB is an example of the industrial, functionalist architecture, the form of it is dictated by function. Therefore, it makes sense to begin with an interior that will contain stuff like structural supports, and then move onto the exterior with confidence your shapes represent the contents of the building properly. Now, when you don't have a good knowledge of things such as architectural standards, typical proportions, structural support types and so on, it's good to have some sort of reference, preferably photography. Well, even if you do (I, for instance, have spent years and years making models of the rusty buildings for unofficial Stalker mods and memorized tons of Soviet construction standards in the process - not that it will help much here). Aimlessly wandering is no good. So I've searched for interior photos of NASA VAB and, while, obviously, its interior proportions are very different (the real building is housing four assembly halls instead of one), it gave me a few good ideas.![](../../assets/1c1d6918886c4c2e.jpg)


The first thing you can notice is it basically has two layers. There is, of course, a boring solid vertical wall, but before it, with a significant offset giving space to the floor areas, stands a layer of structural supports comprised of repeating square sections. That's a very good feature. Overall, the use of modular geometry is very widespread in game-oriented modeling. Every single game from Bethesda, Valve, Epic and many other AAA dev teams is using this approach. Working with a grid and compatible elements is a very useful trick that allows you to save time, have lots of detail, and leave a lot of room for revisions. So it was a no-brainer to use, especially when I was unsure what scale would work best, whether the height should be 50, 60 or 100 meters, and so on - so the ability to quickly rework things was crucial. So, first, I created a modular set of those structural supports aligned onto the 8x8m grid:![](../../assets/b78fdd483925246d.jpg)


These meshes have to be extremely optimized as they will be reused hundreds of times over as floors grow wider and stack higher. One of the tricks here is not to create any faces on the back, which faces the wall where players won’t be able to look. ![](../../assets/72b20d01c42ae1f2.jpg)


Next, I build vertical stacks out of that part set. In the end, I decided on a 96 meter-high assembly hall, which is twice the height of the original VAB interior. That makes precisely twelve 8 meter-high floors. To spice things up on the horizontal direction, I replaced two stacks with recessed shafts for elevator platforms. So, everything on the structural layer is built using these three basic vertical elements:![](../../assets/d6ebb0eb333b2d3b.jpg)


Now, time to make the walls, floors, left/right/top/down pieces surrounding the supports, and basic shapes filling the floors behind the structural supports. Those are, again, comprised of repeating modular components: top and down sections comprised of two types of 8 meter-wide "lips" (one simple and one with elevator shaft opening), vertical borders built from 16 meter-high sections, three basic shapes of "boxes" that populate the floors and are used together to make something different on each level, and so on. Ah, and I can’t forget ladders and railings. Ladders are, again, modular objects comprised of 4 meter-high sections, and railings are sub-objects assigned to floor objects. Also, one of the higher floors has double the height, 16 meters, to add more variety to the looks:![](../../assets/5d9e0424dacf4038.jpg)


Next, it was time to decide on the horizontal dimensions and close the interior. As my walls are 64 meters-wide, that became the length of the floor. The width of it was set instead to 48 meters, as a square floor would look lame from an architectural standpoint, and would require a pretty ridiculous door width to be used. Some more space adds up from recessed galleries surrounding the floor. Then, a bright idea appeared: why not ditch the symmetrical layout of the old VAB? Having two identical doors is quite a boring sight, especially when there is no point in another one as there is only one spacecraft and one launch pad involved at a time. And why not add a huge window in place of it? As mentioned earlier, it is assembled from 8x8 meter blocks of three types (opaque wall, windows themselves and the gate), then covered with one layer of structural supports adhering to the same grid, and covered with modular walkways and ladders. That window construction allowed for much more interesting lighting and greatly improved the look of the VAB. And it also allowed for a very logical addition – the doors can be closed for prolonged periods of time, while the translucent wall lets light in no matter the weather nor time of year. Not to mention, completely artificial lighting is going to leave your space agency some chilling electric bills if you want to reliably flood all that enormous volume with the doors closed and pitch black darkness rising inside. So, sunlight it is! Next, I added a roof with a forest of horizontal structural supports (again, everything is modular to allow easy altering). It's a bit boring to have a dark and flat ceiling, so I decide to add four windows there, which comes in very handy later when I will need ideas on roof decoration. And finally, we have a structure that's starting to shape up as a usable interior scene:![](../../assets/34c2a1537f2e2aaf.jpg)


Time to glue it together. Next, I'm making a set of modular props. The building needs some clutter, lots of small objects like crates, lights, machinery, color accents to liven it up, so it's a very important part of work that's as hard and demanding as making a whole set of new rocket parts. In the end, I decide on this set:![](../../assets/30f70863e381a0c4.png)


It has multiple varieties of wooden and metal crates scaled to be reminiscent of part sizes (they have to be housed somewhere, right?), unpacked empty sections of 1.25 meter and 2.5 meter standard hulls, some machinery, a large set of various transport and service vehicles (smaller ones can ride elevator platforms, large ones deliver parts from outside), and some floodlights (not depicted there). As with modular structural supports, it's extremely important to keep props as optimized as possible, as they will be reused over and over and piled into huge groups. Once props are done, I make a few separate objects containing all the clutter, comprised of a few hundred of those props:![](../../assets/18dfa577003d9872.jpg)


Once those are done, I combine them together. Phew, finally.![](../../assets/4e7d707716f4c0eb.jpg)


Ah, nope, we're not done. I have made those screenshots by disassembling the final model, so everything above was textured. I didn’t have the luxury when I first modeled that interior, as everything was white and empty. So, how was texturing done?

You're texturing it where?!

Those of you familiar with 3D modeling are probably pretty disturbed by this point because they have recognized the familiar viewport and UI and know what software I used. They have that crawling sensation under their skin. Oh god, that's right, it's SketchUp. Why the hell would anyone use that for any serious work and, most importantly, how the hell would you texture anything in it when proper texturing tools don't even exist there? Well...![](../../assets/3cba9798158e4fbd.jpg)


I'll be doing a separate devblog on the subject of using SketchUp for game development later, so let's just focus on a short version.

First, SketchUp has indeed gathered a reputation of a problematic choice for 3d modeling, with models of abysmal quality inhabiting 3D Warehouse and horror stories of conversion attempts flooding forums of many game engines. SketchUp has a reputation of a software that's only capable of producing inherently broken, unoptimized and dirty geometry that's unfit for use as game art. Well, surprise, that's untrue. The problem lies in the fact that SketchUp is just so well designed and so easy to start with that lots of users jump into modeling straight away, prior to learning about any optimization techniques, general modeling rules, and so on (which is generally not a bad thing unless it involves someone else trying to use the resulting models). So when they make e.g. a house model, they rely on horrifying boolean extrusions, ignore surface normals and edge smoothing, then cover the result with some ultra-lossy JPEG juice from standard material library and publish that work to aforementioned 3D Warehouse where Mr. John Brown, an esteemed and imaginary game developer and professional 3d artist, finds this horror and dies from heart stroke.![](../../assets/ea6ee070dc6ec24d.jpg)


But it doesn't have to be like that! SketchUp is a modeling package just like the others, and all the general rules of 3D modeling are still applied there. You must keep an eye on surface orientation, you must optimize your model, keep neatly organized component hierarchy, avoid boolean operations, etc. The program won't magically solve all these issues for you. And once you work cleanly, you will start getting clean results. All models in the B9 Aerospace Pack (with the exception of the last engines modeled by Taverius) were made in SketchUp, and it isn’t all that obvious. Every single building and detail of the interior in the latest update were done there too. Again, I'll expand on the process later. Okay, SketchUp is convenient and nice, - for now, let's switch to a more important question of texturing.

The old VAB interior was using 16 materials, which, as we have already discussed earlier, was not very nice for performance, especially considering the amount of separate meshes there. The new one is using three: ![](../../assets/b7a4c643629ece1b.png)


A large texture atlas for all main surfaces like walls, supports, floor, windows, ladders, etc.

Another, smaller texture atlas for small props like trucks, crates, lamps, toolboxes, etc. (additionally, it's reused in the SPH interior scene)

And a transparent texture for spotlights and other fake light sprites used to enhance the scene (also reused in SPH interior scene).


Those textures are called unwraps and contain every single unique surface of the model. Every one who has used SketchUp also knows that this type of texture mapping is completely absent from it, requiring an advanced editor like Unwrap UVW from 3ds Max, which just doesn't exist. What the hell? Well, a few years ago I was particularly lazy to leave the cozy interface of SU for another unwrap, so I came up with an exotic workaround that allowed me to make textures and mapping like that without using external packages.![](../../assets/20e8f92b5e1fdf80.jpg)


Essentially, I set up a bounding box, manually rip every single surface I need to be present on the layout from the model, condense them into the smallest possible layout with some Tetris-like exercises, and render the resulting mess with 2d camera in wireframe mode, into the resolution I want (for the main VAB layout that was 2048x2048).

Here is another example, for another, less complex model. ![](../../assets/2a9cf92849206087.jpg)


And, if you are still not asleep, here is the layout I have used for those trucks and crates:![](../../assets/161e8f8afb24b645.jpg)


After getting that out of the way, we drop the model with the textures into Unity and get a lovely result that looks just like promotional screenshots we have released. Oh wait, we don't.

THE RIDE NEVER ENDS

Let's take a deep breath and look back at old VAB & SPH interiors for a moment. Notice anything bad about the lighting specifically?![](../../assets/b2bf5ff5958400bb.jpg)


Well, the lighting is less than ideal. Here is why:

The lighting consists of a directional light source (faked sun) and an ambient light (level of brightness all surfaces get even when unlit). Nice combo for Quake 1, but not really something that's showcasing geometry nicely: surfaces are only being lit from one side, so half of the geometry detail remains invisible without being highlighted differently. A properly lit scene should have every single point illuminated from at least two directions to create a good interplay of light on surfaces. So, maybe that could be solved by adding a second directional light?

No it cannot. Look at those shadows! Those are the best shadows our renderer can offer, and they are alright for stuff like being casted from Kerbals onto the grass. There are a few glaring, unacceptable limitations to traditional shadows that make them unsuitable here. First, they are perfectly sharp, without any penumbra being simulated. Second, they are stencil, flat, completely monotonous fills the geometry gets flooded with - which has almost nothing to do with how real shadows look. This means that the ceiling of the room will never be fading softly into the dark while lower floors are enjoying bright sunlight with faint shadows: everything gets the same masked fill. That just won’t work!

Next, the amount of lights needs to be improved. Right now we can only use up to 8 per-pixel light sources, everything over the limit then falls back to hideous per-vertex lighting mode. Lower quality settings are only using one per-pixel light, or none at all. One of those limited light sources is already occupied: it's the light that has to illuminate parts added to the scene. Now, good looking interior needs rich lighting, potentially hundreds of light sources. Goog luck trying to decorate everything with just a few. All and all, you will end up with a gray boring room at best, and with messy, jagged, vertex-lit room at worst. Old rooms were already reaching those limits.

And finally, there is a complete lack of proper global illumination, ambient occlusion, radiosity, translucent surfaces and other important effects, which leaves us with a completely flat picture that's not just unrealistic, it also fails to showcase the geometry properly. That leaves us to guess whether crates are touching the floor or floating ten meters into the air above it.


But what are our options? Changing the renderer to deferred is tempting as it theoretically allows an unlimited amount of per-pixel light sources, but that is not an option because KSP is using a multi-camera setup that will never work with it properly. Settling for the mediocre current lighting won't do either. Well, there is one more way. Aren't VAB and SPH interiors almost completely static, with gates always open, outdoors predefined, and walls unmovable? Well, then we can cheat out of using real-time lighting completely: by precalculating some extremely fancy lighting and storing it in the lightmaps. It's an old and proven technique that was constantly evolving from the beginning when games couldn't use real-time lighting, growing and improving alongside it. While some engines like CE3 opt to have completely real-time lighting, many others are relying on precomputed lighting, notable examples being UE3 and Frostbite. As we aren't developing a Martian rebellion simulator with building destruction (for now, at least), and both the geometry and lighting conditions are predefined and static, it's a fairly good option.![](../../assets/12a8dfcae06eb5a8.png)

![](../../assets/5de7751add17e3a7.png)

![](../../assets/a62386c3115b8f01.png)

![](../../assets/76c7f3e9d6f2499c.png)


Unity has a very powerful and easy to use integrated solution for precomputed lighting, which I put to use. First, you need to set up all light sources you want to be baked into the lightmap. No restrictions on anything this time. So, I have gone bananas with detail, adding wide variety of lights onto the floors, around static vehicles, using around a hundred of lights to simulate translucency of windows, and so on. ![](../../assets/2b399591cede478f.jpg)


Then, add a variety of parameters like strength of global illumination, amount of bounces, lightmap resolution and other things that need to be configured. All of that work takes the whole day in the best case, and we finally were able to press the "Bake" button. So of course, that meant I need to watch my poor PC choke for about half an hour while managing insanely complex calculations. There is a good reason why that kind of lighting quality is not available at real time. But in the end, the result is worth it:![](../../assets/590e9f3722ed11bd.png)

![](../../assets/324076d55b2aa8f2.png)

![](../../assets/bc652aa22c064874.png)

![](../../assets/17758a77c020e4a0.png)


Although guess what? I'm still not satisfied. Lightmaps are limited by resolution, which you need to restrict yourself with to save the memory of the players. I have used only two 1024x1024px maps for the VAB and one 2048x2048px map for the SPH. Going higher was unreasonable, even though I wanted smaller detail like tiny corridor lamps and nice detailed floodlights. Thankfully, there is a solution for that:![](../../assets/652e088bd54957fe.jpg)


I'm imitating small light sources and volumetric light with the sprite sheet I showed earlier! That allowed me to use high-resolution detail. The only problem is every single sprite will have the same intensity, opacity and color, which isn't nice. A solution for that was found too. I created a looped animation which overrides the parameters for each sub-object of the assembly separately, turning one array to blue, toning down opacity of another object to 50%, and so forth. The same animation also allowed me to add nice subtle effects like flickering floodlights.

Phew. Are we done yet?

Almost. One last thing is we have a few dynamic, moving objects in the interior scenes, such as, parts, Kerbals walking around and animated trucks. They can't use lightmaps, and they can't be affected by anything depicted in lightmaps of the surrounding environment, but we would really like them to be grounded into the scene. So, we create a shadow casting light source, like the one used in our old VAB and SPH. But this time, we set it to affect only the objects I listed above. The one problem with this is shadows can't be properly casted onto the lightmapped floor. So here is a little trick we used: we created a plane situated a tiny bit above the floor, with the special shader Felipe Falanghe (HarvesteR) wrote that handles it. The shader makes the plane completely invisible, but receives all shadows onto itself, thus leaving all lightmapped geometry free from any interference:![](../../assets/3a6c495b6e4c6eee.jpg)


Another thing we worked on was exterior lighting. Old scenes had a directional light acting as a sun, so terrain stretching into the horizon was evenly lit and shadows of the building were coarse and sharp. We didn’t want such a view to spoil things outside of our beautiful interior, so another trick is used. Instead of uniformly distributed directional sunlight I create a spotlight, much similar to ones you have in the part list, but with much higher intensity and extreme effective range, around 1000 meters. This spotlight is then used to illuminate the exterior outside of the doors. The circular nature of it is not visible with the very narrow field we have available looking through the doors, so the whole thing looks like real sun is producing a very soft shadow of the building and the light is softly fading away into the fog in the distance:![](../../assets/f53f0c9cf8f30a02.jpg)


And with that, finally, we are done with interiors!

I don't want to go out

As I have mentioned before, as we have an industrial/functionalist building, the shape of the exterior is defined by the shape and function of the interior. So, first, I built a rough shape that will enclose the interior while loosely resembling the NASA VAB:![](../../assets/15983e926b35fd8a.jpg)


It's very easy to get stuck at this point, because there is too much you can do and it's extremely easy to end in a place similar to the old buildings, spending your time covering surfaces with meaningless extrusions and trying to come up with detail for the sake of detail. To avoid that, we wanted to establish rules. The more rules and standardized systems you have, the better. They will guide you and your object will start taking shape. ![](../../assets/0daf6d7e4bbb479c.jpg)


The very first rules was the grid: I decided every single thing in the model had to be snapped to the grid with the step of 1 meter.

Then, I decided on the texel density: it would be 64px per meter. This level had to be consistent across every single surface for the buildings to look good both from afar and up close.

From texel density requirements arose textures. The most optimal choice that allowed most varied detail for reasonable file size was using 512x512 textures with an 8x8 meter area. Some were smaller, though, as monotonous surfaces like asphalt can get away with using small textures without noticeable tiling.

Next, you need to create guidelines for yourself to govern the sizes, offsets and types of windows and doors. What greatly helped there was the strict grid and seams established by tile textures.

From those guidelines, you can go off to create a set of ready-to-use windows, doors, grates, gates, ladders and combined objects that you can quickly place around the building without wasting time on remodeling each time.

And finally, you need a system of versatile props so you won't have to drag yourself into modeling meaningless greeble whenever you need high-frequency detail. For me it was a set of HVAC objects.


Let's take a bit closer look at the materials and props I have used.

As you remember, old buildings weren't particularly optimized in terms of textures and materials, so I made it a point to use as few materials as efficiently as possible. First and foremost, that meant creating textures that could be used for multiple buildings, not just the VAB. So, here are the materials used for every exterior building model:![](../../assets/3c547b0bb5b90f59.png)


I decided to use an approach similar to one found in Valve levels, where you are working on a clean grid with tiled textures that have strictly defined real sizes. It's possible to push everything further into, let's say, three materials, but I opted for a sensible compromise. Storing everything in a single texture wouldn't have allowed to use the same, almost FPS-like resolution on walls, and would have necessitated much higher polycounts because of how mapping of texture atlases works. For example, I would have been forced to split VAB wall into hundreds of separate squares to translate the tiles onto the surface. With my setup, two polygons are often enough.

With efficient and quick texture mapping tools in SketchUp, it's easy to start texturing before you're even finished with geometry, which, when you have grid-adherent textures like those, helps you to come up with ideas for the shapes. You set extrusion borders to match tile seams, place windows within tile rows and so on. Next, you need some props. Vertical walls have high-frequency detail covered by walls and windows, so it was the roof that was the most glaringly empty surface. It was especially important as many players like to land onto the building roofs and otherwise explore them, so some good detail was needed there. After some thinking, creating a set of HVAC props was the most obvious choice. So, that's what I created, and again, with the same optimized atlas texturing that allowed the use of only one texture for lots of different objects, thus saving drawcalls and memory.![](../../assets/a6ecf5bbb0cc7096.jpg)

![](../../assets/5f2dbfdaa59d9817.jpg)

![](../../assets/f46ad29f77c96625.jpg)


Then we have the doors, windows, stairs and grates mapped with another texture atlas you saw above.![](../../assets/38b3e9680a71e624.jpg)


Are we done yet? Almost there. As the exterior is forced to work with fully dynamic lighting, it can't resort to lightmaps and precomputed lighting for fancy ambient occlusion. So, I came up with another solution: blended decals! Mike Geelan (Mu) wrote a set of great decal shaders (diffuse, additive, multiply) which I have used for a few things, most important of those being decals imitating a basic ambient occlusion.![](../../assets/0e7e94cd7050373f.jpg)

![](../../assets/8d536f968a4cd474.jpg)

![](../../assets/d4fa9b495d711e18.jpg)


And with that, we are finally, finally done with both exteriors and interiors. Or are we?

How about you stop

Not yet. While buildings themselves are done, there are few more things needed to make a proper scene.

First, we need to create surrounding ground models with pathways, lawns and roads for each building, because leaving a building right in the middle of terrain surface is bad for texel density consistency. It's nice when the ground surrounding the building has the same texture resolution as the walls that go into it, even if you have to move onto inherently less-detailed terrain a bit further.![](../../assets/3ce13ef329c19c68.jpg)


To liven the roads up a bit we need to somehow paint stuff like line markings on them. Obviously that can't be done over the asphalt texture itself, which is just a small square that gets repeated thousands of times over those varied shapes. Initially I have intended to use decals, like ones used on vertical surfaces of the buildings for AO and highlights such as the ones used on the SPH floor for all those lines. But exterior ground surface has one important difference: it's being observed from insane range of distances, from extreme close ups when Kerbals traverse the place on foot to dozens of kilometers in flight. Tests, though, have demonstrated that writing a decal shader that would be reliably sorted properly over that whole range is nearly impossible.![](../../assets/b0eeae0442ee0b8f.jpg)


So something different had to be used. Our solution was to make cutouts in the road mesh and fill them with modeled markings using a simple diffuse texture. No transparency and no sorting issues this way at a cost of few hundred additional polygons:![](../../assets/fe61db16d40fd65a.jpg)


Next, we need the Crawlerway to connect the VAB to the launch pad. While serving no functional role at the moment, it's an important model for the space center to look complete, and leaving an old ugly decal was not an option. The Crawlerway was molded by a few obvious requirements. It had to fit the VAB, it had to fit the launch pad that was modeled without any knowledge of a new VAB, and it had to have minimal depth-sorting issues. In the end, the compromise between those requirements gave birth to this model which, I must add, haven't required even one additional texture to be created:![](../../assets/6142dc9d3d41ff3a.jpg)


Now, we have only one final problem left. While the space center looks good during the daytime, it looks quite strange at night without exhibiting any sign of life in the pitch black windows. How about lighting it up? Thankfully, a solution exists - emissive textures and animations! First, I needed to draw a mask that will show which areas of the relevant textures you want to ignore the lighting and stay bright. Then, I created an animation that turned the effect on and off in a loop:![](../../assets/f5d39cd363d1942f.jpg)


And finally, Mike Geelan (Mu) wrote a script that used that animation and, similar to how heat animations on engines work, forced the space center to use certain places of the animation depending on the time of day. With that done, the space center finally lit up at night. Now, there are limitations to this approach. All emissive effect does is change the appearance of certain parts of a texture. You don't get glow showing up outside the shape of an object, you don't get flares (those are all separate effects that have to be coded additionally), but most importantly, nothing gets illuminated when you get close to those windows, because emissive textures are not light sources, much like in every other game you see illuminated windows in. Unfortunately, using real light sources for windows is completely cost-prohibitive, even on deferred renderers, not to mention the forward rendering we are using where even a dozen of per-pixel lights being displayed simultaneously is a rare occurrence. Area lights and true light-emitting materials are, unfortunately, effects that can only be properly achieved with more advanced, next-gen technology like UE4, and you'll have to wait for something like that to appear in games for a few more years. We have plans for more night time effects though, in particular adding a flare system for the runway lights and warning lights on top of the buildings. It will render unlit sprites that will face the camera and sort above other geometry, which will finally be an effect that's not constrained by bounds of building models and will be visible from far away. Until then, using emissive materials and animation will do and livens up the space center quite nicely.![](../../assets/be75a5e8f73e210a.jpg)


One other interesting bit was the tracking center. The most notable thing about it is the beautiful animated dishes that were modeled by Chad Jenkins (C7) and are controlled by another script written by Mu: they randomly select a target in the sky, track it for a while, then move onto the next. Inspired by timelapses of real radar arrays, that was really great touch. As mentioned previously, my input there consisted of making the central control building, the ground plane, and the texture for the dishes.![](../../assets/c8014f0625b99646.jpg)


And with that, we can finally conclude the development of the space center.

Wow, it's over?

Yeah. So, the space center is complete and ready for use. While I had to drop some of the details like spaceplane hangar interior modeling and crew/tracking buildings’ exterior creation (I'm sure you're thankful I did), I believe all of this should offer a fairly complete understanding of our development process for the new content like that. I think it was worth it and hope you liked the results!![](../../assets/878fb60aa95be7af.jpg)


What's next? Well, I'm sure I'll find [something](http://i.imgur.com/xD1RUuF.jpg) to do: there are plenty of scenery assets left in dire need of reworking, plenty of additional content requirements born with ever-expanding features like career mode, and an enormous task of reworking most of the part sets looming ahead. It's going to be fun.

For now, have a good day or enjoy a nap (admit it, you want to).