---
title: Shipping a security update of Firefox in less than a day – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2018/03/shipping-a-security-update-of-firefox-in-less-than-a-day/
author: Sylvestre Ledru
published: '2018-03-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One of Mozilla’s top priorities is to keep our users safe; this commitment is written into [our mission](https://www.mozilla.org/en-US/mission/). As soon as we discover a critical issue in Firefox, we plan a rapid mitigation. This post will describe how we fixed a Pwn2Own exploit discovery in less than 22 hours, through the collaborative and well-coordinated efforts of a global cross-functional team of release and QA engineers, security experts, and other stakeholders.

[Pwn2Own](https://en.wikipedia.org/wiki/Pwn2Own) is an annual computer hacking contest. The goal of this event is to find security vulnerabilities in major software such as browsers. Last week, this event took place in Vancouver. Without getting into [technical details](https://www.zerodayinitiative.com/blog/2018/3/15/pwn2own-2018-day-two-results-and-master-of-pwn) of the exploit here, this blog post will describe how Mozilla responded quickly to ship updated builds of Firefox once an exploit was found during Pwn2Own.

We will share some of the processes that enable us to update and release a new version of the Firefox browser to hundreds of millions of users on a regular recurring basis.

This browser is a huge piece of software: 18 million+ lines of code, 6 platforms (Windows 32 & 64bit, GNU/Linux 32 & 64bit, Mac OS X and Android), 90 languages, plus installers, updaters, etc. Releasing such a beast involves coordination among many people from several cross-functional teams spanning locations such as San Francisco, Philadelphia, Paris, Cluj in Romania, and Rangiora in New Zealand.

The timing of the Pwn2Own event is known weeks beforehand, and so Mozilla is prepared! The [Firefox train release calendar](https://wiki.mozilla.org/RapidRelease/Calendar) takes into consideration the timing of Pwn2Own. We try not to ship a new version of Firefox to end users on the release channel on the same day as Pwn2Own.

## A Firefox Chemspill

A [chemspill](https://wiki.mozilla.org/Release_Management/Glossary#Chemspill) is a “*security-driven dot release of our product*.” It’s an internal name for the Mozilla machinery that produces updated builds of Firefox on all channels (Nightly, Beta, Release, ESR) in response to an event that negatively impacts browser stability or user security.

Our rapid response model is similar to the way emergency personnel organize and mobilize to deal with a chemical spill and its hazards. All key people stop working on their current tasks and focus only on the cleanup itself. Because our focus is our end users, we need to ensure that they are using the safest and fastest version of Firefox!

This year, we created a private Slack channel prior to Pwn2Own to coordinate all the activity related to the event. The initial Slack group consisted only of security experts, directors of engineering, senior engineers, release managers and release engineers – essential staff.

We prepared a release checklist in advance with added items and a specific focus on the potential for a chemspill triggered by Pwn2Own. This document helped track the cross-functional tasks, their owners, status and due date, which helped track individual tasks and the necessary coordination. It also helped stakeholders view and report chemspill status down to the minute.

One of the members of our security team was attending the Pwn2Own event. After it [was announced](https://twitter.com/thezdi/status/974332691330904064) that one of the participants, Richard Zhu, found the security issue in Firefox, this Mozilla representative received the exploit directly from Richard Zhu as part of the regular Pwn2Own disclosure process for affected vendors. The bug was added to our bug tracking system at **10:59AM PDT** on March 15th with the necessary privacy settings. Soon after, the chemspill team reviewed the issue and made a decision to ship updated builds ASAP.

In parallel, there was a discussion happening on the private Slack channel. When we saw [the tweet](https://twitter.com/HowellONeill/status/974330194591866881) from cybersecurity reporter [@howelloneill](https://twitter.com/HowellONeill/) that made the news public, we knew it was time to identify the developer who’d be getting to work on fixing the bug…

And so, quickly, the developer got to work.

## The fix: planning, risk analysis, go-live timelines

While engineers were investigating the exploit and coming up with a fix, the cross-functional coordination needed to ship updated builds had already begun. The chemspill team met within 2 hours of the event. We discussed the next steps in terms of fix readiness, test plans, go-to-build, QA sign-offs, and determined the sequence of steps along with rough timelines. We needed to ensure a smooth hand-off from folks in North America to folks in Europe (France, Romania, UK) and then back to California by morning.

From the moment we had information about the exploit, two discussions began in parallel: a technical discussion on the bug tracking system; and a release-oriented discussion, driven by the release and security managers, on the Slack channel.

12 minutes later, at **11:11AM**, a relevant developer is contacted.

**11:17AM**: The bug is updated to confirm that our long-term support release (ESR) has also been impacted by the issue.

**12:32PM**: Less than 3 hours after the disclosure, the developer provides a first patch addressing the issue.

**14:21PM**: An improved version of the fix is pushed.

**15:23PM**: This patch is pushed to the development branch. Then, in the next 70 minutes, we go through the process of getting the patch landed into the other release and pre-release repositories.

![](../../assets/5f9d2933795a8598.png)


**17:16PM**: Little more than 6 hours after the publication of the exploit, the Beta and Release builds (desktop and Android) are in progress.

## During the build phase

Let’s take a step back to describe the regular workflow that happens every time a new build of Firefox is released. Building the Firefox browser with our complete test suite for all platforms takes about 5 hours. While the builds are in progress, many teams are working in parallel.

### Test plan

The QA team designs a test plan with the help of engineering. When fixing security issues, we always have two goals in mind:

- Verify that the fix addresses the security issue,
- Catch any other potential regressions due to the fix.

With these two goals, the QA team aims to cover a wide range of cases using different inputs.

For example, the following test case #3 has been played on the various impacted versions and platforms:

*Test Case 3 (ogg enabled false – Real .ogg File)*

*Select a channel**Navigate to about:config**Set pref “media.ogg.enabled” to false**Download an .ogg file**Drag the .ogg file into the Mozilla build**Observe an error message/prompt “You have chosen to open [name of file].ogg**Try and open the file with Firefox as the application**Observe that Firefox does not play the selected .ogg file (or any sound)**Repeat step 1 for all builds (ESR, RC, Beta/DevEdition, Fennec)*

### Exploit analysis

In parallel, our security experts jumped on the exploit to analyze it.

They look closely at several things:

- How the exploit works technically
- How we could have detected the issue ourselves
- The
*in progress*efforts: How to mitigate this kind of attack - The
*stalled*efforts: What we started but didn’t finish - The
*future*efforts: Scoping the long term work to eliminate or mitigate this category of attacks

### Outreach

The vulnerability was found to be in a library that did not originate with the Mozilla project, and is used by other software. Because we didn’t want to [0-day](https://en.wikipedia.org/wiki/Zero-day_(computing)) the vulnerable software library and make the vulnerability more widely known, we reached out to the maintainer of the library directly. Then, we investigated which other applications use this code and we tried to notify them and make them aware of the issue.

In parallel, we worked with the library maintainers to prepare a new version of the standalone library code.

Last but not least, as GNU/Linux distributions provide packages of this library, we also informed these distributions about the issue.

## Once the builds are ready

After roughly 5 hours, the builds were ready. This is when the QA team starts executing the test plans.

They verify all the scenarios on a bunch of different platforms/operating systems.

In a matter of 22 hours, less than a day from when the exploit was found, Mozilla was ready to push updated builds of Firefox for Desktop and Android on our Nightly, Beta, ESR and release update channel.

For the *release go live*, the security team wrote the security advisories and created an entry for the [CVE](https://cve.mitre.org/) (Common Vulnerabilities and Exposures), a public reference that lists publicly known cybersecurity vulnerabilities.

And then, at the last moment, we discovered a second variant of the affected code and had to rebuild the Android version. This was also impacting Firefox ESR on ARM devices. We shipped this fix as well at **23:10PM**.

Nobody likes to see their product get [pwned](https://en.wikipedia.org/wiki/Pwn), but as with so much in software development, preparation and coordination can make the difference between a chemspill where no damage is done, and a potentially endangering situation.

Through the combined work of several distributed teams, and good planning and communication, Mozilla was able to test and release a fix for the vulnerability as fast as possible, ensuring the security of users around the world. That’s a story we think is worth sharing.

## Related Resources

If you’re interested in learning more about Mozilla’s security initiatives or Firefox security, here are some resources to help you get started:

[Mozilla Security](https://www.mozilla.org/en-US/security/)

[Mozilla Security Blog](https://blog.mozilla.org/security/)

[Bug Bounty Program
](https://www.mozilla.org/en-US/security/bug-bounty/)

[Mozilla Security playlist on YouTube](https://www.youtube.com/playlist?list=PLo3w8EB99pqIpX-NyaSResBdZqDpzv40K)

## 3 comments

SkatoxMarch 22nd, 2018 at 19:24harikrishnanMarch 29th, 2018 at 09:40Paul FindlayApril 4th, 2018 at 14:04