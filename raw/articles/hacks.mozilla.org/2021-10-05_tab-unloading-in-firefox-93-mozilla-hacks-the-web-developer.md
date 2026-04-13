---
title: Tab Unloading in Firefox 93 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/10/tab-unloading-in-firefox-93/
author: Haik Aftandilian
published: '2021-10-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Starting with Firefox 93, Firefox will monitor available system memory and, should it ever become so critically low that a crash is imminent, Firefox will respond by unloading memory-heavy but not actively used tabs. This feature is currently enabled on Windows and will be deployed later for macOS and Linux as well. When a tab is unloaded, the tab remains in the tab bar and will be automatically reloaded when it is next selected. The tab’s scroll position and form data are restored just like when the browser is restarted with the *restore previous windows* browser option.

On Windows, out-of-memory (OOM) situations are responsible for a significant number of the browser and content process crashes reported by our users. Unloading tabs allows Firefox to save memory leading to fewer crashes and avoids the associated interruption in using the browser.

We believe this may especially benefit people who are doing heavy browsing work with many tabs on resource-constrained machines. Or perhaps those users simply trying to play a memory-intensive game or using a website that goes a little crazy. And of course, there are the tab hoarders, (no judgement here). Firefox is now better at surviving these situations.

We have experimented with tab unloading on Windows in the past, but a problem we could not get past was that finding a balance between decreasing the browser’s memory usage and annoying the user because there’s a slight delay as the tab gets reloaded, is a rather difficult exercise, and we never got satisfactory results.

We have now approached the problem again by refining our low-memory detection and tab selection algorithm and narrowing the action to the case where we are sure we’re providing a user benefit: if the browser is about to crash. Recently we have been conducting an experiment on our Nightly channel to monitor how tab unloading affects browser use and the number of crashes our users encounter. We’ve seen encouraging results with that experiment. We’ll continue to monitor the results as the feature ships in Firefox 93.

With our experiment on the Nightly channel, we hoped to see a decrease in the number of OOM crashes hit by our users. However, after the month-long experiment, we found an overall significant decrease in browser crashes and content process crashes. Of those remaining crashes, we saw an *increase* in OOM crashes. Most encouragingly, people who had tab unloading enabled were able to use the browser for longer periods of time. We also found that average memory usage of the browser *increased.*

