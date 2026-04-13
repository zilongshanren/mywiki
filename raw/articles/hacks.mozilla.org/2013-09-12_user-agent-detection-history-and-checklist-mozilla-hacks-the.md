---
title: User-Agent detection, history and checklist – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/09/user-agent-detection-history-and-checklist/
author: Karl Dubost
published: '2013-09-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## History

`User-Agent: <something>`

is a string of characters sent by HTTP clients (browsers, bots, calendar applications, etc.) for each individual HTTP request to a server. The HTTP Protocol as [defined in 1991](http://www.w3.org/Protocols/HTTP/AsImplemented) didn’t have this field, but the next [version defined in 1992](http://www.w3.org/Protocols/HTTP/HTTP2.html) added [ User-Agent](http://www.w3.org/Protocols/HTTP/HTRQ_Headers.html#user-agent) in the HTTP requests headers. Its syntax was defined as “

the software product name, with an optional slash and version designator“. The prose already invited people to use it for analytics and identify the products with implementation issues.

This line if present gives the software program used by the original client. This is for statistical purposes and the tracing of protocol violations. It should be included.


Fast forward to August 2013, the HTTP/1.1 specification is being revised and also defines [ User-Agent](http://tools.ietf.org/html/draft-ietf-httpbis-p2-semantics-23#section-5.5.3).

A user agent SHOULD NOT generate a User-Agent field containing


needlessly fine-grained detailand SHOULD limit the addition of

subproducts by third parties. Overly long and detailed User-Agent

field values increase request latency and the risk of a user being

identified against their wishes (“fingerprinting”).Likewise, implementations are encouraged

not to use the product, as this circumvents the purpose of the field. If a user

tokens of other implementations in order to declare compatibility

with them

agent masquerades as a different user agent, recipients can assume

that the user intentionally desires to see responses tailored for

that identified user agent, even if they might not work as well for

the actual user agent being used.

Basically, the HTTP specification discouraged since its inception the detection of the `User-Agent`

string for tailoring the user experience. Currently, the user agent strings have [become overly long](http://webaim.org/blog/user-agent-string-history/). They are abused in every possible way. They include detailed information. They lie about what they really are and they are used for branding and advertising the devices they run on.

## User-Agent Detection

User agent detection (or sniffing) is the mechanism used for parsing the `User-Agent`

string and inferring physical and applicative properties about the device and its browser. But let get the record straight. User-Agent sniffing is a **future fail strategy**. By design, you will detect only what is known, not what will come. The space of small devices (smartphones, feature phones, tablets, watches, arduino, etc.) is a very fast-paced evolving space. The diversity in terms of physical characteristics will only increase. Updating databases and algorithms for **identifying correctly is a very high maintenance task** which is doomed to fail at a point in the future. Sites get abandoned, libraries are not maintained and Web sites will break just because they were not planned for the future coming devices. All of these have costs in resources and branding.

New solutions are being developed for helping people to adjust the user experience [depending on the capabilities](https://hacks.mozilla.org/2012/07/the-web-developer-toolbox-modernizr/) of the products, not its name. Responsive design helps to create Web sites that are adjusting for different screen sizes. Each time you detect a product or a feature, it is important to thoroughly [understand why](https://hacks.mozilla.org/2013/04/detecting-touch-its-the-why-not-the-how/) you are trying to detect this feature. You could fall in the same traps as the ones existing with user agent detection algorithms.

We have to deal on a daily basis with abusive user agent detection blocking Firefox OS and/or Firefox on Android. It is not only Mozilla products, every product and brand has to deal at a point with the fact to be excluded because they didn’t have the right token to pass an ill-coded algorithm. User agent detection leads to situation where a new player can hardly enter the market even if it has the right set of technologies. Remember that there are huge benefits to create a system which is [resilient to many situations](http://christianheilmann.com/2012/02/16/stumbling-on-the-escalator/).

Some companies will be using the `User-Agent`

string as an identifier for bypassing a pay-wall or offering specific content for a group of users during a marketing campaign. It seems to be an easy solution at first but it creates an environment easy to by-pass in spoofing the user agent.

## Firefox and Mobile

Firefox OS and Firefox on Android have very [simple documented User-Agent strings](https://developer.mozilla.org/en-US/docs/Gecko_user_agent_string_reference#Firefox_OS).

Firefox OS

```
Mozilla/5.0 (Mobile; rv:18.0) Gecko/18.0 Firefox/18.0
```

Firefox on Android

```
Mozilla/5.0 (Android; Mobile; rv:18.0) Gecko/18.0 Firefox/18.0
```

The most current case of user agent detection is to know if the device is a mobile to redirect the browser to a dedicated Web site tailored with mobile content. We recommend you to limit your detection to the simplest possible string by matching the substring `mobi`

in lowercase.

```
/mobi/i
```

If you are detecting on the client side with JavaScript, one possibility among many would be to do:

```
// Put the User Agent string in lowercase
var ua = navigator.userAgent.toLowerCase();
// Better to test on mobi than mobile (Firefox, Opera, IE)
if (/mobi/i.test(ua)) {
// do something here
} else {
// if not identified, still do something useful
}
```

You might want to add more than one token in the `if`

statement.

```
/mobi|android|touch|mini/i.test(ua)
```

Remember that whatever the number of tokens you put there, you will fail at a point in the future. Some devices will not have JavaScript, will not have the right token. The pattern or the length of the token was not as you had initially planned. The stones on the path are plenty, choose the way of the simplicity.

## Summary: UA detection Checklist Zen

- Do not detect user agent strings
- Use responsive design for your new mobile sites (media queries)
- If you are using a specific feature, use feature detections to enhance, not block
- And if finally you are using UA detection, just go with the most simple and generic strings.
**Always**provide a working fallback whatever the solutions you chose are.

Practice. Learn. Imagine. Modify. And start again. There will be many road blocks on the way depending on the context, the business requirements, the social infrastructure of your own company. Keep this checklist close to you and give the Web to more people.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 24 comments

RonSeptember 12th, 2013 at 03:25Ronan CreminSeptember 16th, 2013 at 03:48Karl DubostSeptember 16th, 2013 at 08:10Ronan CreminSeptember 16th, 2013 at 08:35Olivier MenguéSeptember 12th, 2013 at 04:39RonanSeptember 12th, 2013 at 05:49Karl DubostSeptember 12th, 2013 at 06:22RonanSeptember 12th, 2013 at 07:03Ivan DejanovicSeptember 13th, 2013 at 02:15Will MitchellSeptember 13th, 2013 at 07:35Karl DubostSeptember 13th, 2013 at 08:48Karl DubostSeptember 13th, 2013 at 08:43Karl DubostSeptember 13th, 2013 at 12:04BridgetSeptember 15th, 2013 at 12:24RalfMCSeptember 13th, 2013 at 07:59Karl DubostSeptember 13th, 2013 at 11:58Ivan DejanovicSeptember 16th, 2013 at 02:53Karl DubostSeptember 16th, 2013 at 03:59Remi GrumeauSeptember 17th, 2013 at 14:08Karl DubostSeptember 17th, 2013 at 14:53Remi GrumeauSeptember 18th, 2013 at 00:20Karl DubostSeptember 18th, 2013 at 03:23Remi GrumeauSeptember 18th, 2013 at 01:41Karl DubostSeptember 18th, 2013 at 06:10