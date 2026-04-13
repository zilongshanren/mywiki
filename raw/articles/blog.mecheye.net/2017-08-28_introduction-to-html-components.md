---
title: Introduction to HTML Components
url: https://blog.mecheye.net/2017/08/introduction-to-html-components/
author: Jasper St Pierre
published: '2017-08-28'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

HTML Components (HTC), introduced in Internet Explorer 5.5, offers a powerful new way to author interactive Web pages. Using standard DHTML, JScript and CSS knowledge, you can define custom behaviors on elements using the “behavior” attribute. Let’s create a behavior for a simple kind of “image roll-over” effect. For instance, save the following as “roll.htc”:

<PUBLIC:ATTACH EVENT="onmouseover" ONEVENT="rollon()" /> <PUBLIC:ATTACH EVENT="onmouseout" ONEVENT="rollout()" /> <SCRIPT LANGUAGE="JScript"> tmpsrc = element.src; function rollon() { element.src = tmpsrc + "_rollon.gif" } function rollout() { element.src = tmpsrc + ".gif"; } rollout(); </SCRIPT>

This creates a simple HTML Component Behavior that swaps the image’s source when the user rolls over and rolls off of the mentioned image. You can “attach” such a behavior to any element using the CSS attribute, “behavior”.

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"> <HTML> <BODY> <IMG STYLE="behavior: url(roll.htc)" SRC="logo"> </BODY> </HTML>

The benefit of HTML Components is that we can apply them to *any* element through simple CSS selectors. For instance:

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"> <HTML> <HEAD> <STYLE> .RollImg { behavior: url(roll.htc); } </STYLE> </HEAD> <BODY> <IMG CLASS="RollImg" SRC="logo"> <IMG CLASS="RollImg" SRC="home"> <IMG CLASS="RollImg" SRC="about"> <IMG CLASS="RollImg" SRC="contact"> </BODY> </HTML>

This allows us to reuse them without having to copy/paste code. Wonderful! This is known as an Attached Behavior, since it is directly attached to an element. Once you’ve mastered these basic Attached Behaviors, we can move onto something a bit more fancy, Element Behaviors. With Element Behaviors, you can create custom element types and create custom programmable interfaces, allowing us to build a library of custom components, reusable between pages and projects. Like before, Element Behaviors consist of an HTML Component, but now we have to specify our component in `<PUBLIC:COMPONENT>`

.

<PUBLIC:COMPONENT TAGNAME="ROLLIMG"> <PUBLIC:ATTACH EVENT="onmouseover" ONEVENT="rollon()" /> <PUBLIC:ATTACH EVENT="onmouseout" ONEVENT="rollout()" /> <PUBLIC:PROPERTY NAME="basesrc" /> </PUBLIC:COMPONENT> <img id="imgtag" /> <SCRIPT> img = document.all['imgtag']; element.appendChild(img); function rollon() { img.src = element.basesrc + "_rollon.gif"; } function rollout() { img.src = element.basesrc + ".gif"; } rollout(); </SCRIPT>

I’ll get to the implementation of ROLLIMG in a bit, but first, to use a custom element, we use the special `<?IMPORT>`

tag which allows us to import a custom element into an XML namespace.

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"> <HTML XMLNS:CUSTOM> <HEAD> <?IMPORT NAMESPACE="CUSTOM" IMPLEMENTATION="RollImgComponent.htc"> </HEAD> <BODY> <CUSTOM:ROLLIMG BASESRC="logo"> <CUSTOM:ROLLIMG BASESRC="home"> <CUSTOM:ROLLIMG BASESRC="about"> <CUSTOM:ROLLIMG BASESRC="contact"> </BODY> </HTML>

The ROLLIMG fully encapsulates the behavior, freeing the user of having to “know” what kind of element to use the Attached Behavior on! The implementation of the Custom Element Behavior might seem a bit complex, but it’s quite simple. When Internet Explorer parses a Custom Element, it *synchronously* creates a new HTML Component from this “template” and binds it to the instance. We also have two “magic global variables” here: “element” and “document”. Each instance of this HTML Component gets its own document, the children of which are reflowed to go inside the custom element. “element” refers to the custom element tag in the outer document which embeds the custom element. Additionally, since each custom element has its own document root, that means that it has its own script context, and its own set of global variables.

We can also set up properties as an API for the document author to use when they use our custom element.

Here, we use an img tag as a “template” of sorts, add it to our custom element’s document root.

After IE puts it together, the combined DOM sort of looks like this:

