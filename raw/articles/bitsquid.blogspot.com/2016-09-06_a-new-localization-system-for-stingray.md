---
title: A New Localization System for Stingray
url: https://bitsquid.blogspot.com/2016/09/a-new-localization-system-for-stingray.html
author: Niklas
published: '2016-09-06'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

The current Stingray localization system is based around the concept of
*properties*. A property is any period separated part of the file name
before the extension. Consider the following three files:

`trees/larch_03.unit`

`trees/larch_03.fr.unit`

`trees/larch_03.ps4.unit`


These three files all have the same type (`.unit`

), and the same name
(`trees/larch_03`

), but their properties differ. The first one has
no properties set. The second one has the property `.fr`

and the last
one has the property `.ps4`

. (Note that resources can have more than
one property.)

Properties are resolved in slightly different ways, depending on
the kind of property. *Platform properties* are resolved at compile
time, so if you compile for PS4, you will get the PS4 version of
the resource (or the default version if there is no `.ps4`

specific
version).

Other properties are resolved at *resource load time*. When you load
a bunch of resources, which property variant is loaded
depends on a global *property preference order* set
from the script. A property preference order of `['.fr', '.es']`

means
that resources with the property `.fr`

are be preferred, then resources
with the property `.es`

(if no `.fr`

resource is available), and finally
a resource without any properties at all.

This single mechanism is used for localizing strings, sounds, textures,
etc. Strings, for example, are stored in `.strings`

files, which are
essentially just key-value stores:

```
file = "File"
open = "Open"
...
```


To create a French localized of this `menu.strings`

resource, you
just create a `menu.fr.strings`

resource and fill it with:

```
file = "Fichier"
open = "Ouvert"
...
```


This basic localization system has served us well for many years, but it has some drawbacks that are starting to become more pronounced:

It doesn't allow file names with periods in them. Since we always interpret periods as properties, periods can't be a part of the regular file name. This isn't a huge problem when users name their own files, but as we are increasing the interoperability between Stingray and other software packages we more and more run into software that has, let's say

*peculiar*, ways of naming its files. Renaming things by hand is cumbersome and can also break things when files cross-reference each other.Switching language requires reloading the resource packages. This seems overly complicated. We have more memory these days than when we started building Stingray. In many cases, especially for strings, it makes more sense to keep them in memory all the time, so we can switch between them easily.

Just switching on platform isn't enough. Mobile devices range from very low-end to at least mid-end. Rather than having

`.ios`

and`.android`

properties, we might want`.low-quality`

and`.high-quality`

and select which one to use based on the actual capabilities of the hardware.-
Making editors work well with the property system has been surprisingly complicated. For example, when the editor runs on Windows, what should it show if there is a

`.win32`

specialization of a resource -- the default version or the`.win32`

one? How would you edit a`.ps4`

resource when those are normally stripped out of the Windows runtime?We used to have this wonky think where you could sort of cross-compile the resources and say that "I want to run on Windows, but

*as if*I was running on PS4. But to be honest, that system never really worked that well and in the new editor we have gotten rid of it.

Interestingly, out of all these problems, it is the first one -- the most stupid one -- that is the main impetus for change.

The new system has several parts. First, we decided that for systems that deal with localization a lot, such as strings and sounds it makes sense to have the system actually be aware of localization. That way, we can provide the best possible experience.

So the `.strings`

format has changed to:

```
file = {en = "File", fr = "Fichier", ...}
open = {en = "Open", fr = "Ouvert", ...}
...
```


All the languages are stored in the same file and to switch language
you just call `Localizer.set_language("fr")`

. We keep all the different
languages in memory at all times. Even for a game with ridiculous
amounts of text this still doesn't use much memory and it means we
can hot-swap languages instantly.

This is a nice approach, but it doesn't work for all resources. We
don't want to add this deep kind of integration to resources that are
normally not localized, such as `.unit`

and `.texture`

. Still, there
sometimes is a need to localize such resources. For example, a `.texture`

might have text in it that needs to be localized. We may need a low-poly
version of a `.unit`

for a less capable platform. Or a less gory version
of an animation for countries with stricter age ratings.

To make things easier for the editor we decided to ditch the property system all together, and instead go for a substitution strategy. There are no special magical parts of a resource's path -- it is just a name and a type. But if you want to, you can say to the engine that all instances of a certain resource should be replaced with another resource:

```
trees/larch_03.unit → trees/larch_03_ps4.unit
```


Note here that there is nothing special or magical about the
`trees/larch_03_ps4.unit`

. There is no problem with displaying it on Windows.
You just edit it in the editor, like any other unit. However, when you play
the game -- any time a `trees/larch_03.unit`

