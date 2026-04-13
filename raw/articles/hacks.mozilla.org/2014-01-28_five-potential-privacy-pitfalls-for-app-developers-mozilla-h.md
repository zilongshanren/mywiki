---
title: Five Potential Privacy Pitfalls for App Developers – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2014/01/five-potential-privacy-pitfalls-for-app-developers/
author: Mozilla
published: '2014-01-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Fighting for data privacy — making sure people know who has access to their data, where it goes or could go, and that they have a choice in all of it — is part of Mozilla’s DNA. Privacy is an integral part of building an Internet where people come first.

“Individuals’ security and privacy on the Internet are fundamental and must not be treated as optional.” ~

[Mozilla Manifesto](principle #4)”

On January 28th, the world will celebrate Data Privacy Day — an international holiday intended to raise awareness and promote data privacy education. It is officially recognized in the United States, Canada, and 27 European countries.

As part of our own Data Privacy Day celebrations this year, we have created a developer-specific list of Privacy Pitfalls to watch out for:

## 1. More isn’t always better

Collecting lots of data is seductive but in a privacy context can create risk (the more you have, the more you need to protect) and a lot of additional work. A privacy policy, for example, may require you to publicly share:

- What personal information your app collects
- Why you are collecting it
- Where it will be stored (on the device or elsewhere)
- Who it will be shared with and why
- How long you will keep it
- How a user can have their data removed

What’s more, you are on the hook to make sure all of the things you’ve communicated are really happening.

The key is to collect only what you need. When you are in the planning stages for your app, document the data collection, usage and flows. You should be able to justify each piece of personal information and describe how it will be used. If you plan to collect personal information for future or extra features beyond core functions, always give users the ability to opt-out.

Finally, know which types of data collection require informed consent such as information about a user’s movements and activities through the use of location and movement sensors, sound, or activation of the device camera.

## 2. Avoid treating your user’s contacts as your own

“Share” buttons and social media sign-in widgets are ubiquitous in today’s apps and Web sites. And while these buttons may make it easier for users to share information, they are not an all-access pass into your user’s address book.

Respect for the people who use your software; allowing them to control what’s being shared and with whom, builds trust and loyalty. These two things have the potential to be exponentially more valuable than a random connection with a stranger.

## 3. Provide a fair trade for the data you collect

User data is undeniably valuable and collecting it isn’t inherently wrong, especially with consent. Oftentimes though, users are asked to trade their valuable personal data without much in return (sometimes, as in the address book example above, they may not even know they’re giving you anything).

Collecting data with a fair trade mindset — making sure the people who give you their information are getting something in return (features, a personalized experience, etc.) helps the user feel respected and in control — resulting in an invaluable sense of trust and loyalty.

## 4. Understand all the privacy conditions you yourself are agreeing to

If you use third party services, like analytics or ad networks, make sure you are aware of their data collection practices as well as your own — they could impact your users. Third party code or software development kits can contain code you aren’t aware of. Providing accurate information to your users on the data collected by these organizations should be part of your privacy policy, and disclosed as if you were collecting it yourself.

Best to identify third parties by name and to link to information about how to modify or delete the data they collect. You should also consider providing a means for your users to opt out of such tracking.

## 5. There is no “one policy fits all” when it comes to privacy

Despite your best intentions to respect user privacy, legal requirements and user expectations can vary widely – a challenge made especially acute now that apps are available to a global audience. While we can’t give you legal advice, we can share some of the nuggets we’ve found through our user research in different countries:

- In the US, non-technical consumers care more about their social circle tracking their online behavior than companies or the government.
- In Thailand, relatives share and swap devices freely with each other, with little desire to create individual accounts or erase their personal data.
- In Germany and most of Europe, consumers are quite sensitive about sharing their personal information with companies and governments, and those countries have strict laws to reflect that stance.
- In Brazil, the middle class is more concerned about thieves physically stealing their devices (particularly mobile phones) than about online piracy.

Ultimately, [talking to real users first](https://blog.mozilla.org/privacy/2013/05/21/exploring-the-emotions-of-security-privacy-and-identity/) can go a long way in making an app that truly reflects their privacy concerns. Engaging with real users not only reveals unique behaviors, but also digs into the motivations and emotions that drive these preferences.

In our experience, it can be hard for users to articulate how they feel about privacy. With the exception of privacy-sensitive countries/individuals, “privacy” may not always be top of mind. Rather than using the term “privacy” when talking to users, we’ve had success asking specific questions, such as who the user feels comfortable sharing personal information with and why, rather than to trying to get the participant to talk about privacy in an abstract way.

Do you have experiences related to these pitfalls? What others have you encountered in your work? Let us know in the comments!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 3 comments

MarcelJanuary 30th, 2014 at 09:17Chicago Website DevelopmentFebruary 18th, 2014 at 04:14ChristaFebruary 20th, 2014 at 16:51