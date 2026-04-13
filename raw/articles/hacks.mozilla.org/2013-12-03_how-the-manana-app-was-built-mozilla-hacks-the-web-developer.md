---
title: How the Manana app was built – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/12/how-the-manana-app-was-built/
author: Alberto Granzotto
published: '2013-12-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We saw Firefox OS as a great opportunity and a challenge to deliver a product true to the values of open web and best standards. We found it exciting to be able to deliver an app that will offer a smooth UX even for people using lower end devices. As many of the users have a very limited data plan we decided that a proper reading app offering the possibility to enjoy their favourite articles offline and without unnecessary distractions would be a key product. And so we decided to build Manana.

Here is the story of how we did it.

![](../../assets/f21d54d81d5b6cb2.png)


On a technological side, we decided to go vanilla but with a little help from [ZeptoJS](http://zeptojs.com/) to handle the DOM manipulation. We also integrated Web Activities to hook into the sharing options in the browser, and to share the selected links via email. We are using also the Readability API to have a nice formatted version of the link. The app is simple and that’s how we wanted it to be. but we have a great plus: it is internationalized in English, Spanish, Portuguese, Polish, German, Italian. Hungarian and Greek are coming soon.

You can [install Manana from the Firefox Marketplace](https://marketplace.firefox.com/app/manana).

## Building the layout and managing transitions between the views

To provide a branded UI/UX, we use a small framework built in-house. With some clever CSS properties and a few lines of JavaScript (to handle the visibility of the Views) the whole thing was quite easy to set up. Basically, we have each View arranged like cards in a deck. Every time we need one of them, we pull it out while the old one goes in the deck again (becoming hidden). When the animation is ended, we capture the `animationend`

event, so right after that we remove the class that brings the animation properties and at the same time we add a `current`

class, which lets the card stay in place and be visible. The old one is hidden automatically since that’s its default state.

![](../../assets/f589b3861db6f8c1.png)


Below you will find a small example of how it works with a `moveRight`

animation.

## Optimize CSS3 transitions

Every smartphone comes with at least a small GPU, so that the CPU doesn’t have to do all the graphical calculations. It’s very much in fashion to take advantage of the Hardware Acceleration and so we do. There are some CSS3 properties that are automatically handled by the GPU, but others are not – usually the ones that are related to 3D. This is because the element (tied to the animated property) is *promoted* to a new layer that doesn’t suffer from repaints imposed by other properties (like `left`

, for example. But this can change in the future).

**tl;dr** Where you can, avoid expensive CPU work, especially on big or complicated elements. Here is a small extract of how we implemented such properties.

```
/* moveLeftIn directive */
.moveLeftIn {
animation: 0.5s moveLeftIn cubic-bezier(…) forwards; /* 1 */
backface-visibility: hidden; /* 2 */
transform: translateY(0) translateX(99%); /* 3 */
/* 1. `forwards` let the animation stop at the last keyframe */
/* 2. avoid some possible glitches caused by 3D rendering */
/* 3. take advantage of the GPU with 3D-related properties */
}
/* moveLeftIn animation */
@keyframes moveLeftIn {
0% { transform: translateY(0) translateX(99%); z-index: 999; }
100% { transform: translateY(0) translateX(0); z-index: 999; }
}
```

## Hooking to the Firefox OS specific Web Activities

One of our favourite APIs of the WebAPIs, is [Web Activities](https://developer.mozilla.org/en-US/docs/WebAPI/Web_Activities). An application emits an Activity (for example, *save bookmark*) then the user is prompted to chose among other applications that handles that activity. At the moment it is possible to register an application as an activity handler through the app manifest (*declaration registration*), but in the future this could be done inside the app itself (*dynamic registration*).

![](../../assets/28b8ad2d4166a499.png)


Saving a link from the browser to Manana is an example of Web Activity (*save-bookmark*). Registering an activity is trivial:

### manifest.webapp

```
"activities": {
"save-bookmark": {
"disposition": "inline",
"index.html#/savebookmark",
"returnValue": true
}
},
```

**returnValue** is of great importance, otherwise the handler application (Manana in our case) will never return to the caller (Browser). The handling in the app is also very easy:

```
navigator.mozSetMessageHandler("activity", function(activity) {
... check if activity is savebookmark
var data = activity.source.data;
... do stuff with activity data
activity.postResult("saved");
});
```

![](../../assets/c1595ae031840927.png)


The applications included in your phone are part of [Gaia](https://github.com/mozilla-b2g/gaia), the UI of Firefox OS, and you can actually browse the source. They provide a lot of examples on how to use WebAPIs. If you are interested in the **save-bookmark** activity, have a look at the [Homescreen app source code](https://github.com/mozilla-b2g/gaia/tree/master/apps/homescreen).

Manana users can also share their resources via email, directly from the app. To achieve that, we’ve implemented the `email`

Web Activity. It’s easy to pre-populate the email subject and body, just follow the `mailto`

URI scheme and you are done.

```
DB.Get(id, function (rs) {
var subject = rs.title,
body = rs.url,
shareActivity = new MozActivity({
name: "new",
data: {
type: "mail",
url : "mailto:?body=" + encodeURIComponent(body) +
"&subject=" + encodeURIComponent(subject)
}
});
});
```

## Retrieving and storing data with IndexedDB

IndexedDB is a client side NoSQL DB. It has some nice features which make it easier working with app updates and is easy to integrate in your app, even if you’re using a framework like AngularJS. Setting up models is fairly easy and extensively documented on the web and in Gaia Apps.

You don’t have a quota limit, although the Firefox OS Simulator seems to have a limit when dealing with datasets larger than 5mb. Each database is tied to an app and a version. Only one version can run at a time, which makes it easier not to break compatibility, especially if you rely on some external API.

Since it is asynchronous, dealing with IndexedDB operations requires having callback. Below is an example on how we deal with the action of adding a link:

- Call Link.Add function, passing a link object and a success callback
- Link.Add get a DB connection by calling getDB
- In the case a DB does not exist, the
**onupgradeneeded**callback is executed- Create DB
- Create collections
- Create indexes

- getDB check if the connection is already open, otherwise it opens a new one

- In the case a DB does not exist, the
- Link.Add fills the missing property of links with default values
- We call the objectStore
**put**method to save/update new data into the collection- If the Link object we are going to save already contains a primary key attribute, IndexedDB does an update
- Otherwise, an insert

- If the
**put**method is successful it calls a success callback, returning the primary key in**event.target.result**

Below is an example of DB action defined in our models: (for the sake of brevity we omitted error checking code)

```
Add: function(data, onsuccess) {
getDB(function(db) {
var transaction = db.transaction(["links"], "readwrite"),
objectStore = transaction.objectStore("links"),
request = objectStore.put(data);
request.onsucces = function(e) {
onsuccess(e.target.result) // e.target.result is the id of the new Link
}
});
},
```

This is how you call it from the other part of the app:

```
var newLink = {url: "http://zombo.com",
title: "Welcome to zombo com"};
Link.Add(newLink, function(linkId) {
window.location.hash = "#/read/:" + linkId;
});
```

## Enhance localization with Markdown support

Localization is a key feature in our app. Manana currently supports 6 languages (soon it will be 8). There is no official recommendation, but after some research we decided to use the same [technique](https://hacks.mozilla.org/2013/08/localizing-firefox-os-apps/) that Gaia is using. This is a great *feature* of working with Firefox OS: the whole source code is there, and you can get inspiration by reading it.

L10n has been used in two different cases: to translate the `text`

content of DOM elements and to translate internal help pages. To make the Localization process as simple as possible, we avoided putting HTML tags in the strings and in the internal help pages; we used markdown instead. By design, we avoided having strings in the Javascript code, all messages and alerts are contained in the HTML.

To support markdown we added some glue between the l10n.js library and [marked.js](https://github.com/chjj/marked).

To load the help resources, Manana first does a lookup in the current installation to find the file named `<resourceName>.<locale>.md`

. If the lookup fails, the fallback is the English version of the resource. Once the file is retrieved succesfully, the content is applied to the `marked`

function to generate the HTML, and then added to the DOM.

```
function resourceInit($oldView, $newView, resource) {
var fallback = "/locales/resources/" + resource + ".en.md",
localized = "/locales/resources/" + resource + "." + getLanguage() + ".md",
renderMd = function (txt) {
$(".js-subpage", $newView).html(marked(txt));
},
renderError = function (txt) {
$(".js-subpage", $newView).text("ouch, cannot find: " + resource);
};
getFile(localized,
renderMd,
function () { getFile(fallback, renderMd, renderError); });
}
```

## A note on retrieving local files with a XMLHttpRequest

Retrieving files asynchronously from your local app is as easy as doing a `XMLHttpRequest`

, but there is a case that took us some time to sort out. If the local file you are retrieving is missing, the request won’t fire the `success`

callback (of course), but neither the `error`

callback. It will just hang there forever.

After some research, we noticed a `try { ... } catch`

block in the `l10n.js`

library. Basically, “in Firefox OS with the `app://`

protocol, trying to XHR a non-existing URL will raise an exception.”

```
function getFile (url, success, error) {
var xhr = new XMLHttpRequest();
xhr.open("get", url, true);
xhr.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
xhr.onreadystatechange = function() {
if (xhr.readyState == 4) {
if (xhr.status == 200 || xhr.status === 0)
success(xhr.responseText);
else
error && error();
}
};
xhr.onerror = error;
xhr.ontimeout = error;
// Here it is!
try {
xhr.send(null);
} catch (e) {
error && error();
}
}
```

## Keeping the UI synchronized with the Database

One of the most challenging aspect of an HTML app is synchronization of state between a data source (db, file, api, etc) and the UI. Frameworks like Backbone and Angular make your life easier but they are not easy beasts to tame. Going vanilla is fun, mostly because JavaScript gives you a lot of flexibility when deciding how to do things.

We really like OO programming by message passing, so we came up with a message based architecture. The `body`

element acts as our global dispatcher while view root element is the local dispatcher. Global events get registered when the application starts and live as long as the app. Local events get registered when entering a view and live until we leave that view.

An example of global events are the CRUD operations we want to perform on our model.

Each action on the UI which changes the state of models is tied to a global event, registered on `document.body`

. On entering a new view, we call a constructor function, which executes some initialization code.

```
var events = {
// global events are never unbinded
global: {
"save-link": function() { ... },
"remove-link": function() { ... },
...
"update-link-collecetion": function { ... },
...
},
// view specific events are unbinded everytime we leave that view
home: {
"update-link-collection-complete": function(e) {
var $caller = e.detail.$caller;
...
}
},
...
}
function homeInit($oldView, $newView, dispatch) {
// $oldView is the previous view
// $newView is the current view
// dispatch in an helper which wrap
// document.body.dispatchEvent(new CustomEvent(...))
dispatch("update-link-collection")
}
```

Leaving a view calls a destructor on that view, and unbinds all the local events. At the end of the day we can open the app source code without spending hours trying to figure out how things work because of framework related black magic.

## Integration with git

When it comes to Git, our hearts melt. We love git. Seriously. Git and Vim are the best pieces of software ever written. Love.

Ok, lets get serious again.

Our application is composed from two components, the app itself and an API Server. The API server is a Golang API proxy to Readability API. So our app directory layout looks like this:

manana/ |- distrib.sh |- srv/ |- app/

**distrib.sh** is a simple bash script which perform three simple tasks:

- Install a post-{commit, merge, rebase} hook, if not already installed
- Update
**app/js/revision.js**writing the current git revision hash. - Create a clean zip containing the app, ready for the app store or your device.

This makes our lives easier.

## Conclusion. What Next?

Manana relies on the Readability API to get the stripped down version of the web page. Readability is doing a really good job, but we’d like to experiment with other solutions, like parsing the page directly in the device. It’s a hard job, but it’d be cool to do it on the client side, and some work has already [been done](http://code.google.com/p/arc90labs-readability/source/browse/trunk/js/readability.js).

We had a great time developing for Firefox OS. The most important thing for us, techwise, is that we developed a webapp, not an **OS-specific app**. We can use all the know-how we gained in the past years, all the great open source libraries we want, and we can even use the browser debug tools we use every day.

To help newcomers in building a Firefox OS app, we have created [a list of resources](http://tmp.devcharm.com/pages/10-resources-you-need-to-develop-a-FirefoxOS-app) we found indispensable.

## About Alberto Granzotto

Full stack developer. Open standards fanboy.

## About
[
Andrea Di Persio ](http://andreadipersio.com)

Backend Developer. He loves writing stuff in golang and python using vim and noisy mechanical keyboards.

## About Riccardo Buzzotta

He is an Art and HTML+CSS lover. Also Digital/Analog Artist/Designer wannabe.

## About Mateusz Fafinski

Copywriter and content creator. Writes stuff and about stuff. Responsible for content curation and localization.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 8 comments

Abhishek ShuklaDecember 3rd, 2013 at 03:31Mateusz FafinskiDecember 3rd, 2013 at 09:48Andre JaenischDecember 5th, 2013 at 01:42Andrea Di PersioDecember 6th, 2013 at 05:21Andre JaenischDecember 9th, 2013 at 13:36Andrea Di PersioDecember 16th, 2013 at 04:47JulienWDecember 5th, 2013 at 04:35Alberto GranzottoDecember 5th, 2013 at 10:25