---
title: Feedback in Production
url: https://claire-blackshaw.com/blog/2011/04/feedback-in-production/
author: Claire Blackshaw
published: '2011-04-29'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Feedback in Production](../../assets/4e402aebc4c1a4e8.png)

[#AltDevBlogADay](http://altdevblogaday.org/2011/04/28/feedback-in-production/)

As game developers we know the importance of Feedback in our games for players, but so often we forget the importance of feedback for ourselves. Implementing good feedback loops in your production cycle can be just as important.

Two stories highlight this for me. The first is personal, a team for a game I was working on was having the critical bug count communicated to them daily in scrums, and key issues pinned to the wall. The engagement with the lists was low, until one programmer asked for a graph. Since the coloured stack graph went up enjoyment is much higher and conversations happen around the graph (and supporting lists).

Edit: Found Source for this article["You Wouldn't Like Me When I'm Angry" by Nick Waanders](http://www.gamasutra.com/view/feature/4111/dirty_coding_tricks.php?print=1)

In an article I read a programmer spoke about a game they were working on and the artists not paying attention to the frame rate. The number just didn’t matter to them. So he replaced the fps counter with a series of photos of his face: Happy, content, angry. The improvement was immediate, because the information was visual and the granularity reduced for clearer communication.

**General Rule**: For every role in the production cycle question what information is critical or a good performance indicator and try to expose feedback in the most appropriate format and make the feedback loop as short as possible.

Claire :)

Below are just some quick ideas and areas to try hit

## Programmers

**Compile or Pack times**: The length of this feedback loop directly impacts the productivity of your team.**Code Reviews**: Not only for quality of code but is the individual receiving adequate feedback on their work. A mentor system or pair programming system can help here, don’t try dump it all on your leads, they won’t have time. Resulting in a breakdown on the feedback loop.**Feedback on Failure**: Are your error messages consistent throughout the business? Can you implement a dump system, or display a call-stack. In the case of failure are you providing the coder with enough quality information to solve the issue? In larger companies, does the error communicate which area of responsibility the error is occurring in?**Live Analytics**: In the case of your programmers working on live systems do they have access to realtime easy to process visual data on player patterns, which functions are performance heavy or what areas of suffering above average load?

## Artists

**Immediate Preview**: As an artist can I, without support from others, quickly view my assets in-game.**Assets Streaming**: Can an artist update an asset without rebooting the game, removing the need to navigate menus and get to the point of the game where they can see the asset.**Performance Data**: Do I get understandable visual feedback on texel to pixel ratio, overdraw density or other technical data in a fashion that is accessible to me?

## Designers

**Real-time Variables:**Can a designer alter values in game on the fly to see how they feel?**Stats Data:**Can I receive feedback from any play-through of the game done by QA, Focus Testers, or coders in the form of visual reports or recorded numbers?**Live Analytics**: Do they have access to real-time easy to process visual data on player patterns, purchases of items, drop of rates and general user flow?**UI Heatmap**: Can the game generate a heat-map of cursor flow?

## QA

**Build Dates**: Can I quickly visual identify the build number and date?**Bug Feedback**: When a bug is returned to QA am I provided with enough information to reassess the bug and is the communication clear?

## Production Staff

**Work Done**: Does a report quickly identify work done and work remaining at present?**Visible Build**: Can I access a recent working version of the game?**Time Spent**: Can I identify areas of the work which have a higher than expected cost, or large investment in them.**Graphs**: It sounds cliché, but a picture is worth a 1000 words. Live graphs prefably on a web system internally will make you life so much easier.**Team Time:**Is there a frequent structured process for me to receive feedback from the team and provide them with feedback?

## Board, CEO, VP, and other Stake Holders

**Visible Progress**: Am I able to see visible progress in an easy visual format?**Team Issues**: Are HR items (such as sickness), morale, rework to content, areas of uncertainty communicated with progress reports?**Target visibility:**Am I aware of the big goals for the next development target(s) and able to assign a confidence level to delivery?