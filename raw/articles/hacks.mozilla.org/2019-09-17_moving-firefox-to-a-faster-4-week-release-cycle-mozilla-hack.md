---
title: Moving Firefox to a faster 4-week release cycle – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2019/09/moving-firefox-to-a-faster-4-week-release-cycle/
author: Ritu Kothari
published: '2019-09-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Editor’s Note: Wednesday, 10:40am PT. We’ve updated this post with the following correction: The SeaMonkey Project consumes Firefox releases, not SpiderMonkey, which is Firefox’s JavaScript engine. Thanks to an astute reader for noticing.*

## Overview

We typically ship a major Firefox browser (Desktop and Android) release every 6 to 8 weeks. Building and releasing a browser is complicated and involves many players. To optimize the process, and make it more reliable for all users, over the years we’ve developed a phased release strategy that includes ‘pre-release’ channels: [Firefox Nightly](https://www.mozilla.org/firefox/channel/desktop/#nightly), [Beta](https://www.mozilla.org/firefox/channel/desktop/#beta), and [Developer Edition](https://www.mozilla.org/firefox/developer/). With this approach, we can test and stabilize new features before delivering them to the majority of Firefox users via general release.

## Today’s announcement

And today we’re excited to announce that we’re moving to a four-week release cycle! We’re adjusting our cadence to increase our agility, and bring you new features more quickly. In recent quarters, we’ve had many requests to take features to market sooner. Feature teams are increasingly working in sprints that align better with shorter release cycles. Considering these factors, it is time we changed our release cadence.

Starting Q1 2020, we plan to ship a major Firefox release every 4 weeks. Firefox ESR release cadence ([Extended Support Release](https://www.mozilla.org/en-US/firefox/enterprise/) for the enterprise) will remain the same. In the years to come, we anticipate a major ESR release every 12 months with 3 months support overlap between new ESR and end-of-life of previous ESR. The next two major ESR releases will be ~June 2020 and ~June 2021.

Shorter release cycles provide greater flexibility to support product planning and priority changes due to business or market requirements. With four-week cycles, we can be more agile and ship features faster, while applying the same rigor and due diligence needed for a high-quality and stable release. Also, we put new features and implementation of new Web APIs into the hands of developers more quickly. (This is what we’ve been doing recently with CSS spec implementations and updates, for instance.)

In order to maintain quality and minimize risk in a shortened cycle, we must:

- Ensure Firefox engineering productivity is not negatively impacted.
- Speed up the regression feedback loop from rollout to detection to resolution.
- Be able to control feature rollout based on release readiness.
- Ensure adequate testing of larger features that span multiple release cycles.
- Have clear, consistent mitigation and decision processes.

## Firefox rollouts and feature experiments

Given a shorter Beta cycle, support for our pre-release channel users is essential, including developers using Firefox Beta or Developer Edition. We intend to roll out fixes to them as quickly as possible. Today, we produce two Beta builds per week. Going forward, we will move to more frequent Beta builds, similar to what we have today in Firefox Nightly.

Staged rollouts of features will be a continued best practice. This approach helps minimize unexpected (quality, stability or performance) disruptions to our release end-users. For instance, if a feature is deemed high-risk, we will plan for slow rollout to end-users and turn the feature off dynamically if needed.

We will continue to foster a culture of feature experimentation and A/B testing before rollout to release. Currently, the duration of experiments is not tied to a release cycle length and therefore not impacted by this change. In fact, experiment length is predominantly a factor of time needed for user enrollment, time to trigger the study or experiment and collect the necessary data, followed by data analysis needed to make a go/no-go decision.

Despite the shorter release cycles, we will do our best to localize all new strings in all locales supported by Firefox. We value our end-users from all across the globe. And we will continue to delight you with localized versions of Firefox.

## Firefox release schedule 2019 – 2020

Firefox engineering will deploy this change gradually, starting with Firefox 71. We aim to achieve 4-week release cadence by Q1 2020. The table below lists Firefox versions and planned launch dates. Note: These are subject to change due to business reasons.

## Process and product quality metrics

As we slowly reduce our release cycle length, from 7 weeks down to 6, 5, 4 weeks, we will monitor closely. We’ll watch aspects like release scope change; developer productivity impact (tree closure, build failures); beta churn (uplifts, new regressions); and overall release stabilization and quality (stability, performance, carryover regressions). Our main goal is to identify bottlenecks that prevent us from being more agile in our release cadence. Should our metrics highlight an unexpected trend, we will put in place appropriate mitigations.

Finally, projects that consume Firefox mainline or ESR releases, such as [SeaMonkey](http://www.seamonkey-project.org/) and [Tor](https://www.torproject.org/) will have to do more frequent releases if they wish to stay current with Firefox releases. These Firefox releases will have fewer changes each so they should be correspondingly easier to integrate. The 4-week releases of Firefox will be the most stable, fastest, and best quality builds.

In closing, we hope you’ll enjoy the new faster cadence of Firefox releases. You can always refer to [https://wiki.mozilla.org/Release_Management/Calendar](https://wiki.mozilla.org/Release_Management/Calendar) for the latest release dates and other information. Got questions? Please send email to [release-mgmt@mozilla.com](mailto:release-mgmt@mozilla.com).

## About Ritu Kothari

Ritu leads the Firefox release management team.

## About Yan Or

Yan leads the Product Integrity team for Firefox.

## 16 comments

Matthew BealeSeptember 17th, 2019 at 09:48Ritu KothariSeptember 17th, 2019 at 15:48CypherousSeptember 17th, 2019 at 10:34PatriciaSeptember 17th, 2019 at 11:46Ritu KothariSeptember 17th, 2019 at 16:16askingforafriendSeptember 18th, 2019 at 02:14Ritu KothariSeptember 18th, 2019 at 08:01gwenSeptember 18th, 2019 at 07:13Thomas BrownSeptember 18th, 2019 at 08:27Ritu KothariSeptember 18th, 2019 at 10:54brankoSeptember 19th, 2019 at 07:37Warren LeeSeptember 19th, 2019 at 10:48Ritu KothariSeptember 25th, 2019 at 15:10YCSMDSeptember 20th, 2019 at 03:16Deepak SoniSeptember 20th, 2019 at 22:28HogrenSeptember 25th, 2019 at 05:17