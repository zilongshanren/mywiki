---
title: How to make a browser app for Firefox OS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/03/how-to-make-a-browser-app-for-firefox-os/
author: Luca Greco
published: '2015-03-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Firefox OS](https://developer.mozilla.org/en-US/Firefox_OS) is an operating system built on top of the Firefox web browser engine, which is called [Gecko](https://developer.mozilla.org/en-US/docs/Mozilla/Gecko). A browser app on Firefox OS provides a user interface written with [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5) technology and manages web page browsing using the [Browser API](https://developer.mozilla.org/en-US/docs/Web/API/Using_the_Browser_API). It also manages tabbing, browsing history, bookmarks, and so on depending on the implementation.

While Firefox OS already includes a browser, you can use the browser API to create your own browser or add browser functionality to your app. This article shows you how to build a browser app for Firefox OS devices. Following the steps, you’ll get a basic Firefox OS browser app with an address bar and back/forward buttons to browse web pages.

The source code can be downloaded at [https://github.com/begeeben/firefox-os-browser-sample](https://github.com/begeeben/firefox-os-browser-sample).

## Prerequisites: WebIDE

The [WebIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE) is available with Firefox 34 or later. A Firefox OS device is not required to develop, build or test a browser app. By using the WebIDE, we can easily bootstrap a web app, make HTML/CSS/JS modifications and run the app on one of the Firefox OS simulators. To open the WebIDE within Firefox, select **Tools > Web Developer > WebIDE** from the top menu:

## Create an app from the template

First, bootstrap a web app using the WebIDE empty template. The app type needs to be privileged so the `browser`

permission can be set. This permission is required in order to use the [Browser API](https://developer.mozilla.org/en-US/docs/Web/API/Using_the_Browser_API). The [Browser API](https://developer.mozilla.org/en-US/docs/Web/API/Using_the_Browser_API) provides additional methods and events to manage iframes.

Below is a screenshot of what the app should look like. Next we’ll start to add code to make a simple browser app.

## Edit the manifest.webapp

Let’s start to make some code changes. The template has already set the app type to `privileged`

in the manifest.webapp.

```
"type": "privileged",
```

To allow our app to use the Browser API, we need to specify the ‘`browser`

‘ permission.

```
"permissions": {
"browser": {}
},
```

## HTML structure

The browser app we’re building will have a toolbar on top and a div as the iframe container which displays ‘Hello myBrowser!’ by default. The browser iframe will be created later using JavaScript. We could have added the iframe to the HTML, but in this example a new browser iframe will be created dynamically.

```
```# Hello myBrowser!


Below is a screenshot of the simple browser app:

## Manage the browser iframe

The browser app has to handle `mozbrowser`

events which are accessible when the app has the `browser`

permission. In order to separate the UI and `mozbrowser`

event handling and preserve the flexibility of supporting multiple tabs in the future, we have added a tab.js file. Following is the code in tab.js which creates an iframe with the ‘`mozbrowser`

‘ attribute to enable the use of the [Browser API](https://developer.mozilla.org/en-US/docs/Web/API/Using_the_Browser_API).

```
/**
* Returns an iframe which runs in a child process with Browser API enabled
* and fullscreen is allowed
*
* @param {String} [url] Optional URL
* @return {iframe} An OOP mozbrowser iframe
*/
function createIFrame (url) {
var iframe = document.createElement('iframe');
iframe.setAttribute('mozbrowser', true);
iframe.setAttribute('mozallowfullscreen', true);
iframe.setAttribute('remote', true);
if (url) {
iframe.src = url;
}
return iframe;
}
```

The `mozallowfullscreen`

attribute enables the embedded web page of the iframe to use fullscreen mode. A web page can request fullscreen mode by calling `Element.mozRequestFullscreen()`

.

The ‘`remote`

‘ attribute separates the embedded iframe into another child process. This is needed for security reasons to prevent malicious web sites from compromising the browser app. Currently, the attribute does nothing in this sample browser app because Nested OOP has not been implemented. See [ Bug 1020135](https://bugzilla.mozilla.org/show_bug.cgi?id=1020135) – (nested-oop) [meta] Allow nested oop <iframe mozbrowser>.

Next the ‘`Tab`

‘ object constructor is added to tab.js. This constructor handles browser iframe creation and browser event handling. When a Tab is constructed, it creates a browser iframe and attaches the `mozbrowser`

event listeners to it:

```
/**
* The browser tab constructor.
*
* Creates an iframe and attaches mozbrowser events for web browsing.
*
* Implements EventListener Interface.
*
* @param {String} url An optional plaintext URL
*/
function Tab (url) {
this.iframe = createIFrame(url);
this.title = null;
this.url = url;
this.iframe.addEventListener('mozbrowserloadstart', this);
this.iframe.addEventListener('mozbrowserlocationchange', this);
this.iframe.addEventListener('mozbrowsertitlechange', this);
this.iframe.addEventListener('mozbrowserloadend', this);
this.iframe.addEventListener('mozbrowsererror', this);
};
```

There are additional `mozbrowser`

events that are not used in this simple browser app. The events used in the sample provide access to useful information about the iframe, and our browser app uses them to provide web page details, like the title, URL, loading progress, contextmenu, etc.

For example, to display the page title on the toolbar, we use the `mozbrowsertitlechange`

event to retrieve the title of the web page. Once the title is updated, a `CustomEvent`

`'tab:titlechange'`

with the Tab itself as the detail is dispatched to notify other components to update the title.

```
Tab.prototype.mozbrowsertitlechange = function _mozbrowsertitlechange (e) {
if (e.detail) {
this.title = e.detail;
}
var event = new CustomEvent('tab:titlechange', { detail: this });
window.dispatchEvent(event);
};
```

Code can now be added to the main app.js to handle this custom event, which updates the title.

```
/**
* Display the title of the currentTab on titlechange event.
*/
window.addEventListener('tab:titlechange', function (e) {
if (currentTab === e.detail) {
urlInput.value = currentTab.title;
}
});
```

## Browse a web page on submit event

Using the address bar as a search bar is a common and useful practice among browsers. When a user submits the input, first we check if it is a valid URL. If not, the input is regarded as a search term and it will be appended to a search engine URI. Note that the validation of the URL can be handled in multiple ways. The sample app uses an input element with its type attribute set to URL. A [URL](https://developer.mozilla.org/en-US/docs/Web/API/URL/URL) object could also have been used with the URL string passed as the first parameter to the constructor. A DOM exception will be thrown if the URL is not valid. This exception can then be caught and the URL string assumed to be a search term.

```
/**
* The default search engine URI
*
* @type {String}
*/
var searchEngineUri = 'https://search.yahoo.com/search?p={searchTerms}';
/**
* Using an input element to check the validity of the input URL. If the input
* is not valid, returns a search URL.
*
* @param {String} input A plaintext URL or search terms
* @param {String} searchEngineUri The search engine to be used
* @return {String} A valid URL
*/
function getUrlFromInput(input, searchEngineUri) {
var urlValidate = document.createElement('input');
urlValidate.setAttribute('type', 'url');
urlValidate.setAttribute('value', input);
if (!urlValidate.validity.valid) {
var uri = searchEngineUri.replace('{searchTerms}', input);
return uri;
}
return input;
}
```

Code can then be added to the main app.js to handle the submit button. This code checks to see if a currently active `Tab`

object exists, and either loads the URL or reloads the URL if it has not changed. If one does not exist, it is created and the URL is loaded.

```
/**
* Check the input and browse the address with a Tab object on url submit.
*/
window.addEventListener('submit', function (e) {
e.preventDefault();
if (!currentUrlInput.trim()) {
return;
}
if (frameContainer.classList.contains('empty')) {
frameContainer.classList.remove('empty');
}
var url = getUrlFromInput(currentUrlInput.trim(), searchEngineUri);
if (!currentTab) {
currentTab = new Tab(url);
frameContainer.appendChild(currentTab.iframe);
} else if (currentUrlInput === currentTab.title) {
currentTab.reload();
} else {
currentTab.goToUrl(url);
}
});
```

The `currentTab.reload`

function uses the `iframe.reload`

function provided by the `Browser API`

to reload the page. The code below is added to the tab.js file to handle the reload.

```
/**
* Reload the current page.
*/
Tab.prototype.reload = function _reload () {
this.iframe.reload();
};
```

## Enable/disable back and forward buttons

Finally the [Browser API](https://developer.mozilla.org/en-US/docs/Web/API/Using_the_Browser_API) can be used to check if the page can go backward or forward in the navigation history. The `iframe.getCanGoBack`

method returns a `DOMRequest`

object which indicates if the page can go backward in its `onsuccess`

callback. We use a `Promise`

to wrap this function for easier access. This code is added to the tab.js file.

```
/**
* Check if the iframe can go backward in the navigation history.
*
* @return {Promise} Resolve with true if it can go backward.
*/
Tab.prototype.getCanGoBack = function _getCanGoBack () {
var self = this;
return new Promise(function (resolve, reject) {
var request = self.iframe.getCanGoBack();
request.onsuccess = function () {
if (this.result) {
resolve(true);
} else {
resolve(false);
}
};
});
};
```

The check is performed in the app.js file when a page is loaded. This occurs when the iframe receives a `mozbrowserloadend`

event.

```
/**
* Enable/disable goback and goforward buttons accordingly when the
* currentTab is loaded.
*/
window.addEventListener('tab:loadend', function (e) {
if (currentTab === e.detail) {
currentTab.getCanGoBack().then(function(canGoBack) {
gobackButton.disabled = !canGoBack;
});
currentTab.getCanGoForward().then(function(canGoForward) {
goforwardButton.disabled = !canGoForward;
});
}
});
```

## Run the app

One of the Firefox OS simulators can now be used to test the sample browser app.

On the top right of the WebIDE, click **Select Runtime** to choose a Firefox OS phone or simulator:

Once a Firefox OS runtime is selected and launched, you can install and run the app by clicking the play button within the WebIDE. See the [WebIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE) documentation for more information on building, debugging, and deploying Firefox OS apps.

## Final thoughts

There’s more functionality that can be added to this simple little browser to make it really useful including bookmarks, settings, search suggestions, and sharing. Feel free to expand on this code and have fun with it. Let us know what you think and be sure to spread the word about Firefox OS!

## Additional information

[https://hacks.mozilla.org/2014/08/building-the-firefox-browser-for-firefox-os/](https://hacks.mozilla.org/2014/08/building-the-firefox-browser-for-firefox-os/)

[https://developer.mozilla.org/en-US/docs/Web/API/Using_the_Browser_API](https://developer.mozilla.org/en-US/docs/Web/API/Using_the_Browser_API)

## 2 comments

Brett ZamirMarch 20th, 2015 at 21:26voracityMarch 21st, 2015 at 18:21