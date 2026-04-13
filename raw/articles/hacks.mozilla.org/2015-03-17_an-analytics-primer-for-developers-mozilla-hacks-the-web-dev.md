---
title: An analytics primer for developers – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/03/an-analytics-primer-for-developers/
author: Mark Wheeler
published: '2015-03-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There are three kinds of lies: lies, damned lies, and statistics – Mark Twain


## Deciding what to track (all the things)

When you are adding analytics to a system you should try to log *everything*. At some point in the future if you need to pull information out of a system it’s much better to have every piece of information to hand, rather than realising that you need some data that you don’t yet track. Here are some guidelines and suggestion for collecting and analysing information about how people are interacting with your website or app.

## Grouping your stats as a best practice

Most analytics platforms allow you to tag an event with metadata. This lets you analyse stats against each other and makes it easier to compare elements in a user interaction.

For example, if you are logging clicks on a menu, you could track each menu item differently e.g.:

```
track("Home pressed");
track("Cart pressed");
track("Logout pressed");
```

Doing this makes it harder to answer questions such as which button is most popular etc. Using metadata you can make most analytics platforms perform calculations like this for you:


```
track("Menu pressed","Home button");
track("Menu pressed","Cart button");
track("Menu pressed","Logout button");
```

The analytics above mean you now have a total of all menu presses, and you can find the most/least popular of the menu items with no extra effort.

## Optimising your funnel

A [conversion funnel](http://en.wikipedia.org/wiki/Conversion_funnel) is a term of art derived from a consumer marketing model. The metaphor of the funnel describes the flow of steps a user goes through as they engage more deeply with your software. Imagine you want to know how many users clicked *log in* and then *paid at the checkout*? If you track events such as “Checkout complete” and “User logged in” you can then ask your analytics platform what percentage of users did both within a certain time frame (a day for instance).

Imagine the answer comes out to be 10%, this tells you useful information about the behaviour of your users (bear in mind this funnel is not order sensitive, i.e., it does not matter in which order the events happen in login *-> cart -> pay* or *cart -> login -> pay*). Thus, you can start to optimise parts of your app and use this value to determine whether or not you are converting more of your users to make a purchase or otherwise engage more deeply.

## Deciding what to measure

Depending on your business, different stats will have different levels of importance. Here are some common stats of interest to developers of apps or online services:

- Number of sessions
- The total number of sessions on your product (the user opening your product, using it, then closing it = 1 session)
- Session length
- How long each session lasts (can be mode, mean, median)
- Retention
- How many people come back to your product having used it before (there are a variety of metrics such as rolling retention, 30 day retention etc)
- MAU
- Monthly active users: how may users use the app once a month
- DAU
- Daily active users: how may users use the app once a day
- ARPU
- Average revenue per user: how much money you make per person
- ATV
- Average transaction value: how much money you make per sale
- CAC
- Customer acquisition cost: how much it costs to get one extra user (normally specified by the channel for getting them)
- CLV
- Customer lifetime value: total profit made from a user (usually projected)
- Churn
- The number of people who leave your product in a given time (usually given as a percentage of total user base)
- Cycle time
- The the time it takes for one user to refer another

## Choosing an analytics tool or platform

There are plenty of analytics providers, listed below are some of the best known and most widely used:

*Google Analytics*

[Website](http://google.com/analytics)

[Developer documentation](https://developers.google.com/analytics/devguides/collection/analyticsjs/)

Quick event log example:

```
ga('send', 'event', 'button', 'click');
```

Pros:

- Free
- Easy to set up

Cons:

- Steep learning curve for using the platform
- Specialist training can be required to get the most out of the platform

**Single page apps:**

If you are making a single page app/website, you need to keep Google informed that the user is still on your page and hasn’t bounced (gone to your page/app and left without doing anything):

```
ga('set' , 'page', location.pathname + location.search + location.hash);
ga('send', 'pageview');
```

Use the above code every time a user navigates to a new section of your app/website to let Google know the user is still browsing your site/app.

*Flurry*

[Website](http://flurry.com)

[Developer documentation](https://developer.yahoo.com/flurry/)

Quick event log example:

```
FlurryAgent.logEvent("Button clicked");
FlurryAgent.logEvent("Button clicked",{more : 'data'});
```

Pros:

- Free
- Easy to set up

Cons:

- Data normally 24 hours behind real time
- Takes ages to load the data

*Mixpanel*

[Website](http://mixpanel.com)

[Developer documentation](https://mixpanel.com/help/reference/javascript)

Quick event log example:

```
mixpanel.track("Button clicked");
mixpanel.track("Button clicked",{more : 'data'});
```

Pros:

- Free trial
- Easy to set up
- Real-time data

Cons:

- Gets expensive after the free trial
- If you are tracking a lot of points, the interface can get cluttered

## Speeding up requests

When you are loading an external JS file you want to do it asynchronously if possible to speed up the page load.

```
```

The above code will cause the JavaScript to load asynchronously but assumes the user has a browser supporting HTML5.

```
//jQuery example
$.getScript('https://cdn.flurry.com/js/flurry.js',
function(){
...
});
```

This code will load the JavaScript asynchronously with greater browser support.

The next problem is that you could try to add an analytic even though the framework does not exist yet, so you need to check to see if the variable framework first:

```
if(typeof FlurryAgent != "undefined"){
...
}
```

This will prevent errors and will also allow you to easily disable analytics during testing. (You can just stop the script from being loaded – and the variable will never be defined.)

The problem here is that you might be missing analytics whilst waiting for the script to load. Instead, you can make a queue to store the events and then post them all when the script loads:

```
var queue = [];
if(typeof FlurryAgent != "undefined"){
...
}else{
queue.push(["data",{more : data}]);
}
...
//jQuery example
$.getScript('https://cdn.flurry.com/js/flurry.js',
function(){
...
for(var i = 0;i < queue.length;i++)
{
FlurryAgent.logEvent(queue[i][0],queue[i][1]);
}
queue = [];
});
```

## Analytics for your Firefox App

You can use any of the above providers above with Firefox OS, but remember when you paste a script into your code they generally are protocol agnostic: they start `//myjs.com/analytics.js`

and you need to choose either *http:* or *https:* -- `https://myjs.com/analytics.js`

(This is required only if you are making a packaged app.)

Let us know how it goes.

## About
[
Mark Wheeler ](http://pixelcode.co.uk)

CTO at Rormix - Music worth watching

## 4 comments

Jesus PeralesMarch 17th, 2015 at 13:56Mark WheelerMarch 17th, 2015 at 14:35Jesus PeralesMarch 17th, 2015 at 15:12Sibil MohammedMarch 19th, 2015 at 12:53