<CUSTOM:ROLLIMG BASESRC="logo"> <IMG ID="imgtag" SRC="logo.gif"> </CUSTOM:ROLLIMG> <CUSTOM:ROLLIMG BASESRC="home"> <IMG ID="imgtag" SRC="home.gif"> </CUSTOM:ROLLIMG> ...

Unfortunately, this has one final flaw. Due to the natural cascading nature of CSS Stylesheets, such “implementation details” will leak through. For instance, if someone adds a `<STYLE>IMG { background-color: red; }</STYLE>`

, this will affect our content. While this can sometimes be a good thing if you want to develop a styleable component, it often results in undesirable effects. Thankfully, Internet Explorer 5.5 adds a new feature, named “Viewlink”, which encapsulates not just the implementation of your HTML Component, but the document as well. “Viewlink” differs from a regular component in that instead of adding things as children of our element, we instead can provide a document fragment which the browser will “attach” to our custom element in a private, encapsulated manner. The simplest way to do this is to just use our HTML Component’s document root.

<PUBLIC:COMPONENT TAGNAME="ROLLIMG"> <PUBLIC:ATTACH EVENT="onmouseover" ONEVENT="rollon()" /> <PUBLIC:ATTACH EVENT="onmouseout" ONEVENT="rollout()" /> <PUBLIC:PROPERTY NAME="basesrc" /> </PUBLIC:COMPONENT> <img id="imgtag" /> <SCRIPT> defaults.viewLink = document; var img = document.all['imgtag']; function rollon() { img.src = element.basesrc + "_rollon.gif"; } function rollout() { img.src = element.basesrc + ".gif"; } rollout(); </SCRIPT>

Using the “defaults.viewLink” property, we can set our HTML Component’s private document fragment as our viewLink, rendering the children but without adding them as children of our element. Perfect encapsulation.

…

…

*cough* OK, obviously it’s 2017 and Internet Explorer 5.5 isn’t relevant anymore. But if you’re a Web developer, this should have given you some pause for thought. The modern Web Components pillars: Templates, Custom Elements, Shadow DOM, and Imports, were all features originally in IE5, released in 1999.

Now, it “looks outdated”: uppercase instead of lowercase tags, the “on”s everywhere in the event names, but that’s really just a slight change of accent. Shake off the initial feeling that it’s cruft, and the actual meat is all there, and it’s mostly the same. Sure, there’s magic XML tags instead of JavaScript APIs, and magic globals instead of callback functions, but that’s nothing more than a slight change of dialect. IE says tomato, Chrome says tomato.

Now, it’s likely you’ve never heard of HTML Components *at all*. And, perhaps shockingly, a quick search at the time of this article’s publishing shows nobody else does at all.

Why did IE5’s HTML Components never quite catch on? Despite what you might think, it’s not because of a lack of open standards. Reminder, a decent amount of the web API, today, started from Internet Explorer’s DHTML initiative. contenteditable, XMLHttpRequest, innerHTML were all carefully, meticulously reverse-engineered from Internet Explorer. Internet Explorer was *the* dominant platform for websites — practically nobody designed or even tested websites for Opera or Netscape. I can remember designing websites that used IE-specific features like DirectX filters to flip images horizontally, or the VML

