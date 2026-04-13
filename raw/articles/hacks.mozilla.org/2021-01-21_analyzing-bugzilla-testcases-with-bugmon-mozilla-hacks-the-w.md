---
title: Analyzing Bugzilla Testcases with Bugmon – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2021/01/analyzing-bugzilla-testcases-with-bugmon/
author: Jason Kratzer
published: '2021-01-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/50ddcb5caba6ddbb.jpeg)


As a member of Mozilla’s fuzzing team, our job is not only to find bugs, but to do what we can to help get those bugs fixed as quickly as possible. Some of the many ways we can do that is by:

- Confirming the validity of new or stalled bugs
- Determining when a bug was introduced
- Verifying that a proposed fix does in fact remediate the issue

To further reduce the delay in getting these bugs fixed, we wanted to automate as much of this process as possible. This effort resulted in the development of [Bugmon](https://github.com/MozillaSecurity/bugmon); a tool that automates these basic triage tasks for Firefox and SpiderMonkey bugs directly in [Bugzilla](https://bugzilla.mozilla.org/).

Bugmon analysis is opt-in and only applies to crash or assertion bugs with a testcase. If you work on Firefox and are interested in having bugmon analyze your bugs, it’s as simple as adding the “bugmon” keyword.

## The Fuzzing Lifecycle

[Fuzzing](https://firefox-source-docs.mozilla.org/tools/fuzzing/index.html) is, in its most basic form, the process of supplying random bits of data to an application in the hopes of triggering unexpected behavior. In relation to Mozilla and those of us fuzzing Firefox, this *random data* often comes in the form of JavaScript, HTML, CSS, etc., and the *unexpected behavior* we’re looking for, often presents itself in the form of application crashes or fatal assertions.

When we identify issues like these, our first step is to notify the team which maintains the problematic code via a bug in [Bugzilla](http://bugzilla.mozilla.org/). When we file these bugs, we include as much relevant data as possible such as:

- A description of the issue
- A stack trace of the crash or assertion
- A testcase containing the
*random data*responsible for triggering the issue - And any additional information such as the tested revision, any build or runtime flags, as well as any required environment variables

*For a recent example of what this looks like, take a look at bug*[ 1682612](https://bugzilla.mozilla.org/show_bug.cgi?id=1682612)

*.*

Many people would consider that at this point, our job is done. The bug is in the hands of the developer and we can move on to breaking more code. Unfortunately for us, that’s not the case.

## A Bug’s Life

There are many reasons why, during the course of a bug’s life, we may be required to provide further information. Oftentimes, the exact cause of a bug may not be clear. Further, the owner of the problematic code may be equally unclear. In order to get our bug in the hands of those best able to fix it, we need to provide more information.

### Bisection

One useful technique that we can leverage is [bisection](https://en.wikipedia.org/wiki/Bisection_(software_engineering)). Bisection is the process of identifying the specific changeset that introduced the problematic behavior (i.e. the crash or the assertion). By identifying the changeset that introduced the bug, we can likely pinpoint not only the area which is responsible for the bug, but also the individual who last modified that code. Both of which can help us to get the bug fixed quicker.

But what happens if the bug is low priority and several weeks or months pass before a developer has a chance to review the bug?

### Confirmation

In these cases, it’s often helpful to determine if a bug still exists. To answer this, we will attempt to trigger the same issue using the original testcase attached to a bug. If the bug no longer reproduces, it’s likely that the bug has already been fixed. We can once again leverage bisection to identify the specific changeset responsible for fixing our bug.

### Verification

At this stage, the bug has been fixed. Success! Or, at least it appears to be. It’s important for us to verify that the original test case no longer triggers the problematic behavior. In these cases, we will once again attempt to trigger the same issue using the original test case. If the bug no longer reproduces, we can safely mark the bug as verified.

After repeating many of these tasks by hand, we quickly realized that we could automate much of the process to provide greater support to the developers tasked with fixing our bugs.

## Introducing Bugmon

[Bugmon](https://github.com/MozillaSecurity/bugmon) is specifically designed to automate many of these basic triage tasks. Originally conceived by [Christian Holler](https://twitter.com/mozdeco?lang=en) nearly 8 years ago as [JSBugMon](https://github.com/mozilla/JSBugMon) for the analysis of bugs affecting SpiderMonkey; Bugmon is a complete redesign of Christian’s efforts. This new approach leverages several additional tools developed by the fuzzing team such as [autobisect](https://github.com/MozillaSecurity/autobisect/), [fuzzfetch](https://github.com/MozillaSecurity/fuzzfetch), and [grizzly](https://github.com/MozillaSecurity/grizzly) to quickly and effectively apply this concept to both SpiderMonkey and Firefox bugs.

*A demo of bugmon processing a bug.*

## How It Works™

Bugmon will perform several automated tasks based on the current status of the bug.

### Confirmation

- Bugmon will automatically confirm the reproducibility of bugs where the status is equal to ASSIGNED, NEW, UNCONFIRMED, or REOPENED.
- Bugs that are confirmed as open will also be bisected.
- If the bug cannot be confirmed using the latest available build, Bugmon will attempt to confirm the bug using a build matching the original revision or a revision closest to the bug creation date. If this succeeds, Bugmon will attempt to bisect which changeset introduced the fix.

### Verification

- Bugmon will automatically confirm that the bug has been fixed where the bug status is RESOLVED and the resolution is FIXED.
- Bugmon will also iterate over the tracking flags and attempt to verify each branch marked as FIXED.

### Triggering Events

Occasionally you may want to trigger specific actions to be performed outside of the timeline described above. This may be because the original testcase no longer reproduces, or you think that the status of the bug may have changed since a prior Bugmon analysis.

In addition to it’s automatic parsing capabilities, bugmon actions can also be requested for immediate processing via the bug whiteboard.

## Next Steps

While the information provided by Bugmon is certainly helpful in getting bugs fixed quicker, there are a number of features we’d still like to implement.

Improvements to the bisection analysis stages may allow us to identify regressions down to a single code change. In these cases, we can automatically update the [relevant regression fields](https://bugzilla.mozilla.org/show_bug.cgi?id=1461492) which can then be leveraged by other Mozilla bots such as [autonag](https://wiki.mozilla.org/Release_Management/autonag). Additionally, we can automate requests for review by the author of the previously identified code change as they may likely be the best candidate to fix it.

Finally, one often requested feature is to include support for recording bugs with [rr](https://rr-project.org/). For those unfamiliar with rr; it is a timeless debugger which allows us to record application failures and replay them deterministically. In combination with [pernosco](https://pernos.co/), a web-based rr session browser, we can get these recordings into the hands of developers instantly and without any required setup on their part. Thus, reducing the overhead associated with hard to reproduce or intermittent bugs.

## Closing

We certainly hope that Bugmon helps reduce the time required to triage new bugs and effectively get bugs fixed faster. If there are specific use cases you have that are not currently supported by Bugmon we’d love to hear from you.

## 2 comments

Jeanderson CandidoJanuary 23rd, 2021 at 03:00Jason KratzerJanuary 25th, 2021 at 08:42