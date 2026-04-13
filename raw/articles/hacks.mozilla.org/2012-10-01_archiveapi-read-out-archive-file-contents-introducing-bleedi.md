---
title: ArchiveAPI – read out archive file contents + Introducing Bleeding Edge – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/10/archiveapi-read-out-archive-file-contents-introducing-bleeding-edge/
author: Robert Nyman
published: '2012-10-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Working with files on the web has been a challenge for a long time, and when things like [various File APIs](https://developer.mozilla.org/en-US/docs/DOM/File_APIs) have surfaced, it has made me really happy! Now on to the latest edition: [ArchiveAPI](https://wiki.mozilla.org/WebAPI/ArchiveAPI), giving the ability to work with archive files.

## Introducing Bleeding Edge

Before I start talking about the ArchiveAPI, I wanted to introduce the new [Bleeding Edge category](https://hacks.mozilla.org/category/bleeding-edge/) here on Mozilla Hacks. What this means is that we cover technologies/features/APIs that haven’t been released in an official version of Firefox, or any other web browser, yet. It covers things that, in most cases, have their first initial implementation in [Firefox Nightly](http://nightly.mozilla.org/) or [Firefox Aurora](http://www.mozilla.org/firefox/aurora/).

The goal is to have these features shipped, but given feedback from you, dear developers, or any other findings during this phase might result in changes to them before they are released.

So, feel more than welcome to try them out! Either you have a headstart on knowing what’s coming, or you have the possibility of affecting the future of features for developers on the web. Win-win! :-)

## What it is

As part of our [WebAPI initiative at Mozilla](https://wiki.mozilla.org/WebAPI/) to make the web an even more powerful platform, I was lucky to talk to Andrea Marchesini, the Lead Developer of the ArchiveAPI. Basically, it allows you to read the content of archive files, e.g. ZIP files, directly in web browsers.

Basically, we have an `ArchiveReader`

object and when it successfully manages to read the contents of an archive file, we can iterate over them, read out file data, show previews of each file’s content etc.

```
var archiveFile = new ArchiveReader(archiveFileReference),
fileNames = archiveFile.getFilenames();
```

When you trigger an action/method on this file, like `getFilenames`

, you will have two handlers: `onsuccess`

and `onerror`

. Like this:

```
fileNames.onerror = function () {
console.log("Error reading filenames");
};
fileNames.onsuccess = function (request) {
// Get list of files in the archive
var result = this.result;
// Iterate over those files
for (var i=0, l=result.length; i<l; i++) {
file = archiveFile.getFile(result[i]);
file.onerror = function () {
console.log("Error accessing file");
};
file.onsuccess = function () {
// Read out data for that file, such as name, type and size
var currentFile = this.result;
console.log(currentFile.name);
}
}
}
```

## Demo

I’ve put together an [ArchiveAPI demo](http://mozilla.github.com/mozhacks/archive-api/) where you can upload an archive file and for any of the image or text files within that archive, it will directly generate a preview in the web page. The [code is available on GitHub](https://github.com/mozilla/mozhacks/tree/gh-pages/archive-api), as part of our [mozhacks GitHub repositiory](https://github.com/mozilla/mozhacks/).

Note: currently this demo only works in [Firefox Aurora](http://www.mozilla.org/firefox/aurora/) and [Firefox Nightly](http://nightly.mozilla.org/).

I’ve also put together a [screencast of this demo at YouTube](http://www.youtube.com/watch?v=6gWZIId-ypI):

(If you’ve opted in to [HTML5 video on YouTube](https://www.youtube.com/html5) you will get that, otherwise it will fallback to Flash)

## Feedback

I hope you find this interesting, and one more step forward for the web as a platform! Please let us know what you think in a comment here.

Additionally, there’s a poll/questionnaire you can take with regards to the asynchronous nature of ArchiveAPI. It’s available in [Feedback on potential ArchiveReader APIs](https://docs.google.com/spreadsheet/viewform?formkey=dGV6SVJzSnlfdTYyOURYMHNUTGJNcUE6MQ#gid=0).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 16 comments

AndreiOctober 1st, 2012 at 12:33Robert NymanOctober 1st, 2012 at 13:22Beben KobenOctober 1st, 2012 at 13:34Robert NymanOctober 2nd, 2012 at 02:26DeveloperOctober 1st, 2012 at 17:38Robert NymanOctober 2nd, 2012 at 02:28Calvin Spealman (@ironfroggy)October 1st, 2012 at 19:09Robert NymanOctober 2nd, 2012 at 02:29Forrest O.October 2nd, 2012 at 06:36Robert NymanOctober 2nd, 2012 at 06:39Ken SaundersOctober 2nd, 2012 at 18:44Robert NymanOctober 3rd, 2012 at 03:56JasonOctober 4th, 2012 at 19:17Robert NymanOctober 5th, 2012 at 02:18JasonOctober 6th, 2012 at 07:58Robert NymanOctober 8th, 2012 at 02:56