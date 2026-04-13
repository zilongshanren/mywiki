---
title: Improved Process Isolation in Firefox 100 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2022/05/improved-process-isolation-in-firefox-100/
author: Gian-Carlo Pascutto
published: '2022-05-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Introduction**

Firefox uses a [multi-process model](https://hacks.mozilla.org/2021/05/introducing-firefox-new-site-isolation-security-architecture/) for additional security and stability while browsing: Web Content (such as HTML/CSS and Javascript) is rendered in separate processes that are isolated from the rest of the operating system and managed by a privileged parent process. This way, the amount of control gained by an attacker that exploits a bug in a content process is limited.

Ever since we deployed this model, we have been working on improving the isolation of the content processes to further limit the attack surface. This is a challenging task since content processes need access to some operating system APIs to properly function: for example, they still need to be able to talk to the parent process.

In this article, we would like to dive a bit further into the latest major milestone we have reached: *Win32k Lockdown,* which greatly reduces the capabilities of the content process when running on Windows. Together with two major earlier efforts ([Fission](https://hacks.mozilla.org/2021/05/introducing-firefox-new-site-isolation-security-architecture/) and [RLBox](https://hacks.mozilla.org/2021/12/webassembly-and-back-again-fine-grained-sandboxing-in-firefox-95/)) that shipped before, this completes a sequence of large leaps forward that will significantly improve Firefox’s security.

Although *Win32k Lockdown* is a Windows-specific technique, it became possible because of a significant re-architecting of the Firefox security boundaries that Mozilla has been working on for around four years, which allowed similar security advances to be made on other operating systems.

**The Goal: Win32k Lockdown**

Firefox runs the processes that render web content with quite a few restrictions on what they are allowed to do when running on Windows. Unfortunately, by default they still have access to the entire Windows API, which opens up a large attack surface: the Windows API consists of many parts, for example, a core part dealing with threads, processes, and memory management, but also networking and socket libraries, printing and multimedia APIs, and so on.

Of particular interest for us is the *win32k.sys API,* which includes many graphical and widget related system calls that have a history of being exploitable. Going back further in Windows’ origins, this situation is likely the result of Microsoft moving many operations that were originally running in user mode into the kernel in order to improve performance around the Windows 95 and NT4 timeframe.

Having likely never been originally designed to run in this sensitive context, these APIs have been a traditional target for hackers to break out of application sandboxes and into the kernel.

In Windows 8, Microsoft introduced a new mitigation named [PROCESS_MITIGATION_SYSTEM_CALL_DISABLE_POLICY](https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-process_mitigation_system_call_disable_policy) that an application can use to disable access to win32k.sys system calls. That is a long name to keep repeating, so we’ll refer to it hereafter by our internal designation: “*Win32k Lockdown*“.

**The Work Required**

Flipping the Win32k Lockdown flag on the Web Content processes – the processes most vulnerable to potentially hostile web pages and JavaScript – means that those processes can no longer perform any graphical, window management, input processing, etc. operations themselves.

To accomplish these tasks, such operations must be remoted to a process that has the necessary permissions, typically the process that has access to the GPU and handles compositing and drawing (hereafter called the GPU Process), or the privileged parent process.

### Drawing web pages: WebRender

For painting the web pages’ contents, Firefox historically used various methods for interacting with the Windows APIs, ranging from using modern Direct3D based textures, to falling back to GDI surfaces, and eventually dropping into pure software mode.

These different options would have taken quite some work to remote, as most of the graphics API is off limits in Win32k Lockdown. The good news is that as of Firefox 92, our rendering stack has switched to [WebRender](https://hacks.mozilla.org/2017/10/the-whole-web-at-maximum-fps-how-webrender-gets-rid-of-jank/), which moves all the actual drawing from the content processes to WebRender in the GPU Process.

Because with WebRender the content process no longer has a need to directly interact with the platform drawing APIs, this avoids any Win32k Lockdown related problems. WebRender itself has been designed partially to be [more similar to game engines, and thus, be less susceptible to driver bugs](https://github.com/servo/webrender/wiki/).

For the remaining drivers that are just too broken to be of any use, it still has a [fully software-based mode](https://bugzilla.mozilla.org/show_bug.cgi?id=1601053), which means we have no further fallbacks to consider.

### Webpages drawing: Canvas 2D and WebGL 3D

The [Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API) provides web pages with the ability to draw 2D graphics. In the original Firefox implementation, these JavaScript APIs were executed in the Web Content processes and the calls to the Windows drawing APIs were made directly from the same processes.

In a Win32k Lockdown scenario, this is no longer possible, so [all drawing commands are remoted](https://bugzilla.mozilla.org/show_bug.cgi?id=1464032) by recording and playing them back in the GPU process over IPC.

Although the initial implementation had good performance, there were nevertheless reports from some sites that experienced performance regressions (the web sites that became faster generally didn’t complain!). A particular pain point are applications that call [getImageData()](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/getImageData) repeatedly: having the Canvas remoted means that GPU textures must now be obtained from another process and sent over IPC.

We compensated for this in the scenario where getImageData is called at the start of a frame, by detecting this and preparing the right surfaces proactively to make the copying from the GPU faster.

Besides the Canvas API to draw 2D graphics, the web platform also exposes an [API to do 3D drawing, called WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API). WebGL is a state-heavy API, so properly and efficiently synchronizing child and parent (as well as parent and driver) takes [great](https://phabricator.services.mozilla.com/D54019) [care](https://phabricator.services.mozilla.com/D54019).

WebGL originally handled all validation in Content, but with access to the GPU and the associated attack surface removed from there, we needed to craft a robust validating API between child and parent as well to get the full security benefit.

### (Non-)Native Theming for Forms

HTML web pages have the ability to display form controls. While the overwhelming majority of websites provide a [custom look and styling for those form controls](https://developer.mozilla.org/en-US/docs/Learn/Forms/Advanced_form_styling), not all of them do, and if they do not you get an input GUI widget that is styled like (and originally was!) a [native element of the operating system](http://stephenhorlander.com/form-controls.html).

Historically, these were drawn by calling the appropriate OS widget APIs from within the content process, but those are not available under Win32k Lockdown.

This cannot easily be fixed by remoting the calls, as the widgets themselves come in an infinite amount of sizes, shapes, and styles can be interacted with, and need to be responsive to user input and dispatch messages. We settled on having Firefox [draw the form controls itself](https://bugzilla.mozilla.org/show_bug.cgi?id=1381938), in a cross-platform style.

While changing the look of form controls has web compatibility implications, and some people prefer the more native look – on the few pages that don’t apply their own styles to controls – Firefox’s approach is consistent with that taken by other browsers, probably because of very similar considerations.

Scrollbars were a particular pain point: we didn’t want to draw the main scrollbar of the content window in a different manner as the rest of the UX, since nested scrollbars would show up with different styles which would look awkward. But, unlike the rather rare non-styled form widgets, the main scrollbar is visible on most web pages, and because it conceptually belongs to the browser UX we really wanted it to look native.

We, therefore, decided to draw all scrollbars to match the system theme, although it’s a bit of an open question though how things should look if even [the vendor of the operating system can’t seem to decide what the “native” look is](https://bugzilla.mozilla.org/show_bug.cgi?id=1719427#c3).

**Final Hurdles**

### Line Breaking

With the above changes, we thought we had all the usual suspects that would access graphics and widget APIs in win32k.sys wrapped up, so we started running the full Firefox test suite with win32k syscalls disabled. This caused at least one unexpected failure: Firefox was [crashing when trying to find line breaks](https://bugzilla.mozilla.org/show_bug.cgi?id=1713973) for some languages with complex scripts.

While Firefox is able to correctly determine word endings in multibyte character streams for most languages by itself, the support for Thai, Lao, Tibetan and Khmer is known to be imperfect, and [in these cases, Firefox can ask the operating system to handle the line breaking](https://searchfox.org/mozilla-central/rev/80f11ac5d938f6fce255c56279f46f13a49ea5c3/intl/lwbrk/LineBreaker.h#65) for it. But at least on Windows, the functions to do so are covered by the Win32k Lockdown switch. Oops!

There are [efforts underway to incorporate ICU4X](https://bugzilla.mozilla.org/show_bug.cgi?id=1684927) and base all i18n related functionality on that, meaning that Firefox will be able to handle all scripts perfectly without involving the OS, but this is a major effort and it was not clear if it would end up delaying the rollout of win32k lockdown.

We did some experimentation with trying to forward the line breaking over IPC. Initially, this had bad performance, but when we [added caching](https://phabricator.services.mozilla.com/D129125) performance was satisfactory or sometimes even improved, since OS calls could be avoided in many cases now.

### DLL Loading & Third Party Interactions

Another complexity of disabling win32k.sys access is that so much Windows functionality assumes it is available by default, and specific effort must be taken to ensure the relevant DLLs do not get loaded on startup. Firefox itself for example won’t load the user32 DLL containing some win32k APIs, but [injected third party DLLs sometimes do](https://bugzilla.mozilla.org/show_bug.cgi?id=1719212). This causes problems because [COM initialization in particular uses win32k calls to get the Window Station and Desktop](https://bugzilla.mozilla.org/show_bug.cgi?id=1751367) if the DLL is present. Those calls will fail with Win32k Lockdown enabled, silently breaking COM and features that depend on it such as our accessibility support.

On Windows 10 Fall Creators Update and later we have a fix that blocks these calls and forces a fallback, which keeps everything working nicely. We measured that [not loading the DLLs causes about a 15% performance gain](https://bugzilla.mozilla.org/show_bug.cgi?id=1750742#c9) when opening new tabs, adding a nice performance bonus on top of the security benefit.

### Remaining Work

As hinted in the previous section, Win32k Lockdown will initially roll out on Windows 10 Fall Creators Update and later. On Windows 8, and unpatched Windows 10 (which unfortunately seems to be in use!), we are still testing a fix for the case where third party DLLs interfere, so support for those will come in a [future release](https://bugzilla.mozilla.org/show_bug.cgi?id=1759167#c7).

For Canvas 2D support, we’re still [looking into improving the performance of applications](https://bugzilla.mozilla.org/show_bug.cgi?id=1766402) that regressed when the processes were switched around. Simultaneously, there is experimentation underway to see if hardware acceleration for [Canvas 2D can be implemented through WebGL](https://bugzilla.mozilla.org/show_bug.cgi?id=1739448), which would increase code sharing between the 2D and 3D implementations and take advantage of modern video drivers being better optimized for the 3D case.

**Conclusion**

Retrofitting a significant change in the separation of responsibilities in a large application like Firefox presents a large, multi-year engineering challenge, but it is absolutely required in order to advance browser security and to continue keeping our users safe. We’re pleased to have made it through and present you with the result in Firefox 100.

### Other Platforms

If you’re a Mac user, you might wonder if there’s anything similar to Win32k Lockdown that can be done for macOS. You’d be right, and I have good news for you: we already quietly [shipped the changes that block access to the WindowServer](https://bugzilla.mozilla.org/show_bug.cgi?id=1467758) in Firefox 95, improving security and speeding process startup by about 30-70%. This too became possible because of the Remote WebGL and Non-Native Theming work described above.

For Linux users, [we removed the connection from content processes to the X11 Server](https://bugzilla.mozilla.org/show_bug.cgi?id=1129492), which stops attackers from exploiting the unsecured X11 protocol. Although Linux distributions have been moving towards the more secure Wayland protocol as the default, we still see a lot of users that are using X11 or XWayland configurations, so this is definitely a nice-to-have, which shipped in Firefox 99.

**We’re Hiring**

If you found the technical background story above fascinating, I’d like to point out that our OS Integration & Hardening team is going to be hiring soon. We’re especially looking for experienced C++ programmers with some interest in Rust and in-depth knowledge of Windows programming.

If you fit this description and are interested in taking the next leap in Firefox security together with us, [we’d encourage you to keep an eye on our careers page](https://www.mozilla.org/en-US/careers/).

*Thanks to Bob Owen, Chris Martin, and Stephen Pohl for their technical input to this article, and for all the heavy lifting they did together with Kelsey Gilbert and Jed Davis to make these security improvements ship.
*

## 5 comments

PeterMay 12th, 2022 at 15:51TobiasMay 16th, 2022 at 04:30Gian-Carlo PascuttoMay 16th, 2022 at 07:58Gian-Carlo PascuttoMay 23rd, 2022 at 10:38MarcoMay 27th, 2022 at 05:28