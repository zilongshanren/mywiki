---
title: Introducing fxpay for in-app payments – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/09/introducing-fxpay-for-in-app-payments/
author: Kumar
published: '2014-09-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A [while ago](https://hacks.mozilla.org/2013/04/introducing-navigator-mozpay-for-web-payments/) Mozilla announced [navigator.mozPay()](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/mozPay_iap) for accepting payments on [Firefox OS](https://developer.mozilla.org/en-US/Firefox_OS). This was our first step toward helping developers do commerce on the web. It solved the problem of processing payments but what about the rest? Today we’re announcing an early peek at [fxpay](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap), a library for the rest of what you need as a developer to sell digital products in your app. This small JavaScript library (11kB minified) gives you some nice additional features on top of payment processing:

- Work with a catalog of in-app products without hosting your own server
- Securely verify each payment in one simple JavaScript callback
- Restore previous purchases from
[receipts](https://wiki.mozilla.org/Apps/WebApplicationReceipt)

The [mozPay()](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/mozPay_iap) API is great if you need to integrate with an existing system but building a product catalog from scratch is a lot of work. If you have an idea for adding revenue to your app, why not quickly toss in some products and see what sells?

The [fxpay](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap) library is designed to get you selling as quickly as possible. Because it interacts with the [Firefox Marketplace API](http://firefox-marketplace-api.readthedocs.org/en/latest/) you don’t need to manage code on your own server — you enter product details on [Firefox Marketplace](https://marketplace.firefox.com/developers/) and call some JavaScript functions in your app to sell them.

## First: A Warning

**fxpay is in an early experimental state**. We’re looking for your help to make it a concise, intuitive library which means the API might change rapidly. There’s a section below for details about how to get involved.

## Offer Some Products For Sale

After running `bower install fxpay`

([installation details](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap#Installation)), show some products for sale within your app using [getProducts()](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap#Fetching_Products):

```
// First, let's test with some fake products.
fxpay.configure({fakeProducts: true});
fxpay.getProducts(function(error, products) {
if (error) {
console.error(error);
} else {
products.forEach(function(product) {
addBuyButtonForProduct(product);
});
}
});
```

The code here would add a buy button for each product so that tapping the button would start a purchase. Here’s a simplistic example:

```
function addBuyButtonForProduct(product) {
var button = document.createElement('button');
button.textContent = 'Buy ' + product.name;
button.addEventListener('click', function () {
fxpay.purchase(product.productId,
function(error, product) {
if (error) {
console.error(error);
} else {
console.log(product.name + ' bought!');
}
});
});
document.body.appendChild(button);
}
```

That’s it. The call to [fxpay.purchase()](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap#Capture_A_Purchase) guides the user through payment via [mozPay()](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/mozPay_iap) and verifies the result on the Firefox Marketplace server. If you receive the callback without an error that means the purchase was verified and funds will be transferred to your account upon completion. It is safe to deliver the product.

## Try It Out

Install an app on the [Firefox OS Simulator](https://developer.mozilla.org/en-US/docs/Tools/Firefox_OS_Simulator) using the [App Manager](https://developer.mozilla.org/en-US/Firefox_OS/Using_the_App_Manager) and tap your custom buy button. Since this is a test with fake products, you’ll see a payment [simulation](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/mozPay_iap#Simulating_payments) screen. Tap Continue and your purchase callback will fire, allowing you to get your product delivery code working.

## Restoring Purchases

When a user completes a purchase, a portable [receipt](https://wiki.mozilla.org/Apps/WebApplicationReceipt) is installed on their device behind the scenes. This is a cryptographically signed JSON object that proves ownership of the product. Each time the user returns to your application, you’ll want to check for any receipts so you can restore their purchased products. The fxpay library does the validation for you but you have to define a callback for when each product is [restored](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap#Restoring_Products_From_Receipt) like this:

```
fxpay.init({
onerror: function(error) {
console.error('init error:', error);
},
onrestore: function(error, product) {
if (error) {
console.error('onrestore error:', error);
} else {
console.log(product.name + ' restored');
}
}
});
```

Just like the purchase callback, if you don’t get an error it means the receipt is valid; the user owns the product so you should make it available. You probably only need to run [init()](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap#Initialization) once when your app starts up.

## Publishing Your Application

Once you get everything working with fake products, the next step is to submit your app to the [Firefox Marketplace developer hub](https://marketplace.firefox.com/developers/) so users can install it. The submission process is detailed in the [documentation](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap); it includes entering bank account details to receive payouts and submitting real names and prices of the products you wish to sell.

Once all of your products are in place and your app has been approved, set `{fakeProducts: false}`

and the same code you see here will begin to work with real products. The `getProducts()`

function will use your app’s [origin](https://developer.mozilla.org/en-US/Apps/Build/Manifest#origin) to retrieve the configured products.

## Example App

The fxpay library ships with an [example app](https://github.com/mozilla/fxpay/tree/master/example) that you can install from the [App Manager](https://developer.mozilla.org/en-US/Firefox_OS/Using_the_App_Manager) and play around with.

## Get Involved

Do you have an idea for an app with in-app payments? Try it out. We’re announcing an early version of [fxpay](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap) so we can make it work well for you, the developer. If something breaks or just feels awkward or if you have an idea to make the library better, get in touch!

- Submit an idea using our
[user voice forum](https://openwebapps.uservoice.com/forums/258478-open-web-apps) - Start a discussion thread on
[dev-marketplace](https://lists.mozilla.org/listinfo/dev-marketplace) - File a
[bug](https://bugzilla.mozilla.org/enter_bug.cgi?product=Marketplace&component=Payments/Refunds) - Submit a pull request to the
[frontend script](https://github.com/mozilla/fxpay)or the[backend API](https://github.com/mozilla/zamboni)

## Going Further

The Payments team at Mozilla is small (but mighty!). This release has a lot of missing features but we wanted to start getting early feedback. Here are a few ideas for features we’d like to add next:

### Support More App Types

Right now, fxpay is limited to privileged [packaged apps](https://developer.mozilla.org/en-US/Marketplace/Options/Packaged_apps) on mobile only. See [all prerequisites](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap#Prerequisites). We’re working to open up access to other app types such as hosted apps and desktop apps.

### Receipt Recovery

If a user loses their device or deletes the app they will lose their in-app purchase receipts. Those receipts are backed up on the Marketplace server but users don’t have an interface to reinstall them yet. We’re trying to figure out a way to do that in [bug 1045228](https://bugzilla.mozilla.org/show_bug.cgi?id=1045228).

### Exact Product Prices

Price points and currencies vary by mobile network but non-certified apps don’t have a reliable way to detect users’ networks. Currently you can’t display prices next to your custom buy buttons. We’d like to offer some solutions for this even if it’s just a manual currency selector. See [bug 1063758](https://bugzilla.mozilla.org/show_bug.cgi?id=1063758).

### Product Assets

This first release of fxpay is best suited for local content such as unlocking a level in a game. If an app were to distribute remote content such as a MP3 file as a ring tone, there would be no way to securely protect the contents of that file. We’ll be considering how to add support for this in [bug 1063059](https://bugzilla.mozilla.org/show_bug.cgi?id=1063059).

We’re planning lots of other stuff too!

## About
[
kumar303 ](http://farmdev.com/)

Kumar hacks on Mozilla web services and tools for various projects, such as those supporting [Firefox Add-ons](https://github.com/mozilla/addons/). He hacks on lots of [random open source projects](https://github.com/kumar303/) too.

## One comment

Viking KARWURSeptember 17th, 2014 at 16:53