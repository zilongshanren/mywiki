---
title: 'Dweb: Building Cooperation and Trust into the Web with IPFS – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2018/08/dweb-building-cooperation-and-trust-into-the-web-with-ipfs/
author: Kyle Drake
published: '2018-08-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*In this series we are covering projects that explore what is possible when the web becomes decentralized or distributed. These projects aren’t affiliated with Mozilla, and some of them rewrite the rules of how we think about a web browser. What they have in common: These projects are open source, and open for participation, and share Mozilla’s mission to keep the web open and accessible for all.*

*Some projects start small, aiming for incremental improvements. Others start with a grand vision, leapfrogging today’s problems by architecting an idealized world. The InterPlanetary File System (IPFS) is definitely the latter – attempting to replace HTTP entirely, with a network layer that has scale, trust, and anti-DDOS measures all built into the protocol. It’s our pleasure to have an introduction to IPFS today from Kyle Drake, the founder of Neocities and Marcin Rataj, the creator of IPFS Companion, both on the IPFS team at Protocol Labs -Dietrich Ayala*

## IPFS – The InterPlanetary File System

We’re a team of people all over the world working on IPFS, an implementation of the distributed web that seeks to replace [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) with a new protocol that is powered by individuals on the internet. The goal of IPFS is to “re-decentralize” the web by replacing the location-oriented HTTP with a content-oriented protocol that does not require trust of third parties. This allows for websites and web apps to be “served” by any computer on the internet with IPFS support, without requiring servers to be run by the original content creator. IPFS and the distributed web unmoor information from physical location and singular distribution, ultimately creating a more affordable, equal, available, faster, and less censorable web.

IPFS aims for a “distributed” or “logically decentralized” design. IPFS consists of a network of nodes, which help each other find data using a content hash via a [Distributed Hash Table (DHT)](https://en.wikipedia.org/wiki/Distributed_hash_table). The result is that all nodes help find and serve web sites, and even if the original provider of the site goes down, you can still load it as long as one other computer in the network has a copy of it. The web becomes empowered by individuals, rather than depending on the large organizations that can afford to build large content delivery networks and serve a lot of traffic.

The IPFS stack is an abstraction built on top of [IPLD](https://ipld.io) and [libp2p](https://libp2p.io):

## Hello World

We have a reference implementation in Go ([go-ipfs](https://github.com/ipfs/go-ipfs)) and a constantly improving one in Javascript ([js-ipfs](https://github.com/ipfs/js-ipfs)). There is also a long list of API clients for other languages.

Thanks to the JS implementation, using IPFS in web development is extremely easy. The following code snippet…

- Starts an IPFS node
- Adds some data to IPFS
- Obtains the Content IDentifier (CID) for it
- Reads that data back from IPFS using the CID

```
<br /><script src="https://unpkg.com/ipfs/dist/index.min.js"></script>
Open Console (Ctrl+Shift+K)
<script>
const ipfs = new Ipfs()
const data = 'Hello from IPFS, <YOUR NAME HERE>!'
// Once the ipfs node is ready
ipfs.once('ready', async () => {
console.log('IPFS node is ready! Current version: ' + (await ipfs.id()).agentVersion)
// convert your data to a Buffer and add it to IPFS
console.log('Data to be published: ' + data)
const files = await ipfs.files.add(ipfs.types.Buffer.from(data))
// 'hash', known as CID, is a string uniquely addressing the data
// and can be used to get it again. 'files' is an array because
// 'add' supports multiple additions, but we only added one entry
const cid = files[0].hash
console.log('Published under CID: ' + cid)
// read data back from IPFS: CID is the only identifier you need!
const dataFromIpfs = await ipfs.files.cat(cid)
console.log('Read back from IPFS: ' + String(dataFromIpfs))
// Compatibility layer: HTTP gateway
console.log('Bonus: open at one of public HTTP gateways: https://ipfs.io/ipfs/' + cid)
})
</script>
```


That’s it!

Before diving deeper, let’s answer key questions:

### Who else can access it?

Everyone with the CID can access it. Sensitive files should be encrypted before publishing.

### How long will this content exist? Under what circumstances will it go away? How does one remove it?

The permanence of content-addressed data in IPFS is intrinsically bound to the active participation of peers interested in providing it to others. It is impossible to remove data from other peers but if no peer is keeping it alive, it will be “forgotten” by the swarm.

The public HTTP gateway will keep the data available for a few hours — if you want to ensure long term availability make sure to pin important data at nodes you control. Try [IPFS Cluster](http://cluster.ipfs.io): a stand-alone application and a CLI client to allocate, replicate and track pins across a cluster of IPFS daemons.

## Developer Quick Start

You can experiment with [js-ipfs](https://github.com/ipfs/js-ipfs/) to make simple browser apps. If you want to run an IPFS server you can [install go-ipfs](https://ipfs.io), or [run a cluster](http://cluster.ipfs.io), as we mentioned above.

There is a growing list of [examples](https://github.com/ipfs/js-ipfs/tree/master/examples/), and make sure to see the [bi-directional file exchange demo](https://github.com/ipfs/js-ipfs/tree/master/examples/exchange-files-in-browser) built with js-ipfs.

You can add IPFS to the browser by installing the [IPFS Companion extension](https://addons.mozilla.org/en-US/firefox/addon/ipfs-companion/) for Firefox.

## Learn More

Learn about IPFS concepts by visiting our documentation website at [https://docs.ipfs.io](https://docs.ipfs.io).

Readers can participate by improving documentation, visiting [https://ipfs.io](https://ipfs.io), developing distributed web apps and sites with IPFS, and exploring and contributing to [our git repos](https://github.com/ipfs) and various things built by the [community](https://awesome.ipfs.io).

A great place to ask questions is our friendly community forum: [https://discuss.ipfs.io](https://discuss.ipfs.io).

We also have an IRC channel, #ipfs on Freenode (or #freenode_#ipfs:matrix.org on Matrix). Join us!

## About Kyle Drake

Kyle Drake is a developer that is currently working on IPFS at Protocol Labs.

## About Marcin Rataj

Marcin Rataj is a carbon based lifeform working on IPFS in Web Browsers at Protocol Labs.

## 2 comments

StrypeySeptember 7th, 2018 at 10:31Marcin RatajSeptember 15th, 2018 at 11:21