---
title: Web Animation tools, Network Security insights, Font Inspector improvements
  and more – Firefox Developer Tools Episode 37 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/01/web-animation-tools-network-security-insights-font-inspector-improvements-and-more-firefox-developer-tools-episode-37/
author: Jordan Santell
published: '2015-01-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A [handful](https://bugzilla.mozilla.org/buglist.cgi?resolution=FIXED&classification=Client%20Software&chfieldto=2015-01-12&chfield=resolution&query_format=advanced&chfieldfrom=2014-11-28&chfieldvalue=FIXED&bug_status=RESOLVED&bug_status=VERIFIED&component=Developer%20Tools&component=Developer%20Tools%3A%203D%20View&component=Developer%20Tools%3A%20Canvas%20Debugger&component=Developer%20Tools%3A%20Console&component=Developer%20Tools%3A%20Debugger&component=Developer%20Tools%3A%20Framework&component=Developer%20Tools%3A%20Graphic%20Commandline%20and%20Toolbar&component=Developer%20Tools%3A%20Inspector&component=Developer%20Tools%3A%20Memory&component=Developer%20Tools%3A%20Netmonitor&component=Developer%20Tools%3A%20Object%20Inspector&component=Developer%20Tools%3A%20Profiler&component=Developer%20Tools%3A%20Responsive%20Mode&component=Developer%20Tools%3A%20Scratchpad&component=Developer%20Tools%3A%20Source%20Editor&component=Developer%20Tools%3A%20Storage%20Inspector&component=Developer%20Tools%3A%20Style%20Editor&component=Developer%20Tools%3A%20Timeline&component=Developer%20Tools%3A%20User%20Stories&component=Developer%20Tools%3A%20Web%20Audio%20Editor&component=Developer%20Tools%3A%20WebGL%20Shader%20Editor&component=Developer%20Tools%3A%20WebIDE&product=Firefox&list_id=11849042) of bug fixes, improvements and some new features, of course, just landed in Firefox 37. Update your [Firefox Developer Edition](https://www.mozilla.org/firefox/developer/), or [Nightly](https://nightly.mozilla.org/) builds to try them out!

## Animation Inspector Panel

A new API that’s quickly gaining traction is the [Web Animations API](https://w3c.github.io/web-animations/), allowing developers to construct more complex animations using web technologies, rather than proprietary plugins. The foundation for animation tooling has begun in Firefox’s Developer Tools, with the first release revealing play/pause controls and a timeline scrubber. When selecting an element in the [Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector), an **animations** panel is now available alongside the **rules**, **fonts**, and other panels, if the element contains animations. Check out [other videos](https://www.youtube.com/watch?v=s7LQrpB6Fi8) of the animation inspector in action, or try it yourself in this [web animation demo](https://bgrins.github.io/devtools-demos/inspector/animation-timing.html).

This is the first iteration of the web animation tools, and we are looking to hear from you on where we should go with this, and what we should build! Share [detailed feedback](http://mzl.la/devtools) with us on UserVoice, leave us a comment right here, or tweet to @FirefoxDevTools. (More detail on how to reach us in the closing paragraph below.)

## Security Panel


The [Network Monitor](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor) is the home of our other new tool, the security panel. Selecting a request in the network panel now displays a security panel in the request inspector. The panel reveals a list of information about the request’s connection, host, as well as the certificate used.

The security panel can help debug issues related to SSL protocol versions, such as sites not working because of the [POODLEBITE issue](https://bugzilla.mozilla.org/show_bug.cgi?id=1085138), and can help ensure that sufficiently strong security measures are implemented.

![DevTools Security Panel, new in Firefox 37](../../assets/a715613c50c287e3.png)


Some other features and small improvements in this release:

[Font inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector#Fonts_view)now shows all fonts (including fonts in iframes) when clicking “show all fonts” button. ([Bug 1097150](https://bugzil.la/1097150))- Addons can now register custom actors. (
[Bug 1107888](https://bugzil.la/1107888)) - The
[inspector sidebar](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector#CSS_pane)now loads and refreshes lazily, leading to better performance of the inspector. ([Bug 1103993](https://bugzil.la/1103993)) [Box Model Highlighter](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector#Box_model_view)colors have been updated so they are easier to see on a wider range of backgrounds, as well as more accessible. ([Bug 989053](https://bugzil.la/989053))- A new Firefox CLI option was added, –start-debugging-server, for starting the Firefox debugging server on a specific port. (
[Bug 1119894](https://bugzil.la/1119894)) - The tools tabbar height has decreased to allow more vertical space in the toolbox. (
[Bug 1109288](https://bugzil.la/1109288))

As we mentioned above, your feedback guides our priorities. Add your comments here, talk to us on Twitter [@FirefoxDevTools](http://twitter.com/firefoxdevtools), or propose changes on the [Developer Tools feedback channel](http://mzl.la/devtools). If you’d like to help out with Dev Tools, check out the [guide to getting involved](https://wiki.mozilla.org/DevTools/GetInvolved).

## About
[
Jordan Santell ](http://jsantell.com)

Mozillian, audio tools & SDK hacker, web audio nerd, metal head

## 2 comments

James FinnJanuary 25th, 2015 at 09:26CallahadJanuary 27th, 2015 at 12:47