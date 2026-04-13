---
title: DOM MutationObserver – reacting to DOM changes without killing browser performance.
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/05/dom-mutationobserver-reacting-to-dom-changes-without-killing-browser-performance/
author: Jeff Griffiths
published: '2012-05-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[DOM Mutation Events](https://developer.mozilla.org/en/DOM/Mutation_events) seemed like a great idea at the time – as web developers create a more dynamic web it seems natural that we would welcome the ability to listen for changes in the DOM and react to them. In practice however DOM Mutation Events were a major performance and stability issue and have been deprecated for over a year.

The original idea behind DOM Mutation Events is still appealing, however, and so in September 2011 a group of Google and Mozilla engineers announced [a new proposal](http://lists.w3.org/Archives/Public/public-webapps/2011JulSep/1622.html) that would offer similar functionality with improved performance: [DOM MutationObserver](http://dvcs.w3.org/hg/domcore/raw-file/tip/Overview.html#mutation-observers). This new DOM Api is available in Firefox and Webkit nightly builds, as well as Chrome 18.

At it’s simplest, a MutationObserver implementation looks like this:

```
// select the target node
var target = document.querySelector('#some-id');
// create an observer instance
var observer = new MutationObserver(function(mutations) {
mutations.forEach(function(mutation) {
console.log(mutation.type);
});
});
// configuration of the observer:
var config = { attributes: true, childList: true, characterData: true }
// pass in the target node, as well as the observer options
observer.observe(target, config);
// later, you can stop observing
observer.disconnect();
```

The key advantage to this new specification over the deprecated DOM Mutation Events spec is one of efficiency. If you are observing a node for changes, your callback will not be fired until the DOM has finished changing. When the callback is triggered, it is supplied a list of the changes to the DOM, which you can then loop through and choose to react to.

This also means that any code you write will need to process the observer results in order to react to the changes you are looking for. Here is a compact example of an observer that listens for changes in an editable ordered list:

```
```
- Press enter


If you want to see this code running, I’ve put it up on jsbin here:

If you play with the live example, you’ll notice some quirks in behaviour, in particular that the callback is triggered when you press enter in each li, in particular when the user action results in a node being added or removed from the DOM. This is an important distinction to be made from other techniques such as binding events to key presses or more common events like ‘click’. MutationObservers work differently from these techniques because they are triggered by changes in the DOM itself, not by events generated either via JS or user interaction.

### So what are these good for?

I don’t expect most JS hackers are going to run out right now and start adding mutation observers to their code. Probably the biggest audience for this new api are the people that write JS frameworks, mainly to solve problems and create interactions they could not have done previously, or at least not with reasonable performance. Another use case would be situations where you are using frameworks that manipulate the DOM and need to react to these modifications efficiently ( and without setTimeout hacks! ).

Another common use of the Dom Mutation Events api is in browser extensions, and in the next week or so I’m going to publish a follow-up post on how MutationObservers are particularly useful when interacting with web content in a Firefox Add-on.

### Resources

[Original Proposal](http://lists.w3.org/Archives/Public/public-webapps/2011JulSep/1622.html)[W3C Spec](http://dvcs.w3.org/hg/domcore/raw-file/tip/Overview.html#mutation-observers)[Screencast](http://www.youtube.com/watch?feature=player_embedded&v=eRZ4pO0gVWw)by Rafael Weinstein[Mutation Summary](https://code.google.com/p/mutation-summary/), a JS library that simplifies MutationObserver usage.

## About
[
Jeff Griffiths ](http://canuckistani.ca/)

Jeff is Product Manager for the Firefox Developer Tools and occasional Open Web hacker, based in Vancouver, BC.

## 19 comments

smaugMay 11th, 2012 at 01:41Jeff GriffithsMay 11th, 2012 at 08:40Henri SivonenMay 11th, 2012 at 02:05Masatoshi KimuraJune 5th, 2012 at 10:18codevikingFebruary 15th, 2013 at 10:39DaoMay 11th, 2012 at 02:18Jeff GriffithsMay 11th, 2012 at 08:41David MulderMay 11th, 2012 at 02:25Jeff GriffithsMay 11th, 2012 at 08:45smaugMay 11th, 2012 at 07:11aaMay 15th, 2012 at 02:46Misha ReyzlinMay 22nd, 2012 at 02:35Robert NymanMay 22nd, 2012 at 02:36Robert HurstJune 17th, 2012 at 13:52Jeff GriffithsJune 18th, 2012 at 15:26DanMarch 25th, 2013 at 10:15muneerApril 7th, 2013 at 22:35Jeff GriffithsApril 8th, 2013 at 10:36ToRoApril 9th, 2013 at 10:01