---
title: Capturing – Improving Performance of the Adaptive Web – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/03/capturing-improving-performance-of-the-adaptive-web/
author: Shawn Jansepar
published: '2013-03-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Responsive design is now widely regarded as the dominant approach to building new websites. With good reason, too: a responsive design workflow is the most efficient way to build tailored visual experiences for different device screen sizes and resolutions.

Responsive design, however, is only the tip of the iceberg when it comes to creating a rich, engaging mobile experience.

Performance is one of the most important features of a website, but is also frequently overlooked. Performance is something that many developers struggle with – in order to create high-performing websites you need to spend a lot of time tuning your site’s backend. Even more time is required to understand how browsers work, so that you make rendering pages as fast as possible.

When it comes to creating responsive websites, the performance challenges are even more difficult because you have a single set of markup that is meant to be consumed by all kinds of devices. One problem you hit is the responsive image problem – how do you ensure that big images intended for your Retina Macbook Pro are not downloaded on an old Android phone? How do you prevent desktop ads from rendering on small screen devices?

It’s easy to overlook performance as a problem because we often conduct testing under perfect conditions – using a fast computer, fast internet, and close proximity to our servers. Just to give you an idea of how evident this problem is, we conducted an analysis into some top responsive e-commerce sites which revealed that the average responsive site home page consists of 87.2 resources and is made up of 1.9 MB of data.

It is possible to solve the responsive performance problem by making the necessary adjustments to your website manually, but performance tuning by hand involves both complexity and repetition, and that makes it a great candidate for creating tools. With Capturing, we intend to make creating high-performing adaptive web experiences as easy as possible.

Introducing Capturing

Capturing is a client-side API we’ve developed to give developers complete control over the DOM before any resources have started loading. With responsive sites, it is a challenge to control what resources you want to load based on the conditions of the device: all current solutions require you to make significant changes to your existing site by either using server-side user-agent detection, or by forcing you to break semantic web standards (for example, changing the src attribute to data-src).

Our approach to give you resource control is done by capturing the source markup before it has a chance to be parsed by the browser, and then reconstructing the document with resources disabled.

The ability to control resources client-side gives you an unprecedented amount of control over the performance of your website.

Capturing was a key feature of Mobify.js 1.1, our framework for creating mobile and tablet websites using client-side templating. We have since reworked Mobify.js in our 2.0 release to be a much more modular library that can be used in any existing website, with Capturing as the primary focus.

A solution to the responsive image problem

One way people have been tackling the responsive image problem is by modifying existing backend markup, changing the src of all their img elements to something like data-src, and accompanying that change with a <noscript> fallback. The reason this is done is discussed in this CSS-Tricks post –

“a src that points to an image of a horse will start downloading as soon as that image gets parsed by the browser. There is no practical way to prevent this“.

With Capturing, this is no longer true.

Say, for example, you had an img element that you want to modify for devices with Retina screens, but you didn’t want the original image in the src attribute to load. Using Capturing, you could do something like this:

if (window.devicePixelRatio && window.devicePixelRatio >= 2) {
var bannerImg = capturedDoc.getElementById("banner");
bannerImg.src = "retinaBanner.png"
}

Because we have access to the DOM before any resources are loaded, we can swap the src of images on the fly before they are downloaded. The latter example is very basic – a better example to highlight the power of capturing it to demonstrate a perfect implementation of the picture polyfill.

Picture Polyfill

The Picture element is the official W3C HTML extension for dealing with adaptive images. There are polyfills that exist in order to use the Picture element in your site today, but none of them are able to do a perfect polyfill – the best polyfill implemented thus far requires a <noscript> tag surrounding an img element in order to support browsers without Javascript. Using Capturing, you can avoid this madness completely.

Open the example and be sure to fire up the network tab in web inspector to see which resources get downloaded:

Here is the important chunk of code that is in the source of the example:

Take note that there is an img element that uses a src attribute, but the browser only downloads the correct image. You can see the code for this example here (note that the polyfill is only available in the example, not the library itself – yet):

Not all sites use modified src attributes and <noscript> tags to solve the responsive image problem. An alternative, if you don’t want to rely on modifying src or adding <noscript> tags for every image of your site, is to use server-side detection in order to swap out images, scripts, and other content. Unfortunately, this solution comes with a lot of challenges.

It was easy to use server-side user-agent detection when the only device you needed to worry about was the iPhone, but with the amount of new devices rolling out, keeping a dictionary of all devices containing information about their screen width, device pixel ratio, and more is a very painful task; not to mention there are certain things you cannot detect with server-side user-agent – such as actual network bandwidth.

