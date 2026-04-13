---
title: 'Web Payments with PaySwarm: Assets and Listings (part 2 of 3) – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2013/04/payswarm-part-2/
author: Manu Sporny
published: '2013-04-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## The Promise of Web Payments

The [first article in this series](https://hacks.mozilla.org/2013/04/web-payments-with-payswarm-identity-part-1-of-3/) on PaySwarm outlined how the technology is designed to transmit and receive funds with the same ease as sending and receiving an email. It went on to explain how taking the tools that have been traditionally only available to banks, Wall Street, and large corporations and making them available to everyone can reshape financial systems in a very positive way. The goal is not just one-click payments, but also to enable crowdfunding innovation, help Web developers earn a living through the Web, boost funding rounds for start-ups, and more.

This article is the second in a three part series on buying and selling content using the PaySwarm specification. It will review some basic concepts covered in the first article and then explain how to list things for sale using PaySwarm.

## Review: Web Keys and JSON-LD

As explained in part one, the Web Keys specification provides a simple, decentralized identity solution for the Web based on public key cryptography. It enables Web applications to send messages that are both protected from snooping and verifiable via digital signatures.

The messages are marked up using the JavaScript Object Notation for Linking Data ([JSON-LD](http://json-ld.org/)). As the name suggests, JSON-LD is a way of expressing [Linked Data](http://www.youtube.com/watch?v=4x_xzT5eF5Q) in JSON. Both HTML documents and JSON-LD documents describe things and have links to other documents on the Web. The primary benefit with JSON-LD is that the entire document is understandable by a machine to the point that it can extract and perform basic reasoning without placing a huge burden on the developer writing the JSON markup.

Web Keys coupled with JSON-LD provide the underlying messaging and product markup mechanism used by PaySwarm to perform Web Payments.

## Decentralized Products and Services

One design requirement of a Web Payments system is that the identity mechanism (Web Keys) must be decentralized. Another requirement is that the data markup mechanism (JSON-LD) must be capable of expressing decentralized resources like people, places, events, goods/services, and a variety of other data that will likely exist on 3rd party websites.

Similarly, PaySwarm does not require that products and services be listed in a central location on the Web. Instead, it allows content creators and developers to be in control of their own product descriptions and prices in addition to giving them the option to delegate this responsibility to an App Store or large retail website. PaySwarm has the following requirements when it comes to listing products and services for sale:

- The listings must be able to be decentralized, which reduces the possibility of monopolistic behavior among retailers.
- The product being sold must be separable from the terms under which the sale occurs, enabling different prices to be associated with different licenses, affiliate sales, and business models like daily deals.
- The creator of the product must be able to specify restrictions on pricing, resellers, validity periods, and a variety of other properties associated with the sale of the product. This ensures that the product creator is in control of her product at all times.
- It must support decentralized extensibility, which enables applications to add application-specific data to the product description and terms of sale.
- It must be secure, such that the risk of tampering with product descriptions and prices is mitigated.
- It must be non-repudiable, such that the creator of the listing cannot dispute the fact that they created it.

## Assets and Listings

There are two concepts that are core to understanding how products and services are listed for sale via PaySwarm.

The first is the *asset*. An asset is a description of a product or service. Examples of assets include web pages, ebooks, groceries, concert tickets, dog walking services, donations, rights to transmit on a particular radio frequency band, and invoices for work performed. In general, anything of value can be modeled as an asset.

An asset typically describes something to be sold, who created it, a set of restrictions on selling it, and a validity period. Since the asset is expressed using JSON-LD, a number of other application-specific properties can be associated with it. For example, a 3D printing store could include the dimensions of the asset when physically printed, the materials to be used to print the asset, and a set of assembly instructions. Upon purchase of the asset, a digital receipt with a description of the asset is generated. This receipt can be given to a printer to produce a physical representation of the asset.

The second concept that is key to understanding how products and services are sold in PaySwarm is the *listing*. A listing is a description of the specific terms under which an asset is offered for sale. These terms include: the exact asset being sold, the license that will be associated with the purchase, the list of people or organizations to be paid for the asset, and the validity period for the listing. Like an asset, a listing may include other application-specific properties.

This tutorial elaborates on creating an asset and listing and publishing them to a website, as shown briefly in the video below:

Code from the [payswarm.js node module](https://github.com/digitalbazaar/payswarm.js) will be used throughout this tutorial. Specifically, it utilizes the [asset publishing example](https://github.com/digitalbazaar/payswarm.js/blob/a2cb8cdb0f764f799f6020a32427c1d77c9e7545/examples/publish-asset-for-sale.js). The payment processor will be the [PaySwarm Developer Sandbox](https://dev.payswarm.com/) and asset hosting service will be the [PaySwarm Developer Listing Service](http://listings.dev.payswarm.com/).

## Creating an Asset

As mentioned previously, an asset is described using JSON-LD. An asset is built in a programming language the same way one would build data to be published as a JSON document. Typically, this involves using an object (in JavaScript), a dictionary (in Python), an associative array (in PHP), or a hash (in Ruby). Here is the code to create an asset in JavaScript. Pay particular attention to the comments as they will explain what each key-value pair means. Let’s try a simple example first:

```
// create a PaySwarm asset
var asset = {
// the @context is a hint to a JSON-LD processor on how to interpret the
// key-value pairs in the document
'@context': 'https://w3id.org/payswarm/v1',
// this is the global identifier for the asset
id: 'http://listings.dev.payswarm.com/mozhacks/demo#asset',
type: ['Asset'],
// this is the person who created the asset
creator: { fullName: 'Developer Joe' },
title: 'Mozilla Hacks Demo Asset',
// this is typically the link to the paid content
assetContent: 'http://listings.dev.payswarm.com/mozhacks/demo#asset',
// this is the entity that has rights to the asset (or owns it)
assetProvider: 'https://dev.payswarm.com/i/YOUR_IDENTITY_HERE'
};
```

The code above is a working example of an asset description in about seven lines of code (without comments). It describes an asset called *Mozilla Hacks Demo Asset*, which can be sold by anyone. The idea is that you would express this data on a website, either as a separate JSON-LD document or directly in an HTML5 page using RDFa markup. Any PaySwarm-compatible payment processor could then get your document and know exactly what you have created and what the sale restrictions are.

Let’s take a look at a more complex example. The asset below specifies a song with a twist on how it can be sold. It can be resold by anyone, with 80% of the proceeds, or a minimum of $0.50, going to the band that created the song.

```
// create a PaySwarm asset
var asset = {
// the @context is a hint to a JSON-LD processor on how to interpret the
// key-value pairs in the document
'@context': 'https://w3id.org/payswarm/v1',
// this is the global identifier for the asset
id: 'http://listings.dev.payswarm.com/mozhacks/html5-me-song#asset',
type: ['Asset', 'schema:MusicRecording'],
// this is the person who created the asset
creator: { fullName: 'The Webdevs' },
title: 'HTML5 Me, Baby',
// this is the link to the paid content
assetContent: 'http://listings.dev.payswarm.com/mozhacks/paid/html5-me-song',
// this is the entity that has rights to the asset (the artist in this case)
assetProvider: 'https://dev.payswarm.com/i/the-webdevs',
// these are restrictions under which the asset can be sold
listingRestrictions: {
// validity dates so that the price information below doesn't
// last forever (you may want to change your price)
validFrom: payswarm.w3cDate(validFrom),
validUntil: payswarm.w3cDate(validUntil),
payee: [{
// this is an entity that should be paid when the asset is sold
type: 'Payee',
// when the asset is sold, put the money for the asset provider here
destination: 'https://dev.payswarm.com/i/the-webdevs/accounts/royalties',
// the name of the group determines how this particular payee's rate comes
// out of the total price of the sale
payeeGroup: ['assetProvider'],
// next 6 lines: the greater of 80% of the vendor's price or $0.50 should go
// to the content creator
payeeRate: '80',
payeeRateType: 'Percentage',
payeeApplyType: 'ApplyInclusively',
payeeApplyGroup: ['vendor'],
minimumAmount: '0.50',
currency: 'USD',
// show this to the buyer as one of the line items in the digital receipt
comment: 'Payment to The Webdevs for creating the HTML5 Me, Baby song'
}],
payeeRule: [{
// next 2 lines: allow the payment processor (the PaySwarm Authority) to add
// a fee for processing the transaction
type: 'PayeeRule',
payeeGroupPrefix: ['authority']
}, {
// next 4 lines: vendors can only specify a flat fee for reselling the song
// from their website
type: 'PayeeRule',
payeeGroup: ['vendor'],
payeeRateType: 'FlatAmount',
payeeApplyType: 'ApplyExclusively'
}]
}
};
```

The code above is a more comprehensive example of an asset description in approximately 30 lines of code (without comments). It describes an asset, which is a song, called *HTML5 Me, Baby* that can be sold by anyone who complies with the other restrictions set forth. A content creator who describes an asset this way on the web creates an incentive for their fan base to blog about and resell the content on their personal blogs. Imagine a WordPress plugin that allows you to review and resell your favorite bands songs directly from your blog. The artist is always guaranteed to get paid, regardless of which blog sells it or which PaySwarm Authority processes the payment. In this particular example, the asset provider has enabled their fans to take a 20% cut of the sale.

When a sale of the song above occurs, 80% of the sale price, or a minimum of $0.50 USD, is transferred to the asset provider. The PaySwarm Authority may add a fee for processing payment for the asset. A vendor may set a flat price for the song. For example, if the song is sold for $1.00, then $0.80 goes to The Webdevs (80% of final price restriction kicks in). If the song is sold for $0.60 USD, then $0.50 goes to The WebDevs ($0.50 USD minimum restriction kicks in). As you can see, the listing restrictions provide a great deal of power to the asset provider to specify exactly how their product should be sold.

Once the asset has been created, the developer can then use her private key to digitally sign the asset:

```
payswarm.sign(asset, {
publicKeyId: publicKey.id,
privateKeyPem: privateKey.privateKeyPem
}, function(err, signedAsset) {
// do something with the signed asset
});
```

Digitally signing the asset ensures that no one can change any of the information associated with it. This is important because, at a minimum, a content creator wouldn’t want to be removed from the list of people who should be paid when the asset is sold. The digital signature also guarantees, to a buyer, that the content creator did in fact describe the asset and its sale restrictions as seen.

The next step in preparing the asset for sale is to create a special identifier for the asset so that it can be accurately referenced by the listing. This identifier is called a [cryptographic hash](http://en.wikipedia.org/wiki/Cryptographic_hash) and is generated using the payswarm.js library’s `hash()`

function:

```
// generate a hash for the signed asset
payswarm.hash(signedAsset, function(err, assetHash) {
// do something with the signed asset hash
});
```

Once we have the signed asset and the signed asset hash, we can create the listing that will be used to purchase the asset.

## Creating a Listing

As mentioned earlier in this article, a listing is a description of the terms under which an asset is offered for sale. A listing, like an asset, is expressed in JSON-LD. The listing below specifies which license to associate with the asset being sold as well as who should get paid for the sale of the asset. It also specifies restrictions on certain payees, such as how much a PaySwarm Authority can charge for processing a payment. Pay particular attention to the comments above each line as they explain what the line does:

```
// create the listing
var listing = {
// the @context is a hint to a JSON-LD processor on how to interpret the
// key-value pairs in the document
'@context': 'https://w3id.org/payswarm/v1',
// this is the identifier for the listing
id: 'http://listings.dev.payswarm.com/mozhacks/html5-me-song#listing',
type: ['Listing'],
// the identity offering the item for sale is The WebDevs
vendor: 'https://dev.payswarm.com/i/the-webdevs',
payee: [{
type: 'Payee',
// payment should be deposited into this financial account
destination: 'https://dev.payswarm.com/i/the-webdevs/accounts/royalties',
// this is used to determine how fees are applied to the final price
payeeGroup: ['vendor'],
// the next 4 lines: Sell the song for $1.00
payeeRateType: 'FlatAmount',
payeeRate: '1.00',
currency: 'USD',
payeeApplyType: 'ApplyExclusively',
// this should be displayed for the line item in the digital receipt
comment: 'Payment to The Webdevs for creating the HTML5 Me, Baby song'
}],
// the next 6 lines: The payment processor cannot take more than 5% of
// the total sale price.
payeeRule : [{
type: 'PayeeRule',
payeeGroupPrefix: ['authority'],
payeeRateType: 'Percentage',
maximumPayeeRate: '5',
payeeApplyType: 'ApplyInclusively'
}],
// this is the ID of the asset being sold
asset: 'http://listings.dev.payswarm.com/mozhacks/html5-me-song#asset',
assetHash: assetHash,
// this is the license that should be associated with the asset upon sale
license: 'https://w3id.org/payswarm/licenses/personal-use',
licenseHash: 'urn:sha256:' +
'd9dcfb7b3ba057df52b99f777747e8fe0fc598a3bb364e3d3eb529f90d58e1b9',
// the offer of sale is only valid between these two times
validFrom: payswarm.w3cDate(validFrom),
validUntil: payswarm.w3cDate(validUntil)
};
```

The code above states that the song *HTML5 Me, Baby* is for sale for $1.00 and a payment processor can’t charge more than 5% of the total sale price in transaction processing fees. The song is licensed for personal use, with the [full text of the license](https://w3id.org/payswarm/licenses/personal-use) available at the provided URL. Once the listing has been created, it must be digitally signed:

```
payswarm.sign(listing, {
publicKeyId: cfg.publicKey.id,
privateKeyPem: cfg.publicKey.privateKeyPem
}, function(err, signedListing) {
// do something with the signed listing
});
```

The listing is digitally signed for the same reason that the asset is: to prevent tampering and for non-repudiation. Once both the asset and the listing are signed, they are ready to be published. This could be done by publishing them as two different documents or as a single document. The easiest way to publish them as a single document in JSON-LD is to use the ‘@graph’ keyword, which essentially states that you want to combine two independent objects into the same JSON-LD document.

```
var assetAndListing = {
'@context': 'https://w3id.org/payswarm/v1',
'@graph': [signedAsset, signedListing]
};
```

## Publishing an Asset and Listing

The final step in the publication process is to take the signed asset and listing document and publish it to the Web. Since PaySwarm is decentralized, we can publish our signed asset and listing to *any* website. Since the assets are digitally signed, the website doesn’t have to be protected by Transport Layer Security (TLS), more commonly known as HTTPS. The digital signature guarantees that no one can modify the data without invalidating the signature on the asset and listing. In the following example, we use the payswarm.js library’s `postJsonLd()`

function to upload the asset and listing to a public PaySwarm listing service.

```
var url = 'http://listings.dev.payswarm.com/mozhacks/html5-me-song';
payswarm.postJsonLd(url, assetAndListing, function(err, result) {
// if result is a 200, then your listing has been published
});
```

After the asset and listing have been uploaded, the asset can be purchased by any PaySwarm client. Note that while the asset and listing information was expressed as JSON-LD, it could have just as easily been published as HTML5+RDFa. PaySwarm Authorities are capable of interpreting both JSON-LD and RDFa. While we won’t go into the details in this blog post, a future blog post will address how to take the asset and listing Linked Data expressed above and publish it as HTML5+RDFa.

## Next: Purchasing an Asset

This is the second article in a three part series on developing PaySwarm-aware Web applications to engage in commerce. The next article will explain how to purchase the asset that was created in this tutorial and retrieve the digital receipt of the sale.

## About
[
Manu Sporny ](https://twitter.com/manusporny)

Founder of [Web Payments](http://www.w3.org/community/webpayments/) at W3C. Chair of [RDFa](http://rdfa.info/) and [JSON-LD](http://json-ld.org/) Working Groups. Lead editor of [PaySwarm](https://payswarm.com/), JSON-LD, and HTML5+RDFa specifications. Founded the company that created [Meritora](https://meritora.com/), the worlds first commercial PaySwarm payments processor. Leading the integration of finance and payments into the core architecture of the Web. Lots of standards-related work where the focus is on making the world a better place for all people. Other accounts: [@manusporny](https://twitter.com/manusporny), [+Manu Sporny](https://plus.google.com/102122664946994504971/about/), [LinkedIn](http://www.linkedin.com/in/manusporny/), and [blog](http://manu.sporny.org/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.