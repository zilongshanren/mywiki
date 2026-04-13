---
title: Influencing the Draw Order
url: http://www.learn-cocos2d.com/files/cocos2d-essential-reference-sample/Influencing_the_Draw_Order/
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

```
[self addChild:labelA];
[self addChild:labelB];
[self addChild:labelC];
[self addChild:labelD];
[self addChild:labelE];
```


Cocos2D determines which node is drawn behind or in front of another node by their relative position in the scene graph (node hierarchy), their zOrder property and the order in which the nodes were added.

The simplest case is when you have a parent node to which you add several child nodes.

Let's assume these nodes are labels and the first label displays the letter A, the next displays B and so on. We name the variables referencing each label labelA, labelB and so forth. They all use the same position and same other properties. Most notably they all have the same zOrder property because we leave it at the default value of 0. Then the labels are added as children in ascending order, like so:

```
[self addChild:labelA];
[self addChild:labelB];
[self addChild:labelC];
[self addChild:labelD];
[self addChild:labelE];
```


Which one will be the topmost label? You may have guessed it: it's label E. Label E is added last, and therefore drawn last. Label A is drawn first.

You have two options to change the draw order: change the order in which the labels are added, or change their zOrder property. When adding child nodes it is convenient to use the z parameter of the addChild method, like so:

```
[self addChild:labelA z:3];
[self addChild:labelB z:-4];
[self addChild:labelC z:7];
[self addChild:labelD z:-14];
[self addChild:labelE];
```


What's the draw order now? The answer is:

labelD (zOrder = -14)

labelB (zOrder = -4)

labelE (zOrder = 0)

labelA (zOrder = 3)

labelC (zOrder = 7)

Label C is drawn last and is now the topmost label. As you can see, cocos2d draws nodes in ascending order, starting with the child node with the lowest zOrder property. The node with the highest zOrder property is drawn last. If two or more nodes have the same zOrder value, then the order in which they were added as child nodes comes into play again.

The zOrder property is a 32-Bit integer value. There is no limitation besides the integer value range from -2,147,483,648 to 2,147,483,637 that would limit the usable range of zOrder values. Well, readability and sanity perhaps.

