---
title: Building Firefox Hub Add-ons for Firefox for Android – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2014/07/building-firefox-hub-add-ons-for-firefox-for-android/
author: Margaret Leibovic
published: '2014-07-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Firefox Hub APIs allow add-ons to add new panels to the Firefox for Android home page, where users normally find their top sites, bookmarks and history. These APIs were introduced in Firefox 30, but there are more features and bug fixes in Firefox 31 and 32. You can already [find some of these add-ons on addons.mozilla.org](https://addons.mozilla.org/en-US/firefox/collections/leibovic/home-panels/), and there is some [boilerplate code on github](https://github.com/leibovic/hub-boilerplate) to help you get started.

## Overview

There are two main parts to building a Firefox Hub add-on: creating a home panel, and storing data to show in that panel. Home panels consist of different views, each of which displays data from a given dataset.

### Creating a new home panel

To create a home panel, first use the [Home.panels API](https://developer.mozilla.org/en-US/Add-ons/Firefox_for_Android/API/Home.jsm/panels) to register a panel. The register API takes a panel id and an options callback function as parameters. This options callback is called to dynamically generate an options object whenever a panel is installed or updated, which allows for dynamic locale changes.

```
function optionsCallback() {
return {
title: "My Panel",
views: [{
type: Home.panels.View.LIST,
dataset: "my.dataset@mydomain.org"
}]
};
}
Home.panels.register("my.panel@mydomain.org", optionsCallback);
```

You must always register any existing panels on startup, but the first time you want the panel to actually appear on the user’s home page (e.g. when your add-on is installed), you also need to explicitly install the panel.

`Home.panels.install("my.panel@mydomain.org");`

You can modify the options callback function to customize the way data is displayed in your panel. For example, you can choose to display your data in a grid or a list, customize the view that is displayed when no data is available, or choose to launch an intent when the user taps on one of the items.

### Storing data for the panel

To actually show something in your new home panel, use the [HomeProvider API](https://developer.mozilla.org/en-US/Add-ons/Firefox_for_Android/API/HomeProvider.jsm) to store data. This API allows you to asynchronously save and delete data, as well as register a callback to allow the browser to periodically sync your data for you.

The HomeProvider API gives you access to [HomeStorage](https://developer.mozilla.org/en-US/Add-ons/Firefox_for_Android/API/HomeProvider.jsm/HomeStorage) objects, which you can interact with to save and delete data from a given dataset. These methods are designed to be used with [Task.jsm](https://developer.mozilla.org/en-US/docs/Mozilla/JavaScript_code_modules/Task.jsm) to execute asynchronous transactions within a task.

```
let storage = HomeProvider.getStorage("my.dataset@mydomain.org");
Task.spawn(function() {
yield storage.save(items);
}).then(null, Cu.reportError);
```

In Firefox 31, we expanded the save API to support replacing existing data for you, which is convenient for periodically refreshing your dataset.

```
function refreshDataset() {
let items = fetchItems();
Task.spawn(function() {
yield storage.save(items, { replace: true });
}).then(null, Cu.reportError);
}
HomeProvider.addPeriodicSync("my.dataset@mydomain.org", 3600,
refreshDataset);
```

This code snippet will ensure that our dataset is refreshed once every 3600 seconds (1 hour).

## What’s new in Firefox 32 Beta

In addition to bug fixes, Firefox 32 also adds a few more features to the set of Firefox Hub APIs.

### Refresh handler

In addition to support for periodically updating data, we also added support for “pull to refresh”, which gives users the power to manually refresh panel data. To take advantage of this feature, you can add an onrefresh property to your view declaration.

```
function optionsCallback() {
return {
title: "My Panel",
views: [{
type: Home.panels.View.LIST,
dataset: "my.dataset@mydomain.org",
onrefresh: refreshDataset
}]
};
}
```

With this new line added, swiping down on your panel will trigger a refresh indicator and call the refreshDataset function. The refresh indicator will disappear after a save call is made for that dataset.

### Authentication view

We added support for an authentication view, to make it easier for your add-on to use data that requires authentication. This view includes space for text and an image, as well as a button that triggers an authentication flow. To use this feature, you can add an auth property to your panel declaration.

```
function optionsCallback() {
return {
title: "My Panel",
views: [{
type: Home.panels.View.LIST,
dataset: "my.dataset@mydomain.org"
}],
auth: {
authenticate: function authenticate() {
// … do some stuff to authenticate the user …
Home.panels.setAuthenticated("my.panel@mydomain.org", true);
},
messageText: "Please log in to see your data",
buttonText: "Log in"
}
};
}
```

By default, the authentication view will appear when your panel is first installed, and the authenticate function will be called when the user taps the button in the view. It is up to you to call setAuthenticated(true) when the user successfully completes an authentication flow, and you can also call setAuthenticated(false) when a user becomes unauthenticated. This authentication state will persist between app runs, so it is up to you to reset it if you need to.

## Future work

We have ideas about ways to expand these APIs, but please let us know if there is anything you would like to see! We’re also always looking for new contributors to Firefox for Android, and we’d love to help you [get started writing patches](https://wiki.mozilla.org/Mobile/Get_Involved).

## About
[
Margaret Leibovic ](http://margaretleibovic.com)

Margaret is a developer on the Firefox for Android team at Mozilla. She loves the web, open source, and helping people get involved with Mozilla. You can find her on IRC as margaret.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 4 comments

pdJuly 25th, 2014 at 03:02Robert Nyman [Editor]July 25th, 2014 at 10:38HuJuly 27th, 2014 at 02:15Margaret LeibovicJuly 28th, 2014 at 07:35