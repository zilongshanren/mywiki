---
title: Building A Paid App For Firefox OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/02/building-a-paid-app-for-firefox-os/
author: Kumar
published: '2013-02-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

At first glance the [Firefox Marketplace](https://marketplace.firefox.com/) for [Firefox OS](http://www.mozilla.org/en-US/firefoxos/) may look similar to the Apple Store or Google Play Store but there is a key difference: it does not lock you into Mozilla or lock you into your Firefox OS phone. **It enables you to sell a web app that will run on any open web device by way of the receipt protocol**. Non-Mozilla

[marketplaces](https://developer.mozilla.org/en-US/docs/Apps/Creating_a_store)can participate in selling apps on Firefox OS out of the box by implementing the receipt format and users won’t notice anything different when running a paid app from either store.

When other devices support the [receipt](https://wiki.mozilla.org/Apps/WebApplicationReceipt) protocol then theoretically you could pay for an app **once** and **run it everywhere**. There is, of course, a chicken vs. egg problem here so Mozilla hopes to be the egg that helps prove out the decentralized receipt concept and iterate on the protocol. Mozilla invites other vendors to help us work on getting receipts right so that paid apps are as portable and “webby” as possible.

## For Developers

It’s the responsibility of each paid app to [validate its own receipt](https://developer.mozilla.org/en-US/docs/Apps/Publishing/Validating_a_receipt). If you’re a developer thinking about selling your app on Firefox OS, this post should give you a head start on implementing the receipt validation bits. This post may also be interesting for those who wish to build a compliant web runtime or a compliant marketplace.

The [navigator.mozApps](https://developer.mozilla.org/en-US/docs/DOM/Apps) JavaScript API exposes device receipts to your application. The simplest way to validate a receipt is to include a client side library like [receiptverifier.js](https://github.com/mozilla/receiptverifier) and use the hosted verification service URL found in the receipt. The receiptverifer docs go into detail but it’s as easy as calling this JavaScript code when your app starts up:

```
mozmarket.receipts.Prompter({
storeURL: "https://marketplace.firefox.com/app/your-app",
supportHTML: '
```[email you@yourapp.com](mailto:you@yourapp.com)',
verify: true
});

That’s it! This is a high-level shortcut that also displays a prompt on the screen within your app if the receipt is missing or invalid. The docs for the verifier show how to do low-level validation.

For a more complete example, you can check out the code to the [Private Yacht](https://github.com/kumar303/yacht/) app which we’ve been using in testing. This app shows you how to do client side checking with the [receiptverifier.js](https://github.com/mozilla/receiptverifier) library as well as server side checking via Node.js. We also have a [Python library](https://github.com/andymckay/receipts) (and one specifically for [Django](https://github.com/andymckay/django-receipts/)) that you can use on a server to check receipts.

How does it work? Each receipt is a mash up of [JSON Web Tokens](http://openid.net/specs/draft-jones-json-web-token-07.html). One of the properties is a link to a hosted verification service that you can use to check the receipt. You also have the option of verifying receipts offline but this requires periodic key synchronization and some details like refund and reissue handling are not well supported yet for offline validation.

By default, a receipt is only allowed to originate from one of the store URLs in the **installs_allowed_from** parameter in your app’s [manifest](https://developer.mozilla.org/en-US/docs/Apps/Manifest). As a developer you’ll create explicit payout relationships with each marketplace and will thus want to limit who can claim to sell your app. This acts as a whitelist for who can provide receipts for your app. Due to the loose nature of client side JavaScript, you can get tighter control over this whitelist by validating receipts server side (that is, on your own app server).

Paid apps for Firefox Marketplace aren’t fully live yet but they’re coming very soon. If you integrate a receipt checker into your app now, you’ll be ready when the submission flow supports payments.

## Fraud Protection

Enabling any party on the web to sell apps is crucial to Mozilla’s vision of open web apps. However, making receipts decentralized while fully protecting app assets (without DRM) is challenging. There are currently attacks users can use in their clients, like a DNS proxy, to access paid apps but there is mitigation to this with [CSP](http://www.w3.org/Security/wiki/Content_Security_Policy), [CORS](http://en.wikipedia.org/wiki/Cross-origin_resource_sharing), and [HSTS](http://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security), just to name a few. The state of today’s paid iOS / Android apps is actually [not much different](http://www.macworld.com/article/1167677/hacker_exploits_ios_flaw_for_free_in_app_purchases.html#lsrc.twt_lexfri). There is an open issue right now that will help [make marketplace whitelists more effective](https://bugzilla.mozilla.org/show_bug.cgi?id=770666) and Mozilla expects to evolve the system further as more developers and more stores participate. Switching to a signed, [packaged app](https://developer.mozilla.org/en-US/docs/Apps/Packaged_apps) may also offer another layer of asset protection but this was designed more to address permission issues.

As always, if you run into issues please file bugs! If it’s an Apps platform bug select [Core](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core) (component: DOM: Apps) or select [Marketplace](https://bugzilla.mozilla.org/enter_bug.cgi?product=Marketplace) (component: Payments/Refunds).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 23 comments

SteveFebruary 27th, 2013 at 09:24Kumar McMillanFebruary 27th, 2013 at 13:02erlehmannFebruary 27th, 2013 at 10:09Robert Nyman [Editor]February 27th, 2013 at 12:52Kumar McMillanFebruary 27th, 2013 at 13:03Andy McKayApril 4th, 2013 at 10:22Nikhil SomaruFebruary 27th, 2013 at 11:12Robert Nyman [Editor]February 27th, 2013 at 12:53JeffreyFebruary 27th, 2013 at 13:06Kumar McMillanFebruary 28th, 2013 at 08:42ZenCODEMarch 17th, 2013 at 02:02pnathanFebruary 27th, 2013 at 14:16Robert Nyman [Editor]February 27th, 2013 at 17:25KostadinovFebruary 28th, 2013 at 12:42Robert Nyman [Editor]March 1st, 2013 at 07:56KostadinovMarch 1st, 2013 at 13:25Kumar McMillanMarch 1st, 2013 at 13:29KorniMarch 12th, 2013 at 07:47Kumar McMillanMarch 13th, 2013 at 07:28WebResourcerMarch 2nd, 2013 at 09:50Rogger ShawMarch 4th, 2013 at 03:14Fred LinMarch 5th, 2013 at 07:32Kumar McMillanMarch 5th, 2013 at 08:54