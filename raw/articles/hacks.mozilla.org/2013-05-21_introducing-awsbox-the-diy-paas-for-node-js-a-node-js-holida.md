---
title: Introducing AWSBOX, the DiY PaaS for Node.JS – A Node.js holiday season, part
  12 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/05/introducing-awsbox-the-diy-paas-for-node-js-a-node-js-holiday-season-part-12/
author: Mozilla
published: '2013-05-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is episode 12, out of a total 12, in the

[A Node.JS Holiday Season series]from Mozilla’s Identity team. It’s the last part, and covers awsbox.

Once you’ve written a server in Node.js, how do you deploy it?

Instead of using a pre-existing “Platform as a Service” (PaaS) provider, the [Identity team at Mozilla](http://identity.mozilla.com/) chose to build custom infrastructure atop [Amazon EC2](http://aws.amazon.com/ec2/), and we’d like to tell you more about it.

Meet [awsbox](https://github.com/mozilla/awsbox), a minimalist PaaS layer for Node.js applications that’s currently handling nearly two dozen of the non-critical services that we support.

Awsbox was designed to deliver simple, PaaS-style deployment without sacrificing the flexibility of custom infrastructure.

## Using awsbox

In order to deploy a Node.JS project with awsbox, you must make some tiny changes to your application, provide your amazon credentials in the environment, and then you can deploy via the command line.

In terms of app changes, you must:

- Create an
`.awsbox.json`

file that specifies how to start the server. - add
`awsbox`

as a dependency in your`package.json`

- ensure your server binds to the port specified in the
`PORT`

environment variable

To provide your amazon credentials, you must set `AWS_ID`

and `AWS_SECRET`

in your environment, two values which you can obtain through the [amazon management console](http://aws.amazon.com/console/).

With the initial application configuration complete, you can `npm install`

which will install awsbox, and you’re ready to create your first server:

```
$ node_modules/.bin/awsbox create -n MyFirstAWSBOX
reading .awsbox.json
attempting to set up VM "MyFirstAWSBOX"
... VM launched, waiting for startup (should take about 20s)
... Instance ready, setting human readable name in aws
... name set, waiting for ssh access and configuring
... public url will be: http://
```
... nope. not yet. retrying.
... victory! server is accessible and configured
... applying system updates
... and your git remote is all set up
... configuring SSL behavior (enable)
Yay! You have your very own deployment. Here are the basics:
1. deploy your code: git push MyFirstAWSBOX HEAD:master
2. visit your server on the web: http://
3. ssh in with sudo: ssh ec2-user@
4. ssh as the deployment user: ssh app@

The final step to deploy your application is to `git push`

:

```
$ git push MyFirstAWSBOX HEAD:master
```

And now your Node.JS application is hosted and running on an EC2 instance. At this point, you’ve spent about twenty minutes with awsbox. You’ve made minimal changes to your application. You’ve deployed a new server and gotten your application up and running in EC2. Finally, you’ve got an easy way to push changes that fits within your existing workflow (you just `git push`

to a remote).

Now that you have a feel for how you use awsbox and the basic features it provides, let’s take a step back and look at what it actually is and how it works.

## awsbox is … A Minimalistic Contract

Any hosting environment has certain expectations of the application that it will be running, *the contract*. For awsbox this contract includes the following:

**What process(es) should be run** are specified by the app in `.awsbox.json`

. At its simplest, the file may look like this:

```
{
"processes": [ "path/to/myprocess.js" ]
}
```

**What software must be installed** is specified by the app in `package.json`

.

**Which port to contact the server** is delivered to the app via the `PORT`

environment variable.

In building awsbox, a main goal was minimal invention, to make it easy to “port” an existing application.

## awsbox is … A Machine Image

During the process of creating an instance, awsbox creates a machine instance from an “Amazon Machine Image”, which results in a running server that’s ready to accept your node.js application, install its dependencies, and run it. The image is built from the [Amazon Linux AMI](http://aws.amazon.com/amazon-linux-ami/) which is a custom linux distribution provided by amazon, and has access to popular rpm-based package repositories via [yum](http://en.wikipedia.org/wiki/Yellowdog_Updater,_Modified). The ID of awsbox AMI is referenced in the `awsbox`

javascript library.

This image is *pre-configured with multiple user accounts*. `ec2-user`

is an account that has sudo access to the machine. `proxy`

is an account that hosts an [HTTP reverse proxy](http://en.wikipedia.org/wiki/Reverse_proxy) that with a [few steps](https://github.com/mozilla/awsbox/blob/master/doc/HOW_DO_I.md#how-do-i-enable-ssl) can serve as an SSL terminator to let you support HTTPS without modifying your application. Finally, the `app`

user is the account that hosts all of your application code, your server logs, the server based git repository that you push to, and the [git post-commit hook](https://www.kernel.org/pub/software/scm/git/docs/githooks.html) responsible for installing dependencies and starting your server after you push.

## awsbox is … Command Line Tools and Libraries

At the time you `npm install`

awsbox, a collection of javascript libraries and a command line tool are installed locally. The command line tool gives you a much faster way to deploy servers than available through Amazon’s web console, and handles most of the complexity of creating an instance in EC2 that is ssh and web accessible.

The `awsbox`

command line tool also provides many command line *verbs* to perform basic administration of your awsbox, which can be listed with `node_modules/.bin/awsbox -h`

.

The most interesting verb is `create`

, which actually creates a virtual machine.

## awsbox is … A Pile Of Features and Hooks

Finally, any non-trivial server requires more than just a Node.JS service. To support the unknown awsbox allows you to [specify yum packages that should be installed](https://github.com/mozilla/awsbox/blob/master/doc/JSON.md#packages-optional) at instance creation time. For more custom configuration you have two options:

**SSH in and do whatever you need to**: The goal of awsbox is to let you move as fast as possible, and sometimes the most expedient way to get a new instance of a service up is to perform required steps manually and write a README. But a more repeatable solution is available…

**Write scripts to automatically configure software for you**: Awsbox has the [notion of hooks](https://github.com/mozilla/awsbox/blob/master/doc/JSON.md#remote_hooks-optional), which occur at various stages of instance creation or deployment. Using these hooks, it’s possible to

[configure mysql](https://github.com/mozilla/browserid/blob/4971e83b897829d866f99c0e398d52a7b3b9ec2b/scripts/awsbox_remote/post_create.sh),

[install redis manually](https://github.com/mozilla/restmail.net/blob/44306506b1a33ed3c1fbc1b61f13b8d557b80141/aws_scripts/post_create.sh), or do whatever you need to in order to get your service running.

# Is awsbox for Me?

Having a single consistent mechanism of deploying non-critical services has been an incredible efficiency benefit for our team. *Collaboration is easier* when you have a simple and well defined contract between application and environment. *Diagnosis of issues* is faster when you have a consistent set of deployment conventions. Finally, *moving from experiment to production environment is less costly* when an application has all of its dependencies explicitly expressed.

If you are looking for a deployment solution for your own experimental Node.JS services, give the ideas and design of awsbox a careful look.

## Previous articles in the series

This was part twelve in [a series with a total of 12 posts about Node.js](https://hacks.mozilla.org/category/a-node-js-holiday-season/as/brief/). The previous ones are:

[Tracking Down Memory Leaks in Node.js](https://hacks.mozilla.org/2012/11/tracking-down-memory-leaks-in-node-js-a-node-js-holiday-season/)[Fully Loaded Node](https://hacks.mozilla.org/2012/11/fully-loaded-node-a-node-js-holiday-season-part-2/)[Using secure client-side sessions to build simple and scalable Node.JS applications](https://hacks.mozilla.org/2012/12/using-secure-client-side-sessions-to-build-simple-and-scalable-node-js-applications-a-node-js-holiday-season-part-3/)[Fantastic front-end performance Part 1 – Concatenate, Compress & Cache](https://hacks.mozilla.org/2012/12/fantastic-front-end-performance-part-1-concatenate-compress-cache-a-node-js-holiday-season-part-4/)[Building A Node.JS Server That Won’t Melt](https://hacks.mozilla.org/2013/01/building-a-node-js-server-that-wont-melt-a-node-js-holiday-season-part-5/)[Fantastic front-end performance, part 2: caching dynamic content with etagify](https://hacks.mozilla.org/2013/02/fantastic-front-end-performance-in-node-part-2-a-node-js-holiday-season-part-6/)[Taming Configurations with node-convict](https://hacks.mozilla.org/2013/03/taming-configurations-with-node-convict-a-node-js-holiday-season-part-7/)[Fantastic front end performance, part 3 – Big performance wins by optimizing fonts](https://hacks.mozilla.org/2013/03/fantastic-front-end-performance-part-3-big-performance-wins-by-optimizing-fonts-a-node-js-holiday-season-part-8/)[Localize Your Node.js Service, part 1 of 3](https://hacks.mozilla.org/2013/04/localize-your-node-js-service-part-1-of-3-a-node-js-holiday-season-part-9/)[Localization community, tools & process, part 2 of 3](https://hacks.mozilla.org/2013/04/localization-community-tools-process-part-2-of-3-a-node-js-holiday-season-part-10/)[Localization in Action, part 3 of 3](https://hacks.mozilla.org/2013/04/localization-in-action-part-3-of-3-a-node-js-holiday-season-part-11/)

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 3 comments

sam dlgMay 21st, 2013 at 14:18Lloyd HilaielMay 21st, 2013 at 14:33MunimMay 22nd, 2013 at 02:00