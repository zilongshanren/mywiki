---
title: Lessons Learned Making and Selling My Third Indiegame
url: https://frgmnts.blog/f/making-selling-indiegame.html
author: Mario Kaiser
published: '2022-09-21'
source_blog: 'FRGMNTS: Bite Size Fiction'
source_site: https://frgmnts.blog
category: game programming
fetched: '2026-04-13'
---

# Lessons Learned Making and Selling My Third Indiegame

![Blacken Slash](../../assets/d11075c23654fd61.png)

Yesterday my third, mostly solo developed indie game Blacken Slash was released on [Steam (opens new window)](https://store.steampowered.com/app/1746560?utm_source=website), [Play Store (opens new window)](https://play.google.com/store/apps/details?id=com.ehmprah.blackenslash) and [App Store (opens new window)](https://apps.apple.com/app/blacken-slash/id1604646442). I worked on it for 12 months and spent ~2500 hours on it. Although Blacken Slash is heavily built on my [previous learnings (opens new window)](https://frgmnts.blog/t/gaming.html), it also served as a testbed for various things which I will try to unpack as far as that's possible this early on.

## Sales

Blacken Slash had the Steam page up since 10/2021 and accumulated 1552 wishlists until the release. Core Defense had more than [twice the wishlists before launch (opens new window)](https://frgmnts.blog/f/core-defense-launch-numbers.html); I think the reason for that is my botched release strategy but more on that below. In the first 24 hours on sale Blacken Slash grossed $1,116:

**Steam**: $488 from 114 copies (78% were wishlist conversions)**App Store**: $565 from 107 copies (39% were pre-orders)**Play Store**: $63 from 14 copies

To be perfectly honest I'm not blown away by the results. But then the strategy for this one was focused on the long tail anyway: Deliver high quality at a low price to gain good reviews to please the allmighty algorithm. And the numbers are good enough for me to stay a full-time indie for a while I guess – and that was the whole point of this exercise.

## Pricing

For my last game Core Defense I opted for a $9.99 price point and frequent and high discounts. I was satisfied with the results but had quite some backlash about the price in the reviews, especially given the fact that it's not exactly a looker.

This time around I wanted to try a new strategy, inspired by the success of SNKRX and Vampire Survivors and similar low-priced titles. Blacken Slash is richer than Core Defense both visually and content-wise, but I'm selling it for $4.99. I did this for three reasons:

- I hate price differences between PC and mobile but felt $4.99 was the ceiling for mobile, so I wanted the PC version to cost just that
- I wanted a low entry barrier so I could hook impulse buyers with my high quality game
- I wanted players to feel they got a good deal, which will be reflected in the reviews

## Mobile

There are two things to unpack regarding the mobile versions. After trying freemium with Core Defense I wanted to try how a premium game with a separate demo would work on mobile. Looking at the early numbers this seems viable.

Coming from a web development background I always wanted to make games which work on both desktop and mobile devices. With just a little more effort you can have the same product reach a bigger audience and market, so why not do it?

Turns out it isn't exactly easy: it took me almost ten years and three games to realize my vision of responsive game development. For Coregrounds mobile versions were planned but cancelled with the game. Core Defense had mobile versions but almost a year after the Steam release. Only with Blacken Slash I finally managed a simship – and I'm happy the mobile sales are more than on par with the Steam sales.

## Godot

Surprise surprise, using a game engine to make games makes a ton of things a lot easier. After making [Coregrounds (opens new window)](https://store.steampowered.com/app/649770/Coregrounds/) and [Core Defense (opens new window)](https://coredefense.ehmprah.com/) with HTML5 and [ultimately being annoyed (opens new window)](https://frgmnts.blog/f/multi-platform-games-javascript.html) I have switched over to Godot for this one – and I haven't looked back. Godot is outstanding open source software which I love and cannot recommend enough – especially if you're developing for mobile as well!

## Quality

You cannot control if a famous streamer picks up your game or if press is going to cover it. What you do control is the quality of your product. Quality is not everything, but without quality, everything is nothing. The Core Defense mobile versions netted me 30k only on reviews and algorithm-assisted word of mouth.

Marketing games in the attention economy is exceedingly hard, so you have to make every sale count. I want a sale to become a multiplier for more sales. To that end I have spent twice as much time as planned on this game, but I'd definitely do that again.

## Hook

I love Diablo – but I can't play games that require so much clicking anymore. I prefer turn-based games nowadays, so I decided to make a mashup of both. "Diablo, but turn-based" isn't the worst hook imaginable, but it sure isn't the best either. And the game's abstract retro theme doesn't exactly scream "Diablo". In the first iteration the game was called "Paint it Black", but I realized too late that name was taken on Steam – but some design choices remained.

Especially the worldbuilding and marketing were unnecessarily hard because of the fact that Blacken Slash has grown organically around the basic gameplay idea. It's hard to describe in one sentence or picture. Things could have been so much easier with a captivating point of view and with a hook that's so strong that a two second GIF is all you need to understand what the game is.

## Worldbuilding

Michael Champion composed the soundtrack for Blacken Slash and penned the narrative. The worldbuilding we did together – but looking back I think we went a bit overboard: while established tropes and names for things may be boring, they sure increase a game's accessibility. There's a sweet spot between fresh and alienating which we haven't quite nailed with this one.

## Localization

I was [ultimately disappointed (opens new window)](https://frgmnts.blog/f/one-year-core-defense-numbers-learnings.html) with the crowdsourced localization strategy for Core Defense. This time around I used friends and paid translators for fewer, but better translations of the game. I'm happy with the results but learned that I could have saved quite a bit of time by amending the strings with some extra context and descriptions for the translators.

## Release Strategy

The Core Defense release strategy was very successful: a closed alpha sparked interest, an Early Access via itch.io built a community (and the game) and then a prologue on Steam brought thousands of wishlists before the launch.

I wanted to replicate that success but unfortunately changed some things for the worse: Because I wanted to take part in the Steam Next Fest, I opted for a demo instead of a prologue. And I released this demo even before the itch.io Early Access. This is what happened:

- I got tons of feedback from the demo already, essentially making the Early Access unnecessary
- The demo performed worse than Core Defense's prologue because it was released with much less polish
- Two months before the release I still sat at 1k wishlists, panicked and did make a prologue after all, which didn't much for the game

Even though I used exactly the same tools, the order made a huge difference. I would still go for a demo first, but probably skip the itch.io EA and use a prologue released in EA on Steam. Furthermore I'd continue sharing early progress on socials, but do the announcement and Steam page at a later point in development. I don't think an early, unpolished version on Steam will hurt your wishlists, but it sure is a lot of work updating it as your game progresses. The amount of time I spent on trailers, screenshots and GIFs for Blacken Slash was **too damn high**.

## Marketing

Core Defense was successful enough for me to make another game – but not successful enough to pay for much marketing. Here's a list of things I did and what I learned:

**Store Page**

Apart from the product itself, the store page is*the*most valuable marketing tool you have. Make sure it's as good as can be. I've spent*weeks*perfecting the copy and assets.**Discord**

With Core Defense I built a cool community on Discord and expected to be able to convert them to Blacken Slash easily. Turns out a Discord server is not a reliable way of reaching your fans: when they're "done" with the game most people will either leave or mute the server. You should definitely have a Discord server, just not as your*only*point of contact with your fans.**Mailing List**

After realizing I had no way of contacting most of my previous fans, I added a newsletter subscription to the end of the demo, incentivised with the promise of a special subscriber item they get upon launch. A very powerful tool which I should have started using*much*earlier!**Steam Next Fest**

The Next Fest was the main reason I opted for a demo instead of a prologue but I've been disappointed. I did two livestreams and only gained around a 100 wishlists during the Next Fest. Instead of the February iteration I should have gone for the June one to showcase a more polished version but I think even then the results would probably have been underwhelming. I think the Next Fest is more valuable the more traction you have before it.**Gameround.co**

I applied for a free spot on[Gameround.co (opens new window)](https://gameround.co/detail/230/info)to get feedback on the game's demo. I got a lot of value out of this and would even recommend paying for it if you have trouble finding people for playtesting.**Web Demo**

I created a browser-based demo of the game and published that to[ArmorGames (opens new window)](https://armorgames.com/blacken-slash-demo-game/19246). Got featured on the front page and got quite a few eyeballs and some useful feedback there.**Twitter**

The social I'm using most successfully with hashtags like #ScreenshotSaturday, #PitchYaGame and #TurnBasedThursday. Also: the game's brilliant sound designer actually[approached me via Twitter (opens new window)](https://twitter.com/ehmprah/status/1429038571147735050), the game's name was[decided on Twitter (opens new window)](https://twitter.com/ehmprah/status/1433032768146051079)and I successfully[recruited content creators for a pre-alpha (opens new window)](https://twitter.com/ehmprah/status/1466789369679908868). Twitter rocks for gamedevs!**Reddit**

I posted about the game on various subreddits to some success. Hard to nail but an invaluable asset in the marketing on a budget arsenal.**9GAG**

Even harder to pull off than Reddit in my opinion, but worth trying nonetheless. The community is brutal, but every little bit helps, right?**IndieDB**

I keep posting about my games there but I have yet to see any meaningful return on investment. Sending traffic to IndieDB to climb the charts is probably how that would work, but I feel wary of directing my hard earned traffic there instead of my store page.**Forums**

I posted about the game on various forums. Most marketing feels like screaming into the void, this one does especially. Won't do this again for my next game.**TikTok**

Everyone's talking about it, but I found it hard to make anything that works on this platform. If you're not actually using a network, it's hard to nail the content. But then which solo indie gamedev has time to be properly active on multiple social networks?**PR Basics**

I write press releases and publish them via[gamespress.com (opens new window)](https://www.gamespress.com/Blacken-Slash#?tab=Press-releases-0). I sent PR beats and keys to my little mailing list of about 300 press and 300 influencer contacts. Not a lot of buck but also not a lot of bang.**Handpicked Creators**

I spent days researching content creators (via the free versions of[Woovit (opens new window)](https://woovit.com/)and[Lurkit](https://frgmnts.blog/lurkit.com)) who are a perfect fit for the game and sent them keys one by one via mail and Twitter. I also tried to get in touch with creators who played my previous games. I'm very surprised that this didn't lead to any substantial coverage, especially as I got[Retromation (opens new window)](https://www.youtube.com/watch?v=cNz7Mc1ekJc)and[Olexa (opens new window)](https://youtu.be/h4lbmour2Lo?t=1651)to cover the alpha demo earlier this year.**Asking for features**

I asked/applied for features on Steam, Play and App Store. It worked for the App Store! They gave me a big feature this time around, without which the sales probably would look at lot worse. Having a 4.7 rating for Core Defense as proof of my ability to deliver high quality (which Apple loves) probably helped getting me selected here.**Bundle**

I reached out to some fellow indies with similar games for a[joint bundle (opens new window)](https://store.steampowered.com/bundle/26946/Tiny_Team_Tactical_RPGs/). Not enough data yet on this but I think[Chris Zukowski is right (opens new window)](https://howtomarketagame.com/2022/05/16/other-indie-developers-are-not-your-competition/)in seeing the potential here!**Box Art**

I hired an artist to create some key art for the game for ~$500. Totally worth it, would definitely do that again.**Professional Trailer**

I hired a professional trailer editor for ~$1000. Would definitely do that again, too. As a designer and engineer my trailers are always just stuffed with features, the one[Gary (opens new window)](https://twitter.com/GaryJKings)made tells a story instead and the difference is huge.**Terminals.io Launch Package**

I got the Launch Package for $2000 for the release. It's still going on so it's hard to assess at this point, but I already got some nice coverage out of it, so I'm optimistic. Unfortunately I didn't have more money to spend, but I'd have liked to see if another $2k in the hands of a popular streamer would have been more bang for my buck but hey, there's always a next game to try that out with.

## What's next?

Blacken Slash was my last solo-developed game. I'm currently working on two games with two of my best friends: Michael Champion and Mathias Tournier have actually been involved in the development of all my games so far – but now we've taken the leap and actually founded a studio together. The three of us will henceforth be making indie games as [Sonderland Games (opens new window)](https://sonderland.games/). Do [subscribe to our mailing list (opens new window)](https://sonderland.games/) for updates on our games and do follow me on [Twitter (opens new window)](https://twitter.com/ehmprah) if you liked this post. Thanks!