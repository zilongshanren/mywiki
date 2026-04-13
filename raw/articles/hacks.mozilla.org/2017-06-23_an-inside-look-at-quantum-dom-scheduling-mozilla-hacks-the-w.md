---
title: An inside look at Quantum DOM Scheduling – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/06/an-inside-look-at-quantum-dom-scheduling/
author: Bevis Tseng
published: '2017-06-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Use of multi-tab browsing is becoming heavier than ever as people spend more time on services like Facebook, Twitter, YouTube, Netflix, and Google Docs, making them a part of their daily life and work on the Internet.*

[Quantum DOM](https://wiki.mozilla.org/Quantum/DOM): *Scheduling is a significant piece of Project Quantum, which focuses on making Firefox more responsive, especially when lots of tabs are open. In this article, we’ll describe problems we identified in multi-tab browsing, the solutions we figured out, the current status of Quantum DOM, and opportunities for contribution to the project.*

## Problem 1: Task prioritization in different categories

Since [multiprocess Firefox (e10s)](https://developer.mozilla.org/en-US/Firefox/Multiprocess_Firefox) was first enabled in Firefox 48, web content tabs now run in separate **content processes** in order to reduce overcrowding of OS resources in a given process. However, after further research, we found that the task queue of **the main thread in the content process** was still crowded with tasks in multiple categories. The tasks in the content process can come from a number of possible sources: through IPC (interprocess communication) from the main process (e.g. for input events, network data, and vsync), directly from web pages (e.g. from setTimeout, requestIdleCallback, or postMessage), or internally in the content process (e.g. for garbage collection or telemetry tasks). For better responsiveness, we’ve learned to prioritize tasks for user inputs and vsync above tasks for requestIdleCallback and garbage collection.

## Problem 2: Lack of task prioritization between tabs

Inside Firefox, tasks running in foreground and background tabs are executed in [First-Come-First-Served](https://en.wikipedia.org/wiki/FIFO_%28computing_and_electronics%29) order, in a single task queue. It is quite reasonable to prioritize the foreground tasks over than the background ones, in order to increase the responsiveness of the user experience for Firefox users.

## Goals & solutions

Let’s take a look at how we approached these two scheduling challenges, breaking them into a series of actions leading to achievable goals:

- Classify and prioritize tasks on the main thread of the content processes in 2 dimensions (categories & tab groups), to provide better responsiveness.
- Preempt tasks that are running the background tabs if this preempting is not noticeable to the user.
- Provide an alternative to
[multiple content processes (e10s multi)](https://wiki.mozilla.org/Electrolysis/Multiple_content_processes)when fewer content processes are available due to limited resources.

## Task categorization

To resolve our first problem, we divide the task queue of the main thread in the content processes into 3 prioritized queues: ![](../../assets/261319379f4a8345.png)


**High**(User Input and Refresh Driver),

**Normal**(DOM Event, Networking, TimerCallback, WorkerMessage), and

**Low**(Garbage Collection, IdleCallback). Note: The order of tasks of the same priority is kept unchanged.

## Task grouping

Before describing the solution to our second problem, let’s define a **TabGroup** as a set of open tabs that are associated via `window.opener`

and `window.parent`

. In the HTML standard, this is called a [unit of related browsing contexts](https://html.spec.whatwg.org/multipage/browsers.html#unit-of-related-browsing-contexts). Tasks are isolated and cannot affect each other if they belong to different TabGroups. **Task grouping** ensures that tasks from the same TabGroup are run in order while allowing us to interrupt tasks from background TabGroups in order to run tasks from a foreground TabGroup.

In Firefox internals, each window/document contains a reference to the TabGroup object it belongs to, which provides [a set of useful dispatch APIs](http://searchfox.org/mozilla-central/rev/d840ebd5858a61dbc1622487c1fab74ecf235e03/xpcom/threads/SchedulerGroup.h#102-110). These APIs make it easier for Firefox developers to associate a task with a particular TabGroup.

### How tasks are grouped inside Firefox

Here are several examples to show how we group tasks in various categories inside Firefox:

- Inside the implementation of
`window.postMessage()`

, an asynchronous task called`PostMessageEvent`

will be dispatched to the task queue of the main thread:

```
void nsGlobalWindow::PostMessageMozOuter(...) {
...
RefPtr<PostMessageEvent> event = new PostMessageEvent(...);
NS_DispatchToCurrentThread(event);
}
```


With the new association of DOM windows to their TabGroups and the new dispatching API provided in TabGroup, we can now associate this task with the appropriate TabGroup and specify the `TaskCategory`

:

```
void nsGlobalWindow::PostMessageMozOuter(...) {
...
RefPtr<PostMessageEvent> event = new PostMessageEvent(...);
// nsGlobalWindow::Dispatch() helps to find the TabGroup of this window for dispatching.
Dispatch("PostMessageEvent", TaskCategory::Other, event);
}
```


- In addition to the tasks that can be associated with a TabGroup, there are several kinds of tasks inside the content process such as telemetry data collection and resource management via
**garbage collection**, which have no relationship to any web content. Here is how garbage collection starts:

```
void GCTimerFired() {
// A timer callback to start the process of Garbage Collection.
}
void nsJSContext::PokeGC(...) {
...
// The callback of GCTimerFired will be invoked asynchronously by enqueuing a task
// into the task queue of the main thread to run GCTimerFired() after timeout.
sGCTimer->InitWithFuncCallback(GCTimerFired, ...);
}
```


To group tasks that have no TabGroup dependencies, a special group called `SystemGroup`

is introduced. Then, the `PokeGC()`

method can be revised as shown here:

```
void nsJSContext::PokeGC(...) {
...
sGCTimer->SetEventTarget(SystemGroup::EventTargetFor(TaskCategory::GC));
sGCTimer->InitWithFuncCallback(GCTimerFired, ...);
}
```


We have now grouped this `GCTimerFired`

task to the `SystemGroup`

with `TaskCategory::GC`

specified. This allows the scheduler to interrupt the task to run tasks for any foreground tab.

- In some cases, the same task can be requested either by specific web content or by an internal Firefox script with system privileges in the content process. We’ll have to decide if the
`SystemGroup`

makes sense for a request when it is not tied to any window/document. For example, in the implementation of DNSService in the content process, an optional`TabGroup`

-versioned event target can be provided for dispatching the result callback after the DNS query is resolved. If the optional event target is not provided, the`SystemGroup`

event target in`TaskCategory::Network`

is chosen. We make the assumption that the request is fired from an internal script or an internal service which has no relationship to any window/document.

```
nsresult ChildDNSService::AsyncResolveExtendedNative(
const nsACString &hostname,
nsIDNSListener *listener,
nsIEventTarget *target_,
nsICancelable **result)
{
...
nsCOMPtr<nsIEventTarget> target = target_;
if (!target) {
target = SystemGroup::EventTargetFor(TaskCategory::Network);
}
RefPtr<DNSRequestChild> childReq =
new DNSRequestChild(hostname, listener, target);
...
childReq->StartRequest();
childReq.forget(result);
return NS_OK;
}
```


## TabGroup categories

Once the task grouping is done inside the [scheduler](https://bugzilla.mozilla.org/show_bug.cgi?id=1350432), we assign a cooperative thread per tab group from a pool to consume the tasks inside a `TabGroup`

. Each cooperative thread is pre-emptable by the scheduler via JS interrupt at any safe point. The main thread is then virtualized via these cooperative threads.

In this new cooperative-thread approach, we ensure that only one thread at a time can run a task. This allocates more CPU time to the foreground `TabGroup`

and also ensures internal data correctness in Firefox, which includes many services, managers, and data designed intentionally as singleton objects.

## Obstacles to task grouping and scheduling

It’s clear that the performance of Quantum-DOM scheduling is highly dependent on the work of task grouping. Ideally, we’d expect that each task should be associated with only one TabGroup. In reality, however, some tasks are designed to serve multiple TabGroups, which require refactoring in advance in order to support grouping, and not all the tasks can be grouped in time before scheduler is ready to be enabled. Hence, to enable the scheduler aggressively before all tasks are grouped, the following design is adopted to disable the preemption temporarily when an ungrouped task arrives because we never know which TabGroup this ungrouped task belongs to.

## Current status of task grouping

We’d like to send thanks to the many engineers from various sub-modules including DOM, Graphic, ImageLib, Media, Layout, Network, Security, etc., who’ve helped clear these [ungrouped (unlabeled) tasks](https://bugzilla.mozilla.org/show_bug.cgi?id=1321812) according to [the frequency shown in telemetry results](https://bugzilla.mozilla.org/show_bug.cgi?id=1333984#c11).

The table below shows telemetry records of tasks running in the content process, providing a better picture of what Firefox is actually doing:

The good news is that over 80% of tasks (weighted with frequency) have cleared recently. However, there are still a fair amount of anonymous tasks to be cleared. [Additional telemetry](https://bugzilla.mozilla.org/show_bug.cgi?id=1351021) will help check the mean time between 2 ungrouped tasks arriving to the main thread. The larger the mean time, the more performance gain we’ll see from Quantum-DOM Scheduler.

**Contribute to Quantum DOM development**

As mentioned above, the more tasks are grouped (labeled), the more benefit we gain from the scheduler. If you are interested in contributing to Quantum-DOM, here are some ways you can help:

- Pick any bug from
[labeling meta-bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1321812)without assignee and follow this[guideline](https://wiki.mozilla.org/Quantum/DOM#Q3:_What_runnables_shall_be_labeled.3F)for labeling. - If you are not familiar with these unlabeled bugs, but you want to help on naming the tasks to reduce the anonymous tasks in the
[telemetry result](https://bugzilla.mozilla.org/show_bug.cgi?id=1333984#c11)to improve the analysis in the future, this[guideline](https://wiki.mozilla.org/Quantum/DOM#Q7:_How_to_name_an_annoymous_runnable_before_supporting_.28Doc.7CTab.7CSystem.29Group_labeling.3F)will be helpful to you. (**Update**: Naming anonymous tasks are going to be addressed by some automation tool in[this bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1372405).)

If you get started fixing bugs and run into issues or questions, you can usually find the Quantum DOM team in Mozilla’s #content IRC channel.

## About Bevis Tseng

Bevis Tseng is a platform engineer at Mozilla who used to work on telephony-related features in Firefox OS (B2G). He has completed the enhancement of IndexedDB in Gecko for Spec v2 recently and now is involving in the task labeling for Quantum-DOM scheduler.