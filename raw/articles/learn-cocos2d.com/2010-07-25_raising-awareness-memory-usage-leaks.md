---
title: 'Raising awareness: memory usage & leaks'
url: http://www.learn-cocos2d.com/2010/07/coding-cocos/
author: Barry says
published: '2010-07-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

While helping others solve their cocos2d project issues over the past year it became obvious that many projects have at least one major problem in one of these areas:

- memory management
- resource management
- code structure

### Examples

Memory management issues normally range from allocating too much memory, either by loading too many textures up front which are only going to be needed later, or by memory leaks such as scenes not deallocating when switching scenes. Resource management problems range from not adding the right resources to the right target, often resulting in increased App size because resources are added to the bundle but never used by the App. It could also mean loading identical resource files except that they have different filenames (copies?), using up additional memory. Or not tightly packing sprites into Texture Atlases but instead using one Texture Atlas per game object - while this is understandable from a standpoint of logical seperation it does waste opportunities for optimization.

Finally, code structure or lack thereof regularly leads to “everything in one class” code design which is most likely an evolutionary process rather than intentional. It’s not uncommon to see classes with thousands of lines of code, sometimes even going past 10,000 lines of code in one class. Other things are using too many CCLayers without them adding a clear benefit, for example just to group all nodes at a specific z order together or to group them by functionality, eg one layer for enemies, one for players, one for background, one for UI, one for score, one for particle effects, and so on - without any of these layers being used for what they’re really good at: modifying multiple nodes at once, like moving, scaling, rotating or z-reordering them. And of course there’s the copy & paste hell, large blocks of code reproduced in various places only to modify some parameters instead of creating a method which takes the modifiable parameters as arguments. Even professionals I worked with got so used to doing that it became hard just to overcome the resistance of letting go of old habits. But they learned.

### Summary

Nothing of this code design and structuring strikes me as odd or surprising. I’ve written code like this myself. I also believe if it’s good enough and works, then why the hell not? It’s a matter of experience and it’s only with experience that you clearly see how to improve things. This boils down to the regular learning curve where only training and tutoring and just simply making mistakes and learning from them helps in the long run. That’s how we learn things.

On the other hand, the things like Memory and Resource Management can also be learned but they have a different nature. They can be statistically assessed, they could be calculated and verified automatically. This makes me wonder if there isn’t some kind of automation and information tools that would help developers achieve better results in terms of memory usage and resource management? In the meantime it’s all about raising awareness …

### Raising Memory Awareness

Most importantly I think we need to raise more awareness to these issues to cocos2d developers. One step towards that would be for cocos2d to display a “available memory counter” alongside the FPS counter. I used to patch CCDirector to simply display memory instead of FPS since that was always more important to me. Fellow cocos2d developer Joseph sent me his version to display both - I simply didn’t think of the obvious. So if you’d like to see FPS and available memory next to each other I think you can handle the changes to CCDirector outlined here:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 |
// CCDirector.h, add below @interface: +(double) getAvailableBytes; +(double) getAvailableKiloBytes; +(double) getAvailableMegaBytes; // CCDirector.m, add as appropriate: #include <sys/sysctl.h> #import <mach/mach.h> #import <mach/mach_host.h> [...] +(double) getAvailableBytes { vm_statistics_data_t vmStats; mach_msg_type_number_t infoCount = HOST_VM_INFO_COUNT; kern_return_t kernReturn = host_statistics(mach_host_self(), HOST_VM_INFO, (host_info_t)&vmStats, &infoCount); if (kernReturn != KERN_SUCCESS) { return NSNotFound; } return (vm_page_size * vmStats.free_count); } +(double) getAvailableKiloBytes { return [CCDirector getAvailableBytes] / 1024.0; } +(double) getAvailableMegaBytes { return [CCDirector getAvailableKiloBytes] / 1024.0; } [...] -(void) showFPS { frames++; accumDt += dt; if ( accumDt > CC_DIRECTOR_FPS_INTERVAL) { frameRate = frames/accumDt; frames = 0; accumDt = 0; // the only change in showFPS is this line: NSString *str = [[NSString alloc] initWithFormat:@"%.1f %.1f", frameRate, [CCDirector getAvailableMegaBytes]]; [FPSLabel setString:str]; [str release]; } } |

### Raising awareness to leaking Scenes

In addition I highly, strongly and with utmost reinforcement (without pulling out a gun) recommend to cocos2d developers to frequently check your scene’s dealloc methods. Preferably add a breakpoint there, or at the very least add the logging line: CCLOG(@”dealloc: %@”, self). If you want a more visible but less intrusive method you could do something like flashing the screen or playing a sound whenever the last scene is deallocated, so that you get so used to it that when you’re not seeing or hearing it anymore it immediately raises your attention.

If at any time during the development of your project the dealloc method of a scene isn’t called when you change scenes, you’re leaking memory. Leaking the whole scene is a memory leak of the worst kind. You want to catch that early while you can still retrace your steps that might have caused the problem. Once you get to using hundreds of assets and thousands of lines of code and then realize the scene isn’t deallocated, you’ll be in for a fun ride trying to figure out where that’s coming from. In that case, removing nodes by uncommenting them until you can close in on the culprit is probably the best strategy, next to using Instruments (which I haven’t found too helpful in those cases).

