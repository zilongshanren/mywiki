---
title: Network Monitor, now in Firefox Beta – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/06/network-monitor-now-in-firefox-beta/
author: Jeff Griffiths
published: '2013-06-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Firefox Developer Tools team is particularly proud announce that Firefox 23 (in [Firefox Beta](http://www.mozilla.org/en-US/firefox/beta/), to be released today) ships with an initial but very functional Network Monitor tool that not only provides similar functionality to other tool sets, but in many improves on them. This important step is the result of lots of hard work from the entire team, but in particular Victor Porof and Mihai Sucan.

### Let’s get started

To give you the best idea of how the network monitor works, here’s a series of steps to follow:

- Download, install and run
[Firefox 23 beta](http://www.mozilla.org/en-US/firefox/beta/)if you haven’t already (or[Firefox Aurora](http://www.mozilla.org/en-US/firefox/aurora/)or[Firefox Nightly](http://nightly.mozilla.org/)– more on[Firefox and the release channels](https://hacks.mozilla.org/2012/05/firefox-and-the-release-channels/)). - Open the Network Monitor tool:
- from the menu:
`Tools => Web Developer => Network`

- from the keyboard:
`Ctrl + Alt + Q`

(Windows/Linux) or`Cmd + Alt + Q`

(Mac OS X)

- from the menu:
- Load an
[interesting site](https://marketplace.firefox.com/).

As Firefox loads the page you’ll see each individual request get added as a row, much as you would expect from other tools. In particular it is now very easy to visualize not just how quickly parts of the page load and in what order, but also where problems are: missing assets, slow web servers, buggy apis.

As you get used to using the Network Monitor, you’ll also notice that you don’t need to necessarily hit refresh on a page that is already loaded, once you open the network tool any subsequent requests that happen will be logged. For example, if you’re interested in xhr requests made by an app, just open the monitor and start clicking buttons – you should see any api calls logged as normal without needing to reload.

### Status at a glance

One thing you should notice right away about the way the Network tool displays a page load is that we’ve taken care to provide both information and design cues to show you what is happening at a glance as the page loads:

We’ve tried to create a clean UI that delivers key aspects of how an entire page loads without creating too much visual clutter:

- An error such as a 404 are colored dark red to make them stand out visually from the green successful or yellow cached requests.
- The url is parsed out and only the file name and domain are shown.
- By default the load is sorted in chronological order, but you can also sort by any of the top columns, for example by domain or filename.
- You can easily see the type of request, whether it be html content, an image or an API request.
- You can click on the column headers to sort requests by method, file name, domain, type or size.

### It’s all in the details

Once all the page’s assets have been loaded, clicking on a single request opens up the sidebar view which provides detailed information about that request, broken down into panels that display different aspects of a given request: Headers, Cookies, Parameters, Response and Timings. Similar to how the Inspector tool works, this panel is responsive and will neatly pop down below the request list if you’ve docked the tools to the right side:

### A quick tour

The **Headers** panel is particularly useful for debugging asset caching problems, and this panel provides parsed lists for both the request and response headers that also supports filtering based on either name or value:

![](../../assets/b3b276f4c1924b7a.png)


The **Timings** panel gives you a detailed, visual breakdown of where time was spent for the selected request. Is it DNS? Is it the server itself?

If you’re debugging API requests or form posts, you’ll really like how we’ve parsed out the url parameters in the **Params** panel:

![](../../assets/f5f237164142da61.png)


Are you using a lot of API calls to improve the responsiveness of your app? JSON responses are parsed and displayed as a navigable object in the **Response** panel to make it easy to check on the data coming back from the server. You can filter the data based on JSON values as well.

![](../../assets/18f67a594d150fbd.png)


### Next Steps

It’s great to deliver the Network Monitor to a much wider set of developers in Firefox 23 Beta but we haven’t stopped adding new features in the meantime. Firefox 24 ( now in the [Aurora channel](http://www.mozilla.org/en-US/firefox/aurora/) ) features several notable improvements that have landed in the last 6 weeks or so:

- You can now filter requests based on the request ‘type’, including XHR, images, html.
- POST request parameters are supported in the Params panel.
- You can browse the list of requests via the Up/Down arrow keys.
- Many more bug fixes and refinements!

## About Victor Porof

Mozillian, hacker, working on Firefox DevTools.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 31 comments

Omega XJune 27th, 2013 at 02:59AlberJune 27th, 2013 at 07:51Sam ChenJune 27th, 2013 at 03:28Robert Nyman [Editor]June 27th, 2013 at 05:49Robson SobralJune 27th, 2013 at 13:51Robert Nyman [Editor]June 27th, 2013 at 14:26BastianJune 27th, 2013 at 04:36Robert Nyman [Editor]June 27th, 2013 at 05:49pdJune 30th, 2013 at 11:28DebjitJune 27th, 2013 at 05:41Robert Nyman [Editor]June 27th, 2013 at 05:49ZetlenJune 27th, 2013 at 06:32Robert Nyman [Editor]June 27th, 2013 at 14:04PeterJune 27th, 2013 at 08:34Robert Nyman [Editor]June 27th, 2013 at 14:06Simon CharetteJune 27th, 2013 at 13:06Robert Nyman [Editor]June 27th, 2013 at 14:08Victor PorofJune 28th, 2013 at 01:21SkouaJune 27th, 2013 at 15:54Robert Nyman [Editor]June 28th, 2013 at 00:22kbrosnanJuly 3rd, 2013 at 10:57Alecs GalindoJune 28th, 2013 at 23:06Robert Nyman [Editor]July 1st, 2013 at 03:02Vik GamovJuly 1st, 2013 at 22:19Robert Nyman [Editor]July 2nd, 2013 at 02:25Dane MacMillanJuly 5th, 2013 at 20:02Victor PorofJuly 6th, 2013 at 01:21Dane MacMillanJuly 10th, 2013 at 12:21Victor PorofJuly 10th, 2013 at 12:23Arthur RousselJuly 10th, 2013 at 14:45Dennis JakobsenJuly 12th, 2013 at 02:19