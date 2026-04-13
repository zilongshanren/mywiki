---
title: There is no simple solution for local storage – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/03/there-is-no-simple-solution-for-local-storage/
author: Chris Heilmann
published: '2012-03-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**TL;DR: ** we have to stop advocating `localStorage`

as a great opportunity for storing data as it performs badly. Sadly enough the alternatives are not nearly as supported or simple to implement.

When it comes to web development you will always encounter things that sound too good to be true. Sometimes they are good, and all that stops us from using them is our notion of being conspicuous about *everything* as developers. In a lot of cases, however, they really are not as good as they seem but we only find out after using them for a while that we are actually “doing it wrong”.

One such case is local storage. There is a [storage specification](http://www.w3.org/TR/webstorage/#storage) (falsely attributed to HTML5 in a lot of examples) with an incredibly simple API that was heralded as the cookie killer when it came out. All you have to do to store content on the user’s machine is to access the `navigator.localStorage`

(or `sessionStorage`

if you don’t need the data to be stored longer than the current browser session):

```
localStorage.setItem( 'outofsight', 'my data' );
console.log( localStorage.getItem( 'outofsight' ) ); // -> 'my data'
```

This local storage solution has a few very tempting features for web developers:

- It is dead simple
- It uses strings for storage instead of complex databases (and you can store more complex data using JSON encoding)
- It is
[well supported by browsers](http://caniuse.com/#search=webstorage) - It is endorsed by a lot of companies (and was heralded as amazing when iPhones came out)

A few known issues with it are that [there is no clean way to detect when you reach the limit of local storage](http://arty.name/localstorage.html) and there is no cross-browser way to ask for more space. There are also more [obscure issues](http://htmlui.com/blog/2011-08-23-5-obscure-facts-about-html5-localstorage.html) around sessions and HTTPS, but that is just the tip of the iceberg.

## The main issue: terrible performance

LocalStorage also has a lot of drawbacks that aren’t quite documented and certainly not covered as much in “HTML5 tutorials”. Especially performance oriented developers are very much against its use.

When we covered localStorage a few weeks ago using it to [store images and files in localStorage](http://hacks.mozilla.org/2012/02/saving-images-and-files-in-localstorage/) it kicked off a massive thread of comments and an even longer internal mailing list thread about the evils of `localStorage`

. The main issues are:

`localStorage`

is synchronous in nature, meaning when it loads it can block the main document from rendering`localStorage`

does file I/O meaning it writes to your hard drive, which can take long depending on what your system does (indexing, virus scanning…)- On a developer machine these issues can look deceptively minor as the operating system cached these requests – for an end user on the web they could mean a few seconds of waiting during which the web site stalls
- In order to appear snappy, web browsers load the data into memory on the first request – which could mean a lot of memory use if lots of tabs do it
`localStorage`

is persistent. If you don’t use a service or never visit a web site again, the data is still loaded when you start the browser

This is covered in detail in a follow-up blog post by [Taras Glek](https://blog.mozilla.com/tglek/2012/02/22/psa-dom-local-storage-considered-harmful/) of the Mozilla performance team and also by [Andrea Giammarchi](http://webreflection.blogspot.com/2012/03/whats-localstorage-about.html) of Nokia.

In essence this means that a lot of articles saying you can use `localStorage`

for better performance are just wrong.

## Alternatives

Of course, browsers always offered ways to store local data, some you probably never heard of as shown by [evercookie](http://samy.pl/evercookie/) (I think my fave when it comes to the “evil genius with no real-world use” factor is the force-cached PNG image to be read out in canvas). In the internal discussions there was a massive thrust towards advocating IndexedDB for your solutions instead of `localStorage`

. We then [published an article how to store images and files in IndexedDB](http://hacks.mozilla.org/2012/02/storing-images-and-files-in-IndexedDB/) and found a few issues – most actually related to ease-of-use and user interaction:

- IndexedDB is a full-fledged DB that requires all the steps a SQL DB needs to read and write data – there is no simple key/value layer like
`localStorage`

available - IndexedDB asks the user for permission to store data which can spook them
- The browser support is not at all the same as
`localStorage`

, right now IndexedDB is supported in[IE10, Firefox and Chrome](http://caniuse.com/#search=index)and there are differences in their implementations - Safari, Opera, iOS, Opera Mobile, Android Browser favour
[WebSQL](http://caniuse.com/#search=websql)instead (which is[yet another standard](http://www.w3.org/TR/webdatabase/)that has been officially[deprecated](http://dev.w3.org/html5/webdatabase/)by the W3C)

As always when there are differences in implementation someone will come up with an abstraction layer to work around that. Parashuram Narasimhan [does a great job with that – even providing a jQuery plugin](http://blog.nparashuram.com/search/label/indexeddb). It feels wrong though that we as implementers have to use these. It is the HTML5 video debate of WebM vs. H264 all over again.

## Now what?

There is no doubt that the real database solutions and their asynchronous nature are the better option in terms of performance. They are also more matured and don’t have the “shortcut hack” feeling of `localStorage`

. On the other hand they are hard to use in comparison, we already have a lot of solutions out there using `localStorage`

and asking the user to give us access to storing local files is unacceptable for some implementations in terms of UX.

The answer is that there is no simple solution for storing data on the end users’ machines and we should stop advocating `localStorage`

as a performance boost. What we have to find is a solution that makes everybody happy and doesn’t break the current implementations. This might prove hard to work around. Here are some ideas:

- Build a polyfill library that overrides the
`localStorage`

API and stores the content in IndexedDB/WebSQL instead? This is dirty and doesn’t work around the issue of the user being asked for permission - Implement
`localStorage`

in an asynchronous fashion in browsers – actively disregarding the spec? (this could set a dangerous precedent though) - Change the
`localStorage`

spec to store asynchronously instead of synchronously? We could also extend it to have a proper`getStorageSpace`

interface and allow for native JSON support - Define a new standard that allows browser vendors to map the new API to the existing supported API that matches the best for the use case?

We need to fix this as it doesn’t make sense to store things locally and sacrifice performance at the same time. This is a great example of how new web standards give us much more power but also make us face issues we didn’t have to deal with before. With more access to the OS, we also have to tread more carefully.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 124 comments

PeteMarch 5th, 2012 at 03:16RonMarch 5th, 2012 at 03:24Chris HeilmannMarch 5th, 2012 at 03:33PeteMarch 5th, 2012 at 03:37Chris HeilmannMarch 5th, 2012 at 03:41PeteMarch 5th, 2012 at 03:46XMarch 13th, 2012 at 02:52AlexMarch 5th, 2012 at 10:12Les OrchardMarch 5th, 2012 at 14:25RonMarch 5th, 2012 at 03:20Jonas SickingMarch 6th, 2012 at 03:14Sean HoganMarch 5th, 2012 at 03:41Marcel JackwerthMarch 5th, 2012 at 03:50Burak Yiğit KayaMarch 5th, 2012 at 06:42Christopher BiscardiMarch 5th, 2012 at 04:11Robert NymanMarch 5th, 2012 at 04:21Remy SharpMarch 5th, 2012 at 04:24pdMarch 5th, 2012 at 04:32Moldován EduárdMarch 5th, 2012 at 04:32Marcel JackwerthMarch 5th, 2012 at 04:47Moldován EduárdMarch 5th, 2012 at 06:01Jens ArpsMarch 5th, 2012 at 05:35Jonas SickingMarch 5th, 2012 at 11:30Ian BickingMarch 5th, 2012 at 12:06Jens ArpsMarch 6th, 2012 at 02:00Jonas SickingMarch 6th, 2012 at 03:33Jens ArpsMarch 6th, 2012 at 04:58Benedikt P. [:Mic]March 5th, 2012 at 05:40Chris HeilmannMarch 5th, 2012 at 05:44check_caMarch 5th, 2012 at 08:26Jonas SickingMarch 5th, 2012 at 11:48check_caMarch 5th, 2012 at 13:08A.J.March 5th, 2012 at 15:34Jonas SickingMarch 6th, 2012 at 03:04Rakesh PaiMarch 5th, 2012 at 08:51Jonas SickingMarch 5th, 2012 at 11:33Jonas SickingMarch 5th, 2012 at 11:47Sean HoganMarch 5th, 2012 at 15:10Jonas SickingMarch 6th, 2012 at 01:58Rakesh PaiMarch 5th, 2012 at 20:17Jonas SickingMarch 6th, 2012 at 02:05CharlesMarch 5th, 2012 at 09:05JulienWMarch 5th, 2012 at 09:26Jonas SickingMarch 6th, 2012 at 02:08Jonas SickingMarch 6th, 2012 at 03:47JulienWMarch 15th, 2012 at 03:04NealleMarch 14th, 2012 at 14:00KevinMarch 5th, 2012 at 09:31Andy FuchsMarch 5th, 2012 at 09:41Larry GarfieldMarch 5th, 2012 at 09:55Steve SoudersMarch 5th, 2012 at 10:58Taras GlekMarch 5th, 2012 at 12:12Larry GarfieldMarch 5th, 2012 at 12:19Taras GlekMarch 5th, 2012 at 13:20starasMarch 5th, 2012 at 11:31Jonas SickingMarch 5th, 2012 at 14:11Rakesh PaiMarch 6th, 2012 at 20:31Ian BickingMarch 15th, 2012 at 13:15Kim TMarch 5th, 2012 at 16:15Chris HeilmannMarch 5th, 2012 at 16:27Rakesh PaiMarch 5th, 2012 at 20:39Matthew HollowayMarch 5th, 2012 at 20:20Jonas SickingMarch 6th, 2012 at 01:55forrestliuMarch 5th, 2012 at 18:17Henri SivonenMarch 6th, 2012 at 00:41Andy WalpoleMarch 6th, 2012 at 01:46John ThomasMarch 6th, 2012 at 11:35Shawn WilsherMarch 8th, 2012 at 11:53John ThomasMarch 6th, 2012 at 11:28Shawn WilsherMarch 8th, 2012 at 11:52John ThomasMarch 6th, 2012 at 11:54John ThomasMarch 6th, 2012 at 12:05Kim TMarch 6th, 2012 at 13:18Jonas SickingMarch 6th, 2012 at 14:59gregMarch 6th, 2012 at 16:22Robert NymanMarch 7th, 2012 at 01:31PeteMarch 7th, 2012 at 02:04Jonas SickingMarch 7th, 2012 at 20:12gregMarch 8th, 2012 at 12:26Lars GuntherMarch 7th, 2012 at 07:38abcNovember 6th, 2012 at 05:45AlenasMarch 7th, 2012 at 21:03PeteMarch 8th, 2012 at 00:53regisMarch 8th, 2012 at 06:29RedMarch 9th, 2012 at 07:21Shawn WilsherMarch 13th, 2012 at 23:31RedMarch 14th, 2012 at 23:26PeteMarch 15th, 2012 at 01:55Nigel KellyMarch 14th, 2012 at 05:10richtaurMarch 14th, 2012 at 10:33steveMarch 15th, 2012 at 05:26GregorMarch 19th, 2012 at 08:56FooMarch 19th, 2012 at 11:07DanniiMarch 19th, 2012 at 22:53RedMarch 20th, 2012 at 03:34ParashuramJune 7th, 2012 at 00:27Marcello NuccioJune 19th, 2012 at 23:22Taras GlekJune 20th, 2012 at 11:37Marcello NuccioJune 20th, 2012 at 23:23JulienWJune 21st, 2012 at 00:08Todd BlanchardNovember 9th, 2012 at 10:56Marcello NuccioJune 21st, 2012 at 01:05MicahSeptember 14th, 2012 at 00:12Robert NymanSeptember 14th, 2012 at 02:01Vance IngallsSeptember 17th, 2012 at 16:29StanOctober 10th, 2012 at 06:37Todd BlanchardNovember 9th, 2012 at 10:53PeteNovember 10th, 2012 at 01:48Todd BlanchardNovember 10th, 2012 at 12:01RedNovember 10th, 2012 at 12:54IvanDecember 2nd, 2012 at 21:01MarcoDecember 16th, 2012 at 04:40RedFebruary 5th, 2013 at 04:17JulienWFebruary 5th, 2013 at 05:40PeteFebruary 5th, 2013 at 06:22JulienWFebruary 5th, 2013 at 06:48Todd BlanchardFebruary 5th, 2013 at 11:15PeteFebruary 5th, 2013 at 11:23JulienWFebruary 5th, 2013 at 11:28RedFebruary 5th, 2013 at 13:07Julien WajsbergFebruary 6th, 2013 at 00:56RedFebruary 6th, 2013 at 06:33PeteFebruary 5th, 2013 at 12:22Todd BlanchardFebruary 6th, 2013 at 08:14