---
title: Network Activity and Battery Drain in Mobile Web Apps – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2015/04/network-activity-and-battery-drain-in-mobile-web-apps/
author: Scott Anecito
published: '2015-04-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s note:** *This post describes the work of a group of students from Portland State University who worked with Mozilla on their senior project. Over the course of the last 6 months, they’ve worked with Mozillian Dietrich Ayala to create a JavaScript library that allows developers to optimize the usage of network operations, thus saving battery life. The group consists of 8 students with varied technology backgrounds, each assigned to take on a different task for the project. Congratulations to the team:*

[Ryan Niebur](https://www.linkedin.com/in/ryanniebur)– Team Lead / Meeting Owner[Nathan Kerr](https://github.com/TheBosZ/)– Architect / Software Developer[Tim Huynh](https://github.com/huynt553)– Scribe / Battery Tester / Software Developer[Bin Gao](https://github.com/gaobin1019)– Software Developer[Brianna Buckner](https://github.com/askore)– DevOps / Software Developer[Sean Mahan](https://github.com/sean97140)– Battery Tester / Software Developer[Scott Anecito](https://www.linkedin.com/in/scottanecito)– Documentation / Software Developer[Casey English](https://github.com/razanur37)– Battery Tester / Software Developer

## Overview and Goals of the Project

The goal of our senior Capstone project was to develop a JavaScript library to make it easier for developers to write applications that use less power by making fewer network requests. In emerging markets, where battery capacities in mobile devices may be smaller and signal strength may be poor, applications that make many requests create serious challenges for the usability of smartphones. Sometimes, applications designed for users in regions with robust network infrastructure can create significant negative effects for users with less reliable access. Reducing battery drain can provide better battery life and better user experiences for everyone. To improve this situation, we’ve created APIs that help developers write mobile applications in a way that minimizes network usage.

In order to solve this problem effectively, we provide developers with mechanisms to delay non-critical requests, batch requests together, and detect when the network conditions are best for a given activity. This involved doing research to determine the efficacy of various solutions. Regardless of the effectiveness of our APIs, this research provides insight into saving battery usage. In addition to our research, we also focused on the developer ergonomics, hoping to make this easy for developers to use.

**Installation & Usage**

Installation of the library is simple: clone the [“dist” folder](https://github.com/askore/capstone2014-firefoxOS/tree/master/dist) and choose the library variant that best suits your needs. [LocalForage](https://github.com/mozilla/localForage) is used in the library for storing the statistical details for each [XMLHttpRequest](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest) (XHR). This way the developer can perform analysis to develop a set of dynamic heuristics such as utilizing when the user is most likely to make successful XHRs. However, if this is something you do not think will be commonly used, you can opt for a LocalForage-free version to get a smaller library memory footprint.

We encourage you to check out our [General Usage section](https://github.com/askore/capstone2014-firefoxOS#general-usage) and [API Usage section](https://github.com/askore/capstone2014-firefoxOS#api-usage) to get a comprehensive idea of usage and context. A brief overview of how to use the core functions of the APIs is provided.

**Critical Requests**

When you need to make a critical XHR for something that the user needs right away, you make it using the following syntax:

`AL.ajax(url [, data] [, success] [, method])`


Where `url`

indicates the endpoint, data is the parameter you pass JSON data to (i.e., POST XHR), success is called after the request has completed successfully, and the optional method parameter specifies the HTTP method to use (e.g. Patch, Post). If method is not specified, and the data field is null, GET will be used, but if data is used, POST will be the default.

A sample critical request would look like this:

```
AL.ajax('http://rocky-lake-3451.herokuapp.com/', {cats: 20}, function(response, status, xhr) {
console.log('Response: ', response);
console.log('Status: ', status);
console.log('Xhr: ', xhr);
});
```


This code when executed would result in the following output:

```
Response: {"request_method":"POST","request_parameters":[]}
Status: 200
Xhr: XMLHttpRequest { readyState=4, timeout=0, withCredentials=false, ...}
```


**Non-Critical Requests**

Non-critical requests are used for non-urgent needs and work by placing the non-critical XHR(s) in a queue which is fired upon certain conditions. The two default conditions are ‘battery is more than 10% and a critical request was just fired’ or ‘battery is more than 10% and the device is plugged in to a power source’. The syntax for making a non-critical request is the same as a critical one, with the exception of the function name and an additional parameter, timeout:

`AL.addNonCriticalRequest(url [, data] [, success] [, method] [, timeout])`


Here’s how timeout works: given a number of milliseconds, the XHR added (and all other XHR in the queue) will fire off if the queue is not already fired off by some other mechanism such as a critical request firing.

**Recording & Analysis**

XHRs are stored within LocalForage. There are a variety of functions to either retrieve the data or trim it. General retrieval syntax is in this format, where callback is an array of XHR-related objects that contain data relevant to the XHR such as start time, end time, and size of the request.

`AL.getHistory(callback)`


You can use this data in all manner of interesting ways, but at a basic level you’ll want to time the XHRs. Calculate the difference between start time and end time of the request for the five most recent requests by doing the following:

```
function getRecords() {
var elem = document.getElementById('recordsList');
AL.getHistory(function (records) {
if (records) {
var counter = 0;
var string = [];
for (var i = Math.max(records.length - 5, 0); i < Math.max(records.length, 0); ++i) {
string[counter] = records[i].end - records[i].begin;
++counter;
}
elem.innerHTML = string.toString();
}
else {
console.log("Records is null");
}
});
}
```


## Research Findings

In order to gather data about the effectiveness of our APIs on reducing battery usage, we hooked up our reference device ([a Flame](https://developer.mozilla.org/en-US/Firefox_OS/Phone_guide/Flame)) to a battery harness and used our demo app to process 30 requests of various different types of media (text, images, and video). All three tests were run on a WiFi network (our university’s WiFi network, specifically). We attempted to run all three tests on a 3G (T-Mobile) network, but due to poor connectivity, we were only able to run the text test over a cellular network.

When running the tests on WiFi, we noticed that the WiFi chip was extremely efficient. It would turn on almost instantly and once all network requests were done, it would turn off just as quickly. Because of this, we realized that the library is not very useful when on a WiFi network; it is hard to be more efficient than instant on/off.

When testing on a 3G network however, it became very apparent that this library could be useful. On the graph of power consumption, there is a very clear (and relatively slow) period where the chip *warms up*, increasing its power usage gradually until it is fully powered. Once all network activity is complete, there is an even longer period of *cool down*, as the power draw of the chip gradually declines. It is clear that stacking the requests together is useful on this type of network to avoid *dead periods*, when the phone is powering down the chips due to lack of activity just as another request comes in, causing chips to be powered back up again at the same slow rate.

![Text over WiFi](../../assets/0085090be6e98675.png)


![Text over WiFi](../../assets/0085090be6e98675.png)

Screen turned on around 2 seconds, 30 XHMLHttpRequest burst sent from roughly the 6 second mark to the end of the graph (~13.5 second mark)

![Text over 3G](../../assets/e5185e41869a8749.png)


![Text over 3G](../../assets/e5185e41869a8749.png)

Screen turned on around 2 seconds, 30 XHMLHttpRequest burst sent from roughly the 2 second mark to roughly the 18 second mark

In conclusion, we believe our library will prove useful when the cellphone is using a 3G network and will help conserve battery usage for requests that are not immediately necessary. Furthermore, the optional data analytics backbone can help advanced developers generate unique heuristics per user to further minimize battery drain.

![Portland State University Firefox OS Capstone Team](https://hacks.mozilla.org/wp-content/uploads/2015/04/image12-500x375.jpg)


![Portland State University Firefox OS Capstone Team](../../assets/6c4ba7794924c51f.jpg)

Portland State University Firefox OS Capstone Team: Back row: Tim Huynh, Casey English, Nathan Kerr, Scott Anecito. Front row: Brianna Buckner, Ryan Niebur, Sean Mahan, Bin Gao (left to right)