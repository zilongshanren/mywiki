---
title: 'Dweb: Serving the Web from the Browser with Beaker – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2018/08/dweb-serving-the-web-from-the-browser-with-beaker/
author: Tara Vancil
published: '2018-08-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*In this series we are covering projects that explore what is possible when the web becomes decentralized or distributed. These projects aren’t affiliated with Mozilla, and some of them rewrite the rules of how we think about a web browser. What they have in common: These projects are open source, and open for participation, and share Mozilla’s mission to keep the web open and accessible for all.*

So far we’ve covered [distributed social feeds](https://hacks.mozilla.org/2018/08/dweb-social-feeds-with-secure-scuttlebutt/) and [sharing files in a decentralized way](https://hacks.mozilla.org/2018/08/dweb-building-a-resilient-web-with-webtorrent/) with some new tools for developers. Today we’d like to introduce something a bit different: Imagine what an *entire browser experience* would be like if the web was distributed… Beaker browser does exactly this! Beaker is a big vision from a team who are proving out the distributed web from top to bottom. Please enjoy this post from Beaker co-creator Tara Vancil. – Dietrich Ayala

## Blue Link Labs and Beaker

We’re [Blue Link Labs](https://bluelinklabs.com), a team of three working to improve the Web with the [Dat protocol](https://datproject.org) and an experimental peer-to-peer browser called [Beaker](https://beakerbrowser.com).

![Blue Link Labs team](../../assets/fefb1a2fc835665d.jpg)


We work on Beaker because publishing and sharing is core to the Web’s ethos, yet to publish your own website or even just share a document, you need to know how to run a server, or be able to pay someone to do it for you.

So we asked ourselves, “What if you could share a website directly from your browser?”

Peer-to-peer protocols like `dat://`

make it possible for regular user devices to host content, so we use `dat://`

in Beaker to enable publishing from the browser, where instead of using a server, a website’s author and its visitors help host its files. It’s kind of like BitTorrent, but for websites!

## Architecture

Beaker uses a distributed peer-to-peer network to publish websites and datasets (sometimes we call them “dats”).

`dat://`

websites are addressed with a public key as the URL, and each piece of

data added to a `dat://`

website is appended to a signed log. Visitors to a `dat://`


website find each other with a tracker or [DHT](https://en.wikipedia.org/wiki/Distributed_hash_table), then sync the data between each other, acting both as downloaders and uploaders, and checking that the data hasn’t been tampered with in transit.

At its core, a `dat://`

website isn’t much different than an https:// website — it’s a collection of files and folders that a browser interprets according to Web standards. But `dat://`

websites are special in Beaker because we’ve added [peer-to-peer Web APIs](https://beakerbrowser.com/docs/apis) so developers can do things like read, write, and watch `dat://`

files and build peer-to-peer Web apps.

## Create a P2P Website

Beaker makes it easy for anyone to create a new `dat://`

website with one click (see our [tour](https://beakerbrowser.com/docs/tour)). If you’re familiar with HTML, CSS, or JavaScript (even just a little bit!) then you’re ready to publish your first `dat://`

website.

Developers can get started by checking out our [API documentation](https://beakerbrowser.com/docs/apis) or reading through our [guides](https://beakerbrowser.com/docs/guides).

This example shows a website editing *itself* to create and save a new JSON file. While this example is contrived, it demonstrates a common pattern for storing data, user profiles, etc. in a `dat://`

website—instead of application data being sent away to a server, it can be stored in the website itself!

```
// index.html
Submit message
<script src="index.js"></script>
```


```
// index.js
// first get an instance of the website's files
var files = new DatArchive(window.location)
document.getElementById('create-json-button').addEventListener('click', saveMessage)
async function saveMessage () {
var timestamp = Date.now()
var filename = timestamp + '.json'
var content = {
timestamp,
message: document.getElementById('message').value
}
// write the message to a JSON file
// this file can be read later using the DatArchive.readFile API
await files.writeFile(filename, JSON.stringify(content))
}
```


## Learn More

We’re always excited to see what people build with `dat://`

and Beaker. We especially love seeing when someone builds a personal site or blog, or when they experiment with Beaker’s APIs to build an app.

There’s lots to explore on the peer-to-peer Web!

[Take a tour of Beaker](https://beakerbrowser.com/docs/tour)[Beaker documentation](https://beakerbrowser.com/docs)[p2pforever.org](http://p2pforever.org)– a humble hub of peer-to-peer Web resources[Beaker on GitHub](https://github.com/beakerbrowser/beaker)

## About Tara Vancil

Tara is the co-creator of the [Beaker browser](https://beakerbrowser.com). Previously she worked at Cloudflare and participated in [the Recurse Center](https://recurse.com).

## 8 comments

IbonAugust 23rd, 2018 at 03:53Pseudo BlümAugust 23rd, 2018 at 13:04Tara VancilAugust 29th, 2018 at 10:49ThorstenAugust 28th, 2018 at 06:31Tara VancilAugust 29th, 2018 at 10:17JohnSeptember 10th, 2018 at 10:32Tara VancilSeptember 10th, 2018 at 13:09pawelSeptember 17th, 2018 at 01:09