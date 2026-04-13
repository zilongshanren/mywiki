---
title: Why no FileSystem API in Firefox? – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/07/why-no-filesystem-api-in-firefox/
author: Jonas Sicking
published: '2012-07-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A question that I get asked a lot is why Firefox doesn’t support the FileSystem API. Usually, but not always, they are referring specifically to the [FileSystem](http://dev.w3.org/2009/dap/file-system/file-dir-sys.html) and [FileWriter](http://dev.w3.org/2009/dap/file-system/file-writer.html) specifications which Google is implementing in Chrome, and which they have proposed for standardization in W3C.

The answer is somewhat complex, and depends greatly on what exact capabilities of the above two specifications the person is actually wanting to use. The specifications are quite big and feature full, so it’s no surprise that people are wanting to do very different things with it. This blog post is an attempt at giving **my** answer to this question and explain why we haven’t implemented the above two specifications. But note that this post represents my personal opinion, intended to spur more conversation on this topic.

As stated above, people asking for “FileSystem API support” in Firefox are actually often interested in solving many different problems. In my opinion most, but so far not all, of these problems have better solutions than the FileSystem API. So let me walk through them below.

## Storing resources locally

Probably the most common thing that people want to do is to simply store a set of resources so that they are available without having to use the network. This is useful if you need quick access to the resources, or if you want to be able to access them even if the user is offline. Games are a very common type of application where this is needed. For example an enemy space ship might have a few associated images, as well as a couple of associated sounds, used when the enemy is moving around the screen and shooting. Today, people generally solve this by storing the images and sound files in a file system, and then store the file names of those files along with things like speed and firepower of the enemy.

However it seems a bit non-optimal to me to have to store some data separated from the rest. Especially when there is a solution which can store both structured data as well as file data. IndexedDB treats file data just like any other type of data. You can write a `File`

or a `Blob`

into IndexedDB just like you can store strings, numbers and JavaScript objects. This is specified by the IndexedDB spec and so far implemented in both the Firefox and IE implementations of IndexedDB. Using this, you can store all information that you need in one place, and a single query to IndexedDB can return all the data you need. So for example, if you were building a web based email client, you could store an object like:

`{`


subject: "Hi there",

body: "Hi Sven,\nHow are you doing...",

attachments: [blob1, blob2, blob3]

}

Another advantage here is that there’s no need to make up file names for resources. Just store the `File`

or `Blob`

object. No name needed.

In Firefox’s IndexedDB implementation (and I believe IE’s too) the files are transparently stored outside of the actual database. This means that performance of storing a file in IndexedDB is just as good as storing the file in a filesystem. It does not bloat the database itself slowing down other operations, and reading from the file means that the implementation just reads from an OS file, so it’s just as fast as a filesystem.

Firefox IndexedDB implementation is even smart enough that if you store the same Blob multiple files in a IndexedDB database it just creates one copy of the file. Writing further references to the same Blob just adds to an internal reference counter. This is completely transparent to the web page, the only thing it will notice is faster writes and less resource use. However I’m not sure if IE does the same, so check there first before relying on it.

## Access pictures and music folders