A bit of caution: every time you change a node's zOrder property the children array of the node's parent is scheduled to be reordered before they are drawn. This is done with an [insertion sort algorithm](https://en.wikipedia.org/wiki/Insertion_sort). It is reasonably fast if the number of objects is small. Which should be the case in most instances, there will (ideally) be no more than a few dozen child nodes in any one parent node. However if you plan on having all your game nodes in the same parent, this can become a problem if you frequently (ie every frame) change at least one child node's zOrder property. You might want to read the [best and worst case scenario](https://en.wikipedia.org/wiki/Insertion_sort#Best.2C_worst.2C_and_average_cases) situations for insertion sort.

The insertion sort algorithm is fast if the array is already sorted. It is also fast in any case if there's only a small number of items, around 10. With increasing number of items, and increasing disorder of the zOrder values the algorithm takes longer to complete. If that may be the case for the game you're planning, you should consider testing this scenario against enabling depth buffering and using the vertexZ property to directly influence the OpenGL draw order (see further down).

![images_s/en_GB/3296/1/_/images/icons/emoticons/warning.png](../../../files/cocos2d-essential-reference-sample/images_s/en_GB/3296/1/_/images/icons/emoticons/warning.png)


We have yet to consider the child node's parent in this example. What if the parent node is a sprite, how does that affect the draw order?

Cocos2D first renders all child nodes with a negative zOrder value. Then it renders the parent node and then goes on to render the child nodes with a zero or higher zOrder property. In general terms this is what happens every frame:

draw child nodes with zOrder < 0

draw parent node

draw child nodes with zOrder >= 0

Going back to the above example, this is where the parent sprite will be sorted in the draw order list:

labelD (zOrder = -14)

labelB (zOrder = -4)

**parent sprite**

labelE (zOrder = 0)

labelA (zOrder = 3)

labelC (zOrder = 7)

Now you might think that you could change the zOrder of the parent to 10 in order to draw it in front of label C. Nope, it doesn't work this way.

The draw order of children is always relative to their parent. Meaning child nodes with positive zOrder will always be drawn on top of the parent, no matter what the parent's zOrder value is. Because the zOrder of the parent only affects the draw order of nodes in the same level as the parent.

To extend on the above you have to consider that every parent may have a parent of its own, and every child node may have additional child nodes. This is the node hierarchy. Cocos2D traverses that hierarchy and at each level of the hierarchy it renders the children and grandchildren based on their zOrder values. It's time for an illustration and a little brain flexing. Can you determine the correct draw order from sprite A through T?

![images_download/attachments/1802380/zorder.png](../../../files/cocos2d-essential-reference-sample/images_download/attachments/1802380/zorder.png)


Let's walk through it. The scene node doesn't matter since it doesn't draw anything - unless you add custom drawing (see [Custom Drawing with OpenGL ES](http://192.168.0.1:8090/display/IDCAR/Custom+Drawing+with+OpenGL+ES)) at which point it would be drawn after sprite A and before sprite B. But leaving that out for a second, here's a rundown of what happens:

sprite A has children with negative zOrder values

cocos2d checks sprite A child nodes

sprite D has lowest zOrder, and no children: draw sprite D

next is Sprite E, it has children but they all have zOrder >= 0: draws sprite E

cocos2d then draws sprite E's child nodes: draw sprite L and then sprite M

cocos2d checks sprite F, it has children but they're all zOrder >= 0: draw sprite F

check sprite N, it has children with negative zOrder: draw P, Q, R in the order they were added

draws sprite N

draws sprite O

...

Can you figure out the rest? Don't get mislead by the vertical order of the nodes in the image.

Here's the solution: D, E, L, M, F, P, Q, R, N, O, G, CCScene, B, H, I, J, S, T, C, K

The sprite C branch deserves an extra explanation. The order is J, S, T, C, K which stems from the fact that cocos2d first visits the negative zOrder children of sprite C. In sprite C it then finds no negative zOrder children and renders sprite J, but then it renders J's positive zOrder children S and T. Then it has finished traversing the JST branch and recurses back to sprite C where it determines there are no more negative zOrder children in C, so it draws sprite C. It then moves on to the positive zOrder children and draws sprite K last.

![images_s/en_GB/3296/1/_/images/icons/emoticons/lightbulb_on.png](../../assets/4c1e0ec152eeb085.png)

**draw order of nodes at the same level and relative to their parent**. But you can not use the zOrder property to change the draw order of nodes which have different parents, ie nodes that live in different parts of the node hierarchy. For example sprite N and O are drawn in front of sprite L and M even though they have a lower zOrder. Sprites N and O are of course children of a parent with a higher zOrder (-5) than the parent E (-10) of which sprite L and M are children of.

Now while this zOrder and order of adding children business is pretty convenient and relatively straightforward once you start using it, there are cases where greater flexibility is important. In particular in games where you need to change the zOrder of nodes every frame. Usually these are [games with an isometric perspective](https://www.google.com/search?num=10&hl=en&site=imghp&tbm=isch&q=isometric+game), where nodes with greater y coordinate are supposed to be drawn behind the nodes with a lower y coordinate.

Enter vertexZ and depth buffering. With depth buffering enabled, you can use the vertexZ property of a node to change it's OpenGL depth value. This vertexZ value allows you to change the draw order of nodes across the board, so a node with vertexZ of 10 will be drawn in front of all nodes with a vertexZ of 9 or lower - regardless of where these nodes are in the hierarchy.

Once you set the vertexZ property of a node to anything else but 0 then only the vertexZ value determines the draw order of that node. You can however still rely on zOrder for nodes whose vertexZ is 0.

The range of vertexZ values is limited, and also depends on the device and/or device resolution and the vertexZ values of parent nodes. You may be looking at a possible value range of roughly around -1,000 to +500 in general. If the vertexZ is too high or too low for the current device, the node will not be visible.

You need to be careful not to set the vertexZ of two or more nodes to the same value, otherwise [z fighting](https://en.wikipedia.org/wiki/Z-fighting) may occur on iPhone 4S, iPad 3 or newer devices if these nodes overlap.

Enabling depth buffering incurs a slight performance penalty and uses more memory. A 24-Bit z buffer on a 960x640 pixels Retina device consumes about 1.8 MB and a 24-Bit z buffer on a 2048x1536 Retina iPad consumes 9 MB.

You can not change projection from the default 2D (orthogonal) projection to 3D projection. You would normally have to enable 3D projection to use 3D rendering and in particular any CCGrid3DAction effects like page turn, twirl, wave or liquid.

You may encounter transparency issues. This occurs for example when you have a node A that would normally be drawn over node B according to the zOrder property and the node hierarchy. But node A's vertexZ property is lower than that of node B and is therefore drawn behind node B by OpenGL. In that case transparent areas of node B will be fully opaque, because cocos2d rendering is optimized on the assumption that node A will be drawn on top of node B (ie cocos2d assumes vertexZ to be 0 for all nodes). To fix this you would have to modify cocos2d's built-in shaders to enable alpha testing.

Using vertexZ is the only way to change the draw order of sprites using different batch nodes. For graphics intensive games with multiple texture atlases per game scene, using vertexZ may be a good way to influence the draw order without having to compromising on the composition of your texture atlases.

Using vertexZ also causes no reordering of children. This is ideal for games which need to frequently change or update the draw order of many nodes and is expected to be faster than frequently changing zOrder.

To use vertexZ you must first enable depth buffering in CCGLView. To do this open AppDelegate.m and find where the CCGLView is initialized. Kobold2D users should make that change in the config.lua file instead.

```
CCGLView *glView = [CCGLView viewWithFrame:[window_ bounds]
pixelFormat:kEAGLColorFormatRGB565
depthFormat:GL_DEPTH_COMPONENT24_OES
preserveBackbuffer:NO
sharegroup:nil
multiSampling:NO
numberOfSamples:0];
```


Change the `depthFormat` parameter from 0 to `GL_DEPTH_COMPONENT24_OES` to enable the 24-Bit z buffer. ![images_s/en_GB/3296/1/_/images/icons/emoticons/information.png](../../../files/cocos2d-essential-reference-sample/images_s/en_GB/3296/1/_/images/icons/emoticons/information.png)

`GL_DEPTH_COMPONENT16_OES` constant for 16-Bit z buffers is no longer available in OpenGL ES 2.0.

Now you can start changing the vertexZ property of your nodes and observe the effect:

```
labelA.vertexZ = -10;
labelB.vertexZ = 40;
labelC.vertexZ = 0;
labelD.vertexZ = -1;
labelE.vertexZ = -50;
```