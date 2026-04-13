---
title: Implementing In-App Payments in Your Firefox OS App – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2013/11/implementing-in-app-payments-in-your-firefox-os-app/
author: Kumar
published: '2013-11-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

At Mozilla, we have been working on bringing payments to the web. We think it is important that developers have an easy way to monetize their apps. It also gives us the chance to offer deeper platform integration, allowing things like carrier billing in addition to credit/debit cards.

We’ve talked about in-app payments before in [navigator.mozPay() For Web Payments](https://hacks.mozilla.org/2013/04/introducing-navigator-mozpay-for-web-payments/), but this is an overview from an app developer’s standpoint. This also includes a few updates, such as real payments being live in the Firefox Marketplace. Payments are different than simply being a paid app, which charges the user once on the initial purchase. In-app payments is a different workflow, and allows you to charge the customer for specific items within your app.

## Architecture Overview

Payments are only enabled on Firefox OS devices for now. We are working on enabling them across other platforms, even desktop Firefox, but that is a ways off. For the rest of this article, we will assume the Firefox OS environment.

The [MDN page for in-app payments](https://developer.mozilla.org/en-US/docs/Web/Apps/Publishing/In-app_payments#Overview) has a good overview of the process, but here’s an even quicker overview. You need a server to generate the payments requests, because otherwise a hacker could easily change the prices to 0. The server creates [JWT](http://openid.net/specs/draft-jones-json-web-token-07.html) tokens, passes them to your app, and your app calls `navigator.mozPay`

with the token. The user will be taken to a built-in payments workflow, and when finished, your server will be notified. The [previous Hacks article on payments](https://hacks.mozilla.org/2013/04/introducing-navigator-mozpay-for-web-payments/) goes into the lower-level mechanics and reasons for payments more thoroughly.

It’s up to you to handle the rest of the workflow: updating the app when an item is successfully purchased, linking purchases to accounts, etc.

## Getting a Simulation Key

In order to use payments, you’ll need use the app key and secret generated for you by the Marketplace. If you just want to simulate payments, you can easily [grab a testing key and secret](https://marketplace.firefox.com/developers/in-app-keys/). The only thing you need to do is create an account if you haven’t done so already.

You will only be able to simulate payments with that key. When you are ready to use real money, you need to submit your app to the Marketplace, setup payments, and obtain a real key and secret. All of this is explained in more detail below.

## Setting up the Server-Side Code

The first thing you need to do is set up the server-side code. A “mozpay” module exists in [a few different languages](https://developer.mozilla.org/en-US/docs/Web/Apps/Publishing/In-app_payments#Code_libraries) which implements the payment workflow for you. If it does not exist in your programming language, you’ll need to use a [JWT module](https://developer.mozilla.org/en-US/docs/Web/Apps/Publishing/In-app_payments#Code_libraries) and do some more legwork. Check the rather [simple code](https://github.com/mozilla/mozpay-js/blob/master/lib/mozpay.js) from [mozpay-js](https://github.com/mozilla/mozpay-js) for an example of what you need to do.

I wrote a game for Firefox OS called [Webfighter](https://github.com/jlongster/webfighter) which uses [node.js](http://nodejs.org/) as the backend, so I used [mozpay-js](https://github.com/mozilla/mozpay-js) on the server-side. Webfighter is a shooter with a store where you can buy more weapons and ships, and it’s a good reference for developers to see actual code for working with payments. Examples below are taken from Webfighter. [You can check out Webfighter’s source here.](https://github.com/jlongster/webfighter)

First, require and configure the mozpay module:

```
var pay = require('mozpay');
var settings = require('settings');
pay.configure({
mozPayKey: settings.payKey,
mozPaySecret: settings.paySecret,
mozPayAudience: 'marketplace.firefox.com',
mozPayType: 'mozilla/payments/pay/v1',
mozPayRoutePrefix: '/mozpay'
});
```

The `settings`

module is just a file with JSON that specifies configuration of the app. It’s nice to separate the configuration so that you can easily swap it out in different environments, like development and production.

Use the key and secret that you got from the Marketplace. You should only change the audience and type options if you are using a different payment server than Mozilla’s. The routePrefix is optional and specifies the URL prefix for postbacks from the payment server.

Next you need to define a route that creates the data used for the payment transaction. The client is the one making the actual payments request (so that you don’t have to handle credit card details, and it’s possible to even be charged through carrier billing). You just need to create an object that represents a purchase. This example uses [express.js ](http://expressjs.com/)as the http server.

```
var purchaseQueue = {};
app.post('/sign-jwt', function(req, res) {
var token = 'o' + Date.now();
var item = getItem(req.body.name);
var jwt = pay.request({
id: item.name,
name: item.name,
description: item.description,
icons: { '64': settings.url + item.icon },
pricePoint: item.price,
productData: token,
postbackURL: settings.url + 'mozpay/postback',
chargebackURL: settings.url + 'mozpay/chargeback',
simulate: { result: 'postback' }
});
// Keep track of which JWT objects we are waiting on
purchaseQueue[token] = 'processing';
res.send(JSON.stringify({
jwt: jwt,
token: token
});
});
```

Notice the `settings`

object again; it’s just a dict that has some configuration properties about our app. `settings.url`

is the base URL where our app is hosted, so that all of the passed URLs are absolute.

We call `getItem`

to get the details about an item (which we don’t define here). I found it easiest to define a JSON file containing info about all the available items. You can see the [JSON for available items in Webfighter](https://github.com/jlongster/webfighter/blob/master/store.js) on GitHub.

There are [several fields for a purchase request](https://developer.mozilla.org/en-US/docs/Web/Apps/Publishing/In-app_payments#Set_up_your_server_to_sign_JWTs). `id`

is just a unique identifer, and we simply use the product name. Other fields describe the product, such as `icons`

which lists icons of various sizes. The `pricePoint`

is a number that maps to a specific price for each available region, and you should look at the [price point table](https://developer.mozilla.org/en-US/docs/Web/Apps/Publishing/App_pricing#Pricing_with_price_points) to find the one you need. For example, a price point of 10 indicates a price of $0.99 in the US.

The `simulate`

parameter tells the payments system to just simulate the request. If it’s passed, no real charges are made and you will be taken through a simulated workflow. This is useful for development. **Just remember** to remove this flag in production.

You can store anything you want to in `productData`

, which you can later use when handling events. Here I generated an arbitrary token to track requests, and I store it in the global object `purchaseQueue`

. We use this when we handle events.

Next, subscribe to the `postback`

event from the mozpay module:

```
pay.on('postback', function(data) {
// the payment was successful
var req = data.request;
purchaseQueue[req.productData] = 'success';
});
```

You can also subscribe to the `chargeback`

event. Chargebacks happen when a customer disputes a charge and gets the money back. This could happen a month later, and is difficult to process. Webfighter keeps track of chargebacks, but the app does not check for them and revoke items. You would need to check periodically or on startup if the user still has access to all purchased items.

```
pay.on('chargeback', function(data) {
var req = data.request;
purchaseQueue[req.productData] = 'chargeback';
});
```

That’s it for the server-side.

## Using mozPay On the Client Side

On the client-side, you need to post to `/sign-swt`

and use `mozPay`

to initiate the purchase. In the following code, we check if `mozPay`

is available and if it’s not we just give the user the item. Remember, it’s just a test app! Once a purchase is initiated, we start polling the server until we get a successful purchase.

```
function buy(name) {
// Purchase an item by requesting a JWT object from the
// server, and posting it to the mozPay API
$.post('/sign-jwt', { name: name }, function(res) {
if(navigator.mozPay) {
var req = navigator.mozPay([res.jwt]);
req.onerror = function() {
console.log('mozPay error: ' + this.error.name);
clearPolling();
};
// Poll to see when the payment is complete
startPolling();
}
else {
alert('in-app payments unavailable, so giving it to you for free');
onPurchase(name);
}
});
}
```

Here are the polling functions which wait until the server responds with a successful purchase. Note that we only check for a successful purchase. The user will be notified of any errors within the native payment screen, and when they close the screen an error event is fired on the `mozPay`

request object, which we handle and stop the polling. See the above code with `req.onerror`

.

```
function pollQueue(token, name) {
// Poll the server every second to see the status of our
// payment request
$.get('/purchaseQueue?token=' + token, function(res) {
if(res == 'success') {
onPurchase(name);
clearPolling();
}
});
}
var pollTimer;
function startPolling() {
pollTimer = setInterval(function() { pollQueue(res.token, name); }, 1000);
}
function clearPolling() {
if(pollTimer) {
clearInterval(pollTimer);
}
pollTimer = null;
}
```

We call `onPurchase`

when an item is successfully purchased and should be enabled for the user. You should create that function and write your app-specific code.

## Real payments: submitting app to the Firefox Marketplace

When you are ready to run real payments, remove the `simulate`

field when the server creates the payment request, and [submit your app](https://marketplace.firefox.com/developers/submit/) to the Firefox Marketplace. It needs to be submitted so that you can hook up real payments.

### Get paid: configuring bank account details and payment options

Once your app is submitted, [edit your app](https://marketplace.firefox.com/developers/submissions) and click on “Compatibility & Payments” on the left side and select “Paid / In-App”. Under “Payment Accounts”, and add your bank account. One thing that tripped me up was needing the SWIFT code for my bank. In the future, Marketplace will hopefully autofill it, but for now you can look it up on the [theswiftcodes.com](http://www.theswiftcodes.com/).

Under “Price & Countries” you can set the price for your app. You may just want “Free with in-app payments”, which is what Webfighter is. Additionally, you can selectively choose which region your app is available in. Apps with payments are only available in regions with them enabled.

### Use a real key & secret

Now click the “In-App Payments” link in the left sidebar. You’ll see a screen where you can grab a new key & secret for real payments. Use these in the `configure`

call on the server. Never share your secret.

At this time of writing, carrier billing is only available in specific countries. Check out the [Payments Status page](https://marketplace.firefox.com/developers/docs/payments/status) for where it’s available. When it is not available, the user will be presented with a credit card screen.

## Go make some money with your app!

We want you to be successful in participating in the app ecosystem and economy. Let us know what your experience is like! We are happy to answer any questions over on the [marketplace mailing list](https://lists.mozilla.org/listinfo/dev-marketplace).

## About
[
kumar303 ](http://farmdev.com/)

Kumar hacks on Mozilla web services and tools for various projects, such as those supporting [Firefox Add-ons](https://github.com/mozilla/addons/). He hacks on lots of [random open source projects](https://github.com/kumar303/) too.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 17 comments

Progi1984November 26th, 2013 at 14:18James LongNovember 26th, 2013 at 14:31Progi1984November 26th, 2013 at 14:45James LongNovember 26th, 2013 at 15:16Progi1984November 26th, 2013 at 15:52James LongNovember 26th, 2013 at 16:45Progi1984November 27th, 2013 at 00:05James LongNovember 27th, 2013 at 08:26Kumar McMillanNovember 26th, 2013 at 18:24Stuart LangridgeNovember 26th, 2013 at 14:22Andy McKayNovember 26th, 2013 at 14:49Stuart LangridgeNovember 26th, 2013 at 15:49Andy McKayNovember 26th, 2013 at 17:28Stuart LangridgeNovember 26th, 2013 at 18:22Kumar McMillanNovember 26th, 2013 at 18:32Stuart LangridgeNovember 26th, 2013 at 18:41Kumar McMillanNovember 26th, 2013 at 18:43