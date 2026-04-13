---
title: The craziness that is joysticks on PC
url: http://joostdevblog.blogspot.com/2012/08/the-craziness-that-is-joysticks-on-pc.html
author: Joost van Dongen
published: '2012-08-11'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)for the PC version, I learned that it was even worse than I thought. So for anyone who wants to have a very sour laugh, or considers supporting joysticks in his own game, here is a list of the oddities I have encountered.

Note that when I say joysticks, I actually mean all kinds of controllers, so also steering wheels, big force feedback flight simulator joysticks and of course the kind of controllers used on the Xbox and Playstation.

**Joysticks have different layouts**

This one is rather obvious, because you can actually see this when you look at a joystick: they all look different and the number of buttons and sticks they have can vary wildly. This makes perfect sense, since a flight sim has radically different requirements than a racing game. However, this does make adding proper joystick support on PC always a lot of work, because many joysticks simply don't work if you lack a very complete controls configuration screen.

It gets even more complex because some sticks don't even have a neutral position, like the throttle on a flightsim joystick. Such sticks can remain in full-output all the time, which is an added complexity when detecting what axis or button the user is trying to assign to an action.

![](../../assets/299cfb228cad9975.jpg)

**Similar joysticks have randomly different mappings**

This is where the craziness starts: joysticks that have exactly the same buttons and sticks often output those under randomly different numbers. It seems rather trivial for joystick manufacturers to come together and all agree on the same indices here, since these numbers don't have any impact on the actual features of the controller. Yet somehow they are so incredibly lame that they have never done this, and all have randomly different numbers for the exact same features.

![](../../assets/08976dc328be9bc7.jpg)

**Common libraries OIS and SDL don't support dynamically connecting**

This is rather surprising to me. On console, when the user disconnects his controller he gets a nice warning message, asking him to reconnect. Since this makes a lot of sense, I wanted to do the same on PC. However, it turns out that OIS and SDL, two of the libraries that are used often for multi-platform joystick support, both don't support dynamically connecting and disconnecting controllers. Joysticks only work when they were already connected before the game started, and it is impossible to detect whether a joystick was disconnected.

The lack of this feature is extra surprising when you know how simple this is to implement: both DirectInput and XInput report whether the joystick is still connected when you try to find out which buttons are being pressed. However, somehow SDL and OIS both choose not to expose this information to the user. Meh. Note that SDL does plan to add this in the future in version 2.0 (whenever that comes), but SDL has existed for 14 years already and this seems rather late for such a basic feature.

An extra reason why this is so annoying, is that wireless controllers may report that they are not connected until you press a button. So if you don't press that button before the game starts, then the joystick won't work until you restart the game.

This is the main reason why I chose to remove our SDL and OIS joystick implementations and have instead built my own joystick library with the more low-level DirectInput and XInput libraries.

**Drivers for the 360 controller on PC are insane**

For low-level joystick support on Windows, the best libraries to use are DirectInput and XInput, both by Microsoft. Strangely, there is a battle between XInput and DirectInput, and the choices Microsoft made here are just straight out unbelievable...

The documentation of these libraries suggests that that DirectInput is the

*old*standard, and XInput is the

*new*one. However, this is not the case: XInput

*only*supports the Xbox 360 controller. It does explain that all controllers that don't support XInput are 'legacy' controllers, but XInput is completely inflexible in terms of number of buttons and such. There are some joysticks that support XInput, but they always have to have the exact same layout as an Xbox 360 controller. This means that according to Microsoft, any new flightstick is automatically 'legacy'. I just can't do anything but cry when I see

