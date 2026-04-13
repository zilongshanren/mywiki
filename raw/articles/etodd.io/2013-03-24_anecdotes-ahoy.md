---
title: Anecdotes ahoy
url: https://etodd.io/2013/03/24/anecdotes-ahoy/
published: '2013-03-24'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Anecdotes ahoy

A smorgasbord of anecdotes carefully compiled just for you, dear reader. This is #2 in a series of three posts which were originally one, before I decided I just had too dang much to say.

## OpenStack

I spent a few weeks at work building a fully operational ~~death star~~ OpenStack cluster. What does that mean? Basically, we have our own little private version of Amazon Web Services. We can create virtual machines, virtual hard drives, even virtual IP addresses, all with just a few clicks. It also includes an S3-alike called Swift.

I worked purely on the software side, but the hardware is pretty cool too. Here's a pic that I hopefully will not get in trouble for posting. It's just too awesome not to brag about.

I used [JuJu](https://juju.ubuntu.com/) to deploy everything, which took care of most of the boring work of installing operating systems and configuring the software. There were still some kinks that I had to iron out manually. I only had to blow away everything and start over three or four times.

Every node in the cluster is monitored by [Ganglia](http://ganglia.sourceforge.net/), which records CPU, disk, network, memory, even VM statistics. I highly recommend it; I even got it recording the datacenter temperature from a USB sensor with relatively little hassle.

There's also a [Nagios](http://www.nagios.org/) server that periodically checks on the Ganglia metrics. We can set a threshold on any metric recorded by Ganglia and have Nagios send us an email when the threshold is exceeded. The only thing still missing is a GSM modem to allow Nagios to send us text messages if the internet connection dies.

Each day, a cron job on each of the three critical machines in the cluster fires up and rsyncs its entire hard disk on to an external RAID machine. I also set up a Nagios alert that fires if a backup fails or misses a day.

## Teaching

For some time now I've felt a tug in the back of my mind calling me to teach. WARNING: religion-speak ahead. In Christianity-land we call this *"being led by the Spirit"*. For those unfamiliar with the lingo, it usually means *"I want to do this thing, and it feels right, and there's nothing stopping me, so I'm pretty sure it's Spirit-led."* (Side note: Christians spend way too much time trying to "discern God's will for my life." Just do your best, people.) (Side side note: I'm not cynical at all.)

So one day on my lunch break, I walked into my old middle/high school and said, "I'd like to teach a computer science class." They said, "can you start in a few weeks?"

In a few weeks I'm starting a teaching "trial run". It's a short, simple class, once a week for six weeks, mostly just to get kids excited about CS. If all goes well, Lord willing I'll probably start a more in-depth class next year. And oh man do I have some crazy ideas.

I was intrigued by an article on [flipped classrooms](http://en.wikipedia.org/wiki/Flip_teaching), which go like this: watch lectures on YouTube at home, and do all your homework in class. Backward from the usual pattern. Here's why:

- Lecturing is probably the
[least efficient form](http://www.chalkbored.com/students-problems-with-classroom-lectures.htm)of teaching you could come up with, but it's often the only practical option for uploading information into people's brains. Recording the lectures on video at least mitigates some of the problems by allowing students to pause, fast-forward, or skip the entire lecture. - As a student, I never thought of good questions in class. They always came later that night (much later) when I pulled out the homework and hit a brick wall. By devoting the whole class period to homework, the teacher can maximize the time they have to answer questions.
- The flipped classroom motivates students to participate in class, since they're already stuck there and it's in their best interest to finish their work quickly while they have access to the teacher.
- I always studied alone, but most students work better in groups. This teaching model obviously encourages lots of collaboration.

This is all theory for me right now, but I'll let you know what I've learned a month or two from now. It's all very scary and new. Kids are going to be harder to program than computers, I think.

## New Apartment

All I have to say is this:

Much more is happening. The next post will cover everything in Lemma. The project that simply will not die.