is requested by the engine, a
`trees/larch_03_ps4.unit`

is substituted. So if you have authored a level
full of `larch_03`

units, when the override above is in place, you will instead
see `larch_03_ps4`

units.

There are many ways for this scheme to go wrong. The gameplay script might
expect to find a certain node `branch_43`

in the unit -- a node that exists in
`larch_03.unit`

, but not in `larch_03_ps4.unit`

and this may lead to unexpected
behavior. The same problem existed in the old property system. We don't try to
do anything special about this, because it is impossible. In the end, it is only
the gameplay script that can know what it means for two things to be *similar
enough* to be used interchangeably. Anyone working with localized resources just
has to be careful not to break things.

Overrides can be specified from the Lua script:

`Application.set_resource_override("unit", "trees/larch_03", "trees/larch_03_ps4");`

Note that this is a much more powerful system than the old property system. Any resource can be set to override any other -- we are not restricted to work within the strict naming scheme required by the property system. Also, the override is dynamic and can be determined at runtime. So it can be based on dynamic properties, such as measured CPU or GPU performance -- or a user setting for the amount of gore they are comfortable with.

It can even be used for completely different things than localization or platform specific resources -- such as replacing the units in a level for a night-time or psychedelic version of the same level. And I'm sure our users will find many other ways of (ab)using this mechanism.

But this dynamic system is not quite enough to do everything we want to do.

First, since the override is dynamic and only happens at runtime, our packaging
system can't be aware of it. Normally, our packaging system figures out all
resource dependencies automatically. So when you say that you want a package with
the `forest`

level, the packaging system will automatically pull in the
`larch_03`

unit that is used in that level, any textures used by that unit, etc.
But since the packaging system can't know that at runtime you will replace
`larch_03`

with `larch_03_ps4`

, it doesn't know that `larch_03_ps4`

and its
dependencies should go into the package as well.

You could add `larch_03_ps4`

to the package manually, since *you* know it will be
used. That might work if you only have one or two overrides. However,
even with a very small amount of overrides micromanaging packages in this way
becomes incredibly tedious and error prone.

Second, we don't want to burden the packages with resources that will never be used. If we are making a game for digital distribution on iOS or Android we don't want to include large PS4-only resources in that game.

So we need a static override mechanism that is known by the package manager
to make sure it includes and excludes the right resources. The simplest thing
would be a big file that just listed all the overrides. For example, to
override `larch_03`

on PS4 we would write something like:

```
resource_overrides = [
{
type = "unit"
name = "trees/larch_03"
override = "trees/larch_03_ps4"
platforms = ["ps4"]
}
]
```


This would work, but could again get pretty tedious if there are a lot of overrides. It would be nice with something that was a bit more automatic.

Since our users are already used to using name suffixes such as `.fr`

and `.ps4`

for localization, we decided to build on the same mechanism -- creating overrides
automatically based on suffix rules:

```
resource_overrides = [
{suffix = "_ps4", platforms = ["ps4"]}
]
```


This rule says that when we are compiling for the platform PS4, if we find a resource
that has the same name as another resource, but with the added suffix `_ps4`

, that
resource will automatically be registered as an override for that resource:

```
trees/larch_03.unit → trees/larch_03_ps4.unit
leaves/larch_leaves.texture → leaves/larch_leaves_ps4.unit
```


In addition to platform settings, the system also generalizes to support other flags:

```
resource_overrides = [
{suffix = "_fr", flags = ["fr"]}
{suffix = "_4k", flags = ["4K"]}
{suffix = "_noblood", flags = ["noblood", "PG-13"]}
]
```


This defines the `_fr`

suffix for French localization. A 4K suffix `_4k`

for high-quality
versions of resources suitable for 4K monitors. And a `_noblood`

suffix that selects
resources without blood and gore.

The flags can be set at compile time with:

```
--compile --resource-flag-true 4K
```


This means that we are compiling a `4K`

version of the game, so when bundling *only* the
4K resources will be included and the other versions will be stripped out. Just as if
we were compiling for a specific platform.

But we can also choose to resolve the flags at runtime:

```
--compile --resource-flag-runtime noblood
```


With this setting, both the regular resource and the `_noblood`

resource will be included
in the package and loaded into memory. And we can hot swap between them with:

`Application.set_resource_flag("noblood", true)`

I have not decided yet whether in addition to these two alternatives we should also
have an option that resolves at *package load time*. I.e., both variants of the resource
would be included on disk, but only one of them would be loaded into memory and if you
wanted to switch resource you would have to unload the package and load it back into memory
again.

I can see some use cases for this, but on the other hand adding more options complicates the system and I like to keep things as simple as possible.

