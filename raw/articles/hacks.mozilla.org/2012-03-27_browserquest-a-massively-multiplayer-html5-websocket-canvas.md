---
title: BrowserQuest – a massively multiplayer HTML5 (WebSocket + Canvas) game experiment
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/03/browserquest/
author: Paul Rouget
published: '2012-03-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*It’s time for some gaming action with a new HTML5 game demo: BrowserQuest, a massively multiplayer adventure game created by Little Workshop (@glecollinet & @whatthefranck) and Mozilla.*

**Play the game: browserquest.mozilla.org**

![BrowserQuest](https://browserquest.mozilla.org/img/common/promo-title.jpg)


![BrowserQuest](https://browserquest.mozilla.org/img/common/promo-title.jpg)

BrowserQuest is a tribute to classic video-games with a multiplayer twist. You play as a young warrior driven by the thrill of adventure. No princess to save here, just a dangerous world filled with treasures to discover. And it’s all done in glorious HTML5 and JavaScript.

Even better, it’s open-source so be sure to check out the [source code on GitHub](http://github.com/mozilla/BrowserQuest)!

**Watch a screencast:**

### A multiplayer experience

![BrowserQuest screenshot](https://people.mozilla.com/~prouget/bq-assets/screenshot3.jpg)


BrowserQuest can be played by thousands of simultaneous players, distributed across different instances of the in-game world. Click on the population counter at any time to know exactly how many total players are currently online.

Players can see and interact with each other by using an in-game chat system. They can also team up and fight enemies together.

BrowserQuest is a game of exploration: the more dangerous the places you go, the better the rewards.

### Powered by WebSockets

[WebSockets](https://developer.mozilla.org/en/WebSockets) are a new technology enabling bi-directional communication between a browser and a server on the web.

BrowserQuest is a demo of how this technology can be used today to create a real-time multiplayer game in a single webpage. When you start to play, your browser opens up a WebSocket connection to one of several load-balanced game servers. Each server hosts multiple world instances and handles the player synchronization and game logic within all instances. Because the server code is running on [Node.js](http://nodejs.org/), both the server and client codebases share a small portion of the same JavaScript source code.

Server code is [available on Github](https://github.com/mozilla/BrowserQuest/tree/master/server).

![BrowserQuest screenshot](https://people.mozilla.com/~prouget/bq-assets/screenshot2.jpg)


### Built on the Web platform

BrowserQuest makes extensive use of different web technologies, such as:

[HTML5 Canvas](https://developer.mozilla.org/en/HTML/Canvas), which powers the 2D tile-based graphics engine.[Web workers](https://developer.mozilla.org/En/Using_web_workers), allowing to initialize the large world map without slowing down the homepage UI.[localStorage](https://developer.mozilla.org/en/DOM/Storage#localStorage), in which the progress of your character is continually saved.[CSS3 Media Queries](https://developer.mozilla.org/en/CSS/Media_queries), so that the game can resize itself and adapt to many devices.[HTML5 audio](https://developer.mozilla.org/En/HTML/Element/Audio), so you can hear that rat or skeleton die!

### Available everywhere

Since BrowserQuest is written in HTML5/JavaScript, it is available across a lot of different browsers and platforms. The game can be played in Firefox, Chrome and Safari. With WebSockets enabled, it’s also playable in Opera. Moreover, it’s compatible with iOS devices, as well as tablets and phones running Firefox for Android.

![BrowserQuest screenshot](https://people.mozilla.com/~prouget/bq-assets/devices.png)


The mobile versions are more experimental than the desktop experience, which has richer features and performance, but it’s an early glimpse of what kind of games will be coming to the mobile Web in the future. Give it a try with your favorite mobile device!

### Join the adventure

Want to be part of BrowserQuest? Create your own character and venture into the world. Fight enemies by yourself or with friends to get your hands on new equipment and items. You might even stumble upon a couple of surprises along the way…

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 236 comments

David MulderMarch 27th, 2012 at 06:45Daniel TiecherMarch 27th, 2012 at 07:04guillaume.lecollinetMarch 27th, 2012 at 08:36Andrew HamptonMarch 27th, 2012 at 07:15guillaume.lecollinetMarch 27th, 2012 at 08:35Lars-Magnus SkogMarch 27th, 2012 at 07:26TchegitoMarch 27th, 2012 at 08:03sombriksMarch 27th, 2012 at 08:09Nicolas FroidureMarch 27th, 2012 at 08:13mkvMarch 27th, 2012 at 08:18Lukas WoMarch 27th, 2012 at 08:27guillaume.lecollinetMarch 27th, 2012 at 08:35wesMarch 27th, 2012 at 13:32Patrick HughesMarch 27th, 2012 at 08:58sombriksMarch 27th, 2012 at 09:00kubicaMarch 27th, 2012 at 09:09kubicaMarch 27th, 2012 at 09:26ZkartsMarch 27th, 2012 at 09:14guillaume.lecollinetMarch 27th, 2012 at 09:24DaRaFFMarch 27th, 2012 at 09:33KLUTCHMarch 27th, 2012 at 09:38sombriksMarch 27th, 2012 at 10:01exactoMarch 27th, 2012 at 11:06JessMarch 27th, 2012 at 11:22AnonymousMarch 27th, 2012 at 12:08ArcMarch 27th, 2012 at 12:26MithosMarch 27th, 2012 at 12:53SteveMarch 27th, 2012 at 13:02AlexApril 4th, 2012 at 05:23StephenApril 11th, 2012 at 13:00WadeApril 12th, 2012 at 05:43Chad HartmanApril 18th, 2012 at 07:05Robert BurkhallAugust 17th, 2012 at 23:57KlintorisMarch 27th, 2012 at 13:13Martin WellsMarch 27th, 2012 at 13:31Alessandro BahgatMarch 27th, 2012 at 14:12KaraiMarch 27th, 2012 at 14:25Benjamin MeyerMarch 27th, 2012 at 14:35Jakub MinkiewiczMarch 27th, 2012 at 14:48KaraiMarch 27th, 2012 at 15:06EricMarch 27th, 2012 at 15:31COCOMarch 27th, 2012 at 16:12ChoochMarch 27th, 2012 at 16:23Jean-Yves PerrierMarch 27th, 2012 at 16:36Ellie KesselmanMarch 27th, 2012 at 17:54JonMarch 27th, 2012 at 16:46noMarch 27th, 2012 at 16:51AsanarMarch 27th, 2012 at 17:01KenMarch 27th, 2012 at 17:06Lonnie TaylorMarch 27th, 2012 at 19:06RomanMarch 27th, 2012 at 19:12BizwankMarch 27th, 2012 at 20:22TimoteoMarch 27th, 2012 at 20:58JimMarch 27th, 2012 at 22:16ShmerlMarch 27th, 2012 at 22:21JamesMarch 27th, 2012 at 22:50JamesMarch 27th, 2012 at 23:19JamesMarch 27th, 2012 at 23:43JonathanMarch 27th, 2012 at 23:52Steve BarkerMarch 28th, 2012 at 00:04EaxMarch 28th, 2012 at 01:15Pera TudtMarch 28th, 2012 at 01:39EricMarch 28th, 2012 at 02:11MickMarch 28th, 2012 at 02:20UlmoMarch 28th, 2012 at 03:40ArcMarch 28th, 2012 at 11:01UlmoMarch 29th, 2012 at 04:43nemoApril 3rd, 2012 at 08:08UlmoApril 20th, 2012 at 05:03MikeCogluciferMarch 28th, 2012 at 04:09Paulo PontesMarch 29th, 2012 at 04:04RoflCopterMarch 29th, 2012 at 13:51JohanMarch 28th, 2012 at 05:11Paul RougetMarch 29th, 2012 at 06:54JohanMarch 29th, 2012 at 07:57GerardMarch 28th, 2012 at 05:30MarkMarch 28th, 2012 at 05:48SebbMarch 28th, 2012 at 05:57ILoveWebSocketsMarch 28th, 2012 at 06:14AzharMarch 28th, 2012 at 06:14cath-leenMarch 28th, 2012 at 06:17JohnnyMarch 28th, 2012 at 06:28Paul RougetMarch 29th, 2012 at 06:54Marc-AndreMarch 30th, 2012 at 10:09VMarch 28th, 2012 at 07:04FanolianMarch 29th, 2012 at 05:55VMarch 29th, 2012 at 06:32zebarnabeMarch 28th, 2012 at 07:20TchegitoMarch 28th, 2012 at 07:21aMarch 28th, 2012 at 07:41Juegos de MarioMarch 28th, 2012 at 07:42Victor PopescuMarch 28th, 2012 at 08:22YousefMarch 28th, 2012 at 08:40Paul RougetMarch 29th, 2012 at 06:56ZaladinMarch 29th, 2012 at 09:45YousefApril 4th, 2012 at 08:47Carl114March 28th, 2012 at 08:43FrederikMarch 28th, 2012 at 09:28Paul RougetMarch 29th, 2012 at 06:56ZsombroMarch 28th, 2012 at 09:55HoenMarch 28th, 2012 at 10:06DeathdragonMarch 28th, 2012 at 10:37Carl114March 28th, 2012 at 13:43Paul RougetMarch 29th, 2012 at 06:57Carl114March 29th, 2012 at 07:15skylerMarch 28th, 2012 at 10:52GrzeshtoffMarch 28th, 2012 at 12:07eikeMarch 28th, 2012 at 12:11Josh LevitanMarch 28th, 2012 at 12:34samnobMarch 28th, 2012 at 12:38Paul RougetMarch 29th, 2012 at 07:03elickMarch 28th, 2012 at 12:42JonMarch 28th, 2012 at 15:24MikeMarch 28th, 2012 at 19:18kenMarch 28th, 2012 at 16:40JuveMarch 28th, 2012 at 22:43JuveMarch 31st, 2012 at 02:34JoeMarch 29th, 2012 at 00:32VEMarch 29th, 2012 at 01:01LeetMarch 29th, 2012 at 03:10MehMarch 29th, 2012 at 17:17webdesignerMarch 29th, 2012 at 01:39darioMarch 29th, 2012 at 04:39perryMarch 29th, 2012 at 07:19AlexMarch 29th, 2012 at 08:34JamesMarch 29th, 2012 at 09:07jadawinMarch 29th, 2012 at 09:17@bjarneo_March 29th, 2012 at 10:19WadeMarch 29th, 2012 at 11:49DomClaxtonMarch 29th, 2012 at 15:42van_banMarch 29th, 2012 at 11:55Barnabus ProboscisMarch 29th, 2012 at 12:42RamussenMarch 29th, 2012 at 13:56AeldonisMarch 29th, 2012 at 13:57RAMMarch 29th, 2012 at 14:29DomClaxtonMarch 29th, 2012 at 15:38JamesMarch 29th, 2012 at 16:50Paul RougetMarch 29th, 2012 at 17:18MehMarch 29th, 2012 at 17:22JonMarch 29th, 2012 at 18:03TyenMarch 29th, 2012 at 21:39Jon SnowMarch 30th, 2012 at 02:04SteveMarch 30th, 2012 at 02:17GerardMarch 30th, 2012 at 05:44GlennMarch 31st, 2012 at 16:48Julien BrightsideMarch 30th, 2012 at 06:24lucasMarch 30th, 2012 at 06:32BullfrogMay 20th, 2012 at 07:27DaggonMarch 30th, 2012 at 06:52PedroponMarch 30th, 2012 at 10:11ReelixMarch 30th, 2012 at 10:26PeregrineApril 29th, 2012 at 10:35ZargggMarch 30th, 2012 at 16:53James C.March 30th, 2012 at 16:58VApril 2nd, 2012 at 04:16yogeshMarch 30th, 2012 at 18:08FioteMarch 30th, 2012 at 19:33FioteMarch 30th, 2012 at 19:37MarkRHMarch 31st, 2012 at 03:00RedBeardMarch 31st, 2012 at 07:22OzerrenMarch 31st, 2012 at 13:42ZASPERSMarch 31st, 2012 at 14:22g1i1chMarch 31st, 2012 at 14:39JoelMarch 31st, 2012 at 18:01oukourjApril 1st, 2012 at 04:35LordJebeApril 1st, 2012 at 07:53JesseApril 1st, 2012 at 09:46WolfenApril 1st, 2012 at 10:39Benya82April 1st, 2012 at 17:45BravoApril 2nd, 2012 at 14:57Jean-Yves PerrierApril 2nd, 2012 at 16:39BravoApril 6th, 2012 at 10:06Anjo666April 2nd, 2012 at 15:54WadeApril 3rd, 2012 at 06:28KeolsApril 3rd, 2012 at 12:15AlexApril 3rd, 2012 at 18:01BugsBunnyApril 6th, 2012 at 23:53Jean-Yves PerrierApril 7th, 2012 at 14:16DanielApril 17th, 2012 at 11:11ghostshadowApril 7th, 2012 at 00:38NeoroApril 9th, 2012 at 08:47NickApril 9th, 2012 at 15:42Juegos de MarioApril 10th, 2012 at 08:12FredApril 10th, 2012 at 11:49rickApril 10th, 2012 at 20:35WolfenApril 15th, 2012 at 09:34DaVinceApril 16th, 2012 at 04:27paccioneApril 17th, 2012 at 08:14Alex MartiniApril 17th, 2012 at 16:34Joseph PruittApril 22nd, 2012 at 22:14argentum onlineApril 24th, 2012 at 12:32KatuirosApril 27th, 2012 at 15:41Jean-Yves PerrierApril 27th, 2012 at 16:03Victor PopescuApril 30th, 2012 at 23:11tedsMay 1st, 2012 at 16:25OkanMay 3rd, 2012 at 14:01ZeeMay 10th, 2012 at 09:22SlaMay 19th, 2012 at 23:31BullfrogMay 20th, 2012 at 07:33ywlcjlMay 23rd, 2012 at 19:43MikeMay 31st, 2012 at 17:41KyleOctober 5th, 2012 at 21:00SassyFebruary 27th, 2013 at 18:33WernJune 1st, 2012 at 22:04Weerayut TejaJune 5th, 2012 at 07:56Simon SmithJuly 15th, 2012 at 09:28Enda MannnJuly 20th, 2012 at 02:54DDAugust 1st, 2012 at 02:31Mark ManningAugust 5th, 2012 at 12:44Robert BurkhallAugust 17th, 2012 at 23:52abhinavAugust 20th, 2012 at 01:13helloAugust 22nd, 2012 at 04:01helloSeptember 3rd, 2012 at 10:00sonnsDecember 24th, 2012 at 01:17alexSeptember 8th, 2012 at 09:45JennySeptember 18th, 2012 at 05:30Robert WagnerSeptember 24th, 2012 at 11:00Justin CliftSeptember 26th, 2012 at 02:53GoldnikoOctober 7th, 2012 at 20:10helloOctober 11th, 2012 at 05:48Chris NikolajsenNovember 7th, 2012 at 01:10Agent BA-2 “J”November 7th, 2012 at 17:51crizcrossNovember 18th, 2012 at 05:42Juan VazquezDecember 7th, 2012 at 07:52Yossi leviDecember 9th, 2012 at 22:52RandomAdventureDecember 30th, 2012 at 05:56RandomAdventureDecember 30th, 2012 at 06:08CameronJanuary 10th, 2013 at 19:57FrancisJanuary 22nd, 2013 at 13:35Stephanie BergmannFebruary 12th, 2013 at 11:34BrianFebruary 15th, 2013 at 19:23PLayerMarch 4th, 2013 at 12:38Fire crowMarch 6th, 2013 at 09:09Zoe BarrieMarch 27th, 2013 at 10:50vuckoMarch 28th, 2013 at 17:41CraigLiamFordApril 8th, 2013 at 04:47