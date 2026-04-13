---
title: QUIC and HTTP/3 Support now in Firefox Nightly and Beta – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2021/04/quic-and-http-3-support-now-in-firefox-nightly-and-beta/
author: Dragana Damjanovic
published: '2021-04-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**tl;dr:** Support for [QUIC](https://tools.ietf.org/html/draft-ietf-quic-transport-34) and [HTTP/3](https://tools.ietf.org/html/draft-ietf-quic-http-34) is now enabled by default in [Firefox Nightly](https://www.mozilla.org/en-US/firefox/nightly/all/) and [Firefox Beta.](https://www.mozilla.org/en-US/firefox/all/#product-desktop-beta) We are planning to start rollout on the release in Firefox Stable Release 88. HTTP/3 will be available by default by the end of May.

## What is HTTP/3?

HTTP/3 is a new version of HTTP (the protocol that powers the Web) that is based on QUIC. HTTP/3 has three main performance improvements over HTTP/2:

- Because it is based on UDP it takes less time to connect;
- It does not have head of line blocking, where delays in delivering packets cause an entire connection to be delayed; and
- It is better able to detect and repair packet loss.

QUIC also provides connection migration and other features that should improve performance and reliability. For more on QUIC, see this [excellent blog post](https://blog.cloudflare.com/http-3-from-root-to-tip/) from Cloudflare.

## How to use it?

[Firefox Nightly](https://www.mozilla.org/en-US/firefox/nightly/all/) and [Firefox Beta](https://www.mozilla.org/en-US/firefox/all/#product-desktop-beta) will automatically try to use HTTP/3 if offered by the Web server (for instance, Google or Facebook). Web servers can indicate support by using the [Alt-Svc](https://tools.ietf.org/html/rfc7838) response header or by advertising HTTP/3 support with a [HTTPS](https://tools.ietf.org/html/draft-ietf-dnsop-svcb-https-03) DNS record. Both the client and server must support the same QUIC and HTTP/3 draft version to connect with each other. For example, Firefox currently supports drafts 27 to 32 of the specification, so the server must report support of one of these versions (e.g., “h3-32”) in Alt-Svc or HTTPS record for Firefox to try to use QUIC and HTTP/3 with that server. When visiting such a website, viewing the network request information in Dev Tools should show the Alt-Svc header, and also indicate that HTTP/3 was used.

If you encounter issues with these or other sites, please file a bug in [Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core&component=Networking%3A+HTTP).

## About Dragana Damjanovic

Dragana is the networking module owner of Firefox. She is responsible for the Firefox’s implementation of HTTP, HTTP/3, HTTP/2, WebSockets, DNS, cache, etc.

## 5 comments

OlafApril 16th, 2021 at 23:06Dragana DamjanovicApril 20th, 2021 at 05:28Marcio MTApril 29th, 2021 at 23:43JeffMay 3rd, 2021 at 09:15Munyalo mwanzaMay 14th, 2021 at 09:17