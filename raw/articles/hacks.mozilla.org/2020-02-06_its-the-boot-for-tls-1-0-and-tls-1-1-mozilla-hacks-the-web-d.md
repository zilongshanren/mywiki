---
title: It’s the Boot for TLS 1.0 and TLS 1.1 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/02/its-the-boot-for-tls-1-0-and-tls-1-1/
author: Thyla van der Merwe
published: '2020-02-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s Update:** June 24, 11:40am PDT – We will be moving ahead with disabling TLS 1.0 and TLS 1.1 by default in Firefox 78, releasing June 30th. If you see a “Secure Connection Failed” message as displayed in the post below, then hit the button to re-enable TLS 1.0 and TLS 1.1. You should only need to hit this button once, the change will be global.

Earlier Update: March 23, 10:43am PDT – We have re-enabled TLS 1.0 and 1.1 in Firefox 74 and 75 Beta to better enable access to sites sharing critical and important information during this time.

# Coming to a Firefox near you in March

The [Transport Layer Security (TLS) protocol](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) is the de facto means for establishing security on the Web. The protocol has a long and colourful history, starting with its inception as the Secure Sockets Layer (SSL) protocol in the early 1990s, right up until the recent release of the jazzier (read faster and safer) TLS 1.3. The need for a new version of the protocol was born out of a desire to improve efficiency and to remedy the flaws and weaknesses present in earlier versions, specifically in TLS 1.0 and TLS 1.1. See the [BEAST](https://nerdoholic.org/uploads/dergln/beast_part2/ssl_jun21.pdf), [CRIME](https://docs.google.com/presentation/d/11eBmGiHbYcHR9gL5nDyZChu_-lCa2GizeuOfaLU2HOU/edit#slide=id.g1d134dff_1_222) and [POODLE](https://www.openssl.org/~bodo/ssl-poodle.pdf) attacks, for example.

With limited support for newer, more robust cryptographic primitives and cipher suites, it doesn’t look good for TLS 1.0 and TLS 1.1. With the safer TLS 1.2 and TLS 1.3 at our disposal to adequately project web traffic, it’s time to move the TLS ecosystem into a new era, namely one which doesn’t support weak versions of TLS by default. This has been the abiding sentiment of browser vendors – Mozilla, Google, Apple and Microsoft have committed to disabling TLS 1.0 and TLS 1.1 as default options for secure connections. In other words, browser clients will aim to establish a connection using TLS 1.2 or higher. For more on the rationale behind this decision, see our [earlier blog post](https://blog.mozilla.org/security/2018/10/15/removing-old-versions-of-tls/) on the subject.

## What does this look like in Firefox?

We deployed this in Firefox Nightly, the experimental version of our browser, towards the end of 2019. It is now also available in [Firefox Beta 73](https://www.mozilla.org/en-US/firefox/channel/desktop/). In Firefox, this means that the minimum TLS version allowable by default is TLS 1.2. This has been executed in code by setting `security.tls.version.min=3`

, a preference indicating the minimum TLS version supported. Previously, this value was set to 1. If you’re connecting to sites that support TLS 1.2 and up, you shouldn’t notice any connection errors caused by TLS version mismatches.

## What if a site only supports lower versions of TLS?

In cases where only lower versions of TLS are supported, i.e., when the more secure TLS 1.2 and TLS 1.3 versions cannot be negotiated, we allow for a fallback to TLS 1.0 or TLS 1.1 via an override button. As a Firefox user, if you find yourself in this position, you’ll see this:

As a user, you will have to actively initiate this override. But the override button offers you a choice. You can, of course, choose not to connect to sites that don’t offer you the best possible security.

This isn’t ideal for website operators. We would like to encourage operators to upgrade their servers so as to offer users a secure experience on the Web. We announced our plans regarding TLS 1.0 and TLS 1.1 deprecation over a year ago, in October 2018, and now the time has come to make this change. Let’s work together to move the TLS ecosystem forward.

## Deprecation timeline

We plan to monitor telemetry over two Firefox Beta cycles, and then we’re going to let this change ride to Firefox Release. So, expect Firefox 74 to offer TLS 1.2 as its minimum version for secure connections when it ships on **10 March 2020**. We plan to keep the override button for now; the telemetry we’re collecting will tell us more about how often this button is used. These results will then inform our decision regarding when to remove the button entirely. It’s unlikely that the button will stick around for long. We’re committed to completely eradicating weak versions of TLS because at Mozilla we believe that user [security should not be treated as optional](https://www.mozilla.org/en-US/about/manifesto/).

Again, we would like to stress the importance of [upgrading web servers](https://hacks.mozilla.org/2019/05/tls-1-0-and-1-1-removal-update/) over the coming months, as we bid farewell to TLS 1.0 and TLS 1.1. R.I.P, you’ve served us well.

## About Thyla van der Merwe

Cryptography Engineering Manager at Mozilla.

## 6 comments

Yuhong BaoFebruary 6th, 2020 at 19:41Alexandre LeducFebruary 8th, 2020 at 08:16Thyla van der MerweFebruary 10th, 2020 at 03:11custom.firefox.ladyFebruary 8th, 2020 at 19:17Thyla van der MerweFebruary 10th, 2020 at 03:51Tim FisherFebruary 11th, 2020 at 05:47