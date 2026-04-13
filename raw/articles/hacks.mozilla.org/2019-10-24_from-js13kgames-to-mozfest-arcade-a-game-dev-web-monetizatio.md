---
title: 'From js13kGames to MozFest Arcade: A game dev Web Monetization story – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2019/10/from-js13kgames-to-mozfest-arcade-a-game-dev-web-monetization-story/
author: Andrzej Mazur
published: '2019-10-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is a short story of how [js13kGames](https://js13kgames.com/), an online “code golf” competition for web game developers, tried out **Web Monetization** this year. And ended up at the [Mozilla Festival](https://www.mozillafestival.org/), happening this week in London, where we’re showcasing some of our winning entries.

## A brief history of js13kGames

The [js13kGames](https://js13kgames.com/) online competition for HTML5 game developers is constantly evolving. We started in 2012, and we run every year from August 13th to September 13th. In 2017, we added a new [A-Frame category](https://hacks.mozilla.org/2017/08/a-frame-comes-to-js13kgames/).

You still had to build web games that would fit within the 13 kilobytes zipped package as before, but the new category added the [A-Frame](https://aframe.io/) framework “for free”, so it wasn’t counted towards the size limit. The new category [resulted](https://hacks.mozilla.org/2018/01/lessons-learned-from-the-a-frame-category-in-the-js13kgames-competition/) in some really cool entries.

Fast forward twelve months to 2018 – the category changed its name to [WebXR](https://js13kgames.com/webxr). We added [Babylon.js](https://www.babylonjs.com/) as a second option. In 2019, the VR category was extended again, with [Three.js](https://threejs.org/) as the third library of choice. Thanks to the [Mozilla Mixed Reality](https://mixedreality.mozilla.org/) team we were able to give away three Oculus Quest devices to the winning entries.

## The evolution of judging mechanics

The process for judging js13kGames entries has also evolved. At the beginning, about 60 games were submitted each year. Judges could play all the games to judge them fairly. In recent years, we’ve received nearly 250 entries. It’s really hard to play all of them, especially since judges tend to be busy people. And then, how can you be sure you scored fairly?

That’s why we introduced a [new voting system](https://medium.com/js13kgames/new-voting-system-judging-and-selecting-winners-1fcf27dfda5e). The role of judges changed: they became experts focused on giving constructive feedback, rather than scoring. Expert feedback is valued highly by participants, as one of the most important benefits in the competition.

At the same time, Community Awards became the official results. We upgraded the voting system with the new mechanism of “1 on 1 battles.” By comparing two games at once, you can focus and judge them fairly, and then move on to vote on another pair.

Voters compared the games based on consistent criteria: gameplay, graphics, theme, etc. This made “Community” votes valuable to developers as a feedback mechanism also. Developers could learn what their game was good at, and where they could improve. Many voting participants also wrote in constructive feedback, similar to what the experts provided. This feedback was accurate and eventually valuable for future improvements.

## Web Monetization in the world of indie games

This year we introduced the [Web Monetization category](https://js13kgames.com/webmonetization) in partnership with [Coil](https://coil.com/). The challenge to developers was to integrate [Web Monetization API](https://webmonetization.org/) concepts within their js13kGames entries. Out of 245 games submitted overall, [48 entries](https://js13kgames.com/entries/2019/25) (including WebXR ones) had implemented the Web Monetization API. It wasn’t that difficult.

Basically, you add a special monetization meta tag to `index.html`

:

```
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Flood Escape</title>
<strong><meta name="monetization" content="your_payment_pointer"></strong>
// ...
</head>
```


And then you need to add code to detect if a visitor is a paid subscriber (to Coil or any other similar service available in the future):

```
if(document.monetization && document.monetization.state === 'started') {
// do something
}
```


You can do this detection via an event too:

```
function startEventHandler(event){
// do something
}
document.monetization.addEventListener('monetizationstart', startEventHandler);
```


If the monetization event starts, that means the visitor has been identified as a paying subscriber. Then they can receive extra or special content: be it more coins, better weapons, shorter cooldown, extra level, or any other perk for the player.

It’s that simple to implement web monetization! No more bloated, ever changing SDKs to place advertisements into the games. No more waiting months for reports to see if spending time on this was even worth it.

The Web Monetization API gives game developers and content creators a way to monetize their creative work, without compromising their values or the user experience. As developers, we don’t have to depend on annoying in-game ads that interrupt the player. We can get rid of tracking scripts invading player privacy. That’s why [Enclave Games](https://enclavegames.com/) creations never have any ads. Instead, we’ve implemented the Web Monetization API. We now offer extra content and bonuses to subscribers.

## See you at MozFest

This all leads to London for the 2019 [Mozilla Festival](https://www.mozillafestival.org/). Working with [Grant for the Web](https://www.grantfortheweb.org/), we’ve prepared something special: [MozFest Arcade](https://arcade.enclavegames.com/).

If you’re attending Mozfest, check out our special booth with game stations, gamepads, virtual reality headsets, and more. You will be able to play Enclave Games creations and js13kGames entries that are *web-monetized*! You can see for yourself how it all works under the hood.

[Grant for the Web](https://www.grantfortheweb.org/) is a $100M fund to boost open, fair, and inclusive standards and innovation in web monetization. It is funded and led by [Coil](https://coil.com/), working in collaboration with founding collaborators [Mozilla](https://foundation.mozilla.org/en/) and [Creative Commons](https://creativecommons.org/). (Additional collaborators may be added in the future.) A program team, led by [Loup Design & Innovation](https://loup.design/), manages the day-to-day operations of the program.

It aims to distribute grants to web creators who would like to try web monetization as their business model, to earn revenue, and offer real competition to intrusive advertising, paywalls, and closed marketplaces.

If you’re in London, please join us at the Friday’s Science Fair at [MozFest House](https://www.mozillafestival.org/en/house/). You can learn more about Web Monetization, Grant for the Web, while playing cool games. Also, you can get a free Coil subscription in the process. Join us through the weekend at the **Indie Games Arcade** at [Ravensbourne University](https://www.mozillafestival.org/en/schedule/)!

## About
[
Andrzej Mazur ](https://end3r.com)

HTML5 Game Developer, Enclave Games indie studio founder, js13kGames competition creator, and Gamedev.js Weekly newsletter publisher. Tech Speaker passionate about new, open web technologies, excited about WebXR and Web Monetization.

## One comment

FelipeNovember 12th, 2019 at 04:36