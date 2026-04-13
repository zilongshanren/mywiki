---
title: The Starting Point for a Train Game with Freeform Tracks
url: http://www.learn-cocos2d.com/2012/07/starting-point-train-game-freeform-tracks/
author: Amit Patel says
published: '2012-07-12'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

If you ever wanted to build your own 2D top-down view train driving game, here’s … well, the things you need to consider plus a rudimentary source code example. Because a train following tracks is not as simple as it might seem, unless you restrict curves and switches to 90° angles and allow only very short cars and locomotives.

Here’s a video of my [example project](https://github.com/LearnCocos2D/LearnCocos2D/tree/master/RailCarDrivingOnTrackTest). Any stuttering is due to the screen recording software taking a toll on my system combined with the video playback framerate not rendering 60 fps (I assume it’s the standard 24 or 30 fps for Youtube videos). The video shows a sequence of three runs with a medium curve radius, a large curve radius and a ridiculously small curve radius. The yellow line indicates the track being followed by the axles, the purple line indicates the car chassis position (center point between axles).



#### The Type of Train Game That’s Wayyyyy Overdone

Before I start, let me show you a collection of screenshots of the type of train games that are overdone and not considered in this article. ![train games](../../../wordpress/wp-content/uploads/train-games-300x200.png)


All 20 games are tile-based train games with 90° curves (minus one exception allowing 45° tracks). All of them are puzzle games. Most follow either the “lay down tracks à la Pipe Dreams” design or the “guide train to right destination” design. These are the Match-3 games of trains. Click on the image to see it enlarged (1500×1000).

Please promise you won’t make any more of those, ok?

I like to mention that [Trainyard](http://trainyard.ca/) (top left corner) is by far the most entertaining, most innovative of the bunch. It’s the reference game for tile-based train games. You’d have to top that to make a splash with yet another grid-based train game. I also found [Train Master](http://itunes.apple.com/app/train-master/id343903943?mt=8) enjoyable. Maybe it’s because the 45° angle tracks make it look a lot more believable than the rest.

#### The Type of Train Games I’d Like to See More of …

Unfortunately there are only very few iOS games that feature free-form tracks with a natural variation of curves.![freeform track train games](../../../wordpress/wp-content/uploads/freeform-track-train-games-144x300.png)


I found three. See the image to the right. From top to bottom, the freeform track train games are:

[Railway Control](http://itunes.apple.com/app/railway-control/id486113784?mt=8)- yes, you guessed it: it’s[Flight Control](http://itunes.apple.com/app/flight-control/id306220440?mt=8)on rails![Build a Train (iPad)](../../assets/409c84b6b33d1626.img)([Free Lite Version](http://itunes.apple.com/app/build-a-train-lite/id423884330?mt=8)) - kid game where you drive around the track to collect crates from the stations. Every crate gives you 50 points, with enough points you unlock a few more levels.[Loco Train (iPad)](http://itunes.apple.com/app/loco-train-christmas-edition/id469489301?mt=8)- a variation of the classic[Tumble Bugs](http://www.wildfire.com.au/content/standard.asp?name=Tumblebugs)game.

That’s an impressive 20:3 for the tile-based train games. How come?

#### There’s a Reason why Free-Form Track Train Games are Rare!

Tile-based train games are trivial to make and … why are you raising your fist … hey wait … you aren’t … aaaaah!

I mean of course technically trivial: laying the tracks and getting trains to move over them. Not the actual gameplay, and artwork, user interfaces, levels, and everything else there is. And when compared to freeform tracks - they’re hard to do. And they’re even harder to do correctly - I’ll scratch on the surface of these issues in this article.

Build a Train is actually a nice game if it weren’t for the awful rail car animation. This inspired me and got me thinking what needs to be done in order to get a relatively long, 2-axle rail car across curves so that the axles stay on the track, not just the center or either end of the car.![](../../../ucpressebooks/data/13030/zn/ft4489n8zn/figures/ft4489n8zn_00018.gif)


In Build a Train, the cars are centered on the track near the rear end of each car, which means the front end isn’t on the track in tight curves. In addition to that the trains don’t move smoothly, as if the curves aren’t truly curves but approximated through a series of straight lines, as exemplified by the picture to the right.

#### Oh Cool, Let’s Use Bezier Curves!

First of all, if you think [bezier curves](https://en.wikipedia.org/wiki/Bézier_curve) (or splines in general) - stop!

Train tracks using bezier curves might look good, but technically it is extremely challenging to get a train moving over a bezier curve at a constant speed. [Read this](http://community.spinxengine.com/content/19-constant-speed-cubic-spline-interpolation.html) and if it didn’t make you want to throw up mentally, maybe you are up to the task? But still, real tracks aren’t modelled with bezier curves anyway, they use [Euler/Cornu spirals](https://en.wikipedia.org/wiki/Cornu_spiral).

An additional problem occurs when you want to connect two bezier curves together. They don’t usually match up. Check out ![Screen Shot 2012-07-11 at 14.47.10](../../../wordpress/wp-content/uploads/Screen-Shot-2012-07-11-at-14.47.10-300x215.png)


[Amit’s road test](http://theory.stanford.edu/~amitp/_test/demo_roads.swf)Flash app from

[this article](http://theory.stanford.edu/~amitp/game-programming/road-applet/roads.html). In the screenshot of the road test app you can see a bezier track to the left (notice the gap) and to the right is a track that uses a simple circular curve. It’s solvable if the bezier curves can only connect at predefined angles but that kind of defies the purpose, doesn’t it?

As [suggested here](http://gamedev.stackexchange.com/questions/504/what-are-some-methods-to-represent-train-tracks) my suspicion against bezier curves were quickly confirmed. My first intuition was to copy the track geometry of a popular model rail track system, like the [Märklin C-Tracks (PDF, it’s german but there’s pictures in it!)](http://www.maerklin.de/media.php/de/pdfs/c-gleis_kataloginfo.pdf). This track geometry uses curves with strictly defined radii and lengths/angles, so that any 6 curve tracks of any radius put together form a 180° curve.

But since we’re on computers, we don’t even need to consider fixed track radius or fixed length/angle. As long as one piece uses the same radius, we can extend and shrink it as much as we want. And we’re free to use any radius for each individual track piece. That way, you can build a freeform and almost bezier-like track but you still reap the benefit of every curve being a part of a circle’s circumference, thus being able to use the [relatively simple algorithms for uniform circular motion](https://en.wikipedia.org/wiki/Circular_motion).

It’s also noteworthy that when you use this approach, straight tracks can be treated like a variation of a curved track but with a 0° angle and an infinite radius. That might make a couple things easier, as you could seamlessly bend a straight into a curve and back. Probably doesn’t have a real-world application but may be useful for a track editor.

#### How to Model a Top-Down View of a Train with Box2D or Chipmunk?

Not at all. Don’t attempt to use a 2D physics engine, it won’t work. Although this is about modelling a 2D top-down view of a train game, a 2D physics engine is simply missing one crucial dimension.

First of all, you can’t have gravity acting on the train, because it would have to act in a dimension that the 2D physics engines don’t know about. You can have gravity pull the train to any side of the screen, but never downwards onto the tracks. For the same reason you can’t model the train’s wheels either. The only thing where a 2D physics engine would work is for connecting the rail cars with joints, and possibly train collisions.

To put it simply: a 2D physics engine knows the two dimensions left/right (X) and top/bottom (Y). But it doesn’t have the dimension from the viewpoint of the player straight downwards onto the tracks - the Z dimension. That’s the missing third dimension, and the main reason why you wouldn’t want to use a 2D physics engine to model train movements in a game with a top-down view.

A 3D physics engine might work but seems like overkill for a 2D game. Especially if you want to take it so far as to model the individual tracks and the wheels accelerating the train through torque.

You’ll be facing similar issues if you attempted to model a top-down view car racing game like Super Cars with 2D physics. It’ll work better only because you’re not restricting the car to a railtrack, but a race track on which the car can practically go wherever physics takes it. In some games even past the track. ![](../../../images/shots/l/76922-supercars-amiga-screenshot-class-3-track-9-alone-against-all.png)


Forcing physics onto rails however is rarely a good idea. From my (only for research of course) experience with Rail Simulators I would say even the big name Railroad Simulators’ physics engines cheat a lot. Check out the [Open Rails](http://www.openrails.org/) source code, I’m sure you’ll find oversimplifications and cheats and tweaks to make things work (better).

#### The Many Issues of Train Movement over Freeform Tracks

- Each rail car has two axles. Both need to be on track all the time. You shouldn’t treat the rail car as a single unit or it won’t look as if it’s driving on the track in curves. You can only get away with this if all cars and locomotives are very short, like the car in the B/W image.
- The rail car’s chassis must be placed at the center point between the two axles, and rotated so it is parallel to the vector between the two axles.
- While crossing from a straight track to a curved track, linear velocity must be translated to angular velocity. And vice versa.
- If train moves at 10 units per frame, but axle enters next track piece after 3 units, you need to carry over the remaining 7 units of movement to the next track, while possibly converting it from/to linear or angular velocity. If the train is moving fast over many tiny track pieces, you may have to carry over the remaining velocity from track piece to track piece multiple times in a frame. You can only get away with not doing that if your trains move slowly. Really slow.
- Rendering the train track should be done with textured polygons to support arbitrary curves (
[CCMotionStreak](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_motion_streak/)probably won’t do without modifications). You also need to do two passes: render the track bed and ties first, then render the rails on top of that. Without the two-pass approach junctions and crossings will not look good. You could also use OpenGL primitives for rails and ties, ie lines in various shapes and sizes. Just rendering a series of sprites won’t cut it because they won’t align well enough to create a believable curved track, and you might have to draw hundreds of sprites which could easily kill performance.

Advanced challenges that may or may not be important depending on the game and desired level of realism.![](../../../wikipedia/commons/thumb/2/2d/Waldbahn_VT_15_jpg/800px-Waldbahn_VT_15.jpg)


- Splines and Bezier Curves are very difficult to move along at a constant speed. See paragraph above.
- Taking car masses into consideration opens up a whole new level of complexity, unless you only use the mass as an additional factor for acceleration and max speed of the train. Since these are factors (multipliers) you can apply them easily without a physics engine. Everything else concerning mass, like derailing due to speeding in tight corners with a heavy train, should not be considered.
- The distance between each car’s axles is fixed. At least it should be. But since one axle enters a curve before the other, the distance may actually deviate if this isn’t accounted for. The deviation may or may not be negligible. To fix this, you could move the leading axle first, then place the rear axle on the tracks at the exact axle distance. You could even apply this process to the entire train. Problem will be finding the right track to put the rear end on. The leading axle may need to keep a list of track pieces it has passed over recently so that only those are considered for placement of the rear axle. This approach requires a minimum curve radius that is greater than the longest axle distance of any car, otherwise the rear-end axle placement code will fail and the rear end might not actually take the curve but travel backwards on the track. Besides such tight curves look completely unrealistic.
- If rail cars are coupled together at their axles, the above must be solved or the distance between cars may deviate noticeably. In all other cases coupling cars in a way that makes sense and looks good will need some tweaking, and it can not be a fixed distance. Couplings require room for movement as rail cars are further apart in curves than they are on straights.
- A train does not start moving all at once. If the locomotive starts pulling the train, all the cars follow with a slight delay as the couplings are stretched to their maximum extents one by one. The same goes for stopping. Once the loco has stopped, the rear cars will still be pushing the train together before coming to rest. Exemption: modern power trains such the german
[ICE](https://en.wikipedia.org/wiki/Intercity-Express)or french[TGV](https://en.wikipedia.org/wiki/Tgv)or japanese[Shinkansen](https://en.wikipedia.org/wiki/Shinkansen)where most or all axles are motorized. For these modern trains like ICE, TGV etc. you may want to model the![](../../../wikipedia/commons/thumb/b/bc/Schematic_Jakobs_bogie_svg/220px-Schematic_Jakobs_bogie.svg.png)

[Jakobs Bogie](https://en.wikipedia.org/wiki/Jakobs_bogie)where the axle is between two cars and connects them together. See the schematic to the right.- Uniform circular motion has trains moving faster over a curve the larger the curve’s radius. The time it takes to do a full revelation remains constant regardless of curve radius. This may or may not be a problem. Fixing this may require a certain amount of tweaking.
- Movement in curves should slow train down, more so the tighter the radius but never abruptly. Calculate the inwards acceleration of each car and then factor this into the overall train speed, so that it slows down as more cars enter the curve.
- Designing the track. You’ll need some kind of visual editor, otherwise you’ll find yourself in a hell of a lot of pain laying down freeform tracks and trying to fit them together neatly. Unless you devise a simpler scheme or restrict yourself to certain radii and track lengths that fit well together.
![](../../../wikipedia/commons/thumb/b/b1/Off_the_Rails_(1)_jpg/220px-Off_the_Rails_(1).jpg)

[Derailment](https://en.wikipedia.org/wiki/Derailment): need it? If so, you should check curve radius against car length, or switching of a junction while a car/train is on it, and of course collisions with obstacles. You might decide to turn your train cars into actual physics objects while keeping each car’s momentum the moment the train derails. Not sure if that’ll look good but might be better looking than most other solutions.

This is just a small list of the issues. I guess I forgot some, and others I’m probably not even aware of yet. I find those issues interesting and challenging, but understandably they also explain why the tile-based train games are so much more popular, and the freeform track train games often leave a lot to be desired in terms of animation and realism.

#### Issues Solved in the Example Project

In the [rail car driving example project](https://github.com/LearnCocos2D/LearnCocos2D/tree/master/RailCarDrivingOnTrackTest) I attempted to solve a few of these issues, and I tried to prove that I’m on the right track (that pun was **not** intended) regarding the two-axle-per-car simulation.

For example, the conversion from linear speed to angular speed went well. Although I did expect the car to travel faster in curves the larger the radius, due to uniform circular movement, the car actually goes faster around tighter curves. Not sure where this is coming from.

I also wanted to see how much the axle distance deviates if I move both axles individually, instead of placing the rear axle a fixed distance away from the front axle. It turns out that in my case the deviation is at a maximum of 6 pixels, meaning the initial axle distance of 100 points shrinks to 94 pixels when the car enters a curve.

Placement and rotation of the chassis looks good. Although I cheated in the left curve. Since I’m not using a velocity vector for speed, I didn’t know which direction the car is going, so I cheated to force it to turn the way I intended in the left curve.

#### Further Research

About (Uniform) Circular Motion: [here](http://www.physicsclassroom.com/class/circles/u6l1a.cfm), [here](http://www.physicsclassroom.com/class/circles/u6l1e.cfm), [here](https://en.wikipedia.org/wiki/Circular_motion) and [here](http://publishing.cdlib.org/ucpressebooks/view?docId=ft4489n8zn;chunk.id=d0e2344;doc.view=print).

About simulating tracks or roads: [here](http://gamedev.stackexchange.com/questions/504/what-are-some-methods-to-represent-train-tracks), [here](http://theory.stanford.edu/~amitp/game-programming/road-applet/roads.html),

About movement on splines/bezier curves: [here](http://community.spinxengine.com/content/19-constant-speed-cubic-spline-interpolation.html)

Other example projects: OpenRailz ([demo video](https://www.dailymotion.com/video/xgl2kp_openrailz-tech-demo-3_videogames), [source code](http://ftp.heanet.ie/mirrors/sourceforge/a/project/ad/adh/OpenRailz/))

Any model railroad for inspiration. Like this amazing, impressive, jaw-dropping

[N scale replica of Stuttgart main station]. The image depicts only a portion of the entire layout. Built by one man in over 34 years (since 1978). If that isn’t inspiring, I don’t know what is.


You can easily spend 30+ minutes gazing at all the pictures … but do come back here!

#### Looking for more?

I’m afraid there’s not much in terms of actual tutorials on the subject or working projects. I’ve had a hard time even finding developer’s questions about the subject. If you come across any article on the subject worth mentioning, please don’t hesitate to post the link in the comments.

My understanding is that trains are a rather niche setting for a game, plus making a good one is rather hard to do. And then expectations from both developers and users are pretty high because everyone knows trains and model railroads, so how hard can it be to program them? I know, because I tried to tackle this a couple years ago and slammed right into all these unexpected and non-trivial issues. Frustration quickly settled in.

If you like where this demo project is going please tell me. Ever since [Railroad Tycoon](https://en.wikipedia.org/wiki/Railroad_Tycoon) I’m fascinated by train games, the challenges they pose and maybe making a good looking, as realistic as can be 2D top-down train simulation once and for all. Maybe it makes sense to turn this into a [Train-Making Game Starterkit](http://www.learn-cocos2d.com/store/line-drawing-game-starterkit/) perhaps?

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I love train games and would love to see more. As much as I like the idea of free form road & track layout, games like OpenTTD show that the constraint of a grid can lead to very interesting gameplay. I’m going to play Cities XL to see how well free form layout works.

[…] Sample project serving as the starting point for a Train Game with free-form tracks - LINK […]

[…] game will pick up the railroad game idea, combine it with the railtrack linedrawing demo (see above) I wrote several months ago, add physics […]

I’m glad you found my game Train Master enjoyable. However, the game is not tile based and actually does use the freeform technique with 2 axles and you will see the effect is more pronounced for the 2 carriage yellow train in the game. It was written in cocos 2d with the track plotted out using a custom created level editor with the actual path plotted out as an array of co-ordinates. The two hidden axle sprites for each train or carriage follow the plotted path at an equal speed and the train sprite is ‘bridged’ over the two.