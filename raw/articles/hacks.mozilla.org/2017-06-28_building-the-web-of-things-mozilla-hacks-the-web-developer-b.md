---
title: Building the Web of Things – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/06/building-the-web-of-things/
author: Ben Francis
published: '2017-06-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Mozilla is working to create a Web of Things framework of software and services that can bridge the communication gap between connected devices. By providing these devices with web URLs and a standardized data model and API, we are moving towards a more decentralized Internet of Things that is safe, open and interoperable.*

The Internet and the World Wide Web are built on open standards which are decentralized by design, with anyone free to implement those standards and connect to the network without the need for a central point of control. This has resulted in the explosive growth of hundreds of millions of personal computers and billions of smartphones which can all talk to each other over a single global network.

As technology advances from personal computers and smartphones to a world where everything around us is connected to the Internet, new types of devices in our homes, cities, cars, clothes and even our bodies are going online every day.

## The Internet of Things

The “Internet of Things” (IoT) is a term to describe how physical objects are being connected to the Internet so that they can be discovered, monitored, controlled or interacted with. Like any advancement in technology, these innovations bring with them enormous new opportunities, but also new risks.

At Mozilla our mission is *“to ensure the Internet is a global public resource, open and accessible to all. An Internet that truly puts people first, where individuals can shape their own experience and are empowered, safe and independent.”*

This mission has never been more important than today, a time when everything around us is being designed to connect to the Internet. As new types of devices come online, they bring with them significant new challenges around security, privacy and interoperability.

Many of the new devices connecting to the Internet are insecure, do not receive software updates to fix vulnerabilities, and raise new privacy questions around the collection, storage, and use of large quantities of extremely personal data.

Additionally, most IoT devices today use proprietary vertical technology stacks which are built around a central point of control and which don’t always talk to each other. When they do talk to each other it requires per-vendor integrations to connect those systems together. There are efforts to create standards, but the landscape is extremely complex and there’s still not yet a single dominant model or market leader.

## The Web of Things

Using the Internet of Things today is a lot like sharing information on the Internet before the World Wide Web existed. There were competing hypertext systems and proprietary GUIs, but the Internet lacked a unifying application layer protocol for sharing and linking information.

The “Web of Things” (WoT) is an effort to take the lessons learned from the World Wide Web and apply them to IoT. It’s about creating a decentralized Internet of Things by giving Things URLs on the web to make them linkable and discoverable, and defining a standard data model and APIs to make them interoperable.

The Web of Things is not just another vertical IoT technology stack to compete with existing platforms. It is intended as a unifying horizontal application layer to bridge together multiple underlying IoT protocols.

Rather than start from scratch, the Web of Things is built on existing, proven web standards like REST, [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP), [JSON](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON), [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) and TLS (Transport Layer Security). The Web of Things will also require new web standards. In particular, we think there is a need for a Web Thing Description format to describe things, a REST style Web Thing API to interact with them, and possibly a new generation of HTTP better optimised for IoT use cases and use by resource constrained devices.

