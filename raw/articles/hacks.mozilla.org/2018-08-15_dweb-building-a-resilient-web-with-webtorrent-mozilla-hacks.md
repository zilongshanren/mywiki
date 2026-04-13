---
title: 'Dweb: Building a Resilient Web with WebTorrent – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2018/08/dweb-building-a-resilient-web-with-webtorrent/
author: Feross Aboukhadijeh
published: '2018-08-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*In this series we are covering projects that explore what is possible when the web becomes decentralized or distributed. These projects aren’t affiliated with Mozilla, and some of them rewrite the rules of how we think about a web browser. What they have in common: These projects are open source, and open for participation, and share Mozilla’s mission to keep the web open and accessible for all.*

The web is healthy when the financial cost of self-expression isn’t a barrier. In this installment of the Dweb series we’ll learn about WebTorrent – an implementation of the [BitTorrent protocol](http://www.bittorrent.org/beps/bep_0003.html) that runs in web browsers. This approach to serving files means that websites can scale with as many users as are simultaneously viewing the website – removing the cost of running centralized servers at data centers. The post is written by Feross Aboukhadijeh, the creator of [WebTorrent](https://webtorrent.io/), co-founder of PeerCDN and a prolific NPM module author… 225 modules at last count! –Dietrich Ayala

## What is WebTorrent?

WebTorrent is the first torrent client that works in the browser. It’s written completely in JavaScript – the language of the web – and uses [WebRTC](https://webrtc.org/) for true peer-to-peer transport. No browser plugin, extension, or installation is required.

Using open web standards, WebTorrent connects website users together to form a distributed, decentralized browser-to-browser network for efficient file transfer. The more people use a WebTorrent-powered website, the faster and more resilient it becomes.

## Architecture

The WebTorrent protocol works just like BitTorrent protocol, except it uses WebRTC instead of TCP or uTP as the transport protocol.

In order to support WebRTC’s connection model, we made a few changes to the tracker protocol. Therefore, a browser-based WebTorrent client or “web peer” can only connect to other clients that support WebTorrent/WebRTC.

Once peers are connected, the wire protocol used to communicate is exactly the same as in normal BitTorrent. This should make it easy for existing popular torrent clients like [Transmission](https://transmissionbt.com/), and [uTorrent](https://www.utorrent.com/) to add support for WebTorrent. [Vuze](https://www.vuze.com/) already has support for WebTorrent!

## Getting Started

It only takes a few lines of code to download a torrent in the browser!

To start using WebTorrent, simply include the `webtorrent.min.js`

script on your page. You can download the script from the [WebTorrent website](https://webtorrent.io/intro) or [link to the CDN copy](https://cdn.jsdelivr.net/webtorrent/latest/webtorrent.min.js).

```
<script src="webtorrent.min.js"></script>
```


This provides a `WebTorrent`

function on the `window`

object. There is also an

[npm package](https://www.npmjs.com/package/webtorrent) available.

```
var client = new WebTorrent()
// Sintel, a free, Creative Commons movie
var torrentId = 'magnet:...' // Real torrent ids are much longer.
var torrent = client.add(torrentId)
torrent.on('ready', () => {
// Torrents can contain many files. Let's use the .mp4 file
var file = torrent.files.find(file => file.name.endsWith('.mp4'))
// Display the file by adding it to the DOM.
// Supports video, audio, image files, and more!
file.appendTo('body')
})
```


That’s it! Now you’ll see the torrent streaming into a `<video width="300" height="150">`

tag in the webpage!

## Learn more

You can learn more at [webtorrent.io](https://webtorrent.io/), or by asking a question in #webtorrent on Freenode IRC or on [Gitter](https://gitter.im/webtorrent/webtorrent). We’re looking for more people who can answer questions and help people with issues on the GitHub issue tracker. If you’re a friendly, helpful person and want an excuse to dig deeper into the torrent protocol or WebRTC, then this is your chance!



## About
[
Feross Aboukhadijeh ](https://feross.org)

Feross writes popular open source software including [WebTorrent](https://webtorrent.io), [StandardJS](https://standardjs.com), and hundreds of Node.js packages (collectively 200+ million downloads per month). He recently released a fun site called [BitMidi](https://bitmidi.com) that curates MIDI files for your listening pleasure! His open source work is supported by generous donors on [Patreon](https://www.patreon.com/feross).

## 14 comments

Valentin C.August 15th, 2018 at 23:36Feross AboukhadijehAugust 15th, 2018 at 23:49Valentin C.August 16th, 2018 at 05:02Feross AboukhadijehAugust 16th, 2018 at 11:01Richie SikraAugust 16th, 2018 at 09:31Richie SikraAugust 16th, 2018 at 09:44Feross AboukhadijehAugust 16th, 2018 at 11:07Tailor VijayAugust 16th, 2018 at 12:00Feross AboukhadijehAugust 16th, 2018 at 13:00Danyl StrypeAugust 29th, 2018 at 10:50Feross AboukhadijehAugust 29th, 2018 at 12:31grSeptember 1st, 2018 at 03:31Feross AboukhadijehSeptember 1st, 2018 at 15:27Abby NionSeptember 11th, 2018 at 11:16