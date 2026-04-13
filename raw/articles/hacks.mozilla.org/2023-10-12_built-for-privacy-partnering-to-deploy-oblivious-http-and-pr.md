---
title: 'Built for Privacy: Partnering to Deploy Oblivious HTTP and Prio in Firefox
  – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2023/10/built-for-privacy-partnering-to-deploy-oblivious-http-and-prio-in-firefox/
author: Bobby Holley
published: '2023-10-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Protecting user privacy is a [core element](https://www.mozilla.org/en-US/about/webvision/full/#privacy) of Mozilla’s vision for the web and the internet at large. In pursuit of this vision, we’re pleased to announce new partnerships with [Fastly](https://www.fastly.com/blog/firefox-fastly-take-another-step-toward-security-upgrade) and [Divvi Up](https://divviup.org/blog/divvi-up-in-firefox/) to deploy privacy-preserving technology in Firefox.

Mozilla builds a number of tools that help people defend their privacy online, but the need for these tools reflects a world where companies view invasive data collection as necessary for building good products and making money. A zero-sum game between privacy and business interests is not a healthy state of affairs. Therefore, we dedicate considerable effort to developing and advancing new technologies that enable businesses to achieve their goals without compromising peoples’ privacy. This is a focus of our work on [web standards](https://wiki.mozilla.org/Standards), as well as in how we build Firefox itself.

Building an excellent browser while maintaining a high standard for privacy sometimes requires this kind of new technology. For example: we put a lot of effort into keeping Firefox fast. This involves extensive automated testing, but also monitoring how it’s performing for real users. Firefox currently [reports](https://dictionary.telemetry.mozilla.org/apps/firefox_desktop/metrics/perf_page_load) generic performance metrics like page-load time but does not associate those metrics with specific sites, because doing so would reveal peoples’ browsing history. These internet-wide averages are somewhat informative but not particularly actionable. Sites are constantly deploying code changes and occasionally those changes can trigger performance bugs in browsers. If we knew that a specific site got much slower overnight, we could likely isolate the cause and fix it. Unfortunately, we lack that visibility today, which hinders our ability to make Firefox great.

This is a classic problem in data collection: We want aggregate data, but the naive way to get it involves collecting sensitive information about individual people. The solution is to develop technology that delivers the same insights while keeping information about any individual person verifiably private.

In recent years, Mozilla has worked with others to advance two such technologies — [Oblivious HTTP](https://datatracker.ietf.org/doc/html/draft-ietf-ohai-ohttp-10) and the Prio-based [Distributed Aggregation Protocol (DAP)](https://datatracker.ietf.org/doc/draft-ietf-ppm-dap/) — towards being proper internet standards that are practical to deploy in production. Oblivious HTTP works by routing encrypted data through an intermediary to conceal its source, whereas DAP/Prio splits the data into two shares and sends each share to a different server [1]. Despite their different shapes, both technologies rely on a similar principle: By processing the data jointly across two independent parties, they ensure neither party holds the information required to reveal sensitive information about someone.

We therefore need to partner with another independent and trustworthy organization to deploy each technology in Firefox. Having worked for some time to develop and validate both technologies in staging environments, we’ve now taken the next step to engage Fastly to operate an OHTTP relay and Divvi Up to operate a DAP aggregator. Both Fastly and [ISRG](https://www.abetterinternet.org/) (the nonprofit behind Divvi Up and Let’s Encrypt) have excellent reputations for acting with integrity, and they have staked those reputations on the faithful operation of these services. So even in a mirror universe where we tried to persuade them to cheat, they have a strong incentive to hold the line.

Our objective at Mozilla is to develop viable alternatives to the things that are wrong with the internet today and move the entire industry by demonstrating that it’s possible to do better. In the short term, these technologies will help us keep Firefox competitive while adhering to our longstanding principles around sensitive data. Over the long term, we want to see these kinds of strong privacy guarantees become the norm, and we will continue to work towards such a future.

**Footnotes:**

*[1] Each approach is best-suited to different scenarios, which is why we’re investing in both. Oblivious HTTP is more flexible and can be used in interactive contexts, whereas DAP/Prio can be used in situations where the payload itself might be identifying.*


## About Bobby Holley

CTO, Firefox