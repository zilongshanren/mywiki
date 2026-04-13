---
title: 'js13kGames 2020: A lean coding challenge with WebXR and Web Monetization –
  Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2020/08/js13kgames-2020-a-lean-coding-challenge/
author: Andrzej Mazur
published: '2020-08-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Have you heard about the [js13kGames](https://js13kgames.com/) competition? It’s an online [ code-golfing challenge](https://hacks.mozilla.org/2016/08/js13kgames-code-golf-for-game-devs/) for HTML5 game developers. The month-long competition has been happening annually since 2012; it runs from August 13th through September 13th. And the fun part? We set the size limit of the zip package to 13 kilobytes, and that includes all sources—from graphic assets to lines of JavaScript. For the second year in a row you will be able to participate in two special categories:

[WebXR](https://js13kgames.com/webxr)and

[Web Monetization](https://js13kgames.com/webmonetization).

## WebXR entries

The **WebXR category** started in 2017, [introduced as A-Frame](https://hacks.mozilla.org/2017/08/a-frame-comes-to-js13kgames/). We allowed the A-Frame framework to be used outside the 13k size limit. All you had to do was to link to the provided JavaScript library in the `head`

of your `index.html`

file to use it.

```
<!DOCTYPE HTML>
<html>
<head>
<script src="https://js13kgames.com/webxr-src/aframe.js"></script>
// ...
</head>
// ...
```


Then, the following year, 2018, we added [Babylon.js](https://www.babylonjs.com/) to the list of allowed libraries. Last year, we made [Three.js](https://medium.com/js13kgames/webxr-with-three-js-and-three-quests-318fdc331c64) another library option.

Which brings us to 2020. Amazingly, the top prize in this year’s WebXR category is a **Magic Leap** device, thanks to the [Mozilla Mixed Reality](https://mixedreality.mozilla.org/) team.

## Adding Web Monetization

**Web Monetization** is the newest category. Last year, it was [introduced](https://medium.com/js13kgames/web-monetization-new-category-this-year-e87bb1c998cd) right after the [W3C Workshop about Web Games](https://end3r.com/blog/2019/07/w3c-games-workshop-trip-report/). The discussion had identified discoverability and monetization as key challenges facing indie developers. Then, after the 2019 competition ended, some web monetized entries were [showcased at MozFest](https://hacks.mozilla.org/2019/10/from-js13kgames-to-mozfest-arcade-a-game-dev-web-monetization-story/) in London. You could play the games and see how authors were paid in real time.

A few months later, [Enclave Games](https://enclavegames.com/) was [awarded a Grant for the Web](https://enclavegames.com/blog/awarded-grant-for-the-web), which meant the Web Monetization category in js13kGames 2020 would happen again. For a second year, Coil is offering free membership coupon codes to all participants, so anyone who submits an entry or just wants to play can become a paying web-monetized user.

### Implementation details

Enabling the Web Monetization API in your entry is as straightforward as the WebXR implementation. Once again, all you do is add one tag to the `head`

of your `index`

:

```
<!DOCTYPE HTML>
<html>
<head>
<meta name="monetization" content="your_payment_pointer">
// ...
</head>
// ...
```


Voila, your game is web monetized! Now you can work on adding extra features to your own creations based on whether or not the visitor playing your game is *monetized*.

```
function startEventHandler(event){
// user monetized, offer extra content
}
document.monetization.addEventListener('monetizationstart', startEventHandler);
```


The API allows you to detect this, and provide extra features like bonus points, items, secret levels, and much more. You can get creative with monetizable perks.

## Learn from others

Last year, we had [28 entries](https://js13kgames.com/entries/2019/26) in the WebXR category, and [48 entries](https://js13kgames.com/entries/2019/25) in Web Monetization, out of the 245 total. Several submissions were entered into two categories. The best part? All the source code—from all the years, for all the entries—is available in a readable format in the [js13kGames repo on GitHub](https://github.com/js13kGames), so you can see how anything was built.

![js13kGames 2019 posts](../../assets/261c5b905dc2577e.png)


Also, be sure to read [lessons learned blog posts](https://js13kgames.github.io/resources/#posts2019) from previous years. Participants share what went well and what could have been improved. It’s a perfect opportunity to learn from their experiences.

## Take the challenge

Remember: The 13 kilobyte zip size limit may seem daunting, but with the right approach, it could be doable. If you avoid big images and [procedurally generate](https://en.wikipedia.org/wiki/Procedural_generation) as much as possible, you should be fine. Plus, the WebXR libraries allow you to build a scene with components faster than from scratch. And most of those entries didn’t even use up the all the allocated zip file space!

Personally, I’m hoping to see more entries in the WebXR and Web Monetization categories this year. Good luck to all, and don’t forget to have fun!

## About
[
Andrzej Mazur ](https://end3r.com)

HTML5 Game Developer, Enclave Games indie studio founder, js13kGames competition creator, and Gamedev.js Weekly newsletter publisher. Tech Speaker passionate about new, open web technologies, excited about WebXR and Web Monetization.