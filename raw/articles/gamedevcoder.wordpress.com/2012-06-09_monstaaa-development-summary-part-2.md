---
title: Monstaaa! development summary – part 2
url: https://gamedevcoder.wordpress.com/2012/06/09/monstaaa-development-summary-part-2/
published: '2012-06-09'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Note: click [here](https://gamedevcoder.wordpress.com/2012/05/29/monstaaa-development-summary-part-1/) to read part 1 of the Monstaaa! development summary.

It’s been over a week since my iOS game [Monstaaa!](https://gamedevcoder.wordpress.com/2013/03/27/end-of-my-indie-game-devevelopment-adventure/) was released on the AppStore. The game was featured in Apple’s New & Noteworthy on the iPhone (Australia and New Zealand only) and got a lot of great reviews including [8/10 by 148Apps](http://www.148apps.com/reviews/monstaaa-review/), [4.5/5 by iFanzine](http://ifanzine.com/monstaaa-review/) or [4/5 by iReviewT](http://ireviewt.com/index.php/2012/06/04/monstaaa-review/) as well as heaps of mentions on various gaming sites. But even though it’s getting mostly very positive feedback, the sales, except for Australia, have been rather low so far. That is no surprise however. Without stronger featuring by Apple only few iOS games succeed these days. But I’m far from saying this is the only reason why Monstaaa! didn’t sell in millions 🙂

Anyway, the game’s been already played by a couple of thousands people, so I thought I’d share analysis of some of the most interesting game statistics here. What surprised me initially was that majority of the Monstaaa! players pirated the game. But this doesn’t matter too much… they still provide good source of information for me 😀

**Statistics gathering**

The game has built-in statistics gathering system that reports pretty much anything that’s happening in the game – from button presses to achievements being unlocked to level progression details. The data is simply sent via HTTP by the game; when received on the server side it gets inserted into one big SQL table using simple PHP code.

Having all this information I was able to quickly extract some of the most interesting data. I was considering using Flurry or other systems for data collection but decided to go with a custom implementation in the end. What I didn’t like about Flurry were its huge delays between data being collected and data being available; with my system everything is real-time. So far everything works well and until the game gets played by an order of magnitude more players bandwidth and SQL efficiency shouldn’t be my worries.

**Gameplay statistics**

One of the most interesting information for me is how many people get to successfully complete each level (the game currently has got 64 levels). That’s exactly what the chart below shows:

Only 70% of all players completed the first level, 62% completed second level and only 10% completed the 9th level. And just so you know if haven’t played the game – the first and second levels are really easy – you have to really try hard not to complete them and there’s no way you can fail!

So, what are the conclusions here? On one hand this doesn’t look very good because it means most people only play the game for a very short time. But on the other hand we should probably take into account the characteristics of average iOS/Android players – it is very common for them to buy the game, run it once or twice and then stop playing it forever. With massive number of games on the market this is unavoidable. And probably even more so with games being pirated – if you didn’t pay for it, you typically have slightly less interest in playing it.

Also, part of the reason why there’s so many people who only played first few levels is – so I believe – that the game’s been out on the AppStore only for a couple of days. But it still doesn’t mean your game can’t do better. Mine certainly could and part of the reason why it didn’t do well enough is explained in the next chart that shows an average number of attempts while trying to complete each of the levels:

While it looks okay’ish up to level 6th, levels number 7 and 12 clearly seem to be too difficult. With both of these levels you can see spikes which indicate sudden difficulty change with respect to previous level. But there’s more levels that are too difficult or not in the right spot in Monstaaa! – and this certainly is one of the things I’m going to improve on with the next update. Ideally, there should be no spikes at all and the chart should show you bars of the same height throughout all of the levels.

Figuring out which levels are too difficult is in fact really tricky before you actually release the game and collect some statistics from a larger group of users. In any case, having tested the game on a couple of friends it wasn’t obvious that levels 7 and 12 are indeed too difficult. Now I know this for sure!

Monstaaa! is a tilt based game and, while I knew tilt controls can be difficult to master for many, I spent a lot of time trying to make the game easy enough, especially at the start. As it now turns out more work is needed on the difficulty balancing side of game.

**Users statistics**

I’m not going to give you exact number of copies sold just yet as I’m too shy for that but I’m going to show you how many users played the game every hour and also how many new users started playing every hour (which kind of gives you clue as to what the sales might be):

The reason you can easily see “daily” spikes in there is because the game was featured in New & Noteworthy in Australia – spikes simply correspond with days and nights there. The highest number of players during one hour (blue line) was 93 and the highest number of new players (orange line; most likely ones who just purchased, or pirated, the game) over single hour was 64.

Ideally you’d want both number of the users (blue line) and number of new users (orange line) to rise indefinitely with the first one rising faster than the latter – this would mean you get more and more new users while the “old users” would still keep playing your game.

**Device statistics**

Finally here is some insight into what were the most popular devices that had Monstaaa! installed on them:

The iPad’s and iPhone’s shares were almost identical at 45% with remaining 10% going to iPod touches. iPad2 was the most popular among iPads and iPhone4 was the most popular among iPhones with iPhone4S being next most popular. Looking at these stats one should take into account the fact that most of the Monstaaa! users are probably from Australia being – that is my impression – a very “iOS friendly” country.

My final word here is, if you’re releasing any game for any platform make sure you implement at least some basic statistics gathering in there. It takes little time but it will give you a lot of priceless information about how your game is played and how you can improve it.

That’s it for now. Check back soon for more development info about Monstaaa!

UPDATE: Check my [next blog post](https://gamedevcoder.wordpress.com/2012/07/22/monstaaa-development-summary-part-3/) in the series covering Android sales and more.

Any status update about Monstaaa! Maciej?

Thanks for asking. I should have next piece published rather soon!

really interesting stuff, shows how important it is to add analytics. will you be releasing information on daily/weekly sales and marketing spend?

Thanks for posting about your experiences with Marmalade and game development.

How are you determining that users are pirating the app? Did you have a breakdown for Android devices as well?

The piracy rate is not known to me but I know that on iOS there’s been about 5-6 times more game installations than there was purchases. Surely there are people who have even more iOS devices but I don’t think average iOS user has that many.

As for the Android data, take a look my next blog post at:

Thanks for the reply. I did actually read on through the rest of your blog posts after my comment, so saw the statistics you’ve mentioned. It’s really great that you’re happy to share your experiences with the rest of the community. Look forward to seeing if the advert strategy pays more dividends than the in app game purchasing. I downloaded and played the game to level 8 yesterday on Android… I didn’t purchase basically because for me I was happy with the 10 minutes of entertainment it provided for me on the train trip home from work. The incentive for me to want to go through more levels simply wasn’t there.