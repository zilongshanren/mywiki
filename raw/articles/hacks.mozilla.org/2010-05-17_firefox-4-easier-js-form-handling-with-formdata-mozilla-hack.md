---
title: 'Firefox 4: easier JS form handling with FormData – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2010/05/formdata-interface-coming-to-firefox/
author: Paul Rouget
published: '2010-05-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This feature has landed in Mozilla Central (trunk) and only available with a Firefox Nightly Build for the time being.*

[XMLHttpRequest Level 2 (editor’s draft)](http://dev.w3.org/2006/webapi/XMLHttpRequest-2/Overview.html) adds support for the new FormData interface. FormData objects provide a way to easily construct a set of key/value pairs representing form fields and their values, which can then be easily sent using the XMLHttpRequest send() method in “multipart/form-data” format.

## Why FormData?

When you want to send complex data to a server from a web page (files, non-ASCII content), you must use the `multipart/form-data`

content type. To set the content type in a `<form>`

, you write:

```
```

This is what you usually do to upload a file.

Starting with Firefox 3.6, you can manipulate files with JavaScript (see [File API](https://developer.mozilla.org/en/Using_files_from_web_applications)), and maybe you want to send files using XMLHttpRequest. But if, for example, you want to reproduce this form, it’s really hard because you’ll have to create the `multipart/form-data`

content yourself in JavaScript (see, for example, [this code](https://developer.mozilla.org/media/uploads/demos/p/a/paulrouget/8bfba7f0b6c62d877a2b82dd5e10931e/hacksmozillaorg-achi_1334270447_demo_package/imageUploader/js/extends/xhr.js) I wrote a while ago implementing a `multipart/form-data`

: ugly and slow).

This is where FormData is useful: to reproduce the `<form>`

submission mechanism in JavaScript

## The FormData object

The FormData object lets you compile a set of key/value pairs to send using XMLHttpRequest. This object has only one method:

```
append(key, value);
```

where `key`

is the name of your value, and where `value`

can be a string or a file.

You can create a FormData object, append values and then send it through XMLHttpRequest. If you want to simulate the previous form, you write:

```
// aFile could be from an input type="file" or from a Dragged'n Dropped file
var formdata = new FormData();
formdata.append("nickname", "Foooobar");
formdata.append("website", "http://hacks.mozilla.org");
formdata.append("media", aFile);
var xhr = new XMLHttpRequest();
xhr.open("POST", "http://foo.bar/upload.php");
xhr.send(formdata);
```

## FormData and the `<form>`

element

Firefox extends the HTML form element slightly, adding a `getFormData()`

method that lets you fetch a form’s data as a FormData object. This is not yet part of the HTML standard, but is expected to be added to the specification at some point in the future (although possibly with a different name):

```
var formElement = document.getElementById("myFormElement");
var xhr = new XMLHttpRequest();
xhr.open("POST", "submitform.php");
xhr.send(formElement.getFormData());
```

You can also add data to the FormData object between retrieving it from a form and sending it, like this:

```
var formElement = document.getElementById("myFormElement");
formData = formElement.getFormData();
formData.append("serialnumber", serialNumber++);
xhr.send(formData);
```

This lets you augment the form’s data before sending it along, to include additional information that’s not necessarily user editable on the form.

## Resources

[MDN: XMLHttpRequest FormData](https://developer.mozilla.org/en/XMLHttpRequest/FormData)[MDN: Using FormData](https://developer.mozilla.org/En/XMLHttpRequest/Using_XMLHttpRequest#Using_FormData_objects)[W3C the FormData interface](http://dev.w3.org/2006/webapi/XMLHttpRequest-2/Overview.html#the-formdata-interface)[W3C the multipart/form-data content type](http://www.w3.org/TR/html401/interact/forms.html#h-17.13.4.2)[Bug 546528 – Implement FormData](https://bugzilla.mozilla.org/show_bug.cgi?id=546528)

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 21 comments

marcoosMay 17th, 2010 at 13:44Paul RougetMay 18th, 2010 at 05:32Edwin MartinMay 17th, 2010 at 15:31Brett ZamirMay 17th, 2010 at 21:38QOALMay 18th, 2010 at 03:06fpiatMay 18th, 2010 at 04:02Paul RougetMay 18th, 2010 at 06:39pdMay 18th, 2010 at 10:36AndyJune 21st, 2010 at 15:53AlfonsoMLJuly 1st, 2010 at 02:04kn33ch41July 18th, 2010 at 17:49kn33ch41July 18th, 2010 at 19:27Daniel KirschSeptember 21st, 2010 at 16:01Glenn MaynardDecember 17th, 2010 at 16:00AndréNovember 25th, 2012 at 15:23Robert NymanNovember 26th, 2012 at 01:28