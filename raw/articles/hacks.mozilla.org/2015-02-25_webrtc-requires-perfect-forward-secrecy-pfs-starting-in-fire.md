---
title: WebRTC requires Perfect Forward Secrecy (PFS) starting in Firefox 38 – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/02/webrtc-requires-perfect-forward-secrecy-pfs-starting-in-firefox-38/
author: Maire Reavy
published: '2015-02-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Today, we are announcing that [Firefox 38](https://developer.mozilla.org/en-US/Firefox/Releases/38) will take further measures to secure users’ communications by removing support in WebRTC for all DTLS cipher suites that do not support forward secrecy. For developers: if you have a WebRTC application or server that doesn’t support PFS ciphers, you will need to update your code.

Forward secrecy, also known as [Perfect Forward Secrecy (PFS)](http://en.wikipedia.org/wiki/Forward_secrecy#Perfect_forward_secrecy_.28PFS.29), is a feature of a cryptographic protocol that limits the damage of a key compromise: “This means that the compromise of one [session] cannot lead to the compromise of others, and also that there is not a single secret value which can lead to the compromise of multiple [sessions]”.

The PFS suites in TLS and DTLS use an ephemeral Diffie-Hellman key exchange (DHE) or elliptic-curve Diffie-Hellman (ECDHE) to create a different shared secret key for each session. The [WebRTC security architecture](https://tools.ietf.org/html/draft-ietf-rtcweb-security-arch-10) recommends that PFS suites be preferred for WebRTC.

Due to [bug 102794](https://bugzil.la/102794), Firefox is unable to act as a server for DHE cipher suites. We plan to add complete DHE support, but until then we recommend the use of the ECDHE cipher suites.

Existing users of the [webrtc.org codebase](http://www.webrtc.org/native-code) who are using OpenSSL and derivatives such as BoringSSL need to update to enable ECDHE ciphers. [This bug](https://code.google.com/p/chromium/issues/detail?id=406458) contains more details.

If you have a WebRTC application or server that doesn’t support PFS ciphers, you should be working on getting that resolved ASAP. Firefox 38 is scheduled for Beta the week of March 30th, and a general release is planned for Tuesday, May 12th.

## About Maire Reavy

Maire is the engineering manager for Mozilla’s WebRTC team.

## 2 comments

RuslanFebruary 25th, 2015 at 07:45Ralph GilesMarch 13th, 2015 at 12:08