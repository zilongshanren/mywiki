---
title: Zombie company feeds on old Flash games
url: https://dewitters.com/zombie-company-feeds-on-old-flash-games/
published: '2017-07-10'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

## The Discovery

Today I was wrapping up my new release of [RPG Playground](http://rpgplayground.com). But when testing, I suddenly saw the following screen:

![](../../assets/8d63adc6041fa322.png)


Which is pretty strange, because I don’t have any ads in RPG Playground whatsoever.

After this initial screen, some other advertisement appeared at the bottom-left of my [RPG making](http://rpgplayground.com) software:

This obviously needed some further investigation!

## The investigation

RPG Playground is built using ActionScript3, and generates a Flash application (I can feel you programmers shivering already!). The reason why I’m still using this notorious technology is up for another discussion.

Anyway, I had to find out where these ads were coming form, because I definitely didn’t add them. The ads are using the [CMPStar](https://www.cpmstar.com/) advertisement network.

After investigating some external libraries that I’m using, I came across some old MochiBot tracking code. And yes, after removing that part, the ads were gone!

MochiBot used to monitor traffic for Flash applications. Kind of like google analytics for Adobe Flash, but way simpler. Unfortunately in 2014, [MochiMedia](https://en.wikipedia.org/wiki/Mochi_Media), which owned MochiBot, was shut down.

But the code was still living on in my code base. To be more specific, the following code:

public dynamic class MochiBot extends Sprite { public static function track(parent:Sprite, tag:String):MochiBot { if (Security.sandboxType == "localWithFile") { return null; } var self:MochiBot = new MochiBot(); parent.addChild(self); Security.allowDomain("*"); Security.allowInsecureDomain("*"); var server:String = "http://core.mochibot.com/my/core.swf"; var lv:URLVariables = new URLVariables(); lv["sb"] = Security.sandboxType; lv["v"] = Capabilities.version; lv["swfid"] = tag; lv["mv"] = "8"; lv["fv"] = "9"; var url:String = self.root.loaderInfo.loaderURL; if (url.indexOf("http") == 0) { lv["url"] = url; } else { lv["url"] = "local"; } var req:URLRequest = new URLRequest(server); req.contentType = "application/x-www-form-urlencoded"; req.method = URLRequestMethod.POST; req.data = lv; var loader:Loader = new Loader(); self.addChild(loader); loader.load(req); return self; } }

For you programmers out there, you can see that it loads a *remote *library! Which means that they can change the library at any time they want!

## The horror

So after discovering this horror, I checked my *online* version of RPG Playground. OH MY! It also featured ads I never requested. (Sorry loyal RPG Playground users!)

Which means that any Flash game that uses MochiBot traffic tracking, is now showing ads.

Back in the day MochiBot was really popular, so I guess someone is making some nice money on ad revenue right now.

## Wrapping up

Although MochiMedia has been dead for 3 years, and still seems to be dead, someone is doing a quick money grab, on top of every Flash game that featured their traffic tracking library. But who came up with this clever idea, after a defunct MochiMedia, I don’t know.

Since I was already in the process of releasing a new [RPG Playground](http://rpgplayground.com) version, I deployed the MochiBot-free version as soon as I could. All is good now! RPG Playground continues to be free and *ad-free*.

## Why? Flash games are dead, right?

Well, probably not entirely. You see, the one that is still running that MochiBot library can see how many games and how many views it is still getting. This means that they have an accurate estimation on how much ad revenue they can get. Because they implemented these ads in 2017, 3 years after they stopped, it was most definitely still worth the effort.

## 1 Comment

## Jason · July 10, 2017 at 12:04

Wow that’s shady. Nice post.