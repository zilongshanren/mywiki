---
title: 'awsbox, a PaaS layer for Node.js: An Update on Latest Developments – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/10/awsbox-a-paas-layer-for-node-js-an-update-on-latest-developments/
author: Andrew Chilton
published: '2013-10-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is the 2nd time we’ve talked about

[awsbox]on the Mozilla Hacks blog. In the first article we gave you[a quick introduction to awsbox]as part of the[Node.js Holiday Season]set of articles. Here we’d like to tell you about some recently added features to awsbox.

To briefly recap, awsbox is a minimalist PaaS layer for Node.js applications which is built on top of [Amazon EC2](http://aws.amazon.com/ec2/). It is a DIY solution which allows you to create instances, setup DNS, run application servers, push new code to and eventually destroy your instances in a matter of minutes.

Since we first released awsbox it’s usage has been steadily increasing and is now downloaded from npm over 3,000 times every month. This has blown away our initial expectations so perhaps we’ve plugged a gap between the ‘Infrastructure’ and the ‘Platform’ services currently available.

### Aim of awsbox

The aim of awsbox is to be an easy to use but configurable abstraction on top of the Amazon APIs to create your own PaaS solution. However, it should also allow you to do more than a PaaS service does – but only if you want to.

With that in mind, we have added a number of new features recently which allows you to take more control of your deployments. In general we’re aiming for speedy setup of development environments which can help quicken the process of development rather than for production deployments (but that doesn’t mean awsbox couldn’t be battle hardened more for this either).

### New Features

Nginx is now being used as the reverse proxy to your application. Since your webserver is run by an unprivileged user on the box (ie. the ‘app’ user) we need a way to listen on port 80 or 443 and proxy through to your app. Whilst this job was admirably done in the past with http-proxy (on npm) we decided Nginx would compliment awsbox more now and in the future. Having the ability to drop config files into Nginx means we can start to add more features such as multiple webservers, multiple apps or serving from multiple subdomains.

Another new feature is the ability to automatically point a subdomain to your instance using Route53. By congregating around another AWS service rather than a separate service means we only have to worry about having one set of credentials in your environment. Subdomain creation and deletion is automatically performed whenever you create or destroy an instance using awsbox and this helps keep things clean.

Some of our team work in Europe as well as North America and a few of us are on the other side of the world. Instead of taking our requests half way around the world to our instances, we decided to bring our instances to us. Our base AMI which used to live only in the ‘us-east-1’ region is now available in all AWS regions and that includes both ‘eu-west-1’ for our European contingent and ‘ap-southeast-2’ too. Being able to create an instance in Sydney makes me very happy. :)

With so many people constantly creating, re-using and destroying instances we also thought it would be fair to be able to search for any instance with whatever criteria. As well as being able to list all VMs you can now find them by IP Address, AMI, Instance Id, Name, Tags or in fact any of 12 different criteria. This makes it super easy to find the instance you’re looking for.

And finally … no-one likes to spend any more money than they need to, so we now have the ability help figure out who launched which instance (so we can ask them if we can terminate it!). The AWS_EMAIL env var is added as a tag to the instance upon creation so that we know who to chat to if we need to reduce our bill.

### New Commands

With these recent architectural changes we’ve also added a number of extra commands to help you with managing both your instances and your DNS. Now that we’re multi-region, there are a few new commands related to that:

```
# lists all AWS regions for EC2
$ awsbox.js regions
# lists all regions and their availability zones
$ awsbox.js zones
```

We can also now list all of our domains and their subdomains in Route53 as well as being able to search which records

point to an IP Address:

```
# lists all domains in Route53
$ awsbox.js listdomains
# lists all resource records in this zone
$ awsbox.js listhosts example.com
# find which subdomains/domains point to an ip address
$ awsbox.js findbyip 1.2.3.4
# delete this subdomain
$ awsbox.js deleterecord sub.example.com
```

To help with AMI management, there is now a command which helps you create an AMI from an existing instance, tidies it up, creates an AMI and then copies it to all of the other available regions:

```
# create an ami and copy to all regions
$ awsbox.js createami ami-adac0de1
```

And finally a few commands which can help with determining who owns which instance:

```
# search instance metadata for some text
$ awsbox.js search 1.2.3.4
$ awsbox.js search ami-adac0de1
$ awsbox.js search persona
# show meta info related to an instance
$ awsbox.js describe i-1cec001
# claim an instance as your own
$ awsbox.js claim i-b10cfa11
# list all unclaimed instances
$ awsbox.js unclaimed
```

These are all in addition to the existing commands which now total 21, all to help manage your own deployments.

### The Future

There has been a small renaissance in awsbox development recently with many people chipping in with new features. It is a valuable tool for the [Persona](https://developer.mozilla.org/en-US/docs/mozilla/persona) team since it enables us to stand-up instances rather quickly, have a poke around either informally or formally and throw them away as quick as we created them (if not quicker)! And we don’t have to feel guilty about this either since acquiring a server on demand is par for the course in these days of IaaS.

We’ve also congregated around using more services within AWS itself. By moving the backend AWS API library to [AwsSum](http://awssum.io/) we’re now able to talk to more AWS services than before and hopefully can leverage these to help make development deploys quicker and easier too.

However, we also feel that awsbox can get better still. We have some ideas for the future but we always welcome ideas or code from you guys too. Feel free to take a look around the docs and issues and leave a comment or two. If you’ve got great code to go with those ideas then we’ll be happy to review a pull request too – after all [awsbox](https://github.com/mozilla/awsbox) is open source.

## About
[
Andrew Chilton ](http://chilts.org)

Andy currently works on Persona in the Identity team at Mozilla. He loves Node.js, Web APIs, async and *aaS (Whatever as a Service). He wrote [AwsSum](http://awssum.io/), a set of Node.js libraries for every AWS API and also releases [a fair few modules](https://npmjs.org/~chilts) to npm too. Andy also runs the

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

Mirco ZeissOctober 17th, 2013 at 03:06Andrew ChiltonOctober 17th, 2013 at 04:29