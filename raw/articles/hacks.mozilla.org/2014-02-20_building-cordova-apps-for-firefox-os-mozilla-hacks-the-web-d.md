---
title: Building Cordova apps for Firefox OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/02/building-cordova-apps-for-firefox-os/
author: Piotr Zalewa Posted; Firefox OS; HTML
published: '2014-02-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Update:** *In addition to the Cordova integration described below, Firefox OS is now supported in the 3.5 release of Adobe PhoneGap.*

If you’re already building apps with PhoneGap, you can quickly and easily port your existing apps to Firefox OS. We think this is so cool that we’ve launched a [ Phones for PhoneGap Apps program](https://hacks.mozilla.org/2014/05/build-your-next-app-with-a-flame/), focused specifically on compelling apps built with PhoneGap and/or Cordova. Got a great PhoneGap app?

[We’d love to send you a device!](https://mozhacks.wufoo.com/forms/apps-on-a-flame/)

[Cordova](http://cordova.apache.org/) is a popular Apache Foundation open source project providing a set of device APIs to allow mobile application developers to access native device functions—such as the camera or the accelerometer—from JavaScript. HTML5 applications can be packaged as native apps via the framework and made available for installation from the app stores of supported platforms, including iOS, Android, Blackberry, Windows Phone—and now [Firefox OS](https://developer.mozilla.org/en-US/Firefox_OS). Cordova is also the underlying software in the Adobe product [PhoneGap](http://phonegap.com/).

Over the past few months, Mozilla has been working with the Cordova team to integrate Firefox OS into the Cordova framework, making it possible to release Cordova apps on the Firefox OS platform. While this is an ongoing project, significant functionality is available now with the [3.4 release](http://cordova.apache.org/announcements/2014/02/20/cordova-340.html) of Cordova. In this post we will describe how to use these new capabilities.

## Creating and building a Firefox OS app in Cordova

The [Cordova site](http://cordova.apache.org/docs/en/3.4.0/guide_cli_index.md.html#The%20Command-Line%20Interface) explains how to install the software. Note the installation procedure requires Node.js and can be executed from the command line.

`$ sudo npm install -g cordova`

Once Cordova is installed, an application can be built with the Cordova create command. (Parameters for the command are described in the Cordova documentation linked above.)

`$ cordova create hello com.example.hello HelloWorld`

This will create a directory named hello that contains the project and a basic web app in the hello/www directory. In order to produce a Firefox OS app, the proper platform needs to be added next.

```
$ cd hello
$ cordova platform add firefoxos
```

With some of the other supported platforms, you would generally run a build command at this stage to produce the output for the platform. Because Firefox OS is an HTML5-based operating system, no compile step is needed to process and produce the app. The only step required is a prepare statement to package the app.

`$ cordova prepare firefoxos`

Those are the basic steps to generate a simple Firefox OS app from a Cordova project. The output for the project will be located in the hello/platforms/firefoxos/www directory.

## Debugging the app

With most other Cordova platforms you would use the emulate or run commands to test an app. With Firefox OS you currently need to use the [App Manager](https://developer.mozilla.org/en-US/Firefox_OS/Using_the_App_Manager), which is the primary tool for debugging and interrogating a Firefox OS app. The tool offers many capabilities including JavaScript debugging and live editing of the CSS while connected to a device.

The above link explains how to install and start the App Manager. Once the App Manager is running, you can click the Add Packaged App button and select the hello/platforms/firefoxos/www directory of your app and press the Open button.

This will add the basic app to the App Manager. You will notice no icons are present. This is because the framework integration does not provide them currently and only a bare-bones manifest.webapp is created. From here you can update the app or debug it. Note that between updates you must run a **cordova prepare firefoxos** command as this step packages the app and puts it in the platforms/firefoxos/www directory. Below is a screenshot of the Cordova HelloWorld app being debugged.

## The Firefox OS Manifest

Firefox OS apps are essentially HTML5 applications that are described by a manifest file. This manifest file points to artifacts like icons, start page, etc. that will be used by the application. In addition, the manifest controls privilege levels and device-specific APIs that are needed by the app. The [manifest documentation is available on MDN](https://developer.mozilla.org/en-US/Apps/Developing/Manifest).

With the default integration in Cordova, a very generic manifest is created and placed in the platforms/firefoxos/www directory. In almost all cases this will not suffice, as you will at least want to provide icons for your app. The App Manager will complain if the app does not contain at least a 128×128 pixel sized icon. This does not prevent you from testing your app, but it is required to upload your app to the Firefox Marketplace. The manifest can be created with a simple text editor or you can modify the manifest in the App Manager. An example `manifest.webapp`

is shown below.

```
{
"name": "My App",
"description": "My elevator pitch goes here",
"launch_path": "/",
"icons": {
"128": "/img/icon-128.png"
},
"developer": {
"name": "Your name or organization",
"url": "http://your-homepage-here.org"
},
"default_locale": "en"
}
```

Make sure the manifest is created or copied into the project/www folder. Subsequent cordova prepare commands will replace the auto-generated manifest with your application-specific manifest.

## Start Up Code

When creating a Cordova app, the starter code generated includes index.html, css/index.css, img/logo.png and js/index.js files. The code in index.js is initiated in index.hml like this:

```
```

The initialize function essentially sets up the event trigger for the onDeviceReady event, which signifies that the Cordova framework is loaded and ready. The generated code is sufficient for Firefox OS unless you want to implement a privileged App. Privileged apps are Marketplace-signed apps that require the use of more sensitive APIs–for example, Contacts API. See the [Packaged apps documentation](https://developer.mozilla.org/en-US/Marketplace/Publishing/Packaged_apps?redirectlocale=en-US&redirectslug=Mozilla%2FMarketplace%2FPackaged_apps#Types_of_packaged_apps) for more information. For privileged Apps, code like this violates [CSP](https://developer.mozilla.org/en-US/Apps/CSP) restrictions because of the inline script tag. To get around this, remove the inline script and initiate the app using a window.onload event in the js/index.js file.

## Sample App

To test and debug the Cordova/Firefox OS integration we developed a sample app. This application is available on [GitHub](https://github.com/JasonWeathersby/cordovasample). It illustrates use of the device-specific plugins. The images and code snippets in the following sections were taken from the sample app. If you want to check out the code and work with it, first create a Cordova project and check the code into the project/www directory. You can then run cordova prepare firefoxos to package the app. Run and debug as described earlier in this post.

![app](../../assets/2331490dec322f08.png)


## Device APIs

Cordova uses a plugin architecture to implement device APIs, such as Accelerometer, Geolocation or Contacts. These APIs are very similar to [Firefox OS Web APIs](https://developer.mozilla.org/en-US/docs/WebAPI) and [Web Activities](https://developer.mozilla.org/en-US/docs/WebAPI/Web_Activities) and are documented on the [Cordova website](http://cordova.apache.org/docs/en/3.4.0/). Below are the current plugins implemented for Firefox OS and a brief description of how you can include them in your app. You can always see the [current status of plugin development for the Firefox OS Platform](https://issues.apache.org/jira/browse/CB-3204) by checking Jira on the Apache website.

## Notification API

The notification API is used to alert the user of your app and is implemented in two plugins: org.apache.cordova.dialogs and org.apache.cordova.vibration. Currently we have implemented the alert, confirm, prompt and vibrate functions. To use this functionality, add the plugins to your project with the following commands:

```
$ cordova plugin add org.apache.cordova.dialogs
$ cordova plugin add org.apache.cordova.vibration
```

To get proper styling of popup boxes in Firefox OS, you will need to add the notification.css file to your project. After adding the dialogs plugin, change to the project/plugins/org.apache.cordova.dialogs/www/firefoxos directory and copy the notification.css file to your project/www/css folder. Link the CSS file in head element of index.html.

```
```

You can now use the notification functions.

```
function onPrompt(results) {
alert("You selected button number " +
results.buttonIndex +
" and entered " + results.input1);
}
navigator.notification.vibrate(500);
navigator.notification.prompt(
'Enter Name', // message
onPrompt, // callback to invoke
'Prompt Test', // title
['Ok', 'Exit'], // buttonLabels
'Doe, Jane' // defaultText
);
```

![prompt](../../assets/054141ce1250dffe.png)


## Compass API

The compass API is implemented using the org.apache.cordova.device-orientation plugin. This plugin implements the compass getCurrentHeading and watchHeading functions. To use it simply run the plugin add command:

```
$ cordova plugin add org.apache.cordova.device-orientation
```

Once the plugin is added, you can use the get or watch heading function to get compass information.

```
function onSuccess(heading) {
var element = document.getElementById('heading');
myHeading = (heading.magneticHeading).toFixed(2);
console.log("My Heading = " + myHeading);
}
function onError(compassError) {
alert('Compass error: ' + compassError.code);
}
var options = {
frequency: 500
};
watchID = navigator.compass.watchHeading(onSuccess, onError, options);
```

![compass](../../assets/0876b373dd40457d.png)


## Accelerometer API

The Accelerometer is accessed using the org.apache.cordova.device-motion plugin and gives the developer access to acceleration data in x, y and z directions. This plugin implements the getCurrentAcceleration and watchAcceleration functions.

To use these functions, add the device-motion plugin to your project by executing the following command.

```
$ cordova plugin add org.apache.cordova.device-motion
```

You can then monitor the acceleration values using code similar to this:

```
var options = {
frequency: 100
};
watchIDAccel = navigator.accelerometer.watchAcceleration(onSuccess, onError, options);
function onSuccess(acceleration) {
var acX = acceleration.x.toFixed(1) * -1;
var acY = acceleration.y.toFixed(1);
var acZ = acceleration.z.toFixed(1);
var vals = document.getElementById('accvals');
var accelstr = "
```**Accel X: **" + acX + "

" + "**Accel Y: **" + acY + "

" + "**Accel Z: **" + acZ;
vals.innerHTML = accelstr;
}
function onError() {
alert('Could not Retrieve Accelerometer Data!');
}

You can also monitor the device orienttation event and retrieve alpha, beta, and gamma rotation values like:

```
function deviceOrientationEvent(eventData) {
//skew left and right
var alpha = Math.round(eventData.alpha);
//front to back - neg back postive front
var beta = Math.round(eventData.beta);
//roll left positive roll right neg
var gamma = Math.round(eventData.gamma);
console.log("beta = " + beta + " gamma = " + gamma);
}
window.addEventListener('deviceorientation', deviceOrientationEvent);
```

![](../../assets/32511a7d2a3218d6.png)


## Camera API

The camera API is used to retrieve an image from the gallery or from the device camera. This API is implemented in the org.apache.cordova.camera plugin. To use this feature, add the plugin to your project.

```
$ cordova plugin add org.apache.cordova.camera
```

In the Firefox OS implementation of this plugin, the getPicture function will trigger a Web Activity that allows the user to select where the image is retrieved.

Code similar to the following can be used to execute the getPicture function:

```
navigator.camera.getPicture(function (src) {
var img = document.createElement('img');
img.id = 'slide';
img.src = src;
}, function () {}, {
destinationType: 1
});
```

## Contacts API

The contacts API is used to create or retrieve contacts on the device and is implemented in the org.apache.cordova.contacts plugin. To access this feature, run the following command:

```
$ cordova plugin add org.apache.cordova.contacts
```

Apps that access contacts must be privileged with the appropriate permission set in the manifest file. See “The Firefox OS Manifest” section earlier in this post to understand how to create a custom manifest for your application. For this API, you will need to add the following permissions to the manifest:

```
"permissions": {
"contacts": {
"access": "readwrite",
"description": "creates contacts"
}
}
```

See the [manifest documentation](https://developer.mozilla.org/en-US/Apps/Developing/Manifest) for specific access rights. In addition, you will need to change the type of app to privileged in the manifest.

```
"type": "privileged",
```

Once the manifest has been changed, you can add contacts with code like the following.

```
// create a new contact object
var contact = navigator.contacts.create();
var name = new ContactName();
name.givenName = fname;
name.familyName = lname;
contact.name = name;
contact.save(onSuccess, onError);
```

![contact](../../assets/25a0377294dba544.png)


## Geolocation API

The geolocation API is used to retrieve the location, time and speed values from the devices GPS unit and is implemented in the org.apache.cordova.geolocation device plugin.

```
$ cordova plugin add org.apache.cordova.geolocation
```

You can retrieve the device latitude, longitude and a timestamp using this API on Firefox OS, but it does require the addition of a permission to the manifest file. See “The Firefox OS Manifest” section earlier in this post to understand how to create a custom manifest for your application.

```
"permissions": {
"geolocation": {
"description": "Marking out user location"
}
}
```

Adding this permission causes the app to prompt the user for permission to retrieve the GPS data. You can use either getCurrentPosition to read the GPS once or watchPosition to get an interval based update.

```
var onSuccess = function (position) {
console.log('Latitude: ' + position.coords.latitude + 'n' +
'Longitude: ' + position.coords.longitude + 'n');
};
function onError(error) {
console.log('Error getting GPS Data');
}
navigator.geolocation.getCurrentPosition(onSuccess, onError);
```

![geolocation](../../assets/e0bb6bd814ea2181.png)


## Join Us

This post covered some of the basics of the new Firefox OS Cordova integration. We will continue to add more device APIs to the project, so stay tuned. If you are interested in working on the integration or need support for a specific device plugin, please contact us on [Stack Overflow under the firefox-os tag](http://stackoverflow.com/questions/tagged/firefox-os) or in #cordova on [Mozilla IRC](https://wiki.mozilla.org/IRC).

In the meantime, if you have a Cordova app that makes use of the APIs discussed above, please try generating it for Firefox OS and submitting it to the Firefox Marketplace!

## About Piotr Zalewa

Piotr Zalewa is a Senior Web Developer at Mozilla's Dev Ecosystem team. Working on web apps. He is the creator of JSFiddle.

## 13 comments

HugoFebruary 20th, 2014 at 12:43James LongFebruary 20th, 2014 at 13:12debbieFebruary 20th, 2014 at 17:21LukeFebruary 20th, 2014 at 19:39Robert Nyman [Editor]February 21st, 2014 at 05:48HugoFebruary 21st, 2014 at 15:15Arul SelvanFebruary 21st, 2014 at 09:46towfique anam rineFebruary 20th, 2014 at 12:55sintaxiFebruary 20th, 2014 at 15:26oztenFebruary 20th, 2014 at 15:56Sébastien BlancFebruary 21st, 2014 at 03:22dac sanFebruary 23rd, 2014 at 17:26grigioFebruary 24th, 2014 at 07:51