[I ran into such a problem once](http://www.cocos2d-iphone.org/forum/topic/5354) because I was passing the CCScene object to subclasses so that they have access to the scene’s methods. The subclass retained the scene and was itself derived from CCNode and added to the CCScene as child. The problem with that: during cleanup of the scene it correctly removed all child nodes but some of the child nodes still retained the scene. Because of that their dealloc method was never called, and in turn the scene was never deallocated.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

the

#include

#import

#import

are empty?

What should those be?

Thanks![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Sorry, the darn WYSIWYG editor messed up the formatting … again. Now using a much nicer codebox.

Thanks! Works like a charm, only in the latest cocos2d version frameRate should be frameRate_

Hey Steffen,

I’m having some trouble with this line:

kern_return_t kernReturn = host_statistics(mach_host_self(), HOST_VM_INFO, (host_info_t)&vmStats, &infoCount);

Getting errors that say amp is undeclared and there are not enough parameters.

Any ideas?

Great article by the way.

Thanks, fixed it. The & should simply be &

Thanks for the prompt reply.

Works great!

Great post, I am having the same problem with my project. I have multiple CCLayers. The game play layer is a child of the scene and the other layers are a child of the main layer.

- One for game play

- One for pause, reply, end game menu

- One for HUD stuff (score, health, etc.)

- One for power-up animations

And after playing multiple games in the same session my memory alloc will sometimes jump though the roof when replacing scenes and eventually crash the game. I want to keep the layers because I am performing actions such as fading the whole layer.

However I can not find a decent code example anywhere that shows how to properly alloc and release multiple layers in one scene. Do you know of any?

- Looking forward to the book, Thanks.

If you rely on cocos2d’s memory management mechanism you only need to remove the layer from its parent:

CCLayer* layer = [CCLayer node];

[self addChild:layer];

…

// later

[self removeChild:layer];

You should use alloc/retain as little as possible when programming with cocos2d.

For what it’s worth I explained the use of several layers in the same scene in the book, and in general how to work with Scenes and Layers. It’s Chapter 5 and now available in the Alpha program.

Thanks, that was definitely part of the problem. I also forgot to unschedule and update method. I have my memory back.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Hello,

Thanks a lot for your wonderful tutorial. I am facing memory issue and I seriously need some advice now![:(](../../../wordpress/wp-includes/images/smilies/frownie.png)


My de-alloc functions are being called. I check every object I created is de-alloced. However when ever I start the game again from main menu, the instrument show additional memory of 120MB. I was reading online that instrument can’t be perfect most of the times, is there some settings, I need to change?

Any advice will be highly appreciated.

PS: I am checking if the object is de-alloced by taking “reference-counter” after [super dealloc] amd release are called….

Thanks.

I heard the same about Instruments. Instead I use the available memory code in this collection to find out how much memory is actually being used as the game is running:

http://www.learn-cocos2d.com/knowledge-base/free-source-code/

Hi,

The link provided is broken

http://www.learn-cocos2d.com/knowledge-base/free-source-code/

I got leak on children sprites..

when i add a lot of child on a sprite [sprite addChild:another sprite];

there will be leaks on [[children alloc] initwithcapacity:4 - not sure

but this pops out on the leak tool,

what should i do..?

help me out please

Is that in your code:

[[children alloc] initwithcapacity:4]

It seems like that would be part of Cocos2D. If it is, it’s a leak in the engine. But I doubt that since the leak tool (Instruments?) often reports false negatives. As long as the memory leaked is just a few bytes (usually 16 to 64 bytes) that shouldn’t be an issue.

This doesn’t work with the latest cocos2d v0.99.5-rc1, can you look into it?

I fixed the problem for this, there is only one little thing to change within this line:

NSString *str = [[NSString alloc] initWithFormat:@”%.1f %.1f”, frameRate, [CCDirector getAvailableMegaBytes]];

Change to this:

NSString *str = [[NSString alloc] initWithFormat:@”%.1f %.1f”, frameRate_, [CCDirector getAvailableMegaBytes]];

The only change was the underscore at frameRate_

it gave me some headache at first but then I realized how simple it was…

Hi,

Few questions:

- How much generally “available memory counter” should show. What is regarded as good value or range.

- What is the number I shouldn’t go under (Threshold number for good app) .

- Whenever I add image or audio file in my resources folder and next time run the app, the “available memory counter” goes down. Is this usual or am I missing something.

Thanks

Hi

I know this is a pretty old post, but I was wondering if the dealloc “trick” to catch leaking scenes still applies under ARC?

Thanks

Yes, it does. The dealloc method only runs if the object is actually deallocating, ARC or not.

Correct, I just wanted to make sure because it seems NONE of my scenes get dealloced when changing scene, almost to good to be true?!

Just want to say thank Steffen, this post helped me understand my retain cycle issues much better. Also, the breakpoint action on dealloc is a great tip to ensure you don’t leak scenes. Much appreciated!

Writing this guide helped me too. I applied what I learned to KoboldTouch and with a little help from ARC I found a way to tell when your previous scene leaked after changing scenes. This is really helpful because if you immediately get notified of a newly introduced retain cycle you better understand why it’s happening (you still remember the most recent code changes). Probably helped me avoid hours of bug-hunting already.