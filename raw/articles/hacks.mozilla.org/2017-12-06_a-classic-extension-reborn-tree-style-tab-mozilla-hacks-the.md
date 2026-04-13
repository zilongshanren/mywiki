---
title: 'A Classic Extension Reborn: Tree Style Tab – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2017/12/webextension-tree-style-tab/
author: Judy McConnell
published: '2017-12-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Yuki “Piro” Hiroshi is a trailblazer and a true do-it-yourselfer. Whenever the Tokyo-based programmer gets irritated with any aspect of his browsing experience, he builds a workaround for himself and shares it with others. After authoring nearly 100 browser extensions, Piro recently took on his **biggest challenge yet: migrating the legacy Tree Style Tab (TST) extension to work with the new WebExtensions API and Firefox Quantum.*

*TST on the legacy XUL platform was a very complicated extension. So rebuilding it for the new WebExtensions API had a lot of unique challenges. Piro hit a number of snags and frustrations, including undocumented behaviors and bugs. What helped? A positive frame of mind and a laser-sharp focus on the capabilities of the new APIs. Working within the context of the new platform, Piro was able to complete the extension and bring a crowd favorite to the fastest Firefox yet.*

*Want more technical detail? Check out Piro’s post WebExtensions Migration Story of Tree Style Tab for his strategies, code snippets, and architectural diagrams of the XUL and WebExtensions platforms.*

**How You Got Started**

**Q: What browser did you first create an extension for?
**I wrote my first extension for Mozilla Application Suite, before Firefox was born.

**Q: What extensions have you created for Firefox?
**

