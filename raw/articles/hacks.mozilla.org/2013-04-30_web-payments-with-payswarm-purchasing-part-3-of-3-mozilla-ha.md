---
title: 'Web Payments with PaySwarm: Purchasing (part 3 of 3) – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2013/04/web-payments-with-payswarm-purchasing-part-3-of-3/
author: Manu Sporny
published: '2013-04-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## The Promise of Web Payments

The [first](https://hacks.mozilla.org/2013/04/web-payments-with-payswarm-identity-part-1-of-3/) and [second](https://hacks.mozilla.org/2013/04/payswarm-part-2/) articles in this series outlined how [PaySwarm](https://payswarm.com/) is designed to transmit and receive funds with the same ease as sending and receiving an email. The articles went on to explain how making the tools that have been traditionally only available to banks, Wall Street, and large corporations available to everyone can help reform our financial systems. The goal is not just one-click payments, but also to enable crowdfunding innovation, help Web developers earn a living through the Web, boost funding rounds for start-ups, and to advance initiatives that will lead to a more egalitarian society.

This is the final article in a three part series on sending and receiving funds using the PaySwarm specification. This article will review some of the concepts in the first two articles and introduce the concepts of a purchase request, digital contract, and digital receipt. A tutorial will go on to explain how to perform a purchase via PaySwarm as well as how to download the digital receipt of sale. Code examples and video of the process are provided.

## Review: Identity

As explained in [the first article](https://hacks.mozilla.org/2013/04/web-payments-with-payswarm-identity-part-1-of-3/), the Web Keys specification provides a simple, decentralized identity solution for the Web based on public key cryptography. It enables Web applications to send messages that are encrypted and verifiable.

The messages are marked up using the JavaScript Object Notation for Linking Data ([JSON-LD](http://json-ld.org/)). As the name suggests, JSON-LD is a way of expressing [Linked Data](http://www.youtube.com/watch?v=4x_xzT5eF5Q) in JSON. Both HTML documents and JSON-LD documents describe things and have links to other documents on the Web. The primary benefit of a JSON-LD document is that a machine can easily extract and perform basic reasoning over the information it contains without placing a large burden on its author.

Web Keys coupled with JSON-LD provide the underlying identity and messaging mechanism used by PaySwarm to perform Web Payments.

## Review: Assets and Listings

As explained in [the second article](https://hacks.mozilla.org/2013/04/payswarm-part-2/), PaySwarm enables products and services to be listed for sale on the Web in a decentralized way. The specification allows content creators and developers to be in control of their own product descriptions and prices in addition to giving them the option to delegate this responsibility to an App Store or large retail website. The second article elaborated on the two basic concepts that are used to describe products and services for sale on the Web: *assets* and *listings*.

An asset is a description of a product or service. Examples of assets include web pages, ebooks, groceries, concert tickets, dog walking services, donations, rights to transmit on a particular radio frequency band, and invoices for work performed. In general, anything of value can be modeled as an asset.

A listing is a description of the specific terms under which an asset is offered for sale. These terms include: the asset being sold, the license that will be associated with the purchase, the list of people or organizations to be paid for the asset, and the validity period for the listing.

## Purchase Requests, Contracts, and Receipts

So far this series has introduced a decentralized identity mechanism, a secure and verifiable messaging mechanism, and a decentralized mechanism for publishing products and services for sale. This article introduces the *purchase request*, the *contract*, and the *receipt*.

A *purchase request* is sent to a PaySwarm Authority when a purchase is requested by the customer. It contains details about the asset and listing that the buyer would like to purchase. There are two ways a purchase request can be authorized:

The first way is for the vendor to provide a customer with a purchase request to give to their PaySwarm Authority. Once the customer submits the purchase request, they can then use an interface provided by their PaySwarm Authority to view the potential contract and decide whether they agree to its terms.

The second way a purchase request can be authorized by a customer is by digitally signing it using software running on a device like a personal computer or a cell phone. The purchase request can then be transmitted by this software to their PaySwarm Authority for processing. This approach allows the customer to use innovative third party applications that need to perform purchases on their behalf.

A *contract* is an electronic document that expresses an agreement between all parties involved in a transaction. It contains the asset, digitally signed by the asset provider, and the listing, digitally signed by the vendor. A contract can be finalized in one of two ways:

The first way a contract is completed is when an authorized purchase request is submitted to a PaySwarm Authority. If payment processing can occur without issue, then a contract for that purchase is completed and kept on record by the PaySwarm Authority.

The second way to complete a contract requires a customer to digitally sign the contract before submitting it to a PaySwarm Authority. This approach allows a customer to fully review the terms of the contract using an interface that is not hosted by the PaySwarm Authority. If the customer agrees to the contract, their software digitally signs it. The digitally-signed contract can then be transmitted to their PaySwarm Authority using a variety of different mechanisms. This is particularly useful when the customer does not have access to the Internet, but the vendor from which they are purchasing does. An example of this is when a customer makes an in-store retail purchase with a PaySwarm-enabled mobile phone with no data plan. The phone could receive a contract from the vendor over NFC, digitally sign the contract on the phone, and transmit the signed contract back to the vendor over NFC. The contract would then be delivered to the customer’s PaySwarm Authority by the vendor and payment processing would be performed.

A *receipt* is the result of a successful purchase. Typically, receipts are provided to a vendor by a PaySwarm Authority with the minimum amount of information necessary to prove that the sale of an asset to a particular customer was completed successfully. For a more comprehensive review of a purchase, a vendor or customer can request a full contract from their PaySwarm Authority. A contract is provided to buyers as a proof-of-purchase and for offline storage. It will contain all of the details proving the purchase occurred, even if the PaySwarm Authority that processed the purchase and/or the vendor go out of business or shut down for any reason.

The video below shows a browser-based mechanism used to process a purchase request, contract, and receipt:

The rest of this tutorial will demonstrate how to perform a console-based purchase where the customer constructs, signs, and transmits the purchase request to a PaySwarm Authority for processing. Code from the [payswarm.js node module](https://github.com/digitalbazaar/payswarm.js) will be used throughout this tutorial. Specifically, it references the [asset purchasing example](https://github.com/digitalbazaar/payswarm.js/blob/40886553ea041563dbd39de2d1cd8f0d782e2438/examples/purchase-asset.js). The payment processor will be the [PaySwarm Developer Sandbox](https://dev.payswarm.com/) and the asset hosting service will be the [PaySwarm Developer Listing Service](http://listings.dev.payswarm.com/).

## Performing the Purchase

This tutorial assumes that you have already read the [first](https://hacks.mozilla.org/2013/04/web-payments-with-payswarm-identity-part-1-of-3/) and [second](https://hacks.mozilla.org/2013/04/payswarm-part-2/) articles in this series. In those articles, an identity was created via a PaySwarm Authority and a Web Key was associated with the identity for the purpose of creating digital signatures. The registered Web Key will be used to digitally sign the purchase request seen in this tutorial. An asset and listing were also published to the [PaySwarm Developer Listing Service](http://listings.dev.payswarm.com/).

The first step in performing a purchase is to retrieve the listing that indicates which asset is for sale. The `getJsonLd()`

function in the payswarm.js library can be used to retrieve the listing data given a URL:

```
var url =
'http://listings.dev.payswarm.com/mozhacks/html5-me-song#listing';
payswarm.getJsonLd(url, {cache: true}, function(listing) {
// do something with the listing
});
```

The code above simply fetches the listing from the given URL in JSON-LD format. The data could be expressed on the page as HTML+RDFa, which is then translated to JSON-LD and returned to the application. The listing data can then be used to construct a purchase request, digitally sign it, and deliver it to a PaySwarm Authority for processing. All of this is done below by calling the `purchase()`

function in the payswarm.js library:

```
// purchase the asset under the terms of the listing by
// digitally signing a purchase request and sending it
// to the PaySwarm Authority
payswarm.purchase(listing, {
// the Web Service that will process the purchase request
transactionService: 'https://dev.payswarm.com/transactions',
// the identity that is performing the purchase
customer: 'https://dev.payswarm.com/i/IDENTITY',
// this financial account will be the source for
// the payment funds
source: 'https://dev.payswarm.com/i/IDENTITY/accounts/ACCOUNT',
// the private key information used to digitally sign
// the purchase request
privateKeyPem: publicKey.privateKeyPem,
// the public key ID that will be associated with the
// digitally signed purchase request
publicKey: publicKey.id,
// log details of the transaction to the console
verbose: true
}, function(err, receipt) {
// if err is null, the purchase was successful
// do something with the receipt
console.log('Receipt:', receipt);
// the transaction ID can be used to download
// the complete contract
console.log('Transaction ID:', receipt.contract.id);
});
```

The code above builds a purchase request using the listing data retrieved in the previous step. The purchase request also includes the financial account which will provide the funds for the purchase. It is then digitally signed using the buyer’s public key. The signed purchase request is then HTTP POSTed to the transaction processing web service on the PaySwarm Authority. If the asset, listing, license, and payment details in the contract are all valid, the PaySwarm Authority will process the payment and return a digitally signed receipt. The receipt will contain the transaction ID for the sale, which can then be used to retrieve the full contract for the sale.

## Downloading the Contract

The contract for the sale can be downloaded and stored to be used as a proof-of-purchase. A utility provided with the payswarm.js library can be used to download the transaction by issuing a simple command:

./bin/payswarm url https://dev.payswarm.com/transactions/1.24.f3d

The video below demonstrates what a console-based purchase looks like using the payswarm.js library:

## Conclusion

This was the final article in this three part series on building PaySwarm-enabled websites and web applications. One of the primary goals of PaySwarm is to make transmitting and receiving funds on the Web as easy as sending and receiving an email. This is not just about one-click payments; it is also about using open standards to bring new and powerful tools to the general public that will breed competition and innovation.

If you would like to keep up-to-date with the latest in Web Payments, [join the Web Payments Community mailing list](http://lists.w3.org/Archives/Public/public-webpayments/).

## About
[
Manu Sporny ](https://twitter.com/manusporny)

Founder of [Web Payments](http://www.w3.org/community/webpayments/) at W3C. Chair of [RDFa](http://rdfa.info/) and [JSON-LD](http://json-ld.org/) Working Groups. Lead editor of [PaySwarm](https://payswarm.com/), JSON-LD, and HTML5+RDFa specifications. Founded the company that created [Meritora](https://meritora.com/), the worlds first commercial PaySwarm payments processor. Leading the integration of finance and payments into the core architecture of the Web. Lots of standards-related work where the focus is on making the world a better place for all people. Other accounts: [@manusporny](https://twitter.com/manusporny), [+Manu Sporny](https://plus.google.com/102122664946994504971/about/), [LinkedIn](http://www.linkedin.com/in/manusporny/), and [blog](http://manu.sporny.org/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## One comment

BrunoMay 7th, 2013 at 07:08