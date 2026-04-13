---
title: Storing images and files in IndexedDB – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/02/storing-images-and-files-in-indexeddb/
author: Robert Nyman
published: '2012-02-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The other day we wrote about how to [Save images and files in localStorage](http://hacks.mozilla.org/2012/02/saving-images-and-files-in-localstorage/), and it was about being pragmatic with what we have available today. There are, however, a number of performance implications with localStorage – something that we will cover on this blog later – and the desired future approach is utilizing [IndexedDB](https://developer.mozilla.org/en/IndexedDB). Here I’ll walk you through how to store images and files in IndexedDB and then present them through an [ObjectURL](https://developer.mozilla.org/en/Document_Object_Model_%28DOM%29/window.URL.createObjectURL).


## The general approach

First, let’s talk about the steps we will go through to create an IndexedDB data base, save the file into it and then read it out and present in the page:

- Create or open a database.
- Create an objectStore (if it doesn’t already exist)
- Retrieve an image file as a blob
- Initiate a database transaction
- Save that blob into the database
- Read out that saved file and create an ObjectURL from it and set it as the src of an image element in the page

## Creating the code

Let’s break down all parts of the code that we need to do this:

### Create or open a database.



// IndexedDB window.indexedDB = window.indexedDB || window.webkitIndexedDB || window.mozIndexedDB || window.OIndexedDB || window.msIndexedDB, IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || window.OIDBTransaction || window.msIDBTransaction, dbVersion = 1; /* Note: The recommended way to do this is assigning it to window.indexedDB, to avoid potential issues in the global scope when web browsers start removing prefixes in their implementations. You can assign it to a varible, like var indexedDB… but then you have to make sure that the code is contained within a function. */ // Create/open database var request = indexedDB.open("elephantFiles", dbVersion);

request.onsuccess = function (event) {

console.log(“Success creating/accessing IndexedDB database”);

db = request.result;

db.onerror = function (event) {

console.log(“Error creating/accessing IndexedDB database”);

};

// Interim solution for Google Chrome to create an objectStore. Will be deprecated

if (db.setVersion) {

if (db.version != dbVersion) {

var setVersion = db.setVersion(dbVersion);

setVersion.onsuccess = function () {

createObjectStore(db);

getImageFile();

};

}

else {

getImageFile();

}

}

else {

getImageFile();

}

}

// For future use. Currently only in latest Firefox versions

request.onupgradeneeded = function (event) {

createObjectStore(event.target.result);

};


The intended way to use this is to have the `onupgradeneeded`

event triggered when a database is created or gets a higher version number. This is currently only supported in Firefox, but will soon be in other web browsers. If the web browser doesn’t support this event, you can use the deprecated `setVersion`

method and connect to its `onsuccess`

event.

### Create an objectStore (if it doesn’t already exist)



// Create an objectStore console.log("Creating objectStore") dataBase.createObjectStore("elephants");

Here you create an ObjectStore that you will store your data – or in our case, files – and once created you don’t need to recreate it, just update its contents.

### Retrieve an image file as a blob



// Create XHR and BlobBuilder var xhr = new XMLHttpRequest(), blob; xhr.open("GET", "elephant.png", true); // Set the responseType to blob xhr.responseType = "blob"; xhr.addEventListener("load", function () { if (xhr.status === 200) { console.log("Image retrieved"); // File as response blob = xhr.response; // Put the received blob into IndexedDB putElephantInDb(blob); } }, false); // Send XHR xhr.send();

This code gets the contents of a file as a `blob`

directly. Currently that’s only supported in Firefox.

Once you have received the entire file, you send the blob to the function to store it in the database.

### Initiate a database transaction



// Open a transaction to the database var transaction = db.transaction(["elephants"], IDBTransaction.READ_WRITE);

To start writing something to the database, you need to initiate a transaction with an objectStore name and the type of action you want to do – in this case read and write.

### Save that blob into the database



// Put the blob into the dabase transaction.objectStore("elephants").put(blob, "image");

Once the transaction is in place, you get a reference to the desired objectStore and then put your blob into it and give it a key.

### Read out that saved file and create an ObjectURL from it and set it as the src of an image element in the page



// Retrieve the file that was just stored transaction.objectStore("elephants").get("image").onsuccess = function (event) { var imgFile = event.target.result; console.log("Got elephant!" + imgFile); // Get window.URL object var URL = window.URL || window.webkitURL; // Create and revoke ObjectURL var imgURL = URL.createObjectURL(imgFile); // Set img src to ObjectURL var imgElephant = document.getElementById("elephant"); imgElephant.setAttribute("src", imgURL); // Revoking ObjectURL URL.revokeObjectURL(imgURL); };

Use the same transaction to get the image file you just stored, and then create an objectURL and set it to the `src`

of an image in the page.

This could just as well, for instance, have been a JavaScript file that you attached to a `script`

element, and then it would parse the JavaScript.

## The complete code

So, here’s is the complete working code:



(function () { // IndexedDB var indexedDB = window.indexedDB || window.webkitIndexedDB || window.mozIndexedDB || window.OIndexedDB || window.msIndexedDB, IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || window.OIDBTransaction || window.msIDBTransaction, dbVersion = 1.0; // Create/open database var request = indexedDB.open("elephantFiles", dbVersion), db, createObjectStore = function (dataBase) { // Create an objectStore console.log("Creating objectStore") dataBase.createObjectStore("elephants"); }, getImageFile = function () { // Create XHR and BlobBuilder var xhr = new XMLHttpRequest(), blob; xhr.open("GET", "elephant.png", true); // Set the responseType to blob xhr.responseType = "blob"; xhr.addEventListener("load", function () { if (xhr.status === 200) { console.log("Image retrieved"); // Blob as response blob = xhr.response; // Put the received blob into IndexedDB putElephantInDb(blob); } }, false); // Send XHR xhr.send(); }, putElephantInDb = function (blob) { console.log("Putting elephants in IndexedDB"); // Open a transaction to the database var transaction = db.transaction(["elephants"], IDBTransaction.READ_WRITE); // Put the blob into the dabase transaction.objectStore("elephants").put(blob, "image"); // Retrieve the file that was just stored transaction.objectStore("elephants").get("image").onsuccess = function (event) { var imgFile = event.target.result; console.log("Got elephant!" + imgFile); // Get window.URL object var URL = window.URL || window.webkitURL; // Create and revoke ObjectURL var imgURL = URL.createObjectURL(imgFile); // Set img src to ObjectURL var imgElephant = document.getElementById("elephant"); imgElephant.setAttribute("src", imgURL); // Revoking ObjectURL URL.revokeObjectURL(imgURL); }; }; request.onerror = function (event) { console.log("Error creating/accessing IndexedDB database"); }; request.onsuccess = function (event) { console.log("Success creating/accessing IndexedDB database"); db = request.result; db.onerror = function (event) { console.log("Error creating/accessing IndexedDB database"); }; // Interim solution for Google Chrome to create an objectStore. Will be deprecated if (db.setVersion) { if (db.version != dbVersion) { var setVersion = db.setVersion(dbVersion); setVersion.onsuccess = function () { createObjectStore(db); getImageFile(); }; } else { getImageFile(); } } else { getImageFile(); } } // For future use. Currently only in latest Firefox versions request.onupgradeneeded = function (event) { createObjectStore(event.target.result); }; })();

## Web browser support

- IndexedDB
- Supported since long (a number of versions back) in Firefox and Google Chrome. Planned to be in IE10 and a future version of Opera. Unclear about Safari.
- onupgradeneeded
- Supported in latest Firefox. Planned to be in Google Chrome soon and hopefully IE10 and a future version of Opera. Unclear about Safari.
- Storing files in IndexedDB
- Supported in Firefox 11 and later. Planned to be supported in Google Chrome. Hopefully IE10 will support it. Unclear about Safari and Opera.
- XMLHttpRequest Level 2
- Supported in Firefox and Google Chrome since long, Safari 5+ and planned to be in IE10 and Opera 12.
- responseType “blob”
- Currently only supported in Firefox. Will soon be in Google Chrome and is planned to be in IE10 and Opera 12. Unclear about Safari.

## Demo and code

I’ve put together a [demo with IndexedDB and saving images and files in it ](http://robnyman.github.com/html5demos/indexeddb/) where you can see it all in action. Make sure to use any Developer Tool to Inspect Element on the image to see the value of its `src`

attribute. Also make sure to check the console.log messages to follow the actions.

The code for [storing files in IndexedDB](https://github.com/robnyman/robnyman.github.com/tree/master/html5demos/indexeddb) is also available on GitHub, so go play now!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 30 comments

FlorianFebruary 24th, 2012 at 02:25Robert NymanFebruary 24th, 2012 at 02:47Andrea GiammarchiFebruary 26th, 2012 at 13:54Robert NymanFebruary 26th, 2012 at 14:01Andrea DoimoFebruary 28th, 2012 at 08:20Robert NymanFebruary 28th, 2012 at 08:51abralMarch 6th, 2012 at 15:46Robert NymanMarch 7th, 2012 at 01:28RubenAugust 24th, 2012 at 08:46Odin Hørthe OmdalMarch 14th, 2012 at 07:24Robert NymanMarch 14th, 2012 at 07:31Víctor QuirozApril 24th, 2012 at 10:49Víctor QuirozApril 24th, 2012 at 10:59Robert NymanApril 24th, 2012 at 15:05Robert NymanApril 24th, 2012 at 15:02AnonymousMay 20th, 2012 at 14:40Robert NymanMay 22nd, 2012 at 02:13MitchellJuly 20th, 2012 at 00:51MitchellJuly 20th, 2012 at 02:41Robert NymanJuly 31st, 2012 at 09:15SamAugust 27th, 2012 at 23:27Robert NymanAugust 28th, 2012 at 01:49RubenSeptember 25th, 2012 at 03:37Robert NymanSeptember 25th, 2012 at 07:39RubenSeptember 25th, 2012 at 12:10Robert NymanSeptember 26th, 2012 at 02:00RubenSeptember 26th, 2012 at 11:45Robert NymanSeptember 26th, 2012 at 12:50TomMarch 17th, 2013 at 14:19Robert Nyman [Editor]March 18th, 2013 at 02:53