[this piece of documentation](http://msdn.microsoft.com/en-us/library/windows/desktop/ee417014(v=vs.85).aspx)...

DirectInput on the other hand documents that it is a flexible library that is set up to support every kind of joystick layout. It does not mention, however, that Microsoft's own Xbox 360 controller is one of the few (only?) joysticks that is

*not*properly supported. Here's a little summary of the oddities regarding the Xbox 360 controller:

- In DirectInput, the Xbox 360 controller does not support rumble.
- In DirectInput, the two triggers on the shoulders are mapped to a single axis, so it is impossible to detect pressing both at the same time.
- Voice chat through a headset connected to a 360 controller only works through XInput.

Since the Xbox 360 controller is, as far as I know, by far the most popular joystick for PC gamers, this means that for good joystick support, it is pretty much necessary to always implement both DirectInput and XInput. Lame!

**XInput performance lameness**

An extra 'nicety' of XInput that I came across is that you are supposed to check whether the controller is connected by calling XInputGetState for all four controllers. However, if you do this while they are not connected, then this will cost a

*lot*of performance. I measured this on various PCs and the time it takes to call XInputGetState for four disconnected controllers was 2ms to 10ms (!). On 60fps a single frame can only take 16ms, so 10ms for checking whether 360 controllers are connected is

*a lot*! The solution was to use windows events to learn whether a new Xbox 360 controller might have been connected. It is incredibly lame that XInput itself does not have an efficient way to detect connecting a controller, and it is even lamer how the XInput documentation advertises a method that actually takes a lot of performance if there is no Xbox 360 controller!

**Some joysticks have a "mode" button**

This is a pretty neat feature of some joysticks: to work with games that don't support all kinds of controllers, some joysticks feature a "Mode" button that may do things like making the DPAD act like a stick. On controllers that only have a DPAD and don't have a stick, this is a great feature to support more games. However, if you are programming for such a joystick and don't know this, and accidentally hit the Mode button, then this is a good excuse to get completely confused. An especially nice example of this is the Speedlink PS3 controller:

![](../../assets/30207ce8e81d0633.jpg)

**Some joysticks have buttons that act as several outputs**

This is also a good thing to know and take into account when programming joystick support for a game: when pressing a single button on some joysticks, it outputs as if you are pressing two different buttons. For example, on one specific USB Super Nintendo controller the DPAD outputs both as buttons 1 to 4, and as a stick. Interestingly, the DPAD does

*not*output as a DPAD.

Many of the things mentioned in this blogpost are not useful in any way. They are just the result of incredibly bad design. Not all, of course, but especially the random button mappings and the inconsistencies between DirectInput and XInput are just so stupid and lame...! So, if you ever plan on making a PC game with joystick support, be sure to take these awesome 'features' into account, and plan some serious time to get it right! (Or just waive it, like many developers seem to do, and don't really support joysticks properly. Sure saves a lot of time!)

Very nice and informative post!


ReplyDeleteMany devs choose to support only the official Xbox controller... Why did you go this far?

Because many people have something else and we wanted to do this right. :)

DeleteBecause XBox Controller it's very popular and uses a total diferent API from the other ones.

DeleteAlso, there is a small program that lets you emulate a XBox 360 controller with a legacy controller, many games plays a lot better using that utility than using the game support for legacy controllers.

The utility is called x360ce , if you have a legacy controller I highly recommend you to use that utility, you will be able to play the games that uses only XBox Controller, you will have no problems if a game is not properly configured with your controller and also, you will save time because you will not need to open the button configuration.

xbox controllers use both HID and xinput to communicate with the PC. Games that ONLY support the XBox controller typically use xinput side of things, however if your game supports HID (which is part of the OS) it WILL support the XBox controller and any other HID controller

DeleteBecause they're Awesome, and this is Awesomenauts!

ReplyDeleteI've been using a PS3 controller and a MotionJoy driver to play Awesomenauts. It's been working out great! I love it when devs add in controller support.

ReplyDeleteDon't use MotioninJoy, its a virus.


DeleteUse SCP driver package instead

I've noticed the same things whilst trying to support joypads properly! Extremely annoying for something that should be relatively simple.


ReplyDeleteDo you have any plans to share any of your input code? This is something a lot of developers will be either implementing independently, or as you say, just not doing properly :)

Maybe at some point in the future, but we are also considering to license out our engine at some point, in which case it would be better to not share too much of the actual implementations online...

DeleteInstead of trying to support every single existing controller (I personally think that's too much hassle if not impossible, as there may be controllers you are not aware of out there)


ReplyDeletea better and safer approach would be to just let the player properly map the buttons before playing, so they can choose the layout they like.

Only the most popular controllers, like the 360 one, would be supported out of the box.

Indeed, we have a control configuration menu, but you still need to take into account most of the things mentioned in the post. And the control configuration menu itself is also quite a lot of work by itself.

DeleteFantastic post I have been working on an open source joystick lib and have run in to many of the same things.

ReplyDeleteI know this post is >4 years old, but an update on SDL: SDL2 is pretty awesome when it comes to joysticks and controllers.



ReplyDeleteYou get connect/disconnect events now (finally!).

But what's really cool: it has a "GameController" API that abstracts xbox/playstation like controllers. It gives you consistent axis and button numbering for all supported devices.

And even if a device is unsupported, one can create a mapping to support it afterwards. At least on Linux, Steam lets you do the corresponding configuration in the Big Picture settings and that mapping should then be used by SDL2 games started from Steam.

On other platforms you could still provide mappings via textfile (https://github.com/gabomdq/SDL_GameControllerDB/blob/master/gamecontrollerdb.txt collects them) or environment variable.

And of course the SDL APIs to handle things are much nicer and easier to use than the platform specific things (XInput, DirectInput, /dev/input/js*, ..)

Thanks for the update! :) Does SDL2 support both triggers and rumble on the Xbox360 controller?


DeleteI heard that Steam's controller support currently only does PS4controller and SteamController, others hopefully coming later. Is that what you are referring to?

Yep, the triggers are handled as axes that give you a value between 0 and 32767 (while normal axes from analog sticks use -32768 to 32767).


DeleteRumble also works, see https://wiki.libsdl.org/CategoryForceFeedback

I think Steam supports configuring (and using) all controllers Linux recognizes as joysticks - I tried an old PS2 controller with a cheap USB adapter. More common controllers probably work without configuration, the xbox360 controller certainly does.

(I'm not sure how these things work on OSX and Windows, but I think on Windows SDL2 supports both XInput and DirectInput, so the xbox360 controller should properly there as well. No idea what Steam on Windows or OSX supports in Big Picture, but I guess they support all kinds of joystick-like devices there as well)

DeleteYes, SDL2 supports both triggers and rumble on the XBox 360 controller. The hope is that most of the craziness that you had to deal with is wrapped up nicely now.



DeleteSteam Big Picture does have UI support to map almost any kind of joystick into the SDL game controller API, and saves out a config mapping string. It's roughly equivalent to the controllermap program here:

https://hg.libsdl.org/SDL/file/default/test/controllermap.c

Steam's Steam controller configuration support is separate from SDL's game controller API, and currently only supports Steam controllers and PS4 controllers, but support for any SDL game controller is coming soon.