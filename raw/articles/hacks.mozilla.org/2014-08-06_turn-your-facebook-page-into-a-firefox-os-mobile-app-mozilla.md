---
title: Turn your Facebook page into a Firefox OS mobile app – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2014/08/turn-your-facebook-page-into-a-firefox-os-mobile-app/
author: Mahmoud Nouman
published: '2014-08-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Whether you are a business or community page owner, what would be better than increasing your page reachability by offering your standalone mobile app?

[Apptuter](http://www.apptuter.org/) is an open source framework to help you achieve that, with minimum coding knowledge and easy to follow steps you would be able to produce your own app. The framework currently supports Facebook pages as a content source and is capable of producing apps for Firefox OS and Android platforms.

## How it works

Let us take a test drive on how this is supposed to work. In our example we will generate a standalone app using Mozilla’s Facebook page as a content source.

### Clone the repository

First step would be to download or clone the Apptuter-Firefox directory from the [Apptuter repository](https://github.com/egirna/apptuter):

```
git clone https://github.com/egirna/apptuter.git
```


Directory structure should look like this:

### Get the Facebook numerical id

Then we will need to get the Facebook numerical page id. If you have assigned a friendly page name, the page ID will not be visible from the page URL, in this case we will need to visit the following URL to retrieve it: `https://graph.facebook.com/mypagename`


In our example this would be: [https://graph.facebook.com/mozilla](https://graph.facebook.com/mozilla)

Page ID will be visible on the first line of data returned.

![](../../assets/ed6127cc4f3f8980.png)


### Create a Facebook app

Next step would be creating a Facebook app: You will able to get App `ACCESS TOKEN`

by combining `APP ID`

& `APP SECRET`

so that the requested URL should be in the following form: `http://graph.facebook.com/endpoint?key=value&access_token=app_id|app_secret`


![](../../assets/898f64b16ca5b896.png)


Requesting Page Info (`Info.js`

) is where we are going to define those parameters, replace PageID with the numerical that can be found at `/Apptuter-Firefox/js`


```
var Main = function () {
this.pageName = ‘pageID’;
this.name = null;
this.category = null;
this.description = null;
this.photoArray = null;
this.postArray = null;
this.infoArray = [];
this.accessToken = 'AppID|AppSecret';
this.pictureUrl = null;
this.paging = 'https://graph.facebook.com/' + this.pageName + '/posts?limit=20&access_token='+this.accessToken;
this.pagingNext = 'https://graph.facebook.com/' + this.pageName + '/posts?limit=20&access_token='+this.accessToken;
}
```

Let us define our new app properties in the `manifest.webapp`

file found at the directory root:

```
{
"name": "Mozilla App",
"description": "This is an example app of apptuter framework",
"launch_path": "/Shared/index.html",
"icons": {
"32": "/images/app_icon_32.png",
"60": "/images/app_icon_60.png",
"90": "/images/app_icon_90.png",
"120": "/images/app_icon_120.png",
"128": "/images/app_icon_128.png",
"256": "/images/app_icon_256.png"
},
"chrome": {
"navigation": true
},
"version": "1.0.1",
"developer": {
"name": "Egirna Technologies Limited",
"url": "http://www.apptuter.org"
},
"orientation": [
"portrait"
],
"default_locale": "en"
}
```

### Artwork

Only thing left is the artwork. From the repository, go to `/Apptuter-Firefox/images`

and replace the default images with those of our example logo with matching dimensions and file name.

![](../../assets/b146c9d6720a36ab.png)


## Success!

And we are done! Let us test what the app would look like using [Firefox OS Simulator](https://developer.mozilla.org/en/docs/Tools/Firefox_OS_Simulator):

![](../../assets/405c54c45fb81dc4.png)


![](../../assets/6c492c05f6cdd615.png)


![](../../assets/3bd75e9c8de97708.png)


You ultimately are responsible to use this software in compliance with Facebook, Google and Mozilla terms of service and end user license agreement. This applies to any service this software may integrate with.

## About Mahmoud Nouman

Apptuter open source framework project coordinator, interested in social media, information security and mobile platforms. M. Sc. computer science.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 5 comments

Veera ManikantaAugust 7th, 2014 at 08:59Mahmoud NoumanAugust 8th, 2014 at 04:39Gabriele VidaliAugust 8th, 2014 at 03:36Mahmoud NoumanAugust 8th, 2014 at 04:38Facebook AlternativeAugust 10th, 2014 at 12:22