[Tree Style Tab](https://addons.mozilla.org/en-US/firefox/addon/tree-style-tab/?src=userprofile),

[Multiple Tab Handler](https://addons.mozilla.org/en-US/firefox/addon/multiple-tab-handler/?src=userprofile),

[Text Link](https://addons.mozilla.org/en-US/firefox/addon/text-link/?src=userprofile), and many others. My extensions mainly aim to change Firefox’s behavior, rather than offering completely new features.

**Q: How many extensions have you created for Firefox?
**I’ve written nearly 100 extensions for Firefox and Thunderbird. About half of those are purely for my personal use. I’ve published around 40, mostly legacy XUL extensions, and most of them are not migrated to WebExtensions yet.

**Q: Where can we find your extensions?
**My published extensions are on

[addons.mozilla.org](https://addons.mozilla.org/firefox/user/piro-piro_or/). You can find older extensions, including unlisted extensions, on

[my website](http://piro.sakura.ne.jp/xul/xul.html.en).

![Tree Style Tab extension for Firefox](../../assets/4b74b20cccc5af79.gif)


![Tree Style Tab extension for Firefox](../../assets/4b74b20cccc5af79.gif)

## More about Your Project

**Q: Why did you create your extensions? What problem were you trying to solve?
**My motivation was to make it easier to browse the web. When I encounter any small trouble or inconvenience, I create a new extension as a workaround.

**Q: How many years have you been working with extensions?
**Sixteen years. My first extension was released in November 2001.

**Q: How has the technology changed during that time?
**There have been changes to Firefox itself, like improvements in the Gecko rendering engine and JavaScript engine. And there have been new Web standard technologies like CSS3, ES6, and others. Recently, I learned the

[async-await](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/async_function)syntax while developing WebExtensions. Those new technologies help me clean up “dirty” or “hacky” code and maintain it more easily.

**Q: Did you migrate your extension from XUL to WebExtensions? How difficult was that process?
**I migrated Tree Style Tab, a large XUL extension, to a WebExtension. It was very difficult, to be honest. The most difficult part was the feature triage. Due to limitations of the WebExtensions APIs, some features were definitely not migratable. Making those decisions was painful for me.

It was also hard to detect the moment when my extension should cancel and override Firefox’s default behavior. As I mentioned earlier, most of my extensions are created to change Firefox’s behavior. But the WebExtensions API provides only limited entry points, so I often have to guess what’s happening in Firefox at any given moment, based on information like the order of events.

**Q: What resources were most helpful when implementing Firefox extensions?
**For researching how to implement extensions in XUL, I used

[DXR](http://dxr.mozilla.org/), the online search system for source code of Mozilla products. For WebExtensions, I looked at the source code of other existing WebExtensions and Google Chrome extensions.

**Q: What sites or tools helped you learn about the WebExtensions API?**

[MDN Web Docs](https://developer.mozilla.org/en-US/Add-ons/WebExtensions) is still the first entry point. Additionally I think links to the source code of existing extensions will help new extension authors, like an inverted dictionary.

## Your Experience with WebExtensions

**Q: What new technology in Firefox Quantum helped you with migration?
**Mozilla introduced many new WebExtensions APIs in Firefox 57 [Quantum], such as the

`openerTabId`

property for tabs. The opener information is highly relevant for Tree Style Tab. If those APIs were not available, Tree Style Tab couldn’t be migrated successfully.**Q: On a scale of 1 to 10, with 1 being the easiest, how difficult was it to write to the WebExtensions APIs?
**In general, it was a 2 or 3. WebExtensions APIs are simple enough and clear for extensions that just add a new button, sidebar, or other unique feature to Firefox. However, there are some undocumented behaviors on edge cases, and they might be closely tied to a specific Firefox release you’re working on. If you’re writing extensions that change Firefox’s behavior, you will need to dig into those undocumented behaviors.

**Q: Now that you’ve moved to WebExtensions, what do you like about it?
**I like the stability of the APIs. Generally, WebExtensions APIs are guaranteed to be compatible with Firefox, now and in the future. So I can develop long-lived extensions with no fear about breakage in future releases.

**Q: How long did it take you to write this extension?
**I started to develop the WebExtensions-based version of Tree Style Tab in late August 2017 and released it in November 2017. Of course, some parts of the tree management functionality were imported from the legacy XUL version, which I developed between 2007 and 2017.

**Q: How difficult is it to debug Firefox extensions?
**Today that is very easy to learn. Most extension authors don’t need to become experts of Firefox-specific technologies, especially XUL and XPCOM. Moreover, the

[about:debugging](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Debugging)feature of Firefox itself is very helpful for debugging of extensions. A command-line tool called

[web-ext](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Getting_started_with_web-ext)is also helpful for debugging and publishing.

**Q: How is adoption of your Tree Style Tab extension?
**Most people seem to welcome the new WebExtension-based version. Some say that Tree Style Tab is the main reason why they use Firefox. And they are excited now that TST is available for Firefox 57 [Quantum] and future releases.

**Q: What problems, if any, did you experience while developing a your extension? How were those problems resolved?
**Because the WebExtensions API is still under active development, I did find some bugs while developing the new Tree Style Tab extension, on edge cases. I reported those bugs in

[Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Toolkit&component=WebExtensions:%20Untriaged). With WebExtensions, problems due to API limitations are basically impossible to fix. Workarounds are available only in a few cases. So reporting to Bugzilla and waiting for the fix is the only thing extension authors can do.

However, that is good news when viewed from another perspective. In legacy XUL extensions, authors could do anything, including replacing Firefox’s internal XPCOM components. As a result, the boundaries of an extension and the author’s responsibility could be widened infinitely, and authors would have to make decisions on all the feature requests from users: to do them or not. That troubled me a lot. But, with WebExtensions, authors can just say, “It is impossible due to the API limitations.” I think this is a very helpful and important change in WebExtensions.

**Q: What advice would you give to others porting to WebExtensions?
**Try to simplify your development tasks. If you want to port a multi-feature extension, think about putting each feature into a separate extension, instead of trying to put them all into one single extension. You can make those extensions interact with each other by using API methods that are either implicit (based on shared information like properties

`tabs.Tab`

and `openerTabId`

) or explicit (based on custom messages for `runtime.sendMessage()`

).Stay focused on the results you want, instead of worrying how you will get it done. You may not be able to fully reproduce the behavior of your XUL extension in the new WebExtensions version. For instance, old method-based synchronous (blocking) APIs are no longer available, and raw DOM events on Firefox UI are no longer “listenable”. So you need to forget how you used to do things, and learn what is the normal approach in the WebExtensions world. You can probably find a better way to go about it, and still get to the same results. Then you’ll successfully dive into the new world, and you’ll have an awesome experience!

## Related Content

[WebExtensions Migration Story of Tree Style Tab
](http://piro.sakura.ne.jp/latest/blosxom/mozilla/extension/treestyletab/2017-10-03_migration-we-en.htm)

[Why Firefox Had to Kill Your Favorite Extension](https://www.howtogeek.com/333230/why-firefox-had-to-kill-your-favorite-extension/)

[Q&A with Grammarly’s Sergey Yavnyi](https://medium.com/mozilla-tech/grammarly-firefox-webextensions-a2b41afc2cfb)

[Q&A with Add-on Developer Stefan Van Damme](https://blog.mozilla.org/addons/2017/11/08/qa-developer-stefan-van-damme/)


[Remaking Lightbeam as a Browser Extension](https://hacks.mozilla.org/2017/10/remaking-lightbeam-as-a-browser-extension/)

[Cross-browser extensions, available now in Firefox](https://hacks.mozilla.org/2017/06/cross-browser-extensions-available-now-in-firefox/)


## About Judy McConnell

Judy is a Technical Writer working with Mozilla. She has written about open source software for many years and now focuses on the open web platform.

## 5 comments

RomanDecember 7th, 2017 at 03:54LampDecember 7th, 2017 at 06:04Alex Che KorotkinDecember 7th, 2017 at 10:46Mike ConcaDecember 7th, 2017 at 15:15BrendanDecember 7th, 2017 at 17:12