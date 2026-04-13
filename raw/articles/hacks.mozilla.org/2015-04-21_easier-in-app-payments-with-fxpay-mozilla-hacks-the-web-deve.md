---
title: Easier in-app payments with fxpay – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/04/easier-in-app-payments-with-fxpay/
author: Kumar
published: '2015-04-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

For developers building web applications on [Firefox OS](https://www.mozilla.org/en-US/firefox/os/) or [Firefox Desktop](https://www.mozilla.org/en-US/firefox/desktop/), supporting payments is easy with Mozilla’s [fxpay](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap) library. In addition to accepting credit cards, Mozilla’s payment system lets users charge purchases directly to their phone bill in many countries—making it ideal for mobile commerce.

Since our [first introduction to fxpay](https://hacks.mozilla.org/2014/09/introducing-fxpay-for-in-app-payments/) the library has received a lot of bug fixes and new features. Based on developer feedback, we also decided to offer a new interface supporting [native promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) ([shimmed](https://github.com/jakearchibald/es6-promise) on older browsers) for flexibility and better error handling. This article explains how to retrieve products, process payments, and restore products from receipts.

If you’ve already set up [in-app payments using the mozPay API](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/mozPay_iap) directly, consider porting to [fxpay](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap) for the convenience of Mozilla-hosted products and additional features such as desktop payments. At the very least, please make sure your [JWT libraries are patched](http://jwt.io/#libraries) for the latest security vulnerabilities.

Let’s get started! After [installing the fxpay library](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap#Installation), you can begin testing it out with some [fake products](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap#Working_with_Fake_Products).

```
fxpay.configure({fakeProducts: true});
fxpay.getProducts()
.then(function(products) {
products.forEach(function(product) {
addBuyButtonForProduct(product);
});
})
.catch(function(error) {
console.error('error getting products: ' + error);
});
```


This retrieves some pre-configured fake products that you can play around with. Once you’ve [configured real products](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap#Set_Up_Your_Products) on the Firefox Marketplace Developer Hub, you can remove this configuration value to work with real products.

In the example function called above, you could display a buy button per product like this:

```
function addBuyButtonForProduct(product) {
var button = document.createElement('button');
button.textContent = 'Buy ' + product.name;
button.addEventListener('click', function () {
fxpay.purchase(product.productId)
.then(function(purchasedProduct) {
console.log('product purchased! ',
purchasedProduct);
})
.catch(function(error) {
console.error('error purchasing: ' + error);
});
});
document.body.appendChild(button);
}
```


The fxpay library does all the payment processing behind the scenes using [Mozilla’s web services](http://firefox-marketplace-api.readthedocs.org/en/latest/topics/payment.html) so when the promise resolves, it’s safe to deliver the product. At this time, fxpay also installs a receipt on the user’s device. When the user returns to your app later on, you’ll want to check for any receipts so you can restore their purchases.

Here’s a rewrite of the product fetching code to restore purchased products:

```
fxpay.getProducts()
.then(function(products) {
products.forEach(function(product) {
if (product.hasReceipt()) {
product.validateReceipt()
.then(function(restoredProduct) {
console.log('restored product from receipt:',
restoredProduct);
})
.catch(function(error) {
console.error('error validating receipt: ' +
error);
});
} else {
addBuyButtonForProduct(product);
}
});
});
```


We’re hoping this new interface makes experimenting with in-app payments even easier than before. You never know what kind of business model will work in your app so why not try out some ideas?

The complete [usage guide to fxpay is here on MDN](https://developer.mozilla.org/en-US/Marketplace/Monetization/In-app_payments_section/fxPay_iap).

## About
[
kumar303 ](http://farmdev.com/)

Kumar hacks on Mozilla web services and tools for various projects, such as those supporting [Firefox Add-ons](https://github.com/mozilla/addons/). He hacks on lots of [random open source projects](https://github.com/kumar303/) too.

## 4 comments

AndersMay 7th, 2015 at 12:23Kumar McMillanMay 7th, 2015 at 13:20AndersMay 7th, 2015 at 15:44Kumar McMillanMay 8th, 2015 at 11:13