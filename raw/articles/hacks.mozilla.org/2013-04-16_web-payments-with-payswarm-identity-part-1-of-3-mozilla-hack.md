---
title: 'Web Payments with PaySwarm: Identity (part 1 of 3) – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2013/04/web-payments-with-payswarm-identity-part-1-of-3/
author: Manu Sporny
published: '2013-04-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## The Promise of Web Payments

The Web has fundamentally transformed the way we publish and interact with information. However, the way we reward people for creating that content has not changed. The Web’s foundation was not built to transmit and receive funds with the same ease as sending and receiving an email.

Making payments on the Web simpler and more accessible has more than superficial advantages. By taking the tools that have been traditionally only available to banks, Wall Street, and large corporations and making them available to everyone, we can reshape the world’s financial system. The goal is not to just simply enable one click payments, but also to enable crowdfunding innovation, help Web developers earn a living through the Web, boost funding rounds for world-changing start-ups, and more.

Whilst bringing new or powerful tools to the general public will breed competition and innovation, open Web payments can also bring about much more basic and societal changes. 2.5 billion people around the world don’t have bank accounts and thus have no ability to save money due to banking corruption and/or high fees. When a family has no way of saving for the future, it greatly limits their chances of pulling themselves out of poverty. The promise of Web payments is about more than just an exciting future, it is about a more egalitarian one.

So, how do we get from where we are today, to a future where sending an receiving funds on the Web is as easy as clicking a button?

## Web Payment Requirements

One of the primary drivers of innovation on the Web is that it is decentralized. You don’t have to ask permission to publish your creation. Open standards such as TCP/IP, HTTP, HTML, CSS, JavaScript, and JSON ensure interoperability between applications. Thus, a solution for payments on the Web must have at least the following traits:

- It must be decentralized.
- It must be an open, patent and royalty-free standard.
- It must be designed to work with Web architecture like URLs, HTTP, and other Web standards.
- It must allow anyone to implement the standard and interoperate with others that implement the standard.

In addition to these basic characteristics of a successful Web technology, a successful Web Payments technology must also do the following:

- It must enable choice among customers, vendors, and payment processors, in order to drive healthy market competition.
- It must be extensible in a decentralized way, allowing application-specific extensions to the core protocol without coordination.
- It must be flexible enough to perform payments as well as support higher order economic behaviors like crowdfunding and executing legal contracts.
- It must be secure, using the latest security best practices to protect the entire system from attack.
- It must be currency agnostic, supporting not only the US Dollar, the Euro, and the Japanese Yen, but also supporting virtual currencies like Bitcoin and Ven.
- It must be easy to develop for and integrate into the Web.