What else can you do with Capturing?

Solving the responsive image problem is a great use-case for Capturing, but there are also many more. Here’s a few more interesting examples:

Media queries in markup to control resource loading

In this example, we use media queries in attributes on images and scripts to determine which ones will load, just to give you an idea of what you can do with Capturing. This example can be found here:

The primary function of Mobify.js 1.1 was client-side templating to completely rewrite the pages of your existing site when responsive doesn’t offer enough flexibility, or when changing the backend is simply too painful and tedious. It is particularly helpful when you need a mobile presence, fast. This is no longer the primary function of Mobify.js, but it still possible using Capturing.

Once again, open up web inspector to see that the original images on the site did not download.

Performance

So what’s the catch? Is there a performance penalty to using Capturing? Yes, there is, but we feel the performance gains you can make by controlling your resources outweigh the minor penalty that Capturing brings. On first load, the library (and main executable if not concatenated together), must download and execute, and the load time here will vary depending on the round trip latency of the device (ranges from around ~60ms to ~300ms). However, the penalty of every subsequent request will be reduced by at least half due to the library being cached, and the just-in-time (JIT) compiler making the compilation much more efficient. You can run the test yourself!

We also do our best to keep the size of the library to a minimum – at the time of publishing this blog post, the library is 4KB minified and gzipped.

Why should you use Capturing?

We created Capturing to give more control of performance to developers on the front-end. The reason other solutions fail to solve this problem is because the responsibilities of the front-end and backend have become increasingly intertwined. The backend’s responsibility should be to generate semantic web markup, and it should be the front-end’s responsibility to take the markup from the backend and processes it in such a way that it is best visually represented on the device, and in a high-performing way. Responsive design solves the first issue (visually representing data), and Capturing helps solve the next (increasing performance on websites by using front-end techniques such as determining screen size and bandwidth to control resource loading).

If you want to continue to obey the laws of the semantic web, and if you want an easy way to control performance at the front-end, we highly recommend that you check out Mobify.js 2.0!

How can I get started using Capturing?

Head over to our quick start guide for instructions on how to get setup using Capturing.

What’s next?

We’ve begun with an official developer preview of Mobify.js 2.0, which includes just the Capturing portion, but we will be adding more and more useful features.

The next feature on the list to add is automatic resizing of images, allowing you to dynamically download images based on the size of the browser window without the need to modify your existing markup (aside from inserting a small javascript snippet)!

We also plan to create other polyfills that can only be solved with Capturing, such as the new HTML5 Template Tag, for example.

We look forward to your feedback, and we are excited to see what other developers will do with our new Mobify.js 2.0 library!

About
Shawn Jansepar

@shawnjan8 Shawn is a software engineer at Mobify where he works on the open source Mobify.js library, and on the Mobify Cloud. He loves to hack both on the front-end and back-end, with a heavy focus on user experience. When he isn't hacking, you will likely find him playing hockey/video games, eating, or travelling. Shawn has a BSc in Computer Science from Simon Fraser University.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at http://robertnyman.com and loves to travel and meet people.

Thanks! Please check your inbox to confirm your subscription.

If you haven’t previously confirmed a subscription to a Mozilla-related newsletter you may have to do so. Please check your inbox or your spam filter for an email from us.

34 comments

louisremi

How do you handle dynamically generated content? If after the load event I insert the same element in the DOM, will it be captured?

This sort of capturing can only happen to content present in the document at the time it is sent from the server. You are of course free to manipulate content you retrieve using ajax as much as you want before adding anything to the DOM.

Great question! Capturing actually happens before any dynamic content created by your existing JS is executed. You first capture the original document without any resources loaded, or javascript executed, and from there, you are free to modify the captured document as you please. When you are finished modifying the captured document, you render it to the main document, and at that point, your inline/external javascript files will execute. Think of capturing as giving you the ability to be an HTML pre-parser, or a middleware into modifying your markup.

I know all about it – I’m the guy behind the Adaptive Images solution :)

I’d say pre-parse hurt more than it helped. Far more. It was a poor solution aimed at saving milliseconds, implemented in a way that killed the ability to save full seconds. Short-sighted, ill conceived, low benefit, and no way to turn the thing off.

I think for a lot of sites it does help, and when Steve Sounders says that “speculative downloading is one of the most important performance improvements from browsers”, I like to think he knows a thing or two! But I think that there are many scenarios where the ability to disable it would be hugely beneficial. Until that happens, go ahead and use Capturing/Mobify.js :)

