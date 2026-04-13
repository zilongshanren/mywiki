---
title: 'Dweb: Creating Decentralized Organizations with Aragon – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2018/09/aragon-ethereum-dweb/
author: Luis Cuende
published: '2018-09-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*In the Dweb series, we are covering projects that explore what is possible when the web becomes decentralized or distributed. These projects aren’t affiliated with Mozilla, and some of them rewrite the rules of how we think about a web browser. What they have in common: These projects are open source and open for participation, and they share Mozilla’s mission to keep the web open and accessible for all.*

*While many of the projects we’ve covered build on the web as we know it or operate like the browsers we’re familiar with, the Aragon project has a broader vision: Give people the tools to build their own autonomous organizations with social mores codified in smart contracts. I hope you enjoy this introduction to Aragon from project co-founder Luis Cuende.
*

*– Dietrich Ayala*

## Introducing Aragon

I’m Luis. I cofounded [Aragon](https://aragon.org), which allows for the creation of decentralized organizations. The principles of Aragon are embodied in the [Aragon Manifesto](https://blog.aragon.org/the-aragon-manifesto-4a21212eac03/), and its format was inspired by the [Mozilla Manifesto!](https://www.mozilla.org/en-US/about/manifesto/)

Here’s a quick summary.

- We are in a key moment in history: Technology either
**oppresses**or**liberates**us. - That outcome will depend on
**common goods being governed by the community**, and not just nation states or corporate conglomerates. - For that to happen, we need technology that allows for
**decentralized governance**. - Thanks to crypto, decentralized governance can provide new means of organization that
**don’t entail violence or surveillance**, therefore providing more**freedom**to the individual and increasing**fairness**.

With Aragon, developers can create new apps, such as voting mechanisms, that use smart contracts to leverage decentralized governance and allow peers to control resources like funds, membership, and code repos.

Aragon is built on Ethereum, which is a blockchain for [smart contracts.](https://auth0.com/blog/an-introduction-to-ethereum-and-smart-contracts-part-2/) Smart contracts are software that is executed in a trust-less and transparent way, without having to rely on a third-party server or any single point of failure.

Aragon is at the intersection of social, app platform, and blockchain.

### Architecture

The Aragon app is one of few truly decentralized apps. Its smart contracts and front end are upgrade-able thanks to [aragonOS](https://blog.aragon.org/introducing-aragonos-say-hi-to-modular-and-extendable-organizations-8555af1076f3/) and [Aragon Package Manager (APM)](https://hack.aragon.org/docs/apm.html). You can think of APM as a fully decentralized and community-governed NPM. The smart contracts live on the Ethereum blockchain, and APM takes care of storing a log of their versions. APM also keeps a record of arbitrary data blobs hosted on decentralized storage platforms like [IPFS](https://hacks.mozilla.org/2018/08/dweb-building-cooperation-and-trust-into-the-web-with-ipfs/), which in our case we use for storing the front end for the apps.

![Aragon architecture diagram](../../assets/021dfcebf2aaae14.png)


The Aragon app allows users to install new apps into their organization, and those apps are embedded using sandboxed iframes. All the apps use [Aragon UI](https://hack.aragon.org/docs/aragonui-intro.html), therefore users don’t even know they are interacting with apps made by different developers. Aragon has a very rich [permission system](https://hack.aragon.org/docs/acl-intro.html) that allows users to set what each app can do inside their organization. An example would be: Up to $1 can be withdrawn from the funds if there’s a vote with 51% support.

![Aragon tech stack diagram](../../assets/662386609ae4a2c5.png)


### Hello World

To create an Aragon app, you can go to the [Aragon Developer portal](https://hack.aragon.org). Getting started is very easy.

First, [install IPFS](https://ipfs.io/docs/install) if you don’t have it already installed.

Second, run the following commands:

```
$ npm i -g @aragon/cli
$ aragon init foo.aragonpm.eth
$ cd foo
$ aragon run
```


Here we will show a basic counter app, which allows members of an organization to count up or down if a democratic vote happens, for example.

This would be the smart contract (in [Solidity](https://solidity.readthedocs.io/en/v0.4.24/)) that keeps track of the counter in Ethereum:

```
contract Counter is AragonApp {
/**
* @notice Increment the counter by 1
*/
function increment() auth(INCREMENT_ROLE) external {
// ...
}
/**
* @notice Decrement the counter by 1
*/
function decrement() auth(DECREMENT_ROLE) external {
// ...
}
}
```


This code runs in a [web worker](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers), keeping track of events in the smart contract and caching the state in the background:

```
// app/script.js
import Aragon from '@aragon/client'
// Initialize the app
const app = new Aragon()
// Listen for events and reduce them to a state
const state$ = app.store((state, event) => {
// Initial state
if (state === null) state = 0
// Build state
switch (event.event) {
case 'Decrement':
state--
break
case 'Increment':
state++
break
}
return state
})
```


Some basic HTML (not using Aragon UI, for simplicity):

```
<!-- app/index.html !-->
<!doctype html>
<button id="decrement">-</button>
<div id="view">...</div>
<button id="increment">+</button>
<script src="app.js"></script>
```


And the JavaScript that updates the UI:

```
// app/app.js
import Aragon, { providers } from '@aragon/client'
const app = new Aragon(
new providers.WindowMessage(window.parent)
)
const view = document.getElementById('view')
app.state().subscribe(
function(state) {
view.innerHTML = `The counter is ${state || 0}`
},
function(err) {
view.innerHTML = 'An error occurred, check the console'
console.log(err)
}
)
```


`aragon run`

takes care of updating your app on APM and uploading your local webapp to IPFS, so you don’t need to worry about it!

### Learn More

You can go to [Aragon’s website](https://aragon.org) or the [Developer Portal](https://hack.aragon.org) to learn more about Aragon. If you are interested in decentralized governance, you can also check out our [research forum](https://research.aragon.org).

If you would like to contribute, you can look at our [good first issues](https://github.com/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+archived%3Afalse+label%3A%22good+first+issue%22+user%3Aaragon).

If you have any questions, please join the [Aragon community chat](https://aragon.chat)!

## About Luis Cuende

Luis is CEO of Aragon One, one of the teams working on the Aragon project. Luis was awarded as the best underage European programmer at the age of 15 and has been listed in [Forbes 30 Under 30](https://www.forbes.com/30-under-30-europe-2016/technology/#6662a3e4a4b3) and [MIT TR35](https://www.innovatorsunder35.com/the-list/luis-cuende/). He cofounded the blockchain startup [Stampery](https://stampery.com/) and has been into crypto since 2011. His first open source project was a Linux distribution focused on UX.

## One comment

John MartinSeptember 22nd, 2018 at 12:10