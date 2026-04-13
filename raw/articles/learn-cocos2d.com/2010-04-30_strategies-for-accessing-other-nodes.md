---
title: Strategies for Accessing Other Nodes
url: http://www.learn-cocos2d.com/files/cocos2d-essential-reference-sample/Strategies_for_Accessing_Other_Nodes/
published: '2010-04-30'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`CCScene* runningScene = [CCDirector sharedDirector].runningScene;`


Many times over, you may wonder how to get access to a particular node that lives somewhere else in the node hierarchy. This article answer this question.

|
|
|
|
|

You can access the running scene via CCDirector like so:

`CCScene* runningScene = [CCDirector sharedDirector].runningScene;`


Now if you need to access your specific subclass of CCScene, you'll have to cast it. Since this poses the risk that the runningScene may not actually be a subclass of MyScene, you should verify that:

```
CCScene* runningScene = [CCDirector sharedDirector].runningScene;
if ([runningScene isKindOfClass:[MyScene class]])
{
MyScene* myScene = (MyScene*)runningScene;
// use myScene here
}
else
{
// error handling here, or ignore
}
```


If you execute CCDirector's replaceScene, pushScene or popScene methods, the runningScene property will point to the new scene. Any code that accesses the runningScene from this point forward may not receive the scene object you might expect. Therefore the isKindOfClass check in the above code sample.

|
|
|
|
|

To gain access to nodes which you know have the same parent, you can do so by sending getChildByTag to the parent:

`CCNode* otherNode = [self.parent getChildByTag:123];`


Of course you need to properly tag the nodes first, and you may have to cast the returned node.

The alternative would be to subclass the parent node's class if not done already, and give the parent class properties with which you can access the commonly used child nodes.

```
@interface MyParent : CCNode
@property (assign) CCSprite* childSprite;
@property (assign) CCLabelBMFont* childLabel;
@end
@implementation MyParent
@synthesize childSprite, childLabel;
@end
```


You need to assign childSprite and childLabel once when you initialize respectively add them as child nodes. Then the child nodes can access each other with a little casting:

```
// in the child sprite class:
MyParent* myParent = (MyParent*)self.parent;
CCLabelBMFont* childLabel = myParent.childLabel;
```


