---
title: Saving images and files in localStorage – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/02/saving-images-and-files-in-localstorage/
author: Robert Nyman
published: '2012-02-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As you might know, [localStorage](https://developer.mozilla.org/en/DOM/Storage) is quite powerful when it comes to quickly storing information in the user’s web browser, and it has also been around in all web browsers a long time. But how do we store files in it?

*Please also make sure to read Storing images and files in IndexedDB*.


## Using JSON for powerful control

Let’s start with some basic information about localStorage. When storing information in localStorage, you use key/value pairs, like this:

`localStorage.setItem("name", "Robert");`


And to read it out, you just get the value of that key:

`localStorage.getItem("name");`


That’s all good and well, and being able to save at least 5 MB, you have a lot of options. But since localStorage is just string-based, saving a long string with no form of structure isn’t optimal.

Therefore, we can utilize the native JSON support in web browsers to turn JavaScript objects to string for saving, and back into objects when reading:



var cast = { "Adm. Adama" : "Edward James Olmos", "President Roslin" : "Mary McDonnell", "Captain Adama" : "Jamie Bamber", "Gaius Baltar" : "James Callis", "Number Six" : "Tricia Helfer", "Kara Thrace" : " Katee Sackhoff" }; // Stores the JavaScript object as a string localStorage.setItem("cast", JSON.stringify(cast)); // Parses the saved string into a JavaScript object again JSON.parse(localStorage.getItem("cast"));

## Storing images

