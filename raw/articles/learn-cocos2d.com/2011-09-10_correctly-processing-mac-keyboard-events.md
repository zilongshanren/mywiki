---
title: Correctly Processing Mac Keyboard Events
url: http://www.learn-cocos2d.com/2011/09/polling-mac-keyboard/
author: Kobold; Learn; Master Cocos
published: '2011-09-10'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Wouldn’t it be cool if you could just check the keyboard state at any time from any class?

I’ll get to the “cool” part in a moment, first let me set the record straight on how to correctly process keyboard input in Cocos2D Mac builds:


#### How NOT to process Mac keyboard input events!

A lot of the keyboard input example code for Cocos2D I found is just wrong. Unfortunately, it’s been copy & pasted numerous times already. No wonder users are being frustrated about Cocos2D Mac keyboard input event processing.

For example, in [this thread](http://www.cocos2d-iphone.org/forum/topic/11725) the code is comparing Apples (unicode character codes) with Oranges ([ASCII codes](http://www.asciitable.com/)):

[cc lang=”c”]

- (void)ccKeyDown:(NSEvent*)keyDownEvent

{

// Get pressed key (code)

NSString* character = [keyDownEvent characters];

unichar keyCode = [character characterAtIndex: 0];

// WRONG: unichar != virtual keycode

if (keyCode == 119) { … } // Up

if (keyCode == 115) { … } // Down

if (keyCode == 100) { … } // Left

if (keyCode == 97) { … } // Right

…

[/cc]

Maybe this works on some systems with unicode disabled, maybe it worked on older Mac OS X versions, maybe it works only if your locale is set to US. It’s definitely not working across all systems.

Some clever folks also turned to comparing the event’s characters which gets around the unicode issue, but won’t help you with keys that don’t print a human-readable character (Page Up, Page Down, Arrow Keys, etc.):

[cc lang=”c”]

-(BOOL) ccKeyUp:(NSEvent *)event

{

if ([[event characters] isEqualToString:@”a”]) {

//do something

}

…

}

[/cc]

#### How Mac keyboard input processing is really done!

The working solution is really simple, you just get the event’s keyCode and compare it with the virtual key codes defined in the Carbon framework:

[cc lang=”c”]

#import

- (void)ccKeyDown:(NSEvent*)keyDownEvent

{

// Get pressed key (code)

UInt16 keyCode = [event keyCode];

// this actually works:

if (keyCode == kVK_ANSI_W) { … } // Up

if (keyCode == kVK_ANSI_S) { … } // Down

if (keyCode == kVK_ANSI_A) { … } // Left

if (keyCode == kVK_ANSI_D) { … } // Right

…

}

[/cc]

The virtual key codes are defined in **<HIToolbox/Events.h>** and posted for convenience in [this forum thread](http://forums.macrumors.com/showthread.php?t=780577). You can include all the virtual key code constants (an enum) in your own Mac app by including **<Carbon/Carbon.h>**. You don’t have to link with the Carbon.framework for using the key code constants.

Using the virtual key codes has another huge advantage: it completely ignores the user’s keyboard layout like language-specific input sources and remapped modifier keys.

For example, it’s quite possible that there’s an odd keyboard layout for some odd language like “Simplified Polynesian Hyperglyphs” or a really, really odd language like “French” where users might not have a “w” key, but instead have to press Shift+Command+Option+Numpad5 to generate the “w” character. Those users will never figure out how to move upward, or they’ll be waiting for you around the corner. Who knows?

By using virtual key codes, it’s not the character that’s important but the location of the key on the keyboard. And keeping the input keys at the same location on the keyboard, you can imagine that’s going to be more important for games than getting a specific character code.

#### Introducing KKInput

The above code is still using Cocos2D’s event-driven input method. But you can’t just check if a certain key is pressed anywhere in your code. That’s something I’m fixing right now.

The following code is a simple keyboard input test with the polling API of the KKInput system that I’m writing for [Kobold2D](http://www.kobold2d.com/). The method can be in any class and can be run at any time, for example in your player character’s update method:

[cc lang=”c”]

-(void) moveShipByPollingKeyboard

{

const float kShipSpeed = 3.0f;

KKInput* input = [KKInput sharedInput];

CGPoint shipPosition = ship.position;

if ([input isKeyDown:kVKC_UpArrow] ||

[input isKeyDown:kVKC_ANSI_W])

{

shipPosition.y += kShipSpeed;

}

if ([input isKeyDown:kVKC_LeftArrow] ||

[input isKeyDown:kVKC_ANSI_A])

{

shipPosition.x -= kShipSpeed;

}

if ([input isKeyDown:kVKC_DownArrow] ||

[input isKeyDown:kVKC_ANSI_S])

{

shipPosition.y -= kShipSpeed;

}

if ([input isKeyDown:kVKC_RightArrow] ||

[input isKeyDown:kVKC_ANSI_D])

{

shipPosition.x += kShipSpeed;

}

ship.position = shipPosition;

}

[/cc]

KKInput will also have an event-driven API, but instead of sending you every event it works by hooking up a selector with a specific input mapping. The mapping could be a single key or mouse button, or a combination of keys, or even a combination of keys, modifiers and mouse buttons that trigger the action and call the specified selector. So you don’t basically just define the keys that should trigger an action, then write the code for the action without all the nitty-gritty input processing stuff.

KKInput is a cross-platform API, so you won’t have to **#ifdef** your input code when you switch over to iOS development. If you run this example on iOS it’ll just ignore all requests to the keyboard (returning nil/NO). I just started working on KKInput today, so it’s still a while before I can release it, and I have some ideas to simplify and unify input event processing in general that I want to test-drive.

In the meantime I’d like to hear from you: do you have a GamePad or any other specialized game input device hooked up with your Mac? Do you think it’ll be worthwhile to add GamePad/Joystick support?

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] Correctly Processing Mac Keyboard Events […]

Thanks for the awesome explanation!

I was searching google for solutions to handling the alpha keys when using the keyboard in different languages — ie. when the unicode string matching was failing — and came across your post.

Looking forward to checking Kobold very soon!

Thanks again,

-flod.