---
title: Introducing navigator.mozPay() For Web Payments – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/04/introducing-navigator-mozpay-for-web-payments/
author: Kumar
published: '2013-04-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

What’s wrong with payments on the web? Any website can already host a shopping cart and take credit card payments or something similar. The freedom of today’s web supports many business models. **Here’s what’s wrong**:

- Users cannot choose how to pay; they have to select from one of the pre-defined options.
- In most cases, the user has to type in an actual credit card number on each site. This is like giving someone the keys to your expensive car, letting them drive it around the block in a potentially dangerous neighborhood (the web) and saying
*please don’t get carjacked!* - Merchants typically have to manage all this on their own: payment processor setup, costly processing fees, and possibly even PCI compliance.

There are services to mitigate a lot of these complications such as PayPal, Stripe, and others but they aren’t integrated into web devices very well. Mozilla wants to introduce a common web API to make payments *easy and secure* on web devices yet still as flexible as the checkout button for merchants.

As a first step, Mozilla will introduce [navigator.mozPay()](https://wiki.mozilla.org/WebAPI/WebPayment) in [Firefox OS](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS) so that web apps can [accept payments](https://developer.mozilla.org/en-US/docs/Apps/Publishing/In-app_payments).

## How Does It Work?

[navigator.mozPay()](https://wiki.mozilla.org/WebAPI/WebPayment) is a JavaScript API inspired by [google.payments.inapp.buy()](https://developers.google.com/commerce/wallet/digital/docs/index) but modified for things like multiple payment providers and carrier billing. When a web app invokes `navigator.mozPay()`

in Firefox OS, the device shows a secure window with a concise UI. After authenticating, the user can easily charge the payment to her mobile carrier bill or credit card. When completed, the app delivers the product. Repeat purchases are quick and easy.

In an earlier article I talked about [purchasing an app and receiving a receipt](https://hacks.mozilla.org/2013/02/building-a-paid-app-for-firefox-os/). `navigator.mozPay()`

is different in that there is no concept of what *product* is purchased, it’s just an API to facilitate a *payment* for a digital good or service, whatever that may be.

The payment starts and finishes in the client but further processing and notifications happen server side. This article briefly explains how it all fits together. For complete, in-depth documentation read the [Firefox Marketplace guide to in-app payments](https://developer.mozilla.org/en-US/docs/Apps/Publishing/In-app_payments).

## Integrating With A Payment Provider

Multiple [providers](https://wiki.mozilla.org/WebAPI/WebPaymentProvider) will facilitate payments behind the scenes of [navigator.mozPay()](https://wiki.mozilla.org/WebAPI/WebPayment). For example, the [Firefox Marketplace](https://marketplace.firefox.com/) will be able to facilitate payments.

As a developer you will essentially grant permission to each provider that you would like to sell through. In the current design of the API, you do this by asking each provider for an *Application Key* and an *Application Secret* so that you can digitally sign payment requests. A signed request prevents unauthorized parties from selling your products and prevents users from tampering with the price, etc.

## Initiating A Payment

When the user clicks a Buy button in your web app, you create a [JSON Web Token](http://openid.net/specs/draft-jones-json-web-token-07.html) (JWT) with your Application Secret. If you have agreements with multiple providers, you would create a JWT for each provider. Starting a payment looks roughly like this:

```
document.querySelector('button.buy').onclick = function() {
navigator.mozPay([mozillaJWT, otherJWT, ...]);
};
```

## Defining A Product

A [JWT](http://openid.net/specs/draft-jones-json-web-token-07.html) is a signed JSON object that defines details like the product name and price. Here is an example with some attributes removed for brevity:

```
{
"iss": APPLICATION_KEY,
"aud": "marketplace.firefox.com",
...
"request": {
"name": "Magical Unicorn",
"pricePoint": 1,
"postbackURL": "https://yourapp.com/postback",
"chargebackURL": "https://yourapp.com/chargeback"
}
}
```

You define prices as *price points* so that the payment provider can handle currency conversions for you in each region. In this example, `pricePoint`

1 might be €0.89 or $0.99, etc. Micropayments in small amounts will be supported. Consult the [navigator.mozPay()](https://wiki.mozilla.org/WebAPI/WebPayment) spec for details on how to construct a payment request JWT.

## Completing a Payment

To complete the payment, you need to wait for the provider to POST a result to your server’s `postbackURL`

(on success) or `chargebackURL`

(on failure). A more complete example of requesting a purchase in JavaScript would involve waiting for the postback to arrive, like this:

```
var request = navigator.mozPay([mozillaJWT, otherJWT]);
request.onsuccess = function() {
// The payment window has closed.
whenPaymentResultReceived(function() {
console.log('Success! User has purchased a Magical Unicorn.');
});
};
```

To implement `whenPaymentResultReceived()`

you might open a web socket to your server, wait for the payment result, and verify the incoming JWT signature. The [navigator.mozPay()](https://wiki.mozilla.org/WebAPI/WebPayment) spec has details on how postback and chargeback notifications work.

## Try It Out

Payments aren’t fully live yet in the Firefox Marketplace but you can simulate a payment to test out your code. Log into the [Firefox Marketplace Developer Hub](https://marketplace.firefox.com/developers/) and [generate](https://marketplace.firefox.com/developers/in-app-keys/) an Application Key and Application Secret for simulations. With those keys you can add a special parameter to the JWT like this:

```
{
"request": {
"name": "Magical Unicorn",
"pricePoint": 1,
...
"simulate": {"result": "postback"}
}
}
```

This will show a payment window on Firefox OS but it won’t charge you real money. It will let you test your client side JavaScript code and your server postback handlers to make sure everything is integrated smoothly. When you go live, just remove the `simulate`

attribute. If you’re new to Firefox OS development, check out the [Firefox OS Simulator](https://hacks.mozilla.org/2013/03/firefox-os-simulator-previewing-version-3-0/).

If you’re already working on a game or a web app for Firefox OS try thinking about using [navigator.mozPay()](https://wiki.mozilla.org/WebAPI/WebPayment) to offer premium content.

## This Would Be Way Easier With A Library

We thought so too! We built libraries for [Node.JS](https://github.com/mozilla/mozpay-js) and [Python](http://mozpay.readthedocs.org/en/latest/) to make the server side logic for [navigator.mozPay()](https://wiki.mozilla.org/WebAPI/WebPayment) as easy as possible. Libraries for more languages are on the way. We also are experimenting with [removing the server prerequisite](https://github.com/kumar303/mozpay-catalog/) entirely.

## Current Status

As you can probably tell by the prefix, `navigator.mozPay()`

is an experimental API and might change drastically or become unprefixed without notice. It will process live payments on the first Firefox OS phones and evolve quickly from real world usage.

Mozilla plans to work with other vendors through the W3C to reach consensus on a common API that supports web payments in the best way possible. After shipping in Firefox OS, Mozilla plans to add `navigator.mozPay()`

to Firefox for Android and desktop Firefox.

## New Business Models

Advertising has been the [primary business model](http://arstechnica.com/business/2010/03/why-ad-blocking-is-devastating-to-the-sites-you-love/) on the web for a long time but users have made it clear that [they don’t want to see ads](https://addons.mozilla.org/en-us/firefox/addon/adblock-plus/statistics/?last=30). Mozilla isn’t trying to directly disrupt the ad business but it is trying to [fix serious privacy issues](https://blog.mozilla.org/privacy/2013/02/25/firefox-getting-smarter-about-third-party-cookies/) relating to ad networks.

What if users explicitly paid for content instead? `navigator.mozPay()`

enables this kind of direct payment model: if something is good on the web, you can pay for it. It already [seems to be working well](http://articles.businessinsider.com/2012-03-21/tech/31218846_1_zynga-revenue-rate) for existing mobile apps. Will mobile ads even generate the same revenue for content producers as they do on desktop? I don’t have answers to these questions but one thing is for certain: the web should support businesses of all kinds and payments should be a first class feature of the web.

## Is It Webby?

Mozilla’s main goal with `navigator.mozPay()`

is to give users and merchants choice, security, and an easy to use payments system. The details about how merchants interact with payment providers is not yet specified in the API and that is clearly a gap. The first Firefox OS phones will ship with a whitelist of allowed payment providers which is also not ideal.

In a more webby model, all parties involved in the payment would be fully decentralized so that innovation can occur naturally and unknown payment providers could emerge. Who will be the next [M-Pesa](http://en.wikipedia.org/wiki/M-Pesa)? An elegant API would support that. Building a secure decentralized payment API is an ambitious challenge; the solution would need to address these core trust issues:

- How can customers trust that they will receive the goods after paying?
- How would customers ensure that their payment credentials are handled securely?
- How do merchants guarantee that they’ll get paid after delivering goods?

As with anything related to money, there is incentive for fraud every step of the way. [BitCoin](http://en.wikipedia.org/wiki/Bitcoin) is a digital currency that solves some of these trust issues with [block chains](https://en.bitcoin.it/wiki/Block_chain) and [PaySwarm](http://payswarm.com/wiki/PaySwarm_Design) is a web payment protocol that solves some of these issues with decentralized assets, public keys, etc. Mozilla will be watching PaySwarm as well as other models and hopefully `navigator.mozPay()`

can incorporate some of these concepts eventually.

## About
[
kumar303 ](http://farmdev.com/)

Kumar hacks on Mozilla web services and tools for various projects, such as those supporting [Firefox Add-ons](https://github.com/mozilla/addons/). He hacks on lots of [random open source projects](https://github.com/kumar303/) too.

## 34 comments

Tim WrightApril 4th, 2013 at 03:18OliverApril 4th, 2013 at 05:23Manu SpornyApril 5th, 2013 at 08:25MarcinApril 4th, 2013 at 05:53Manu SpornyApril 5th, 2013 at 08:27Kumar McMillanApril 5th, 2013 at 10:52Kumar McMillanApril 4th, 2013 at 08:02JulienApril 4th, 2013 at 08:23Kumar McMillanApril 4th, 2013 at 15:13Manu SpornyApril 4th, 2013 at 14:12crenApril 4th, 2013 at 16:38Manu SpornyApril 5th, 2013 at 08:30MikeApril 4th, 2013 at 17:17DanApril 5th, 2013 at 01:52Manu SpornyApril 5th, 2013 at 08:32David BialerApril 8th, 2013 at 11:54Manu SpornyApril 9th, 2013 at 10:13RApril 5th, 2013 at 03:51evanApril 6th, 2013 at 17:22PasiApril 6th, 2013 at 23:34MarcinApril 7th, 2013 at 03:19Kumar McMillanApril 7th, 2013 at 23:27Corn¸April 7th, 2013 at 05:28Fernando JiménezApril 7th, 2013 at 09:43Fernando JiménezApril 7th, 2013 at 09:50FranciscoApril 7th, 2013 at 16:47Kumar McMillanApril 7th, 2013 at 23:22Blue HandApril 7th, 2013 at 23:35DavidApril 8th, 2013 at 00:53Kumar McMillanApril 8th, 2013 at 10:13Justin ShortApril 9th, 2013 at 01:05Kumar McMillanApril 9th, 2013 at 10:39Justin ShortApril 9th, 2013 at 18:04StephenApril 29th, 2013 at 10:22