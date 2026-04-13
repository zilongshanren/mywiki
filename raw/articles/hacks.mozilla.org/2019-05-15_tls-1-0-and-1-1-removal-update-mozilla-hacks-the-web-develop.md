---
title: TLS 1.0 and 1.1 Removal Update – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/05/tls-1-0-and-1-1-removal-update/
author: Mike Taylor
published: '2019-05-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*tl;dr* Enable support for Transport Layer Security (TLS) 1.2 today!


*Editor’s Note: We updated this post on July 1, 2019 to mention the newly updated SSL Configuration Generator. This service from Mozilla provides boilerplate SSL configurations for the most popular server software setups, with multiple TLS compatibility options. It’s a great starting place for updating your existing servers configs, or for standing up new servers.*

As you may have read last year in the original announcement posts, [Safari](https://webkit.org/blog/8462/deprecation-of-legacy-tls-1-0-and-1-1-versions/), [Firefox](https://blog.mozilla.org/security/2018/10/15/removing-old-versions-of-tls/), [Edge](https://blogs.windows.com/msedgedev/2018/10/15/modernizing-tls-edge-ie11/) and [Chrome](https://security.googleblog.com/2018/10/modernizing-transport-security.html) are removing support for TLS 1.0 and 1.1 in March of 2020. If you manage websites, this means there’s less than a year to enable TLS 1.2 (and, ideally, 1.3) on your servers, otherwise all major browsers will display error pages, rather than the content your users were expecting to find.

In this article we provide some resources to check your sites’ readiness, and start planning for a TLS 1.2+ world in 2020.

## Check the TLS “Carnage” list

Once a week, the Mozilla Security team runs a scan on the [Tranco list](https://tranco-list.eu/) (a research-focused top sites list) and generates a [list of sites still speaking TLS 1.0 or 1.1](http://tlscanary-plot-8e95d89854d73f4d.elb.us-west-2.amazonaws.com/tlsdeprecation-carnage.txt), without supporting TLS ≥ 1.2.

As of this week, there are just over 8,000 affected sites from the one million listed by Tranco.

There are a few potential gotchas to be aware of, if you do find your site on this list:

- 4% of the sites are using TLS ≤ 1.1 to redirect from a bare domain (
[https://example.com](https://example.com)) to*www*([https://www.example.com](https://www.example.com)) on TLS ≥ 1.2 (or vice versa). If you were to only check your site post-redirect, you might miss a potential footgun. - 2% of the sites don’t redirect from bare to
*www*(or vice versa), but do support TLS ≥ 1.2 on one of them.

The vast majority (94%), however, are *just bad*—it’s TLS ≤ 1.1 everywhere.

If you find that a site you work on is in the [TLS “Carnage”](http://tlscanary-plot-8e95d89854d73f4d.elb.us-west-2.amazonaws.com/tlsdeprecation-carnage.txt) list, you need to come up with a plan for enabling TLS 1.2 (and 1.3, if possible). However, this list only covers 1 million sites. Depending on how popular your site is, you might have some work to do regardless of whether you’re not listed by Tranco.

## Run an online test

Even if you’re not on the “Carnage” list, it’s a good idea to test your servers all the same. There are a number of online services that will do some form of TLS version testing for you, but only a few will flag not supporting modern TLS versions in an obvious way. We recommend using one or more of the following:

[Hardenize](https://www.hardenize.com/)will fail your site if it doesn’t support TLS 1.2.[ImmuniWeb](https://www.immuniweb.com/ssl/)will indicate old versions of TLS as violations of[PCI DSS](https://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard)requirements.- Qualys’
[SSL Server Test](https://www.ssllabs.com/ssltest/index.html)will penalize you if[TLS 1.2 is not currently supported](https://blog.qualys.com/ssllabs/2015/05/22/ssl-labs-increased-penalty-when-tls-12-is-not-supported).

## Check developer tools

Another way to do this is open up Firefox (versions 68+) or Chrome (versions 72+) DevTools, and look for the following warnings in the console as you navigate around your site.

![Chrome DevTools console warning](../../assets/32326693c907b2dc.png)


## Update your SSL Configuration

Now that you know which servers need to be updated, it’s time to start the work.

Mozilla maintains an [SSL Configuration Generator](https://ssl-config.mozilla.org/) service that provides boilerplate SSL configurations for the most popular server software setups, with multiple TLS compatibility options. It’s a great starting place for updating your existing servers configs, or for standing up new servers.

## What’s Next?

This October, we plan on disabling old TLS in [Firefox Nightly](https://www.mozilla.org/en-US/firefox/channel/desktop/) and you can expect the same for Chrome and Edge Canaries. We hope this will give enough time for sites to upgrade before affecting their release population users.

## About
[
Mike Taylor ](https://miketaylr.com)

Mike works at Mozilla as a Web Compatibility Engineer from Austin, TX.

## 2 comments

Herbert HatleyMay 17th, 2019 at 01:08Mike TaylorMay 17th, 2019 at 08:01