---
title: JavaScript Error- and XHR Log Recording With Every Bug Report – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2014/08/javascript-error-and-xhr-log-recording-with-every-bug-report/
author: Bogomil Shopov
published: '2014-08-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Let’s start with a story. A user story:

A friend of mine called me in the middle of the day with a very strange request. He told me

“Could you come over and help me to fill-in a form”.


I was surprised as filling forms is the easiest thing to do online, isn’t it? Even for not so-tech-savvy people.

So I went to my friend’s home and surprise, it wasn’t so easy! It took me 25 min to debug what was wrong with this website (a government one, in Bulgaria). The problem was missing validation (via XMLHttpRequest).

Of course, I called the agency, expecting everything to go to `/dev/null/`

, but surprisingly they were interested in the problem, so I spent another 25 min explaining the problem and sending them all data they needed. These included:

- Screen Size
- Browser and OS version
- Where exactly the problem occurs
- Javascript errors and XHR Logs (pasted in an email)
- Plugins installed on my friend’s browser

etc, etc, etc … you know what I am talking about.

It was exhausting.

## The perfect bug report

Let’ step aside from the story and think more like developers. What a developer will need to fix the problem quickly, WITHOUT asking the user difficult questions:

- Screen size, plugins, installed on your browser, URL where the problem happened, OS and Browser version
- A visual and annotated screenshot showing where exactly is the problem and how it looks like through the user’s eyes with all steps on how to reproduce the bug.

Right?

Wait, something is missing.

The worst thing about most error reports from users is that they happen on the client-side, in front-end javascript, a cruel, cruel place, far away from the developer trying to fix them.

Agreed? That’s why a perfect bug report should contain something else – a browsable [JavaScript error- and XHR-logs recorder](https://usersnap.com/features/console-recorder).

See

## Let’s Talk Code: Recorded JavaScript Errors

The [Usersnap Console Recorder](https://usersnap.com/features/console-recorder) saves every kind of JavaScript error. You can **browse** through the web developer console in the Usersnap dashboard, as if you would sit right on your user’s browser!

Every error / log contains a NTP synced timestamp, a full stack including JavaScript **source files** and **line numbers** and **formatting** like the developer console you already know from *Firebug*

Every debug log issued by `console.log`

, `console.info`

, `console.warn`

or `console.error`

gets properly formatted (including recursive object/array formatting and browsing).

Guaranteed no `[object Object]`

hell during debugging!

#### Accessing Properties of Undefined/Null Objects

First example which happens quite often in the wild: a fixed element should be aligned by another element by using the `top`

property during scrolling.

However, due to a markup rework, the element `#inexistent`

does no longer exist. This leads to `offset()`

returning `null`

and the property `top`

can no longer be accessed:

```
function clicky() {
console.info("Accessing a property of an undefined object");
console.log("calculating scroll top %d", $('#inexistent').offset().top);
};
```

### Calling Methods of Undefined Objects

Another rework case here: One tries to call a method on an undefined object.

```
function clicky2() {
console.info("Calling a method of an undefined object");
adjust.ScrollBottom();
};
```

### Plain Exceptions

Sometimes you even know during development that something can break – wouldn’t it be great to know it when it actually breaks?

```
function clicky3() {
console.info("Throwing an exception");
throw "Version Mismatch!";
};
```

## XHR Errors

Sometimes, XHRs deliver errors (like `404 Not Found`

or `500 Internal Server Error`

). Most of the time, such errors lead to bugs which are very hard to reproduce.

```
function clicky4() {
console.info("404 on XHR");
$.ajax({
"url": "non_existing.php"
});
};
```

Cross-Origin XHRs are troublesome. Image someone changes the CORS header and your cross origin XHR does no longer work from one day to another.

```
function clicky5() {
console.info("Cross-Origin on XHR");
$.ajax({
"url": "http://facebook.com/cross-origin"
});
};
```

### XHR and Time Tracking

#### Recording the Steps During a Checkout

Conversion rates are key in most businesses. Any obstacle for the user can lower your rates – e.g. it takes too long to load a page or you even have an error during checkout.

This short example shows a standard click handler which calls `getcheckout.php`

via XHR. Unfortunately, the second XHR (`confirm.php`

) fails and throws a JavaScript exception. That’s nice, but: the user does not get any feedback. The page just stalls.

```
function checkout() {
console.log("check out clicked!");
$.ajax({
url: "getcheckout.php",
dataType: "json"
}).done(function(data) {
console.log("Checked out: %o", data);
confirm();
});
};
```

```
function confirm() {
confirmService.checkConfirm();
$.ajax({
url: "confirm.php"
}).error(function() {
throw "internal server error on confirm!";
});
};
```

Additionally, you will get a full synced time frame of your user’s action (regardless if the time on the user’s browser is correct or not!). The full formatting support for objects (`console.log(“Checked out: %o”, data);`

) is super convenient for debugging.

## Conclusion

Now every developer can have the superpower of understanding what the problem is even on the client-side and stop worrying about “It does not work. Fix it ASAP!” type of communication.

And now every user will be able to report the issues better, because he/she needs just to [press one button to report and issue](https://usersnap.com/), using the tools he/she knows well, and the magic will happen in the background.

## Free licenses for FOSS projects

We at Usersnap [support and believe](http://usersnap.com/blog/free-open-source-project-license-request/) in the FOSS (Free/Libre and Open Source) movement and that’s why Usersnap is free (*as in free beer*) for any FOSS project to use.

We utilize a number of open source components like nginx, python, rabbitmq, angular and giving back to the community + improving the quality of your projects is a way to say “Thanks”

Your project must meet all of the following criteria to be approved:

- The project is licensed under a
[license approved](http://www.opensource.org/licenses/alphabetical)by the Open Source Initiative. - The project source code is available for download.
- Your open source project has a publicly accessible website.

## About Bogomil Shopov

Bogo is a long time Mozilla contributor. Currently helping web project teams to be awesome at Usersnap. Monthy Python fan.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

Hello71August 5th, 2014 at 04:32Bogomil ShopovAugust 5th, 2014 at 04:40LukeAugust 6th, 2014 at 21:56Bogomil ShopovAugust 7th, 2014 at 05:15