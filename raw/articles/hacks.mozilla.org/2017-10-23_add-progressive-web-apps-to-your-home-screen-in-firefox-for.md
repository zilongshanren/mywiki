---
title: Add Progressive Web Apps to your Home screen in Firefox for Android – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/10/progressive-web-apps-firefox-android/
author: Andreas Bovens
published: '2017-10-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Update 2018-01-22:** This article was updated at the time of the stable Firefox 58 release to reflect minor UI changes as well as documentation updates.*

In 2010, the concept of “responsive web design” (RWD) started resonating in web development circles. Over time, it became a recommended best practice, which was strengthened by the emergence of a number of RWD-enhancing web technologies, such as responsive images, `@supports`

, flexbox, grid, and [so much more](https://developer.mozilla.org/en-US/docs/Glossary/Responsive_web_design). Today, practically all websites are built with RWD principles at their core: truly a dramatic improvement over yesteryear’s desktop-focused web.

Over the last two years, a similar and complementary evolution has been happening: [Progressive Web Apps](https://developer.mozilla.org/en-US/Apps/Progressive) (PWA), an umbrella term for a new set of standardized browser technologies that combine the low-friction nature of the web with the reliability and capabilities we typically associate with native apps, are gaining ground, with more and more top online services [sharing their success stories](https://www.pwastats.com/), and with browser support increasing.

While the Chrome team has been spearheading the PWA effort, other browsers have been landing supporting implementations, and Mozilla has been heavily involved as well: [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) and [Push](https://developer.mozilla.org/en-US/docs/Web/API/Push_API), two of the technologies powering PWAs shipped last year in Firefox 44, and Mozillian Marcos Caceres has been heading up the [Web App Manifest](https://w3c.github.io/manifest/) spec work.

### “Add to Home screen” comes to Firefox 58 for Android

So, continuing our commitment to making PWAs a top experience on mobile, we’re pleased to announce that Firefox 58 for Android ships with Web App Manifest support, in the form of [“Add to Home screen” functionality](https://developer.mozilla.org/en-US/Apps/Progressive/Add_to_home_screen).

When a Firefox 58 user arrives on a website that is served over HTTPS and has a valid manifest, a subtle **badge** will appear in the address bar: when tapped, an “Add to Home screen” confirmation dialog will slide in, through which the web app can be added to the Android home screen. When launched from there, the web app will be shown in the configured view mode and orientation, and it will appear as a separate entry in the app switcher. Note that at present, `beforeinstallprompt`

is not supported, but it might yet be added in a future release: we’re investigating how to proceed.

### New menu option to add page shortcuts

It’s also worth pointing out that there is now also a new “Add Page Shortcut” option in the Page section of the three-dot overflow menu, which allows users to place a simple shortcut to any URL on their home screen — super handy when you want to keep a quick link to a bus schedule, sports section, or other specific page right at your fingertips. When the shortcut icon is tapped, the web page in question is opened in the full browser UI, just like a bookmark.

### External links open in Custom Tabs

Another neat feature is how external links are handled: when a user is browsing an installed progressive web app and taps an external link, the page in question is opened in a Custom Tab. This keeps the user secure as the URL and safety information are visible, speeds up page load time (a Custom Tab loads faster than the full browser), preserves the progressive web app’s color branding, and is in line with native app behavior.

### What’s next?

In upcoming releases, we plan to add more support for other PWA-related APIs: our Background Sync implementation is well underway (currently targeting Firefox 59), and we’re quite excited about the [Payment Request](https://www.w3.org/TR/payment-request/) and [Web Share](https://wicg.github.io/web-share/) APIs as well.

So, try out the “Add to Home screen” implementation in [Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox). Stay tuned for more goodies to come in future releases!

### Documentation

[Progressive Web Apps docs on MDN](https://developer.mozilla.org/en-US/Apps/Progressive)[“Add to Home screen” docs on MDN](https://developer.mozilla.org/en-US/Apps/Progressive/Add_to_home_screen)[Simple “Add to Home screen” example on GitHub](https://github.com/mdn/pwa-examples)

## 6 comments

DeyanOctober 23rd, 2017 at 12:35Andreas BovensNovember 6th, 2017 at 07:37Saijin_NaibOctober 26th, 2017 at 09:30Andreas BovensNovember 6th, 2017 at 07:39LeonNovember 1st, 2017 at 11:14Andreas BovensNovember 6th, 2017 at 07:40