The Web of Things is not just a Mozilla Initiative, there is already a well established[ Web of Things community](http://webofthings.org/) and related standardization efforts at the[ IETF](https://www.ietf.org/id/draft-keranen-t2trg-rest-iot-04.txt),[ W3C](https://www.w3.org/WoT/),[ OCF](https://openconnectivity.org/developer/specifications) and[ OGC](https://github.com/opengeospatial/sensorthings). Mozilla plans to be a participant in this community to help define new web standards and promote best practices around privacy, security and interoperability.

From this existing work three key integration patterns have emerged for connecting things to the web, defined by the point at which a Web of Things API is exposed to the Internet.

### Direct Integration Pattern

The simplest pattern is the direct integration pattern where a device exposes a Web of Things API directly to the Internet. This is useful for relatively high powered devices which can support TCP/IP and HTTP and can be directly connected to the Internet (e.g. a WiFi camera). This pattern can be tricky for devices on a home network which may need to use NAT or TCP tunneling in order to traverse a firewall. It also more directly exposes the device to security threats from the Internet.

**Gateway Integration Pattern**

The gateway integration pattern is useful for resource-constrained devices which can’t run an HTTP server themselves and so use a gateway to bridge them to the web. This pattern is particularly useful for devices which have limited power or which use PAN network technologies like Bluetooth or ZigBee that don’t directly connect to the Internet (e.g. a battery powered door sensor). A gateway can also be used to bridge all kinds of existing IoT devices to the web.

### Cloud Integration Pattern

In the cloud integration pattern the Web of Things API is exposed by a cloud server which acts as a gateway remotely and the device uses some other protocol to communicate with the server on the back end. This pattern is particularly useful for a large number of devices over a wide geographic area which need to be centrally co-ordinated (e.g. air pollution sensors).

## Project Things by Mozilla

In the Emerging Technologies team at Mozilla we’re working on an experimental framework of software and services to help developers connect “things” to the web in a safe, secure and interoperable way.

**Project Things** will initially focus on developing three components:

**Things Gateway**— An open source implementation of a Web of Things gateway which helps bridge existing IoT devices to the web**Things Cloud**— A collection of Mozilla-hosted cloud services to help manage a large number of IoT devices over a wide geographic area**Things Framework**— Reusable software components to help create IoT devices which directly connect to the Web of Things

## Things Gateway

Today we’re announcing the availability of a prototype of the first component of this system, the Things Gateway. We’ve made available a software image you can use to [build your own Web of Things gateway](http://iot.mozilla.org/gateway) using a Raspberry Pi.

So far this early prototype has the following features:

- Easily discover the gateway on your local network
- Choose a web address which connects your home to the Internet via a secure TLS tunnel requiring zero configuration on your home network
- Create a username and password to authorize access to your gateway
- Discover and connect commercially available ZigBee and Z-Wave smart plugs to the gateway
- Turn those smart plugs on and off from a web app hosted on the gateway itself

We’re releasing this prototype very early on in its development so that hackers and makers can get their hands on the source code to build their own Web of Things gateway and contribute to the project from an early stage.

This initial prototype is implemented in JavaScript with a NodeJS web server, but we are exploring an adapter add-on system to allow developers to build their own Web of Things adapters using other programming languages like Rust in the future.

## Web Thing API

Our goal in building this IoT framework is to lead by example in creating a Web of Things implementation which embodies Mozilla’s values and helps drive IoT standards around security, privacy and interoperability. The intention is not just to create a Mozilla IoT platform but an open source implementation of a Web of Things API which anyone is free to implement themselves using the programming language and operating system of their choice.

To this end, we have started working on a draft [Web Thing API specification](https://mozilla-iot.github.io/wot/) to eventually propose for standardization. This includes a simple but extensible **Web Thing Description** format with a default JSON encoding, and a REST + WebSockets **Web Thing API**. We hope this pragmatic approach will appeal to web developers and help turn them into WoT developers who can help realize our vision of a decentralized Internet of Things.

We encourage developers to experiment with using this draft API in real life use cases and provide [feedback](https://github.com/mozilla-iot/wot/issues) on how well it works so that we can improve it.

## Get Involved

There are many ways you can contribute to this effort, some of which are:

**Build a Web Thing**— build your own IoT device which uses the[Web Thing API](https://mozilla-iot.github.io/wot/)**Create an adapter**— Create an[adapter](https://github.com/mozilla-iot/wiki/wiki/Adapter-IPC)to bridge an existing IoT protocol or device to the web**Hack on Project Things**— Help us develop Mozilla’s Web of Things[implementation](https://github.com/mozilla-iot)

You can find out more at ** iot.mozilla.org** and all of our source code is on

[GitHub](https://github.com/mozilla-iot). You can find us in #iot on

[irc.mozilla.org](https://wiki.mozilla.org/IRC)or on our

[public mailing list](https://mail.mozilla.org/listinfo/mozilla.dev.iot).

## About
[
Ben Francis ](http://tola.me.uk)

Former Mozilla Software Engineer. W3C Invited Expert on Web Applications and the Web of Things.

## 3 comments

RolandJuly 6th, 2017 at 22:30Sally GJuly 7th, 2017 at 15:16Henning SummerJuly 7th, 2017 at 22:06