The idea here is to be able to take an image that has been loaded into the current web page and store it into localStorage. As we established above, localStorage only supports strings, so what we need to do here is turn the image into a [Data URL](http://en.wikipedia.org/wiki/Data_URI_scheme). One way to do this for an image, is to load into a [canvas element](https://developer.mozilla.org/en/HTML/Canvas). Then, with a `canvas`

, you can read out the current visual representation in a canvas as a Data URL.

Let’s look at this example where we have an image in the document with an `id`

of “elephant”:



// Get a reference to the image element var elephant = document.getElementById("elephant"); // Take action when the image has loaded elephant.addEventListener("load", function () { var imgCanvas = document.createElement("canvas"), imgContext = imgCanvas.getContext("2d"); // Make sure canvas is as big as the picture imgCanvas.width = elephant.width; imgCanvas.height = elephant.height; // Draw image into canvas element imgContext.drawImage(elephant, 0, 0, elephant.width, elephant.height); // Get canvas contents as a data URL var imgAsDataURL = imgCanvas.toDataURL("image/png"); // Save image into localStorage localStorage.setItem("elephant", imgAsDataURL); }, false);

Then, if we want to take it further, we can utilize a JavaScript object and do a date check with localStorage. In this example, we load the image from the server through JavaScript the first time, but for every page load after that, we read the saved image from localStorage instead:

### HTML



<figure> <img id="elephant" src="about:blank" alt="A close up of an elephant"> <noscript> <img src="elephant.png" alt="A close up of an elephant"> </noscript> <figcaption>A mighty big elephant, and mighty close too!</figcaption> </figure>

### JavaScript



// localStorage with image var storageFiles = JSON.parse(localStorage.getItem("storageFiles")) || {}, elephant = document.getElementById("elephant"), storageFilesDate = storageFiles.date, date = new Date(), todaysDate = (date.getMonth() + 1).toString() + date.getDate().toString(); // Compare date and create localStorage if it's not existing/too old if (typeof storageFilesDate === "undefined" || storageFilesDate < todaysDate) { // Take action when the image has loaded elephant.addEventListener("load", function () { var imgCanvas = document.createElement("canvas"), imgContext = imgCanvas.getContext("2d"); // Make sure canvas is as big as the picture imgCanvas.width = elephant.width; imgCanvas.height = elephant.height; // Draw image into canvas element imgContext.drawImage(elephant, 0, 0, elephant.width, elephant.height); // Save image as a data URL storageFiles.elephant = imgCanvas.toDataURL("image/png"); // Set date for localStorage storageFiles.date = todaysDate; // Save as JSON in localStorage localStorage.setItem("storageFiles", JSON.stringify(storageFiles)); }, false); // Set initial image src elephant.setAttribute("src", "elephant.png"); } else { // Use image from localStorage elephant.setAttribute("src", storageFiles.elephant); }

**Note:** A word of warning here is that you might exceed the size available in localStorage, and the best way to control that is using `try...catch`

.

## Storing any kind of file

So thats great, we can use canvas to turn images into Data URL and save in localStorage. But what if we want a mechanism that works for any kind of file?

Then it becomes a bit interesting, and we will need to use:

The basic approach is:

- Do an XMLHttpRequest for a file, and set the responseType to “arraybuffer”
- Load the response, i.e. file, of the XMLHttpRequest into a Blob
- Use FileReader to read that file and load it into the page and/or localStorage

Let’s look at a complete example where we request an image named “rhino.png”, save it onto a blob, use FileReader to read out the file and finally save that in localStorage:



// Getting a file through XMLHttpRequest as an arraybuffer and creating a Blob var rhinoStorage = localStorage.getItem("rhino"), rhino = document.getElementById("rhino"); if (rhinoStorage) { // Reuse existing Data URL from localStorage rhino.setAttribute("src", rhinoStorage); } else { // Create XHR, Blob and FileReader objects var xhr = new XMLHttpRequest(), blob, fileReader = new FileReader(); xhr.open("GET", "rhino.png", true); // Set the responseType to arraybuffer. "blob" is an option too, rendering manual Blob creation unnecessary, but the support for "blob" is not widespread enough yet xhr.responseType = "arraybuffer"; xhr.addEventListener("load", function () { if (xhr.status === 200) { // Create a blob from the response blob = new Blob([xhr.response], {type: "image/png"}); // onload needed since Google Chrome doesn't support addEventListener for FileReader fileReader.onload = function (evt) { // Read out file contents as a Data URL var result = evt.target.result; // Set image src to Data URL rhino.setAttribute("src", result); // Store Data URL in localStorage localStorage.setItem("rhino", result); }; // Load blob as Data URL fileReader.readAsDataURL(blob); } }, false); // Send XHR xhr.send(); }

### Using “blob” as responseType

In the above example we used the responseType “arraybuffer” and a Blob to create something we could use for the FileReader. However, there’s also a responseType called “blob” which returns a blob directly that we can use with the FileReader. The above example would instead look like this then:



// Getting a file through XMLHttpRequest as an arraybuffer and creating a Blob var rhinoStorage = localStorage.getItem("rhino"), rhino = document.getElementById("rhino"); if (rhinoStorage) { // Reuse existing Data URL from localStorage rhino.setAttribute("src", rhinoStorage); } else { // Create XHR and FileReader objects var xhr = new XMLHttpRequest(), fileReader = new FileReader(); xhr.open("GET", "rhino.png", true); // Set the responseType to blob xhr.responseType = "blob"; xhr.addEventListener("load", function () { if (xhr.status === 200) { // onload needed since Google Chrome doesn't support addEventListener for FileReader fileReader.onload = function (evt) { // Read out file contents as a Data URL var result = evt.target.result; // Set image src to Data URL rhino.setAttribute("src", result); // Store Data URL in localStorage localStorage.setItem("rhino", result); }; // Load blob as Data URL fileReader.readAsDataURL(xhr.response); } }, false); // Send XHR xhr.send(); }

## Web browser support

- localStorage
- Supported since long in all major web browsers, including IE8.
- Native JSON support
- Same long support as localStorage.
- canvas element
- Supported a long in most major web browsers, but only since IE9.
- XMLHttpRequest Level 2
- Supported in Firefox and Google Chrome since long, Safari 5+ and planned to be in IE10 and Opera 12.
- Blob
- Supported in Firefox and Google Chrome since long, and is planned to be in IE10. Also in Safari 6.0+ and Opera Opera 12.1+
- FileReader
- Supported in Firefox and Google Chrome since long, Opera since 11.1 and is planned to be in IE10. Unclear about Safari.
- responseType “blob”
- Currently only supported in Firefox. Will soon be in Google Chrome and is planned to be in IE10. Unclear about Safari and Opera.

## Checking and clearing localStorage

The easiest way to check what’s in localStorage:

- Firebug: DOM tab, then scroll down to or search for localStorage
- Google Chrome: Developer Tools, under the Resources tab
- Opera: In the Storage tab in Opera Dragonfly

## Demo and code

I’ve put together a [demo with localStorage and saving images and files in it ](http://robnyman.github.com/html5demos/localstorage/) where you can see both the canvas approach and the one using XMLHtpRequest 2, Blob and FileReader.

The code for [storing files in localStorage](https://github.com/robnyman/robnyman.github.com/tree/master/html5demos/localstorage) is also available on GitHub, so go play now!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 46 comments

Andrea GimmarchiFebruary 21st, 2012 at 03:30Chris HeilmannFebruary 21st, 2012 at 03:44Robert NymanFebruary 21st, 2012 at 03:47Taras GlekMarch 2nd, 2012 at 11:59Robert NymanMarch 2nd, 2012 at 16:10Taras GlekFebruary 21st, 2012 at 15:25sonnyFebruary 21st, 2012 at 04:36Robert NymanFebruary 21st, 2012 at 06:35sonnyFebruary 21st, 2012 at 07:49Robert NymanFebruary 21st, 2012 at 07:51IvanFebruary 21st, 2012 at 05:28Robert NymanFebruary 21st, 2012 at 06:11Andrea GimmarchiFebruary 21st, 2012 at 05:34Chris HeilmannFebruary 21st, 2012 at 05:54Robert NymanFebruary 21st, 2012 at 06:15sonnyFebruary 21st, 2012 at 07:56Robert NymanFebruary 21st, 2012 at 08:03Andrea GiammarchiFebruary 21st, 2012 at 06:11Robert NymanFebruary 21st, 2012 at 06:16Andrea GiammarchiFebruary 21st, 2012 at 07:37Robert NymanFebruary 21st, 2012 at 07:49pdFebruary 21st, 2012 at 08:56Robert NymanFebruary 21st, 2012 at 09:14pdFebruary 22nd, 2012 at 08:37Robert NymanFebruary 22nd, 2012 at 11:30JoanFebruary 25th, 2012 at 11:31Robert NymanFebruary 26th, 2012 at 07:32Joan CreusFebruary 26th, 2012 at 07:49Robert NymanFebruary 26th, 2012 at 14:26Mihai CherejiFebruary 29th, 2012 at 16:55Robert NymanMarch 1st, 2012 at 04:31Cezary TomczykMarch 2nd, 2012 at 02:23Robert NymanMarch 2nd, 2012 at 02:53Cezary TomczykMarch 2nd, 2012 at 03:18Robert NymanMarch 2nd, 2012 at 03:19mihaiMarch 2nd, 2012 at 02:40Robert NymanMarch 2nd, 2012 at 02:54Mohamed JamaJune 27th, 2012 at 04:15Robert NymanJune 28th, 2012 at 02:23RaniOctober 4th, 2012 at 06:35Robert NymanOctober 4th, 2012 at 06:39SamNovember 17th, 2012 at 21:22benDecember 6th, 2012 at 08:49Robert NymanDecember 6th, 2012 at 08:58SidDecember 19th, 2012 at 04:20Robert NymanDecember 19th, 2012 at 16:09