A nice thing about this suffix mapping is that it can be configured to be backwards compatible with the old property system:

```
resource_overrides = [
{suffix = ".fr", flags = ["fr"]}
{suffix = ".ps4", platforms = ["ps4"]}
{suffix = ".xb1", platforms = ["xb1"]}
]
```


Whenever we change something in Stingray we try to make it more flexible and data-driven, while at the same time ensuring that the most common cases are still easy to work with. This rewrite of the localization is a good example:

It fixes the problem with periods in file names. Periods are now only an issue if you have made an explicit suffix mapping that matches them.

We can switch language (or any other resource setting) at runtime.

The new system is more flexible -- it doesn't just handle localization and platform specific resources, we can set up whatever resource categories we want. And we can even dynamically override individual resources.

The editor no longer needs to do anything special to deal with the concept of "properties". Resources that are used to override other resources can be edited in the editor just like any other resource.

And the system can easily be configured to be backwards compatible with the old localization system.


I still feel slightly queasy about using name matching to drive parts of this system. Name matching is a practice that can go horribly wrong. But in this case, since the name matching is completely user controlled I think it makes a good compromise between purity and usability.


ReplyDeleteNorton Setup with your product key online. Download & Install Norton Product, Visit activation website norton.com/setup to register your code.Norton Account Support Service 1_844~777~7886 by Phone Call Toll Free Customer Care Support Contact Number.

http://www.nortonsetup-norton.com

To reply, you just need to open your Inbox, click gmail sign in that you want to reply. The email will be open for you. If you only want to reply to the sender who sent the email to you, click the "Reply" button at the bottom and begin composing your email.To reply, you just need to open your Inbox, click the email that you want to reply. The email will be open for you. If you only want to reply to the sender who sent the email to you, click the "Reply" button at the bottom and begin composing your email.


ReplyDeleteSetup your norton Antivirus with help from norton setup , norton.com/setup after reaching the site go with the given steps. http://norton-nortoncom.com


ReplyDeleteThis comment has been removed by the author.

ReplyDeleteThis comment has been removed by the author.

ReplyDeletePython is simple and straightforward sentence structure to learn and peruse also and thus the expense of program upkeep gets reduced. Python bolsters modules and bundles that empower program measured quality and code reuse.


ReplyDeleteFor More Info:- Python Training in Gurgaon

Travelling Atomwas started with a vision of Travel Blogging back in 2016 .

ReplyDeleteTravelling Atom was started with a vision of Travel Blogging back in 2016 . Earlier the blog was named Virtual Nerves .




ReplyDeleteData security is a very big issue nowadays. Viruses harm the data. Here you can know more about how to remove viruses from your computer and makes your data secure and safe.

ReplyDeleteEasy Steps To Remove Viruses

How to Remove Viruses from your computer?

kamakhya temple black magic The Black magic of Kamakhya temple . The blog post seems to be superstious in this era . In the 21st centuary we don’t believe in all these terms Black m.agic and Vashikaran . But we cant turn our eyes from this . The blog post is all concerned about the origin and belief about the Black magic of Kamakhya Temple .

ReplyDeleteVisit McAfee official website www.mcafee.com/activate. Enter your 25 digits Mcafee activation Product Key Enter your Email and password Click Submit and Log in to your account. Once Logged in, Download your Setup in download folder. Run application to install, you’re all set to go!

ReplyDeletemcafee.com/activate

visit norton official website for download norton setup then log in your norton account with email and password. follow few steps to activate your norton setup for any help visit website.


ReplyDeletenorton.com/setup

choose mcafee antivirus for your system

ReplyDeleteMcAfee is exceptional among other security gadgets for any of your devices. This isn't just an ordinary instrument that clears little contaminations and reports bugs.

In any case, this is one whole full security course of action for your Device. Macintosh or Windows just as it works with various tablets and even mobile phones also.

With security being the central point of convergence of the McAfee security systems, it in like manner saves you from potential threats and alerts you, To guarantee your device with mcafee.

visit:

mcafee.com/activate

"It was an informative post indeed. Now It's the time to make the switch to solar power,

ReplyDeletecontact us(National Solar Company) today to learn more about how solar power works.

battery storage solar

united solar energy

solar panels

solar inverter

solar batteries

solar panels adelaide

best solar panels

solar power

battery storage solar

battery charger solar

solar regulators

solar charge controllers

solar battery storage

instyle solar

solar panels melbourne

solar panels for sale

solar battery charger

solar panels cost

buy solar panels"

Great work. Yellowstone Coat

ReplyDeleteIt is always goos idea to collect some good knowledge from reliable sources, thanks