The latter may seem very counter-intuitive, but is easily explained by survivorship bias. Much like in the [archetypal example of the Allied WWII bombers with bullet holes](https://en.wikipedia.org/wiki/Survivorship_bias#In_the_military), browser sessions that had such high memory usage would have crashed and burned in the past, but are now able to survive by unloading tabs just before hitting the critical threshold.

The increase in OOM crashes, also very counter-intuitive, is harder to explain. Before tab unloading was introduced, Firefox already responded to Windows memory-pressure by triggering an internal memory-pressure event, allowing subsystems to reduce their memory use. With tab unloading, this event is fired after all possible unloadable tabs have been unloaded.

This may account for the difference. Another hypothesis is that it’s possible our tab unloading sometimes kicks in a fraction too late and finds the tabs in a state where they can’t even be safely unloaded any more.

For example, unloading a tab requires a garbage collection pass over its JavaScript heap. This needs some additional temporary storage that is not available, leading to the tab crashing instead of being unloaded but still saving the entire browser from going down.

We’re working on improving our understanding of this problem and the relevant heuristics. But given the clearly improved outcomes for users, we felt there was no point in holding back the feature.

## When does Firefox automatically unload tabs?

When system memory is critically low, Firefox will begin automatically unloading tabs. Unloading tabs could disturb users’ browsing sessions so the approach aims to unload tabs only when necessary to avoid crashes. On Windows, Firefox gets a notification from the operating system (setup using [CreateMemoryResourceNotification](https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-creatememoryresourcenotification)) indicating that the available physical memory is running low. The threshold for low physical memory is not documented, but appears to be around 6%. Once that occurs, Firefox starts periodically checking the commit space ([MEMORYSTATUSEX.ullAvailPageFile](https://docs.microsoft.com/en-us/windows/win32/api/sysinfoapi/ns-sysinfoapi-memorystatusex)).

When the commit space reaches a low-memory threshold, which is defined with the preference “browser.low_commit_space_threshold_mb”, Firefox will unload one tab, or if there are no unloadable tabs, trigger the Firefox-internal memory-pressure warning allowing subsystems in the browser to reduce their memory use. The browser then waits for a short period of time before checking commit space again and then repeating this process until available commit space is above the threshold.

We found the checks on commit space to be essential for predicting when a real out-of-memory situation is happening. As long as there is still swap AND physical memory available, there is no problem. If we run out of physical memory and there is swap, performance will crater due to paging, but we won’t crash.

On Windows, allocations fail and applications will crash if there is low commit space in the system even though there is physical memory available because Windows does not overcommit memory and can refuse to allocate virtual memory to the process in this case. In other words, unlike Linux, Windows always requires commit space to allocate memory.

How do we end up in this situation? If some applications allocate memory but do not touch it, Windows does not assign the physical memory to such untouched memory. We have observed graphics drivers doing this, leading to low swap space when plenty of physical memory is available.

In addition, [crash data](https://bugzilla.mozilla.org/show_bug.cgi?id=1711610) we collected indicated that a surprising number of users with beefy machines were in this situation, some perhaps thinking that because they had a lot of memory in their machine, the Windows swap could be reduced to the bare minimum. You can see why this is not a good idea!

## How does Firefox choose which tabs to unload first?

Ideally, only tabs that are no longer needed will be unloaded and the user will eventually restart the browser or close unloaded tabs before ever reloading them. A natural metric is to consider when the user has last used a tab. Firefox unloads tabs in least-recently-used order.

Tabs playing sound, using picture-in-picture, pinned tabs, or tabs using WebRTC (which is used for video and audio conferencing sites) are weighted more heavily so they are less likely to be unloaded. Tabs in the foreground are never unloaded. We plan to do more experiments and continue to tune the algorithm, aiming to reduce crashes while maintaining performance and being unobtrusive to the user.

## about:unloads

For diagnostic and testing purposes, a new page about:unloads has been added to display the tabs in their unload-priority-order and to manually trigger tab unloading. This feature is currently in beta and will ship with Firefox 94.

![Screenshot of the about:unloads page in beta planned for Firefox 94.](../../assets/9e8fc58ad937aac4.png)

Screenshot of the about:unloads page in beta planned for Firefox 94.

## Browser Extensions

Some browser extensions already offer users the ability to unload tabs. We expect these extensions to interoperate with automatic tab unloading as they use the same underlying [tabs.discard() API](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/discard). Although it may change in the future, today automatic tab unloading only occurs when system memory is critically low, which is a low-level system metric that is not exposed by the WebExtensions API. (Note: an extension could use the [native messaging support](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging) in the WebExtensions API to accomplish this with a separate application.) Users will still be able to benefit from tab unloading extensions and those extensions may offer more control over when tabs are unloaded, or deploy more aggressive heuristics to save more memory.

Let us know how it works for you by leaving feedback on [ideas.mozilla.org](https://ideas.mozilla.org) or [reporting a bug](https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox&component=Tabbed+Browser). For support, visit [support.mozilla.org](https://support.mozilla.org).Firefox crash reporting and telemetry adheres to our [data privacy principles](https://www.mozilla.org/en-US/privacy/principles/). See the [Mozilla Privacy Policy](https://www.mozilla.org/en-US/privacy/) for more information.

*Thanks to Gian-Carlo Pascutto, Toshihito Kikuchi, Gabriele Svelto, Neil Deakin, Kris Wright, and Chris Peterson, for their contributions to this blog post and their work on developing tab unloading in Firefox.*

## 19 comments

UristqwertyOctober 5th, 2021 at 12:53BelaOctober 5th, 2021 at 18:50Haik AftandilianOctober 5th, 2021 at 20:41Reik RedOctober 7th, 2021 at 13:17mooseOctober 5th, 2021 at 23:52Gian-Carlo PascuttoOctober 7th, 2021 at 05:56Reik RedOctober 7th, 2021 at 13:24Cookie EngineerOctober 5th, 2021 at 20:56zakiusOctober 6th, 2021 at 03:23Reik RedOctober 7th, 2021 at 13:01zakiusOctober 6th, 2021 at 02:38martixyOctober 6th, 2021 at 03:08Janio SarmentoOctober 6th, 2021 at 03:32DanOctober 6th, 2021 at 09:53DmitryOctober 7th, 2021 at 00:37Haik AftandilianOctober 7th, 2021 at 14:09Reik RedOctober 7th, 2021 at 12:46Reik RedOctober 7th, 2021 at 13:20Joel CrumplerNovember 4th, 2021 at 07:38