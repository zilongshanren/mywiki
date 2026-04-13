---
title: 'Trainspotting: Firefox 37, Developer Edition and More – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2015/04/trainspotting-firefox-37-developer-edition-and-more/
author: Dietrich Ayala Posted; Firefox; Trainspotting
published: '2015-04-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Welcome to *Trainspotting*, a new series on Mozilla Hacks designed to help the busy Web developer keep up with what’s new, what’s changed and what is coming soon in all of the Firefoxes, the Web platform, and the tools for building the Web!

Mozilla develops Gecko and Firefox on a “train model” – we branch the code and ship a release on a time-based schedule (every six weeks). If a feature is not finished, it’s reverted or disabled and has to, as we say, ride the next train. This means we ship new features, performance improvements, and bug fixes to users every six weeks, instead of having to wait up to 18 months.

*Trainspotting* will publish every six weeks when we branch the code – and we’ll point out any changes that might require action or cause compatibility issues, as well as new features that Web developers would want to take advantage of.

## Firefox 37

For a detailed list of all noted changes in the release, check out the [official release notes for Firefox 37]. Below is a list of notable features, links to documentation, and anything that requires action by developers or site operators.

### Desktop Features

- A subset of the Media Source Extensions (MSE) API has been implemented and is enabled to allow native playback of HTML5 video on websites such as YouTube. You can
[read about the various MSE APIs and their usage on MDN](https://developer.mozilla.org/en-US/docs/tag/Media%20Source%20Extensions). - Bing search now uses HTTPS. Hurray for private and secure searching!
- Heartbeat is a new feedback feature in Firefox desktop: Each day a random subset of Firefox users will be shown a notification bar with an opportunity to provide feedback on their experience. You can see screenshots and read more about how it works on the
[Heartbeat project page].

### Firefox for Android

This time around, Firefox for Android is getting a security and stability release. The biggest user-facing changes—improved performance of file downloads, and the addition of some new locales: Albanian, Burmese, Lower Sorbian, Songhai, Upper Sorbian, Uzbek. Read the [full list of security fixes for Firefox Android 37] and the [full release notes](https://www.mozilla.org/en-US/mobile/37.0/releasenotes/).

### HTML5 & Web Platform

There are a bunch of new Web platform features that you can now use in production content in Firefox 37, and here are a few examples:

[IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB)is now available in[Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers).[display:contents](https://developer.mozilla.org/en-US/docs/Web/CSS/display)is now supported in CSS. Read[Sam Rueby’s great post](http://samrueby.com/2015/02/09/firefox-is-releasing-support-for-css-display-contents/)to find out more.

Keep reading the [Firefox 37 for Developers article on MDN](https://developer.mozilla.org/en-US/Firefox/Releases/37) for a detailed look at all the rest.

### Developer Tools

If you’re using Firefox Developer Edition these additions won’t be news, but if you’ve been doing your development in the release build, there are a few new features to note:

- The new
[Security Panel in the Network Monitor](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor#Security)shows security details for a network request, such as which cipher was negotiated for each resource, and much more.[See a screenshot here](https://www.dropbox.com/s/dkcu20bwx5mvp3a/Screenshot%202015-03-27%2013.51.37.png?dl=0).Previously, we only showed the site info dialog, with information for the top-level load, which is sometimes misleading. The new UI also shows if connections were protected by HTTP strict-transport-security or key pinning. Read more about[the Security Panel](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor#Security)on MDN. - The new
[Animations panel in the Page Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Work_with_animations#Firefox_37)displays information about your animations and gives you a play/pause button for them. Read the[Firefox DevTools Animations Guide](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Work_with_animations)and[watch the video](https://youtu.be/0teX91eQEVo). - WebIDE can now run a custom build step before pushing your apps to a device, in case you want to minify your code or integrate with your Web app build tool of choice. The
[WebIDE docs on MDN](https://developer.mozilla.org/en-US/docs/Tools/WebIDE/Running_and_debugging_apps#Running_a_custom_build_step)explain how to use this feature.

### Security

Firefox 37 has a bunch of security changes. Most of these do not require any action, however if you are a site operator you should definitely look to see if any of these changes impact you. Big thanks to [David Keeler](https://twitter.com/mozkeeler), security engineer for Firefox, for his help deciphering this section of the release notes.

- We removed support for DSA in certificates and TLS, because we found that almost nobody was using these. If you’re a site operator and your certificate
*was*signed with a DSA algorithm, contact your CA and get a new certificate. You can check with `openssl x509 -in {certificate file} -text -noout` and search for “Signature Algorithm.” If you do have one of these certificates and do not change it, users will see an override-able error. [HTTP/2 AltSvc is temporarily disabled due to a bug](https://www.mozilla.org/en-US/security/advisories/mfsa2015-44/).~~We implemented HTTP/2 AltSvc support for opportunistic encryption. This feature allows encryption over TLS for unauthenticated connections that would otherwise be clear text. Configuration is very simple, and Patrick McManus has written~~[instructions for how to set it up on your server](http://bitsup.blogspot.com/2015/03/opportunistic-encryption-for-firefox.html).- We have disabled insecure TLS version fallback. If a secure site isn’t working, you can try setting the “security.tls.version.fallback-limit” preference in about:config to 1 and see if it works then. If you see this anywhere,
[please file a Tech Evangelism bug](https://bugzilla.mozilla.org/enter_bug.cgi?product=Tech%20Evangelism&component=Desktop), noting the URL of the site, so we can work with the operators to update it. Site operators should make sure their servers aren’t TLS-intolerant, which you can do with the[SSL Labs tool](https://www.ssllabs.com/ssltest/analyze.html). - Users can now report SSL connection problems for a variety of non-certificate-related errors. For example, if a user encounters a non-override-able TLS error, they can now send a report to Mozilla directly from the error page. The information in the report consists of the domain you were trying to reach, the certificates the server sent, the time, which error was encountered, and some user agent information. We use this information to work with site operators to fix their configurations, and to improve our software that detects these issues, so please do send reports. Check out a
[screenshot of what this looks like](https://www.dropbox.com/s/d8seg2kwtpewv0w/Screenshot%202015-03-27%2013.26.18.png?dl=0). - TLS False Start optimization now requires a cipher suite using AEAD construction. If you’re running a server and false start isn’t working as expected, try using an AEAD cipher suite. Learn more about
[AEAD at Wikipedia](http://en.wikipedia.org/wiki/Authenticated_encryption)and in[RFC 5288](http://tools.ietf.org/html/rfc5288#section-3). The only AEAD cipher suite that Firefox supports at this time is AES-GCM. - We now log usage of weak ciphers to the web console. For example, if you visit a site with a SHA-1 certificate with the web console open you’ll now see a message like, “This site makes use of a SHA-1 Certificate; it’s recommended you use certificates with signature algorithms that use hash functions stronger than SHA-1. Learn more…” If you run a site and your certificate was signed with SHA-1, get a new certificate from your CA.

## Firefox Beta

In six short weeks Beta will be available for general release, becoming Firefox 38. Here’s some of what’s coming your way:

- All Firefox preferences are now in a new tab-based UI.
- Improved page-load times with speculative connection warmup.
- MSE support on Mac OS X.
- EME support for encrypted media playback.
- Web platform features: WebSockets in Web Workers, KeyboardEvent.code, and the BroadcastChannel API.

Read the [Firefox 38 Beta release notes](https://www.mozilla.org/en-US/firefox/38.0beta/releasenotes/) for the full list.

## Firefox Developer Edition

This release of Firefox Developer edition (which will be Firefox 39) is frankly kind of ridiculous. The developer tools are getting precariously close to something indistinguishable from magic. Huge props to the developer tools team for what you’re about to see.

**Developer Tools:**[Wi-Fi debugging of Firefox OS devices from WebIDE](http://convolv.es/blog/2015/03/25/wifi-debug-fxos/), drag and drop of nodes in the Inspector’s markup view, Web Console input history persistence, localhost works with WebSocket connections when you’re offline, and the cubic bezier tooltip now shows a gallery of pre-sets you can choose from to make your CSS animations super slick.**Web platform features**include the “switch” role in Aria 1.1, CSS scroll snap points, Cache API, Fetch API, <link rel=”preconnect”> and more.

Read the [full release notes for this release of Firefox Developer Edition.](https://www.mozilla.org/en-US/firefox/39.0a2/auroranotes/)

## Nightly

The [nightly branch of Firefox](http://nightly.mozilla.org/) is where a lot of features are in active development. It’s a place where you can test experimental Web APIs and see user-facing browser features that are not yet ready for hundreds of millions of users. You might see a crash or two, you might lose you session data, but you also might experience the vision and wonder of what the future holds. It’s the Mos Eisley of browsers – a dangerous place, but we stick around for the action.

There are a number of features that have landed and are shipping nightly builds either enabled by default or by pref:

- E10s – Web content runs in a separate process from the browser UI.
- Partial implementation of Service Workers.
- Shumway – Flash implemented in JavaScript is enabled for some sites.

Thus concludes the first edition of *Trainspotting*. Let us know what you think in the comments, and what you’d like to see more of!

## 5 comments

trancheApril 8th, 2015 at 02:27ChristianApril 8th, 2015 at 07:34dietrich@mozilla.comApril 8th, 2015 at 10:35PingApril 13th, 2015 at 18:20dietrich@mozilla.comApril 13th, 2015 at 19:51