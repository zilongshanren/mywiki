---
title: Making Multi-Platform Games With Javascript – The Good, the Bad & The Ugly
url: https://frgmnts.blog/f/multi-platform-games-javascript.html
author: Mario Kaiser
published: '2022-09-21'
source_blog: 'FRGMNTS: Bite Size Fiction'
source_site: https://frgmnts.blog
category: game programming
fetched: '2026-04-13'
---

# Making Multi-Platform Games With Javascript –

The Good, the Bad & The Ugly

In my [last blog post](https://frgmnts.blog/f/how-make-successful-indie-game.html) about my game [Core Defense (opens new window)](https://coredefense.ehmprah.com/) I raved about how I love JavaScript for making cross-platform games and that I would soon make a boilerplate out of the game's setup. Over half a year later I am sad to announce that I won't be doing such a thing. In lieu, I will explain in this post why I won't. Please keep in mind that this is very opinionated and should be taken with a grain of salt.

## The Stack: What's it made of?

- Custom built ECS engine
- WebGL rendering via
[Pixi.js (opens new window)](https://github.com/pixijs/pixijs) - Embedded in a
[Vue.js (opens new window)](https://github.com/vuejs/vue)application - Tests via
[Cypress (opens new window)](https://github.com/cypress-io/cypress) - Win, Mac, Linux via
[Electron (opens new window)](https://github.com/electron/electron)&[Vue CLI Plugin Electron Builder (opens new window)](https://github.com/nklayman/vue-cli-plugin-electron-builder) - Steam SDK integration via
[Greenworks (opens new window)](https://github.com/greenheartgames/greenworks) - iOS and Android app via
[Capacitor (opens new window)](https://github.com/ionic-team/capacitor) - IAP via
[Cordova Purchase Plugin (opens new window)](https://github.com/j3k0/cordova-plugin-purchase) [Ionic Appflow (opens new window)](https://ionic.io/appflow)for iOS and Android builds- Analytics via
[Firebase (opens new window)](https://firebase.google.com/docs/analytics) - Highscore backend via
[Firebase Cloud Functions (opens new window)](https://firebase.google.com/products/functions) - Shell scripts for release automation

## The Good: One Codebase to Rule Them All

Don't get me wrong: I absolutely love JavaScript and would love to continue making games with it. I love my setup for Core Defense and the fact that I have one repository and one codebase which powers everything from Windows, Mac and Linux to iOS and Android.

## The Good: A Plethora of Plugins

The JavaScript ecosystem is awesome, there's a plugin for everything and then some. Because you don't have to reinvent the wheel all the time, your time to market can be extremely short, which is especially useful in the day and age of early access where games are released early on and are continously developed.

## The Good: Responsive Design

Thanks to CSS it's startlingly easy to deliver a game with a responsive design which works on 4k displays just as well as on an old iPhone. You have to design your game accordingly from the start, but the actual implementation is remarkably easy.

## The Bad: Console Support

According to my research, getting an HTML5 game to consoles is possible but so much work (see [this video (opens new window)](https://www.youtube.com/watch?v=KfBzlzvt8RU) about the CrossCode console port) that in most cases it's easier to just rewrite the game in Unity or Godot. This essentially is the deal breaker for me: I want to be able to publish my games to consoles. Mobile gaming is where the money is, but especially as an indie it's much easier to get a slice of the pie on PC and consoles than it is on mobile and not being able to somewhat comfortably do that is the main reason I'm making my next game with Godot.

## The Bad: Native addons and SDKs

But even for the platforms we can reasonably target with JavaScript: As soon as you leave the comfort of your dev environment and try to package your web application for sale on Steam, the Play Store or the App Store, things start getting complicated.

You will need to somehow interface native SDKs for achievements, purchases and whatnot and you're either at the mercy of plugin developers delivering high quality work – or you're faced with doing that work yourself, improving said plugins or even rolling out your own, thus fiddling with platform specific native code which you wanted to avoid by choosing JavaScript, right?

## The Bad: Dependency Hell

The amount of unnecessary fiddling with platform-specific quirks and the countless ugly workarounds I had to find to make it all work together is mindboggling. The current state of my game is a fragile balance between versions of third-party code I can't reasonably change without everything falling apart. Every single time I update one plugin something else breaks and I'm leaving the goldilocks zone of compatibility.

## The Bad: Performance

The performance is a double-edged sword: I was impressed with the performance I finally squeezed out of my game, especially on mobile. But it took quite a bit of optimization to get there, which is true for all games but much less so for games made in engines like Unity or Godot – but we'll see about that, come back in a year for another post and possibly another changed opinion.

## The Ugly: Firebase Analytics vs Electron

And from here on out it gets ugly: I have spent way too much time these past few months working around limitations imposed by third-party tools and software. Because I wanted cross-platform analytics for my game and had opted for mobile ads via Google Admob and utilized Firestore and Cloud Functions for my highscore backend, I naturally chose to go with Firebase Analytics, which basically is Google Analytics v4.

Unfortunately, the http endpoint dubbed "Measurement Protocol" for v4 is not available yet, which forces you to use the SDK wrapper, which in turn does not play nice at all with Electron. The SDK only works in a web environment with the HTTP protocol, while Electron uses the file protocol or variations of it. You can imagine the ugly workaround I had to write to overcome this limitation – essentially switching protocols at runtime to trick the SDK into thinking it's used in a regular browser.

## The Ugly: Mobile Ads

And while we're speaking of ads: I wanted to use rewarded ads for the mobile versions to allow for some easy extra cash flow through some little bonuses here and there – but boy oh boy was I mistaken. In the end I have spent weeks on a feature which I have since removed completely, replacing all rewarded ad placements with a consumable currency.

Apart from the fact that the implementation was not trivial at all, there are just so many things that can break. So many cryptic config files to get right. And when you finally get it all working ad serving limits are placed on your accounts left and right. I have had tens of thousands of ad requests and only a couple of hundreds of impressions to show for. Oh and did I mention it is borderline impossible to reach the Admob support?

Of course you could argue that there are much better services than Admob, that my implementation was flawed or that proper ad monetization needs a lot of work. But that's exactly the kind of work I wanted to avoid in the first place by using JavaScript. I don't want to implement dozens of different native ad SDKs. I want to install a plugin, configure it and make money with rewarded ads. The current state of the ecosystem does not cater to this need.

## The Ugly: Appflow vs Electron

My monorepo for Core Defense was a thing of beauty for a long time. Enter Appflow, a cloud build service for packaging mobile apps made with Capacitor. I love and still use that service – but it had trouble building for iOS with the Electron packages in my repository, leading to signing issues unless all references to Electron were removed. Ultimately I had to resort to creating a separate sub-package for the mobile versions, symlinking the source folder of the main package. I cringe every time I look at that repo since.

## All in All: Room for Improvement

All jaded rants aside: I've built a successful game with a programming language I love and I've been massively aided by open source software and cool proprietary tools. But looking back at the overall experience and the missed opportunities I'm going to try new things going forward – as I mentioned before my [next game (opens new window)](https://thousandlives.ehmprah.com/) will be made with Godot. I'm not expecting this to be the silver bullet, but at this point I'm really keen on trying a framework that was actually made for games instead of endlessly trying to use a wrench as a hammer. If you liked this post, consider bookmarking this blog and coming back in the future, or following me on [Twitter (opens new window)](https://twitter.com/ehmprah) for updates. Oh and do ping me there if you've got different experiences or opinions, I'd love to hear your story as well!