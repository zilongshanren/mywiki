---
title: Embedding an HTTP Web Server in Firefox OS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/02/embedding-an-http-web-server-in-firefox-os/
author: Justin D'Arcangelo
published: '2015-02-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Nearing the end of last year, Mozilla employees were gathered together for a week of collaboration and planning. During that week, a group was formed to envision what the future of [Firefox OS](https://developer.mozilla.org/en-US/Firefox_OS) might be surrounding a more P2P-focused Web. In particular, we’ve been looking at harnessing technologies to collectively enable *offline* P2P connections such as [Bluetooth](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API), [NFC](https://developer.mozilla.org/en-US/docs/Web/API/NFC_API) and [WiFi Direct](https://developer.mozilla.org/en-US/docs/Web/API/MozWifiP2pManager).

Since these technologies only provide a means to communicate between devices, it became immediately clear that we would also need a protocol for apps to send and receive data. I quickly realized that we already have a standard protocol for transmitting data in web apps that we could leverage – HTTP.

By utilizing HTTP, we would already have everything we’d need for apps to send and receive data on the client side, but we would still need a web server running in the browser to enable offline P2P communications. While this type of HTTP server functionality might be best suited as part of a standardized [WebAPI](https://developer.mozilla.org/en-US/docs/WebAPI) to be baked into Gecko, we actually already have everything we need in Firefox OS to implement this in JavaScript today!

### navigator.mozTCPSocket

[Packaged apps](https://developer.mozilla.org/en-US/Marketplace/Options/Packaged_apps) have access to both raw TCP and UDP network sockets, but since we’re dealing with HTTP, we only need to work with TCP sockets. Access to the [TCPSocket](https://developer.mozilla.org/en-US/docs/Web/API/TCPSocket) API is exposed through [navigator.mozTCPSocket](https://developer.mozilla.org/en-US/docs/Web/API/Navigator.mozTCPSocket) which is currently only exposed to “privileged” packaged apps with the [tcp-socket](https://developer.mozilla.org/en-US/Apps/Build/App_permissions#tcp-socket) permission:

```
"type": "privileged",
"permissions": {
"tcp-socket": {}
},
```

In order to respond to incoming HTTP requests, we need to create a new [TCPSocket](https://developer.mozilla.org/en-US/docs/Web/API/TCPSocket) that listens on a known port such as 8080:

```
var socket = navigator.mozTCPSocket.listen(8080);
```

When an incoming HTTP request is received, the `TCPSocket`

needs to handle the request through the `onconnect`

handler. The `onconnect`

handler will receive a `TCPSocket`

object used to service the request. The `TCPSocket`

you receive will then call its own `ondata`

handler each time additional HTTP request data is received:

```
socket.onconnect = function(connection) {
connection.ondata = function(evt) {
console.log(evt.data);
};
};
```

Typically, an HTTP request will result in a single calling of the `ondata`

handler. However, in cases where the HTTP request payload is very large, such as for file uploads, the `ondata`

handler will be triggered each time the buffer is filled, until the entire request payload is delivered.

In order to respond to the HTTP request, we must send data to the `TCPSocket`

we received from the `onconnect`

handler:

```
connection.ondata = function(evt) {
var response = 'HTTP/1.1 200 OK\r\n';
var body = 'Hello World!';
response += 'Content-Length: ' + body.length + '\r\n';
response += '\r\n';
response += body;
connection.send(response);
connection.close();
};
```

The above example sends a proper HTTP response with “Hello World!” in the body. Valid HTTP responses must contain a status line which consists of the HTTP version `HTTP/1.1`

, the response code `200`

and the response reason `OK`

terminated by a CR+LF `\r\n`

character sequence. Immediately following the status line are the HTTP headers, one per line, separated by a CR+LF character sequence. After the headers, an additional CR+LF character sequence is required to separate the headers from the body of the HTTP response.

### FxOS Web Server

Now, it is likely that we will want to go beyond simple static “Hello World!” responses to do things like parsing the URL path and extracting parameters from the HTTP request in order to respond with dynamic content. It just so happens that I’ve already implemented a basic-featured HTTP server library that you can include in your own Firefox OS apps!

[FxOS Web Server](https://github.com/justindarc/fxos-web-server) can parse all parts of the HTTP request for various content types including `application/x-www-form-urlencoded`

and `multipart/form-data`

. It can also gracefully handle large HTTP requests for file uploads and can send large binary responses for serving up content such as images and videos. You can either download the source code for FxOS Web Server on [GitHub](https://github.com/justindarc/fxos-web-server) to include in your projects manually or you can utilize [Bower](http://bower.io/) to fetch the latest version:

```
bower install justindarc/fxos-web-server --save
```

Once you have the source code downloaded, you’ll need to include `dist/fxos-web-server.js`

in your app using a `<script>`

tag or a module loader like RequireJS.

### Simple File Storage App

Next, I’m going to show you how to use [FxOS Web Server](https://github.com/justindarc/fxos-web-server) to build a simple Firefox OS app that lets you use your mobile device like a portable flash drive for storing and retrieving files. You can see the source code for the finished product on [GitHub](https://github.com/justindarc/WebDrive).

Before we get into the code, let’s set up our [app manifest](https://developer.mozilla.org/en-US/Apps/Build/Manifest) to get permission to access [DeviceStorage](https://developer.mozilla.org/en-US/docs/Web/API/DeviceStorage) and [TCPSocket](https://developer.mozilla.org/en-US/docs/Web/API/TCPSocket):

```
{
"version": "1.0.0",
"name": "WebDrive",
"description": "A Firefox OS app for storing files from a web browser",
"launch_path": "/index.html",
"icons": {
"128": "/icons/icon_128.png"
},
"type": "privileged",
"permissions": {
"device-storage:sdcard": { "access": "readwrite" },
"tcp-socket": {}
}
}
```

Our app won’t need much UI, just a listing of files in the “WebDrive” folder on the device, so our HTML will be pretty simple:

```
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>WebDrive</title>
<meta name="description" content="A Firefox OS app for storing files from a web browser">
<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1">
<script src="bower_components/fxos-web-server/dist/fxos-web-server.js"></script>
<script src="js/storage.js"></script>
<script src="js/app.js"></script>
</head>
<body>
<h1>WebDrive</h1>
<hr>
<h3>Files</h3>
<ul id="list"></ul>
</body>
</html>
```

As you can see, I’ve included fxos-web-server.js in addition to app.js. I’ve also included a [DeviceStorage](https://developer.mozilla.org/en-US/docs/Web/API/DeviceStorage) helper module called storage.js since enumerating files can get somewhat complex. This will help keep the focus on our code specific to the task at hand.

The first thing we’ll need to do is create new instances of the `HTTPServer`

and `Storage`

objects:

```
var httpServer = new HTTPServer(8080);
var storage = new Storage('sdcard');
```

This will initialize a new `HTTPServer`

on port 8080 and a new instance of our `Storage`

helper pointing to the device’s SD card. In order for our `HTTPServer`

instance to be useful, we must listen for and handle the “request” event. When an incoming HTTP request is received, the `HTTPServer`

will emit a “request” event that passes the parsed HTTP request as an `HTTPRequest`

object to the event handler.

The `HTTPRequest`

object contains various properties of an HTTP request including the HTTP method, path, headers, query parameters and form data. In addition to the request data, an `HTTPResponse`

object is also passed to the “request” event handler. The `HTTPResponse`

object allows us to send our response as a file or string and set the response headers:

```
httpServer.addEventListener('request', function(evt) {
var request = evt.request;
var response = evt.response;
// Handle request here...
});
```

When a user requests the root URL of our web server, we’ll want to present them with a listing of files stored in the “WebDrive” folder on the device along with a file input for uploading new files. For convenience, we’ll create two helper functions to generate the HTML string to send in our HTTP response. One will just generate the listing of files which we’ll reuse to display the files on the device locally and the other will generate the entire HTML document to send in the HTTP response:

```
function generateListing(callback) {
storage.list('WebDrive', function(directory) {
if (!directory || Object.keys(directory).length === 0) {
callback('<li>No files found</li>');
return;
}
var html = '';
for (var file in directory) {
html += `<li><a href="/${encodeURIComponent(file)}" target="_blank">${file}</a></li>`;
}
callback(html);
});
}
function generateHTML(callback) {
generateListing(function(listing) {
var html =
`<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>WebDrive</title>
</head>
<body>
<h1>WebDrive</h1>
<form method="POST" enctype="multipart/form-data">
<input type="file" name="file">
<button type="submit">Upload</button>
</form>
<hr>
<h3>Files</h3>
<ul>${listing}</ul>
</body>
</html>`;
callback(html);
});
}
```

You’ll notice that we’re using [ES6 Template Strings](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/template_strings) for generating our HTML. If you’re not familiar with [Template Strings](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/template_strings), they allow us to have multi-line strings that automatically include whitespace and new lines and we can do basic string interpolation that automatically inserts values inside the `${}`

syntax. This is especially useful for generating HTML because it allows us to span multiple lines so our template markup remains highly readable when embedded within JavaScript code.

Now that we have our helper functions, let’s send our HTML response in our “request” event handler:

```
httpServer.addEventListener('request', function(evt) {
var request = evt.request;
var response = evt.response;
generateHTML(function(html) {
response.send(html);
});
});
```

As of right now, our “request” event handler will always respond with an HTML page listing all the files in the device’s “WebDrive” folder. However, we must first start the `HTTPServer`

before we can receive any requests. We’ll do this once the DOM is ready and while we’re at it, let’s also render the file listing locally:

```
window.addEventListener('DOMContentLoaded', function(evt) {
generateListing(function(listing) {
list.innerHTML = listing;
});
httpServer.start();
});
```

We should also be sure to stop the `HTTPServer`

when the app is terminated, otherwise the network socket may never be freed:

```
window.addEventListener('beforeunload', function(evt) {
httpServer.stop();
});
```

At this point, our web server should be up and running! Go ahead and install the app on your device or simulator using [WebIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE). Once installed, launch the app and point your desktop browser to your device’s IP address at port 8080 (e.g.: http://10.0.1.12:8080).

You should see our index page load in your desktop browser, but the upload form still isn’t wired up and if you have any files in your “WebDrive” folder on your device, they cannot be downloaded yet. Let’s first wire up the file upload by first creating another helper function to save files received in an `HTTPRequest`

:

```
function saveFile(file, callback) {
var arrayBuffer = BinaryUtils.stringToArrayBuffer(file.value);
var blob = new Blob([arrayBuffer]);
storage.add(blob, 'WebDrive/' + file.metadata.filename, callback);
}
```

This function will first convert the file’s contents to an [ArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer) using the `BinaryUtils`

utility that comes with fxos-web-server.js. We then create a [Blob](https://developer.mozilla.org/en-US/docs/Web/API/Blob) that we pass to our `Storage`

helper to save it to the SD card in the “WebDrive” folder. Note that the filename can be extracted from the file’s `metadata`

object since it gets passed to the server using ‘multipart/form-data’ encoding.

Now that we have a helper for saving an uploaded file, let’s wire it up in our “request” event handler:

```
httpServer.addEventListener('request', function(evt) {
var request = evt.request;
var response = evt.response;
if (request.method === 'POST' && request.body.file) {
saveFile(request.body.file, function() {
generateHTML(function(html) {
response.send(html);
});
generateListing(function(html) {
list.innerHTML = html;
});
});
return;
}
generateHTML(function(html) {
response.send(html);
});
});
```

Now, anytime an HTTP `POST`

request is received that contains a “file” parameter in the request body, we will save the file to the “WebDrive” folder on the SD card and respond with an updated file listing index page. At the same time, we’ll also update the file listing on the local device to display the newly-added file.

The only remaining part of our app to wire up is the ability to download files. Once again, let’s update the “request” event handler to do this:

```
httpServer.addEventListener('request', function(evt) {
var request = evt.request;
var response = evt.response;
if (request.method === 'POST' && request.body.file) {
saveFile(request.body.file, function() {
generateHTML(function(html) {
response.send(html);
});
generateListing(function(html) {
list.innerHTML = html;
});
});
return;
}
var path = decodeURIComponent(request.path);
if (path !== '/') {
storage.get('WebDrive' + path, function(file) {
if (!file) {
response.send(null, 404);
return;
}
response.headers['Content-Type'] = file.type;
response.sendFile(file);
});
return;
}
generateHTML(function(html) {
response.send(html);
});
});
```

This time, our “request” event handler will check the requested path to see if a URL other than the root is being requested. If so, we assume that the user is requesting to download a file which we then proceed to get using our `Storage`

helper. If the file cannot be found, we return an HTTP 404 error. Otherwise, we set the “Content-Type” in the response header to the file’s MIME type and send the file with the `HTTPResponse`

object.

You can now re-install the app to your device or simulator using [WebIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE) and once again point your desktop browser to your device’s IP address at port 8080. Now, you should be able to upload *and* download files from your device using your desktop browser!

The possible use cases enabled by embedding a web server into Firefox OS apps are nearly limitless. Not only can you serve up web content from your device to a desktop browser, as we just did here, but you can also serve up content from one device to another. That also means that you can use HTTP to send and receive data between apps on the *same* device! Since its inception, [FxOS Web Server](https://github.com/justindarc/fxos-web-server) has been used as a foundation for several exciting experiments at Mozilla:

-
[Guillaume Marty](https://twitter.com/g_marty/)has combined FxOS Web Server with his amazing[jsSMS](http://gmarty.github.io/jsSMS/)Master System/Game Gear emulator to enable multi-player gaming across two devices in conjunction with[WiFi Direct](https://developer.mozilla.org/en-US/docs/Web/API/MozWifiP2pManager). -
Several members of the

[Gaia](https://developer.mozilla.org/en-US/Firefox_OS/Platform/Gaia)team have used FxOS Web Server and[dns-sd.js](https://github.com/justindarc/dns-sd.js)to create an app that allows users to discover and share apps with friends over WiFi. -
I have personally used FxOS Web Server to build an app that lets you share files with nearby users without an Internet connection using

[WiFi Direct](https://developer.mozilla.org/en-US/docs/Web/API/MozWifiP2pManager). You can see the app in action here:

I look forward to seeing all the exciting things that are built next with FxOS Web Server!

## About
[
Justin D'Arcangelo ](https://github.com/justindarc)

Software engineer at Mozilla creating cutting-edge mobile web apps. Proud father, husband, musician, vinyl record aficionado and all-around tinkerer.

## 14 comments

Tom4hawkFebruary 9th, 2015 at 16:33Havi Hoffman [Editor]February 10th, 2015 at 12:26Tom4hawkFebruary 11th, 2015 at 07:32Justin D’ArcangeloFebruary 11th, 2015 at 09:48Tom4hawkFebruary 11th, 2015 at 13:47Doug ReederFebruary 9th, 2015 at 20:33Justin D’ArcangeloFebruary 10th, 2015 at 08:20Doug ReederFebruary 10th, 2015 at 09:20Doug ReederFebruary 25th, 2015 at 15:44Steven MaleFebruary 10th, 2015 at 00:26voracityFebruary 10th, 2015 at 20:52Justin D’ArcangeloFebruary 11th, 2015 at 08:33niutechFebruary 11th, 2015 at 13:37EricaFebruary 13th, 2015 at 15:44