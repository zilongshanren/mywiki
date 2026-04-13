---
title: Exporting RPG Maker games to iPhone, Android or other platforms
url: https://dewitters.com/exporting-rpg-maker-games-to-iphone-android-or-other-platforms/
published: '2014-03-21'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

![mobiledevices Mobile devices are so popular](../../assets/ca7e5a46457d0205.jpg)

Mobile devices are so popular

Although RPG Maker doesn’t officially support building games for other platforms than Windows, some people have succeeded in doing so. All available options will be explained in this blog post. So if you know of any other options to port an RPG Maker game to other platforms, please contact me or leave a comment below, so I can improve this article.

RPG Maker is probably the most popular tool to make your own JRPG’s. Unfortunately, it is only available for Windows, and can only create Windows games.

As far as Enterbrain (the creator or RPG Maker) is concerned, Windows will remain the only platform that they officially support. This is extensively explained in [a forum post on their official website](http://forums.rpgmakerweb.com/index.php?/topic/1343-do-not-ask-if-rpg-maker-games-can-be-made-to-run-on-your-ds-psp-whatever/). The general conclusion is that it’s technically too difficult or costly for them to support other platforms. RPG Maker heavily depends on Windows only technology, which makes it nearly impossible to go beyond the Windows platform.

![final_fantasy Final Fantasy, the mother of all Japanese role-playing games](../../assets/88077ef3455bef64.png)

Final Fantasy, the mother of all Japanese role-playing games

Although technically difficult, exporting RPG Maker games to other platforms has always been a mayor feature request, and I’m sure Enterbrain had many attempts to do so. In 2012 for example, someone named Mitchell [declared on Steam](http://steamcommunity.com/app/220700/discussions/0/846939614976997143/) that they were working on supporting other platforms, and it even got [confirmed by other reliable sources](http://forums.rpgmakerweb.com/index.php?/topic/10485-exporting-to-xna-ios-android/). But since then nothing has turned up, so I’m afraid we can assume that all these efforts were in vain.

So if exporting your games to other platforms is not officially supported, what options are there? Well, let me explain what’s currently known on this subject.

## Don’t use RTP resources!

First of all, if you ever intent to port your game to non-Windows platforms, make sure you don’t use any RTP or RTP derived resources. That license is very restrictive, and doesn’t allow you to use these resources on games that are not using the RPG Maker Windows engine. So if you don’t want to get sued, stay away from using the default RTP resources.

## Use MKXP for Linux/Mac

![to the moon To the moon, made with RPG Maker XP](../../assets/185a9d0891289c29.jpg)

To the moon, made with RPG Maker XP

The commercial game “[To The Moon](http://freebirdgames.com/to_the_moon/)” was created with RPG Maker XP, and was successfully ported to Linux. It uses [the mkxp library](https://github.com/Ancurio/mkxp), and it is probably the most straight forward way of porting your RPG Maker game.

It is an open source library that provides the same Ruby Game Scripting System as RPG Maker XP (RMXP). And if I take a look at the libraries used, this could also be used for a MacOS version of your game. Since it’s Open Source, a good programmer should be able to make it available on MacOS X. But remark that this is for RPG Maker XP, and not the newer RPG Maker VX (Ace) (RMVX).

## Porting your game to another engine

When you want a version of your RPG Maker game to run on other platforms such as iPhones, iPads, Android tablets or phones, you will have to do some manual porting. This means using another game engine and programming language to reconstruct the logic of your game.

![240746-zenonia Zenonia, an RPG for iPhone](../../assets/d2ef9211f504b2d0.jpg)

Zenonia, an RPG for iPhone

The first game engine that comes to mind is [Unity 3D](http://unity3d.com/). It supports plenty of platforms (iOS, Android, Windows Mobile, BlackBerry, OSX, Linux, Web Player, PS3, Wii U, Xbox 360), isn’t too expensive, and has a large community.

Another option is using [Haxe](http://haxe.org/) in combination with [OpenFL](http://www.openfl.org/). You can find a [detailed explanation on gamasutra](http://www.gamasutra.com/blogs/LarsDoucet/20140318/213407/Flash_is_dead_long_live_OpenFL.php) on how to use it for creating your games. It also supports plenty of platforms like Windows, Mac, Linux, iOS, Android, BlackBerry, Firefox OS, Tizen, Flash and even HTML5.

But whatever engine you choose, it still requires a lot of (technical) work, and you need to repeat this for every game you want to export.

## Plan B: Emulation

Emulation is an option if you want to play RPG Maker games on other platforms, but not if you want to distribute your own game on these platforms. Some emulators even run the complete RPG Maker editor.

For Linux, you can use Wine as described in [this post](http://forums.rpgmakerweb.com/index.php?/topic/3069-install-rpgvxace-in-ubuntu/).

A similar solution exists for MacOS using Virtual Box, more details [here](http://blog.rpgmakerweb.com/tips-and-tricks/rpg-maker-on-your-mac/).

For android, there is a [Neko RPGXP Player](https://play.google.com/store/apps/details?id=net.kernys.rgss) that can play RPG Maker games on your android device.

## Conclusion

None of the solutions currently available are easy. They all require a lot of effort. This is probably also the reason why commercial game developers such as [Amaranth games](http://www.amaranthia.com/) and [Aldorlea](http://aldorlea.org/) haven’t ported their games to other platforms. I’m sure they are disappointed for not being able to make their games available on Mac or Linux, or on the now so popular mobile platforms such as the iPad, iPhone or Android devices. But for now, no proper solution exists.

## Working on the solution

One of the reasons why I started [my own RPG creation tool](http://rpgplayground.com) is to support as many platforms as possible. Since I have experience in programming and porting games to a long list of different platforms, I know what technical things you need to take care of when developing a game engine. If you haven’t considered it from the beginning, it might be really hard to get your game on other platforms (but not impossible).

So, what have I done to support this? First of all the main code base of RPG Playground is written in ActionScript3, which allows me to make game builds (out of the box) for the following platforms: Flash, Windows, Mac, iOS and Android. Exporting to any of these platforms can basically be done by a “push of a button”. AS3 also supports other platforms such as the Ouya game console, but extra libraries need to be used for that (which isn’t a major issue).

Unfortunately, Linux is not supported, and neither are game consoles. So for supporting those platforms, a ‘real’ port will need to happen. Since my code base is structured in a way described in [this blog post on how to structure your game code](http://www.koonsolo.com/news/flexible-use-of-game-libraries/), only the generic game library will need to be ported. This is not an effort that is currently in progress, but it will happen once RPG Playground is more feature complete.

One of the main goals of RPG Playground it to let you export your games to any popular platform, by a simple push of a button. That would be really nice if you could already do this, right? But unfortunately, RPG Playground is still under heavy development, and a lot of features are still missing, so I’m afraid for now this also isn’t a viable option. But if you believe this might be a solution in the future, go and [start making your own game with RPG Playground](http://rpgplayground.com).

## 15 Comments

## Mattchaby · June 19, 2014 at 08:17

Great article, thanks a lot! It helped me discover some apps and new ways to share my RM projects. Your platform seems great too!

## hundrick · July 19, 2014 at 18:27

Brilliant, thanx for the advice

## ZEDorDEAD · August 27, 2014 at 06:43

Brilliant platform would really like to see this developed more and made into a product i can subscribe to or buy – 5 star

## Ancu · October 28, 2014 at 18:11

Just for your information, mkxp supports both VX and VX Ace games now.

## Aiham · December 29, 2014 at 13:35

thx very much … very usefull

## Garth · June 14, 2015 at 04:35

Not so much .. This is a poorly titled article and has nothing to do with “Exporting”

It is all about “converting”…..

## Garthisrude · August 13, 2015 at 23:08

Lol. What a tool. This was a very knowledgeable post. Go type into google “define: export”. This guy is teaching us how to TAKE FROM windows and GIVE TO iOS. EXPORT. Much like when they exported you from your mothers hooha into the world, this kind and intelectual poster has shown us that you can export your RPG Maker design to iOS. So instead of dogging this guy, in a very rude way, you could realize you are the odd man out and the only one that told this guy his post was bad. Go to reddit if you want to be a douche. Seriously. The post was awesome.

## Garthisrude · August 13, 2015 at 23:10

PS. I love you mods. Please allow my previous post <3

## Garthisrude+1 · October 20, 2015 at 07:00

I’ll second that comment, what a tool bag, this is a very informative article and he’s picking on something so tiny…that the poster is technically CORRECT on.

## Nisshoku · October 28, 2015 at 20:40

Here you go guys. I will post in this thread for you and anyone else coming here. With the release of RPG Maker MV on October 23, it is now possible to package the game for windows, iOS, android and Mac. It costs $79.99 so go on and get it.

http://www.rpgmakerweb.com/

## Riyaan · November 22, 2015 at 04:22

lol

## Riyaan · December 12, 2015 at 07:13

The new RPG Maker – RPG Maker MV allows you to do this through the application itself

## User · February 6, 2016 at 18:57

You should mention EasyRPG Player. It is for RPG Maker 2000 and 2003 games and has a good port for Android. There are also ports for OS X, Wii, GCW Zero and OpenPandora.

There are popular games working already, like “Off” or “Ib”.

## J.A.C · November 13, 2016 at 13:02

Hmm… I understand the majority of it but still very confusion. Before I go on, I am very new to this. I’m a dreamer hoping to make it a reality to help people that love RPG games from the old PlayStation to PS2, play new stories in the same game plays like Final Fantasy, Suikoden, etc. I do not have any of the programs and I need to make my decision before I buy any of it. Are there any recommended program(s) that every like or love that can play on any consoles or devices? Or maybe the most consoles or devices?

Thank you, J.A.C

## Sankalpsk · September 24, 2019 at 08:37

Which android device can run pokemon fire ash