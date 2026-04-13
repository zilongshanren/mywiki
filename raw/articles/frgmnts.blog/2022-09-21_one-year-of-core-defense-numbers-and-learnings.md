---
title: One year of Core Defense – numbers and learnings
url: https://frgmnts.blog/f/one-year-core-defense-numbers-learnings.html
author: Mario Kaiser
published: '2022-09-21'
source_blog: 'FRGMNTS: Bite Size Fiction'
source_site: https://frgmnts.blog
category: game programming
fetched: '2026-04-13'
---

# One year of Core Defense – numbers and learnings

It has been exactly one year since [Core Defense (opens new window)](https://coredefense.ehmprah.com/) was released on Steam and in this post I'll share with you both the hard numbers as well as the lessons I learned along the way. If you haven't read it already, I can also recommend my [previous post with lessons learned](https://frgmnts.blog/f/how-make-successful-indie-game.html).

Before we get to it, I'll give you a quick recap of the game's history so far, especially of the things I did after the release on Steam:

- Core Defense was available as first access on itch.io six months prior to the release, where it sold 106 units and grossed $1,144
- It was fully released on Steam on July 31, 2020 at a $9.99 price point, had 3632 wishlists before the launch, sold 2,546 units and grossed $20,186 in the first week on Steam
- I've since built 25 patches (3 of which were big content updates)
- Released the Mastery Expansion DLC on Steam on March 19, 2021 at a $4.99 price point
- Released the iOS & Android versions of the game on April 21, 2021 with a freemium business model, unlocking the full game at a $4.99 price point, the expansion for $2.99 and a bundle for both priced at $6.99

## Grand total

Across all platforms Core Defense has grossed **$72,916** in the past year. I will break down this grand total per platform below.

## Steam Breakdown

- gross revenue:
**$67,404** - reviews:
**81% positive of 236 reviews** - copies sold:
**7,872** - median time played:
**3h 53m** - wishlist conversion rate:
**23.9%** - outstanding wishes:
**6,896** - DLC attach rate:
**17.7%** - return rate:
**9.4%**

Since I've [previously written](https://frgmnts.blog/f/how-make-successful-indie-game.html) about why the game sells on Steam, I will let the numbers speak for themselves here – but I wanted to share a few words about the DLC: The Mastery Expansion adds a permanent progression to the game with skill points to spend on various bonuses and a few other things, but doesn't really add new content but horizontally scales what's already there.

I wanted to add that anyway but saw that as an opportunity to make an extra buck, especially as I opted for a "high" price paired with regular sales strategy. I thought that a DLC would increase my earnings as people buy the game on sale but because they might be buying the bundle, the DLC compensates for the sale – and this works surprisingly well: At least 50% of the more recent sales have been bundle sales.

But even though I expected some backlash from players, especially due to the relatively aggressive $4.99 price point, I was surprised by just how mad this made some players. My reviews plunged from 86% to 81% within days of the DLC release and suddenly the recent review score showed "Very Negative" in deep red at the top of the store page. The baseline daily purchases dropped from 3-5 to zero, the still "Very Positive" score below notwithstanding. In the end I just had to wait a few weeks before those recent reviews vanished in the crowd but heck those were a few scary weeks.

## Windows vs Mac and Linux

As an avid Linux user, I always wonder why so few developers publish their games for operating systems other than Windows. Looking at the sales of Core Defense, it makes a little more sense: Mac and Linux account for only 8.5% of sales. In my case, packaging the game for these OS was virtually no extra effort, so it made sense – but if it's additional work, it may very well be not worth the effort.

## Localization

I think that localizing Core Defense was an important part of the game's success: about 50% of sales on Steam come from non-English speaking countries. But I'm really unhappy with the state and the quality of the translations. The [enthusiasm I previously shared](https://frgmnts.blog/f/how-make-successful-indie-game.html) has subsided over the past year for various reasons:

- the quality of the crowdsourced translations is mostly sub-par
- while there was a lot of momentum around the launch it quickly faded after a while, leaving me with half-finished translations as I introduced new content
- I made quite a few mistakes in organizing the strings, leading to an unnecessary amount to translate, further reducing motivation for the translators
- I didn't funnel translators through the Discord server to be able to reach them

While the localizations helped me sell the game, they don't keep the promise they made in the game itself. I would surely have sold fewer copies of the game without them, but enough to make a professional translation worth it – I don't know. One of the two games I'm currently working on ([Thousand Lives (opens new window)](https://thousandlives.ehmprah.com/)) will be a narrative game that probably won't be localized and I can't wait to see (and share) the numbers in that case.

## Mobile ads and marketing

Before I break down the numbers for iOS and Android, I feel the need to explain: I have only recently begun marketing for the mobile versions because my monetization strategy involved rewarded ads via AdMob, which did not work at all as I expected, leading me to postpone marketing again and again.

I wanted the ads to work before I start the marketing – but in the end I was so frustrated with the whole shebang I discarded them and replaced them with a consumable currency, which players can now buy and spend instead of watching a rewarded ad.

Since the game made with JavaScript and relies on Capacitor for the mobile versions, AdMob was pretty much my only option because I didn't want to write other native plugins the ecosystem didn't offer. I had heard this network might not be the best choice, but that turned out to be quite the overstatement. The implementation was easy enough, but as soon as the game was released, the troubles started:

- ad serving limits were placed on the account left and right, leading thousands of ad requests into the void
- ads on iOS were not working until two weeks after I "connected" the App Store listing to the AdMob account and it took almost two months after the release (!) for the listing to even appear in the AdMob interface to connect
- to this day I have not been able to reach AdMob support because the contact form displays generic errors

I am aware that these may have been problems with this particular network or even a faulty implementation on my end – but this whole ordeal felt so incredibly frustrating and inefficient that I'm pretty sure I won't use ads for monetizing my games again. Quite honestly that's fine because I hate ads anyway, I just wish I'd have been spared the trouble.

## Rating prompt

Coming from the world of steampowered games I underestimated the power of the rating prompt on mobile, postponing it until I was unsatisfied with the amount and the average rating. I was surprised to see how quickly both went up as soon as I placed a native rating prompt after winning a run in one of the recent updates – which in turn seems to please the Play and App Store's algorithms. Downloads and sales are clearly trending upwards since, but this is yet another reason why the mobile versions had a bit of a slow start and the numbers are not conclusive yet.

## iOS Breakdown

- gross revenue:
**$4,154** - rating:
**4.5 across 105 ratings** - downloads:
**16,6k**

Despite the lack of marketing, the iOS version has been doing surprisingly well – which does feel kind of right when taking into account how arduous a process it was to get the game past the App Store review team. I spent two weeks of my life trying to debug and fix an issue which ultimately was clearly on Apple's side of things: because in app purchases are separately reviewed there, sometimes IAP connected to a rejected version of the app can get stuck in an erroneous state where they cannot be purchased anymore, after which every review attempt will be rejected because the IAP don't work. In the end I contacted an Apple employee whose email address I found on various forum threads about that issue; after I poked around the void for two weeks, he solved the problem within a few hours.

## Android Breakdown

- gross revenue:
**$1,358** - rating:
**4.0 across 80 ratings** - downloads:
**4.4k**

The numbers for Android aren't great – but then it's just not been enough time I think. Given that I didn't have to jump through any extra hoops for the Android version that feels fine though. We'll see where this is going in the next year!

## What's next

I always envisioned Core Defense to be playable across all platforms – not just PC and mobile, but also on various consoles. Unfortunately I chose the wrong tech stack to reasonably make this vision a reality.

Coming from a web development background I wanted to use JavaScript and optimistically assumed that it would be possible to package Core Defense for consoles as well. I did the actual research too late and only recently found out that while this is actually possible, [it's incredibly hard](https://frgmnts.blog/f/multi-platform-games-javascript.html). I've since decided to not port Core Defense to consoles and focus on my next games for now – this time using Godot to make sure I won't run into the same roadblocks again.

Apart from the aforementioned [Thousand Lives (opens new window)](https://thousandlives.ehmprah.com/) I'm working on the spiritual successor of Core Defense, which is still unannounced but will follow the same successful recipe: a simple, high quality game which features an unusual combination of genres and sucks players in with a quick and dopamine-rushing core loop. If you're interested in this or any other stuff I make, be sure to follow me on [Twitter (opens new window)](https://twitter.com/ehmprah) for updates. Thank you for reading this, I hope my experiences prove useful to you!