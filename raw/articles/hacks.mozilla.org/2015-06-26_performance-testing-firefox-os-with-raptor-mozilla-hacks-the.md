---
title: Performance Testing Firefox OS With Raptor – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/06/performance-testing-firefox-os-with-raptor/
author: Eli Perelman
published: '2015-06-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When we talk about performance for the Web, a number of familiar questions may come to mind:

- Why does this page take so long to load?
- How can I optimize my JavaScript to be faster?
- If I make some changes to this code, will that make this app slower?

I’ve been working on making these types of questions easier to answer for Gaia, the UI layer for Firefox OS, a completely web-centric mobile device OS. Writing performant web pages for the desktop has its own idiosyncrasies, and writing native applications using web technologies takes the challenge up an order of magnitude. I want to introduce the challenges I’ve faced in making performance an easier topic to tackle in Firefox OS, as well as document my solutions and expose holes in the Web’s APIs that need to be filled.

*From now on, I’ll refer to web pages, documents, and the like as applications, and while web “documents” typically don’t need the performance attention I’m going to give here, the same techniques could still apply.*

## Fixing the lifecycle of applications

A common question I get asked in regard to Firefox OS applications:

How long did the app take to load?


Tough question, as we can’t be sure we are speaking the same language. Based on UX and my own research at Mozilla, I’ve tried at adopt this definition for determining the time it takes an application to load:

The amount of time it takes to load an application is measured from the moment a user initiates a request for the application to the moment the application appears ready for user interaction.


On mobile devices, this is generally from the time the user taps on an icon to launch an app, until the app appears visually loaded; when it **looks** like a user can start interacting with the application. Some of this time is delegated to the OS to get the application to launch, which is outside the control of the application in question, but the bulk of the loading time should be within the app.

### So `window load`

right?

