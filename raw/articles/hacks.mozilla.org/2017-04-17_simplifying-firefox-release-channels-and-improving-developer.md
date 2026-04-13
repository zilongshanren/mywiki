---
title: Simplifying Firefox Release Channels and Improving Developer Edition’s Stability
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/04/simplifying-firefox-release-channels/
author: Ali Spivak
published: '2017-04-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Streamlining our release process and quickly getting stable new features to users and developers is a priority for Firefox. Taking a close critical look at our release channels, it became clear that Aurora was not meeting our expectations as a first stabilization channel.

Starting on April 18, the Firefox Aurora channel will stop updating, and over the course of the next several months, the Aurora build will be removed from the train release cycle. [Developer Edition](https://developer.mozilla.org/en-US/Firefox/Developer_Edition) will be based on the Beta build. Developer Edition users will maintain their Developer Edition themes, tools, and preferences, will keep their existing profile, and should not experience any disruption.

This change benefits developers in several ways:

- Clearer choices in
[pre-release channels](https://www.mozilla.org/en-US/firefox/channel/desktop/)–[Nightly](https://www.mozilla.org/en-US/firefox/channel/desktop/#nightly)for experimental features and[Developer Edition/Beta](https://www.mozilla.org/en-US/firefox/developer/)for stability. - Higher quality and more stable environment for Developer Edition users.
- Faster release cycles for platform features. (Benefits everyone!)

Here’s the timeline: On April 18, code for Firefox 54 will move from Aurora to Beta as usual, while Firefox 55 will remain on Nightly for a second cycle in a row (a total of 14 weeks). On the next merge day, June 12, Firefox 55 will move directly from Nightly to Beta. Between April and June, Firefox Aurora on Desktop (54) will continue to receive updates for critical security issues and the Aurora and Developer Edition populations will be migrated to the Beta update channel. On Android, Aurora users will be migrated to Nightly.

Aurora was originally created in 2011 to provide more user feedback after Firefox shifted from version 5 to the high-speed release cycle. Today, in 2017, we have more modern processes underlying our train model, and believe we can deliver feature-rich, stable products without the additional 6-8 week Aurora phase.

A staged rollout mechanism, similar to what we do today with Release, will be used for the first weeks of Beta. Our engineering and release workflow will continue to have additional checks and balances rolled out to ensure we ship a high quality release. A new feature will merge from Nightly to Beta only when it’s deemed ready, based on preestablished criteria determined by our engineering, product and product integrity teams. If features are not ready, they won’t migrate from Nightly to Beta.

New tools and processes will include:

- Static analyzers integrated as part of the workflow, in order to detect issues during the review phase. They will be able to identify potential defects while minimizing technical debt.
- Code coverage results will be used to analyze the quality of the test-suite and the risk introduced by the change.
- The ability to identify potential risks carried by changes before they even land by correlating various data sources (VCS, Bugzilla, etc.) in order to identify functions where a modification is more likely to induce a regression.
- Monitoring crash rates, QE’s sign offs, telemetry data and new regressions to determine overall Nightly quality and feature readiness to merge to Beta.

For a deeper dive into transition details, please see the Mozilla [Release Management blog](
http://release.mozilla.org/firefox/release/2017/04/17/Dawn-Project-FAQ.html) for in-depth answers to the most common questions about this change.

## About Ali Spivak

[@alispivak](https://twitter.com/alispivak). Ali is the head of Developer Ecosystem at Mozilla, and has been developing and managing web sites for longer than she cares to admit. She's passionate about keeping the web open and working on things developers love (like MDN).

## About Dave Camp

Dave Camp is Director of Engineering for Firefox at Mozilla.

## 19 comments

DimasApril 17th, 2017 at 09:29SylvestreApril 25th, 2017 at 05:14Benjamin KerensaApril 17th, 2017 at 10:08Šime VidasApril 17th, 2017 at 12:36CharlesApril 17th, 2017 at 19:19Bryan ClarkApril 18th, 2017 at 12:33FranzApril 18th, 2017 at 06:11Ali SpivakApril 18th, 2017 at 07:18Robin BerjonApril 20th, 2017 at 06:55M Edward/Ed Borasky (@znmeb)April 20th, 2017 at 13:25Dan CallahanApril 21st, 2017 at 12:52clemApril 22nd, 2017 at 03:13OriolApril 24th, 2017 at 10:38YvanMay 1st, 2017 at 10:57Dan CallahanMay 3rd, 2017 at 16:19ElonasMay 1st, 2017 at 11:16Dan CallahanMay 3rd, 2017 at 16:21IbrahimMay 3rd, 2017 at 15:25Dan CallahanMay 3rd, 2017 at 16:29