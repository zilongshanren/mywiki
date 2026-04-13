---
title: jsDelivr – The advanced open source public CDN – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/03/jsdelivr-the-advanced-open-source-public-cdn/
author: Dmitriy Akulov
published: '2014-03-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post by Dmitriy Akulov and his project jsDelivr. – Editor’s note.*

As a developer you are probably aware of [Google Hosted Libraries](https://developers.google.com/speed/libraries/). Google offers an easy and fast way to include 12 of the most popular js libraries in your websites.

But what if you are a webmaster and you want take advantage of a fast CDN with other less popular projects too? Or if you are a developer and you want to make your project easier to access and use by other users.

This is where [jsDelivr](https://github.com/jsdelivr/jsdelivr) comes into play. jsDelivr is a free and open source CDN created to help developers and webmasters. There are no popularity restrictions and all kinds of files are allowed, including JavaScript libraries, jQuery plugins, CSS frameworks, fonts and more.

## Adding a library

To add a new library or update an existing one all the developer has to do is to clone [our Github repository](https://github.com/jsdelivr/jsdelivr) and apply the modifications they see fit. Once a moderator reviews the Pull Request and merges it, the files become instantly available from the [official website](http://www.jsdelivr.com/).

If a mod is online the approval should not take more than 20 minutes, otherwise it can take up to 10 hours until someone comes online. But once our auto-update utility comes online review times will drop.

## Reliability

But what actually makes it so advanced? The idea of jsDelivr was not to create another public CDN but to offer a super fast and reliable infrastructure that developers and website owners could trust and use. Any big or small website can use it without worrying about it. There are no bandwidth limits and our service is rock solid.

Slow responses, timeouts and downtime are not tolerated, so we designed a unique system to overcome these problems and offer a product that even Enterprise CDNs would be jealous of. Uptime and performance are top priority, we monitor everything at all times and we are always looking into new technologies and providers that may further improve our CDN.

## Infrastructure

Unlike the competition jsDelivr uses a unique Multi-CDN infrastructure to offer the best possible uptime and performance. The main backbone of it is built on top of CDN networks provided by [MaxCDN ](http://www.maxcdn.com/)and [CloudFlare](https://www.cloudflare.com/).

And we also use custom servers in locations where CDNs have little or no presence. In total at this moment this results in 42 global POP locations. In the future we plan to add even more locations to offer top performance even in less popular countries.

Of course lots of locations means nothing if you can’t load balance across them correctly. For the load balancing system we use services provided by [Cedexis](http://www.cedexis.com/). One of their main features is the real time performance data they gather on all major CDN providers. 1.3 billion RUM (Real User Metrics) performance tests per day are processed and available to all Cedexis users.

## Measuring performance

To gather these RUM tests they have deployed a special JavaScript code on thousands of websites. Every visitor to one of these websites executes the code and starts testing different CDN providers in the background as they browse the website. The testing does not impact on the browsing experience in any way and is completely transparent to the user. You can actually see how it works by visiting our [website ](http://www.jsdelivr.com/)and opening developer tools to “Network” tab.

The beauty of these tests is that they are not synthetic. They reflect the real performance real users will get if they download a file from one of those CDNs.

The following information is then stored:

- Performance metrics to each of our providers.
- Availability metrics to each of our providers.
- Browser’s User-Agent
- First three octets of the user’s IP address

Now that we have all this information we can use it in our smart load balancing algorithm.

Every user gets a unique response that is based on their location and ISP provider. Each time a users requests to download a file from jsDelivr, our algorithm extracts the performance and availability data it has available for the last few minutes and then figures out the most optimal provider for that particular user and that particular time. All that in a few ms.

First it makes sure that all available providers are online. For this it uses the RUM availability data and a synthetic test that checks each provider every minute for uptime. Then it proceeds to sort the providers by performance for the ISP of the user and his/her location.

Once it has the fastest provider it returns the hostname to the user. So for example 2 different users in London with different ISPs could get 2 different responses because their ISPs have different routing and performance to different CDN providers. This smart system guarantees maximum uptime and fast loading times to all users. If a provider goes down jsDelivr won’t experience any issue at all and immediately start serving a different provider.

This algorithm also immediately responds to performance degradation. For example a CDN provider gets DDoSed in Europe and their response times increase, jsDelivr will pick up the change and simply stop using this provider in Europe but still consider it for users in USA and other locations that were not affected by the attack.

Don’t rely on a single CDN for uptime and speed. Everything can go down, but the chances for 2 CDNs and multiple servers to go down at the same time are very slim. And this is why jsDelivr is the most optimal solution for every website out there. No matter how big it is.

I should also point out that MaxCDN, CloudFlare, Cedexis and the [rest of the companies](http://www.jsdelivr.com/about.php) sponsor jsDelivr for free. Its nice to see that there are companies out there that are willing to help open source projects and build a fast and free internet.

## Advanced Features

jsDelivr also supports some interesting and very helpful features such as:

### Version Aliasing

Instead of using a unique URL for each version to load a project with jsDelivr you can use aliasing. Lets take for example the project Abaaso. At this moment the latest version is 3.10.50 and you can load it by specifying the exact version in your url as always. But since this project gets updated very often you would end up with using the old version pretty soon. To overcome this problem you can now simply use the following URL:

`//cdn.jsdelivr.net/abaaso/3.10/abaaso.min.js`

By using 3.10 you tell jsDelivr to load the latest version it has in the 3.10 branch which in this case is 3.10.50. This is the optimal solution for most authors because they can load the latest minor version without worrying for major changes that could break their website.

It is of course possible to load the latest version in the v3 branch by using the following URL:

`//cdn.jsdelivr.net/abaaso/3/abaaso.min.js`

And if for any reason you need to always load the latest available version in any major branch you can use:

`//cdn.jsdelivr.net/abaaso/latest/abaaso.min.js`

By using the `latest`

version you tell the server to load the absolute latest version it has. This of course is dangerous and given enough time may and will break your website. So use this feature with caution.

### Load multiple files with a single HTTP request

jsDelivr is the first CDN to support this kind of functionality. You can load multiple files using a single HTTP request. Similar to combining and minifying js files in your own server, but cached by the huge and smart network of jsDelivr.

All you have to do is to build your own URL with the projects and files you want to combine and their versions if needed. For example, to load the latest version for projects abaaso, ace and alloyui you would use the following syntax:

`//cdn.jsdelivr.net/g/abaaso,ace,alloyui`

Have in mind that loading the latest version is not recommended and given enough time will break your website. This is why you should specify the exact versions or use version aliases:

`//cdn.jsdelivr.net/g/jquery@2.1,angularjs@1.2`

So jquery@2.1 will load 2.1.0 and angularjs@1.2 will load 1.2.14. But the above URL will load the main files of each project and nothing else.

If you want to load multiple files from a single project then you can do the following:

`//cdn.jsdelivr.net/g/jquery@2.1,angularjs@1.2.14(angular.min.js+angular-resource.min.js+angular-animate.min.js+angular-cookies.min.js+angular-route.min.js+angular-sanitize.min.js)`

If you want to load CSS then select css files using the above format. If all files in the group URL have a .css extension then the server will automatically respond with a `Content-Type: text/css`

HTTP header. In all other cases (for /g/ URLs) `Content-Type: application/javascript`

is used.

Next you simply include the url in your website and you are done. Less DNS resolving, less TCP connections, less HTTP requests = Faster website.

You can even use this feature to offer your users a builder to allow them to generate a URL with the modules they need and then load them all using a fast CDN.

### A real API

jsDelivr has a fully featured API that can be used by developers in their websites,to create custom modules and anything else you might think of [https://github.com/jsdelivr/api](https://github.com/jsdelivr/api)

You can request exactly what you need using our API without downloading a huge package json. And it also supports cdnjs and Google. This way developers have everything they need to build their applications.

### Auto-Updates

[jsDelivr libgrabber](https://github.com/jsdelivr/libgrabber) is a utility that is going to run on our servers and can auto-update all hosted projects if configured. The best part is that the authors don’t have to change anything in their repos. All changes are made on jsDelivr side.

All you need is to create an update.json file with some basic info inside the project you want to keep auto-updated in jsDelivr repo. This file also supports multiple sources for new versions. Like npm, bower and directly Github repos. It is still under development but is planned to be released soon.

### Try it out, help out!

jsDelivr is a very interesting project that I enjoy developing and making better. It also heavily relies on the [help of the community](https://github.com/jsdelivr/jsdelivr/issues/397). Consider using it in your websites and host there your projects.

And if you are interested in helping out, we can always use some help, just join the conversation on [Github](https://github.com/jsdelivr/jsdelivr).

Feel free to leave your comments and ask me any questions you might have.

Thank you

## About
[
Dmitriy Akulov ](http://www.jsdelivr.com)

System administrator. In love with technology, high performance and fast web. Some times pretending to be a dev. Working for MaxCDN.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 37 comments

PetterMarch 19th, 2014 at 07:44Dmitriy AkulovMarch 19th, 2014 at 07:47Fabricio C ZuardiMarch 19th, 2014 at 09:01Dmitriy AkulovMarch 19th, 2014 at 10:00PetterMarch 19th, 2014 at 10:23Dmitriy AkulovMarch 19th, 2014 at 10:29AdarshMarch 19th, 2014 at 10:35Dmitriy AkulovMarch 19th, 2014 at 10:40PetterMarch 19th, 2014 at 17:12Paul IrishMarch 19th, 2014 at 14:00Steve SoudersMarch 19th, 2014 at 15:38PetterMarch 19th, 2014 at 17:06ChordsMarch 19th, 2014 at 10:53Dmitriy AkulovMarch 19th, 2014 at 10:56sokratisMarch 19th, 2014 at 11:34Dmitriy AkulovMarch 19th, 2014 at 11:49Steve SoudersMarch 19th, 2014 at 12:11Dmitriy AkulovMarch 19th, 2014 at 12:22Steve SoudersMarch 19th, 2014 at 12:35Dmitriy AkulovMarch 19th, 2014 at 12:45PetterMarch 19th, 2014 at 17:15Dmitriy AkulovMarch 19th, 2014 at 17:19Evan ProdromouMarch 19th, 2014 at 12:39Dmitriy AkulovMarch 19th, 2014 at 16:01AshMarch 19th, 2014 at 15:32Brett ZamirMarch 19th, 2014 at 17:23Dmitriy AkulovMarch 19th, 2014 at 18:07Niloy MondalMarch 19th, 2014 at 22:34Dmitriy AkulovMarch 20th, 2014 at 05:15Matt FreemanMarch 19th, 2014 at 23:37Dmitriy AkulovMarch 20th, 2014 at 05:47MarcelMarch 21st, 2014 at 04:04Dmitriy AkulovMarch 21st, 2014 at 07:51Per ØstergaardMarch 25th, 2014 at 08:24Dmitriy AkulovMarch 25th, 2014 at 09:47DanApril 9th, 2014 at 06:22Dmitriy AkulovApril 9th, 2014 at 07:41