ReplyDeleteyellowatone hoodie coat

I like this article.I was searching over search engines and found your blog and its really helps thank you so much the


ReplyDeleteHow To Download AOL Desktop GoldVery Interesting and wonderfull game keep Download Ludo Online Game

ReplyDeletehttps://bitsquid.blogspot.com/2016/09/a-new-localization-system-for-stingray.html#comment-form

ReplyDeleteHello Sir I saw your blog, It was very nice blog, and your blog content is awesome, i read it and i am impressed of your blog, i read your more blogs, thanks for share this summary.

ReplyDeleteFacebook Not Working Properly

Plan for Jio tower installation 2022 - Apply Now For Jio Tower | Apply Reliance Jio Tower Installation Online | Jio tower installation monthly rent | Jio Tower Complaint Helpline Number - Jio Tower Helpline Number | Reliance Jio Tower Installation Process Steps To Install | Reliance Jio Tower Installation Apply Online and Contact Number 2022 | Jio tower installation customer care number and contact number | Jio tower installation apply online 2021 & jio advance amount

ReplyDeleteطراحی سایت شرکتی میتواند دارای امکانات بسیار زیادی باشد. ساخت سایت شما باید متناسب با هدف و خدماتی که عرضه کند. مشتریان زیادی را به طرف خود هدایت کنید.

ReplyDeleteThanks for sharing your precious time to create this post, it's so informative, and the content makes the post more interesting.really appreciated. Atreides Coat

ReplyDeleteThank you for posting the very nice informative article. Looking forward to reading more articles from you. Visit my website and Join our community!! There are promo's and event everyday!!


ReplyDelete사설토토

카지노사이트

파워볼

Daebak precisely what I was looking for, appreciate it for putting up. Kindly check the following link below Thank you in advance.


ReplyDelete스포츠토토

안전놀이터

토토사이트

안전카지노사이트

Way cool! Some very valid points! I appreciate you penning this article plus the rest of the site is very good. Kindly visit my website and learn more about casino & sports betting



ReplyDelete스포츠토토

카지노사이트

파워볼게임

바카라

Airtel Tower Office - Airtel tower installation and complain

ReplyDeleteSubmit Airtel tower complaint online & get solved in 24hours

Registration open for Airtel mobile tower installation 2022

Airtel tower agreement letter & Airtel tower approval letter

Airtel tower installation customer care number & contact no

Airtel tower head office contact number and helpline number

Documents require for Airtel mobile tower installation

Airtel tower installation process and details step by step

Great Blog! I read your blog, it is very helpful. I appreciate your thoughts which you have shared with us. Keep sharing more content. Are you facing problem to fix AOL Desktop is Not Opening Error? if yes, then please visit our blog.

ReplyDeleteThanks for one marvelous posting! I truly enjoyed reading it, you might be a great author. I will make sure to bookmark your blog and will come back in the future. I want to encourage that you continue your great job.

ReplyDeleteeniac full form in computer

dvd full form

sit full form

pcc full form

iucn full form

full form of lcd

brics full form

tally erp full form

full form of ctbt

crpf full form

I found some useful information in your blog, it was awesome to read, thanks for sharing this great content to my vision, keep sharing..

ReplyDeleteeniac full form in computer

dvd full form

sit full form

pcc full form

iucn full form

full form of lcd

brics full form

tally erp full form

full form of ctbt

crpf full form

You have a real knack for making complicated ideas easy to understand. Thank you for sharing your brilliance!

ReplyDeleteKevin Costner Sherpa Lined Suede Jacket

Great post! I really enjoyed reading about the new localization system for Stingray. It's impressive how much thought went into improving the workflow and making things more intuitive. This is definitely a game changer for game developers looking for more flexibility. Keep up the great work! Also, if anyone ever finds themselves in need of expert legal help, feel free to check out this, It’s always great to have reliable professionals on your side!


ReplyDeleteabogado de flsa

leyes de divorcio nueva jersey

cuál es la ley de divorcio en nueva jersey

traffic lawyer lunenburg virginia

abogado dui southampton virginia

abogado trafico arlington va

adivorcio sin oposición barato en virginia

This gave me a new perspective on the topic!

ReplyDeleteWhen it comes to


ReplyDeleteMacBook repair Dubai, customers can expect top-notch service tailored to their specific needs. Skilled technicians are equipped to handle a wide range of issues, from hardware malfunctions to software glitches, ensuring that each device is restored to optimal performance.The repair process is efficient, often completed within a short timeframe, allowing users to get back to their daily tasks with minimal disruption. With a focus on quality and customer satisfaction, MacBook repair services in Dubai are dedicated to providing reliable solutions for all Apple laptop users.