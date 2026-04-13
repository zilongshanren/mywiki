---
title: Table of Contents
url: http://www.learn-cocos2d.com/files/cocos2d-essential-reference-sample/Table_of_Contents/
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Entries followed by a dash and descriptive text are complete articles. Entries without descriptive text are planned and will be added at a later time or may be work in progress.

[Cocos2D Basics](http://192.168.0.1:8090/display/IDCAR/Cocos2D+Basics) — Articles explaining basic or fundamental Cocos2D concepts, possibilities and limitations.

[Cocos2D Coordinate System](http://192.168.0.1:8090/display/IDCAR/Cocos2D+Coordinate+System) — Explains what Coordinate System Cocos2D uses, and how it's different from UIKit's coordinate system.

[How Well Cocos2D Cooperates With UIKit](http://192.168.0.1:8090/display/IDCAR/How+Well+Cocos2D+Cooperates+With+UIKit) — Learn in how far you can mix Cocos2D with UIKit, how well it'll work or if at all, and what is required and how difficult it is.

[Technical Limitations](http://192.168.0.1:8090/display/IDCAR/Technical+Limitations) — This article contains fundamental limitations of Cocos2D that may not be immediately obvious. It's good to know about them.

[Node Classes](http://192.168.0.1:8090/display/IDCAR/Node+Classes) — Node classes can be displayed on screen (CCSprite, CCLabelTTF, CCParticleSystem, CCTMXTilemap and more) and non-visible nodes can be used to structure the hierarchical layout of a scene (CCNode, CCScene, CCLayer and others).

[Common Node Tasks](http://192.168.0.1:8090/display/IDCAR/Common+Node+Tasks) — The most common and essential operations performed on or with classes inheriting from CCNode.

[Adding, Querying and Removing Child Nodes](http://192.168.0.1:8090/display/IDCAR/Adding%2C+Querying+and+Removing+Child+Nodes) — To create the scene graph (hierarchy of nodes) you add nodes as children of other nodes. How to add, access and remove child nodes is explained here.

[Attaching Custom Data Objects](http://192.168.0.1:8090/display/IDCAR/Attaching+Custom+Data+Objects) — Each node can store custom data objects. You don't have to subclass a node class just to add a few properties. Instead, create a data object and assign it to the node.

[Converting Between Coordinate Spaces](http://192.168.0.1:8090/display/IDCAR/Converting+Between+Coordinate+Spaces) — From time to time you may find that you need to convert a screen coordinate (ie from a touch) to a node's local coordinate space. Or vice versa.

[Custom Drawing with OpenGL ES](http://192.168.0.1:8090/display/IDCAR/Custom+Drawing+with+OpenGL+ES) — How to plug in custom OpenGL ES rendering code to a node. And draw order considerations.

[How The Anchor Point Works And What To Use It For](http://192.168.0.1:8090/display/IDCAR/How+The+Anchor+Point+Works+And+What+To+Use+It+For) — The anchorPoint property is mysterious, often used incorrectly and has a major use most developers don't know about.

[Influencing the Draw Order](http://192.168.0.1:8090/display/IDCAR/Influencing+the+Draw+Order) — Cocos2D determines which node is drawn behind or in front of another node by their relative position in the scene graph (node hierarchy), their zOrder property and the order in which the nodes were added.

[Positioning and Moving Nodes](http://192.168.0.1:8090/display/IDCAR/Positioning+and+Moving+Nodes) — All about the position property, how position is affected by parent and other properties, and how to use it to move nodes.

[Reacting to Scene Graph Change Events](http://192.168.0.1:8090/display/IDCAR/Reacting+to+Scene+Graph+Change+Events) — Specific messages are sent to a node when a node is added or removed from the hierarchy, and when a scene transition begins and ends.

[Running, Querying and Stopping Actions](http://192.168.0.1:8090/display/IDCAR/Running%2C+Querying+and+Stopping+Actions) — How to run, access and stop actions on a node. Plus important considerations when working with actions.

[Scheduling Updates and Selectors](http://192.168.0.1:8090/display/IDCAR/Scheduling+Updates+and+Selectors) — At the heart of any game engine there must be a system that executes methods in regular intervals. That's where scheduling updates and selectors comes into play.

[Transferring a Node to Another Parent](http://192.168.0.1:8090/display/IDCAR/Transferring+a+Node+to+Another+Parent) — Sometimes you want to remove a node from its parent only to add it as child to another parent. This article describes the process.

[Composition Nodes](http://192.168.0.1:8090/display/IDCAR/Composition+Nodes) — Non-drawing nodes for organizing the scene graph and grouping other nodes.

[CCNode](http://192.168.0.1:8090/display/IDCAR/CCNode) — The CCNode class is the super class for all node classes. A CCNode defines common properties like position, rotation and common methods like boundingBox.

[CCScene](http://192.168.0.1:8090/display/IDCAR/CCScene) — The CCScene class is the root node for any scene. It behaves virtually identical to a CCNode but is required as the first (root) node in the node hierarchy.

[Color Nodes](http://192.168.0.1:8090/display/IDCAR/Color+Nodes) — Nodes that fill an area with a solid color or a color gradient: CCLayerColor, CCLayerGradient

[Label Nodes](http://192.168.0.1:8090/display/IDCAR/Label+Nodes) — Nodes that display text using a truetype or bitmap font: CCLabelTTF, CCLabelBMFont, CCLabelAtlas

[Texture Nodes](http://192.168.0.1:8090/display/IDCAR/Texture+Nodes) — Nodes which draw from a texture: CCSprite, CCRenderTexture, CCAtlasNode, CCProgressTimer, CCMotionStreak

[Particle Effect Nodes](http://192.168.0.1:8090/display/IDCAR/Particle+Effect+Nodes) — Nodes to display particle effects: CCParticleSystem, CCParticleSystemQuad, CCParticle[Example]

[Batch Draw Nodes](http://192.168.0.1:8090/display/IDCAR/Batch+Draw+Nodes) — Nodes which draw their children in a single (batched) draw call: CCSpriteBatchNode, CCParticleBatchNode

[Menu Nodes](http://192.168.0.1:8090/display/IDCAR/Menu+Nodes) — Nodes which display a simple horizontal or vertical menu: CCMenu, CCMenuItem, CCMenuItemLabel, CCMenuItemSprite, CCMenuItemToggle

[Tilemap Nodes](http://192.168.0.1:8090/display/IDCAR/Tilemap+Nodes) — Nodes which display a tilemap in the Tiled Map Editor TMX format: CCTMXTiledMap, CCTMXLayer

[Node Protocols](http://192.168.0.1:8090/display/IDCAR/Node+Protocols) — Objective-C protocols used by some nodes: CCBlendProtocol, CCLabelProtocol, CCRGBAProtocol, CCTextureProtocol, CCTransitionEaseScene

[Action Classes](http://192.168.0.1:8090/display/IDCAR/Action+Classes) — Actions perform (continuous) updates of a node's properties in order to animate the node over time, once only, repeating or as part of a sequence. Actions can also call blocks and selectors.

[Core Engine Classes](http://192.168.0.1:8090/display/IDCAR/Core+Engine+Classes) — At the core of cocos2d classes like CCDirector, CCScheduler, CCTouchDispatcher, CCActionManager and others control the flow of updates and event processing.

[Cache Classes](http://192.168.0.1:8090/display/IDCAR/Cache+Classes) — Cocos2D's cache classes keep resources like textures, sprite frames, animations and shaders in memory. The cache classes bypass loading of resources already in memory, thus speeding up access to the resource.

[Rendering Classes](http://192.168.0.1:8090/display/IDCAR/Rendering+Classes) — Rendering classes include the CCGLView, the CCGLProgram shaders, the ccDrawPrimitives functions and classes closely connected to OpenGL: CCCamera, CCGridBase, CCTexture2D and CCTextureAtlas to name a few.

[Utility Classes](http://192.168.0.1:8090/display/IDCAR/Utility+Classes) — Utility classes include CCFileUtils for accessing files, CCProfiler for profiling, CCArray as an alternative to NSMutableArray and CCTimer as an alternative to NSTimer. Macros are also described here.

[Best Practices](http://192.168.0.1:8090/display/IDCAR/Best+Practices) — This section includes best practices and tips for cocos2d-iphone development with Objective-C and Xcode that help you work more efficiently.

[ARC: By All Means Use It!](http://192.168.0.1:8090/pages/viewpage.action?pageId=1802537) — Really, not using ARC is bad for your mental health. Learn why.

[Strategies for Accessing Other Nodes](http://192.168.0.1:8090/display/IDCAR/Strategies+for+Accessing+Other+Nodes) — Many times over, you may wonder how to get access to a particular node that lives somewhere else in the node hierarchy. This article answer this question.

[Use Classes Instead of Structs](http://192.168.0.1:8090/display/IDCAR/Use+Classes+Instead+of+Structs) — If you're in the habit of writing C struct objects to store data, switch over to writing simple Objective-C class objects with either @public instance variables or actual properties. It's very little extra code, and a lot safer and more flexible. In addition access to public instance variables is just as fast as accessing struct fields. And C structs are not fully supported in ARC anyway.

[Troubleshooting](http://192.168.0.1:8090/display/IDCAR/Troubleshooting) — Common cocos2d, Objective-C and Xcode issues with their symptons, causes and remedies are explained here. If you get in trouble, this is the place to check!

[The Many Reasons Why A Node Won't Show](http://192.168.0.1:8090/display/IDCAR/The+Many+Reasons+Why+A+Node+Won%27t+Show) — This article is an attempt at documenting the possible causes of a node not being visible on screen. You'll learn steps you can take to verify and hopefully rectify the situation. You can use this as a checklist for situations where a node isn't visible or where it should be.