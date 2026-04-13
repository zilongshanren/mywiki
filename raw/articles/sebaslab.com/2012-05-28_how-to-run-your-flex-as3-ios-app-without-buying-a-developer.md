---
title: How to run your Flex/AS3 iOS App without buying a developer license
url: https://www.sebaslab.com/run-flas-application-iphone-buying-developer-license/
author: Sebastiano Mandalà
published: '2012-05-28'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

So, I wanted to experiment with actionscript, flex and iPhone, but I do not have a mac and I am not really keen to pay 99$ just to make some plain experiments; besides I have not intention to make a living out of it, so I do not think it was really a good investment right now.

So I wondered, are there alternatives?

Yes there are and the one I found involves a[ jailbroken iPhone](http://en.wikipedia.org/wiki/IOS_jailbreaking), which seems to be not illegal (and it makes a lot of sense), [flashdevelop](http://www.flashdevelop.org/), adobe air SDK 3.2 (that is downloaded automatically with flashdevelop), a [fake mobile provision ](http://www.instructables.com/id/How-to-use-Adobes-iPhone-Packager-without-an-Appl/step2/Exporting-the-App/)(this could be borderline) and this nice app: [i-FunBox](http://www.i-funbox.com/)

it is very simple. You need to create a *flashdevelop* project using the air mobile template (do not worry if there is the android icon, it works for iOS too), add your actionscript code and make it compile. If you have problems running it (especially if you want to use the new air 3.2 features), these are my two tips: edit the application.xml file and change the air version from 3.1 to 3.2 and add the line -swf-version=15 to the compiler options.

Once your application compiles, follow the flashdevelop instructions reading the file AIR_iOS_readme.txt that you can find inside the project structure. Once the fake certificate and provisioning file are copied, just set the right path where asked to.

Now you are just ready to build your first ipa with flash develop; it is as easy as run the PackageApp.bat file.

Good! You should have your ipa now. Next step is just to upload it on the iPhone. In order to do it I decided to use i-funbox. I do not even know if it is possible to do it with iTunes since I did not even try (you need to have it installed though), but uploading it was a piece of cake. If your iPhone has been just jailbroken, remember that you need to install [Cydia](http://cydia.saurik.com/) before to use i-funbox.

Few second after I had a new application with an air icon that ran right away. My first [Starling](http://gamua.com/starling/) application was already on the screen exploiting the new stage3D feature as well. Enjoy 😉

By the way: buy your developer license if you want to upload the application on appstore 😀


1 million times thanks. I was looking for those fake mobile provisions that I found here.