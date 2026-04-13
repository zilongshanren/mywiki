---
title: 'Firefox 58: The Quantum Era Continues – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2018/01/firefox-58-the-quantum-era-continues/
author: Sergi Mansilla
published: '2018-01-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

2017 was a big year for Mozilla, culminating in the release of Firefox Quantum, a massive multi-year retooling of the browser focused on speed, and laying the groundwork for the years to come. In 2018, we’ll build on that incredible foundation, and in that spirit our next several releases will continue to bear the Quantum moniker. Let’s take a look at some of the new goodies that Firefox 58 brings.

## Gecko Engine Performance

Project Quantum is all about modernizing Gecko, Firefox’s rendering engine. Several significant changes have shipped already in Firefox 57 and its predecessors, and we’ve [covered](https://hacks.mozilla.org/2017/08/inside-a-super-fast-css-engine-quantum-css-aka-stylo/) [them](https://hacks.mozilla.org/2017/04/firefox-53-quantum-compositor-compact-themes-css-masks-and-more/) [here](https://hacks.mozilla.org/2017/06/an-inside-look-at-quantum-dom-scheduling/) on this blog. More are yet to come, or are shipping incrementally over the course of 2018. In addition to the banner parts of Quantum, we’re constantly working to streamline and speed up elements of the browsing experience. Here are a few improvements that have landed in the latest Firefox.

### Off-Main-Thread Painting (OMTP)

![Off-Main-Thread Paint diagram showing individual frames.](../../assets/c5bb1acfa53f03f3.png)


[Quantum Render](https://hacks.mozilla.org/2017/10/the-whole-web-at-maximum-fps-how-webrender-gets-rid-of-jank/) (or WebRender) is a major graphical system overhaul that’s coming to Firefox this year, and it promises hardware-accelerated painting of web content with huge performance wins. But it’s not the only graphics performance work we’ve been up to! In Firefox 58, the painting process (the act of actually drawing all the pixels of a web page) has been moved to its own thread.

The main thread of a browser is always a scarce commodity. It runs the page’s scripts, responds to user input, and maintains the current state of the page. Prior to OMTP (Off-Main-Thread Painting), the current state of the page was converted to drawing commands, and the pixel data of the whole page was generated (or rasterized) on the main thread. This meant the performance-critical tasks of scrolling or animation or script could be interrupted, or that a script could cause dropped frames or “jank”.

With OMTP on the other hand, the visual state of the page is still computed on the main thread, but the potentially costly task of rasterization is passed off to a designated “rasterization thread”, and the main thread can carry on and stay responsive.

Even after work on WebRender is complete and enabled in Firefox, there are many situations where hardware acceleration is not available or drivers have bugs that could (ahem) render WebRender unavailable. OMTP will provide a significantly better experience than the current rendering process.

OMTP is the culmination of years of incremental work to modernize the graphics infrastructure, and we’re pumped that users will get a significantly improved experience as a result. If you want to know more about OMTP or want to see some early performance numbers, there’s a [blog post with lots more detail](https://mozillagfx.wordpress.com/2017/12/05/off-main-thread-painting/).

### Keeping Firefox Focused with Background Tab Throttling

To reduce CPU usage overall, Firefox 58 will begin throttling the timers (specifically `setTimeout`

/`setInterval`

) in background tabs. These timers will still fire, but at a reduced rate. Exceptions exist for WebRTC/WebSocket connections as well as audio playback. The specifics are [available on MDN](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API#Policies_in_place_to_aid_background_page_performance).

### WebAssembly Streaming Compiler

![](https://hacks.mozilla.org/wp-content/uploads/2018/01/ezgif-5-73711fc5d3.gif)

[WebAssembly](https://hacks.mozilla.org/2017/02/a-cartoon-intro-to-webassembly/) is a portable binary compilation format designed to run on the web platform, with darn-near-native runtime performance. Several toolchains, like the Rust compiler and the Unity Engine, already support exporting directly to WebAssembly binaries. The biggest challenge with large binary payloads is their download size, and traditional plugin-based web runtimes like Flash need to download the entire bundle before it can be run.

Fortunately, WebAssembly was designed for a networked environment like the web! Firefox 58 takes advantage by adding support for streaming compilation. This means that the browser can begin compiling for the computer before the download is even complete. Once the compiler is up to speed, your module can be ready to use nearly instantly after it’s done downloading.

Lin Clark wrote (and illustrated!) a [much deeper write-up on streaming compilation for WebAssembly](https://hacks.mozilla.org/2018/01/making-webassembly-even-faster-firefoxs-new-streaming-and-tiering-compiler/), and it’s a great bit of reading even if you’re familiar with WebAssembly already. You can also find a full [WebAssembly reference](https://developer.mozilla.org/en-US/docs/WebAssembly) on MDN.

## CSS Font Display

Webfonts and the [ @font-face directive](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face) allow for immense customization of typography on the web. However, even with the latest compressed font formats, file sizes can be large. This can lead to long loading times during which users will see either the text of a site rendered in a system fallback font (FOUT) or no text at all (FOIT). Different browsers have different default behaviors, and it can be hard to get the behavior just right for a site and its users.

The [ font-display descriptor](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display) was introduced to let a site choose the proper font-loading behavior on a font-by-font basis. One may have body text immediately render in a fallback system font, while an icon font or display type can wait to fallback giving a stylized or symbolic font a chance to properly load.

Given that this is the Firefox 58 announcements post, it’s a bit redundant to say that `font-display`

is now available in Firefox. It is added to individual `@font-face`

blocks and takes one of several values:

`auto`

is the default and lets the browser use its normal fallback/hidden text strategy.`block`

tells the browser to render invisible text for a short duration and then fallback. If at any point in the future the webfont loads successfully, the text will switch to the new font.`swap`

immediately renders text in a fallback font, but will wait an arbitrary length of time for the font to load like`block`

.`fallback`

shortens the time the browser will render hidden text, after which the fallback will render. If the font still hasn’t loaded after an additional short period, the browser won’t bother swapping in the font, even if it eventually loads.`optional`

uses the same short hidden text waiting time as`fallback`

, but eliminates the eventual swapping entirely. If the font hasn’t loaded by the end of the hidden text timeout, a fallback font will be used for the rest of the page session. Better luck next load!

Different use cases will warrant different preferences. A highly designed magazine-style layout may want to wait as long as necessary to load the elaborate type it needs, and a news site rendering on mobile may elect treat its webfont as a nice-to-have.

## New Promise feature to reduce redundant code

[Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) were introduced in ES2015, and allow for a standardized way to write asynchronous code and handle success and error cases. Firefox 58 includes the new standard `.finally()`

method to include code to be run regardless of whether a Promise was resolved or rejected. Take the following short snippet:

```
showLoadingSpinner();
fetch('data.json')
.then(data => {
renderContent(data);
hideLoadingSpinner();
})
.catch(error => {
displayError(error);
hideLoadingSpinner();
});
```


The code repeats `hideLoadingSpinner()`

because we want to remove the spinner whether `loadPage()`

succeeds or not. `.finally()`

lets us not repeat ourselves:

```
showLoadingSpinner();
fetch('data.json')
.then(data => {
renderContent(data);
})
.catch(error => {
displayError(error);
})
.finally(() => {
hideLoadingSpinner();
});
```


It’s a little thing, but there’s a reason Don’t Repeat Yourself is a mantra for code. [Read more about .finally() on MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/finally).

## Add to Home screen available on Firefox for Android

“Progressive Web Apps” is a term for a group of modern web technologies that let you enhance a well-built website to deliver an experience that feels at home on your device alongside native applications. Firefox 58 for Android introduces improved support for Progressive Web Apps by letting users install compatible websites to the Home screen of their mobile devices. Here’s a quick look at why we’re excited about these new capabilities:

When a Firefox 58 user arrives on a website that is served over HTTPS and has a valid manifest, a subtle badge will appear in the address bar: when tapped, an “Add to Home screen” confirmation dialog will slide in, through which the web app can be added to the Android home screen. When launched from there, the web app will be shown in the configured view mode and orientation, and it will appear as a separate entry in the app switcher.

You can find a basic guide on MDN — see

[Add to Home screen].Another neat feature is how external links are handled: when a user is browsing an installed progressive web app and taps an external link, the page in question is opened in a Custom Tab. This keeps the user secure as the URL and safety information are visible, speeds up page load time (a Custom Tab loads faster than the full browser), preserves the progressive web app’s color branding, and is in line with native app behavior.

In upcoming releases, we plan to add more support for other PWA-related APIs: our Background Sync implementation is well underway (currently targeting Firefox 59), and we’re quite excited about the Payment Request and Web Share APIs as well.


You can learn more in the rest of [Andreas Bovens’ post](https://hacks.mozilla.org/2017/10/progressive-web-apps-firefox-android/), and (of course) read more about [Progressive Web Apps on MDN](https://developer.mozilla.org/en-US/Apps/Progressive).

## That’s Not All!

In addition to these high-level features, there’s plenty more in Firefox 58. Check the [official release notes](https://www.mozilla.org/en-US/firefox/58.0/releasenotes/) or MDN’s [feature-by-feature breakdown for developers](https://developer.mozilla.org/en-US/Firefox/Releases/58).

Lots more to come in Firefox this year; see you all in six weeks!

## 5 comments

zakiusJanuary 23rd, 2018 at 08:57Mark AdamsJanuary 24th, 2018 at 03:31PotchJanuary 24th, 2018 at 09:24Marcy SuttonJanuary 24th, 2018 at 08:28PotchJanuary 24th, 2018 at 09:17