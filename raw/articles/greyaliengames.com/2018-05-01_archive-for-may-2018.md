---
title: Archive for May, 2018
url: http://greyaliengames.com/blog/2018/05/
published: '2018-05-01'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

Back in 2014, before SteamSpy, I wrote [this article](http://greyaliengames.com/blog/how-to-estimate-how-many-sales-a-steam-game-has-made/) about using Steam’s review count to estimate sales. Then SteamSpy came along and we all used that instead.

However, now that SteamSpy is unable to show the number of owners due to Valve’s privacy policy changes, the good old review count method has become valid again!

I decided it was worth getting an updated “Boxleiter” number (how much you should multiply a game’s review count by in order to estimate units sold). So as per usual I asked a bunch of indies to supply accuate data. This time I got over 50 data points. Read on to discover my conclusions!

**The Headline**

The average from my dataset is 82x and the median is 77x. e.g. if a game has 1000 reviews you can estimate it has sold about 80000 units. *But please keep reading as there are some important things to note.*

I think someone mentioned the Boxleiter number was 50x, but in my blog post from 2014 I came up with 30-100x with 70x being the middle, but that included AAA as well as indie games. This new number is for premium indie games only (no F2P), although I did collect data from small titles and big (complex) ones, and the range in success is huge as well.

**The Range**

There’s also a pretty wide range from 30x to 150x. So if you use the median of 77x, you might have overestimated or underestimated by about 2x. I think it’s still useful though as you can say 1000 reviews could mean 30,000 to 150,000 sales but it’s more likely to be in the middle somewhere.

**Notes**

– This ratio was calculated from looking at Steam sales only (not “retail” sales from Steam keys such as via Humble Bundle) and “All Reviews” from the top of a game’s store page just under the description (this filters out reviews made by people who got the game through a Steam key).

– These results could contain errors although I’ve done my best to check them with the devs when I got strange readings.

– I’ve excluded any games that launched before Steam reviews went live in Nov 2013 even though some of those results are still probably pretty accurate.

– I also excluded two outliers with values of 18 an 226 but they didn’t really alter the average/median anyway.

– You still can’t estimate revenue using this number because you don’t know how many sales are from discounts and how big those discounts were. If a game is newer you can assume it’s been discounted less and get a better figure, say for the 1st month or 1st year.

**Caveat**

As with all my posts, I’m just collecting this data and sharing it and my conclusions for fun. Please don’t base any critical business decisions on it.

**Does Review Score Matter?**

I noted down the current Steam review score for all the titles and you can see the results above. To be honest I can’t see a decent correlation there, maybe a slight one indicated by the trendline. So you could assume that a well-reviewed game will have slightly LESS sales per review, but not many.

**Does Launch Date Matter?**

YES! I bet you are glad you read this far because I bucketed the results into launch year (see chart above) and there does seem to be a decrease in the ratio as time goes on.

If the trendline is somewhat accurate it could mean that newer games do get more reviews and that over time reviews become less frequent, OR it’s a change in players’ reviewing habits on Steam (especially as reviews were a relatively new thing in 2014), OR it’s a change in the types of games being made because I believe genre probably affects the amount of reviews you get the most (more on this below).

Also it’s possible that games get the most reviews per sale in the first month when true fans buy them but I don’t have decent data on that. Though I was pretty sure I saw this happen for Shadowhand and I’ve checked the ratio for a couple of games released in the last 3 days and it is low (average of 38x). So make of that what you will.

**The Headline V2**

OK so now we need to tweak the headline a bit. Basically if I ignore games launched in 2014 the average is more like 71x and the median is 64x. It makes sense to use more recent data anyway. The range is still about 30x to 150x.

So what about 2017? Well the average drops to 63x and the median is 65x. The range is about 30x to 100x but I only have 8 data points, so be careful with that.

**Does Genre Matter?**

I’m pretty sure it does but it’s really hard to attach a label to many indie games and also I’ll end up with too few data points for many of the labels.

But based on what I can see, I think that Roguelikes/sims/strategy have a higher ratio, and adventure/casual/puzzle with story elements have a lower ratio.

This could be because players who feel personally “affected” by a story-based game are more likely to leave a review than someone who was playing a more mechanics-driven game? OR it could be that the player demographics of those games are different and people in those demographics are more or less likely to leave reviews. But it’s just speculation at the moment (and may have to remain that way!)

Anyway, potentially you could use genre to chose which end of the range to edge towards. e.g. for story-based, go lower than the average/median, and for mechanics-driven go higher.

**What else could be a factor?**

Could the quantity of sales affect things? The idea being that later sales are to less hardcore fans who are less likely to leave a review. Well I plotted that (see below), and no it doesn’t seem to be a factor, which is kinda interesting. Though probably I need more data for highly successful games.

What about Median Play time? Well unfortunately I don’t have that data, but perhaps if players play your game for longer they might be more likely to leave a review. But then again, this goes against my theory that story-based games (which are typically shorter) get more reviews per sale than longer mechanics-driven games.

OK so that’s it for now. If you feel like sharing your data (don’t share actual sales numbers in public), just post your sales per review ratio in the comments (see the notes section above for how to accurately get that data).