And it’s not because of a lack of evangelism or documentation. Microsoft *was* trying to push DHTML and HTML Components hard. Despite the content being nearly 20 years old at this point, documentation on [HTML Components](https://msdn.microsoft.com/en-us/library/ms532146(v=vs.85).aspx) and [viewLink](https://msdn.microsoft.com/en-us/library/ms531428(v=vs.85).aspx) is surprisingly well-kept, with diagrams and images, sample links and all, archived without any broken links. Microsoft’s librarians deserve fantastic credit on that one.

For any browser or web developer, please go read the [DHTML Dude](https://msdn.microsoft.com/en-us/library/bb263969(v=vs.85).aspx) columns. Take a look at the breadth of APIs available on display, and go look at some [example](http://samples.msdn.microsoft.com/workshop/samples/dhtmltechcol/dndude/sep.htc) [components](http://samples.msdn.microsoft.com/workshop/samples/dhtmltechcol/dndude/vtable.htc) on display. Take a look at [the persistence API](https://msdn.microsoft.com/en-us/library/ms533007(v=vs.85).aspx), or [dynamic expression properties](https://msdn.microsoft.com/en-us/library/bb263986(v=vs.85).aspx). Besides the [much-hyped-but-dated-in-retrospect XML data binding](https://msdn.microsoft.com/en-us/library/bb264001(v=vs.85).aspx) tech, it all seems relatively modern. Web fonts? [IE4](https://msdn.microsoft.com/en-us/library/ms533034(v=vs.85).aspx). CSS gradients? [IE5.5](https://msdn.microsoft.com/en-us/library/ms532997(v=vs.85).aspx). Vector graphics? [VML](https://msdn.microsoft.com/en-us/library/bb250524(v=vs.85).aspx) (which, in my opinion, is a more sensible standard than SVG, but that’s for another day.)

So, again I ask, why did this never catch on? I’m sure there are a variety of complex factors, probably none of which are technical reasons. Despite our lists of “engineering best practices” and “[blub paradoxes](http://www.paulgraham.com/avg.html)“, computer engineering has, and always will be, dominated by fads and marketing and corporate politics.

The more important question is a bigger one: Why am I the first one to point this out? Searching for “HTML Components” and “Viewlink” leads to very little discussion about them online, past roughly 2004. Microsoft surely must have been involved in the Web Components Working Group. Was this discussed at all?

Pop culture and fads pop in and fade out over the years. Just a few years ago, web communities were excited about Object.observe before React [proved it unnecessary](https://mail.mozilla.org/pipermail/es-discuss/2015-November/044684.html). Before node.js’s take on “isomorphic JavaScript” was solidified, heck, even before [v8cgi / teajs](https://code.google.com/archive/p/teajs/), an early JavaScript-as-a-Server project, another bizarre web framework known as [Aptana Jaxer](https://web.archive.org/web/20101216172526/http://jaxer.org/) was doing it in a much more direct way.

History is important. It’s easier to point and laugh and ignore outdated technology like Internet Explorer. But tech, so far, has an uncanny ability to keep repeating itself. How can we do a better job paying attention to things that happened before us, rather than assuming it was all bad?

Kudos to you and Microsoft. Your post has provide me with more of context than expected. And actually this is more of what I am able to admin from Microsoft since I consider my self open source guy and not a lover of MS policies/ways.

Recall me some similar discussion with friends long ago about DCOM :)

Thanks for posting this piece of writing. I enjoyed reading it.

David

Wow. I am ashamed because I was a Microsoft fan at the time… and I never knew about this. I remember being excited about IE 5.5 and DHTML, but I never once heard about WebComponents (or rather, I probably read about them and didn’t realize what it meant).

Thank you for the history lesson.

> And, perhaps shockingly, a quick search at the time of this article’s publishing shows nobody else does at all.

Do you mean, nobody knew ?

https://www.google.fr/search?q=dhtml&dcr=0&source=lnt&tbs=cdr%3A1%2Ccd_min%3A%2Ccd_max%3A8%2F28%2F1999&tbm=

Perhaps it was more popular in countries where IE was way more dominant than Netscape (in the EU? ) ?

> How can we do a better job paying attention to things that happened before us, rather than assuming it was all bad?

Knowing a tiny bit of CompSci (while keeping a lot of IT) help a bit (the new design pattern for GUI on the web are eeriy similar to GUI design pattern on desktop apps)

Regarding this point:

> The more important question is a bigger one: Why am I the first one to point this out? Searching for “HTML Components” and “Viewlink” leads to very little discussion about them online, past roughly 2004. Microsoft surely must have been involved in the Web Components Working Group. Was this discussed at all?

I can’t seem to track it down at the moment but the original email thread sent by Dimitri Glazkov to the public-webapps working group that started the whole Web Components discussion specifically mentions XBL (a similar idea from Mozilla) and HTC I think. Microsoft also mentioned them in their blog post on Edge and Web Components (https://blogs.windows.com/msedgedev/2015/07/14/bringing-componentization-to-the-web-an-overview-of-web-components/#r0sZDDbcbllmSFqf.97). I can’t speak for Dimitri or the other folks, but if I recall the discussion in the thread, it considered this prior art, acknowledged that there had been issues with each of them, and proposed some new primitives to improve on those spots. Those new primitives became the web component standards we have now.

I’m asking a teammate to help me track down the original thread. When we turn it up I’ll post it here :)

Huh, I guess I didn’t do a good enough job searching for this. Glad to know that the parallels have been pointed out.

Monica Dinculescu pointed me to some of the older threads:

https://lists.w3.org/Archives/Public/public-webapps/2010OctDec/0913.html

https://lists.w3.org/Archives/Public/public-webapps/2010OctDec/0951.html

http://kaytcat.github.io/web-components/#has-this-been-done-before

Great article, thanks for digging this up.

It is worth to remind people that everything new (Web Components) is well forgotten old (HTML Components). And often old has way more to offer. I wish the riches of HTC eventually will reincarnate in Web Components. Working on that :)

https://raw-dot-custom-elements.appspot.com/EPA-WG/embed-page/v0.0.3/embed-page/demo/index.html