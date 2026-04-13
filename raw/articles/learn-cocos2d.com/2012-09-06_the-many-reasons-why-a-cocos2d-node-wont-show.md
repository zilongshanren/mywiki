---
title: The Many Reasons Why A Cocos2D Node Won’t Show
url: http://www.learn-cocos2d.com/2012/09/reasons-node-show/
author: KleMiX says
published: '2012-09-06'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

As a cocos2d user you’ve probably encountered this before: you just added another sprite, a label, a particle effect or some other node to your scene - but it just won’t show up!

This article is an attempt at documenting the possible causes, providing steps you can take to verify and hopefully rectify the situation. You can use this as a checklist to provide help for this exact situation. Bookmark this page because you will have to use it eventually, I guarantee you.


### Debugging Tip

If you have a non-showing node that ought to be there, you can exclude a whole bunch of potential causes by adding that node directly to the scene object temporarily. Just make sure you position it somewhere on-screen.

If the node shows up now, you know that the cause must be due to one of its parent nodes and you can limit your search to those. If the node still doesn’t show up, it’s an issue with the node itself and you should look into the code you wrote to display it, including your custom draw methods and how you init the node and its resources.

### Node not added as child

The most obvious but also quite elusive reason is first: you simply forgot to call:

|
1 |
[xxx addChild:myNewNode]; |


It happens more often than you might think. It’s elusive because neither cocos2d nor Xcode will provide a warning in this case. It’s perfectly legal to create a node but not add it as child to some other node.

Another elusive aspect is that it may not be the node you’re missing. You may have actually added it as child, but you forgot to add its parent. For example if you were adding a new layer with a sprite in it, you may have added the sprite to the layer, but not the layer to the scene.

Much less common but still a possibility is adding the node as child and then removing it almost instantly. This may be a logic bug in your code.

![](../../assets/970075067dcae45f.jpg)


**Children: you must add them to a parent or they will not show up.**

### Node Z Order

One way to not show a node is to set its zOrder to a lower value than a much larger node in the foreground. Then the foreground node is drawn over the lower z order background nodes. Simple enough.

A bit more headscratching may be in order if you never changed the z order for your nodes in question, or any node for that matter. In this case cocos2d renders the nodes in the order they were added as child. That means the nodes added last will be drawn last, and over previously added nodes. So far so good. Now consider the case where you have several nodes that you remove and recreate during gameplay. Eventually you’ll run into a situation that’s merely based on timing when one node is added earlier than another, and the node added earlier simply won’t show. That’s because the node added later is drawing its content over the node, and that content may be quite large. In such cases you use fixed z values relative to other nodes of the same parent to avoid this kind of problem.

One thing to keep in mind is that the zOrder property is propagated from parent nodes to their children. For example if you have three nodes A, B and C with z values of A:5 / B:-1 / C:0 then all of node B’s child nodes and the child nodes of their nodes are drawn first. Next all of C’s child nodes are drawn before finally all child nodes of A are drawn. It doesn’t matter if all child nodes in A have a zOrder of -1000 whereas the child nodes of B have a zOrder of 500. The child nodes in A will appear to be in front of the child nodes in B at all times. Since this is also true for CCSpriteBatchNode, it’s one of the things to consider early in your code design so that you get your draw order "in order" so to speak.

### Node Vertex Z

I just described that cocos2d uses the node hierarchy for z ordering. Sometimes, as in the example described above, this may be too restrictive. You may want to use several CCSpriteBatchNode "layers" in your game and still be able to change the draw order of any sprite in any of the batch nodes freely. To achieve that, developers need to take the CCGLView’s depth buffering option (disabled by default). From then on you can use vertexZ to change the actual "depth" which OpenGL considers the node to be at. This works globally, so any node with a vertexZ of -100 will be drawn behind any other node anywhere in the hierarchy that uses a higher vertexZ value.

So far so good. All the precautions for regular z order apply. However, there’s one additional caveat: the regular z order now only has an effect if two nodes have the same parent and the same vertexZ. In that case the regular z order still comes into play, and if z order is also equal then only the order in which the nodes were added determines which node gets drawn first. The problem working with vertexZ is often simply that you now have to consider all vertexZ values globally, and regular z order has little to no influence. Yet if you’re not used to using vertexZ you may find yourself frantically modifying regular z values where instead you have a z ordering problem between two completely unrelated nodes in two unrelated branches of your node hierarchy. Think globally!

