---
title: An Interview with Oxide's Bryan Cantrill
url: https://chipsandcheese.com/p/an-interview-with-oxides-bryan-cantrill
author: George Cozma
published: '2025-03-28'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# An Interview with Oxide's Bryan Cantrill

Hello you fine Internet folks,

Today we have an interview with Bryan Cantrill from [Oxide Computer Company](https://oxide.computer/).

Cloud computing has been a tour de force in the computing industry, with many businesses and even governments moving over to cloud services for their computing infrastructure. This gives these companies and governments near complete isolation from any hardware issues that may crop up due to the sheer size of many cloud providers, which allows them to automatically migrate VMs to other systems while the hardware issue is being resolved. But not everything can or even should be moved to the cloud, for various reasons such as compliance reasons, cost, etc. This means that some folks may have to stick with on-premises compute, but the cloud model of automatic migration in the case of hardware failure is still relevant and this is where Oxide fits in.

What Oxide is building is effectively an on-premises cloud. To start with, Oxide’s philosophy is to treat a rack of servers in the same way as a hyperscaler (AWS, GCP, Azure, etc) does. So, instead of directly accessing a single node in a server and running your workload, you start up a VM in the Oxide control panel just like in AWS or Azure. This allows for automatic fail-over of VMs in the event of a hardware failure. Now, in order to facilitate this cloud-like behavior, Oxide is building their own racks, which resemble a rack that you may be able to find in a hyperscaler’s datacenter. I had the chance to interview their CTO, Bryan Cantrill, while I was in the Bay Area this past week to ask about their hardware and what they are doing.

Hope y'all enjoy!

Transcript below has been edited for conciseness and readability.

**GEORGE:** Hello you fine internet folks! Today, we're here at Oxide Computer Company, and I have with me, Bryan.

**BRYAN:** Heya!

**GEORGE:** Who are you, and what do you do at Oxide?

**BRYAN:** Hi, I'm Bryan Cantrill, I'm the CTO at Oxide Computer Company, we're here at our office in Emeryville- our office and lab, kind of our playhouse here in Emeryville.

We're a computer company! We're a modern computer company, we are a rack-scale computer company.

So, this is the Oxide rack behind you, and what we have done- our observation was, if you look at those folks deploying compute at scale- Amazon, Google... hyperscalers right? They've all built their own computers. And we were (I along with my cofounder) were at a public cloud company, Joyent, that was purchased by Samsung-

**GEORGE:** Interesting!

**BRYAN:** It was interesting! And, we were... after Samsung bought the company, they were really trying to deploy at Samsung-scale. And we were deployed on commodity gear; we were deployed on Dell, Supermicro, some HP, some Arista... and uh...

**GEORGE:** Trying to match all that stuff can be very difficult.

**BRYAN:** When we hit scale, everything broke.

**GEORGE:** I can imagine.

**BRYAN:** And, to be fair, everything broke in hardware and software, but the difference is, with the software, we could actually go fix it. And we fixed a bunch of our software systems, but then the problems you're left with are those problems, that are at the hardware/software boundary. And... it was pretty frustrating, and you look at like, "how did these other folks do it?" And you realize, they've done their own machines.

**GEORGE:** So, what makes... (if you wanna show to the audience) one of these?

**BRYAN:** Right! So this is an Oxide sled, and this doesn't look like a normal server computer, right?

**GEORGE:** No, no it doesn't. It looks like a blade.

**BRYAN:** It looks like a blade, right. And actually, if you look at the back... it even looks more like a blade. Lemme take off the Kapton tape there... It blind mates in the power first of all, we - like everybody running at scale - we run a DC bus bar, up and down the rack. So you've got an actual power shelf, that contains [bridge] rectifiers, those rectifiers then take you from AC to DC, you run DC on the bus bar,

**GEORGE:** DC 48v?

**BRYAN:** Uh, yeah, 54v. That is the way that everybody at scale runs, with a DC bus bar.

... you can't buy a DC bus bar based machine, DC bus bar-based rack, from Dell, HP, Supermicro! And they'll tell you nobody wants it.

**GEORGE:** [Sounds of incredulity] Hmmm...

**BRYAN:** Right, exactly!

**GEORGE:** The fact that this exists tells me otherwise!

**BRYAN:** Exactly, it definitely does, and one of the things I've appreciated... we've kind of accreted the server architectures that we have.

This traditional [server] architecture has accreted over time, and until we took a clean sheet of paper, you really don't appreciate just how many things are broken with it! One of the things you commented on, is the noise; it's so much quieter.

**GEORGE:** Yeah, and, it's off-camera right here, but there's one rack running right now over to my right side... you can hear it, but it's not a tinny noise. It's a very... almost sort of wind-blowing noise. Which is exactly what it is.

**BRYAN:** Right, and you know what's funny? We didn't design this thing to be acoustically pleasant, ...

**GEORGE:** It just turned out like that?

**BRYAN:** It just turned out like that. And one of the things you'll appreciate is, when you look at the acoustic unpleasantness in a traditional server... yes, you've got a bunch that's coming from those small fans at the back; a bunch of it is *also* coming from those fans on the power supplies. Because you've got those AC power supplies...

**GEORGE:** And it's all like, 40mm fans.

**BRYAN:** Those are *tiny* fans, and, those AC power supplies, you take them apart... they're crammed. So there's a high static pressure that [the fans] have to overcome; those fans are workin' hard! And it's hot. And of course, that fan is a thing that blows on AC power supplies, so you have two of them. So now we've got two AC power supplies, in every one of these servers, all these power cords... and it's just like, the whole thing is a mess.

And... that's just the beginning; the DC bus bar is to me just the beginning.

**GEORGE:** So, speaking of... well, you say basic- the way a computer is booted, is you usually start with what's known as a Basic Input Output System, the BIOS,

**BRYAN:** The BIOS... yeah.

**GEORGE:** Now, in the early 2000s, this was replaced by UEFI,

**BRYAN:** UEFI, yes, Itanium's gift to the world!

**GEORGE:** Yeah, and while that works perfectly well for your average laptop or desktop, when you get to this scale,

**BRYAN:** It doesn't make sense.

**GEORGE:** Why is that?

**BRYAN:** Because it's giving you this kind of optionality you actually don't want. When you have something of this scale - and we have co-designed our host operating system with our hardware - you don't need that optionality, of booting kind of... I don't need to boot DOS on this thing!

**GEORGE:** [Laughing] You don't want DOS on these machines?!

**BRYAN:** Okay, that would be kind of entertaining, but... we actually don't need any of that. But we have preserved all of this kind of ancient optionality in the BIOS. A big problem that we have with the BIOS, is that the BIOS has to boot the system in order to boot the system.

So one of the things the BIOS has to do... it needs to find like, how do I boot this thing? I need to actually do I/O, to pull a boot image off of somewhere. I/O, as we know, everything's complicated... you can't just like "do I/O", like, we actually have to bring up PCIE engines, you have to bring up all the CPUs... so you're doing all this work to boot the system, and then you find the image you want to boot, and now you have to be like, "okay, now we have to pretend like we were never here".

So it then tries to- we call it "setting the machine backward", where it makes the machine **look like** it has not been booted, when it executes that first operating system instruction. But in reality an **entire city** has been constructed, and ploughed under; and the operating system can actually see the artifacts of that over time. There's something called System Management Mode, SMM…

**GEORGE:** [Laughing] Ahhh yes, what some people refer to as "ring -2" if I remember correctly?

**BRYAN:** That's right, ring -2, and that kind of platform initialization layer, can stuff whatever it wants in SMM.

**GEORGE:** I still find it hilarious - I think it was HP? - tried putting like a day-calendar in the SMM, which is like... why are you doing this?! [Laughing]

**BRYAN:** They're doing it, because they wanted to add value to their hardware, without controlling the system software.

So the way to do that, is to jam that software into the system software they do control, which is SMM, but from the perspective of actually running this thing as a server, that's just a problem for me. I don't want to have ring -2. So for us, SMM is empty. Because the other thing is... why do you end up in SMM? For any reason! If you look at the architecture manual, it can go into SMM for any reason, can stay there for any length of time... it's unspecified, that you have to wait.

**GEORGE:** So, how do you solve this?

**BRYAN:** So for us, we do have something in SMM mode: if you ever hit SMM mode, we panic the system. Because, under no condition should we enter SMM. So if we entered SMM mode, we bring the system down and take a crash dump.

That would be pretty wild, if we ever saw that happen, right? Because it would mean that... but we have not seen that happen, and we wanted to do that to make sure, if something were to errantly enter System Management Mode.

But we didn't use System Management Mode at all, we also didn't want to have a BIOS at all.

**GEORGE:** Yep, so how are you getting around that?

**BRYAN:** Yeah, so that was tough, and in fact, this is something that we didn't really appreciate at the time... AMD didn't think we could pull this off, apparently Google tried this and failed. And if Google has tried something and failed it must be impossible for humanity?!

**GEORGE:** [Laughing] Well, oftentimes what they do is succeed and then claim that they failed, and then just, cancel the product.

**BRYAN:** [Laughing] That's right, and it was tough, and it required us to work very closely with AMD. I think that AMD didn't really believe that we could pull it off,

**GEORGE:** It's... I wouldn't even say it's not a trivial- it's a very complicated problem.

**BRYAN:** It is, because you are doing that *lowest* layer of platform initialization.

**GEORGE:** And that platform initialization, people forget, is like, [AMD] memory training, bringing up the PCIE,

**BRYAN:** That's right.

**GEORGE:** And, remember, what's bringing up the system? Well, oftentimes, like if you try and access a BMC, that BMC is on a PCIE bus, it has to be brought up and initialized, so there's a lot of complex problems with the BMC,

**BRYAN:** Speaking of the BMC, we also threw that into the sea!

So the BMC - Baseboard Management Controller - the computer-within-the-computer... we felt that the BMC had grown far too large, far too complicated. BMC should not be on PCIE, from our perspective. What you actually want is environmentals; you want power control, it needs to be on its own network, ... and that's basically it. Its job is really to hand the host CPU its cup of coffee.

**GEORGE:** I wish I had someone that hands me my cup of coffee!

**BRYAN:** So we eliminated the BMC, and we replaced it with what we call the Service Processor, the SP, kind of going back to an order model... so if you look at this compute sled here, and it may be hard to see in there, that's our Service Processor.

So this a ST Microelectronics part, and this is a part that is kinda funny because it doesn't need a heatsink, right? This is a 400 MHz part! Which is faster than machines were when I was coming up; like faster than the first workstation that I had at Sun Microsystems, by a long shot.

**GEORGE:** It's what, 80x faster than the original x86? [Ed: Original 8086 was 5 MHz, 400 MHz is exactly 80x faster - good memory and quick arithmetic!]

**BRYAN:** That's right. So it's like, why are we taking this kind of BMC and running this kind of multi-user operating system on it, when we actually have plenty of compute power there. We did our own operating system, we took a clean sheet of paper there as well. I think we were looking around for kind of, best-of-breed, but we weren't finding anything that we liked exactly.

One of the things that we were not finding is operating systems have this kind of multi-user heritage, where, they know how to load programs... which makes sense, absolutely. The idea that an operating system can load a program that it has never seen before makes it valuable, makes it usable!

**GEORGE:** I mean if you think about it, everytime you power a system off, and you reboot the OS; essentially the OS goes, I'm brand new, and then you go to let's say Steam for example... it doesn't know what Steam is.

**BRYAN:** Right, yes, exactly.

**GEORGE:** So the OS has to figure out the program, and boot it.

**BRYAN:** So even in microcontroller-based operating systems, they still had this idea of program loading. We wanted programs, but we don't want to load foreign programs on this; we want - all the of things that are in this, we want it to be aware of, when it actually boots.

So Hubris is our operating system-

**GEORGE:** I love the names Hubris, and then-

**BRYAN:** Humility is for the debugger. So Cliff Biffle, the engineer who pioneered Hubris - this is of course one of the Deadly Sins of Programmers - the idea being a nod to, oh my god you're doing your own operating system, the hubris of doing your own operating system! And then of course the debugger for that is Humility.

What's been interesting, is that that kind of model - and Cliff has a great talk at OSFC, my colleague Matt Keeter also did a terrific talk on some of the debugging infrastructure we've built on this thing - that model has allowed us to keep Hubris as a very tight image. So Hubris knows about all the tasks that it's going to run, when it actually boots; that image has every task in it. It does not load foreign programs, which is what you want in this kind of firmware.

**GEORGE:** Yeah, you don't want someone to be able to- even if you had physical access, ... could I, change that?

**BRYAN:** Great question, so if you had physical access, you could load a new image on here. But, then there's a Root of Trust on here, that Root of Trust would know that that image - unless you were Oxide doing it - it would know that image has actually not been signed by Oxide. So we actually test the image.

**GEORGE:** Now, can you... so let's say I get access somehow to a just single node, I only have time to mess with a single node. You have a single node in a big rack, could you, re-... essentially, download a new system image for that microcontroller?

**BRYAN:** You could create your own image, but it would know this is not an Oxide image.

**GEORGE:** Nono I mean, can it then pull an image, a known good image, off a different sled?

**BRYAN:** Ohhh, yeah, well no, you need to have enough to actually get over our Service Processor network, so you'd have to qualify just how crippled this image is. If you put a brick on here, it's going to be a problem...

**GEORGE:** [Laughs]

**BRYAN:** As a result, we're as a practical matter very careful about that, we've got, there are A and B sides to the microcontroller, so if you do put a bad image on it can rollback to the other one, and so on. This thing is really designed- it is fit to purpose, for booting and operating a computer. Unlike a BMC, which is really designed to make a server look like a desktop.

**GEORGE:** Yep. I think, well, we're running quite long here, but... one last question- always my last question, what's your favorite type of cheese?

**BRYAN:** Ooooh... that's a good question you know. I... um, God I mean I love a good sharp cheddar.

**GEORGE:** I agree with you on that one.

**BRYAN:** Actually, I also really like Swiss, not just Swiss cheese but Swiss cheeses, so a good Emmentaler, something like that, but my kids are less into that. I guess I'm pretty traditional in that regard.

**GEORGE:** I 100% agree. Well thank you so much, Bryan, for this, thank you for watching! Like, hit subscribe, do all that, comment... it really does help the algorithm, and we must appease the algo gods.

So, thank you so much!

**BRYAN:** Thank you!

If you like the content then consider heading over to the [Patreon](https://www.patreon.com/ChipsandCheese) or [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks to Chips and Cheese. Also consider joining the [Discord](https://discord.gg/TwVnRhxgY2).