With [SPAs (single-page applications)](https://en.wikipedia.org/wiki/Single-page_application), Ajax, script loaders, deferred execution, and friends, `window load`

doesn’t hold much meaning anymore. If we could merely measure the time it takes to hit `load`

, our work would be easy. Unfortunately, there is no way to *infer* the moment an application is visually loaded in a predictable way for everyone. Instead we rely on the apps to *imply* these moments for us.

For Firefox OS, I helped develop a series of conventional moments that are relevant to almost every application for implying its loading lifecycle (also documented as a [performance guideline](https://developer.mozilla.org/en-US/Apps/Build/Performance/Firefox_OS_app_responsiveness_guidelines#Implementation) on MDN):

**navigation loaded** (`navigationLoaded`

)

The application designates that its core chrome or navigation interface exists in the DOM and has been marked as ready to be displayed, e.g. when the element is not `display: none`

or any other functionality that would affect the visibility of the interface element.

**navigation interactive** (`navigationInteractive`

)

The application designates that the core chrome or navigation interface has its events bound and is ready for user interaction.

**visually loaded** (`visuallyLoaded`

)

The application designates that it is visually loaded, i.e., the “above-the-fold” content exists in the DOM and has been marked as ready to be displayed, again not `display: none`

or other hiding functionality.

**content interactive** (`contentInteractive`

)

The application designates that it has bound the events for the minimum set of functionality to allow the user to interact with “above-the-fold” content made available at `visuallyLoaded`

.

**fully loaded** (`fullyLoaded`

)

The application has been completely loaded, i.e., any relevant “below-the-fold” content and functionality have been injected into the DOM, and marked visible. The app is ready for user interaction. Any required startup background processing is complete and should exist in a stable state barring further user interaction.

The important moment is visually loaded. This correlates directly with what the user perceives as “being ready.” As an added bonus, using the `visuallyLoaded`

metric pairs nicely with camera-based performance verifications.

## Denoting moments

With a clearly-defined application launch lifecycle, we can denote these moments with the [User Timing API](https://bugzilla.mozilla.org/show_bug.cgi?id=782751), available in Firefox OS starting with v2.2:

```
window.performance.mark( string markName )
```


Specifically during a startup:

```
performance.mark('navigationLoaded');
performance.mark('navigationInteractive');
...
performance.mark('visuallyLoaded');
...
performance.mark('contentInteractive');
performance.mark('fullyLoaded');
```


You can even use the `measure()`

method to create a measurement between start and another mark, or even 2 other marks:

```
// Denote point of user interaction
performance.mark('tapOnButton');
loadUI();
// Capture the time from now (sectionLoaded) to tapOnButton
performance.measure('sectionLoaded', 'tapOnButton');
```


Fetching these performance metrics is pretty straightforward with `getEntries`

, `getEntriesByName`

, or `getEntriesByType`

, which fetch a collection of the entries. The purpose of this article isn’t to cover the usage of [User Timing](http://www.w3.org/TR/user-timing/) though, so I’ll move on.

Armed with the moment an application is visually loaded, we know how long it took the application to load because we can just compare it to—oh, wait, no. We don’t know the moment of user intent to launch.

While desktop sites may be able to easily procure the moment at which a request was initiated, doing this on Firefox OS isn’t as simple. In order to launch an application, a user will typically tap an icon on the Homescreen. The Homescreen lives in a process separate from the app being launched, and we can’t communicate performance marks between them.

## Solving problems with Raptor

Without the APIs or interaction mechanisms available in the platform to be able to overcome this and other difficulties, we’ve build tools to help. This is how the [Raptor performance testing tool](https://developer.mozilla.org/en-US/Firefox_OS/Automated_testing/Raptor) originated. With it, we can gather metrics from Gaia applications and answer the performance questions we have.

Raptor was built with a few goals in mind:

- Performance test Firefox OS without affecting performance. We shouldn’t need polyfills, test code, or hackery to get realistic performance metrics.
- Utilize web APIs as much as possible, filling in gaps through other means as necessary.
- Stay flexible enough to cater to the many different architectural styles of applications.
- Be extensible for performance testing scenarios outside the norm.

###### Problem: Determining moment of user intent to launch

Given two independent applications — Homescreen and any other installed application — how can we create a performance marker in one and compare it in another? Even *if* we could send our performance mark from one app to another, they are incomparable. According to [High-Resolution Time](http://www.w3.org/TR/hr-time/), the values produced would be monotonically increasing numbers from the moment of the page’s origin, which is different in each page context. These values represent the amount of time passed from one moment to another, and not to an absolute moment.

The first breakdown in existing performance APIs is that there’s no way to associate a performance mark in one app with any other app. Raptor takes a simplistic approach: log parsing.

Yes, you read that correctly. Every time Gecko receives a performance mark, it logs a message (i.e., to `adb logcat`

) and Raptor streams and parses the log looking for these log markers. A typical log entry looks something like this (we will decipher it later):

```
I/PerformanceTiming( 6118): Performance Entry: clock.gaiamobile.org|mark|visuallyLoaded|1074.739956|0.000000|1434771805380
```


The important thing to notice in this log entry is its origin: `clock.gaiamobile.org`

, or the Clock app; here the Clock app created its visually loaded marker. In the case of the Homescreen, we want to create a marker that is intended for a different context altogether. This is going to need some additional metadata to go along with the marker, but unfortunately the User Timing API [does not yet have that ability](https://github.com/w3c/user-timing/issues/3). In Gaia, we have adopted an `@`

convention to override the context of a marker. Let’s use it to mark the moment of app launch as determined by the user’s first tap on the icon:

```
performance.mark('appLaunch@' + appOrigin)
```


Launching the Clock from the Homescreen and dispatching this marker, we get the following log entry:

```
I/PerformanceTiming( 5582): Performance Entry: verticalhome.gaiamobile.org|mark|appLaunch@clock.gaiamobile.org|80081.169720|0.000000|1434771804212
```


With Raptor we change the context of the marker if we see this `@`

convention.

###### Problem: Incomparable numbers

The second breakdown in existing performance APIs deals with the incomparability of performance marks across processes. Using `performance.mark()`

in two separate apps will not produce meaningful numbers that can be compared to determine a length of time, because their values do not share a common absolute time reference point. Fortunately there is an absolute time reference that all JS can access: the Unix epoch.

Looking at the output of `Date.now()`

at any given moment will return the number of milliseconds that have elapsed since [January 1st, 1970](https://en.wikipedia.org/wiki/Unix_time). Raptor had to make an important trade-off: abandon the precision of high-resolution time for the comparability of the Unix epoch. Looking at the previous log entry, let’s break down its output. Notice the correlation of certain pieces to their User Timing counterparts:

- Log level and tag:
`I/PerformanceTiming`

- Process ID:
`5582`

- Base context:
`verticalhome.gaiamobile.org`

- Entry type:
`mark`

, but could be`measure`

- Entry name:
`appLaunch@clock.gaiamobile.org`

, the`@`

convention overriding the mark’s context - Start time:
`80081.169720`

, - Duration:
`0.000000`

, this is a mark, not a measure - Epoch:
`1434771804212`


For every performance mark and measure, Gecko also captures the epoch of the mark, and we can use this to compare times from across processes.

### Pros and Cons

Everything is a game of tradeoffs, and performance testing with Raptor is no exception:

- We trade high-resolution times for millisecond resolution in order to compare numbers across processes.
- We trade JavaScript APIs for log parsing so we can access data without injecting custom logic into every application, which would affect app performance.
- We currently trade a high-level interaction API,
[Marionette](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette), for low-level interactions using[Orangutan](https://github.com/wlach/orangutan)behind the scenes. While this provides us with transparent events for the platform, it also makes writing rich tests difficult. There are plans to improve this in the future by adding Marionette integration.

### Why log parsing

You may be a person that believes log parsing is evil, and to a certain extent I would agree with you. While I do wish for every solution to be solvable using a performance API, unfortunately this doesn’t exist yet. This is yet another reason why projects like Firefox OS are important for pushing the Web forward: we find use cases which are not yet fully implemented for the Web, poke holes to discover what’s missing, and ultimately improve APIs for everyone by pushing to fill these gaps with standards. Log parsing is Raptor’s stop-gap until the Web catches up.

### Raptor workflow

Raptor is a [Node.js module](https://github.com/mozilla-b2g/gaia/tree/master/tools/raptor) built into the Gaia project that enables the project to do performance tests against a device or emulator. Once you have the project dependencies installed, running performance tests from the Gaia directory is straightforward:

- Install the Raptor profile on the device; this configures various settings to assist with performance testing. Note: this is a different profile that will reset Gaia, so keep that in mind if you have particular settings stored.

`make raptor`

- Choose a test to run. Currently, tests are stored in
`tests/raptor`

in the Gaia tree, so some manual discovery is needed. There are plans to improve the command-line API soon. - Run the test. For example, you can performance test the cold launch of the Clock app using the following command, specifying the number of runs to launch it:

`APP=clock RUNS=5 node tests/raptor/launch_test`

- Observe the console output. At the end of the test, you will be given a table of test results with some statistics about the performance runs completed. Example:

```
[Cold Launch: Clock Results] Results for clock.gaiamobile.org
Metric Mean Median Min Max StdDev p95
-------------------------------- ------- ------- ------- ------- ------ -------
coldlaunch.navigationLoaded 214.100 212.000 176.000 269.000 19.693 247.000
coldlaunch.navigationInteractive 245.433 242.000 216.000 310.000 19.944 274.000
coldlaunch.visuallyLoaded 798.433 810.500 674.000 967.000 71.869 922.000
coldlaunch.contentInteractive 798.733 810.500 675.000 967.000 71.730 922.000
coldlaunch.fullyLoaded 802.133 813.500 682.000 969.000 72.036 928.000
coldlaunch.rss 10.850 10.800 10.600 11.300 0.180 11.200
coldlaunch.uss 0.000 0.000 0.000 0.000 0.000 n/a
coldlaunch.pss 6.190 6.200 5.900 6.400 0.114 6.300
```


### Visualizing Performance

Access to raw performance data is helpful for a quick look at how long something takes, or to determine if a change you made causes a number to increase, but it’s not very helpful for monitoring changes over time. Raptor has two methods for visualizing performance data over time, in order to improve performance.

##### Official metrics

At [raptor.mozilla.org](http://raptor.mozilla.org), we have dashboards for persisting the values of performance metrics over time. In our automation infrastructure, we execute performance tests against devices for every new build generated by mozilla-central or b2g-inbound (Note: The source of builds could change in the future.) Right now this is limited to Flame devices running at 319MB of memory, but there are plans to expand to different memory configurations and additional device types in the very near future. When automation receives a new build, we run our battery of performance tests against the devices, capturing numbers such as application launch time and memory at `fullyLoaded`

, reboot duration, and power current. These numbers are stored and visualized many times per day, varying based on the commits for the day.

Looking at these graphs, you can drill down into specific apps, focus or expand your time query, and do advanced query manipulation to gain insight into performance. Watching trends over time, you can even pick out regressions that have sneaked into Firefox OS.

##### Local visualization

The very same visualization tool and backend used by [raptor.mozilla.org](http://raptor.mozilla.org) is also available as a [Docker image](https://registry.hub.docker.com/u/eliperelman/raptor/). After running the local Raptor tests, data will report to your own visualization dashboard based on those local metrics. There are some additional prerequisites for local visualization, so be sure to read the [Raptor docs on MDN](https://developer.mozilla.org/en-US/Firefox_OS/Automated_testing/Raptor#Local_visualization) to get started.

### Performance regressions

Building pretty graphs that display metrics is all well and fine, but finding trends in data or signal within noise can be difficult. Graphs help us understand data and make it accessible for others to easily communicate around the topic, but using graphs for finding regressions in performance is reactive; we should be proactive about keeping things fast.

##### Regression hunting on CI

[Rob Wood](https://github.com/rwood-moz) has been doing incredible work in our pre-commit continuous integration efforts surrounding the detection of performance regressions in prospective commits. With every pull request to the [Gaia repository](https://github.com/mozilla-b2g/gaia/), our automation runs the Raptor performance tests against the target branch with and without the patch applied. After a certain number of iterations for statistical accuracy, we have the ability to reject patches from landing in Gaia if a regression is too severe. For scalability purposes we use emulators to run these tests, so there are inherent drawbacks such as greater variability in the metrics reported. This variability limits the precision with which we can detect regressions.

##### Regression hunting in automation

Luckily we have the post-commit automation in place to run performance tests against real devices, and is where the dashboards receive their data from. Based on the excellent [Python tool](https://github.com/wlach/phanalysis) from [Will Lachance](https://github.com/wlach), we query our historical data daily, attempting to discover any smaller regressions that could have crept into Firefox OS in the previous seven days. Any performance anomalies found are promptly reported to [Bugzilla](https://bugzilla.mozilla.org/buglist.cgi?emailreporter1=1&list_id=12346619&resolution=---&emailtype1=exact&query_format=advanced&email1=raptor%40mozilla.com) and relevant bug component watchers are notified.

## Recap and next steps

Raptor, combined with User Timing, has given us the know-how to ask questions about the performance of Gaia and receive accurate answers. In the future, we plan on improving the API of the tool and adding higher-level interactions. Raptor should also be able to work more seamlessly with third-party applications, something that is not easily done right now.

Raptor has been an exciting tool to build, while at the same time helping us drive the Web forward in the realm of performance. We plan on using it to keep Firefox OS fast, and to stay proactive about protecting Gaia performance.