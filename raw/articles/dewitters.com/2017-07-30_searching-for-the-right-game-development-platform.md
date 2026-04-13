---
title: Searching for the right game development platform
url: https://dewitters.com/searching-for-a-game-development-platform/
published: '2017-07-30'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

*This post is part of the series moving aways from ActionScript 3 and Flash.*

There are a lot of programming languages and game libraries available to make electronic games. So which one will I pick to port [RPG Playground](http://rpgplayground.com) to? To find out, let’s first define what I need.

# Must Haves

## Supports Web Browser games

The major advantage of [RPG Playground](http://rpgplayground.com) over other game editors is that you can use it straight in your web browser. No download, no installation, no wasting of disk space. So the technology I pick should definitely support web browsers.

It seems that there is only 1 choice of technology for that: HTML5 with either canvas or WebGL.

So the game development platform should definitely support export to HTML5

## Multiplatform

There are so many platforms now. Web-browser, desktop, mobile, game consoles, … . Lots of opportunities for game developers. I don’t want to limit the games that my users make to a certain platform. Want to make a mobile RPG? Or one for consoles? Or one of web? Or plain old Windows? Or maybe you definitely need to support Linux? I got you covered.

So multiplatform support on both the programming language and for libraries is very important.

## Open Source

The libraries and technology that I use needs to be open source. I worked with closed source libraries in the past, and the drawback is that you are dependent on the vendor to support and fix certain things. With open source, you always have a way to do it yourself. I like that.

## Highly productive

I want to be able to produce the most functionality with the least amount of effort. This means I want some high level language, and some easy to use libraries that take the burden out of my hands.

# Nice to haves

## Toolchain runs on Linux

I’ve been developing ActionScript 3 for some time now, and the best IDE is by far FlashDevelop, which unfortunately only runs on Windows. But lately I’m getting more fed up with Windows 10.

After a few days of not turning off my computer, my hard disk gets accessed constantly and everything slows down. It also acts weird when some sound starts playing. So… back to Linux (probably Mint).

## Shaders

Almost every platform has hardward 3D acceleration now, including shaders. It would be nice to give my RPG games an extra touch by using shaders.

# Programming language/environment choice

## Unity 3D

Unity 3D is very popular nowadays with indie game developers. It’s a very nice multiplatform game development environment. But there is a huge major drawback for me: Whenever my users export their game and want to distribute it, they need a valid Unity 3D license. I don’t want that, and neither do my users.

It’s also not open source, so I don’t have enough control over it.

On to the next thing.

## JavaScript

There are some nice JavaScript game libraries, but I consider the dynamic typing of the language a drawback.

The RPG Playground codebase is becoming bigger, so it’s nice to have some static typing to protect you.

## Haxe

I’ve been keeping an eye on [Haxe](https://www.google.be/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwi905-bnKzVAhUNEVAKHe1ECE4QFggoMAA&url=https%3A%2F%2Fhaxe.org%2F&usg=AFQjCNFLt7S1g20dItRTNsqYogSDpqVdFA) for some time now, and it shouts “multiplatform” more than any other language. Being able to compile to a [huge list](https://haxe.org/documentation/introduction/compiler-targets.html) of other programming languages, there is nothing else that compares to it. Although it might make things more complex when debugging.

Conclusion: Haxe it is!

# Game library choice

RPG Playground has a specific requirement. Because it is a game editor, it needs its own high level game library with entity/component system, data driven design and dynamic adaption of the running game.

So it needs libraries to draw images, play sound and music, and handle 2D physics. But needs freedom related to game objects and overall game architecture.

After reviewing a lot of game libraries, I narrowed it down to 2: [OpenFL](http://www.openfl.org/) and [Kha](http://kha.tech/).

## OpenFL

Probably the most famous Haxe game library. It is very mature, has a large community, and the API is based on Flash. This last part means that porting my ActionScript3 code would be really straight forward.

On the other hand, my dependencies on external libraries is shielded off as I [described earlier](http://www.koonsolo.com/news/flexible-use-of-game-libraries/), so changes would be minimal anyway.

OpenFL has a lot going for it, but the use of shaders doesn’t look straight forward.

## Kha

Kha annouces itself on its wiki as “Think SDL, but super-charged.”. Since my experience with SDL has always been very nice, they got my attention.

Kha supports more platforms than OpenFL. Especially because you can target Unity 3D, which opens up a whole lot of platforms that are otherwise harder to target.

A quick look in the [API](http://api.kha.ktxsoftware.com/kha/graphics2/index.html) shows a very simple, straightforward interface.

2D graphics are hardware accelerated if the platform supports it. And shaders are supported by a shader cross compiler called Krafix.

Conclusion: Kha it is!

## 0 Comments