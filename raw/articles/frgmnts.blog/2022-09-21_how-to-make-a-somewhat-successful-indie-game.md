---
title: How to Make a Somewhat Successful Indie Game
url: https://frgmnts.blog/f/how-make-successful-indie-game.html
author: Mario Kaiser
published: '2022-09-21'
source_blog: 'FRGMNTS: Bite Size Fiction'
source_site: https://frgmnts.blog
category: game programming
fetched: '2026-04-13'
---

# How to Make a Somewhat Successful Indie Game

![Core Defense](../../assets/1a4daa457789e3b2.png)

A few months ago I released [Core Defense (opens new window)](https://store.steampowered.com/app/1203360/Core_Defense/) on Steam and grossed $20,186 in the first week. Nothing crazy, but good enough for a solo indie developer – especially if you take into account that you can expect to make 2-5x your first week's revenue during your first year, [according to (opens new window)](https://www.gamasutra.com/blogs/SimonCarless/20200615/364798/Steam_the_new_wishlists_to_first_week_sales_expectations.php) Simon Carless, whose [newsletter (opens new window)](https://gamediscoverability.substack.com/) I cannot recommend enough.

Currently I am at around 2.5x of the first week's revenue and I haven't done a single sale on Steam yet, which will profit from more than twice the amount of wishlists I had at launch. And then the game's coming to Android and iOS soon, so all in all I would call Core Defense a somewhat successful indie game so far.

In this post mortem (which contains much of my [AMA on r/gamedev (opens new window)](https://www.reddit.com/r/gamedev/comments/i1oi1o/im_a_solo_indie_dev_my_new_game_just_make_3k_in/)) I will share my lessons learned and give you my take on why Core Defense became a modest success.

Naturally this post will contain lots of dos – but if you're also interested in the don'ts, check out the [post mortem (opens new window)](https://frgmnts.blog/f/how-not-to-make-a-game.html) about my first failed game Coregrounds.

## Simplicity

Being a minimalist at heart, I like simple things. But that didn't keep me from making my last game a complexity monster.

This time around I made a game that's simple but highly replayable and strategically diverse – and I think its simplicity is one of the reasons for Core Defense's success. It has no tutorial and does not need one. Its simple, dopamine-rushing core loop: get rewards, update your build, survive the next wave, repeat.

Embracing simplicity allows you to easily communicate what your game is about and why people should care, which helps selling your game. Players can dive right in and get to the fun faster (oh yeah your game needs that, too) – meaning less churn, more positive reviews and ultimately even more sales.

Oh and did I mention that simple games are not only faster to build and easier to maintain, but also much more fun and rewarding to work on?

## Quality

My first game was hemorrhaging players from the start. And it was not just the game's complexity I've mentioned above: apart from a terrible user experience the game had bugs and technical issues aplenty – all of which were completely avoidable.

When talking about selling games and things, we always talk about how to reach more – but personally I think it's the wrong way to go about it. We have huge markets to tap into anyway and I think we should worry more about loosing people than about reaching more. By releasing a game on Steam, we get our games in front of thousands of people no matter what – so we should make sure we loose as few of those as we can.

Quality is not everything, but without quality everything is nothing. With Core Defense I have tried to put quality first and to remove as much friction as possible. From the game design and user interface to the Steam capsule image everything was designed to be as crystal clear and appealing and as much fun to use as possible. Among the many positive reviews several called it "one of the best tower defense games" on the market.123456

## Community-driven development

For Core Defense I chose a community-driven development approach. After finishing the concept I whipped up an alpha version within two months and created a Discord server to get people to play it. I kickstarted the server by alerting my last game's community (from which Core Defense is spin-off after all) and gaming outlets like [AlphaBetaGamer (opens new window)](https://www.alphabetagamer.com/core-defense-alpha-download/).

Since then the Discord server has been constantly growing and has been an invaluable ressource for the game's development. Much of the content in the game today is based on player's ideas and feedback. Countless bugs and issues were reported and the community is an endless source of both motivation and inspiration.

One reason this was working so well though: I was actively engaged with the community, reading absolutely everything they posted and commenting on most of it. The same is true for the Steam community discussions, where there's virtually no post without feedback from me. So while that's a considerable amount of work, not a minute of it is spent in vain.

## Polished Store Page

Your store page is everything: you can have the best game of all time but if no one's going to make it past the store page, no one will ever know. All in all I spent at least an entire week on creating and finetuning the Steam store page; and there's not even that much content on it, the description fits above the fold. In the past couple of months, the game has sold almost as many copies as it gained wishlists, which I think is an indicator for a strong store page and proper pricing.

Mostly because of the minimalist graphics which obfuscate the production value I opted for a $9.99 price point. I have heard all kinds of feedback on this, mostly that the price is fair or could have been higher. But my feeling is that the price was perfect and one of the reasons it sells so well.

## Release Strategy

You might not know that you get a visibility boost in the first month after a release on Steam. After learning this the hard way with my last game I knew that this time I wanted to make the most out of that boost by releasing a polished product on Steam and convert as much of that traffic as possible.

After reading about Martin Nerurkar's [launch strategy (opens new window)](https://www.gamasutra.com/blogs/MartinNerurkar/20180410/316400/Early_Access_without_Steam.php) for Nowhere Prophet, which had an Early Access phase via itch.io before being released on Steam as a finished game, I knew that was perfect.

After the short public alpha I had released the beta version of Core Defense on itch.io in mid-January 2020, six months before the release on Steam. I think it was very important to have had the Steam store page ready for the itch.io release – I even included a Steam wishlist widget on the itch.io store page and announced free Steam keys for all owners of the game.

In the end Core Defense only sold about 150 copies there, but that was more than enough to keep the community-driven development going and to arrive at the level of polish necessary to nail the Steam release.

## Localization

More than half of the game's sales come from non-english speaking countries – which might not entirely be attributed to the fact that the game is localized in almost a dozen languages, but I'm pretty sure it helped.

I crowdsourced the localization via [localizor.com (opens new window)](https://www.localizor.com/core-defense), which was still in beta at the time. It was good then already and just keeps getting better and better.

All I had to do is add a call to action on the game's home screen and thanks to the community I was able to add another translation to the game every other update. The store pages I had successively translated via [translated.com (opens new window)](https://translated.com/). What I could have done better here: funneling the translators through the Discord server would have helped as I have no way of reaching most of them for updates.

## Standalone Demo

When I stumbled upon Mike Rose's [thread about pre-launch demos on Steam (opens new window)](https://twitter.com/RaveofRavendale/status/1228269323195748352) I quickly decided to give this a try and created a standalone pre-launch demo on Steam. It turned out a complete success: the demo netted me about 3000 wishlists for the game, among many other benefits which I have outlined in a [separate blog post (opens new window)](https://frgmnts.blog/f/why-you-need-a-separate-prelaunch-demo-on-steam.html). In terms of time and money spent on marketing, the demo was by far the most effective thing I did.

My next game definitely will have a demo as well, the only question is whether it will be a standalone one. An onpage demo is less work and costs nothing, but the standalone demo will benefit from Steam's visibility boost, which means a lot more eyeballs on your game for just $100 you have to pay for the extra app credit. An onpage demo lets you take part in the Steam Festival as well, which is nice – but you also have to do a livestream to actually get extra visibility out of it (which I didn't unfortunately).

## Marketing

Apart from the demo, influencer outreach was by far the most effective marketing tool for Core Defense:

- I used dodistribute and Keymailer for key distribution
- I did an Indieboost campaign for the beta launch on itch.io and spent about $200 on sponsored influencer videos with good results
- Before the Steam launch, I used Woovit to send out keys to influencers, got featured by a few smaller ones but no big reach here
- I did a Keymailer ad for $100 two weeks before the launch which netted about 80 key requests and a few videos, again not much reach here though
- Around the Steam release I finally wrote cold call emails to a bunch of bigger influencers who seemed like a perfect genre match, one of which actually
[covered the game (opens new window)](https://youtu.be/-D_7ISiKeI8)!

Aside from influencer outreach I did the following things:

- posted regularly on Twitter (#screenshotsaturday!)
- posted about the game on various related subreddits
- wrote press releases, posted them to
[gamespress.com (opens new window)](https://www.gamespress.com/)and sent them to my (puny self-collected) press list - did a few key giveaways on various platforms
- posted about the game on IndieDB and various indie game forums
- shared data and knowledge on my blog and platforms like reddit

## JavaScript FTW

One feels a bit like an outsider using JavaScript to make games in the day and age where Unity seems to dominate the indie space — but I just love the language and the ecosystem. And it easily allows me to make a cross-platform game with one codebase at no license costs whatsoever.

Although the game engine is custom, I rely heavily on Vue.js and Pixi.js, Electron, Capacitor and a few little helper plugins for the Steam integration or mobile ads for example.

In fact I like the setup so much that I plan to make a boilerplate out of it in the future — including my beautiful release script which runs tests and builds and uploads the game to all platforms.

## Ok thanks bye

Thanks for reading – I hope you liked this post! If you did, consider bookmarking this blog and coming back in the future, or following me on [Twitter (opens new window)](https://twitter.com/ehmprah) for updates.