---
title: Porting Chrome Extensions to Firefox with WebExtensions – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2015/10/porting-chrome-extensions-to-firefox-with-webextensions/
author: Dan Callahan
published: '2015-10-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

After reading last month’s “[Let’s Write a Web Extension](https://hacks.mozilla.org/2015/09/lets_write_a_webextension/),” I was inspired to try and port a real-world add-on to a WebExtension. Specifically, I tried to port the Chrome version of the popular, open-source “[Reddit Enhancement Suite](http://redditenhancementsuite.com/)” (RES) to Firefox. Here’s what I learned, and what you can do today to prepare your own add-ons for the transition.


Note:The authors of RES are excited about WebExtensions and plan to officially port their add-on, butthis is not that. If you want to use RES, you should install the supported version from[AMO].

First, I want to stress that [WebExtensions](https://developer.mozilla.org/Add-ons/WebExtensions) are a long-term, multi-year project. Our first releases will be focused on building a foundation of basic, well-supported, cross-browser APIs. This means that it may take a while before we’re ready to support complex add-ons that rely on unique browser features, but we’ll get there eventually.

Because everything here is still *very* early and experimental, you’ll need to use a [Nightly build](https://nightly.mozilla.org/) of Firefox if you want to follow along. This is a sneak peek, not something you should plan on deploying.

That said, if you have a Chrome extension or a cross-browser add-on, now is a great time to experiment with WebExtensions and provide feedback. Your input will be crucial in helping Mozilla figure out which APIs to prioritize and initially support.

## Preparing to Port

- Download and install a
[Nightly build](https://nightly.mozilla.org/)of Firefox. - Create a
[new profile](https://support.mozilla.org/kb/profile-manager-create-and-remove-firefox-profiles)for testing and development. - Visit
`about:config`

and set`xpinstall.signatures.required`

to`false`

.

## Declaring Firefox Compatibility

You must explicitly mark your add-on as compatible with Firefox by adding an `applications`

key to your manifest.json. It looks like this:

```
"applications": {
"gecko": {
"id": "YOUR_ADDON_ID"
}
},
```


Set `"YOUR_ADDON_ID"`

to a made-up string formatted like `"ext@example.org"`

. If you plan on directly upgrading your users from an existing Firefox add-on to a WebExtension version of the same, you should re-use the value found in the `"id"`

field of your package.json.

## Checking Manifest Support

The next step is to compare the keys in your manifest.json to [the ones that Firefox supports](https://developer.mozilla.org/Add-ons/WebExtensions/Chrome_incompatibilities). Unsupported keys are ignored, so you can leave them in your manifest until we get around to implementing them, at which point they should Just Work.

Looking at [Reddit Enhancement Suite’s manifest](https://github.com/honestbleeps/Reddit-Enhancement-Suite/blob/6ddfad39da8b80097d981d182678bae6e777c0e2/Chrome/manifest.json), we’re in pretty good shape. The metadata attributes are all implemented, and there’s sufficient support for `background`

, `content_scripts`

, and `web_accessible_resources`

to work with RES.

Let’s look at what’s missing, and what impact it has:

`options_page`

: We’re OK without this since RES also injects a link to its settings via`content_scripts`

, rather than solely relying on the`options_page`

property.`page_action`

: We’re OK here, too. RES only uses the page action as a shortcut for toggling a checkbox that it injects into pages via`content_scripts`

.`permissions`

: All of the permissions that RES requests are supported except for`history`

, which hasn’t been implemented yet. RES only[uses the history API](https://github.com/honestbleeps/Reddit-Enhancement-Suite/blob/4ac07e6403de818af22d3822e460c260030e2028/Chrome/background.js#L234-L236)to mark links as visited[when previewing images inline](https://github.com/honestbleeps/Reddit-Enhancement-Suite/blob/d587bcbda88eae2f975d666f53a8c6d1ea91f245/lib/modules/showImages.js#L1652)from an “expando” button. Missing this means a slight degradation in functionality, but nothing catastrophic.`optional_permissions`

: We don’t yet support optional permissions, which for RES means we won’t support embedding inline previews from Twitter or OneDrive via expando buttons. Unfortunate, but not a showstopper.

At this point, I’m feeling pretty good about our prospects. Most of the APIs we need are supported, and we should be able to deliver most of RES’s functionality despite the handful of missing APIs.

## To Bugzilla!

Since we’ve identified some gaps in Firefox’s API coverage relative to our needs, it’s time to head to [Bugzilla](https://bugzilla.mozilla.org/). **Filing and voting for bugs are two of the most important contributions you can make as an add-on developer.** In addition to keeping you informed of progress, it helps us judge which APIs are the most important to implement.


Note:Bugzilla has a[somewhat esoteric]search syntax. To look for all open and closed WebExtension bugs that mentioned the`history`

API,[try searching]for`ALL Component:WebExtensions #history`

, which should turn up[Bug 1208334]: “Implement history API for open extension API.”

Since I’m writing this article, I’ve gone ahead and made sure bugs were filed for the above APIs. Feel free to CC yourself on these bugs if you want to be notified of their progress, or click the little “vote” link next to the “Importance” field if the bug is particularly important to you.

[Bug 1212684](https://bugzilla.mozilla.org/show_bug.cgi?id=1212684): Implement options_page manifest property for open extension API[Bug 1197422](https://bugzilla.mozilla.org/show_bug.cgi?id=1197422): Implement pageAction API for open extension API[Bug 1208334](https://bugzilla.mozilla.org/show_bug.cgi?id=1208334): Implement history API for open extension API[Bug 1197420](https://bugzilla.mozilla.org/show_bug.cgi?id=1197420): Implement permissions API and optional_permissions manifest property for open extension API

If you need to file a WebExtension bug, please file it against the “WebExtensions” component in the “Toolkit” product, and tag it with the “dev-doc-needed” keyword. This link should pre-fill all the right fields: [File a WebExtension Bug](https://bugzilla.mozilla.org/enter_bug.cgi?product=Toolkit&component=WebExtensions&keywords=dev-doc-needed).

## Grepping the Code

In addition to manifest properties, we also need to ensure that Firefox actually supports the APIs we need. We’ve set up a visual dashboard of API progress at [AreWeWebExtensionsYet.com](http://www.arewewebextensionsyet.com/), but for specifics you have to [go to MDN](https://developer.mozilla.org/Add-ons/WebExtensions/Chrome_incompatibilities). Since Chrome’s extension APIs are exposed as properties on a global `chrome`

object, we can run grep to find out what we use:

```
$ grep -r 'chrome\.' ./Chrome ./lib
./Chrome/background.js: chrome.tabs.sendMessage(event.id, { requestType: 'subredditStyle', action: 'toggle' }, function(response) {
./Chrome/background.js:chrome.pageAction.onClicked.addListener(handlePageActionClick);
./Chrome/background.js:chrome.runtime.onMessage.addListener(
# and so on...
```


Of the APIs that RES depends on, only a few are unimplemented:

**history**.addUrl**pageAction**.hide, onClicked, setIcon, and show**permissions**.remove, request**tabs**.getCurrent

Before diving into the code, let’s head back to [Bugzilla](https://bugzilla.mozilla.org/) and make sure bugs have been filed for these. The bugs mentioned above cover History, Page Actions, and Permissions, but they don’t cover `tabs.getCurrent`

. I’ve filed [Bug 1212890](https://bugzilla.mozilla.org/show_bug.cgi?id=1212890) for that.

## Hacks and Workarounds

Now that we’ve identified our limitations, we need to work around them. In the short term, we can just insert guards that check for the existence of an API before calling methods on it. For example, let’s look at how `history.addUrl`

is [used in background.js](https://github.com/honestbleeps/Reddit-Enhancement-Suite/blob/4ac07e6403de818af22d3822e460c260030e2028/Chrome/background.js#L234-L236):

```
case 'addURLToHistory':
chrome.history.addUrl({url: request.url});
break;
```


As long as `chrome.history.addUrl`

is undefined, this will throw an error. Instead, let’s check for its existence before we use it:

```
case 'addURLToHistory':
if (chrome.history && chrome.history.addUrl) {
chrome.history.addUrl({url: request.url});
}
break;
```


This keeps the script from blowing up, but it means that `addURLToHistory`

will silently fail until [Bug 1208334](https://bugzilla.mozilla.org/show_bug.cgi?id=1208334) gets resolved. Under certain circumstances, like with RES, this might be acceptable. If it’s not, you’ll need to find a creative workaround or wait for the relevant bug to get resolved. Remember: file and vote on bugs! It’s how we know what we need to work on.

Page actions are another great example: while it’s handy to have a button in the browser’s UI, you may also be able to provide the same functionality by using content scripts to inject custom UI into target pages until [Bug 1197422](https://bugzilla.mozilla.org/show_bug.cgi?id=1197422) is fixed.

Lastly, we could get around the lack of `permissions.request()`

by moving all of the `optional_permissions`

from our manifest.json up into the normal `permissions`

block. That *would* work, but it’s best not to require more permission than you need, and changing the `permissions`

stanza generally results in your users being prompted to re-authorize your add-on. If possible, just wait for [Bug 1197420](https://bugzilla.mozilla.org/show_bug.cgi?id=1197420).

## Packaging your WebExtension

We’re working on a better workflow in [Bug 1185460](https://bugzilla.mozilla.org/show_bug.cgi?id=1185460), but for now:

- Zip your files so that your manifest.json is at the root of the zip file.
- Rename it from
`.zip`

to`.xpi`

. - Navigate to
`about:addons`

. - Drag and drop your XPI onto the page.
- Click “Install” in the prompt.

If anything goes wrong, check out the [packaging and installation docs](https://developer.mozilla.org/Add-ons/WebExtensions/Packaging_and_installation) on MDN for troubleshooting tips.

## Testing it Out

Despite WebExtensions being a brand new initiative at Mozilla, we’ve already implemented most of the building blocks needed to support the Reddit Enhancement Suite. Things *should* work, as long as we’ve properly routed around unsupported API calls.

Let’s load it up and see if reality matches our expectations…

Hey! That looks good! Maybe it’s working? Let’s try the feature that loads more content when you scroll to the bottom of a page…

![Animation showing RES failing to load additional content when scrolling to the bottom of the page.](../../assets/0e4754848fc764ac.gif)


…no dice. :( So, what went wrong?

## Debugging

To find out what failed, we need to open up the Browser Console. It’s a global log of everything that happens in the browser, and it’s where uncaught exceptions from WebExtensions show up. It’s in the Developer menu.

Note: Though they are related, the

Browser Consoleisnotthe same thing as theWeb Consolein that menu.

Looking at the Browser Console, there’s an uncaught exception: “TypeError: window.Favico is not a constructor.”

This happens when [orangered.js](https://github.com/honestbleeps/Reddit-Enhancement-Suite/blob/d587bcbda88eae2f975d666f53a8c6d1ea91f245/lib/modules/orangered.js#L199-L200) calls:

`favicon = new window.Favico();`


The root cause of the bug is that the Favico library exports itself as `this.Favico`

in [its content script](https://github.com/honestbleeps/Reddit-Enhancement-Suite/blob/d587bcbda88eae2f975d666f53a8c6d1ea91f245/lib/vendor/favico.js#L839-L842), and RES assumes that it will then be available as `window.Favico`

in other scripts. It turns out that Firefox doesn’t work the same way. Off to Bugzilla to file [Bug 1208775](https://bugzilla.mozilla.org/show_bug.cgi?id=1208775)!

Fortunately, there’s an easy workaround: just omit the `window.`

part.

`favicon = new Favico();`


This gets us past that error and results in working infinite scrolling. Hooray! Also, kudos to RES for fixing this in pull request [#2465](https://github.com/honestbleeps/Reddit-Enhancement-Suite/pull/2465)!

Of course, we’re not done yet. There are many other fascinating and hilarious bugs to be found, like [Bug 1208874](https://bugzilla.mozilla.org/show_bug.cgi?id=1208874), which prevents RES from saving any of your settings because WebExtension localStorage is getting nuked every time the browser restarts. Boo!

Remember: Keep your Browser Console open and [file bugs](https://bugzilla.mozilla.org/enter_bug.cgi?product=Toolkit&component=WebExtensions&keywords=dev-doc-needed) when you find them!

## Wrapping Up

As I mentioned at the beginning of the article, WebExtensions are still very early in their development, and things are rapidly changing. For example, PageAction support should [land any day now](https://bugzilla.mozilla.org/show_bug.cgi?id=1197422). That said, WebExtensions are already astonishingly capable. For add-ons like RES that isolate and minimize browser-specific code, a port to WebExtensions is surprisingly close to being viable on Nightly builds of Firefox.

We’re still several months out from any of this landing in mainline Firefox, but it’s encouraging to see rapid progress. Each day we’re closer to a future in which a single add-on codebase can be fully re-used across many browsers, and where add-ons are written using the same technology as the Web itself.

If you want to follow along with the bugs that are blocking a port of RES to WebExtensions, CC yourself on the RES metabug at [Bug 1208765](https://bugzilla.mozilla.org/show_bug.cgi?id=1208765) and check out my own attempt at porting RES [on GitHub](https://github.com/callahad/res-webextension).

Lastly, consider contributing to Firefox! Everything we do is open source, and most WebExtension APIs are implemented in JavaScript. If you can hack JS, you can make a difference. Check out the [open WebExtension bugs](https://bugzilla.mozilla.org/buglist.cgi?component=WebExtensions&product=Toolkit&bug_status=__open__) and drop by the #webextensions channel on [irc.mozilla.org](https://wiki.mozilla.org/IRC) to get started.

Finally, a quick word of thanks to [Steve Sobel](https://twitter.com/honestbleeps), creator of the Reddit Enhancement Suite, who would like me to remind you that any port of RES to WebExtensions is *unfinished, unofficial, and unsupported* until he personally tells you otherwise. Don’t bug him about our bugs. ;-)

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 5 comments

niu techOctober 15th, 2015 at 08:02Dan CallahanOctober 15th, 2015 at 08:23RobertOctober 17th, 2015 at 21:48dimaOctober 31st, 2015 at 05:29Dan CallahanOctober 31st, 2015 at 05:43