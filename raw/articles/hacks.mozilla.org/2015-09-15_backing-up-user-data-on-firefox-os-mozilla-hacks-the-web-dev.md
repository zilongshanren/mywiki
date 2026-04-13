---
title: Backing Up User Data on Firefox OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/09/backing-up-user-data-on-firefox-os/
author: Ryan Bernstein
published: '2015-09-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## The FFOS Backup/Restore Team

Portland State University’s Computer Science degree culminates in a capstone program that matches teams of students with industry sponsors for a six-month software engineering project. We had the privilege of working with Mozilla on an application to back up and restore personal data on Firefox OS. We are:

[Ryan Bernstein](https://github.com/RyanLB): Team Lead/History/Demo application.

[David Cobbley](https://github.com/dcobbley): Contacts/SMS Messages.

[Thomas Guerena](https://github.com/thomasguerena): Architecture/Build environment/Media.

[Wu Hao](https://github.com/wuhaooooo): SMS Messages/Space checking.

[Kai Jiang](https://github.com/vectorijk): SMS Messages. Space checking.

[Nathan Larson](https://github.com/nlarsonX): History/System settings.

[Ruben Niculcea](https://github.com/RubenSandwich): Build environment/Media/SMS Messages.

[Dean Nida](https://github.com/drnida): Media/Contacts/Testing.

![From left: Nathan Larson, Jiang Kai, Wu Hao, David Cobbley, Dean Nida, Ruben Niculcea, Thomas Guerena, Ryan Bernstein](../../assets/a5f889b6f12a7acf.jpg)


![From left: Nathan Larson, Jiang Kai, Wu Hao, David Cobbley, Dean Nida, Ruben Niculcea, Thomas Guerena, Ryan Bernstein](../../assets/a5f889b6f12a7acf.jpg)

From left: Nathan Larson, Jiang Kai, Wu Hao, David Cobbley, Dean Nida, Ruben Niculcea, Thomas Guerena, Ryan Bernstein

## The Firefox OS Backup/Restore Library

The purpose of this capstone project was to allow users of Firefox OS to back up and restore their personal data. The OS does not provide any native support for such backups, despite the fact that it is sorely needed; Firefox OS was initially targeted at developing nations, where it runs on inexpensive hardware and may be the user’s primary computing device.

Making a backup application is a difficult task. As developers, we’re unable to anticipate future changes in both the operating system itself and the types of data that users create. Ultimately, we decided that the ephemeral nature of a senior capstone team meant that we would be unable to provide the long-term support necessary to deploy and maintain an application on the app store.

We therefore decided to create a library, rather than a standalone application. Our reasoning was that we would be able to make a stronger impact by providing a foundation for other developers to build their own backup applications on. After six months of development, we had created the Firefox OS Backup/Restore (FFOSBR) library, as well as a small test application to demonstrate its basic capabilities.

## Capabilities of FFOSBR

The Firefox OS Backup/Restore (FFOSBR) library is designed to back up media to an SD card. While we had envisioned being able to back up data via USB as well, this would have required the development of a companion application to interpret the data on the receiving PC, which was outside the scope of our project.

The FFOSBR library is capable of backing up and restoring:

- Photos
- Music
- Videos
- Contacts
- System Settings

The library can also back up the user’s SMS and MMS messages. However, Firefox OS currently provides no API for adding messages to the phone without actually sending them via SMS or MMS. As such, messages are backed up as JSON objects to a text file on the SD card, but cannot be restored back to the phone.

## Implementation

FFOSBR is implemented as a collection of modules. Each type of personal data has a module, but there are additional “helper” modules that are used to hold the library together. Notably, these include a `ffosbr.settings`

module to track application settings (such as which data types have backups enabled) and a ffosbr.history module that tracks backup dates and sizes for each data type.

Data type-specific modules each implement, at minimum, three public functions: `backup()`

, `restore()`

, and `clean()`

. These functions all take a single callback parameter, oncomplete. The callback should be a function that takes two arguments. The first argument will always be the name of the type backed up; any errors that occur will be passed to the oncomplete function in the second argument. Passing the type as the first argument allows us to use a technique that we refer to as *patient oncompletes*, which will be described shortly.

In addition, there are top-level helper modules — `ffosbr.backup()`

, `ffosbr.restore()`

, and `ffosbr.clean()`

— which iterate over all of the enabled data type-specific modules and invoke their `backup()`

, `restore()`

, or `clean()`

methods, respectively. This is where *patient oncompletes* come into play. Let’s look at `ffosbr.backup()`

as an example.

`ffosbr.backup()`


`ffosbr.backup()`

takes three arguments, all of which are callback methods. These are onsuccess, onerror, and oncomplete.

`ffosbr.backup()`

runs each data type’s `backup()`

method asynchronously with a function called `callbackManager()`

as an oncomplete. As mentioned above, each data type’s `backup()`

method calls its oncomplete method with the name of the data type as the first argument so that the `callbackManager()`

can identify it. As each data type completes, the `callbackManager()`

examines its second argument to determine whether or not an error occurred. If so, it calls `onerror()`

; otherwise, it calls `onsuccess()`

. Only after every data type’s `backup()`

method has completed does the `ffosbr.backup()`

method finish and invoke its own oncomplete callback.

## Usage

A function that backs up all types of user data might therefore look something like this:

```
var successes = [];
var failures = [];
var reportSuccess = function(type) {
if (type && !successes.includes(type)) {
alertUser(type + ' saved successfully');
successes.push(type);
}
};
var reportError = function(type, error) {
if (type && !failures.includes(type)) {
alertUser(type + ' failed');
failures.push(type);
}
};
var finished = function() {
var sitrep = 'SUCCESSES:\n';
for (var i = 0; i < successes.length; ++i) {
sitrep += '\t' + successes[i] + '\n';
}
sitrep += '\nFAILURES:\n';
for (i = 0; i < failures.length; ++i) {
sitrep += '\t' + failures[i] + '\n';
}
alert(sitrep);
};
ffosbr.backup(reportSuccess, reportError, finished);
```


Cleaning and restoring look similar, but with `ffosbr.clean()`

or `ffosbr.restore()`

used in place of `ffosbr.backup()`

on the last line.

## Demo Application

In addition to the FFOSBR library itself, we’ve also created a simple demo application to show off some of its capabilities. The home screen displays information about current backup status, and has buttons to back up and restore all enabled types:

![2015-08-29-03-38-19](../../assets/9faadbd1f7c99e4d.png)


![2015-08-29-03-38-19](../../assets/9faadbd1f7c99e4d.png)

Clicking on any of the listed types opens a submenu:

![2015-08-30-23-47-11](../../assets/493dc835330b4dc9.png)


![2015-08-30-23-47-11](../../assets/493dc835330b4dc9.png)

Do keep in mind that our primary product was the library itself; as a demo, the application is relatively bare-bones. However, it does provide the capability for users to back up and restore their media, contacts, and system settings to an SD card.

## Future Improvements

Unfortunately, not all backups are entirely nondestructive. Music, pictures, and videos work on a per-file basis. Thus, backing up or restoring data doesn’t remove the data already on the phone or SD card. However, contacts, messages, and system settings are backed up to specific files in the backup directory on the SD card. These files are overwritten with each backup. In the future, we can address this by appending a timestamp to the filenames so that each backup creates a new file.

The contacts module also currently runs synchronously. `ffosbr.contacts.backup()`

calls a function that gets contacts from the SIM card, which in turn calls a function that gets contacts from the device. Ideally, these should be two entirely separate operations which back up to entirely separate files, since it will also allow us to restore SIM contacts back to the SIM card and device contacts back to the device. We didn’t devise our *patient oncomplete* strategy until after the contacts module had been written, but employing this would allow us to back up SIM and device contacts in parallel to separate files.

## Installing Firefox OS Backup/Restore

The FFOSBR project can be found on GitHub at [github.com/autonome/FFOSBR](https://github.com/autonome/FFOSBR). If you are a Firefox OS developer or technical user, take a look and let us know what you think.