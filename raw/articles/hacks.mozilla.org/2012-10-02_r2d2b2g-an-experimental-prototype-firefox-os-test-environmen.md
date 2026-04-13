---
title: 'r2d2b2g: an experimental prototype Firefox OS test environment – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2012/10/r2d2b2g-an-experimental-prototype-firefox-os-test-environment/
author: Myk Melez
published: '2012-10-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Developers building apps for [Firefox OS](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS) should be able to test them without having to deploy them to actual devices. I looked into the state of the art recently and found that the existing desktop test environments, like [B2G Desktop](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Using_the_B2G_desktop_client), the [B2G Emulators](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Using_the_B2G_emulators), and Firefox’s [Responsive Design View](https://hacks.mozilla.org/2012/07/debugger-responsive-design-view-and-more-in-firefox-aurora-15/), are either difficult to configure or significantly different from Firefox OS on a phone.

Firefox add-ons provide one of the simplest software installation and update experiences. And B2G Desktop is a lot like a phone. So I decided to experiment with distributing B2G Desktop via an add-on. And the result is [r2d2b2g](http://people.mozilla.com/~myk/r2d2b2g/), an experimental prototype test environment for Firefox OS.

## How It Works

r2d2b2g bundles B2G Desktop with Firefox menu items for accessing that test environment and installing an app into it. With r2d2b2g, starting B2G Desktop is as simple as selecting *Tools > B2G Desktop*:

![B2G Desktop Menu Item](https://people.mozilla.com/~myk/r2d2b2g/b2g-desktop-item.png)


To install an app into B2G Desktop, navigate to it in Firefox, then select *Tools > Install Page as App*:

![Install Page As App Menu Item](https://people.mozilla.com/~myk/r2d2b2g/install-page-as-app-item.png)


r2d2b2g will install the app and start B2G Desktop so you can see the app the way it’ll appear to Firefox OS users:

![B2G Desktop](https://people.mozilla.com/~myk/r2d2b2g/b2g-desktop.png)


## Try It Out!

Note that r2d2b2g is an experiment, not a product! It is neither stable nor complete, and its features may change or be removed over time. Or we might end the project after learning what we can from it. But if you’re the adventurous sort, and you’d like to provide feedback on this investigation into a potential future product direction, then we’d love to hear from you!

Install r2d2b2g via these platform-specific XPIs: [Mac](https://ftp.mozilla.org/pub/mozilla.org/labs/r2d2b2g/r2d2b2g-mac.xpi), [Linux (32-bit)](https://ftp.mozilla.org/pub/mozilla.org/labs/r2d2b2g/r2d2b2g-linux.xpi), or [Windows](https://ftp.mozilla.org/pub/mozilla.org/labs/r2d2b2g/r2d2b2g-windows.xpi) (caveat: the Windows version of B2G Desktop currently crashes on startup due to bug [794662](https://bugzilla.mozilla.org/show_bug.cgi?id=794662) [795484](https://bugzilla.mozilla.org/show_bug.cgi?id=795484)), or [fork it on GitHub](https://github.com/mozilla/r2d2b2g), and let us know what you think!

## About
[
Myk Melez ](http://www.mykzilla.org/)

Myk is a Principal Software Architect and in-house entrepreneur at Mozilla. A Mozillian since 1999, he's contributed to the Web App Developer Initiative, PluotSorbet, Open Web Apps, Firefox OS Simulator, Jetpack, Raindrop, Snowl, Personas, Firefox, Thunderbird, and Bugzilla. He's just a cook. He's all out of bubblegum.

## 71 comments

Stephanie DaughertyOctober 2nd, 2012 at 16:31Robert NymanOctober 3rd, 2012 at 03:57Michael Fitzpatrick RuthOctober 2nd, 2012 at 16:47Robert NymanOctober 3rd, 2012 at 03:58Myk MelezOctober 3rd, 2012 at 10:35AshishOctober 2nd, 2012 at 23:11Olly HodgsonOctober 3rd, 2012 at 03:25PahellebrandOctober 9th, 2012 at 22:13Robert NymanOctober 3rd, 2012 at 03:59Aleks ToticOctober 2nd, 2012 at 23:18Jean ClaveauOctober 3rd, 2012 at 02:07Robert NymanOctober 3rd, 2012 at 04:00Myk MelezOctober 3rd, 2012 at 10:41gvnmcknzOctober 3rd, 2012 at 03:47Robert NymanOctober 3rd, 2012 at 04:02Richard VidlerOctober 3rd, 2012 at 04:56Myk MelezOctober 3rd, 2012 at 10:56GuyOctober 3rd, 2012 at 22:08Robert NymanOctober 3rd, 2012 at 23:50GuyOctober 4th, 2012 at 07:38Myk MelezOctober 4th, 2012 at 09:17MartijnOctober 4th, 2012 at 10:09Myk MelezOctober 4th, 2012 at 12:13Ignacio Agulló SousaOctober 5th, 2012 at 04:44Ignacio Agulló SousaOctober 5th, 2012 at 04:50Myk MelezOctober 5th, 2012 at 15:04Ken SaundersOctober 5th, 2012 at 09:27Myk MelezOctober 5th, 2012 at 09:36geraldoOctober 6th, 2012 at 15:06Robert NymanOctober 9th, 2012 at 23:32Brandon ChengOctober 9th, 2012 at 22:15Robert NymanOctober 9th, 2012 at 23:33GabrielaOctober 10th, 2012 at 06:25Robert NymanOctober 14th, 2012 at 05:14Kelvin SOctober 10th, 2012 at 12:26Robert NymanOctober 14th, 2012 at 05:15Jonathan W.October 10th, 2012 at 18:26Robert NymanOctober 14th, 2012 at 05:14Rodolfo De NadaiOctober 12th, 2012 at 16:37Robert NymanOctober 14th, 2012 at 05:15Jean ClaveauOctober 16th, 2012 at 02:41Myk MelezOctober 18th, 2012 at 16:18Jean ClaveauOctober 19th, 2012 at 04:31Myk MelezOctober 19th, 2012 at 09:18OLLI_SOctober 23rd, 2012 at 12:33AndreOctober 31st, 2012 at 02:17GabrielaOctober 31st, 2012 at 16:18Myk MelezNovember 2nd, 2012 at 13:31GabrielaNovember 2nd, 2012 at 13:48Christos BacharakisNovember 6th, 2012 at 04:17AndreaNovember 6th, 2012 at 04:21Myk MelezNovember 8th, 2012 at 10:18Myk MelezNovember 8th, 2012 at 09:56OLLI_SNovember 8th, 2012 at 13:07Myk MelezNovember 8th, 2012 at 14:38OLLI_SNovember 10th, 2012 at 03:16Myk MelezNovember 15th, 2012 at 12:32OLLINovember 15th, 2012 at 13:47Myk MelezNovember 15th, 2012 at 12:33Ken SaundersNovember 8th, 2012 at 16:38Myk MelezNovember 15th, 2012 at 12:35GabrielaNovember 8th, 2012 at 16:40Myk MelezNovember 15th, 2012 at 12:38GabrielaNovember 15th, 2012 at 13:18Myk MelezNovember 15th, 2012 at 14:21GabrielaNovember 15th, 2012 at 14:31qunowNovember 13th, 2012 at 19:09Myk MelezNovember 15th, 2012 at 12:40Ken SaundersNovember 16th, 2012 at 08:30yanglifu90March 15th, 2013 at 03:13Robert Nyman [Editor]March 15th, 2013 at 03:36