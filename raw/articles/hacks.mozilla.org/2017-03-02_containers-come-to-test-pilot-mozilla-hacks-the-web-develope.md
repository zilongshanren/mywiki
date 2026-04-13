---
title: Containers Come to Test Pilot – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/03/containers-come-to-test-pilot/
author: John Gruen
published: '2017-03-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Containers feature in [Firefox Nightly](https://nightly.mozilla.org/) gives users the ability to place barriers on the flow of data across sites by isolating cookies, indexedDB, localStorage, and caches within discrete browsing contexts. If you’re interested in the history and technology behind Containers, [please read this blog post](https://blog.mozilla.org/tanvi/2016/06/16/contextual-identities-on-the-web/) outlining the rationale for the Nightly implementation.

While the feature has garnered positive notice among our Nightly audience, there remain outstanding questions about the user experience that suggest the need for further exploration.

After running the Containers UI through successive rounds of user research and UX iteration, we are happy to announce that we’ve launched a [ Containers experiment in Firefox Test Pilot](https://testpilot.firefox.com/experiments/containers) in order to widen the audience exposed to the feature, iterate on the UI, and reason about the future of the feature.

## The road to Test Pilot

[Tanvi’s above-mentioned post introducing Containers](https://blog.mozilla.org/tanvi/2016/06/16/contextual-identities-on-the-web/) explores the complexity of contextual identity on the web. She points out that people may wish to represent themselves differently in different browsing contexts: for example, while browsing social media versus doing research about a medical condition.

Today, browsers don’t do a great job of respecting contextual boundaries. We know from user research that Firefox users make do with a variety of ad hoc tools such as private browsing, multiple profiles, or multiple browsers to manage and protect their online contexts. The Containers experiment provides a tool that’s specifically designed to address context on the web.

The difficulty with Containers is that the UI and UX proposed by the feature are more-or-less unique among browsers. This presents some challenge for shipping to a general audience. Will users get it? Will the UI be sensible and will the security and privacy story behind the Containers feature match users’ mental models?

We’ve conducted user research on Nightly Containers using a [think aloud protocol](https://en.wikipedia.org/wiki/Think_aloud_protocol) and our provisional answer to these questions have been a resounding *kinda*. We found, for example, that many users are more concerned with local threats (a snooping roommate or boss, for example) than your average security engineer. We also found that some research participants who totally missed the privacy features saw a lot of upside in containers as a strictly organizational tool. With these perspectives in mind, we decided that Test Pilot would be a great platform to expose Containers to a broader audience while continuing to learn more about user perceptions of the feature.

[Firefox Test Pilot](https://testpilot.firefox.com/) is a platform that lets us test potential new Firefox features while getting quantitative and qualitative feedback from participants. If you’re interested in the overall process and goals of Test Pilot, you can [read more about it here](https://testpilot.firefox.com/about). With the Containers experiment, we hope to answer the following:

- Is the security model intelligible to Test Pilot users? How do they understand the feature?
- Is the feature useful? If so, how much do people use it, and are there specific use cases that are particularly appealing?
- Which container types do people use? Do people create custom containers?
- Do containers keep people from opening a different browser to perform specific tasks?

### How does the Test Pilot experiment differ from Containers in Nightly?

As with all experiments in Test Pilot, we’ve built an onboarding flow to give the uninitiated an introduction to the experiment. In addition to normal Test Pilot onboarding that’s standard across all experiments, we’ve added a few extra extra steps to the Containers experiment itself to introduce the unfamiliar UI.

In response to user feedback about task management, Test Pilot Containers also introduces some organizational and visibility improvements over the Nightly version. Container management is moved to a toolbar button from which users can sort, hide, rename, create, and delete Containers. To aid in discoverability, users can now create new Container tabs by hovering over the new tab button.

Behind the scenes, the Containers experiment sends [Telemetry data back to Test Pilot](https://github.com/mozilla/testpilot-containers/blob/master/docs/metrics.md), so that we can learn more about users’ experiences with Containers. As with all Test Pilot experiments, users will be able to submit qualitative feedback in the form of ratings and survey responses about their experiences.

Most of the above covers the product rationale for Containers, but since this is Hacks, we should talk implementation as well. Like all Test Pilot experiments, [Containers is shipped as an add-on](https://github.com/mozilla/testpilot-containers/) signed and served from Test Pilot.

Containers require a special Firefox preference, so we started with an [Embedded WebExtension](https://developer.mozilla.org/Add-ons/WebExtensions/Embedded_WebExtensions) to use the [SDK preferences service](https://developer.mozilla.org/Add-ons/SDK/Low-Level_APIs/preferences_service) and the [WebExtension pageAction](https://developer.mozilla.org/Add-ons/WebExtensions/API/pageAction) in tandem. During the development process, we learned that the [contextualIdentities API](https://developer.mozilla.org/Add-ons/WebExtensions/API/contextualIdentities) that affords the underlying technology would not land in Firefox release in time for our experiment to ship.

To resolve this gap, we explored bundling the lower-level service as a [WebExtension Experiment](https://webextensions-experiments.readthedocs.io/en/latest/). However, WebExtension Experiments are only currently allowed in Nightly and Aurora. Since Test Pilot targets users across all channels, we needed a different solution. Thus, the experiment you see today in Test Pilot wound up as a mix of platform, SDK, and WebExtension code.

## What is the security model provided by Containers?

The security enhancements of Containers in Nightly and Test Pilot is common across both versions, and are based on a modification to the browser’s [Same Origin Policy](https://developer.mozilla.org/docs/Web/Security/Same-origin_policy) (SOP).

The Same Origin Policy ensures that documents and data from distinct origins are isolated from each other. It is a critical browser security mechanism that prevents content from one site from being read or altered by another, potentially malicious site.

Containers work by adding an extra bit – a `userContextId`

integer – to the normal (scheme, host, port) tuple that defines an origin. So, an origin is now defined as (`userContextId`

, scheme, host, port). For example, when a user visits Gmail in a **Work** container tab, the browser performs the SOP check against (2, https, mail.google.com, 443). When the same user visits Gmail in a **Personal** container tab, the browser performs the SOP check against (1, https, mail.google.com, 443).

[Containers separate cookies, localStorage, indexedDB, and cache data](https://wiki.mozilla.org/Security/Contextual_Identity_Project/Containers#What_is_.28and_isn.27t.29_separated_between_Containers) from each other and from the **Default** container in Firefox. So, when a user visits their email site in a Work container tab, the browser sets its cookies only in the Work container. If they then visit their email site in a Personal container, the origin that has their cookies doesn’t match and the user is therefore “signed out”.

Because cookies are not shared across containers, cookie-based attacks in one container are unsuccessful against cookies stored in another container. Similarly, cookie-based tracking only tracks a single container – it does not track the user’s entire browsing.

Many privacy and security mechanisms can be realized by including more keys in the origin check. Because of this, Gecko has added attributes to the origin called `OriginAttributes`

. In addition to Containers, this allows us to implement features like [Private Browsing Mode](https://www.mozilla.org/en-US/firefox/private-browsing/), [First Party Isolation](https://bugzilla.mozilla.org/show_bug.cgi?id=1260931), and potentially the proposed [Suborigins standard](https://w3c.github.io/webappsec-suborigins/).

## So what happens now?

Well, we wait and see. As users come into new Test Pilot experiments they inevitably uncover bugs and request features. Our immediate task will be to resolve bugs and prioritize new feature concepts. We’ll continue to push releases to the Containers experiment while it’s in Test Pilot. In the meantime we’ll monitor both qualitative feedback from surveys and quantitative feedback from Telemetry to help us reason about the viability of the experiment and the prioritization of new features.

There is also ongoing work at the platform level, to further separate [History](https://bugzilla.mozilla.org/show_bug.cgi?id=1283320), [Bookmarks](https://bugzilla.mozilla.org/show_bug.cgi?id=1213290), and [TLS Certificate Security Exceptions](https://bugzilla.mozilla.org/show_bug.cgi?id=1249348) data between Containers. Each of these present their own UX, UI, and platform-level challenges.

In the long run, we will have to decide whether Containers makes it to release Firefox. Maybe the feature as we’ve built it for Test Pilot will prove to be a hit, or maybe we will need to go back to the drawing board. Maybe exposing the [underlying APIs to WebExtensions](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/contextualIdentities) kickstarts further add-on development around `OriginAttributes`

. Shipping Containers in Test Pilot is the next step to help us make informed decisions about the future of Containers. If you’re interested in helping to shape that future [please check out the experiment today!](https://testpilot.firefox.com/experiments/containers)

## About John Gruen

Current Test Pilot Product Manager. Former Test Pilot Designer.

## About Jonathan Kingston

Front End Security for Firefox, working on HTTPS adoption, containers and content security.

## About
[
Luke Crouch ](https://groovecoder.com)

Privacy Engineer

## About
[
Tanvi Vyas ](https://blog.mozilla.org/tanvi/)

Security/Privacy Engineer and Tech Lead at Mozilla - @TanviHacks

## 10 comments

SebastiánMarch 2nd, 2017 at 08:44JMMarch 2nd, 2017 at 12:54Luke CrouchMarch 6th, 2017 at 08:36ron22March 2nd, 2017 at 14:11Luke CrouchMarch 6th, 2017 at 08:42Aaron MoodieMarch 2nd, 2017 at 14:39Luke CrouchMarch 6th, 2017 at 08:43MTMarch 3rd, 2017 at 06:51Luke CrouchMarch 6th, 2017 at 09:00MTMarch 6th, 2017 at 10:20