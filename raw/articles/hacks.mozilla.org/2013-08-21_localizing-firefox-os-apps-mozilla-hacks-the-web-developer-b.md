---
title: Localizing Firefox OS Apps – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/08/localizing-firefox-os-apps/
author: Robert Nyman Posted; Localization
published: '2013-08-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox OS Apps are being used around the world—Spain, Poland, Colombia and Venezuela with many more countries coming—so it’s important to consider localizing your app from the beginning. But with the open web being as open as it is, there are many frameworks and technologies to pick from when it comes to localization. For example, the [Jed](http://slexaxton.github.io/Jed/) Gettext-style library is a popular traditional option. There are also new localization platforms in development that extend the capabilities available in current libraries. For example, at Mozilla we have a very promising [localization project](https://wiki.mozilla.org/L20n) that extends L10n with a variety of compelling new features. To learn more about it, check out the Mozilla [Tools group](https://groups.google.com/forum/#!forum/mozilla.tools.l10n).

In this post, we will discuss how to localize your Firefox OS app using the libraries currently employed for localization in the [Gaia](https://github.com/mozilla-b2g/gaia) layer of Firefox OS. Gaia encompasses all of the built-in web apps in the operating system, including the Dialer and the Contacts Manager, so it provides a good model to emulate. However, if you decide to use this approach, bear in mind that some features of the library (for example l10n_date.js uses non-standard toLocaleFormat method) are not cross-browser compatible, and know Gaia will likely move to L20n at some point in the future.

## L10n.js

Currently Firefox OS Gaia uses a modified version of Fabien Cazenave’s [L10n.js](https://github.com/fabi1cazenave/webL10n) library to localize the default Apps that are available in Firefox OS. It is available in the Gaia [source tree](https://github.com/mozilla-b2g/gaia/blob/master/shared/js/l10n.js). The library relies on the key/value based properties format. The L10n.js parser also supports import rules that can be used for client side language selection. The default Gaia apps use an ini file to specify the import statements and a link tag to load up the ini file.

As an example of how it works, examine the Bluetooth App, which can be used to transfer files. The App’s properties files are structured in the following fashion.

![bluetooth](../../assets/d9733232f60b2efc.png)


This App contains properties files for four locales (ar, en-US, fr, and zh-TW). A portion of the en-US properties file is listed below:

```
bluetooth = Bluetooth
confirmation = Confirmation
bluetooth-status-description = Bluetooth is disabled
turn-bluetooth-on = Do you want to turn Bluetooth on?
cancel = Cancel
turn-on = Turn On
```

As you can see, it’s a simple key/value property file with the set of strings to localize. All of these files are stored in the locales directory of the Bluetooth App. In addition, this folder contains a locales.ini file with the following content:

```
@import url(bluetooth.en-US.properties)
[ar]
@import url(bluetooth.ar.properties)
[fr]
@import url(bluetooth.fr.properties)
[zh-TW]
@import url(bluetooth.zh-TW.properties)
```

The ini file specifies what properties files to load based on the locale of the App user. It acts as multi-locale dictionary listing all supported locales. Also, in this particular instance, the en-US properties file acts as the default locale if no entry is found for a given user locale. This ini file is loaded by using the following syntax with the link tag.

The rel attribute can also be set to “prefetch” to preload the ini file to increase performance.

## L10n Element Attributes

You define elements that need translation by adding a data-l10n-id attribute, which is the key defined in the properties file. For example, a header that needs localization can look like this:

## Label One


The value of the attribute “label1” serves as the key into the properties file. Complex strings can be created in the properties files using argument substitution and the plural macro.

## Argument Substitution

Argument substitution is achieved by surrounding the argument with double curly braces {{arg}}. A message can then be customized for a specific user using syntax similar to the following:

`loginmessage = Hello {{user}}, glad you decided to visit`

Default values for arguments can be set using the data-l10n-args attribute. This attribute expects a JSON formatted value. In the above example, a default value could be set for the user argument by using the HTML below.

## Label One


## Plural macro

The plural macro can be used to customize messages based on an argument value. The macro takes a number value and returns zero, one, two, few, many, or other. The return value depends on the value passed in and the current locale’s [Unicode Plural Rules](http://unicode.org/repos/cldr-tmp/trunk/diff/supplemental/language_plural_rules.html). As an example, a customized mail message for the en-US locale may look something like:

```
mailMessage = {[ plural(n) ]}
mailMessage[zero] = you have no messages
mailMessage[one] = you have one message
mailMessage[two] = you have two messages
mailMessage[other] = you have {{n}} messages
```

### Mail Message


## L10n Script

Most of the default Firefox OS Apps use a script tag similar to the following to load the L10n.js library.

To use this library in your own application, you will need to copy the l10n.js file to your local project and change the source attribute.

Once loaded, the L10n.js library will expose a ‘navigator.mozL10n’ object that can be used for client side localization.

The most useful methods and properties for mozL10n are described below.

## The get Method

The get method is used to get a translated string for the current locale. The method takes a key parameter and an optional args parameter. The key parameter specifies the key defined the properties file.

`navigator.mozL10n.get("mylabel")`

The args parameter can be used to pass a JSON formatted argument for strings that contain arguments.

```
//properties file
welcome = Welcome {{user}}!
//JavaScript
alert( navigator.mozL10n.get(“welcome”, { user: "Martin" }));
```

## The localize Method

The localize method can be used to add the L10n attributes to dynamically created content. The method takes an element parameter, and id parameter, and an optional args parameter. The element parameter specifies the element to be localized. The id parameter specifies the L10n-based attribute id you want to assign to the element. The optional args parameters allows you to create the data-l10n-args attribute and set its JSON value.

```
var button2 = document.querySelector("#button2");
if (button2) {
button2.onclick = function () {
var myElement = document.createElement('span');
var lblTxt =document.createTextNode("My Label");
myElement.appendChild( lblTxt );
navigator.mozL10n.localize(myElement, 'label3'{ arg: "myarg" });
document.body.appendChild(myElement);
}
};
```

This will create the following HTML.

` My Label`

In addition the text will also be translated immediately.

## The ready method

The ready method allows you to define a callback when localization for the current document is complete.

```
var button1 = document.querySelector("#button1");
if (button1) {
button1.onclick = function () {
navigator.mozL10n.language.code = "fr";
navigator.mozL10n.ready( function() {
alert(navigator.mozL10n.get("button1"));
});
}
};
```

## The language property

The language property contains a getter and setter for the language code. The language property also contains a getter for the language direction for supporting right to left (Arabic or Hebrew) and left to right languages.

```
var mycode = navigator.mozL10n.language.code;
navigator.mozL10n.language.code = "fr";
navigator.mozL10n.language.direction //returns rtl or ltr
```

## L10n_Date Script

For date and time manipulation, Gaia applications extend the capabilities of L10n.js with the l10n_date.js library. As with the l10n.js library, it implements some features that may not be compatible with all browsers. The library is available in the Gaia [source tree](https://github.com/mozilla-b2g/gaia/blob/master/shared/js/l10n_date.js) and uses the same property structure described in the L10n.js section of this article. Gaia Apps that use this library all rely on a shared set of properties files and a date.ini file to import the locale specific properties file. The date.ini file is located in the Gaia [source tree](https://github.com/mozilla-b2g/gaia/blob/master/shared/locales/date.ini) and the locale specific properties files are located in https://github.com/mozilla-b2g/gaia/tree/master/shared/locales/date directory. These properties files define formats and strings for things like the day a week starts on, short date formats and then names of months. To use this library in your own application, you will need to copy all of the files to your specific project. The ini and script files are loaded in a similar manner to the L10n.js library.

```
```

When using the L10n_date library’s format methods, the strings in the properties files can use standard C++ date/time [formatting codes](http://www.cplusplus.com/reference/ctime/strftime/). As an example of this, examine the Gaia Clock App’s properties file. This file contains the following entry for dateFormat for the en-US locale.

`dateFormat = %A, %B %e`

Using the formatLocale method within the L10n_Date library, this will return:

“Full Weekday Name” “Full Month Name” “Day of the Month” (Thursday January 29). The French version of the properties file defines the same key in the following fashion.

`dateFormat = %A %e %B`

This will produce:

“Full Weekday Name” “Day of the Month” “Full Month” (jeudi 25 janvier).

When you include the L10n_Date library, a new method is available to the mozL10n object (`navigator.mozL10n.DateTimeFormat()`

). Once instantiated this object has several methods that can be used to localize dates. The most useful ones are:

## The localeFormat method

The localeFormat method takes a date object parameter and a format pattern parameter and returns the date formatted as specified in the pattern. This method should be used in conjunction with the L10N.js get method to format a localized date.

```
button3.onclick = function () {
navigator.mozL10n.language.code = "fr";
navigator.mozL10n.ready( function() {
var d = new Date();
var f = new navigator.mozL10n.DateTimeFormat();
var format = navigator.mozL10n.get('dateFormat');
var formatted = f.localeFormat(d, format);
alert( formatted );
});
}
```

## The localeDateString, localeTimeString and localeString methods

These three methods are just variations of the localeFormat method that return formatted dates based on the following key values within the date properties files.

```
//en-US
//localeString returns
dateTimeFormat_%c = %a %b %e %Y %I:%M:%S %p
//localeDateString returns
dateTimeFormat_%x = %m/%d/%Y
//localeTimeString rerturns
dateTimeFormat_%X = %I:%M:%S %p
```

## The fromNow method

The fromNow method takes a date/time parameter and returns a locale-formatted string expressing the difference between the current date/time and the date/time passed in. The formatted string will be based on the strings defined in the date properties file. For example:

```
//Executed on 7/25/2013 12:11:00
var d = new Date("July 25, 2013 11:13:00");
var f = new navigator.mozL10n.DateTimeFormat();
alert( f.fromNow(d));
```

Would alert “58 Minutes Ago” in the en-US locale. The String will be formatted using the minutes-ago-long key in the date properties file.

```
minutes-ago-long={[ plural(value) ]}
minutes-ago-long[zero] = just now
minutes-ago-long[one] = a minute ago
minutes-ago-long[two] = {{value}} minutes ago
minutes-ago-long[few] = {{value}} minutes ago
minutes-ago-long[many] = {{value}} minutes ago
minutes-ago-long[other] = {{value}} minutes ago
```

## Learn more, and get involved!

For further reading on good localization practices, see the Mozilla Developer Network article,[ “Creating localizable web applications.”](https://developer.mozilla.org/en-US/docs/Web_Localizability/Creating_localizable_web_applications)

And after you’ve finished localizing your own Firefox OS app, why not help with localization of Firefox OS itself? Take a look this [link](https://developer.mozilla.org/en-US/docs/Firefox_OS/Hacking_Firefox_OS/Localizing_Firefox_OS) for more information on how to contribute.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 10 comments

goofyAugust 22nd, 2013 at 09:36Chris MillsAugust 22nd, 2013 at 10:22niutechAugust 22nd, 2013 at 15:08Jason WeathersbyAugust 26th, 2013 at 08:42Peter RukavinaAugust 25th, 2013 at 12:38Peter RukavinaAugust 26th, 2013 at 05:55Peter RukavinaAugust 26th, 2013 at 06:03Jason WeathersbyAugust 26th, 2013 at 08:41Abin AbrahamAugust 26th, 2013 at 19:21Jason WeathersbyAugust 27th, 2013 at 08:29