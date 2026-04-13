---
title: Screenshot Saturday 206
url: https://etodd.io/2015/01/09/screenshot-saturday-206/
published: '2015-01-09'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Screenshot Saturday 206

I moved my office into an incubator / art gallery this week.

![](../../assets/bacc4332a4a05083.jpg)


![](../../assets/bacc4332a4a05083.jpg)

The move is mostly for my own sanity. Turns out, working alone in your apartment for 9 months isn't the most fun in the world. It's a Herculean effort just to stay motivated. I also lost all semblance of a disciplined sleep schedule.

Productivity has been great since the move, and I'm back on a normal sleep schedule. Having people around is great, even if I mostly tune them out to focus on work (sorry guys).

In keeping with the production schedule, I finished the last frost level today. Unfortunately its massive size doesn't lend itself too well to screenshots. I tried my best:

![](../../assets/3b231bca502001c7.jpg)


![](../../assets/3b231bca502001c7.jpg)

I also completed the dialogue and cutscene for the first major player decision in the story. Sorry, no screenshots. It isn't much to brag about, but spoilers are spoilers.

Lastly, I updated the visuals for the movement prediction / block creation mechanic. Someone pointed out a while back that the old visuals made it difficult to distinguish overlapping shapes. Here's how it used to look (I always love sneering at old screenshots):

![](../../assets/67222d68266a9755.png)


![](../../assets/67222d68266a9755.png)

And here's the new effect with edge highlights:

![](../../assets/42afc0bcb913c445.jpg)


![](../../assets/42afc0bcb913c445.jpg)

I could have used a texture, but I ended up doing it in the shader based on UV coordinates:

```
const float radius = 0.15f;
float2 diff = float2(min(max(uv.x, radius), 1.0f - radius), min(max(uv.y, radius), 1.0f - radius)) - uv;
float highlight = 0.6f + (5.0f * (diff.x * diff.x + diff.y * diff.y) / radius);
```


I seem to recall reading a way to do it with only arithmetic primitives, but I couldn't remember it or figure it out.

A bunch of other stuff also happened that I won't bother listing.
If you are for some reason interested in nitty gritty details, the [Steam beta tester group](http://steamcommunity.com/groups/lemmabeta) has extensive changelogs.

That's it for this week! Thanks for reading.