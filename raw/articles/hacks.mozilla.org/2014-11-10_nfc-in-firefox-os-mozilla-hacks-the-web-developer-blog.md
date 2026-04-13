---
title: NFC in Firefox OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/11/nfc-in-firefox-os/
author: Sandip Kamat
published: '2014-11-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox OS is being developed in an open collaboration with Mozilla’s partners and community. In that spirit, and over the course of over a year, Mozilla and Deutsche Telekom (DT) teams worked closely together to develop a platform-level support for NFC within Firefox OS. During that time, both teams had regular product and engineering meet-ups for the end-to-end development cycle.

From proposing the NFC API, to defining the overall architecture, to prototyping and completing a production-level implementation on shipping products, this collaboration model worked so well that it really helped showcase the power of the “open” (Open technology and Open contribution model) for pushing the web forward. After all, this is exactly what Mozilla and Firefox OS stand for.

In this post, we describe a few basics around Firefox OS NFC implementation.

## NFC Roadmap

Currently in release 2.0, Firefox OS supports NFC based sharing of contents (contacts, images, videos, URLs), as well as wirelessly reading information stored in NFC enabled tags (tag reading). Our sharing use cases are compatible with NFC enabled devices from other OSes like Android/Windows, so sharing of these contents across these devices would work. Our NFC API (first introduced in v1.3) has been put to use for these sharing use cases in v2.0 with core apps.

