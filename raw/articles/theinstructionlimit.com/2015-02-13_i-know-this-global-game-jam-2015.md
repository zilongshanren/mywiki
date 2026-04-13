---
title: I Know This (Global Game Jam 2015)
url: https://theinstructionlimit.com/i-know-this-global-game-jam-2015
author: Author Renaud Bédard
published: '2015-02-13'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

**“I Know This”** is a game I made for the Global Game Jam 2015 along with [Gavin McCarthy](http://www.artbygavin.com/) (art, design), [Adam Axbey](http://www.adbofdifference.com/) (sound effects) and [Matthew Simmonds (4mat)](https://4mat.bandcamp.com/) (music); I did programming and design. The name we chose for the team was *Two’s Complement*.

As seen on [Kill Screen](http://killscreendaily.com/articles/hold-your-butts-because-now-you-too-can-hack-unix-system/) (who posted the first article on the game, thanks a million!), [Polygon](http://www.polygon.com/2015/2/17/8055759/jurassic-park-hacking-i-know-this), [Popular Mechanics](http://www.popularmechanics.com/technology/a14146/relive-jurassic-park-with-this-fake-unix-system/), [Rock Paper Shotgun](http://www.rockpapershotgun.com/2015/02/20/freeware-garden-i-know-this/) and many more! We’re flabbergasted, and very grateful for how popular our silly jam game has gotten.

## Downloads

**Windows x86 (version 1.1)** : [iknowthis_win_v1.1.zip](http://theinstructionlimit.com/wp-content/uploads/2015/02/iknowthis_win_v1.1.zip)

**Mac Universal (version 1.1)** : [iknowthis_mac_v1.1.zip](http://theinstructionlimit.com/wp-content/uploads/2015/02/iknowthis_mac_v1.1.zip)

**Linux Universal (version 1.1)** : [iknowthis_linux_v1.1.tar.gz](http://theinstructionlimit.com/wp-content/uploads/2015/02/iknowthis_linux_v1.1.tar.gz)

## Soundtrack

4mat released the OST he made for I Know This on [his Bandcamp](https://4mat.bandcamp.com/album/i-know-this-ost), pay what you want!

### Update Notes

**v1.1 (2015-02-20)**

- Linux : Build now works! The Unity 5.0 beta version it was originally built with had issues with Linux, now built with RC2
- Mac/Linux : Builds should be executable out of the zip or tarball without the need for chmod
- Mac/Linux : File icons and names now display correctly, though they are not sniffed from the machine, it’s a pre-built list coming from mine
- Mac : Hacking now affects percentages (yeah… I should’ve tested this a bit more thoroughly)
- Fixed “magenta rectangle” overlay on Shader Model 2.0 or lower GPUs
- Delete key works as well as backspace key to clear red characters
- Tweaked Clicky interactions (6 honeypots instead of 5, the wrong text was triggered when finishing your first hack, mentions more clearly that red text needs to be removed)
- Admin scan bar flashes and turns red when you’re running out of hacking time
- Hacking timer now starts at 35 seconds (originally 30), and will get shorter or longer depending if you fail or succeed hacks (cheap adaptive difficulty!)
- Added license file with credits and acknowledgements (released under a
[Creative Commons Attribution-Non-Commercial-ShareAlike license](https://creativecommons.org/licenses/by-nc-sa/4.0/))

Version 1.1 should clear all known bugs except for the seemingly rare “return does nothing” and the “redtext has HTML code in it” bugs which I can’t reproduce accurately at the moment. Let me know if there are new/other issues! And thanks for your patience.

## Straight outta Isla Nublar

Remember that one scene in Jurassic Park? The one where Lex hacks the computer system in order to lock a door and protect everyone from the raptors, and exclaims…

That was basically the whole premise for our game.

When I saw the movie as a kid, that scene (and the file system UI that Lex “hacks”) always stuck with me as a quintessential faux-futuristic Hollywood representation of how computers work. I learned a bit later that this GUI was not made for the movie, but [actually existed on SGI workstations](https://en.wikipedia.org/wiki/Fsn) and was [ported to Linux](https://en.wikipedia.org/wiki/File_System_Visualizer) as well, so it’s more legit than it looks! But in the end, it’s still a really great artifact of 90’s VR hopes and dreams, in which everything is better in 3D, even file browsers. (and [Web browsers](https://en.wikipedia.org/wiki/VRML), too)

### The Game

It starts with the same basic premise as the scene in the movie : you have to find a file. To make it more interesting than your average hidden object game, you need to hack specific *Search Nodes* (purple files) which, upon successful hacking, will help you narrow down which potential *Golden Folder* contains what you’re looking for. Don’t pick the wrong one though, all the other ones are full of viruses and bad stuff!

Fun fact : the filenames you’ll see in the game are lifted from your hard drive, and [8.3](https://en.wikipedia.org/wiki/8.3_filename)ified for formatting and retro-chic reasons!

Hacking involves mashing your keyboard until code appears, and hitting the return key where the line endings are, just like in real life. The hacking minigame was heavily inspired by [hackertyper.net](http://hackertyper.net/), a fantastic way to feel like you’re real good at making up C code on the fly. However, we gamified it (*oh, the horror*) by not letting you go further than line endings, and adding a timer.

As you hack (or fail to hack) search nodes, sentinels will spawn and start looking for you. If they catch you, they warp you back at the root folder. Not a huge punishment, but enough to make you at least a little careful.

And then there’s *Clicky*, your favourite [Office Assistant](https://en.wikipedia.org/wiki/Office_Assistant) ripoff. He means well, but he sometimes gets in the way… and hides a dark secret. :o

### Closing Thoughts

I don’t know that the game really qualifies as a jam game, because I worked for many evenings after the jam to smooth out the rough edges, make better Clicky interactions, fix the endings and other various bugs. The party version of the game was without music, I asked 4mat to produce something for us after the fact, and we were so *so* * so* lucky to have him contribute the lovely tunes you can hear in the game.

This was also my first experience with Unity 5, but I barely touched what it can accomplish. I’d say that the Audio engine is really nice, ducking was painless to implement… and the new UI stuff (even if it’s 4.6 and not 5) was a joy to use compared to the old GUI system.

And Gavin is the best! First time jamming with him, and it was a great match of design sensibilities, work-mindedness and just plain fun. <3

I hope you support the Oculus Rift :-)

I cannot play this game because there’s a huge pink rectangle covering most of the screen. Please fix this.

Which operating system are you playing the game on? And do you know your system configuration, especially which graphics card you have? Have you tried the game in “Fastest” graphics mode?

The pink box is there in fastest mode, windowed mode, fullscreen, different resolution, every mode I tried.

Bummer. Are you running on Windows, OS X or Linux?

Windows 7. My graphics card is an old Radeon X800GTO.

I’ll see if I can emulate that setup locally, but it just might be that the Unity 5 beta I used doesn’t support that old a videocard… I’ll let you know if I find out anything.

Okay, I was able to fix the pink box (a shader required SM3.0 but didn’t actually need it), so a fix is on the way! :)

It crashes with core dump on Linux x86_64:

-> ./I\ Know\ This.x86_64

Set current directory to /home/kiril/downloads

Found path: /home/kiril/downloads/I Know This.x86_64

Mono path[0] = '/home/kiril/downloads/I Know This_Data/Managed'

Mono path[1] = '/home/kiril/downloads/I Know This_Data/Mono'

Mono config path = '/home/kiril/downloads/I Know This_Data/Mono/etc'

displaymanager : xrandr version warning. 1.4

displaymanager : trying .X11-unix

client :0 has 1 screens

displaymanager screen (0): 2560 x 1600

Using libudev for joystick management

Importing game controller configs


zsh: abort (core dumped) ./I\ Know\ This.x86_64

->

Same exact crash here (Arch x86_64, linux 3.18.6-1, ATI Mobility Radeon HD 6570M) both in windowed/fullscreen and even in “fastest” Unity mode.

I have been getting this exact error.

~~Sorry folks, looks like the Linux build is busted. I didn’t test it before putting it up, I’ll debug it when I get the chance and upload a fixed version.~~v1.1 should work on Linux! Sorry for the wait.

Ah, ah, ahhhh… you didn’t say the magic word.

PLEASE!!! God damn it! I hate this hacker crap.

there seems to be a bug where the text instead of turning red at the end of a line it appears as html text. After that I can never get the line to return correctly.

Ah yeah, I’m actually aware of that one but I haven’t found a good way to reproduce it.

“Clicky” deserves a facepalm. It’s an obvious Windows reference which has no relevance to this film in any way.

That scene in Jurassic Park was just the inspiration, we deviated from it in many ways.

And yep, Clicky is a Dumb Idea, but we like him! ¯\_(ツ)_/¯

Amazing! I’ve always wanted the experience of knowing a Unix System too, since seeing Jurassic Park as a kid. I hope you still plan to fix the Linux version, I’m working on a RetroPie project that would PAINFULLY lack this if it remains broken.

Either way, great work!

Thanks so much! The linux build should be good to go now, give it a shot. :)

Please fix the linux build!

~~Working on it :)~~Edit : v1.1 should work!

Mac version won’t launch. I just get a “The application “I Know This.app” can’t be opened” error. Gatekeeper is off.

Hmm, I was able to start it on my Retina Macbook with Mavericks. Which version of OS X are you on?

Doesnt work on Yosemite, it wont start.

Works on my late 2013 mbp retina with yosemite. Highest res, highest graphics.

Funnily enough, on Yosemite. Figured out it was a UNIX system, got it, and chmod +x’d the executable in the .app package and lo and behold it actually worked. ;)

That’s the spirit! Also… I’ll look into making it executable in the zip file, sorry ’bout that. ^_^

This game made my day. As the original author of FSN, it was great to see this tribute. I especially enjoyed how you reproduced the spotlight.

Even then we knew that this didn’t really work as a file browser. But back in the days when disk cleanup was something I had to deal with on a weekly basis, this was actually a useful tool; big old files stood out like a sore thumb.

Eventually this morphed in to the hierarchical data visualizer of MineSet, a data mining and visualization tool developed by SGI.

Wow, did not expect the author of FSN to come here and play the game! Thanks so much for trying it out and leaving a comment, I’m glad you enjoyed it.

I completely understand how seeing your hard drive spatially helps cleaning it up, we end up having the same problem on today’s small SSDs. I use WinDirStat every once in a while :)

I can’t actually complete 10 lines of code. I get maybe one line of code and when I try to press Return it does nothing. More keyboard banging gives me red characters and eventually the timer runs out.

Windows version

That’s a weird one. The return key is never recognized in the hacking minigame? Do you hear a “beep” noise when pressing the return key even when it’s not moving the cursor?

I have the same issue. It treats the return/enter key as if it’s any other key, and instead of beeping prints out a garbage red character.

Same for me, Mac version.

There is an audible beep when I hit enter, but I can never advance to a new line.

Thanks! I love the concept

I think the current version has a clarity problem :

you need to remove the red characters with the backspace key, the hacking minigame won’t let you progress to the next line unless you make it “compile” by removing syntax errors. If that’s not your issue, let me know!Got it! Everything seems to work correctly now, thank you! Great game.

Haha.. love this for the Jurassic Park reference alone. Also Clicky the f’ing annoying office assistant!

It runs fine on my MacBook Pro (Retina, 13-inch, Late 2013) running OS X Yosemite (ver 10.10) except that the percentages don’t seem to change when I complete a successful hack: they all stay at 100%. Not sure if i’m supposed to do anything on that screen?

In the end I just picked a file at random and gloriously failed miserably=D

Same with me! Successful hacks don’t change percentages on my Mac.

~~Argh, I see why this happens… consider the Mac version somewhat broken too, I’ll post an updated build this weekend.~~Mac version has been updated (v1.1), this issue should be fixed now. Sorry for the confusion!

Everything seems to work for me but no matter how many pink nodes I hack, all the gold nodes display 100%. Am I misunderstanding something? I’m pretty sure I’m getting 10 lines of code out successfully. Playing on a Mac.

Mac version has been updated, this issue should be fixed now. Sorry for the confusion!

Confirming “return does nothing” bug when entering hacking code (impossible to eol). It worked the first time without issue.

Linux system (Ubuntu 12.04), 1920×1200, fullscreen, fastest mode.

By the way, I love every piece of this game idea. Thank you!

Thanks!

Meaning you were able to hack once, but the second node had issues with the return key? Try to backspace all the way on the first line and see if that helps, if you can be bothered to reproduce.

I gave it another couple of tries. In the second game (always picked the wrong folder, dammit) near the end the error reproduced, but I was able to get rid of it by backspacing all the (first) line out. Great!

Also, sometimes the *first* bad character at eol is a *space* what may lead to the wrong assumption that it is incorrect. A space does not appear in red :)

Seriously, this game is great stuff. I encourage you to expand it a little bit (size, random “dungeons”, difficulty progression, etc.) and consider its distribution. I have seen far worse ones going through Humble Bundles and the like.

Spare no expense!

PD: In the end I took the right honeypot. Brilliant :)

Thanks for the kind words! And good call about the “red spaces”, I didn’t think of that… There’s still a 1.2 planned release with Oculus Rift support, I’ll sneak in other fixes in there too.

As far as expanding/selling, we can’t justify spending more time on it right now (we’re all very busy) but who knows… maybe we’ll revisit it later. :)

“(and the file system UI that Lex “hacks”)”

She isn’t trying to hack anything. She is literally just looking for the right file. It’s literally what your game is about, finding the right file.

Yup, hence the quotation marks; I’m aware that it’s not literal hacking, but to the layman it’s a classic movie hacking sequence. I guess intrusion is the right word…

Are lets play videos of this game allowed?

That would be lovely, yes! Drop me a line when it’s posted :)

Is there a README or INSTALL file for the Linux build?

No, but the executable should run as-is. Are you having issues with it?

Bit of an odd issue – return does nothing on the initial screen (when the “I know this” logo is displayed). I’m on Windows 7 – any thoughts or am I just on an old computer?

I can’t get this to run.

Clicking does nothing and running “./I Know This.x86_64” will give me:

“Error in `./I Know This.x86_64′: munmap_chunk(): invalid pointer: 0x000000000365aa10”