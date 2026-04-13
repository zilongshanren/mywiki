---
title: Introducing State Partitioning – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/02/introducing-state-partitioning/
author: Johann Hofmann
published: '2021-02-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

State Partitioning is the technical term for a new privacy feature in Firefox called Total Cookie Protection, which will be available in ETP Strict Mode in Firefox 86. This article shows how State Partitioning works inside of Firefox and explains what developers of third-party integrations can do to stay compatible with the latest changes.

Web sites utilize a variety of different APIs to store data in the browser. Most famous are cookies, which are commonly used to build login sessions and provide a customized user experience. We call these stateful APIs, because they are able to establish state that will persist through reloads, navigations and browser restarts. While these APIs allow developers to enrich a user’s web experience, they also enable nefarious web tracking which jeopardizes user privacy. To fight abuse of these APIs Mozilla is introducing State Partitioning in Firefox 86.

Stateful Web APIs in Firefox are:

- Storage: Cookies, Local Storage, Session Storage, Cache Storage, and IndexedDB
- Workers: SharedWorkers and ServiceWorkers
- Communication channel: Broadcast channel

To fight against web tracking, Firefox currently relies on [Enhanced Tracking Protection](https://blog.mozilla.org/blog/2019/06/04/firefox-now-available-with-enhanced-tracking-protection-by-default/) (ETP) which blocks cookies and other shared state from known trackers, based on the [Disconnect list](https://disconnect.me/trackerprotection). This form of cookie blocking is an effective approach to stop tracking, but it has its limitations. ETP protects users from the 3000 most common and pervasive identified trackers, but its protection relies on the fact that the list is complete and always up-to-date. Ensuring completeness is difficult, and trackers can try to circumvent the list by registering new domain names. Additionally, identifying trackers is a time-consuming task and commonly adds a delay on a scale of months before a new tracking domain is added to the list.

To address the limitations of ETP and provide comprehensive protection against trackers, we introduce a technique called State Partitioning, which will prevent cookie-based tracking universally, without the need for a list.

State Partitioning is complemented by our efforts to eliminate the usage of non-traditional storage mechanisms (“supercookies”) as a tracking vector, for example [through the partitioning of network state](https://blog.mozilla.org/security/2021/01/26/supercookie-protections/), which was recently rolled out in Firefox 85.

## State Partitioning – How it works in Firefox

To explain State Partitioning, we should first take a look at how stateful Web APIs enable tracking on the Web. While these APIs were not designed for tracking, their state is shared with a website regardless of whether it is loaded as a first-party or embedded as a third-party, for example in an iframe or as a simple image (“[tracking pixel](https://en.wikipedia.org/wiki/Web_beacon)”). This shared state allows trackers embedded in other websites to track you across the Web, most commonly by setting cookies.

For example, a cookie of www.tracker.com will be shared on foo.com and bar.com if they both embed www.tracker.com as a third-party. So, www.tracker.com can connect your activities on both sites by using the cookie as an identifier.

ETP will prevent this by simply blocking access to shared state for embedded instances of www.tracker.com. Without the ability to set cookies, the tracker can not easily re-identify you.

![](../../assets/ae8fbe6dba31c8de.png)

Cookie-based tracking without protections, both instances of www.tracker.com share the same cookie.


In comparison, State Partitioning will also prevent shared third-party state, but it does so without blocking cookie access entirely. With State Partitioning, shared state such as cookies, localStorage, etc. will be partitioned (isolated) by the top-level website you’re visiting. In other words, every first party and its embedded third-party contexts will be put into a self-contained bucket.

Firefox is using *double-keying* to implement State Partitioning, which will add an additional key to the origin of the website that is accessing these states. We use the scheme and [registrable domain](https://url.spec.whatwg.org/#host-registrable-domain) (also known as eTLD+1) of the top-level site as the additional key. Following the above example, cookies for www.tracker.com will be keyed differently under foo.com and bar.com. Instead of looking up the cookie jar for www.tracker.com, Storage partitioning will use www.tracker.com^http://foo.com and www.tracker.com^http://bar.com respectively.

![](../../assets/121968b77a179b28.png)

Cookie-based tracking prevented by State Partitioning, by double-keying both instances of www.tracker.com.


Thus, there will be two distinct cookie jars for www.tracker.com under these two top-level websites.

This takes away the tracker’s ability to use cookies and other previously shared state to identify individuals across sites. Now the state is separate (“partitioned”) instead of shared across different first-party domains.

It is important to understand that State Partitioning will apply to **every embedded third-party resource**, regardless of whether it is a tracker or not.

This brings great benefits for privacy allowing us to extend protections beyond the Disconnect list and it allows embedded websites to continue to use their cookies and storage as they normally would, as long as they don’t need cross-site access. In the next section we will examine what embedded websites can do if they have a legitimate need for cross-site shared state.

## State Partitioning – Web Compatibility

Given that State Partitioning brings a fundamental change to Firefox, ensuring web compatibility and an unbroken user and developer experience is a top concern. Inevitably, State Partitioning will break websites by preventing legitimate uses of third-party state. For example, [Single Sign-On](https://en.wikipedia.org/wiki/Single_sign-on) (SSO) services rely on third-party cookies to sign in users across multiple websites. State Partitioning will break SSO because the SSO provider will not be able to access its first-party state when embedded in another top-level website so that it is unable to recognize a logged-in user.

![](../../assets/3cb3a46046a1ec96.png)

Third-party SSO cookies partitioned by State Partitioning, the SSO iframe cannot get the first-party cookie access.


In order to resolve these compatibility issues of State Partitioning, we allow the state to be **unpartitioned **in certain cases. When unpartitioning is taking effect, we will stop using double-keying and revert the ordinary (first-party) key.

Given the above example, after unpartitioning, the top-level SSO site and the embedded SSO service’s iframe will start to use the same storage key, meaning that they will both access the same cookie jar. So, the iframe can get the login credentials via a third-party cookie.

![](../../assets/ca99fddd41812171.png)

The SSO site has been unpartitioned, the SSO iframe gets the first-party cookie access.


## State Partitioning – Getting Cross-Site Cookie Access

There are two scenarios in which Firefox might unpartition states for websites to allow for access to first-party (cross-site) cookies and other state:

- When an embedded iframe calls the Storage Access API.
- Based on a set of automated heuristics.

### Storage Access API

The [Storage Access API](https://privacycg.github.io/storage-access/) is a newly proposed JavaScript API to handle legitimate exceptions from privacy protections in modern browsers, such as ETP in Firefox or Intelligent Tracking Prevention in Safari. It allows the restricted third-party context to request first-party storage access (access to cookies and other shared state) for itself. In some cases, browsers will show a permission prompt to decide whether they trust the third party enough to allow this access.

![](../../assets/5f6f2a0a703247c9.png)

The Firefox user prompt of the Storage Access API.


A partitioned third-party context can use the Storage Access API to gain a storage permission which grants unpartitioned access to its first-party state.

This functionality is expressed through the [document.requestStorageAccess](https://developer.mozilla.org/en-US/docs/Web/API/Document/requestStorageAccess) method. Another method, [document.hasStorageAccess](https://developer.mozilla.org/en-US/docs/Web/API/Document/hasStorageAccess), can be used to find out whether your current browsing context has access to its first party storage. As outlined on MDN, document.requestStorage is subject to a number of restrictions, standardized as well as [browser-specific](https://developer.mozilla.org/en-US/docs/Web/API/Storage_Access_API#safari_implementation_differences), that protect users from abuse. Developers should make note of these and adjust their site’s user experience accordingly.

As an example, [Zendesk](https://www.zendesk.com/) will show a message with a call-to-action element to handle the standard requirement of [transient user activation](https://html.spec.whatwg.org/multipage/interaction.html#tracking-user-activation) (e.g. a button click). In Safari, it will also spawn a popup that the user has to activate to ensure that the browser-specific requirements of Webkit are satisfied.

![](../../assets/8e048f046edbef06.png)

Zendesk notification to allow the user to trigger the request for storage access.


After the user has granted access, Firefox will remember the storage permission for 30 days.

Note that the third-party context will only be unpartitioned under the top-level domain for which the storage access has been requested. For other top-level domains, the third-party context will still be partitioned. Let’s say there is a cross-origin iframe example.com which is embedded in foo.com. And example.com uses the Storage Access API to request first-party access on foo.com and the user allows it. In this case, example.com will have unpartitioned access to its own first-party cookies on foo.com. Later, the user loads another page bar.com which also embeds example.com. But, this time, the example.com will remain partitioned under bar.com because there is no storage permission here.

| document.hasStorageAccess().then(hasAccess => { if (!hasAccess) { return document.requestStorageAccess(); } }).then(_ => { // Now we have unpartitioned storage access for the next 30 days!//// …}).catch(_ => { // error obtaining storage access.}); |

Javascript example of using the Storage Access API to get the storage access from users.

Currently, the Storage Access API is supported by Safari, Edge, Firefox. It is behind a feature flag in Chrome.

### Automatic unpartitioning through heuristics

In the [Firefox storage access policy](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Privacy/Storage_access_policy#Storage_access_grants), we have defined several heuristics to address Web compatibility issues. The heuristics are designed to catch the most common scenarios of using third-party storage on the web (outside of tracking) and allow storage access in order to make websites continue normally. For example, in Single-Sign-On flows it is common to open a popup that allows the user to sign in, and transmit that sign-in information back to the website that opened the popup. Firefox will detect this case and automatically grant storage access.

Note that these heuristics are not designed for the long term. Using the Storage Access API is the recommended solution for websites that need unpartitioned access. We will continually evaluate the necessity of the restrictions and remove them as appropriate. Therefore, developers should not rely on them now or in the future.

## State Partitioning – User controls for Cross-Site Cookie Access

We have introduced a new UI for State Partitioning which allows users to be aware of which third parties have acquired unpartitioned storage and provides fine-grain control of storage access. Firefox will show the unpartitioned domains in the permission section of the site identity panel. The “Cross-site Cookies” permission indicates the unpartitioned domain, and users can delete the permission from the UI directly by clicking the cancel button alongside the permission entries.

![](../../assets/51ea6c3d8cf87aea.png)


## About
[
Johann Hofmann ](http://johannh.me)

Firefox Security & Privacy Engineer

## About Tim Huang

Firefox Privacy Engineer

## 12 comments

Fazal MajidFebruary 23rd, 2021 at 07:18Graham PerrinFebruary 23rd, 2021 at 11:58voracityFebruary 24th, 2021 at 04:21Bill WadleyFebruary 24th, 2021 at 10:26Ronald ScottFebruary 24th, 2021 at 10:49gwarserFebruary 25th, 2021 at 14:31antistressFebruary 25th, 2021 at 15:01antistressFebruary 26th, 2021 at 06:25Helle VaanzinnFebruary 25th, 2021 at 23:36Thanks!February 26th, 2021 at 00:43Thanks!February 26th, 2021 at 00:46Mark de RoussierMarch 20th, 2021 at 19:11