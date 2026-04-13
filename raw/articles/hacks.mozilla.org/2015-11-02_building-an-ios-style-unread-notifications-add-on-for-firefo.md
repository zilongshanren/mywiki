---
title: Building an iOS-style “Unread Notifications” add-on for Firefox OS – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/11/building-an-ios-style-unread-notifications-add-on-for-firefox-os/
author: Shing Lyu
published: '2015-11-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

# What is a Firefox OS add-on and why do we need it?

The Firefox [add-on ecosystem](https://addons.mozilla.org/en-US/firefox/) has been a key differentiator in the desktop browser arena. However, the mobile space lacks a strong add-on framework. Some solutions exist for Android, such as [Xposed](http://repo.xposed.info/), but these solutions typically require a rooted phone, and the content is usually not reviewed by a well-trusted party, making it challenging for the average person to use. Also, it requires a deep knowledge of the Android platform, making it hard for web developers to get involved.

In version 2.5 of Firefox OS, Mozilla introduces [a new add-ons model](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Add-ons). These new add-ons leverage the [WebExtensions API](https://wiki.mozilla.org/WebExtensions), which is what Chrome Extensions are built upon. Since Firefox OS is built using standard HTML5 technologies, web developers can easily jump in.

One of the most useful features of Firefox OS add-ons is the [ "content_scripts" API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/content_scripts). It is used to inject custom JavaScript and CSS into selected apps. The injected script will be executed when the app starts (or when the add-on is first enabled), so we can immediately change the behavior of apps or of the system itself!

In this post, we’ll show you how to develop iOS-style “unread message” notifications using the new Firefox OS add-on framework.

# High-level architecture of the unread icon add-on

Our add-on will display the unread message counts for app icons on the homescreen (see screenshot below). The add-on needs to be able to retrieve unread notifications from the system, store them in persistent storage (so we can retrieve the correct number even after a system reboot), and display them accurately alongside the homescreen app icons.

**Note**: You can find all the [Unread Icon code](https://github.com/shinglyu/fxos-unread-icon) on GitHub. The code snippets below are simplified for readability, so copy-and-paste from the example code in this article will not work.

Luckily, we don’t need to hack into each app and write custom logic to retrieve the unread message counts. Instead, we can watch for built-in notifications from Firefox OS. Most of the core apps like Phone, SMS, E-Mail, and Calendar use this notification system when new unread messages come in. We can analyze the content of those notifications to detect when an app receives a new unread message.

Now, it might be tempting to inject JavaScript directly into the Homescreen app so that the add-on can listen for system notifications and add little red numbers onto the app icons at the same time. Keep in mind that the injected JavaScript code will have the same permissions as the app it injects into, and the Homescreen app doesn’t have permission to access notifications from the other apps. So instead, we need to inject JavaScript into the System app, since it can access all the other apps’ notifications.

So far, so good. However, the System app doesn’t have access to the DOM of the Homescreen, so we also need to inject JavaScript into the Homescreen app in order to add the unread numbers onto the app icons.

For the System app to communicate unread message counts to the Homescreen app, we use the [Settings API](https://developer.mozilla.org/en-US/docs/Web/API/Settings_API). Since Settings is a key-value store, we can let the System app write json data into it, and then the Homescreen can read this data and update the UI accordingly.

# Add-on folder structure

A Firefox OS add-on looks like a hybrid of a [WebExtensions-based add-on](https://developer.mozilla.org/en-US/Add-ons/WebExtensions) and an [open web app](https://developer.mozilla.org/en-US/Apps/Build/Building_apps_for_Firefox_OS). The folder will usually looks like this:

```
.
├── icons
│ ├── icon-128.png
├── main.js
└── manifest.json
```


First, let’s look at `manifest.json`

, which is the [WebExtension manifest](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json). In `manifest.json`

we explicitly specify the JavaScript and CSS files to be injected, and we specify which apps and/or webpages we will inject them into. We do this by using the `content_script`

field:

```
{
"content_scripts": [{
"matches": [ // which app we want to inject
"app://system.gaiamobile.org/index.html",
"app://verticalhome.gaiamobile.org/index.html*"
],
"js": ["main.js"] // the JavaScript we want to inject
"css": [],
}],
"name": "Unread Icons",
"description": "Add unread count on icons on the homescreen. Works on: Phone, Messages, Calendar, E-mail, Gallery, BzLite",
"author": "Shing Lyu",
"version": "1.0",
"icons": {
"128": "/icons/icon-128.png"
}
}
```


To simplify the add-on structure, we don’t inject separate JavaScript files into System and Homescreen. Instead, we inject a single JavaScript file (`main.js`

) that contains the code for both apps, and we check `window.location`

to determine which app we are currently in. More about this later.

# How to install an add-on through WebIDE and how to enable it in settings

Before we get into the JavaScript code, let’s take a short detour to install and enable the add-on.

Although you’ll probably want to install the final product through the [Firefox Marketplace](https://marketplace.firefox.com/content/), during development it’s easier to install your add-on through [WebIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE). Use the latest build of [Firefox Nightly](http://nightly.mozilla.org/) for desktop, otherwise WebIDE may not recognize the add-on package.

Start by opening up your Firefox Nightly and open **Tools > Web Developer > WebIDE**. Then use the “Open Packaged App” button to open your add-on (select the folder containing the add-on code, zipping is not required). Connect your Firefox OS phone or [Simulator](https://developer.mozilla.org/en-US/docs/Tools/Firefox_OS_Simulator) and press the install button.

Once the add-on is successfully installed, we need to enable it on the phone. Go to the Settings app, click the “Add-ons” section, and you should see our add-on at the end of the list.

Click on the title, **Unread Icons**, then toggle the switch to enable it.

It’s important to keep in mind that when the add-on is enabled, and the app you are injecting into is already running (e.g. System), the add-on code will run immediately. Otherwise, the add-on code will be injected only once the app is opened. Also note that when an add-on is disabled in Settings, the add-on code that is running will not be disabled automatically. This means that if you keep toggling an add-on, multiple copies of the code will be injected. It’s a very good idea to prevent this in your add-on code! See [Preventing multiple injections](https://developer.mozilla.org/en-US/Firefox_OS/Add-ons#Preventing_multiple_injections) on MDN for more information.

# How to collect unread messages in the System app

First, in order to collect the unread notifications in the System app, the JavaScript code has to know about unread messages in the System app:

```
if (window.location.toString() === 'app://system.gaiamobile.org/index.html') {
//Listen for system notification for new unread messages
}
```


Once we’re sure we’re in the System app, we add an event listener to watch for the `mozChromeNotificationEvent`

, the system event that is fired when a notification pops up. Here’s an example of the notification event:

```
mozChromeNotificationEvent {
target: Window,
detail: Object, //The meat is in here
timeStamp: 1445421387703168,
… //irrelevant details are omitted
}
```


Digging deeper into the `detail`

object reveals:

```
{
"id": "app://system.gaiamobile.org/manifest.webapp#tag:screenshot:1445421387658", //This is what we want
"appIcon": "app://system.gaiamobile.org/style/icons/system_126.png",
"appName": "System",
"data": {
"systemMessageTarget": "screenshot"
},
"manifestURL": "app://system.gaiamobile.org/manifest.webapp",
"text": "screenshots/2015-10-21-17-56-27.png",
"title": "Screenshot saved to Gallery",
… //irrelevant details are omitted
}
```


We can see that in `event.detail`

, the `id`

field is particularly interesting. It contains the app manifest URL, the event type (`screenshot`

) and some random UUID. We can easily build a whitelist that maps event detail ID patterns to apps.

Since each app may generate many kinds of notifications, we need to filter only for those which tell us about an unread message, and map them to the app icons. The mapping is required because sometimes the app generating the notification is not the app that has an unread message. For example, the System is responsible for generating a “screenshot taken” notification, but the unread notification number should be shown on the Gallery app.

After we receive a notification, we check if it represents a new unread message by looking up its event type in the lookup table described above. If the notification does represent an unread message for a particular app, we increment the unread count for that app. This can be done using the following code example:

```
window.addEventListener('mozChromeNotificationEvent', function(evt){
var iconUrl = notificationIdToIconUrl(evt.detail.id); // filtering and mapping is done here
if (typeof iconUrl != "undefined") {
increaseUnreadByOne(iconUrl); //We’ll get to this later
}
})
```


Inside the `increaseUnreadByOne()`

function we keep a count of the unread messages for each app using the following JavaScript object:

```
{
"unreads": {
"app://calendar.gaiamobile.org/manifest.webapp": 0,
"app://communications.gaiamobile.org/manifest.webapp-dialer": 0,
"app://gallery.gaiamobile.org/manifest.webapp": 0,
"app://sms.gaiamobile.org/manifest.webapp": 0,
...
}
}
```


In order for the Homescreen to access the unread counts, we need to write these values to Settings from the System app. Since many apps may want to access the settings simultaneously, we need to acquire a lock before we can read/write the data. This is how the `increaseUnreadByOne()`

function is implemented:

```
function increaseUnreadByOne(appUrl){
var unreads = {}
var lock = navigator.mozSettings.createLock();
var setting_get = lock.get('unreads');
setting_get.onsuccess = function () {
if (typeof setting_get.result.unreads === "undefined"){
unreads[appUrl] = 1
}
else {
unreads = setting_get.result.unreads;
if (appUrl in unreads){
unreads[appUrl] += 1;
}
else {
unreads[appUrl] = 1;
}
}
// Write the unread count to the Settings database.
var lock = navigator.mozSettings.createLock();
var setting_set = lock.set({ 'unreads': unreads });
}
setting_get.onerror = function () {
console.log("[UNREAD] An error occure, the settings remain unchanged");
}
}
```


# How to draw unread notifications onto the Homescreen app icons

Now that we have the unread message counts ready, we need to display them correctly on the Homescreen. As we mentioned above, the same copy of the add-on JavaScript code (`main.js`

) will be injected into both System app and Homescreen app. Therefore we must now check that we are in the Homescreen app, just as we did for the System app.

The following JavaScript code reads the unread counts from the settings database, and tries to draw those counts onto the app icons. The unread count icon is actually a

<div/>

node injected under the app icon DOM node, with a red background and a border-radius of 100% (which makes it a circle). The app icon DOM node can be located easily because it has a `data-identifier`

attribute which is (almost always) the app manifestURL. (One exception is the Dialer app, which has a strange `-dialer`

suffix, but for the sake of architectural simplicity we treat it as a special case and hard-code it.)

```
function drawUnreadIcon(appUrl, number){
var app_selector = '.icon[data-identifier="' + appUrl + '"]'; //for locating the app icon
var unreadIconElement = document.getElementById(app_selector+"-unread");
if (number === 0){
if (unreadIconElement){
unreadIconElement.parentNode.removeChild(unreadIconElement);
}
return
}
else{
if (number > 99) { number = "N" }
if (unreadIconElement){
unreadIconElement.textContent = number;
}
else {
unreadIconElement = document.createElement('div');
unreadIconElement.id = app_selector + "-unread";
unreadIconElement.style.backgroundColor = "red";
unreadIconElement.style.borderRadius = "100%";
//More unreadIconElement.style.foo = "bar" lines are omitted
unreadIconElement.appendChild(document.createTextNode(number));
document.querySelector(app_selector).appendChild(unreadIconElement);
}
}
}
```


Notice that we use `element.style.foo="bar"`

syntax to assign the CSS instead of injecting a separate CSS file. This began as a workaround for an earlier version of the add-on framework that didn’t work well when injecting CSS files. (You can check the status of this issue in [Bug 1179536](https://bugzilla.mozilla.org/show_bug.cgi?id=1179536).) Now, as CSS support becomes available, there’s no strong reason to change our approach. This add-on is quite simple, so we don’t bother to split our code into too many files. However, if you want to build a more complex add-on, you might consider splitting the CSS into a different file for clarity.

# How to update in real-time

We want our unread count to update in real-time, but we don’t want to poll the settings database because it does not provide timely information and it can drain the battery. Instead, we can subscribe to the settings’ update event, and so any time data in the settings database changes we can trigger a re-draw immediately.

```
window.navigator.mozSettings.addObserver('unreads', function(evt){
var settings = evt.settingValue;
for (appUrl in setting.result.unreads){
drawUnreadIcon(appUrl, setting.result.unreads[appUrl]);
}
})
```


## A side note about inter-app communication for add-ons

Since this add-on was built during a recent hackathon, we chose a quick and hacky way to build the inter-app communication channel using the system settings storage. There doesn’t seem to be a well-accepted pattern for inter-app communication for add-ons yet. But you may want to check out the following options (which are still experimental and not guaranteed to work):

# Debugging and testing

Although we can install the add-on through WebIDE, the JavaScript console and debugger are not ready yet for debugging add-ons. The only way to debug add-ons right now is to use `console.log()`

to print debug messages to `adb logcat`

output. You might want to prepend some prefix to the log output so you can easily filter the log output. Also, you’ll find yourself checking how the core apps work frequently (if you want to change the system behavior), and WebIDE will be handy in these situations. You can connect your real phone to WebIDE, then use “Runtime Info” > “request higher privileges” to access the system and built-in apps. (See [MDN](https://developer.mozilla.org/en-US/docs/Tools/WebIDE/Running_and_debugging_apps#Unrestricted_app_debugging_%28including_certified_apps_main_process_etc.%29) for more info.)

Once the phone reboots, you’ll be able to see the “Main Process” options and other core apps in the running app list:

You can use the DOM inspector to check the DOM elements you want to tweak:

And use the JavaScript console to try out some code snippets before you write them in your app:

# How to publish

Once you’ve built an add-on that makes you proud, you’ll definitely want to share it with the world. Firefox Marketplace offers you the option to publish it to the whole world.

You’ll need to zip your files, including the `manifest.json`

into a zip file. Then upload it to the newly released [Marketplace add-on submission page](https://marketplace.firefox.com/content/addon/submit/).

Since add-ons are quite powerful, your add-on will be reviewed by Mozilla’s expert reviewers to insure that user security and privacy aren’t compromised. You can find the [review criteria here](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Add-ons/Review_criteria), be sure to take a look before you submit your add-on.

# Wrap-up

We’ve walked you through the process of building a simple Firefox OS add-on. We’ve shown you how to intercept system notifications, read and write System settings, and draw your custom UI elements on top of the Homescreen UI. We also showed you how to install and debug add-ons using WebIDE. Personally, I believe Firefox OS add-ons will be a game-changer for the Firefox OS platform. Add-ons empower the user to take full control of their mobile experience! This article also demonstrates how easy it is to build an add-on using standard web technology. We look forward to seeing how many ingenius add-ons people can build!

## About
[
Shing Lyu ](https://shinglyu.github.io)

I am now a QA engineer in Firefox OS. I do test automation and build test tools. I also work on Firefox OS apps, add-ons and various other open source projects.

## 4 comments

Mahdi DibaieeNovember 2nd, 2015 at 11:43Francis KimNovember 2nd, 2015 at 20:21Mauricio Navarro MirandaNovember 6th, 2015 at 14:11Jesús PeralesNovember 9th, 2015 at 11:34