A common issue is caused by a sibling like childSprite receiving a strong (retaining) reference to another sibling like childLabel, and vice versa. This can easily lead to a [retain cycle](http://www.mikeash.com/pyblog/friday-qa-2010-04-30-dealing-with-retain-cycles.html) if you're not careful, even under ARC!

It is always better to relay access to sibling and their child nodes to the parent node. The parent node can safely retain references to a child or grandchild node. All other strong references (child retains parent or grandparent, child retains sibling or sibling's child) are prone to causing a retain cycle.

|
|
|
|
|

Now wait a minute … couldn't you access the scene simply by using self.parent with the appropriate number of parents?

Yes, indeed you could:

```
// Hi Grand-grand-grand-grandparent!
MyScene* myScene = (MyScene*)self.parent.parent.parent.parent.parent;
```


The above code is not bad practice. It is **terrible practice!**

This code breaks as soon as you add or remove a node from the hierarchy, or move the node executing the above code to some other place in the node hierarchy. Anything that changes the number of parent calls necessary to reach the scene, or whatever parent node you want to get, is going to break the above code. At best, the returned reference is nil and nothing happens. At worst it's a totally different object and that will crash with either "does not respond to selector" or EXC_BAD_ACCESS.

Not only that, there can be subtle, hard to debug issues introduced as well. For example if you were to change a common property of the parent, such as position and scale, you may only notice on screen that there's something wrong with the position or scale of some nodes. Or possibly all nodes if suddenly you position or scale the entire layer or scene. These issues are not obviously attributed to the use of the multiple-parent-accessor style. It's side effects like these that will drive you crazy.

Finally, it's a total slap in the face for code reuse and maintenance. You can't use the node using the above code anywhere else unless the fifth parent is the parent it needs for whatever reason. And you're also going to hesitate making beneficial or necessary changes to your node hierarchy, because it'll break your code.

There is an acceptable use for self.parent.parent, and that is when you want to bypass a sprite-batched sprite's or particle-batched particle's parent node:

```
// ok if parent is CCSpriteBatchNode or CCParticleBatchNode
MyParent* myParent = (MyParent*)self.parent.parent;
```


It is acceptable because the relationship of the sprite/particle and batch node is hardly going to change.

Similarly, you may find multi-parent-accessor style convenient in very self contained nodes. But frankly one has to wonder how one got there with this multi-parent-accessor style? Maybe that node is so self-contained mainly because it was locked into this specific node hierarchy setup by using the multi-parent-accessor style. In any case, such self-contained nodes usually grow over time, they evolve and change. So even in that case it seems counterproductive to use the multi-parent-accessor style because it prevents them from changing and evolving.

|
|
|
|
|

Now comes the difficult question. If you shouldn't just make any node a temporary singleton, and multi-parent-accessor style is bad news, how could unrelated node A with 3 parents gain access to unrelated node B with 5 parents - without any of them knowing where they are?

Here's some questions for you if you run into this situation:

Why does node A need a reference to node B (or vice versa)?

Can the access be relayed / routed through other (controlling) nodes?

If they require direct access to each other, how come they're in so very different branches of the node hierarchy?

Do they each store data that maybe should be global in the scene or a singleton for game data?

Setting any lingering design issues aside - (this is your homework assignment and yes, there **will** be a test on monday!) - the most common misconception is that you need **direct** access to the other node.

Assume the case where you have a player node that lives in a gameplay layer, and a score label that lives in the UI layer. Now the player kills a bad guy and that gives him score. We register the kill in the player node, so how do we inform the score label?

The most obvious solution seems to be that the player needs a reference to the score label. But that creates a strong dependency to the score label, and how that score is displayed (or if at all). Now depending on how rigorous you want to model your "dependency borders", you could route the score update from the player via the gameplay layer to the scene which then informs the UI layer which in turn notifies the score label. That is the ultra-rigid variant of separating different code modules from one another. If you had to separate the ties between gameplay layer and UI layer, you'd only have to modify the scene's routing methods in order to cut out and ignore the messages going to either the UI layer or the gameplay layer. This makes your node hierarchy flexible, but it can also be tedious and in rare cases costly.

A more reasonable approach seems to be to allow the player direct access to the UI layer via a shared instance of the UI layer. The UI layer then informs the score label. So how is that better than accessing the score label itself?

First, it's more reasonable because you probably will always have the UI layer where the player lives. So it's reasonably safe to assume that it'll exist, and safe to require it. Not so much for the score label though. The score label might be changed from a numeric label to a score bar or something else entirely. Furthermore, wouldn't it be cool if there would be an animation playing where the score appears over the player's or enemy's head and floats towards the score label? In addition to updating the score label (or bar), the UI layer could also kick off such an extra animation. The player doesn't know about this. In fact, he doesn't need to. All he knows and should know is that he scored. Whether it was big time or not, that's up to the UI layer.

It is this: in a branching, tree-like system of objects such as the Cocos2D node hierarchy, there's really no way around performing some message routing.

In general there are two strategies:

event-driven (messaging)

polling (frequent updates)

For example, in a multiplayer game the UI layer could be informed about every player joining or leaving (messaging). It could then store a reference to each player while the player remains active. In order to update the player's status (hitpoints, mana, etc) it could periodically check the player's properties related to hitpoints and mana (polling).

The alternative is for the UI layer to rely solely on messaging. So besides being informed when players join and leave, the UI layer would also receive messages passing in a specific player, and the type of change that occured. Or simply a general request to update all player UI values if there aren't that many.

Polling is really only preferable in two instances:

very frequent changes are the norm and expected (ie several times per second)

the observed object does not send the required messages (and the object can not be changed to do so)

The latter is mainly to pull out data from objects which were never designed to inform other about certain changes. Since you're writing most of the classes yourself and can change the sending node, the only real question is whether the properties you're interested in polling are expected to change frequently or not. Frequently as in probably every couple frames. In that case polling may be suitable. In all other cases event-driven is the way to go. And that means sending a message to another node whenever a change occurs. Messaging also has the added benefit that the target won't hold a strong reference to the sending node, therefore eliminating potential retain cycle issues.

There are generally two ways of informing another node that a change occured:

send (and route) message to node

send a NSNotification

|
|
|
|
|

For number one, there's a difficult truth to accept: in hierarchical systems with many branches, direct access between individual nodes is often not possible, and where it may be possible it is not advisable. Hence the general recommendation to refactor your scene or the scene's first-level child nodes (often layers and nodes) to be message relaying controllers.

For example if your scene contains the gameplay and UI layers, you'll want the scene to give access to the gameplay and UI layer via properties:

```
GamePlayLayer* gameLayer = [GameScene sharedGameScene].gamePlayLayer;
UILayer* uiLayer = [GameScene sharedGameScene].uiLayer;
```


Now that you have access to individual layers, the player node for example could then send the score update message to the UI layer:

```
-(void) killedEnemy:(Enemy*)enemy
{
UILayer* uiLayer = [GameScene sharedGameScene].uiLayer;
[uiLayer updateScore:enemy.scoreWhenKilled
atPosition:enemy.position
painful:(self.currentWeapon == kWeaponMegaBlaster)];
}
```


The UI layer is fed with just the information it needs. Notice that although we could send both the player and enemy nodes to the UI layer, it doesn't really need to know about these objects. In fact the less the UI layer knows about game objects, the better. The UI layer can then do its job, which is not only updating the score label but possibly also playing audio and particle effects:

```
-(void) updateScore:(int)score atPosition:(CGPoint)killPos painful:(BOOL)painful
{
[self.scoreLabel updateScore:score];
if (painful)
{
[self createBloodAndGoreEffectAtPosition:killPos];
[self playPositionalAudio:@"Wuaaarghsplash.caf" atPosition:killPos];
}
}
// for conveniently updating the score and nothing else
-(void) updateScore:(int)score
{
[self updateScore:score atPosition:CGPointZero painful:NO];
}
```


Everything that should happen on the UI side, like playing audio, particle effects and updating the HUD, is now handled on the UI side. Furthermore, no dependencies are introduced by unnecessarily passing in the player or enemy nodes, or passing in the weapon types. Finally, for the common case where only the score needs to be updated (ie item pickup etc) a convenience method allows to skip the two extra parameters that are only intended for kill scores.

|
|
|
|
|

Notifications are useful when the sender doesn't know anything about the receiver. Not even whether the sent message will be received at all, or by whom. Generally NSNotification are only used when the sender has no way of easily informing the receiver(s) via regular Objective-C messaging. You can learn more about notifications in Apple's [Notification Programming Topics guide](https://developer.apple.com/library/ios/#documentation/Cocoa/Conceptual/Notifications/Articles/Registering.html#//apple_ref/doc/uid/20000723-CEGCCFID).

Sender and receiver only have to agree on a common notification name, and perhaps named parameters to pass along. The latter is particularly disadvantageous for fast paced games, since you have to create a temporary NSDictionary and populate it with the data every time you send a notification with additional parameters. That's an overhead you should try to avoid in notifications that are sent every frame or hundreds of times per second. I'll leave this out of this discussion, there are examples in Apple's notification guide.

The receiver needs to register and unregister itself at the appropriate time to receive a specific notification via the NSNotificationCenter:

```
-(void) onEnter
{
[super onEnter];
// register for player died notification
NSNotificationCenter* notifyCenter = [NSNotificationCenter defaultCenter];
[notifyCenter addObserver:self
selector:@selector(playerDied:)
name:kPlayerDiedNotification
object:nil]; // nil means that notification could be sent from any object
}
-(void) cleanup
{
[super cleanup];
// deregister as observer
[[NSNotificationCenter defaultCenter] removeObserver:self];
}
```


In cases where you want to receive the message only when it is sent from a specific object, you'd have to pass the object in as the last parameter. Otherwise leave it nil to receive notifications with this name from all objects.

The kPlayerDiedNotification is just an NSString. The notification names should be defined in a global header file, and the notification string can be anything, as long as the string is unique:

`static NSString* kPlayerDiedNotification = @"player died";`


Defining the notification strings globally instead of writing the strings inline with the message parameters is good practice. This prevents any potential typo that could lead to difficult-to-debug issues like not sending or receiving (some) notifications.

To send a message you would use the postNotificationName method and optionally pass in an object that the receiver might need:

```
NSNotificationCenter* notifyCenter = [NSNotificationCenter defaultCenter];
[notifyCenter postNotificationName:kPlayerDiedNotification
object:self];
```


The receiver then has to implement the selector with a specific signature: it returns void and receives an NSNotification* object:

```
-(void) playerDied:(NSNotification*)notification
{
CCLOG(@"player died: %@ - received object: %@ - user info: %@",
notification, notification.object, notification.userInfo);
}
```


The received NSNotification gives you access to the passed in object, and the userInfo NSDictionary should you choose to use it.