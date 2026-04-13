---
title: Notes on developing an API – Mobozi, a WebFWD project – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/03/notes-on-developing-an-api-mobozi-a-webfwd-project/
author: Nick Gottlieb
published: '2013-03-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 has made it easy to do a lot of really cool stuff on the mobile web, but one thing that is still pretty difficult is dealing with photos. Android has supported access to the device camera via the File API since version 3.0 and iOS opened it up last Fall with iOS 6. Allowing users to snap and upload photos in HTML5 is not as simple as just connecting a form to a database however. With a multitude of devices, OS versions, and browsers the image files come in different orientations, sizes, and with different encoding.

I frequently encountered this headache when developing HTML5 apps, which lead myself and my partner to create [Mobozi](https://mobozi.com/). Mobozi is a front end library that optimizes and normalizes images across mobile devices, OSs, and browsers and also a simple API for photo upload and serving. This post is a brief overview of how we went about creating the API to to be functional and also easy and effort free for developers to use.

## Planning

The first thing we did was map our all the functionality we would need and walk through the different use cases and flows from our users perspective. We thought about things like formatting and version control and how we could structure them to make it as developer friendly as possible.

We also considered data formats and decided to support JSON, XML and JSONP in order to keep the API as flexible as possible. We also made sure to model the API calls in a way that they were predictable and did not require the developer to guess. For example, to add an item, POST method is always used and to retrieve GET is used.

## Security

Next we thought security, one of the most important parts of any public facing API. We decided to serve our API from a subdomain ([https://api.mobozi.com](https://api.mobozi.com)) and allow CORS (Cross Origin Resource Sharing) on this domain only (our main domain and all other sub domains don’t entertain any request that originated from a different domain). Additionally, [CORS on Apache](http://enable-cors.org/server_apache.html) is a great resource.

## Developer Experience

Once all the nuts and bolts of the domain had been decided upon, we had to think about how developers would actually get access to and implement our API. We decided to provide an API key and use an HTTP token authentication in order to authenticate them. We also spent a lot of time refining our docs and are continuing to listen to feedback in order to get them as streamlined as possible.

## Technology

Once we decided on the functionality the API would need to provide, as well as how it would be implemented, we had to choose a stack to build it on. We chose PHP/MySQL because it’s stable, scaleable, and most importantly because our team was very comfortable and familiar with it. Next we began searching for a framework that would keep our API lightweight but also offer our users a very quick response time.

After researching and testing out different API frameworks we found two that met our needs – [Limonade](http://limonade-php.github.com/) and [Slim](http://www.slimframework.com/). Limonade is a PHP micro framework for rapid web development and prototyping. Slim is also a PHP micro framework that helps you quickly write simple yet powerful web applications and APIs.

We eventually decided on Limonade because it was easier to implement and provides functionality we needed like clean URLs and cross origin request handling. Slim was powerful and light as well but had issues with cross origin requests as well as with the auto loader.

Here is a brief example from our API. This code will allow you upload an image from any device and get back the URL where it is being stored.

### Include this snippet in your page’s head

```
```

```
mobozi.init('123456789');
function uploadImage(){
var myFile = document.getElementById('idimage').files[0];
var imageData = {
"file": myFile
};
mobozi.image.uploadGetUrl(imageData,function(response) {
if (response.status == 201){
$('#imgUrl').html('URL: ' + response.data.imageUrl);
$('#upImage').attr('src',response.data.imageUrl);
} else {
alert (response.error);
}
});
}
```

### Include this snippet in your page’s body

```
```


### A working example

A working example is [available on jsFiddle](http://jsfiddle.net/mobozi/2mn9E/).

## Outreach

So the functionality has been hashed out, the plan of attack decided, and the code written; what next? Get developers to use the thing! And hopefully get feedback from them on how to make it better. This is what we’re currently doing at Mobozi by [holding a Hackathon](http://www.mobozi.com/hackathon.php) (awesome HiFi speaker for the winner). More details in that page and feel free to ask any questions at founders@mobozi.com.

## About
[
Nick Gottlieb ](http://www.mobozi.com)

entrepreneur, builder, designer, hacker, explorer, surfer, Japanese speaker.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.