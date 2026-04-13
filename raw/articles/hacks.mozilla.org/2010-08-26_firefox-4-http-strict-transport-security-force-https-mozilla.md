---
title: 'Firefox 4: HTTP Strict Transport Security (force HTTPS) – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2010/08/firefox-4-http-strict-transport-security-force-https/
author: Paul Rouget
published: '2010-08-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This article is about a new HTTPS header: Strict-Transport-Security, which force a website to be fetched through HTTPS. This feature will be part of Firefox 4.*

How do you type URLs?

Do you prefix them with **http://** or **https://** systematically? Or do you just type **example.com** and let your browser add **http://**, like most of the people do?

If a web page provide has an **https** version but you access it through **http**, what happens? The **http** version of the Website re-direct you to the **https**, but you first *talked* to the non-encrypted version of the website.

These behaviors can be exploited to run a * man-in-the-middle* attack.

To avoid this, you may want to force your website to be visited through **https** to transform any **http://x.com** request to **https://x.com** (with no client-server dialog).

[Sid Stamm](http://blog.sidstamm.com/) recently integrated HTTP Strict Transport Security (HSTS) into

Firefox. HSTS, specified in an [IETF draft](http://tools.ietf.org/html/draft-hodges-strict-transport-sec-02), allows sites to specify when they wish to be accessed only over **https**.

A website can specify strict transport security for their domain via an HTTP header sent by the server set **during an HTTPS response**:

```
Strict-Transport-Security: max-age=15768000
```

or

```
Strict-Transport-Security: max-age=15768000 ; includeSubDomains
```

`max-age`

sets how long to remember the forced HTTPS (seconds). If

`includeSubDomains`

is set, then this rule will apply to all the sub-domains too.

In the future, any requests to **x.com** are modified to be via **https** if they are attempted through **http** before the request hits the network.

*This header is not considered during a non-encrypted HTTP transaction because the User-Agent doesn’t know if the https actually exists and also because the header can be injected by an attacker.*

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 41 comments

zoonmanAugust 26th, 2010 at 10:59klJuly 12th, 2011 at 15:01FerdinandAugust 26th, 2010 at 14:00zoonmanAugust 26th, 2010 at 22:51TomerAugust 26th, 2010 at 14:23SidAugust 26th, 2010 at 16:38TomerAugust 26th, 2010 at 23:53SidAugust 27th, 2010 at 07:47JamesAugust 27th, 2010 at 00:28annieAugust 29th, 2010 at 01:08SidAugust 31st, 2010 at 08:55StenAugust 29th, 2010 at 04:42MikeAugust 30th, 2010 at 23:12SidAugust 31st, 2010 at 08:52StenSeptember 1st, 2010 at 01:47SidSeptember 1st, 2010 at 15:35StenSeptember 2nd, 2010 at 12:10SidSeptember 2nd, 2010 at 13:57StenSeptember 2nd, 2010 at 14:30SidSeptember 2nd, 2010 at 14:36StenSeptember 2nd, 2010 at 14:55MikeSeptember 2nd, 2010 at 15:28SidSeptember 2nd, 2010 at 16:35PatSeptember 6th, 2010 at 09:04PatSeptember 6th, 2010 at 09:15SidSeptember 8th, 2010 at 09:24PatSeptember 8th, 2010 at 12:53PatSeptember 8th, 2010 at 16:01PatSeptember 9th, 2010 at 12:11Audin MalminNovember 2nd, 2010 at 16:44Hans W.September 8th, 2010 at 05:36PatSeptember 11th, 2010 at 07:29zinkSeptember 8th, 2010 at 12:30steven olsonSeptember 17th, 2010 at 08:08JoshuaOctober 20th, 2010 at 09:26Doug WrightNovember 4th, 2010 at 07:56Ano NymDecember 19th, 2010 at 08:07valchazzzJanuary 6th, 2011 at 09:14JasonMarch 16th, 2011 at 08:23LeandroApril 1st, 2011 at 15:06ouinonouiJune 14th, 2011 at 03:29