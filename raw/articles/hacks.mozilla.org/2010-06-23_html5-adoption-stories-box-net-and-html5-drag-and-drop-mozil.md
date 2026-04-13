---
title: 'HTML5 adoption stories: box.net and html5 drag and drop – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2010/06/html5-adoption-stories-box-net-and-html5-drag-and-drop/
author: Christopher Blizzard
published: '2010-06-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post from Tomas Barreto, a developer who works at box.net. They recently adopted HTML5 drag and drop as a way to share files with other people using new features in Firefox. The included video is a pitch for the feature and service, but shows how easy it is to do simple HTML5-based upload progress even with multiple files. Tomas gives an overview of the relatively simple JavaScript required to do this, and how improvements in Firefox 4 will make things even easier. Also have a quick look at the bottom of the post for links to additional docs and resources.
*

At Box.net, we’re always exploring new ways to help users get content quickly and securely onto our cloud content management platform. So when asked, “What feature would make you use Box more?” during the Box Hack Olympics in April, my colleague CJ and I decided to tackle the most intuitive way to upload files: simply dragging them from the desktop into Box.

We considered technologies ranging from Gears to Firefox plugins, but only HTML5 had sufficient adoption. By using some of the JavaScript APIs defined in the HTML5 standard, CJ and I could create a seamless drag and drop experience for our users on supporting browsers. Furthermore, using an HTML5-based upload feature would allow us to enable users to select multiple files at once, and also display progress on the client without polling. And with HTML5 adoption across the latest versions of three of the top four browsers, we felt confident about building an upload method based on this new technology without the trade-offs of using a third-party plug-in.

We rolled out the first rev of our drag and drop feature a few weeks ago, and we’re impressed with how quickly it has been adopted. It’s already one of the most popular ways to get files onto Box, and in its first week it surpassed our old AJAX upload method. You can check out our demo video to get a feel for the feature:

To build this feature, we referenced a handful of online examples that explained how to use Firefox 3 [FileReader](https://developer.mozilla.org/en/DOM/FileReader) object and the drag and drop file event support. Our first implementation used this object to load the file into memory and then took advantage of the latest [XMLHttpRequest](https://developer.mozilla.org/En/Using_XMLHttpRequest) events to track progress on the client.

```
var files = event.originalEvent.dataTransfer.files; // drop event
var reader = new FileReader();
reader.onload = function(event) {
var file_contents = event.target.result;
var request = new XMLHttpRequest();
... // attach event listeners to monitor progress and detect errors
var post_body = '';
.. // build post body
post_body += file_contents;
.. // finish post body
var url = 'http://example.com/file_upload';
var request = new XMLHttpRequest();
request.open("POST", url, true); // open asynchronous post request
request.setRequestHeader('content-type', 'multipart/form-data; boundary=""'); // make sure to set a boundary
request.send(post_body);
}
reader.readAsBinaryString(files[0]);
```

This approach worked well because we could use the same server processing code that we previously used for uploads. The main disadvantage here is that the FileReader object reads the entire file into memory, which is not optimal for a general upload use case. Our current HTML5 implementation uses this logic and has forced us to restrict drag and drop uploads to just 25mb. However, thanks to recommendations from the Mozilla team, we’ll be taking an alternative approach for V2 of drag and drop, where the file is read chunks as needed by the request. Here’s how we’re going to do it:

```
var files = event.originalEvent.dataTransfer.files; // drop event
var url = 'http://example.com/file_upload';
var request = new XMLHttpRequest();
request.open("POST", url, true); // open asynchronous post request
request.send(files[0]);
```

Since this approach is not formatted as a multipart form-data, it will require some adjustments on our back-end to support receiving file uploads in this way. However, it’s definitely worth the trade-off since we’ll get all the benefits of the previous method and we don’t need special file size restrictions. In the future, we’ll consider using [yet another way to efficiently upload files that is supported in Firefox 4 and uses the traditional multi-part form](http://hacks.mozilla.org/2010/05/formdata-interface-coming-to-firefox/):

```
var files = event.originalEvent.dataTransfer.files; // drop event
var url = 'http://example.com/file_upload';
var request = new XMLHttpRequest();
var fd = new FormData;
fd.append("myFile", files[0]);
request.open("POST", url, true); // open asynchronous post request
request.send(fd);
```

We’re already exploring more ways to enrich the Box experience using HTML5. With HTML5, we can build faster, richer and more interactive features with native browser support, and bridge the traditional gap between desktop software and web applications. Here are just a few cool new upload-related features on our roadmap:

- Pause/Resume uploads using the Blob slice API to split files into chunks (this will be a huge robustness boost, especially for large uploads)
- Allowing uploads to resume even after the browser closes by caching the file using
[IndexedDB](http://hacks.mozilla.org/2010/06/comparing-indexeddb-and-webdatabase/)support (possibly in Firefox 4)

We’d also like to begin a discussion about supporting the reverse drag and drop use case: dragging files from the browser to the desktop. Based on our users’ enthusiasm around the drag and drop upload feature, we think the reverse functionality would well received. If you are interested in contributing to a specification for this feature, please let us know (html5 [-at$] box.net)!

Resources:

## 12 comments

wildanr05June 24th, 2010 at 18:51SanderTJune 25th, 2010 at 02:14SanderTJuly 23rd, 2010 at 03:01arieffJune 26th, 2010 at 23:07lenJuly 1st, 2010 at 14:29RyanJuly 4th, 2010 at 22:40ardhanJuly 7th, 2010 at 22:55detJuly 18th, 2010 at 23:04Komrade KilljoyJuly 28th, 2010 at 05:52Dave MerrillMarch 17th, 2011 at 04:32DavidJuly 6th, 2011 at 06:52YasinDecember 24th, 2011 at 05:51