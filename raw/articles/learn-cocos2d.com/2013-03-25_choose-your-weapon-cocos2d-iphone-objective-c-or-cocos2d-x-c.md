---
title: 'Choose Your Weapon: Cocos2D-iPhone & Objective-C or Cocos2D-X & C++'
url: http://www.learn-cocos2d.com/2013/03/choose-weapon-cocos2d-iphone-objective-cocos2d-x/
author: Smin Rana says
published: '2013-03-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

This is a guest post by Nat Weiss, author of the

[cocos2d-iphone RPG Game Engine]and the[cocos2d-x Paralaxer Game Kit]. Today he shares his experience working with the two most popular cocos2d game engines, and explains how and where they’re different.He also

[needs more beta-testers]for his latest game:[Awesome Heroes Arena].

Over the last year, my bro Kristopher Horton and I have been developing a realtime [Multiplayer-Online Battle Arena](https://en.wikipedia.org/wiki/Multiplayer_online_battle_arena) (MOBA) game for tablets with cocos2d-x. The game’s called ** Awesome Heroes Arena** and we are finally at the point of taking on beta testers: here’s the

[beta sign up](http://www.surveymonkey.com/s/26VPPXR)if you are interested.

Steffen thought it would be interesting if I shared some thoughts on switching from cocos2d-iphone to cocos2d-x. What’s it like? What things do I miss?

#### Why did we choose cocos2d-x?


Before we go into that, it’s important to understand our reason for choosing cocos2d-x. We wanted to develop one codebase and be able to deploy to varied platforms. The challenge (and blessing) of cocos2d-iphone is that you develop with Objective-C and Apple’s [Foundation Kit](https://en.wikipedia.org/wiki/Foundation_Kit). Trying to port that foundation to Android is tricky business.

Yes, the newer Android tool chains support GCC 4.6+ and therefore can compile Objective-C code, but you’re still missing the Foundation Kit. Yeah, there are open-source alternatives, but even after implementing those you still need to write some Java code to handle input, setting up the window and playing sounds. Cocos2d-x does all that for you.

So because we wanted to be able to deploy to iPad, Kindle Fire and even have the option of going to Windows, and since we were already familiar with the cocos2d paradigm — okay, and also because we are frugal open-source advocates — we chose cocos2d-x.

#### So what’s cocos2d-x like?

Well, first of all, you develop in C++ as opposed to Objective-C. You can now use Javascript and Lua as well, but for the purpose of writing a larger, more complex game, I find C++ to be essential.

Yes, there is a tiny bit of Objective-C to get your iOS app started, and there’s a little Java to get your Android app going, but these are mostly behind the scenes, handled nicely by cocos2d-x.

Switching from Objective-C to C++ is kind of like switching between Australian and Canadian accents. There’s some higher-level differences there, some raised eyebrows may be inevitable, but the fundamentals of the language are the same. Both languages have their roots in C. Sacred, simplistic, procedural C. So it isn’t too difficult to switch.

#### Objective-C vs C++

There’s plenty of stuff I miss from Objective-C and there’s a few things C++ has that I wish Objective-C would.

The thing I miss most about Objective-C is the readability. Consider the following:

|
1 |
[myPlayerObject swingSwordAt:target withDuration:1.0f]; |


Pretty clear, right? Every parameter has a name, sweet. Consider the C++ equivalent:

|
1 |
myPlayerObject.swingSwordAt(target, 1.0f); |


Now it’s unclear. What’s that 1.0f represent? There’s ways of getting around that, like using a clearly named variables:

|
1 2 |
float swingDuration = 1.0f; myPlayerObject.swingSwordAt(target, swingDuration); |

However, that can get cumbersome, and when you’re feeling lazy who wants to do that? In my humble opinion, Objective-C has a decided advantage in code readability.

On the flip side of the coin, I wish you could overload operators in Objective-C. Consider this cocos2d-iphone snippet:

|
1 |
CCPoint pos = ccpAdd(ccpMult(ccp(150.0f, 300.0f), 0.5f), anotherPos); |

Ugh! That looks horrible and is hard to understand. Consider the C++ alternative if you subclass CCPoint and give it some overloaded operators:

|
1 |
MyCCPoint pos = (mccp(150.0f, 300.0f) * 0.5f) + anotherPos; |

Much better.

#### cocos2d-iphone vs cocos2d-x

Besides the languages, there’s really not much difference between cocos2d-iphone and cocos2d-x. They are the exact same API and are neck and neck when it comes to versions.

When it comes down to it, if cocos2d-iphone could deploy to Android and Windows, there’s no debate in my mind I’d stick with Objective-C! For more info on the topic, check out my article at Paralaxer.com: [C++ vs Objective C](http://paralaxer.com/cpp-vs-objective-c/).

#### Multiplayer Code

Steffen also asked me about the multiplayer aspect of AHA. What framework did we use? Is the game peer 2 peer (P2P)?

First off, AHA is a peer to peer game. We wanted to have the lowest ping times between players and also lighten our server load, so going P2P was one of our first, albeit difficult, choices.

The choice was difficult because the client-server model is so popular (most frameworks don’t even support P2P), the client-server model makes it difficult to cheat, and frankly, this was my first realtime multiplayer game I’d ever written. The choice seemed daunting. In the end, doing the math on ping times and server loads helped to make the choice clear.

Regarding the framework, we went with [Raknet](http://www.jenkinssoftware.com/) because it’s C++, supports P2P, and has an affordable hobbyist license. Though after using Raknet for a year, I have mixed feelings about it.

Raknet does everything it claims to and on the outside, and it appears to do them well. But on the inside, the code can sometimes resemble spaghetti code. It makes me wish the programmer had read [Scott Meyer’s Effective C++](http://www.aristeia.com/books.html). I guess in the end, that doesn’t really matter as long as it works, right?

#### Multiplayer Frameworks

If you’re at the point of choosing a multiplayer framework for your game, besides [Raknet](http://www.jenkinssoftware.com/) there’s also [Photon](http://www.exitgames.com/), [Electroserver](http://www.electrotank.com/es5.html), [Chilly](http://chillyframework.com/), [NodeJS](http://nodejs.org/) and [SmartFox](http://www.smartfoxserver.com/). If you’d rather roll your own, then I think it’s possible with [Boost’s asio](http://www.boost.org/doc/libs/1_53_0/doc/html/boost_asio.html).

When it comes to writing server-side code, it really helps to use the same language for the client/peer as the server. You’re going to have to switch back and forth between writing something client-side to make it work server-side, and vice versa.

That’s a bonus point to RakNet. We use it on both ends, pure C++. The added benefit here is that packets can be encoded and decoded exactly the same. I can’t even imagine the nightmares I’d be facing if my client was C++ and the server was Java.

#### Check out Awesome Heroes Arena!

So that’s about it for this post. I hope you learned a thing or two and if you’ve got any questions, hit me up in the comments. If you’d like, you can follow our progress with *Awesome Heroes Arena* on our website at [EscBros.com](http://escbros.com/) or join our [beta test](http://www.surveymonkey.com/s/26VPPXR). Here’s the little trailer movie Kristopher put together:


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Very nice explanation![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)