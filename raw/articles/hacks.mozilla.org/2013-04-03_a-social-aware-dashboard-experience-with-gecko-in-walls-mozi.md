---
title: A Social-aware Dashboard Experience with Gecko in Walls – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/04/a-social-aware-dashboard-experience-with-gecko-in-walls/
author: Marcio Galli
published: '2013-04-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This article covers a Web project that rethinks how TV appliances can be used in public spaces for real-time content and interaction with social networks. Tela Social is a powered by Mozilla system application that runs in Linux appliances and creates a visual experience that presents custom and interactive content with real time data using the Web. It’s different of a standard kiosk and far from the personal browser experience because it’s not tailored for an individual. Instead, it explores how online data can be used to provide impact to users in common areas. In the following sections, you will read about the general system’s architecture; a special focus is given to how CSS3 and JavaScript is used to support the user experience with engaging animated effects.

## First, boot to the Web

The application starts following the Linux system’s reboot. A monitor process is launched and starts to check whether the Gecko-based client is running or not. If not running, it starts the main process: a Gecko-based single window browsing engine with no toolbars in full screen.

The following image shows an overview of the web stack infrastructure that is launched. The web application sits above the engine in a similar way to applications such as Firefox or other [Powered by Mozilla](http://www.mozilla.org/projects/powered-by.html) apps using Gecko.

![Gecko architecture overview](../../assets/e099b9ab7600b8af.png)


## Online and Offline

Instead of loading a remote web page, most of the resources are loaded from a local web server written in JavaScript using NodeJS — [TelaSocial Mediator](https://github.com/taboca/TelaSocial-Mediator). This system is also monitored in order to reduce problems in the case of script execution failures.

Once the web app comes from a local web server, a main HTML layout may bring inner HTML components that are loaded within iframes. This degree of separation exists to help developers to create isolated components in a standard test environment: all the components are made of plain pages. As part of this project, an experimental project script was created to help developers to quickly deploy new grid layouts — [Gridtype.JS](https://github.com/taboca/TelaSocial-Grid-Type) can take strings as arguments and can generate a grid layout that is tableless. The following example shows how to generate a grid of DIVs:

```
grid('abcdabee',4);
```

The above “string” specification will generate the following layout:

![Layout design](../../assets/389327099812b6a0.png)


## Free of pop-ups or unwanted desktop interfaces

There are many systems using online data to display information in TV appliances. Some of these systems are applications launched on top of the operating system graphic user interface. The following photos were taken from airports in 2012 in Brazil. These are a few of many examples of problems with unwanted user interface elements that are displayed on top of systems using operating system desktops. For this reason, and also the principle of simplicity and cost reduction, the designed approach was to launch Gecko from the basic X Window infra structure. Such approach ensures that no other visual applications are running at the same time, thus creating an improved quality experience without those unwanted pop-ups.

![Picture shows an Operating System update pop up which is common in airports in Brazil](../../assets/567b07bb3efd9bc3.jpg)


![Picture shows an Operating System update pop up which is common in airports in Brazil](../../assets/91dd645a060fdcdd.jpg)


## Routing Gecko pop-ups into frames

While OS desktop pop-ups are out of the scene, yet there are some conditions where Gecko used to display pop-ups to alert the user. The solution to this problem was to use Gecko’s preferences API and ask Gecko to display network error messages inline. With this, all errors are displayed in the iframe which is great because it is possible to track the errors and signal application logic outside the Gecko process. As an example, we can monitor the output console and change the layout depending on network error conditions. So, for example, if a weather channel frames brings a network error, the system should be able to launch an alternate layout.

## Animation library with zoom and pan

The above elements are essential to keep the level of quality that is expected in enterprise environments. With this functional base, it’s when things can be creative and the web developer mindset rules. HTML5 and modern effects, provided by CSS3, can be used to help understand and improve the user experience in this scenario that is not the same of a desktop or a mobile.

To help the creation of content, a small JavaScript library was also produced as part of this project. The main goal of this library is to help the creation of visual narratives out of HTML pages. [The TagVisor library](https://github.com/taboca/TagVisor/) reads a list of <li> elements which tells how CSS3 and other transformation effects are applied with time-referenced data:

The above script dispatches transformation functions that can modify the document using JavaScript for DOM transformations and DOM style changes that will take care of the visual effects. These effects are common in many systems, including well known JS-based solutions such as Impress.JS. However TagVisor comes with tailored functions that are very important for the scenarios in digital signage. One difference is that the script allows modifications to be performed within iframes which is good for cases where many separated HTML resources are loaded in a grid arrangement.

The zoom and animation metaphor does a lot of the heavy work to ensure a level of smoothness in animation which is expected by users in front of a TV panel. Some effects can also be combined in time in order to produce engaging visual narratives as shown in the [TagVisor video demonstration](http://labs.telasocial.com/tagvisor-demo).

## Web-driven, for adaptation

User experience is of major importance and a main reason for the use of a web-based infrastructure. Such model brings a level of dynamism supporting organisations who can tailor the system with custom data-sources using web services formats such as JSON or RSS. This approach has allowed us to test the screens with a variety of online sources; and to learn how the stream of web events can impact users in local organisations.

The following videos are examples of systems with Tela Social. The first video refers to the system at a major science park in Brazil ([Press release in Portuguese](http://www.pti.org.br/imprensa/noticias/pti-lanca-ferramenta-de-comunicacao-interna-digital)). It’s an example with a variety of content areas that are tied to a variety of sources: from journalists to editors plus open channels using social networks. The second video shows an example where the TV appliance is set in vertical position.

People recognise that using data from events plus local interest content can build local participation. For most people, TV content is something far away and not tailored to their local community interests. To make things different, we have even used TVs in the vertical position to make a point that the whole experience was flipped and that content and interaction is bottom up.

The objective of the project is to develop web-based solutions that can be useful in spaces and bring social-aware experiences that are positive to local communities . While social features can be used in the mobile and on desktop, we believe that our approach can help communities because it extends the physical environment — it creates a social reflection to the environment. It’s a chance for custom web experiences that build awareness about contributions made by local communities and real-time data of interest. This approach also explores challenges in user interfaces since it engages people to interact in new ways: it’s not a direct touch like standard kiosks. It’s the web in the first place and opportunities for interaction are explored based on live data.

## About
[
Marcio Galli ](http://www.telasocial.com)

Long time Mozilla contributor Marcio Galli is the founder of TelaSocial, a social-aware kiosk system powered by Mozilla. Marcio is an entrepreneur and uses this project to push the good parts of the Web into public and semi-public spaces. Marcio is category ( Best Open Web Hack ) winner of the Mozilla + MacArthur Foundation "Jetpack for Learning" competition / Austin Texas and was priorly winner of a mobile contest for the early mobile apps effort from Mozilla. Before working on TelaSocial marcio worked for Mozilla Labs Chromeless, Mozilla Joey, Mozilla Minimo and Marketing in Brazil. Marcio provided contributions to Mozilla since 2000 when we was hired by Netscape to become a technology evangelist for Gecko engine. Where TelaSocial crosses with mozilla? TelaSocial uses Gecko as a solution for communication in display appliances in enterprise environment. Visit http://www.telasocial.com

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.