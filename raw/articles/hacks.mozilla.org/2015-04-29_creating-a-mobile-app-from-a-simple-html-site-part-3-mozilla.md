---
title: 'Creating a mobile app from a simple HTML site: Part 3 – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2015/04/creating-a-mobile-app-from-a-simple-html-site-part-3/
author: Piotr Zalewa
published: '2015-04-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Adding a server to separate the app from its data

This is the third part in our series of posts about creating a dynamic mobile app from a simple HTML site. In [Part 2](https://hacks.mozilla.org/2015/04/creating-a-mobile-app-from-a-simple-html-site-part-2/) we separated the data from its visual representation, but the data is still contained inside the app. In this article, we take that data, remove it from the app altogether, and serve it from the server instead, to maximise reusability between different users.

We will go through the steps required to create a suitable server using NodeJS. Then we will make the app work as a client of this server.

If you have your code handy from last time, then you are ready to go. Make sure you have [NodeJS](https://nodejs.org/) installed. If you don’t have a previous code base setup you can follow the [instructions](https://github.com/zalun/school-plan-app/blob/master/README.md) on how to load any stage in this tutorial. Use stage5 as a starting point.

## Refactoring our code

Let’s quickly look at the [code created in part 2](https://github.com/zalun/school-plan-app/tree/master/stage5).

Two things happen in the `app.onDeviceReady`

method (see `js/index.js`

) — data is loaded from a JSON file and touch events are listened for on `<brick-deck id="plan-group">`

. After data is loaded, `app.renderData`

parses the JSON string and `app.createUI`

creates a UI for each plan separately.

`onDeviceReady`

and `createUI`

are currently not very efficient, so let’s update them. Let’s split `onDeviceReady`

by creating a new method called `activateFingerSwipe`

that will contain all the code after the `request.send()`

line and simply call it without arguments. Update your code as follows:

```
onDeviceReady: function() {
var request = new XMLHttpRequest();
request.onload = app.renderData;
request.open("get", "app_data/plans.json", true);
request.send();
app.activateFingerSwipe();
},
activateFingerSwipe: function() {
// Switching from one tab to another is done automatically
// We just need to link it backwards - change menu if slides
// changed without touching the menu
app.planGroupMenu = document.getElementById('plan-group-menu');
// Implementing one finger swipe to change deck card
app.planGroup = document.getElementById('plan-group');
var startX = null;
var slideThreshold = 100;
// ...
```


Now, let’s move on to updating `createUI`

. Instead of having the code to create the UI for each individual plan inside `createUI`

, we will create a new user-defined object type called Plan and instantiate it in the loop. Update `app.renderData`

to look like the block below:

```
renderData: function() {
var plans = JSON.parse(this.responseText);
var deck = document.getElementById('plan-group');
var tabbar = document.getElementById('plan-group-menu');
navigator.globalization.getDateNames(function(dayOfWeek){
for (var i = 0; i < plans.length; i++) {
var plan = new Plan(plans[i]);
plan.createUI(deck, tabbar, dayOfWeek);
}
}, function() {}, {type: 'narrow', item: 'days'});
},
```


We will define the `Plan`

type as an object having two methods — `createUI`

and `selectTab`

— which are copied from the existing methods and functions. The only changes are related to the data now having an object nature. Instead of `plan.week`

we use `this.schedule`

. `this`

always relates to the current plan’s scope. All changes related to storing parameters in the object are as follows:

`plan.title`

->`this.title`

`plan.week`

->`this.schedule`

`plan.id`

->`this.id`

`plan.active`

->`this.active`

`var tab`

->`this.tab`

`var card`

->`this.card`

`var table`

->`this.table`

`selectTab(deck, tab)`

->`this.selectTab(deck)`


At the top of your index.js file, add the following code:

```
function Plan(plan) {
this.schedule = plan.week;
this.title = plan.title;
this.id = plan.id;
this.active = plan.active;
this.tab = null;
this.card = null;
this.table = null;
};
Plan.prototype.selectTab = function(deck) {
var self = this;
function selectActiveTab() {
if (!self.tab.targetElement) {
return window.setTimeout(selectActiveTab, 100);
}
deck.showCard(self.tab.targetElement);
}
selectActiveTab();
}
Plan.prototype.createUI = function(deck, tabbar, dayOfWeek) {
// create card
this.card = document.createElement('brick-card');
this.card.setAttribute('id', this.id);
deck.appendChild(this.card);
//create tab
this.tab = document.createElement('brick-tabbar-tab');
this.tab.setAttribute('target', this.id);
this.tab.appendChild(document.createTextNode(this.title));
tabbar.appendChild(this.tab);
// link card and tab DOM Elements
this.card.tabElement = this.tab;
this.card.addEventListener('show', function() {
this.tabElement.select();
});
// create plan table
this.table = document.createElement('table');
var numberOfDays = this.schedule.length;
var cleanPlan = [];
for (var j = 0; j 0) {
cleanPlan.push(this.schedule[j]);
}
}
var daysInHours = [];
for (j = 0; j < cleanPlan.length; j++) {
for (var k = 0; k < cleanPlan[j].length; k++) {
if (!daysInHours[k]) {
daysInHours[k] = [];
}
daysInHours[k][j] = cleanPlan[j][k];
}
}
for (var j = 0; j < daysInHours.length; j++) {
var tr = this.table.insertRow(-1);
var td = tr.insertCell(-1);
td.appendChild(document.createTextNode(j + 1));
for (var k = 0; k < cleanPlan.length; k++) {
var td = tr.insertCell(-1);
if (daysInHours[j][k]) {
td.appendChild(document.createTextNode(daysInHours[j][k]));
}
}
}
var thead = this.table.createTHead();
var tr = thead.insertRow();
var th_empty = document.createElement('th');
tr.appendChild(th_empty);
var weekDayNumber;
for (var j = 0; j 0) {
var th = document.createElement('th');
th.appendChild(document.createTextNode(dayOfWeek.value[weekDayNumber]));
tr.appendChild(th);
}
}
this.card.appendChild(this.table);
if (this.active) {
this.selectTab(deck);
}
}
```


You can check your work against the full [refactored code source in github](https://github.com/zalun/school-plan-app/blob/master/stage5-refactored/js/index.js).

You might notice `var self = this;`

and then `deck.showCard(self.tab.targetElement);`

in `Plan.prototype.selectTab`

. `this`

in scope of `selectActiveTab`

would represent a different value then outside of it.

Read more about the [ new operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/new) and the


`this`

keyword on MDN if you want more information.## Building the server

Building a server using [NodeJS](http://nodejs.org) is fairly simple — `http`

is the only module required, although we will also include `fs`

(as we need to load the file from disk) and `sys`

(to display logs.)

We will place the server’s code into a separate directory (it’s named `stage6-server/`

in the related Github project) as it is not part of the app.

First of all, create a new directory in the same level as `school-plan`

called `server`

. Move the `plans.json`

file out from the `school-plan/www/app-data`

directory to the `server`

directory, then remove `school-plan/www/app-data`

. You could do these actions using the following terminal commands from `school-plan`

‘s parent directory:

```
mkdir server
mv school-plan/www/app_data/plans.json server/
rm -rf school-plan/www/app_data
```


Now onto the NodeJS server code. Create a new file called `server.js`

inside the `server`

directory, and fill it with the following content — this simply reads the file from disk:

```
var fs = require('fs'),
sys = require("sys");
fs.readFile(__dirname + "/plans.json", function (err, data) {
sys.puts(data);
});
```


Run it with the terminal command `node server.js`

— you should see the content of the `plans.json`

file listed in terminal.

Now we will serve this file using the `http`

module. Modify your NodeJS code like so:

```
var fs = require('fs'),
sys = require("sys"),
http = require('http');
http.createServer(function (request, response) {
fs.readFile(__dirname + "/plans.json", function (err, data) {
response.writeHead(200, {"Content-Type": "application/json"});
response.end(data);
sys.puts("accessed");
});
}).listen(8080);
sys.puts("Server Running on http://127.0.0.1:8080");
```


First we’ve created the server using the `http.createServer`

method and ordered it to listen on port `8080`

. On every single request, the `plans.json`

file is read and returned as an HTTP response. Then we simply log `accessed`

to the terminal.

Test your file again, as before.

Navigate to [http://127.0.0.1:8080](http://127.0.0.1:8080) using your browser and you should see the contents of the file inside the browser. (I use the [JSON View](http://jsonview.com/) add-on to make the code look nice too — it’s worth getting.)

So we’re able to serve the file from our machine — now we just need to read it in our app.

Note: The server is serving for any address – it works on http://localhost:8080 and also on your local network address (usually http://192.168.xx.xx:8080). This address should be used when testing the app on a device.


## Reading the data from the server

We need to change the app to read from the server instead of the file distributed inside the app. Let’s change the `request.open`

call (inside `deviceReady`

method) to read from the URL instead of the local file. Replace `app_data/plans.json`

with `http://127.0.0.1:8080`

, so it will look like this:

```
request.open("get", "http://127.0.0.1:8080", true);
```


Now for a test. Run the `cordova prepare`

command in the terminal, and reload the app in WebIDE.

You will receive an error in the browser console: *Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at http://127.0.0.1:8080/. This can be fixed by moving the resource to the same domain or enabling CORS.*.

### CORS, and cross-origin fixes

The error is due to a [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS) security policy preventing us from loading a script from a different domain.

There are two ways of loading a script from a different domain. Whitelisting it in Cordova is one of them, but as we’ve got control over the server, we can simply allow cross-site HTTP requests. This is done by setting a header call `Access-Control-Allow-Origin`

in the request. Its value is the domain name(s) that can request content from the server. As our app will be used on phones, all domains should have access. The needed headers are as follows:

```
"Access-Control-Allow-Origin": "*",
"Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
```


We will add these headers to the existing `Content-Type`

one specified in our `server.js`

script — update the `response.writeHead()`

call to the following:

```
response.writeHead(200, {
"Content-Type": "application/json",
"Access-Control-Allow-Origin": "*",
"Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"});
```


Save your NodeJs code, stop (`Control + C`

) the server running in your terminal, and run it again. The application should now be able to read from the server as desired.

If you are having problems getting the app to work, check your code for the [app](https://github.com/zalun/school-plan-app/tree/master/stage6) and [server](https://github.com/zalun/school-plan-app/tree/master/stage6-server).

## Serving and loading user plans

Currently we load all plans available in `plans.json`

. As we want to be able to serve plans for any user we need to identify and serve a set.

We will need to identify a plan. To find a plan in our “database” (JSON file) we will change the plan structure from array to object. For example:

```
{
"somehashtag": {
"title": "A",
"id": "a",
"active": 1,
"week": [
// ...
]
}, {
"otherhashtag": {
"title": "B",
"id": "b",
"week": [
// ...
]
}
```


We also need to find a way to store hashtags. Most of the users will have a different list of them. Should they be stored only on the device or on the server? Considering that many users change their phone fairly often, it’s best to keep the list of hashtags on the server. In production we would have separate user accounts, but for the sake of this tutorial and the simplicity of the server’s code no security is provided.

We again need to modify the JSON file, to allow for different users and separate plans:

```
{
"users": {
"userA": {
"name": "John Doe",
"plans": ["somehashtag", "otherhashtag"]
},
// ...
},
"plans": {
"somehashtag": {
"title": "A",
"id": "a",
"active": 1,
"week": [
// ...
]
}, {
"otherhashtag": {
"title": "B",
"id": "b",
"week": [
// ...
]
}
}
```


From now on, `data.plans`

will represent all plans and `data.users`

will represent all of the users.

At this point, download the updated [plans.json](https://github.com/zalun/school-plan-app/blob/master/stage7-server/plans.json) file from Github, and replace old with new.

I defined the URL to access a user’s plans as follows:

`http://{address}/plans/{userid}`


Reading URLs is easy with the `url`

module — now you should add it to the loaded modules:

```
var fs = require('fs'),
sys = require("sys"),
http = require('http'),
url = require('url');
```


Now remove the current `response.end();`

and sys.puts() calls, replacing them with:

```
var args = url.parse(request.url).pathname.split('/');
var command = args[1];
var data = JSON.parse(data);
if (command === 'plans') {
// get user from data.users
var userid = args[2];
var user = data.users[userid];
var plans = [];
var i, hashtag;
for (i = 0; i < user.plans.length; i++) {
hashtag = user.plans[i];
// copy each user's plan to plans
plans.push(data.plans[hashtag]);
}
response.end(JSON.stringify(plans));
sys.puts("accessed user - " + userid);
}
```


The only change in the app’s usage now is that we can load the data for different users using the new URL scheme:

`http://127.0.0.1:8080/plans/someuser`


Go to your index.js file and update the following:

`request.open("get", "http://127.0.0.1:8080/", true);`


to

`request.open("get", "http://127.0.0.1:8080/plans/johndoe", true);`


## Conclusion

We have now provided a way to display different plans for different users. However, we are still downloading the plans every time the app is used, which is not much good for an offline experience, plus we currently can’t change the plans displayed unless we edit the XHR call in the code itself. We’ll tackle these problems in our next article.

For now, check out the final code for the [app](https://github.com/zalun/school-plan-app/tree/master/stage7) and [server](https://github.com/zalun/school-plan-app/tree/master/stage7-server). And look out for Part 4, coming in May!

## About Piotr Zalewa

Piotr Zalewa is a Senior Web Developer at Mozilla's Dev Ecosystem team. Working on web apps. He is the creator of JSFiddle.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 4 comments

jensApril 30th, 2015 at 03:00Chris MillsApril 30th, 2015 at 03:19DanielMay 5th, 2015 at 14:00Piotr ZalewaMay 5th, 2015 at 14:26