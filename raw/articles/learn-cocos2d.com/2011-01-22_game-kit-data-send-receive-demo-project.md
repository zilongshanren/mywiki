---
title: Game Kit Data Send/Receive Demo Project
url: http://www.learn-cocos2d.com/2011/01/game-kit-data-sendreceive-demo-project/
author: The Ultimate Cocos; Learn; Master Cocos
published: '2011-01-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

An ongoing [discussion about how to correctly send/receive data with Game Kit](http://cocos2d-central.com/topic/115-gamekithelper-sending-and-receiving-data) on Cocos2D Central prompted me to write a demo project to complement the Learn Cocos2D book’s Game Center chapter. The [resulting working code is in this post](http://cocos2d-central.com/topic/115-gamekithelper-sending-and-receiving-data/page__view__findpost__p__588), and also reprinted below.

The Game Kit Data Send/Receive Demo Project ([download here](http://cocos2d-central.com/files/file/7-game-kit-data-sendreceive-demo-project/)) is based on the Learn Cocos2D book code made for the Game Center Chapter. It’s called Tilemap16 just to stay in line with the naming scheme.

You control the little Ninja as usual, but this time anytime you move it, it will also move on all other connected devices because the tile coordinate is sent via Game Kit to all connected players but only when it actually changes. The demo even allows you to move the Ninja on any device, and all others will follow, so it truly works in every direction. In addition, a score variable (int) is transmitted every frame just to show how to send different types of data at different times.

I wish I could have made a movie to show how cool this is but alas, my iPod was busy running the demo, so all I can show as proof is my iPod and iPad running the game with both Ninjas at the same position (mushy image made with my already-ancient iPhone 3G under perfect programming but terrible lighting conditions):

![tilemap-network](../../../wordpress/wp-content/uploads/tilemap-network-300x225.jpg)


### Source Code Example

In summary this is the code that’s used to send/receive data with the help of the GameKitHelper class I wrote for the book (also included in the download and free to use for anyone and any purpose):

[cc lang=”ObjC”]// add this to the header

typedef enum

{

kPacketTypePoint,

} EPacketTypes;

typedef struct

{

EPacketTypes type;

} SPacketInfo;

typedef struct

{

EPacketTypes type;

CGPoint point;

} SPointPacket;

[/cc]

Sending a packet:

[cc lang=”ObjC”]

-(BOOL)ccTouchBegan:(UITouch *)touch withEvent:(UIEvent *)event

{

CGPoint location = [touch locationInView: [touch view]];

SPointPacket packet;

packet.type = kPacketTypePoint;

packet.point = location;

gkHelper = [GameKitHelper sharedGameKitHelper];

[gkHelper sendDataToAllPlayers:&packet length:sizeof(packet)];

}

[/cc]

Receiving the packet:

[cc lang=”ObjC”]

-(void) onReceivedData:(NSData*)data fromPlayer:(NSString*)playerID

{

// first, assume it’s the general SPacketInfo, that way we can access type

SPacketInfo* packet = (SPacketInfo*)[data bytes];

switch (packet->type)

{

case kPacketTypePoint:

{

SPointPacket* pointPacket = (SPointPacket*)packet;

CCLOG(@”received point: %.1f, %.1f”, pointPacket->point.x, pointPacket->point.y);

break;

}

default:

CCLOG(@”received unknown packet type %i”, packet->type);

break;

}

}

[/cc]

### Requirements & Setup

You need:

- 2 devices which are Game Center capable, eg they must have the Game Center App installed. If it isn’t, that device is not ready for Game Center. 1st & 2nd Generation devices up to iPhone 3G do not support Game Center. In addition Simulator will not work due to Matchmaking/Invites not being supported on the Simulator.

- 2 Game Center accounts (you can create dummy accounts via the Game Center App)

What you have to do:

- Create a new App on iTunes Connect, enable Game Center for that App, and replace the Bundle ID of your App with the one in the project’s info.plist. Please refer to the [Game Center section in the iTunes Connect documentation](http://www.learn-cocos2d.com/docs/iTunesConnect_DeveloperGuide.pdf).

- Make sure Push Notifications are enabled on all devices via Settings App.

- Run the Game Center App on both devices, login and make sure each device is logged in with a unique account. Then invite the other device’s account as friend and accept the friend request, this makes it easier to join each other’s matches.

- Build the Tilemap16 App and deploy it to both devices. Whenever you make a change to the code, you must deploy the App to both devices again, to make sure they run the same code.

- Run the App on one device, wait for the matchmaking screen to appear. Invite your other device’s friend account to join the match.

- Wait on the other device for the match invite to pop up. Tap Accept. The Tilemap16 game will launch.

- Tap **Play Now** on the first device once the other player has successfully connected and is ready.

- Move the Ninja on either device and watch it move on the other.

Enjoy!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] This post was mentioned on Twitter by sergimtz.losa, Steffen Itterheim. Steffen Itterheim said: New #Cocos2D #iDevBlogADayWL post: Game Kit Data Send/Receive Demo Project - http://tinyurl.com/4u9ezlg […]

[…] Gems: GameKitHelper, ClippingNode, Multiple Update Selectors, FrameOrFile, […]

Great helper!

Thanks a lot for taking the time and effort of putting this together.

Jnani

Sometimes the game “Finds a Player” instantly, other times nothing happens at all. Any idea what the issue may be?

[…] something has something everything to do with multiplayer game programming. I think synchronizing the game state across multiple devices should be as simple as saying: […]

Hi Steffen,

I’ve used GameKitHelper in the past for simple stuff and it’s great. I’m now using it in a somewhat more complicated app and have noticed that whilst it does most things for us, it doesn’t detect if the device has multi-player games restricted. This then allows an invitation view controller to display without cocos2d being paused (this is with cocos2d v2.0) which causes an assertion. I’ve added a workaround to the initialisation that tries to set up an invalid match (1 player) which, if multi-player is disabled, gets an gk error 10. I’d like a better way but I couldn’t find an API call to ask the device the state of that setting.

Thanks again for all the goodies you’ve put together.

Hmmm the Game Kit Programming Guide also makes no mention of this “multiplayer games off” setting. There is an “underage” property in the GKLocalPlayer class but it doesn’t say if this is set if multiplayer games are turned off. It might be worth checking if this is actually the case or if the underage setting is derived from the GK account and not related to multiplayer games being turned off.

Agreed. I couldn’t find any reference to the setting in the documentation. I’ve hunted around with no luck. Good thought on the underage setting; I’ll test that, but I’m not confident. My mechanism that attempts to create an invalid match works, but I’m concerned that it relies on a possible side effect and if Apple change the error response my app won’t function as intended.

It might be worth my posting a query off to Apple.

Hi Steffen,

My project has progressed a fair way since my last comment. It’s all working fairly well though I’m finding the whole matchmaking process to be flaky and unreliable. I’m probably going to abandon it in favour of my own interface to the GKSession and peer-to-peer networking via gamekit. I’m hoping it will be faster (I need to keep the players in sync at a high frequency), and less prone to WAN based connectivity issues that seem to plague Apple’s matchmaking interface.

Before I reinvent the wheel, is there a version of GameKitHelper that does the peer-to-peer stuff?

Thanks