The second most common thing that people ask for related to a file system APIs is to be able to access things like the user’s picture or music libraries. This is something that the FileSystem API submitted to W3C doesn’t actually provide, though many people seems to think it does. To satisfy that use-case we have the [DeviceStorage API](https://wiki.mozilla.org/WebAPI/DeviceStorageAPI). This API allows full file system capabilities for “user files”. I.e. files that aren’t specific to a website, but rather resources that are managed and owned by the user and that the user might want to access through several apps. Such as photos and music. The DeviceStorage API is basically a simple file system API mostly optimized for these types of files.

We’re still in the process of specifying and implementing this API. It’s available to test with in recent nightly builds, but so far isn’t enabled by default. The main problem with exposing this functionality to the web is security. You wouldn’t want just any website to read or modify your images. We could put up a prompt like we do with the GeoLocation API, given that this API potentially can delete all your pictures from the last 10 years, we probably want something more. This is something we are actively working on. But it’s definitely the case here that security is the hard part here, not implementing the low-level file operations.

## Low-level file manipulation

A less common request is the ability to do low-level create, read, update and delete (CRUD) file operations. For example being able to write 10 bytes in the middle of a 10MB file. This is not something IndexedDB supports right now, it only allows adding and removing whole files. This is supported by the FileWriter specification draft. However I think this part of this API has some pretty fundamental problems. Specifically there are no locking capabilities, so there is no way to do multiple file operations and be sure that another tab didn’t modify or read the file in between those operations. There is also no way to do fsync which means that you can’t implement ACID type applications on top of FileWriter, such as a database.

We have instead created an API with the same goal, but which has capabilities for locking a file and doing multiple operations. This is done in a way to ensure that there is no risk that pages can forget to unlock a file, or that deadlocks can occur. The API also allows fsync operations which should enable doing things like databases on top of FileHandle. However most importantly, the API is done in such a way that you shouldn’t need to nest asynchronous callbacks as much as with FileWriter. In other words it should easier to use for authors. You can read more about FileHandle at

## The `filesystem`

URL scheme

There is one more capability that exist in the FileSystem API not covered above. The specification introduces a new `filesystem:`

URL scheme. When loading URLs from `filesystem:`

it returns the contents of files in stored using the FileSystem API. This is a very cool feature for a couple of reasons. First of all these URLs are predictable. Once you’ve stored a file in the file system, you always know which URL can be used to load from it. And the URL will continue to work as long as the file is stored in the file system, even if the web page is reloaded. Second, relative URLs work with the `filesystem:`

scheme. So you can create links from one resource stored in the filesystem to another resource stored in the filesystem.


Firefox does support the `blob:`

URL scheme, which does allow loading data from a Blob anywhere where URLs can be used. However it doesn’t have the above mentioned capabilities. This is something that I’d really like to find a solution for. If we can’t find a better solution, implementing the Google specifications is definitely an option.

## Conclusions

As always when talking about features to be added to the web platform it’s important to talk about use cases and capabilities, and not jump directly to a particular solution. Most of the use cases that the FileSystem API aims to solve can be solved in other ways. In my opinion many times in better ways.

This is why we haven’t prioritized implementing the FileSystem API, but instead focused on things like making our IndexedDB implementation awesome, and coming up with a good API for low-level file manipulation.

Focusing on IndexedDB has also meant that we very soon have a good API for basic file storage available in 3 browsers: IE10, Firefox and Chrome.

On a related note, we just fixed the last known spec compliance issues in our IndexedDB implementation, so Firefox 16 will ship with IndexedDB unprefixed!

As always, we’re very interested in getting feedback from other people, especially from web developers. Do you think that FileSystem API is something we should prioritize? If so, why?

## About Jonas Sicking

Jonas has been hacking on web browsers for over a decade. He started as a open source contributor in 2000 contributing to the newly open sourced mozilla project. In 2005 he joined mozilla full time and has since been working on the DOM and other parts of the web platform. He is now the Tech Lead of the Web API project at mozilla as well as an editor for the IndexedDB and File API specifications at W3C.

## 117 comments

Neel MehtaJuly 5th, 2012 at 13:41Devon GovettJuly 5th, 2012 at 13:45Jonas SickingJuly 5th, 2012 at 13:53Marat DenenbergJuly 5th, 2012 at 13:50Devon GovettJuly 5th, 2012 at 14:01Jonas SickingJuly 5th, 2012 at 14:23Robert KaiserJuly 5th, 2012 at 15:47Devon GovettJuly 5th, 2012 at 16:16Devon GovettJuly 5th, 2012 at 13:56Devon GovettJuly 5th, 2012 at 13:57Robert NymanJuly 5th, 2012 at 14:21Jonas SickingJuly 5th, 2012 at 16:26Devon GovettJuly 5th, 2012 at 16:42Jonas SickingJuly 5th, 2012 at 16:56Samuel ErdtmanJuly 5th, 2012 at 15:12DanielJuly 5th, 2012 at 16:03Jonas SickingJuly 5th, 2012 at 16:19Angelo BorsottiSeptember 15th, 2012 at 01:17DanielJuly 5th, 2012 at 16:25Jonas SickingJuly 5th, 2012 at 16:31DanielJuly 5th, 2012 at 16:36Style ThingJuly 5th, 2012 at 23:47Tane PiperJuly 6th, 2012 at 01:22Jonas SickingJuly 9th, 2012 at 20:50Jussi KalliokoskiJuly 6th, 2012 at 04:18Jonas SickingJuly 9th, 2012 at 20:51OlegJuly 6th, 2012 at 08:43Jonas SickingJuly 9th, 2012 at 22:04Eric UhrhaneJuly 10th, 2012 at 16:55Jonas SickingJuly 9th, 2012 at 22:05Eric BidelmanJuly 6th, 2012 at 09:23Eric UhrhaneJuly 6th, 2012 at 17:10Jonas SickingJuly 9th, 2012 at 22:18Brian StellMarch 21st, 2013 at 16:17Jonas SickingMarch 22nd, 2013 at 11:38Brian StellMarch 22nd, 2013 at 13:26Jonas SickingMarch 22nd, 2013 at 14:10pdJuly 7th, 2012 at 00:44Jonas SickingJuly 9th, 2012 at 22:29Eric UhrhaneJuly 10th, 2012 at 17:01John ThomasJuly 10th, 2012 at 05:58Eric UhrhaneJuly 10th, 2012 at 18:41Joran GreefJuly 19th, 2012 at 00:48Jonas SickingJuly 19th, 2012 at 01:54Joran GreefJuly 19th, 2012 at 03:19BenzOctober 20th, 2012 at 13:07Jonas SickingOctober 21st, 2012 at 10:13BenzOctober 21st, 2012 at 11:04Daniel O’CallaghanJanuary 3rd, 2013 at 21:13Michaela MerzJanuary 13th, 2013 at 18:26Jonas SickingJanuary 14th, 2013 at 18:23Michaela MerzJanuary 17th, 2013 at 15:45Jonas SickingJanuary 17th, 2013 at 16:49Michaela MerzJanuary 18th, 2013 at 01:37Michaela MerzJanuary 18th, 2013 at 01:51Jonas SickingJanuary 18th, 2013 at 02:13Jonas SickingJanuary 18th, 2013 at 02:16Michaela MerzJanuary 18th, 2013 at 02:50Jonas SickingJanuary 18th, 2013 at 03:00BenzJanuary 18th, 2013 at 04:03Michaela MerzJanuary 18th, 2013 at 14:25Jonas SickingJanuary 18th, 2013 at 14:57Michaela MerzJanuary 18th, 2013 at 15:06BenzJanuary 18th, 2013 at 15:29Michaela MerzJanuary 18th, 2013 at 15:43Geoff FlarityJanuary 19th, 2013 at 06:54maxw3stFebruary 1st, 2013 at 21:46Michaela MerzFebruary 4th, 2013 at 13:02John McLaneFebruary 9th, 2013 at 09:48Anthony CaudillFebruary 14th, 2013 at 08:52Jonas SickingFebruary 14th, 2013 at 20:40Jonas SickingFebruary 14th, 2013 at 20:45Anthony CaudillFebruary 14th, 2013 at 23:40Michaela MerzFebruary 15th, 2013 at 05:39Jonas SickingFebruary 15th, 2013 at 06:13Michaela MerzFebruary 15th, 2013 at 06:28Jonas SickingFebruary 15th, 2013 at 07:12Rob HigginsFebruary 21st, 2013 at 18:18Anthony CaudillMarch 4th, 2013 at 10:27Angelo BorsottiMarch 4th, 2013 at 11:49RobMarch 4th, 2013 at 22:34Brett ZamirMarch 13th, 2013 at 02:51Michaela MerzMarch 5th, 2013 at 08:21Angelo BorsottiMarch 5th, 2013 at 11:37Jonas SickingMarch 5th, 2013 at 11:45Michaela MerzMarch 5th, 2013 at 14:17Angelo BorsottiMarch 5th, 2013 at 16:42Michaela MerzMarch 5th, 2013 at 18:14Angelo BorsottiMarch 6th, 2013 at 00:54Michaela MerzMarch 6th, 2013 at 01:30Angelo BorsottiMarch 6th, 2013 at 02:25Rob HigginsMarch 6th, 2013 at 13:21Angelo BorsottiMarch 6th, 2013 at 16:59Rob HigginsMarch 6th, 2013 at 19:04Angelo BorsottiMarch 7th, 2013 at 00:50Anthony CaudillMarch 12th, 2013 at 23:18Anthony CaudillMarch 12th, 2013 at 23:35Brett ZamirMarch 13th, 2013 at 03:25Brett ZamirMarch 13th, 2013 at 03:46Rob HigginsMarch 14th, 2013 at 11:08Rob HigginsMarch 14th, 2013 at 12:09Anthony CaudillMarch 14th, 2013 at 12:21Brett ZamirMarch 14th, 2013 at 16:49Brett ZamirMarch 14th, 2013 at 16:37Rob HigginsMarch 14th, 2013 at 16:50Angelo BorsottiMarch 14th, 2013 at 13:17Rob HigginsMarch 14th, 2013 at 13:50Angelo BorsottiMarch 15th, 2013 at 00:08Brett ZamirMarch 14th, 2013 at 18:21Brett ZamirMarch 14th, 2013 at 18:31Michaela MerzMarch 15th, 2013 at 02:25RobMarch 16th, 2013 at 13:22Brett ZamirMarch 16th, 2013 at 18:51Angelo BorsottiMarch 16th, 2013 at 15:34Brett ZamirMarch 16th, 2013 at 18:53RobMarch 17th, 2013 at 10:43Brett ZamirMarch 18th, 2013 at 18:50