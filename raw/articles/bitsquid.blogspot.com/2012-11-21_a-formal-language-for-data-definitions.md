---
title: A Formal Language for Data Definitions
url: https://bitsquid.blogspot.com/2012/11/a-formal-language-for-data-definitions.html
author: Niklas
published: '2012-11-21'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Lately, I've started to think again about the irritating problem that there is no formal language for describing binary data layouts (at least not that I know of). So when people attempt to describe a file format or a network protocol they have to resort to vague and nondescript things like:

```
Each section in the file starts with a header with the format:
4 bytes header identifier
2 bytes header length
0--20 bytes extra data in header
The extra data is described below.
```

As anyone who has tried to decipher such descriptions can testify, they are not always clear-cut, which leads to a lot of unnecessary work when trying to coax data out of a document.

It is even worse when I create my own data formats (for our engine's runtime data). I would like to document those format in a clear and unambiguous way, so that others can understand them. But since I have no standardized way of doing that, I too have to resort to ad-hoc methods.

This whole thing reminds me of the state of mathematics before formal algebraic notation was introduced. When you had to write things like: *the sum of the square of these two numbers equals the square of the previous number*. Formal notation can bring a lot of benefits (just look at what it has done for mathematics, music, and chess).

For data layouts, a formal definition language would allow us to write a tool that could open any binary file (that we had a data definition) for and display its content in a human readable way:

```
height = 128
width = 128
comment = "A funny cat animation"
frames = [
{display_time = 0.1 image_data = [100 120 25 ...]}
...
]
```

The tool could even allow us to edit the readable data and save it back out as a binary file.

A formal language would also allow debuggers to display more useful information. By writing data definition files, we could make the debugger understand all our types and display them nicely. And it would be a lot cleaner than the hackery that is *autoexp.dat*.

Just to toss something out there, here's an idea of what a data definition might look like:

```
typdedef uint32_t StringHash;
struct Light
{
StringHash name;
Vector3 color;
float falloff_start;
float falloff_end;
};
struct Level
{
uint32_t version;
uint32_t num_lights;
uoffset32_t light_data_offset;
...
light_data_offset:
Light lights[num_lights];
};
```

This is a C-inspired approach, with some additions. Array lengths can be parametrized on earlier data in the file and a labels can be used to generate offsets to different sections in the file..

I'm still tossing around ideas in my head about what the best way would be to make a language like this a reality. Some of the things I'm thinking about are:

## Use Case

I don't think it would do much good to just define a langauge. I want to couple it with something that makes it immediately useful. First, for my own motivation. Second, to provide a "reality check" to make sure that the choices I make for the language are the right ones. And third, as a reference implementation for anyone else who might want to make use of the language.

My current idea is to write a binary-to-JSON converter. I.e., a program that given a data definition file can automatically convert back and forth between a binary and a JSON-representation of that same data.

## Syntax

The syntax in the example is very "C like". The advantage of that is that it will automatically understand C structs if you just paste them into the data definition file, which reduces the work required to set up a file.

The disadvantage is that it can be confusing with a language that is very similar to C, but not exactly C. It is easy to make mistakes. Also, C++ (we probably want some kind of template support) is quite tricky to parse. If we want to add our own enhancements on top of that, we might just make a horrible mess.

So maybe it would be better to go for something completely different. Something Lisp-like perhaps. (Because: Yay, Lisp! But also: Ugh, Lisp.)

I'm still not 100 % decided, but I'm leaning towards a restricted variant of C. Something that retains the basic syntatic elements, but is easier to parse.

## Completeness

Should this system be able to describe *any* possible binary format out there?

Completeness would be nice of course. It is kind of annoying to have gone through all the trouble of defining language and creating the tools and *still* not be able to handle all forms of binary data.

On the other hand, there are a lot of different formats out there and some of them have a complexity that is borderline insane. The only way to be able to describe *everything* is to have a data definition language that is Turing complete and procedural (in other words, a detailed list of the instructions required to pack and unpack the data).

But if we go down that route, we haven't really raised the abstraction level. In that case, why even bothering with creating a new language. The format description could just be a list of the C instructions needed to unpack the data. That doesn't feel like a step forward.

Perhaps some middle ground could be found. Maybe we could make language that was simple and readable for "normal" data, but still had the power to express more esoteric constructs. One approach would be to regard the "declarative statements" as syntactic sugar in a procedural language. With this approach, the declaration:

```
struct LightCollection
{
unsigned num_lights;
LightData lights[num_lights];
};
```

Would just be syntactic sugar for:

```
function unpack_light_collection(stream)
local res = {}
res.num_lights = unpack_unsigned(stream)
res.lights = []
for i=1,res.num_lights do
res.lights[i] = unpack_light_data(stream)
end
end
```

This would allow the declarative syntax to be used in most places, but we could drop out to full-featured Turing complete code whenever needed.

Years ago, I wrote a tool that made some steps towards this. It was a very simple hierarchical block structured language - like a minimal xml and trivial to parse. In it you could write both the data to be converted to binary, and a 'rules' file that would tell a compiler how to do the conversion.







ReplyDeleteThe compiler would walk the structure of both the rules and the data file simultaneously translating it as it went. There were a set of special rules for common things like adding a header, or saving the size of a block (including those in the future), or the length of an array.

The basic point of it was to minimise the amount of crap we had to write when converting data from our tools to game ready binary data. We could change the binary format independently of the data and the tools, which was nice.

It was also a big pain in the ass, mostly because that's all it did. It didn't help with versioning or backwards compatibility (which was a nightmare), or generate your binary loading code for you, and frankly I wrote it when I was still only 1 year into industry so it wasn't exactly my finest piece of code .

These things are all fixable, but it's definitely a problem with a lot of details that need carefully unpicking. Code gen and backwards compatibility are definitely two biggies. Being able to avoid having to put your data into a text file first is another.

It's an interesting problem though. We also have a need for this, so I'd be interested in talking to you about it. It just appears that standardised, but adhoc methods, have been easier to date.

ta,

Sam

FWIW, there's an existing standard called ASN.1 that provides a formal language for describing binary data layouts. I think it's generally used for defining messaging protocols.


ReplyDeleteIt's verbose and nowhere near as readable as your pseudocode though, so even if ASN.1 provides some of the functionality you're looking for I suspect it's more heavyweight than most game developers would want.

I can see merit in having more formal way for structural definition.



ReplyDeleteOne approach that brings to mind is a hex editor called Synalyze It[1], where you can define

grammars for file formats etc. and it can highlight and understand parts of the binary.

The grammar isn't quite as human readable, being a xml created by the grammar editor, but it has the mechanics laid out needed for many file formats.

[1] http://www.synalysis.net

Google's protocol buffers might interest you...

ReplyDeleteHi,







ReplyDeleteI think 010Editor [1] does something similar of what you describe but they have a language close to C in syntax which allows you to describe "every" cases. So it's less simple than what you are proposing but it's very powerful.

By the way, I totally love your blog, believe it or not but I was working in a game company which was trying to do exactly what your are doing at bitsquid (but only for internal use) and I think we made all the errors you list in this blog (All-in one editor, complex XML format, complex serialization system, everything is an object etc.). I was very disappointed about the technical decisions and... a colleague show me your blog and it blows my mind!!

Now, I don't work anymore for the game industry neither I code in C++ but I think your blog is one of the main reason (maybe also the book "Coders at work") I'm still coding for a living.

Keep up good work,

Andreas, a true fan

[1] http://www.sweetscape.com/010editor/

Indeed 010Editors Templates have been what I have been using. After talking to a lot of friends that do reverse engineering this is basically the standard.

DeleteThanks for the nice words!



DeleteI had a quick look at the 010Editor data templates. And you are right, it looks very similar to what I was looking for.

I'll investigate it further.

You're welcome :)



DeleteWhen I read your blog for the first time I was so amaze cause it was like you answered all our problematic with a very simple, understandable and yet extremely powerful and modular solution. On our side we had some hyper blotted tech that was almost unusable despite five years of R&D... What a waste of time and resources !

I want to write something about that cause it's the exact opposite (in term of design) as your engine and I think it will be a great example of what to avoid :).

There's such examples of reading such data if you look at any open-source Halo map editor. We had a very similar approach to what you're looking at when writing updates to the editor, Entity. Though this approach would of course need some way to detect the different sets of data.

ReplyDeleteAnswer is "Protocol buffers", already mentioned, but worth to look at.


ReplyDeleteThis is my blog. Click here.

ReplyDeleteเว็บแทงหวยออนไลน์ สมัครเลยตอนนี้ "

blog is very amazing. Yellowstone Coat

ReplyDeletelove the way you've expressed idea






ReplyDeleteyellowatone hoodie coat



ReplyDeleteI will be looking forward to your next post. Thank you

drpepperstarcenter.com/

kentrylee.com/

A good website is useful.

ReplyDeletejoventuthandbolmataro.com/

joventuthandbolmataro.com/

Hey, what a blog you write, it is such wonderful post i never read this kind of stuff.











ReplyDeleteAssisted Living Near MeAssisted Living Service Near MeAssisted Living Homes Near MeAssisted Living ServiceAssisted Living Services Near MeCastle Rock Assisted LivingAurora Assisted LivingFederal Heights Assisted LivingDenver Assisted LivingColorado Assisted LivingThis comment has been removed by the author.

ReplyDeleteDuring the printer establishment, numerous user see the 'Epson Printer WiFi Setup Failed' message springing up on the screen. The error message showing up on the screen demonstrates that your Printer Wi-fi setup is flopped because of some specialized difficulty. Luckily, a user can undoubtedly manage issues with basic apparatuses. Epson printer wifi connection problem


ReplyDeleteOn the off chance that your printer is also showing you the 'Epson Printer WiFi Setup Failed' message on the screen, you can continue with the directions referenced in the guide and fix your concern. Along these lines, on the off chance that you would prefer not to return to your old-wired association, peruse and adhere to the guidelines. Assuming you are stressing associating your Epson printer to the remote organization, we will assist you with doing that. Here you can figure out how to set up an Epson printer remotely with no outer assistance. In the wake of introducing the product furnished with your new printer, you can go before setting up your printer to work remotely user WLAN network. This availability doesn't need links and it offers arrangement without the capability of network disappointment. brother printer MFC L2750DW setup

Thanks for the best share and i loved it,

ReplyDeletecucotv

google 402

ReplyDeletegoogle 403

google 404

google 405

google 406

Impressive written blog and valuable information shared here. สมัครสมาชิก 123betting

ReplyDeleteIf you are Looking for the best Massage Near Me Bangalore, then you have come to the right place. We have young models who offer b2b massaging. Female to male spa near me

ReplyDelete


ReplyDeleteLooking for Full Female to male massage centre near me Service, Body Spa in Bangalore for female to male at our renowned sparsh body spa. Book now Nearby me.

We serve our Body to body massage service in the whole Hyderabad city Our services are at the top when it comes to massage Service in Hyderabad. We have the best Body to body massage spa near me to satisfy.

ReplyDeleteHave u ever tried a Massage near me ? If your answer is no, then you are missing out on loads. Fun is one quotient and getting relaxed is another. for more info visit here:- Nuru massage

ReplyDeleteWe assure you world class nuru massage service in Bangalore.Bella spa having special nuru therapist where you can get 100% satisfied service.



ReplyDeleteVisit female to male spa near me 24 hours

I am committed towards providing excellent customer experience with each client session by ensuring that they are comfortable during their time at Massage spa near me

ReplyDeleteLishasingh is a massage therapist from Bangalore. He has worked over the last few years to provide top customer service and support, for both male and female customers.He is always striving to become massage parlour near me a better version of his self by ensuring high quality control throughout the day.Obedient6 minutes ago

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteOur spa bring the b2b massage service from female therapist who are trained to provide 100% result based massage sessions.Customers go with stress free and relax mode after our oil, thai, swedish, hot stone massage.

ReplyDeleteVisit massage spa in Hyderabad

we have to do on this at the sources massage near me

ReplyDeleteWith us, you will not only receive a complete body massage, but also other options like Foot Massage as well as Body Scrubs spa near to me and Face Pack. Our prices are reasonable so that anyone can enjoy our services with no trouble.

ReplyDeleteSo good that you wrote here awesome stuff.

ReplyDeleteMumbai CompanionOur agency is ready to fulfill your desire best service provider in Bangalore .Best girl are available for service 24/7 assured 100% satisfaction.

ReplyDeleteBangalore Companion


ReplyDeleteOur agency is ready to fulfill your desire best service provider in Chandigarh. Best girl are available for service 24/7 assured 100% satisfaction.

Chandigarh Companion

The Companion in Chandigarh are therefore considered to be such brilliant associates who can bring in ultimate happiness in your minds.


ReplyDeleteNice knowledge gaining article. This post is really the best on this valuable topic.


ReplyDeleteNuru massage in Chennai



ReplyDeleteFemale Companion BangaloreBangalore Dating GirlsArriving on time: Make sure to arrive on time, as coming in a rushed state can make it harder to relax.nuru massage in chennai

ReplyDeleteRelaxing your muscles and mind: Let go of unimportant thoughts and be more body-centered. This way, you’ll relax your body and loosen your muscles.

niec one b2b massage in hyderabad


ReplyDeleteEffleurage, petrissage, lymphatic female to male body massage centres drainage and myofascial release are all massage techniques that can be used following exercise

ReplyDeleteThe craniosacral system includes the hot massage in hyderabad membranes and cerebrospinal fluid that surround and protect the brain and spinal cord.



ReplyDeleteac have become necessary equipment to keep homes and workplaces comfortable, particularly in areas with high temperatures. Air conditioners come in various prices and features to accommodate a broad range of demands, tastes, and energy efficiency standards. When selecting an air conditioner, it's essential to consider many aspects, including cooling capacity, energy use, technology used (such as inverter technology for efficiency), and extra functions like air purification.

ReplyDeletecool body massage spa near me

ReplyDeleteGet ready for a spectacular eid al adha mega sale celebration with our massive sale event, when joy knows no limits and savings soar to new heights! Explore a world of unbeatable deals on a variety of goods, including electronics, clothing, home goods, and more. Treat yourself and your loved ones to the best bargains in town this Eid al-Adha, and make every purchase a reason to celebrate. Come celebrate with us on this unique occasion by taking advantage of deals that really add up!

ReplyDeleteNear Massage Goa Spa

ReplyDeleteRiya Mehra Massage and Spa Center

ReplyDeleteThanks

ReplyDeleteonline dating

This was such a valuable post. I’ve already started applying some of your tips to my daily life!

ReplyDeleteMahadev Book is a popular platform designed for players who enjoy smooth and engaging online gameplay. The user-friendly Mahadev Book App makes it simple to access a wide range of games in just a few clicks. With secure login, fast performance, and 24/7 support, it ensures a hassle-free experience.

ReplyDeleteCricbet99 is built for true cricket enthusiasts, offering real-time odds, quick settlements, and an easy-to-use environment. Our platform focuses on transparency, fast performance, and providing the best experience for live cricket and T20 league.

ReplyDelete