I think you have to be careful declaring that the look-ahead pre-fetcher is the most destructive performance enhancement ever.

Yes the interaction between it and responsive/adaptive images needs some work but you’ve only got to compare waterfalls from older browsers with newer ones to see the positive difference it makes.

This looks promising, can’t wait to try it! Any issues if my scripts are loaded asynchronously? Also wondering about progressive enhancement. Would you use capturing to build picture elements and even the multiple sources, so in the case JS fails you’re left with just an image tag?

Nope, no issue with asynchronously loaded scripts! The scripts that you use to asynchronously load other scripts will be executed after capturing is complete. And yes, if you use Capturing in conjunction with using the picture element, the picture element will work fully as intended – with an img element fallback (no `noscript` element required!).

Doesn’t Capturing really just solve a problem that Twitter Bootstrap has already addressed? How is Capturing different? When should I use Capturing instead of Bootstrap?

Capturing and Bootstrap are actually completely different. Bootstrap is a front-end framework to help you create websites (responsive and non-responsive). Capturing is a library that allows you to modify the document before any resources have been loaded. Thus, if you have a Bootstrap site, you can easily use the Capturing library in Mobify.js to bring you more performance benefits!

Hey James, I’ll try to explain my thinking at the time I asked the question… Bootstrap-responsive.css has made manipulating page content to deal with different ranges of browser sizes dead simple. From resizing columns and content, to controlling which things should be displayed or not for various browser dimensions. Granted, you wouldn’t use Bootstrap to conditionally load content based on business logic, but this article isn’t focusing on that capability of Capturing. The focus seems to be on improving performance for browsers on mobile devices using responsive design. In that specific regard, I thought Capturing was addressing the same problem a different way.

Wow, very clever trick! But the plaintext element is deprecated, right? They removed if from the spec. Do you think we will have any issues in the future with browsers dropping support?

When plaintext is considered “obsolete”, then we’ll have to worry :). When an element or attribute is considered depricated, the W3C still recommends that browsers should still implement them for backwards compatibility reasons. Checkout the official W3C spec for deprecated/obsolete elements:

The HTML5 consider plaintext obsolete. It also states that web browsers *must* now treat “plaintext” as “pre”. I didn’t find a browser doing this yet, but it’s already in the spec:

My colleague Noah nailed the answer to this question below – from the wording in the spec, it seems like the browser will always maintain special behaviour for this element. We believe that it’s much more likely that Capturing becomes obsolete not from changing the behaviour of Plaintext, but from the browser API giving you native control over resource loading.

This may be a really dumb question, but how would this process work for a WordPress site, where many images will be posted via the admin by non-developers? Is there a way to set that up?

Not a dumb question at all! For a WordPress site, you simply need to get the tag into the very top of the HEAD of your website, and then write the code that modifies your site in your main.js, and have that hosted somewhere that is accessible. Have a look at the quick start guide:

Ding-dong, the pre-parser is dead! Very clever, gentlemen. Three questions: 1) Can you explain in a bit more detail how writing the plaintext element stops loading? You haven’t really explained the magic, just shown the trick! (I believe that it works, I just want to know why.) I’ve always been under the impression that the preparser always just bolts ahead no matter what, ahead of script execution? 2) Can you respond to Sérgio’s question about deprecation of plaintext? (E.g. MDN warns strongly against it.) 3) Browser support: Why no support for IE<10? And what about mobile browser support?

1) The plaintext element is the pre-cursor to the `pre` tag, and it was meant to instruct the browser to ignore formatting. For some reason, every browser implements the plaintext element by ignoring the ending tag, causing everything in the document to be swallowed up into a big string inside of the plaintext element, thus each node that proceeds the plaintext is no longer rendered. The pre-parser behaves in different ways – Firefox will actually start loading the resources (as many as the maximum allows) as you would expect the pre-parser to do, but after the plaintext escaping, the requests get cancelled after 1-3 KBs. With Webkit, the preparser is completely stopped in its tracks.

2) Done :)

3) The reason we only support IE10 is because every single IE browser prior to it treats document.write completely. When you execute `render` with Capturing, we document.write your entire site, and unfortunately in older IEs, scripts do not get executed in the order that they are in, they get executed in the order that they download, which is a serious problem. We have put some thought into how we might be able to get around it, but haven’t came up with anything yet (only recently did we start supporting Desktop browsers, as this used to be a mobile-only framework). If you have some ideas, feel free to fork our repo! Here is the capturing file: https://github.com/mobify/mobifyjs/blob/v2.0/src/capture.js