Fortunately, the [Web Payments group](http://www.w3.org/community/webpayments/) at the [World Wide Web Consortium](http://www.w3.org/) (W3C) has created a set of specifications called [PaySwarm](https://payswarm.com/) that addresses all of the requirements listed above. The group is currently in contact with Mozilla and is trying to converge with the [mozPay() API](https://wiki.mozilla.org/WebAPI/WebPayment#Proposers) as well as [Persona](http://www.mozilla.org/en-US/persona/) to provide a truly excellent Web Payments experience. There is even a [commercial launch of the technology](http://blog.meritora.com/launch/) using real money, which means you can use it to send and receive funds today.

This is the first blog post in a three part series that will explore the PaySwarm specifications and demonstrate, using code examples and video, how to build a fully functional PaySwarm client in Node.js.

## Decentralized Identity

A [decentralized](http://www.soa-world.de/echelon/2011/09/the-decentralized-web-movement.html) payment system for the Web means that, ultimately, the identity mechanism must be decentralized as well. There are a number of identity solutions today that are decentralized. OpenID, WebID, Web Keys, and BrowserID/Persona are among some of the more well-known, decentralized identity mechanisms that are designed for the Web. Identity for Web Payments brings in an additional set of requirements on top of the normal set of requirements for a Web identity solution. The following is a brief list of these requirements:

- It must be decentralized.
- It must support discoverability by using a resolvable address, like a URL or email address.
- It must support, with authorization, arbitrary machine-readable information being attached to the identity by 3rd parties.
- It must be able to provide both public and private data to external sites, based on who is accessing the resource.
- It must provide a secure digital signature and encryption mechanism.

The solution we ended up settling on is called [Web Keys](https://payswarm.com/specs/source/web-keys/). It enables secure, decentralized, discoverable, controlled access to arbitrary machine-readable information associated with an identity. This identity mechanism and the functionality it enables is at the heart of the PaySwarm work.

## Web Keys

For reasons that we don’t have time to go into in this blog post, OpenID, WebID, and OAuth were considered but ultimately did not make the cut because they don’t provide at least one of the features above. At the time, BrowserID, which was later rebranded as Persona, was still too early in the design stage to consider as a viable solution. The Web Payments group is currently working with the Persona team to see if all of the features above could be integrated into Persona to support Web Payments, but it is not certain that it will happen.

In the end, we had to create a minimal identity solution for Web Payments because one did not exist that met all of the requirements above. So, let’s dive into using the Web Keys technology to establish an identity online for the purposes of making decentralized Web Payments.

This tutorial will use code from the [payswarm.js node module](https://github.com/digitalbazaar/payswarm.js). Specifically, it will use code snippets from the [Web Key registration example](https://github.com/digitalbazaar/payswarm.js/blob/8ceff433cb7d30fefbb76009634aa2ca3503108c/examples/register-new-key.js). The tutorial will also use the [PaySwarm Developer Sandbox](https://dev.payswarm.com/) as our Web Key host and payment processor.

The following video shows what we will be building throughout the rest of this tutorial:

## Generating a Key

The Web Keys specification is built on top of a technology called [public-key cryptography](http://en.wikipedia.org/wiki/Public-key_cryptography). We don’t have time to go into how this technology works in detail in this blog post, so what follows is a quick overview for those that are unfamiliar with the technology.

Public key cryptography is used to secure traffic on the Web. If you have ever seen a padlock icon when doing a purchase online, you’re using public key cryptography. When you generate these *keys*, you are given two of them: a public key and a private key. Together the keys can be used to do two major operations that are important in Web Payments. The first is that the private key can be used to digitally sign a purchase request. The public key can be used to verify the digital signature on the purchase request, proving that you, and only you, wish to make a purchase. The second is that the public key can be used to encrypt information so that only the holder of the private key can read that information. Together these keys can be used to prove your identity online to others and to encrypt messages sent to you so that only you can read them.

To generate the pair of keys in PaySwarm, you can do the following:

```
var payswarm = require('payswarm-client');
...
payswarm.createKeyPair({keySize: 2048}, function(err, pair) {
if(err) {
console.log('Oops, something went wrong:', err);
}
else {
var publicKeyPem = pair.publicKey;
var privateKeyPem = pair.privateKey;
...
}
});
```

In the code above, the PaySwarm library’s `createKeyPair()`

function is used to create a 2048-bit key pair. The more bits that are used for the key pair, the harder it is to do a [brute-force attack](http://en.wikipedia.org/wiki/Brute-force_attack) against it. At present (April 2013), a key length of 2048 bits is considered very secure for PaySwarm transactions. You should never use a key length below 2048 bits; it should be rejected by the financial network. Once the key pair is created, both the public key and the private key are returned to you. It is up to the application to then store the keys. The private key must be stored very securely, preferably encrypting the key with a long passphrase before writing it to disk. The public key should be published in a way that other people can use it to verify your digital signatures and send encrypted data to you that only you will be able to read. The process of publishing the public key to the web will be covered in the next section.

## Registering a Key

The Web Keys specification details how an application can associate a public key with an identity. Associating a Web Key with an identity consists of a multi-step process:

- Discover the Web Key server’s key registration base URL.
- Generate a key registration URL.
- Register the key via a web browser.

The steps above are demonstrated in the code snippet below:

```
async.waterfall([
...
function(callback) {
// Step #1: Fetch the Web Keys endpoint from the PaySwarm Authority.
payswarm.getWebKeysConfig('dev.payswarm.com', callback);
}, function(endpoints, callback) {
// Step #2: Generate the key registration URL
var registrationUrl = URL.parse(endpoints.publicKeyService, true, true);
registrationUrl.query['public-key'] = publicKeyPem;
registrationUrl.query['response-nonce'] =
new Date().getTime().toString(16);
delete registrationUrl.search;
registrationUrl = URL.format(registrationUrl);
callback(null, registrationUrl)
},
function(registrationUrl, callback) {
// Step #3: Register the key via a web browser.
console.log('Register your key here: ', registrationUrl);
...
```

A PaySwarm client running the code above will fetch the Web Keys configuration for the `dev.payswarm.com`

site first. The URL used when retrieving the Web Keys configuration via the `getWebKeysConfig()`

function will be [https://dev.payswarm.com/.well-known/web-keys](https://dev.payswarm.com/.well-known/web-keys). The result is a [JSON-LD](http://json-ld.org/) document, which can be used as a JSON document. The JSON key that holds the registration endpoint is `publicKeyService`

. A registration URL is then constructed by adding URL parameters to the registration endpoint URL. First, the public key that was generated by the application is added. Then, a single-use response [nonce](http://en.wikipedia.org/wiki/Cryptographic_nonce) is added, which is used to prevent replay attacks. The response from the server will include the response nonce, so be sure to store it somewhere. It is very important that the response nonce is tracked by the application and never used more than once. If an application detects that a response nonce has been used more than once when receiving a message from the server, you may be under attack and must ignore the message. Messages in PaySwarm are transient in nature, so nonces may only need to be stored for a limited period of time, simplifying certain implementations.

What the PaySwarm Authority does when the browser goes to the registration URL is implementation specific. The only requirement is that it provides a permanent URL location for the public key and the URL for the owner of the public key being registered. Note that the URL for the owner must also be deferenceable, so it can provide information that indicates the owner does, in fact, own the public key. The response will be encrypted using the public key provided and can only be decrypted by the application’s private key. The next section will cover handling the registration response from the PaySwarm Authority.

## The Registration Response

The last step in registering a Web Key is receiving the encrypted response from the PaySwarm Authority. Finalizing the registration of a Web Key consists of the following two steps:

- Receive the encrypted key registration response.
- Decode the key registration response.

The steps above are demonstrated in the code snippet below:

```
async.waterfall([
...
// step #1: receive the encrypted key registration response
...
function(encryptedMessage, callback) {
// step #2: decode the key registration response
payswarm.decrypt(encryptedMessage, {privateKey: privateKeyPem}, callback);
},
function(message, callback) {
var publicKeyUrl = message.publicKey;
var publicKeyOwnerUrl = message.owner;
var financialAccountUrl = message.destination;
callback();
},
...
```

When registering a public key, the application will ask you to go to a URL on your PaySwarm Authority. If your application is a console application, the final step of the registration process will provide an encrypted message that you can copy and paste into your application. If your application is a Web application, you can provide a callback URL that the encrypted message will be sent to after registration. That encrypted message is the input to the JavaScript code above. The PaySwarm library uses a function called `decrypt()`

that will take the encrypted message and the application’s private key, which was generated earlier in the tutorial, and provide the unencrypted message that was sent to you by the PaySwarm Authority.

The unencrypted message will contain, at a minimum, the URL for the public key and the identity URL for the owner of the public key. The Web Payments specification also requires that a financial account is associated with the public key, which is useful when you need to tell another application where to send funds. Once the application has this information, it should store it in a safe place, preferably password protected, along with the private key data.

## Browser-based Web Key Registration

This tutorial covered the basics of creating a console-based Web Key client for the purposes of registering a public key. Typically a Web Key client will be built into software running on a public website that is accessed using a Web browser. An example of the experience provided by a purely browser-based Web Key workflow is shown below:

## Next: Listing an Asset for Sale

This is the first article in a three part series on using the PaySwarm specifications which can be used to send and receive funds via the Web in a decentralized way. The next article in the series will explain how to create an Asset, such as an article, song, or movie, and list it for sale on the Web. The beauty of PaySwarm is that a customer on your site does not need to use the same payment processor as you, just as you don’t need to care which payment processor the customer uses. With PaySwarm, the money just flows to the appropriate place.

## About
[
Manu Sporny ](https://twitter.com/manusporny)

Founder of [Web Payments](http://www.w3.org/community/webpayments/) at W3C. Chair of [RDFa](http://rdfa.info/) and [JSON-LD](http://json-ld.org/) Working Groups. Lead editor of [PaySwarm](https://payswarm.com/), JSON-LD, and HTML5+RDFa specifications. Founded the company that created [Meritora](https://meritora.com/), the worlds first commercial PaySwarm payments processor. Leading the integration of finance and payments into the core architecture of the Web. Lots of standards-related work where the focus is on making the world a better place for all people. Other accounts: [@manusporny](https://twitter.com/manusporny), [+Manu Sporny](https://plus.google.com/102122664946994504971/about/), [LinkedIn](http://www.linkedin.com/in/manusporny/), and [blog](http://manu.sporny.org/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

Manu SpornyApril 16th, 2013 at 10:13Manu SpornyApril 16th, 2013 at 10:36