A precautionary side note: the iPhone 4GS and iPad 3 have changed internally in such a way that actual [z fighting](https://en.wikipedia.org/wiki/Z-fighting) can occur if two nodes use the same vertexZ and depth buffering is enabled. You may notice triangular overlap of two or more nodes, which may even flicker as the nodes move. Since this isn’t going to go away, enabling vertexZ basically means that you have to ensure that there will be no nodes in any screen using the same vertexZ value, or else z fighting with visual artifacts is likely to occur.

**Z / Draw Order: this is how it works!**

### Node position

Of course your node should have a position that keeps it visible on screen. So check that you’re actually using proper coordinates.

Some developers haven’t understood the points vs pixel coordinate system, so they may try to position nodes at Retina pixel positions, like 900×600. That puts the node off screen even on Retina devices because position is expressed in points, not pixels. And both Retina and Non-Retina devices have 480×320 points, respectively 1024×768 points on iPad.

This is especially important to consider if you’re working with an API that’s using pixels instead of points. For example cocos2d itself has some tilemap methods that return pixel coordinates instead of point coordinates. And then there’s OpenGL ES code which also expects you to use pixel coordinates instead of point coordinates.

Coordinate conversion issues can also occur if you’re using Box2D and incorrectly apply the PixelsToMeters ratio. One commonly made mistake is to try to accommodate Retina resolution in Box2D position transformations by applying the CC_CONTENT_SCALE_FACTOR() method, which is not necessary. Why? See above: you are working only with point coordinates, and Box2D itself is completely oblivious to the actual screen resolution anyway.

Actions can also be tricky since they’re time-based. Specify a very tiny duration and the effect can be instant. Thus the node using CCMoveBy might essentially "teleport" from A to B in an instant. And it may overshoot, especially badly written custom actions can be an issue but more common is simply running two or more CCMoveTo/By at the same time on the same node. Chaos ensues.

Finally, a node’s position is always relative to its parent position. If the parent (and their parents) are all CCNode, CCScene or CCLayer objects (and a few others) and all the parent positions are CGPointZero (0x0) then the position of your node is equal to an actual screen coordinate. In that case a position of 450×300 will place your node somewhere close to the upper right corner of the screen. But if any of the parent’s position is not CGPointZero, that parent node’s position will be added to your node’s position. So if the parent is at position 100×100 then your node will be offset by 450×300 and therefore positioned off screen at 550×400.

Now this gets more complicated if you consider that most nodes are not offset from the parent’s position, but from the parent’s lower left corner of the texture that it is displaying. This is an unfortunate (but intentional) design choice of cocos2d. If the parent is at position 200×200 and uses a texture for display (sprite, label and a few others) and the texture has the dimension 150×150, then the child nodes will be positioned at 125×125 (200×200 minus 150×150 divided by 2). This is assuming the default anchorPoint of 0.5×0.5 (hence the division by 2) has remained unchanged. This effect does not occur if the parent doesn’t use a texture for display (its contentSize property is all zero).

### Node anchorPoint

Related to position and rotation is the anchorPoint property. It’s default value is 0.5×0.5 for most nodes, which means whatever image the node is displaying will be centered on the node’s position. The anchorPoint is also the point where the node rotates around itself.

Because of this the anchorPoint is often and falsely regarded as one (easy) way to modify position or rotation behavior. I have heard of cases where developers simply did not understand that anchorPoint is a multiplier that is supposed to be in the range 0.0 to 1.0. So if you use awkwardly large values for anchorPoint, that will not only affect the position of the node but also all of its children, and could very well turn out to be problematic in the long term when it comes to positioning nodes. In a way, changing the anchorPoint too much causes a "desynch" between the node’s position and its visual representation (sprite, label, etc).

Another thing to consider is that modifying the anchorPoint also changes the center point of rotation. Instead of child nodes rotating around the center of their parent, they may actually rotate around a far-offset center point. That means even small changes in the parent’s rotation property could move the child nodes off screen.

![](../../../decopix/pix/yellowtest/790_anchorpoint/pict0006_5.jpg)


**AnchorPoint welcomes you - but only if you leave it as it is.**

### Parent rotation

As hinted above this one can be devious. Should your node intentionally be placed at an offset to its parent position, consider that the parent’s rotation property also affects your node’s position.

For example, let’s assume for simplicity that we have a parent which doesn’t use a texture and is positioned at 100×100. Your node’s position of 300×0 should then offset it to an absolute position of 400×0. But only if your parent’s rotation property is 0. Let’s further assume the parent’s rotation property is 90, 180 or 270 - that would also rotate your node around the parent’s position. Therefore, the resulting absolute positions for your node will be 100×500, -200×100 and 100x-200 respectively. All of these positions would render the node off screen.

As with any parent-inherited property such as position, the effect accumulates the greater the offset and the more parents with offset positions or rotations are involved.

### Node not animated

You may be expecting your node to move onto the screen. Or animate into view in any other way. But it doesn’t happen.

If it’s not one of the issues here, it may be as simple as forgetting to run the animation actions. Or running them more than once, that’s just as bad. Or interrupting them prematurely is also a possibility.

And if you manually animate your node, it may simply be a case of forgetting to schedule an update selector. Or inadvertently stopping it. For example by calling pauseSchedulerAndActions on the node.

### Node visible

Sounds obvious that the node’s visible property should be YES. But what might throw you off-guard is the fact that visible is a property which nodes inherit from its parents. So if any of the node’s parents has the visible property set to NO, the node will not be visible either.

The mean thing about this is that the child’s visible property will still read YES in the debugger, because the value is not propagated from the parent. The parent node simply stops calling the draw method of its children if its visible property is set to NO.

### Node opacity

The CCFadeOut action is quite commonly used. So it’s not surprising to think that your node’s opacity property may simply be 0 (or close to zero). This can happen if you have a logic bug.

Calling stopAllActions or stopActionByTag may be involved because you may have stopped the fade in/out animation at an unfortunate point in time.

### Node scale

The same could be said about CCScaleTo and related actions. If your node’s scale factor is very small (below 0.1 perhaps) the node might as well be invisible.

Again a logic bug like stopping actions at inappropriate times may be the cause. Or a user input issue, where you might allow the user to pinch and zoom but never check for the fact that the scale factor might become 0. Now if you continue to use the scale factor in related calculations as a multiplier, you may end up never being able to recover from a scale of zero. Multiply anything with zero and the result is zero.

### Node custom draw

A simple but easily overlooked fact when overriding a node’s draw method to perform custom (or debug) drawing is to forget to call the super implementation:

|
1 2 3 4 5 6 7 |
-(void) draw { // call super implementation to draw node (if desired) [super draw]; // custom draw code here } |

Calling the super implementation isn’t always necessary. For example a CCNode doesn’t draw anything anyway. In other cases you simply want the super class not to draw itself, because you’re drawing it your own way. But sometimes not calling super draw means you won’t see anything but your custom draw code, which may not be what you want.

### Node custom draw #2 (visit)

Another important thing to know is the order in which nodes are drawn. First, the node draws all children with a negative zOrder, then it draws itself followed by all children with a zOrder of 0 or higher. That means if you wanted to highlight the position of all the child nodes using OpenGL (with ccDrawCircle(..) for example) you can only do so in the draw method if the child nodes in question have a z order of -1 or less. Otherwise they would simply draw their images over the OpenGL stuff you’ve drawn.

To avoid this draw order problem, or other cumbersome workarounds like custom draw code for all child nodes, you should instead overwrite the visit method:

|
1 2 3 4 5 6 7 |
-(void) visit { // call super implementation to draw self and all children in order [super visit]; // custom draw code here draws over node and all of its children } |


Of course forgetting to call super visit will cause you to draw nothing but your custom draw code. But maybe that’s exactly what you want?

### Node blend func

A rare possibility for an invisible node is modifying the node’s blendFunc property in an unfortunate way. Some blend func combinations can lead to your node becoming invisible. Most will simply cause some form of distortion, like rectangular shapes, no alpha, black image content or background shining through at image outlines. The real biggy here is that both the texture format and CCGLView render format affect the results of the blendFunc. So what might work for one sprite or one app may not work with another sprite (or label) or another app with different CCGLView settings.

### Node init

Last but not least, since so many developers thoughtlessly subclass cocos2d node classes, they’re prone to eventually running into an issue I call "bad init". You can for example subclass CCSprite in such a way that you end up calling only super init, and therefore no texture is initialized. If it doesn’t crash outright, the sprite will simply not show up at all. If you do subclass any of the cocos2d node classes and it just won’t show up, check your init! Step through the initialization code, including the cocos2d code, and see if it takes a path it shouldn’t be. It’s all too easy to make cocos2d skip important code when subclassing instead of simply **using** the node classes.

### This Paragraph Intentionally Left Blank

If you know of any other reasons why a node might not show up on screen (or where you expect it), please leave me a comment. I’ll add it to the post.


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

If you override onEnter or onExit and forget to call [super onEnter/onExit] it will lead to not being visible and responsive.

Good catch! I had this in my mind when I wrote the bulletpoint list of things that could cause this. But I lost that trail of thought, I could only remember that there was something else I forgot. Now I know, thanks!

Amendment #1:

Node overrides onEnterIf you override either the onEnter (or onExit) method, you have to call the super implementation:

Failure to call the super implementation specifically in onEnter may lead to the node not being visible. The onEnter and onExit methods of CCNode change the node’s “running” state. The “running” flag affects how cocos2d works with the node internally. If a node is not “running” it may be unresponsive because all scheduled selectors will be paused (they won’t execute) and the “running” state may affect various node classes in different ways.

Most importantly if you don’t call the super implementation of onEnter or onExit, the node’s children won’t execute their onEnter and onExit methods either!

I have almost same kind of problem but in my case my iad Banner is now showing. I have checked eveything, it says banner is created and calls all the call back function but it does not show up on any cost.

In cocos2D 2.x you need to setup a shader program before your custom CCNode subclass is drawn. If you fail to do so, the node uses the currently used shader program which may give unexpected results (or the node is not drawn at all if no other shader program is used in your app).

In simple cases, select the shader program in your init method. Then, enable the shader program and update its uniforms etc. before drawing your node (see CCDrawNode.m, for example)

With regard to the “Node Vertex Z” section, I am running into a problem. To set things up, I have a map created with Tiled that has multiple layers. For all layers except for the top layer I added a cc_vertexz property with a value of -1000. For the top layer, lets just call it the “tree” layer, I have this same property set to “automatic”, and have also added the cc_alpha_func property with a value of .5. I then create a sprite for my hero, which is also animated and using textures that are not part of the tile map textures, and add it as a child of the map with the same zorder as the to the tree layer. This is all in accordance with the Cocos2d programers guid found here:

http://www.cocos2d-iphone.org/wiki/doku.php/prog_guide:tiled_maps

I then have a method that is scheduled to run to adjust the vertexz of this sprite based on its Y coordinate within the map. This all works great.

However, it falls apart when I then create some additional sprites as enemies and add them to the map in the same manner as the hero, and adjust their vertexz value based on their Y coordinate within that map as well. If my hero is “below” one of these enemy sprites, everything is fine as the enemy sprite passes behind the hero sprite. However, if my hero sprite is “above” one of these enemy sprites, there is a very strange effect where the background, which is one of the other tile map layers with a cc_vertexx property of -1000, comes through the transparent areas of the enemy sprites and appears ON TOP of the hero sprite.

From looking into things it appears to be a blending issue. But the solution that is suggested, which is to subclass the sprite or spritesheet classes and override the draw method is for COCOS2d 1.0 and not 2.0, which is what I am using. The overridden draw method would be as follows:

- (void) draw {

glEnable(GL_BLEND);

glBlendFunc( GL_GREATER, 0 );

[super draw];

glDisable(GL_BLEND);

}

It should be noted that the hero sprite is added to the map after the enemy sprites.

I apologize for the lengthly response. Is this even a proper solution, and if so what is the Cocos2d 2.0 equivalent? In addition, much of what I have described does not appear to be necessary based on how you have described it above.

I appreciate any assistance you can provide. Thank you!

Not sure if this is still valid code in GL ES 2.0. Definitely try changing the glBlendFunc 2nd parameter, try 0.5 and 1.0 or any values in between. There was a lengthy thread about this on the cocos2d-iphone forum, sounds like you found that but in case you didn’t it may be helpful: http://www.cocos2d-iphone.org/forums/topic/tmxtilemap-isometric-zorder-ad-hoc-sprite-issue/page/3/

One workaround was to add a layer underneath the tilemap, fully black, creating a black outline around the characters. That’s one solution if you can live with the cartoon-ish looks.

Many mistakes comes when you dont initialize your subclass with [class node] instead common [[class alloc] init]

If you edit the source code of cocos2D it can cause this problem as well. I do it sometimes to add functionallity