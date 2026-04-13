---
title: About the author & this blog
url: https://gametorrahod.com/about-5argon/
author: Sirawat Pitaksarit
published: '2019-03-01'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/551c6b99a0e9937f.png)

Hi! I often goes by the name **5argon **and I am usually found always creating something with a computer.** **Everything else is in my homepage : [http://5argon.info](https://5argon.info)

This blog's full name อยากทำเกมต้องทรหดอดทน is a Thai language meaning roughly "painful game dev life". It is now a self hosted Ghost ([http://ghost.io](http://ghost.io)) which I just migrated from Medium. Markdown and inline code handling are miles better!! Not to mention you can do syntax highlight code, or just add some arbitrary HTML, like tables. Something inferior are just that I can't click the image to zoom, and there is no button to go to edit mode from blog page for the author.

The migration was going to be very painful that I hesitated to let go of Medium at first. But I decided to bite the bullet after Unity's ECS big apocalypse where it would deprecates 80% of my written articles anyways. I thought if they are left as is, it will be dangerous for Googler that stumbles upon them and waste time reading unusable/stupid code. Now it is a good opportunity to burn all the junks along with the Medium blog. I threw away most of them, "API update" some of them (about 3-4 ECS articles remains from total 20+), and decided to start a new blog onwards.

Initially I was writing only in Thai, but lately the article gets more "useful" (mainly Unity ECS stuff that I thought others might want to know, it is still the early day of ECS and the internet is still missing knowledge) that I think maybe it is better to leave something useful on the net with English article.

Ghost's commenting system is still in development so for now I turned to Disqus. Also if you want to ask something, I have a Discord channel originally setup for Asset Store stuff I made. But there is also the `#Chat`

channel where anything goes.. maybe you could go over there if you have questions or something! : [https://discord.gg/WsmAP2](https://discord.gg/WsmAP24)

Subscription/member system is also nonexistence on Ghost. However you could use that old school RSS feed. Just add `/rss`

to the end of homepage URL. It works for tag page too, for example if you would like to receive only Unity ECS related RSS you would use this : [https://gametorrahod.com/tag/unity-ecs/rss](https://gametorrahod.com/tag/unity-ecs/rss)

### How to support the author

I have received several messages from readers that wanted to support me, which I am really grateful. As you can see this blog has no ads nor paywall. And self-hosted Ghost do bite into my savings.

Instead you could get some of my [Unity Asset Store works](https://gametorrahod.com/unity-stuff/#asset-store-works), maybe someday they might become useful for you. I have also opened Patreon [https://www.patreon.com/5argon](https://www.patreon.com/5argon) and lastly, my PayPal.me link is also available : [https://paypal.me/5argon](https://www.paypal.me/5argon). Thank you.

### How to link to a specific sub-topic

Sometimes you may want to share a link that jumps to some header. Apparently Ghost generates `id`

for each topic. I wonder if there are easier way but what I did is to enter debug inspector (With `Ctrl+Shift+C`

, `F12`

, etc.) and highlight the topic to see the `id`

. Then you could append to the end of post's URL next to the `#`

like this : [https://gametorrahod.com/world-system-groups-update-order-and-the-player-loop#scriptbehaviourupdateorder-updateplayerloop-world-](https://gametorrahod.com/world-system-groups-update-order-and-the-player-loop#scriptbehaviourupdateorder-updateplayerloop-world-)

![](../../assets/57db18ecfa938830.png)

## Changelog

The blog itself has its own [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)... heh

### [1.1.0] - 2019-05-31

I have go learned something at [https://practicaltypography.com/](https://practicaltypography.com/) and had overridden Ghost's default casper theme.

- Words per line is lower. Line height is smaller.
- Main font is now
[Gentium Book Basic](https://fonts.google.com/specimen/Gentium+Book+Basic)because I didn't like how fat and curved Georgia was. - Header font is now
[Maitree](https://fonts.google.com/specimen/Maitree)because I want to try serif header. (And promotes Thai font crafters!) - Monospace code font is now
[Fira Mono](https://fonts.google.com/specimen/Fira+Mono). - The main font was too faded and I discovered it was actually dark cool grey instead of black. I changed it to neutral almost-black.
- Removed annoying transition animations.
- Changed colors to brown-red.

### [1.0.0] - 2019-03-28

I almost forgot when I migrated from Medium, but I guess I will use [the time of this post](https://forum.unity.com/threads/i-have-started-an-ecs-blog.652123/).