The [Overall B2G roadmap is available on the wiki](https://wiki.mozilla.org/B2G/Roadmap).

## WebNFC API

The Firefox NFC APIs allow Peer to Peer (P2P) communication between any 2 devices that support NFC Data Type Exchange format (NDEF). NFC passive tags that can present themselves as NDEF compatible tags can also be read and written to. Firefox OS’ NFC implementation is currently for certified applications only, but as stated above, will be opened to marketplace applications as the API is developed to cover more use cases and data formats.

### An example using this API

The following does P2P communications between 2 NFC devices (from the [NFC API docs on MDN](https://developer.mozilla.org/en-US/docs/Web/API/NFC_API)):

```
// Utility Function for UTF-8 string conversion to Uint8Array.
// Or ideally, simply add this to your webapp HTML to use NfcUtils:
// <script defer src="shared/js/nfc_utils.js"></script>
function fromUTF8(str) {
if (!str) {
return null;
}
var enc = new TextEncoder('utf-8');
return enc.encode(str);
}
var tnf = 1; // NFC Forum Well Known type
var type = new Uint8Array(fromUTF8("U")); // URL type
var id = new Uint8Array(fromUTF8("")); // id
var payload = new Uint8Array(fromUTF8("u0003mozilla.org")); // URL data, with a record prefix 0x3 replacing http://
var ndefRecords = [new MozNDEFRecord(tnf, type, id, payload)];
var nfcdom = window.navigator.mozNfc;
nfcdom.onpeerready = function(event) {
// event.detail is a session token
var nfcPeer = navigator.mozNfc.getNFCPeer(event.detail);
var req = nfcpeer.sendNDEF(ndefRecords); // push NDEF message to other NFC device.
req.onsuccess = function(e) {
console.log("Successfully pushed P2P message");
};
req.onerror = function(e) {
console.log("P2P push failed!");
};
};
```

More such examples that ship with Firefox OS can be found in [Using the NCF API](https://developer.mozilla.org/en-US/docs/Web/API/NFC_API/Using_the_NFC_API).

### Current Supported data types

The WebNFC API currently supports NFC Data Exchange Format (NDEF). There are some future plans for Non-NDEF types. From the example above, it is 4 fields, which is defined with 3 optional Uint8Array data types. The TNF and type are used to route the message to the appropriate registered web application(s).

```
[Constructor(octet tnf, optional Uint8Array type, optional Uint8Array id, optional Uint8Array payload)]
interface MozNDEFRecord
{
/**
* Type Name Field (3-bits) - Specifies the NDEF record type in general.
* tnf_empty: 0x00
* tnf_well_known: 0x01
* tnf_mime_media: 0x02
* tnf_absolute_uri: 0x03
* tnf_external type: 0x04
* tnf_unknown: 0x05
* tnf_unchanged: 0x06
* tnf_reserved: 0x07
*/
[Constant]
readonly attribute octet tnf;
/**
* type - Describes the content of the payload. This can be a mime type.
*/
[Constant]
readonly attribute Uint8Array? type;
/**
* id - Identifier is application dependent.
*/
[Constant]
readonly attribute Uint8Array? id;
/**
* payload - Binary data blob. The meaning of this field is application
* dependent.
*/
[Constant]
readonly attribute Uint8Array? payload;
};
```

Note, in upcoming Firefox OS releases, we will be updating the data types slightly to make TNF an enum type instead of an octet.

### Mozilla’s Flame device supports NFC, more devices coming

Our [Flame device](https://developer.mozilla.org/en-US/Firefox_OS/Developer_phone_guide/Flame) supports NFC and we are expecting more commercial devices from our partners soon. Flame device supports NFC chipset from NXP (PN547C2).

## Videos

Here is a demo video of some of the NFC sharing features based on Firefox OS:

Core Apps In Flame device that use NFC:

- Gallery
- Video
- Music
- Settings
- System browser

## A sample 3rd party App

Here is an app that Mozillian [Dietrich Ayala](https://twitter.com/dietrich) put together using the NFC tag reading API. BikeCommute is an app that registers an NFC tag to track bike commuters at the Mozilla Portland office. The app is running on a Nexus 4 with Firefox OS 2.2, and is built with Famo.us for UI and PouchDB for data storage and syncing to a remote CouchDB. Currently, the app just reads the user’s email address from a text record written to the tag.

The next version will add support for running the app on users’ phones, using a local contact (user) instead of a plain text record, and being able to configure the NFC tag from their own device. The plan is to develop leaderboards from the CouchDB data and Mozillians.org integration so we can deploy and compete with other offices and Mozillians everywhere! The source [code is available on GitHub](https://github.com/autonome/bikecommute) and pull requests welcome!

Here is a Video demo of this app in action:

## More NFC documentation

- For Developers: NFC
[API details](https://developer.mozilla.org/en-US/docs/Web/API/NFC_API) [GSMA API 6.0 Compliance of FxOS (in progress)](http://goo.gl/93wS5J)- For OEMs:
[NFC Compatibility doc](https://docs.google.com/a/mozilla.com/document/d/1XFwZrqW9LSLfdCcrkdd8WY8C8aH1jB8bjUcq4KPD3IE/)

So, there it is!

We are really excited to introduce this new addition to growing list of APIs and features in Firefox OS! We hope developers will take full advantage of all that NFC enables by way of device-to-device sharing and also services like contactless payment planned in future.

## When can developers start using this API?

Currently this API is available for [certified apps](https://developer.mozilla.org/en-US/Firefox_OS/Security/Application_security). We can’t wait to finish the work to make this API available for privileged apps, so all of you developers can take advantage of this. If you wish to follow along or jump in and help out, feel free to track [Bug 1042851](https://bugzilla.mozilla.org/show_bug.cgi?id=1042851). We are targeting to finish the work for the next release v2.2.

## Next in NFC

In upcoming releases, with the help of our partners, we are focusing on expanding the NFC coverage for supporting Secure elements and services like NFC based payments. More on that in a separate post later. Please stay tuned.

Here’s to the open web!

## About
[
Sandip Kamat ](https://twitter.com/sankam)

Sandip Kamat is part of Mozilla's Connected Devices Product Management team. He has spent most of his career in building mobile technologies and products. Prior to joining Mozilla, he worked at Motorola Mobility (later, owned by Google) and Siemens Mobile. He is an alum of IIT Madras and UCSD (Rady). He is passionate about bringing cutting edge technologies to everyday people to make their lives meaningfully better.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 9 comments

Steve LeeNovember 10th, 2014 at 11:42Sandip KamatNovember 10th, 2014 at 13:22Garner LeeNovember 10th, 2014 at 16:59Garner LeeNovember 10th, 2014 at 17:01Steve LeeNovember 11th, 2014 at 02:41Sandip KamatNovember 11th, 2014 at 18:58Moinuddin ChinuNovember 13th, 2014 at 08:00CharlesNovember 18th, 2014 at 04:29Garner LeeNovember 19th, 2014 at 14:51