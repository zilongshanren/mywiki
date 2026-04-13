---
title: Firefox 4 – FormData and the new File.url object – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2010/07/firefox-4-formdata-and-the-new-file-url-object/
author: Christopher Blizzard
published: '2010-07-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post from Jonas Sicking, who does much of the work inside of Gecko on content facing features. He covers FormData, which we’ve talked about before, but shows how it can connect to an important part of the File API we’ve added for Firefox 4: File.url.*

In Firefox 4 we’re continuing to add support for easier and better file handling. Two features that are available in Firefox 4 Beta 1 are `File.url`

and `FormData`

. In this post I’ll give a short introduction to both of them.

Starting with Firefox 3.6 we supported a standardized way of reading files using the `FileReader`

object. This object allowed you to read the contents of a file into memory to analyze its content or display the contents to the user. For example to display a preview of an image to a user, you could use the following script

```
var reader = new FileReader();
reader.onload = function() {
previewImage.src = reader.result;
}
reader.readAsDataURL(myFile);
```

There are two unfortunate things to note here. First of all, `reader.result`

is a data url which contains the whole contents of the file. I.e. the full file contents is kept in memory. Not only that, data urls are often base64 encoded, and each base64 encoded character is stored in a javascript character, which generally uses 2 bytes of memory. The result is that if the above code is used to read a 10MB image file, `reader.result`

is a 26.7MB large string.

The other unfortunate thing is that the above code is somewhat complicated since it needs to use asynchronous events to read from disk.

In Firefox 4 Beta 1 you can instead use the following code

```
previewImage.src = myFile.url;
```

This uses the `File.url`

property defined by the [File API](http://dev.w3.org/2006/webapi/FileAPI/) specification. The property returns a short, about 40 characters, url. The contents of this url you generally won’t have to care about, but for the interested it contains a randomly generated identifier prefixed by a special scheme.

This can url can then be used anywhere where generic urls are used, and reading from that url directly reads from the file. The example above makes the image element read directly from the file and display the resulting image to the user. The load works just like when loading from a http url, normal ‘load’ events and ‘error’ events are fired as appropriate.

You can also display HTML files by using an `<iframe>`

and setting its `src`

to the value returned by `File.url`

. However you have to watch out for that relative url in the HTML file won’t work as the relative urls are resolved against the generated url returned from `File.url`

. This is intentional as the user might have only granted access to the HTML file, and not to the image files.

Other places where this URL can be useful is for CSS background images, to set the background of an element to use a local file. Or even read from the url using `XMLHttpRequest`

if you have existing code that uses `XMLHttpRequest`

and which you don’t want to convert to use `FileReader`

.

The other feature that we are supporting in Firefox 4 Beta 1 is the `FormData`

object. This object is useful if you have existing server infrastructure for receiving files which uses `multipart/form-data`

encoding.

In Firefox 3.6, sending a file to a server using `multipart/form-data`

encoding using `XMLHttpRequest`

required a a bit of manual work. You had to use a `FileReader`

to read the contents of the file into memory, then manually `multipart/form-data`

encode it, and then finally send it to a server. This both required more code, as well as required that the whole file contents was read into memory.

In Firefox 4, you’ll be able to use the FormData object from the [XMLHttpRequest Level 2](http://dev.w3.org/2006/webapi/XMLHttpRequest-2/Overview.html) specification. This allows the following clean code

```
var fd = new FormData();
fd.append("fileField", myFile);
var xhr = new XMLHttpRequest();
xhr.open("POST", "file_handler.php");
xhr.send(fd);
```

This will automatically `multipart/form-data`

encode the file and send it to the server. The contents of the file is read in small chunks and thus doesn’t use any significant amounts of memory. It will send the same contents as a form with the following markup:

```
```

If you want to send multiple files, simply call `fd.append`

for each file you want to submit and the files will all be sent in a single request. You can of course still use the normal progress events, both for upload and download progress, that `XMLHttpRequest`

always supplies.

However `FormData`

also has another nice feature. You can also send normal, non-file, `multipart/form-data`

values. For example

```
var fd = new FormData();
fd.append("author", "Jonas Sicking");
fd.append("name", "New File APIs");
fd.append("attachment1", file1);
fd.append("attachment2", file2);
var xhr = new XMLHttpRequest();
xhr.open("POST", "file_handler.php");
xhr.send(fd);
```

You can even get a FormData object which contains all the information from a `<form>`

. (However note that the syntax for this is likely to change before final release)

```
var fd = myFormElement.getFormData();
var xhr = new XMLHttpRequest();
xhr.open("POST", "file_handler.php");
xhr.send(fd);
```

Here `fd`

will contain data from all the form fields, from radio buttons to file fields, that are contained in the form.

As always, we’re all ears for feedback about these features. Please let us know what you think, and especially if you have tested them out and they do not appear to do what you expect them to. You can use [http://www.mozilla.com/en-US/firefox/beta/feedback/](http://www.mozilla.com/en-US/firefox/beta/feedback/) to give us feedback, or use the feedback button in the upper right corner (see below screenshot).

![](https://farm2.static.flickr.com/1373/4728758428_bc8645d408.jpg)


## 20 comments

DavidJuly 8th, 2010 at 09:56Jonas SickingJuly 12th, 2010 at 02:00Paul RougetJuly 15th, 2010 at 21:28srigiJuly 13th, 2010 at 09:18AnshumanJuly 15th, 2010 at 00:28tobiistgutJuly 16th, 2010 at 15:20Jonas SickingJuly 24th, 2010 at 21:14FirenzeJuly 25th, 2010 at 18:17Paul RougetJuly 26th, 2010 at 01:41Werner PunzAugust 1st, 2010 at 08:29Werner PunzAugust 1st, 2010 at 13:03Kensaku KOMATSUAugust 24th, 2010 at 23:39mawryaAugust 29th, 2010 at 20:49Shiv KumarSeptember 19th, 2010 at 22:08Shiv KumarSeptember 22nd, 2010 at 23:09MichelOctober 27th, 2010 at 09:17SolNovember 22nd, 2010 at 01:02Radek TetíkFebruary 15th, 2011 at 06:04CopyKatMarch 16th, 2012 at 04:02Stephanie ManleyMarch 28th, 2012 at 03:56