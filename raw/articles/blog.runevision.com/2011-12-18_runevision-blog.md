---
title: runevision blog
url: https://blog.runevision.com/2011_12_18_archive.html
published: '2011-12-18'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

For the past - hmm, almost 2 months now - I've taken a break from my other hobbies and let myself become distracted by Google's [AI Challenge](http://aichallenge.org) - an Artificial Intelligence (AI) programming contest.

Not for much longer though since the final submission deadline is in 10 hours at the time of writing.

When I [wrote about it a months ago](http://blog.runevision.com/2011/11/ant-colony-google-ai-challenge.html) I'd only been at it for a few weeks but [my bot](http://aichallenge.org/profile.php?user=9661) was already ranked 39th in the world out of 10000+.

Since then I've made a lot of improvements - but so have the other contestants, so the overall level has continuously risen.

Whenever a new version of a bot is uploaded to the content servers, the skill and rank is completely reset, so the bot will have to fight its way all the way back up from the bottom. That can take a few days to a week depending on how high a ranking it can get before it's stabilized.

I last uploaded a bot four days ago. It has gotten up to rank 22 in the world; my highest ranking yet. It's also the top ranked bot in Denmark by a large margin and the 3rd ranked bot written in C#.

When working on improving the bot, it's usually hard to know if some new idea will actually improve the bot or just make it worse without having tested it first. I usually test by running a game with the new version against the old version. However, most changes only make a small difference that will only slightly increase the bot's chances of winning, so it has to be in many games before it's clear if it's better or not. Did it win 4 out of 6 games? Might just be a coincidence due to random luck.

You can see it quickly becomes tiresome to test these things manually. That's why I programmed a simple framework to automatically run many games in a row between the various version of the bot and gather statistics on which versions win the most times. I've often let this run overnight so I have statistics from hundreds of games the next day.

Sometimes, however - sometimes an idea turns out to be a significant improvement. By significant I mean that the new version consistently beat the previous version - as in 10 out of 10 times. Those times when I've managed to make such an improvement have been the most satisfying moments of this competition.

The most interesting improvements have all been related to how the ants handle combat. The way [battle resolution](http://aichallenge.org/specification.php#Battle-Resolution) works in the game follows simple rules but has complex consequences and my understanding of it has increased in stages.

The combat is basically about ants being in majority winning over ants that are in minority. If one red ant is within combat range of one white ant, they both die. But if one red ant is within combat range of two white ants, only the red ant die and both of the white ants survive.

Initially I thought combat was a matter of being cautious. Only move into combat range if you have more ants you can move within range than the opponent has. But it's not that simple. There's various potential outcomes to consider and also an element of gamble. I might write some more about it after the competition has ended if not somebody higher ranking does it first. Not that I'm an expert by any count - I feel like I've only scratched the surface.

Anyway, since I uploaded that last bot four days ago I've made several significant improvements in the combat skillz of my bot, meaning that the newest version I have here totally and consistently kicks the ass of that version I uploaded four days ago. Now I've just uploaded this new version. It will probably be the last unless I get some last-minute epiphany which is not likely by now.

We'll see how it performs in the final tournament.