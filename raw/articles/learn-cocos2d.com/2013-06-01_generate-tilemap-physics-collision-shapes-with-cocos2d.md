---
title: Generate Tilemap Physics Collision Shapes with Cocos2D
url: http://www.learn-cocos2d.com/2013/06/generate-tilemap-physics-collision-shapes-cocos2d/
author: George says
published: '2013-06-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

You have a tilemap and you want physics collisions on it? The solution seems obvious: create a rectangle shape for every blocking tile. ![Screen Shot 2013-05-31 at 00.59.01](../../../wordpress/wp-content/uploads/Screen-Shot-2013-05-31-at-00.59.01-300x259.png)


But ouch! This solution is not just hugely wasteful and unnecessarily slows down the physics collision code, it also introduces the well known problem of characters getting stuck even on flat surfaces.

This is in particular a problem for Box2D because its collision mechanic doesn’t work well with flat surfaces subdivided into smaller segments (rectangle shapes in this case).

A workable but still very awkward solution to work around this behavior is to create characters with [bevelled edges at the character shape’s bottom](http://www.cocos2d-iphone.org/forums/topic/box2d-issue-with-platformer-tiled-game/#post-352485) at the risk of bopping characters as they walk about the map.

### Lupines in the Moore Neighborhood

A good solution to generate physics collisions is to implement the [Moore Neighborhood algorithm](https://en.wikipedia.org/wiki/Moore_neighborhood) to generate chain shapes which are more suitable for tilemap collisions. The downside is that adding or removing individual blocking tiles at runtime requires updating the shapes - this is not implemented in this project.

Every flat surface, no matter how many tiles form the surface, will then consist of only one straight collision segment. Here’s a quick demo video of the project discussed in this post that shows the algorithm at work and the resulting “game”:


While researching the subject I found very little work done for cocos2d tilemaps. But I did find [this page from the stone ages of the Internet](http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html) which was instrumental in understanding the Moore Neighborhood algorithm, largely thanks to the animated GIFs.

The page also discusses the other contour tracing algorithms and examines their strengths and weaknesses. Without it, I would have probably spent a lot more time than 4 days on this problem, and as you can see at 5:00 in the video it’s still not quite perfect.

Tracing the contour tiles is one thing, but actually generating the line segments around the tiles correctly and properly closing them required an extra level of optimization I hadn’t initially anticipated.

### Generate Physics Collision Shapes from Contours

The most important method is how the chain shapes are created after the map’s contours have been scanned and segments created for each contour:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 |
-(void) createCollisionShapesFromContourMap { // static body that gets the chain shapes added to it b2BodyDef bodyDef; b2Body* contoursBody = world->CreateBody(&bodyDef); for (KTPointArray* segments in _contourMap.contourSegments) { NSUInteger vertexCount = 0; b2Vec2 vertices[8]; // Box2D allows for 8 vertices per shape for (NSUInteger i = 0; i < segments.count; i++) { CGPoint point = segments.points[i]; vertices[vertexCount] = b2Vec2(point.x / PTM_RATIO, point.y / PTM_RATIO); vertexCount++; if (vertexCount == 8) { b2ChainShape chainShape; chainShape.CreateChain(vertices, vertexCount); contoursBody->CreateFixture(&chainShape, 0); // last point becomes first point vertexCount = 1; vertices[0] = vertices[7]; } } // create the last chain shape if (vertexCount >= 2) { b2ChainShape chainShape; chainShape.CreateChain(vertices, vertexCount); contoursBody->CreateFixture(&chainShape, 0); } } } |


That code should be straightforward to adapt to Chipmunk, provided you know your way around Chipmunk. The contour tracing algorithm in KTContourMap is completely independent from Box2D, you’ll notice it doesn’t even have the .mm file extension.

There’s one assumption made by the KTContourMap, that is that the Tile with **GID 150 is considered blocking**.

You will need to change this for your own tilemap, and most likely adapt the code to allow the blocking test to check for multiple GIDs, or tiles with certain properties, or any other way you define blocking tiles in your tilemap. This is something I’ll improve before adding the contour mapping feature to [KoboldTouch](http://www.koboldtouch.com/). I’m also considering to make this a build step so that when I get to work on streaming tilemaps the physics collision shapes can also be streamed and don’t have to be recalculated at runtime.

### Deviating from the process

Since I’ve already spent double the time I allotted for this research, I will deviate a little from the usual tutorial style and just leave you with the video and project source code “as is”. This is actually the first time I missed my usual Thursday spot for iDevBlogADay articles, this one being 2 days late.

Feel free to ask questions in the comments or post modifications of the code - like every other code in [my github repository](https://github.com/LearnCocos2D/LearnCocos2D) this code is distributed under the MIT license.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi Steffen,

Firstly I would like to thank you for the immense contribution you have made to Cocos2d literacy. You’ve have the learning process a lot simpler for a good number of us.

Basically, I’ve been trying for the past few days to call a method when a particular CCAnimationFrame displays in a CCAnimation sequence. You might have seen my post on stackoverflow (http://stackoverflow.com/questions/17611628/calling-a-method-when-a-particular-ccanimationframe-is-displayed-using-ccanimati). I would really appreciate it if you could assist me in solving this issue, I’ve been at it for a while and I’m not making much headway. Thanks in advance.

Have you tried the notifications as suggested?

Otherwise you can always override the setDisplayFrame method and check which sprite frame was set, and if it matches the one that should send a message, send a message. 😉

Yes, I have tried the notifications but I was having issues with:

1. define my nsdictionary for accessing 3rd frame

2. linking the nsdictionary to the selector in addObserver

Basically I’ve not been able to get beyond the code I posted in the in the question.

I think overriding the setDisplayFrame method could be a simpler approach. How can I do this?

to be more specific how will I send the message?

I’ve not been able to make much progress. I’m still trying to get it solved.

Hi,

nice tutorial.. I’ve been wondering this too long, and now you have done this. And it looks good! But the only problem to me is that it’s written in Objective-C (somehow I understand it but there’s many things different compared to C++, and my mind just goes apepoop) could you somehow provide that chain shape generation and the contour tracing in C++? =) I would be very grateful for such thing.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Hi!

First of all, thanks for the explanation! I find it a bit difficult to understand, because you explain only in parts.

Just to make sure I got it correctly:

1. Use Moore to detect outer block of “block bunches”. Many of those outer blocks go to a segment. Many segemts go to the ContourMap

2. ->Loop through Segments in the ContourMap

3. —-> Loop through Blocks in those segments, get all vertices, bundle each 8 of them to a ChainShape, put many ChainShapes to a

4. Magic happens in Box2D as it “unclutters” (kind of) random polygons and creates a clean outer shape with as few vertices as possible?

Did I understood 4 right? Because I didn’t find a solution to obtain a polygon-shape out of the pox shape.

Best,

synth