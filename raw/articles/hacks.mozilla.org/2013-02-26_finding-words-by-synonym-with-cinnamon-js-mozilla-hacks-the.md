---
title: Finding Words by Synonym with Cinnamon.js – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/02/finding-words-by-synonym-with-cinnamon-js/
author: Thomas Park
published: '2013-02-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There are only two hard things in Computer Science: cache invalidation and naming things.

— Phil Karlton


Naming things in web development is hard too, from evolving CSS classes to headers and links. From the perspective of information architecture, headers and links serve as visual waypoints, helping users build mental models of a site and navigate from page to page.

But a second, underappreciated role that header and link names play is through the browser’s built-in Find function. I can only speak from personal experience — and maybe I’m the exception to the rule — but I often rely on Find to do existence checks on in-page content and quickly jump to it.

Sometimes Find falls short though. For instance, consider a visitor that likes your site and decides to subscribe to your RSS feed. They search the page for “RSS” but nothing comes up. The problem is that you named your link “Feed” or “Subscribe”, or used the RSS symbol. They shrug their shoulders and move on — and you’ve lost a potential follower.

I wrote [Cinnamon.js](https://github.com/thomaspark/cinnamon.js) to ease the pain of naming things, by having Find work with synonyms ([demo](http://thomaspark.me/2013/02/cinnamon-js-find-in-page-text-using-synonyms/)).

## Try It Out

To use Cinnamon.js, you can simply include the script on your page:

Then wrap your word with synonyms, separated by commas, like so:

`Fire`

This is an example of a [markup API](http://www.toolness.com/wp/2013/01/building-bridges-between-guis-and-code-with-markup-apis/), requiring only a bit of HTML to get going.

## The Basic Style

In a nutshell, the script takes each synonym listed in the `data-cinnamon`

attribute and creates a child element, appropriately styled.

To style the synonyms, I stack them behind the original text with the following CSS. The synonym text is hidden while the original text gets highlighted.

```
position: absolute;
top: 0;
left: 0;
z-index: -1;
display: inline-block;
width: 100%;
height: 100%;
overflow: hidden;
color: transparent;
```

Here’s how it looks in [Firefox’s 3D view](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/3D_view). The green blocks represent the synonyms.

## Cross-Browser Quirks

For the purposes of the script, when a synonym is found, the text should stay invisible while its background gets highlighted. This gives the illusion that the original word is the one being highlighted.

In testing this, I discovered some differences in how browsers handle Find. These are edge cases that you hopefully won’t ever have to deal with, but they loomed larger in making Cinnamon.js.

### Finding Invisible Text

If text is set to `display: none;`

, Find doesn’t see it at all — this much is true of all browsers. Same goes for `visibility: hidden;`

(except for Opera, where Find matches the synonym but nothing is seen).

When opacity is set to 0, most browsers match the text, but nothing is visibly highlighted (Opera is the odd man out again, highlighting the background of the matched text).

When text is set to `color: transparent;`

, most browsers including Firefox and Chrome will highlight the area while the text stays transparent — just what we want for our script.

### Safari

However, Safari does things differently. When transparent text is found, Safari will display it as black text on yellow. If the text is buried under elements with a higher z-index, it brings it to the top.

Another difference: most browsers match text in the middle of a string. Safari only does so when the string is CamelCase.

## Other Issues

Hidden text, used deceptively, [can be penalized](http://support.google.com/webmasters/bin/answer.py?hl=en&answer=66353) in Google’s search results. Given the techniques used, Cinnamon.js carries some small measure of risk, especially if it’s misused.

Another issue is the impact of Cinnamon.js on accessibility. Fortunately, there’s `aria-hidden="true"`

, which is used to tell screen readers to ignore synonyms.

## Keep On Searching

I’ve used the browser’s Find function for years without giving it much thought. But in writing Cinnamon.js, I’ve learned quite a bit about the web and how a small piece of it might be extended. You just never know what’ll inspire your next hack.

## About
[
Thomas Park ](http://thomaspark.me)

Thomas is a researcher at Drexel University in Philadelphia, where he studies better ways to support people learning web development. He blogs at [http://thomaspark.me](http://thomaspark.me) and tweets at [@thomashpark](http://twitter.com/thomashpark).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

Brett ZamirFebruary 26th, 2013 at 23:07Janet SwisherMarch 1st, 2013 at 15:47