Thanks–I suppose one workaround for the IE<10 script execution issue would be to concatenate completely, or write everything completely async, with a loader like yepnope. Definitely possible, but it is a constraint, and I think I speak for just about everybody when I say that IE9 is an absolute requirement. The plaintext trick is a brilliant discovery though!

In the meantime, has anyone proposed/drafted/submitted a standards-based markup solution to taming the pre-parser? There's got to be a simpler long-term answer to this problem, without any goofy noscript tags or the blocking behavior of Capturing that Souders has (fairly, IMHO) criticized…

Sergio, you’ll notice when discussing that has similar semantics to pre, the spec mentions “The parser has special behavior for this element, though.”

The uncloseable nature of this element (there is no tag), and hence its usefulness for this capturing technique, are the special parsing behaviour.

Obviously, this is not an intended use of the element, but moving forward I think it’s obvious that it would be beneficial to have more contextually aware behaviour in browser pre-parsers and resource schedulers, with respect to what to load with things like the forthcoming picture element, and maybe even some programmatic control over what’s to be loaded, short of crafty DOM manipulation like this.

Using this capturing technique will slow down the load of your pages by 1-2 seconds on a mobile network. You can read more about my assessment (including WebPagetest tests that show the performance cost of this technique) here: https://plus.google.com/117340630485537362092/posts/iv3iPnK3M1b

Thanks for the in-depth post! I’ve updated the same G+ thread linked above with a more accurate test regarding capturing. In my test, the penalty of capturing is about ~0.5s. As stated in my response to your post, the test you ran used a mobify.js file that was not gzipped, and my test also combines the mobify.js file and the main.js file, causing a huge jump in the speed of Capturing.

The question is, how far do you go when it comes to sending information about the client in the request headers? You could also send information about connection speed, etc. But all of the information you need is on the client itself, it seems silly to take that information and pass it on to the server for processing. It also makes caching of pages harder because of the variety of different pages that can be served for all the various devices.

Plus, even if this did happen and people were happy about it, it would be a while before you see browsers ship with this feature, which doesn’t help the performance of current browsers on the market.

Also, in regards to the responsibilities of the client and server, I mentioned my opinion in my article:

“The backend’s responsibility should be to generate semantic web markup, and it should be the front-end’s responsibility to take the markup from the backend and processes it in such a way that it is best visually represented on the device, and in a high-performing way”.

## 34 comments

louisremiMarch 19th, 2013 at 01:52Noah AMarch 19th, 2013 at 02:28Shawn JanseparMarch 19th, 2013 at 03:10Shawn JanseparMarch 19th, 2013 at 03:14Matt WilcoxMarch 19th, 2013 at 04:37Shawn JanseparMarch 19th, 2013 at 09:51Matt WilcoxMarch 19th, 2013 at 10:11Shawn JanseparMarch 19th, 2013 at 11:23Andy DaviesMarch 19th, 2013 at 14:20Ray SchwartzMarch 19th, 2013 at 05:02Shawn JanseparMarch 19th, 2013 at 09:54BruceMarch 20th, 2013 at 10:01Shawn JanseparMarch 20th, 2013 at 18:13jamesMarch 26th, 2013 at 08:38BruceMarch 26th, 2013 at 13:44Sérgio LopesMarch 21st, 2013 at 12:30Shawn JanseparMarch 22nd, 2013 at 16:23Sérgio LopesMarch 22nd, 2013 at 18:05Shawn JanseparMarch 25th, 2013 at 07:13CindyMarch 22nd, 2013 at 08:28Shawn JanseparMarch 25th, 2013 at 07:20Alex BellMarch 22nd, 2013 at 15:45Shawn JanseparMarch 26th, 2013 at 10:44Alex BellMarch 26th, 2013 at 11:25Noah AdamsMarch 23rd, 2013 at 00:35Robin BerjonMarch 27th, 2013 at 04:44Bryan McQuadeApril 6th, 2013 at 09:02Shawn JanseparApril 8th, 2013 at 14:23AndreApril 6th, 2013 at 18:35Gary StephensonApril 6th, 2013 at 20:08RugbyApril 7th, 2013 at 01:12Shawn JanseparApril 7th, 2013 at 07:43Shawn JanseparApril 7th, 2013 at 07:45Sean HoganApril 7th, 2013 at 21:57