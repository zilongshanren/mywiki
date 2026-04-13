---
title: 'Flying the Nest: WebThings Gateway 1.0 – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2020/12/flying-the-nest-webthings-gateway-1-0/
author: Ben Francis
published: '2020-12-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## WebThings Gateway 1.0

After four years of incubation at Mozilla, we are excited to announce the release of [WebThings Gateway 1.0](https://webthings.io/gateway/) and a new home for the WebThings platform.

You may have heard that following a company [restructuring](https://blog.mozilla.org/blog/2020/08/11/changing-world-changing-mozilla/) in August, the WebThings platform is being [spun out](https://discourse.mozilla.org/t/an-important-update-on-mozilla-webthings/67764) of Mozilla as an independent open source project, at the new community-run home of [webthings.io](https://webthings.io).

This blog post will explain what to expect from the 1.0 release, the action you need to take if you want to transition your existing WebThings Gateway to new community-run infrastructure, and what to expect from the WebThings project going forward.

See the [release notes](https://github.com/WebThingsIO/gateway/releases/tag/1.0.0) for the full set of new features and changes in the WebThings Gateway 1.0 release including support for new types of sensors, searchable add-ons and translations into five new languages.

## The Journey So Far

The Mozilla IoT team [released](https://hacks.mozilla.org/2017/06/building-the-web-of-things/) the first version of “Project Things” in June 2017, six months after an initial whitepaper proposing how Mozilla could apply its mission to the emerging IoT ecosystem. We wanted to apply lessons learned from the World Wide Web to the Internet of Things, to create an IoT which *“puts people first, where individuals can shape their own experience and are empowered, safe and independent”*.

Our team’s goal was to create an open source implementation of the [Web of Things](https://www.w3.org/WoT/) which embodied Mozilla’s values and helped drive IoT standards around privacy, security and interoperability. We aimed to bridge the communication gap between connected devices and work towards a more decentralised Internet of Things that is safe, open and interoperable.

Some of the highlights of the last four years have included:

- Twelve releases of our
[WebThings Gateway](https://webthings.io/gateway/)software, which allows users to directly monitor and control their home over the web without a middleman. [Translation](https://pontoon.mozilla.org/projects/webthings-gateway/)of WebThings Gateway into 34 spoken languages, with over 100,000 downloads powering thousands of DIY smart homes around the world.- Over a hundred
[add-ons](https://api.webthings.io:8443/addons/info)developed for WebThings Gateway, bridging a wide range of different protocols and devices to the Web of Things, providing various types of user notifications and extending the gateway’s user interface. [WebThings Framework](https://webthings.io/framework/)implementations in over a dozen programming languages, enabling developers to implement their own web things in the language of their choice.- The growth of a worldwide community of hackers, makers and educators who have been pivotal in building, testing and promoting WebThings around the world.
- Presentations and workshops at conferences from Mozilla Festival in London and FOSDEM in Brussels to LinuxConf in South Africa and Maker Faire in Silicon Valley.
- Countless innovative DIY projects by the community – controlling physical devices using voice and virtual reality, smart campervans, smart yurts, earthquake alerts, pool heating, air quality monitoring and plant watering.
- The release of the
[Mozilla WebThings Gateway Kit](https://www.okdo.com/p/mozilla-webthings-gateway-kit/)in partnership with OKdo (still available for a limited time only!) - Contributions to the W3C
[Thing Description](https://www.w3.org/TR/wot-thing-description/)specification which became a W3C recommendation in April this year.

## Our New Home

Going forward, you will be able to find the WebThings community at our new home of [webthings.io](https://webthings.io). You can follow [@WebThingsIO](https://twitter.com/WebThingsIO) on Twitter, [fork us on GitHub](http://github.com/WebThingsIO) and sign up for our [newsletter](https://webthings.io/#newsletter) to keep up to date with all the latest news.

For the time being we will still be using the [WebThings forum](https://discourse.mozilla.org/c/iot/252) at discourse.mozilla.org and the #iot channel at [chat.mozilla.org](https://chat.mozilla.org) for discussions.

## Transition

As part of the transition the Mozilla IoT remote access service and automatic software updates will be discontinued on 31st December 2020, to be replaced by community-run services at webthings.io which you can transfer to if you choose.

If you have an existing WebThings Gateway then you should shortly receive an automatic update to the 1.0 release and see a banner appear at the top of your gateway’s web interface.

Clicking the “choose” button will display a dialog explaining the choices you have about whether to transfer to new community-run services. This includes whether you wish to continue to receive software updates from the community, and whether you wish to use the replacement remote access service and swap your mozilla-iot.org subdomain for a webthings.io subdomain.![WebThings Gateway transition banner](../../assets/6902f193c6f4fe59.png)


You will also have the option of signing up for the new WebThings newsletter and will need to accept the WebThings community Privacy Policy and Terms of Service in order to make use of any replacement services.

If you choose not to transfer your gateway to the new webthings.io infrastructure then fear not, your gateway will continue to work just as it did before on your local network as it doesn’t rely on any cloud services to function. But please be aware that after 31st December 2020 you will no longer be able to use the mozilla-iot.org remote access service and Mozilla will no longer provide software updates, including security fixes.![WebThings Gateway transition dialog](../../assets/97d784542e45fcbc.png)


## Governance

Following the transition, governance of the project is being passed to the community using a [module ownership system](https://github.com/WebThingsIO/wiki/wiki/Module-Ownership-System) independent of the Mozilla Corporation’s organisational structure, like the[ one used by the Mozilla project](https://www.mozilla.org/en-US/about/governance/policies/module-ownership/). For continuity the initial module owners of the top level WebThings module will be [Ben Francis](https://github.com/benfrancis) and [Michael Stegeman](https://github.com/mrstegeman) from the original Mozilla IoT team. These module owners will then be able to create sub-modules and assign new module owners and peers to help govern the project going forward.

You can find the initial list of modules and module owners on our [wiki](https://github.com/WebThingsIO/wiki/wiki/Modules). If you would like to volunteer to be an owner or peer of a module, or propose the creation of a new sub-module, then you can contact the owner of the module or parent module, or contact the top level module owners at [team@webthings.io](mailto:team@webthings.io).

The best way to achieve module owner or peer status is by demonstrating your commitment to the module through ongoing contributions, so rather than wait for permission we encourage you to just get stuck in and start hacking on whatever area interests you.

## How to Contribute

Having flown the nest from Mozilla, the future of the WebThings project is now in the hands of its worldwide community. Your support is going to be crucial in enabling the project to continue to thrive and grow.

There are many ways you can contribute to WebThings:

**💻 Development**– Pick a bug, task or feature off the[Product Backlog](https://github.com/orgs/WebThingsIO/projects/3)and start hacking**🐜 Testing**– Either writing or fixing[automated tests](https://github.com/webthingsio/gateway#running-tests), or manual testing of builds of the latest master branch**🧩 Add-ons**–[Write an add-on](https://github.com/WebThingsIO/wiki/wiki/HOWTO%3A-Create-an-add-on)(or help maintain[an existing one](https://api.webthings.io:8443/addons/info)), to add support for a new type of device or protocol, add new notification mechanisms or extend the UI for new use cases**💡 Things**– Build a new web thing using the[WebThings Framework](https://webthings.io/framework/)to expand the Web of Things ecosystem, or even create a web thing library in a new programming language- 📖
**Documentation**– Our[documentation](https://github.com/WebThingsIO/docs)could do with some love, and we are currently overhauling[this section of the website](https://webthings.io/docs/) **💬 Support**– Help other community members with questions and problems on the[forums](https://discourse.mozilla.org/c/iot/252)and #iot[chat](https://chat.mozilla.org/)channel**🌍 Localisation**– Help translate the WebThings Gateway into new languages[using Pontoon](https://pontoon.mozilla.org/projects/webthings-gateway/)**📣 Evangelism**– Talk about WebThings at events, on blogs and on social media, give talks and run workshops to help spread the word**📄 Standardisation**– Help with standardising the[Thing Description](https://www.w3.org/TR/wot-thing-description/)and[Web Thing Protocol](https://www.w3.org/community/web-thing-protocol/)(see the recent[call for use cases & requirements](https://www.w3.org/community/web-thing-protocol/2020/07/06/call-for-use-cases-requirements-web-thing-protocol/))

## What’s Next?

Now that version 1.0 is out of the door, we are already starting to think about working towards a version 2.0. In terms of a roadmap, WebThings’ new commercial sponsor [Krellian](https://krellian.com/) has some [ideas](https://medium.com/krellian/introducing-the-webthings-iot-platform-9fe4f97c0c72) about where to take the project next, but we’d most like to hear from you (the WebThings Community) about what you’d like to see from the project in the future.

We’d again like to take this opportunity to thank you all for your contributions and support for the project so far. The team is looking forward to this new chapter in the WebThings story, as the project flies the nest from Mozilla to make its own way in the world! We hope to take you all along for the ride.

Come and join the [discussion](https://discourse.mozilla.org/c/iot/252) on our forum, and follow us on [Twitter](https://twitter.com/WebThingsIO) or subscribe to our new email [newsletter](https://webthings.io/#newsletter) if you’d like to be kept up to date with the latest WebThings news.

Happy hacking!

## About
[
Ben Francis ](http://tola.me.uk)

Former Mozilla Software Engineer. W3C Invited Expert on Web Applications and the Web of Things.