---
title: Monetization with Inneractive on Firefox OS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/10/monetization-with-inneractive-on-firefox-os/
author: Louis Stowasser
published: '2013-10-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Monetization is important for any viable platform so developers can benefit from their hard work and to further encourage quality apps. Mozilla teamed up with the ad network, [Inneractive](http://inner-active.com), to create a simple library for integrating ads into apps and games specifically for Firefox OS.

This article will go through the process of integrating Inneractive ads in your Firefox OS app.

## Getting Started

- Download the library from the
[Github page](https://github.com/mozilla/inneractive), specifically`inneractive.js`

. - Include the
`inneractive.js`

script in your HTML (or through any other script loader): - Create an account at
[Inneractive](https://console.inner-active.com/iamp/iamp/publisher/register). Once your account is approved you can access the console and create an App.This will generate a unique ‘App ID’ and can be found at the bottom of the Dashboard.


```
```

## Creating the Ad

Your app should have access to the global `Inneractive`

object. Create an ad with the function `createAd`

.

`var myAd = Inneractive.createAd(options)`

`options`

is an object where you customize the ad. The available options

are:

**APP_ID**– This can be found in the previous section when creating an App through the Inneractive Console.**TYPE**– Can be one of three types of ads:`Banner`

: Small ad that is usually constant at the bottom of the screen.`Rectangle`

: Medium sized ad that is usually centered in the middle of

the screen.`Interstitial`

: Fullscreen ad to display usually during levels or

screens.

**REFRESH_RATE**– Time in seconds between rotating ads. Minimum is 15 seconds, default is 30.

### Example

```
var options = {
TYPE: "Banner",
REFRESH_RATE: 18,
APP_ID: "Test_App_ID"
};
var myAd = Inneractive.createAd(options);
```

## Placing the Ad

Once the ad has been created with your options, you need to place it on the screen.

The function `addTo`

will place the ad into the DOM tree under a parent node. You can usually just use `document.body`

for this:

```
myAd.addTo(document.body);
```

This will place the ad under the `<body>`

element of your webpage.

Then you need to position the ad with the function `placement`

. This function takes two arguments, vertical position and horizontal position where the options are `top`

, `bottom`

, `center`

and `left`

, `right`

, `center`

.

For a banner ad to sit at the bottom of the screen you would do the following:

```
myAd.placement("bottom", "center");
```

A rectangle that is exactly in the center of the screen:

```
myAd.placement("center", "center");
```

## Removing the Ad

If you need to remove the ad from the screen for whatever reason, use the function `remove`

.

```
myAd.remove();
```

Once the ad is removed you cannot bring it back and will need to create a new ad with `Inneractive.createAd()`

.

If you have any issues or need support using the library you can file issues on the [Github Issue Tracker](https://github.com/mozilla/inneractive/issues).

## More Monetization options

With Firefox OS you may use any of your favorite ad networks that would work in a browser such as Google Adsense using their integration code.

You also have the option of integrating [In-app payments](https://developer.mozilla.org/en-US/Apps/Publishing/In-app_payments) for selling digital goods through your app or game.

## About
[
Louis Stowasser ](http://louisstowasser.com)

I am a Partner Engineer for Mozilla, maintainer of [Gamedev Weekly](http://gamedevweekly.com) and creator of the [CraftyJS](http://craftyjs.com) game engine, based in Brisbane Australia.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 15 comments

LukeOctober 31st, 2013 at 19:55Jason WeathersbyNovember 1st, 2013 at 09:20MykePNovember 2nd, 2013 at 03:47Hillel FuldNovember 4th, 2013 at 22:58William ForrestNovember 4th, 2013 at 23:05Louis StowasserNovember 6th, 2013 at 15:25HuNovember 6th, 2013 at 05:56Louis StowasserNovember 6th, 2013 at 15:23HuNovember 10th, 2013 at 07:19Kedar LasaneNovember 18th, 2013 at 21:38Louis StowasserNovember 18th, 2013 at 22:42The Tech DigitNovember 26th, 2013 at 17:37LukeNovember 18th, 2013 at 23:27Daniel ZorroNovember 23rd, 2013 at 17:20HaoweNovember 26th, 2013 at 08:48