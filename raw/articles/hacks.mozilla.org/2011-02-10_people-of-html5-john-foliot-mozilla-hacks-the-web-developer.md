---
title: People of HTML5 – John Foliot – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/02/people-of-html5-john-foliot/
author: Chris Heilmann
published: '2011-02-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 needs spokespeople to work. There are a lot of people out there who took on this role, and here at Mozilla we thought it is a good idea to introduce some of them to you with a series of interviews and short videos. The format is simple – we send the experts 10 questions to answer and then do a quick video interview to let them introduce themselves and ask for more detail on some of their answers.

![john foliot](../../assets/fdb36a177f265e35.jpg)

[John Foliot](http://john.foliot.ca/) co-chair of the [subcommittee on the accessibility of media elements in HTML5](http://www.w3.org/WAI/PF/HTML/wiki/Media_Sub-Group) and well-known accessibility warrior of the wild wild web.

John’s been around the web, mailing lists and W3C meetings for longer than he’d care to remember and has always been a voice of reason when it comes to making the web accessible for everyone and still use new technologies. As this is a topic not often covered in the HTML5 context we thought it a good idea to bring up.

## The video interview

You can [see the video on any HTML5 enabled device here](http://vid.ly/4h9d5v) (courtesy of vid.ly).

## Ten questions about HTML5 for John Foliot

### 1) There is quite some confusion going on about what HTML5 is. Even the W3C shot an own goal with the release of the HTML5 logo and describing it as a branding for modern development that encompassed other technologies. What is your definition of HTML5?

Personally, HTML5 is the next major iteration of HTML – Hyper Text Markup Language – which will be standardized by the W3C in due course. It will effectively take over from HTML4.01/XHTML1.1, which [has not been updated since December 1999](http://www.w3.org/TR/html401/). It is one of the core standards that support today’s Open Web Technologies.

I understand and accept however that in terms of marketing and mass communication, having a term that describes the idea of the current larger eco-structure is by necessity going to be abstract. The conversation around naming has gone on for some time now, and I suspect that most developers remotely interested already know that the stack of Open Web Technologies we are using needs a name (my buddy Bruce Lawson dubbed it [NEWT](http://www.brucelawson.co.uk/2010/meet-newt-new-exciting-web-technologies/)).

But the horse was already out of the gate, and HTML5 is the name. So when communicating with developers in general today, I believe we all understand what is meant by HTML5. HTML5 has also become the way the mainstream thinks of what it is we are doing, so I really don’t worry too much about a marketing name. Over time, a new buzz word will emerge, the world will move on, and HTML5 will mean the standard for hyper text markup language – fifth iteration.

### 2) There seems to be two battling sources of truth about HTML5. The WHATWG and the W3C. When would you consider which group to be more important? What is the relationship between them?

Their relationship? Complicated.

The relationship acknowledges that two diverse groups can share a common goal, and working together can lead to progress. But it is hard work.

The WHAT WG serves a useful – likely critical – role in the emergence and growth of many of the Open Web Technologies. With the support of many (but not all) of the browser vendors, a common sharing of technical ideas, including experiments and evaluation by multiple teams, leads to improvements in the technology. It is the place of the engineers, and it is accustomed to working in an Agile environment, which works well for engineers. It’s an exciting place where new ideas emerge and first get roughly specc’d out, and then refined, seeing greater support in developmental browsers, and then reaching released browser versions.

However, even if tentatively working, those specs may not yet be complete, even if being implemented; often implementation is varied from browser to browser, and shortcomings (sadly often with regard to accessibility) are often significant.

The specification WHAT WG are working is constantly evolving – which is good – but it makes it very difficult for large entities outside of the browser vendors to keep up. Large scale projects require more stability than what a “living specification” can provide, as by its nature that specification is in constant change. Witness [this recent comment on a developer’s blog](http://blog.millermedeiros.com/2011/01/ipad-is-the-new-ie6/):

“The worse part of it is that you can’t simply search blogs/forums or look the documentation to figure out how to solve the problems, since “nobody” knows how to do those things, information gets outdated really fast with the release of a new OS version, documentations are very poor and doesn’t cover edge-cases, specs are constantly changing and different versions of iOS adopt a different set of rules…” – and that was just trying to get <video> to work properly on the iPad.


As well, by organization and politics, not all vested interests are part of the WHAT WG process, which can be problematic but not insurmountable.

Microsoft is not part of the WHAT WG, and likely never will be. We can rail on about the problems that IE has wrought upon us, but with a current majority market-share we simply cannot ignore it. So the WHAT WG is somewhat ham-strung by this situation.

I am known as being a staunch W3C supporter, as I believe very strongly that they best carry the banner for Web Technologies on a global level. The W3C is more than just websites in browsers; their Standards cover a wide scope of related technologies that all leverage the larger network, and whenever possible the W3C strives to ensure that they can all work together. It is a global organization that has financial support and backing from national governments, academic institutions, and technology companies that rely on the global internet network. I acknowledge however that like any large entity, it can sometimes struggle with rapid movement – bureaucracy being a necessary evil in any globally reaching organization.

For a younger person, involved in the daily race that is this new technology, this pace can be understandably frustrating, but engineers working in larger corporations such as IBM, Microsoft, etc. are accustomed to this already. Nobody has to like it, but it exists.

The WHAT WG explores ideas and works out wrinkles, W3C stabilizes, scrutinizes and “publishes” a benchmark that everyone can refer to. Both roles are important, but each is unique.

As to the “truth”, I will leave that to others to decide.

### 3) You are quite an advocate of accessibility. Do you see the new open technologies as a benefit for accessibility or are we forgetting about

it?

I think much of what HTML5 is starting to deliver will be of benefit to all users, including those using Assistive Technology. However much of what is promised is not yet supported in all browsers, and related technologies – Assistive Technologies – have a long way to come to leverage this benefit.

For example, most browser rendering engines do not do native processing of the landmark elements (I believe Firefox 4 uses an HTML5 rendering engine), and support for other [parts of the emerging spec that have an impact on accessibility is still lacking](http://www.html5accessibility.com/). All the more reason to get HTML5 Standardized; certainly to Candidate Recommendation at the W3C.

I think that some of the emergent stuff that the WHAT WG is working on occasionally falls short on accessibility concerns; thankfully less so now than when some of the earlier HTML5 work was undertaken.

Overall, I am generally thankful to see how much the awareness for accessibility has grown, and the generally productive dialog between engineers and accessibility specialists.

### 4) A lot of showcases of HTML5 show a certain effect but fall behind in basic accessibility concerns. There’s no keyboard interaction and a lack of testing for support. You find empty links pointing nowhere and HTML that is stored in the document for later use – like a whole list of error messages that get shown and hidden when needed. What could be done about this? What is your message to developers why keyboard access or even non-JavaScript fallbacks matter?

I think part of the problem, perhaps the biggest part, is lack of education. The barrier to entry for creating and posting to the web is extremely low: any fool can do it, and so even fools do – without knowing or understanding what it is that they really are doing. It is also hurt by web-sites and blogs that recommend some of these poor techniques as “the way to do…”, further perpetuating bad coding practice.

I think one of the other problems, especially with regard to accessibility issues, is that many developers (that have any kind of engineering background) have become very comfortable, even dependant on, the AGILE development process: code it, test it, break it, fix it, test it, break it, fix it,… I can’t count how many times I’ve heard “This is just our first iteration, we’ll get to the accessibility stuff in a future build.” The problem here is that accessibility is relegated to the role of ‘feature request’ instead of ‘core requirement’. Here again, it’s a larger education issue: mainstream developers need to understand and commit to making accessibility a core requirement, which then helps shape the functional and technical decisions that they will be making as their project evolves.

Keyboard access is an important requirement for many users, and increasingly not just users with disabilities. The massive growth in web content being created for mobile devices is helping make developers more aware of this fact. I challenge everyone reading this piece who creates web content to remove the battery from their wireless mouse for one day, and then test their site(s). This is perhaps one of the easiest “accessibility tests” any developer can do, as it does not require any special tools (hardware or software) for testing, and yet has a huge impact on both non-sighted users as well as users with various forms of mobility impairment.

With regard to JavaScript, the W3C Web Content Accessibility Guidelines 2 (WCAG 2) are more relaxed about JavaScript than WCAG 1 was. Virtually every browser out there today supports JavaScript, and client-side scripting is a necessary piece of today’s modern web infrastructure: remember that most Adaptive Technology interacts with these web browsers, so the pitfalls and problems of relying on JavaScript for ‘mission critical’ functionality are equally present for all users. Again, the real answer to this problem is education.

### 5) Let’s talk assistive technology. As markup and scripting should not only be targeted towards certain browsers we need to know what for example screen readers can do these days. How is the support for the new technologies?

First, I define Assistive Technology as a collection of off-the-shelf software tools, specialized programs, and alternate combinations of hardware; all are Assistive Technology: Dragon not only types when you talk, but provides a hands-free solution to UI interaction to those with severe mobility issues; screen readers are programs that communicate between browsers and other UI tools, and the operating system, leveraging the OS’s accessibility APIs; and Braille output bars connected to various devices allowing for a specialize output for those that require it. OS level offerings such as VoiceOver has been a boon to non-sighted users (allowing them to interact with their iPhones and iPads) and can also be considered AT.

Screen readers are sophisticated software, and while some screen readers such as NVDA are actively working to keep up with improvements in HTML5, the majority are sadly (I believe) waiting for a more formal standard to settle down before committing resources to re-factor their software. Whether this is the right decision or not is not really the question – it isn’t a question, it is an apparent fact.

It is a difficult chicken and egg scenario, and it is one of the reasons why I continue to advise that production class development proceed cautiously when using many of the new “HTML5” technologies. The silver lining in this story is the fact that ARIA has pretty good support in the current screen readers, and so developers can safely rely upon most of ARIA today, in concert with many of the HTML5 goodies. Many of the current UI JavaScript libraries (such as YUI3 and jQuery UI) are also helping out here, so working devs should be looking at a robust blend of current and new technology solutions.

### 6) One very important thing to make a document understandable for assistive technology is maintaining a logical order, especially when it comes to headings. With HTML5, we have sections and articles, hgroups and heading order in parts of the document rather than the full document. There is even implicit outlining of the document. How does assistive technology deal with that? Do we block out users by doing the right thing?

This is actually a very topical issue right now, as recently (January2011) many have come to [question the viability and usefulness of the hgroup element in HTML5](http://www.w3.org/html/wg/wiki/ChangeProposals/hgroup). W3C Process is such that any real dialog and discussion on this issue is being deferred to later this spring, as the Working Group is trying to clear older bugs and issues that were raised prior to the end of September 2010 cut-off date. I believe that currently no browser supports hgroup

The outline algorithm for headings is a great idea which has not yet seen implementation or support in Adaptive Technology. The idea is that the browser would heuristically know that an <hx> element was actually supposed to be at an appropriate level (say <h3>) based upon its surrounding ‘inheritance’.

This makes the outline and structure of a composite document more legible and understandable from the DOM on out to user-interfaces, whether the GUI of the browser, or Adaptive Technology. In effect the browsers would ‘re-write’ the heading level. The need for doing something like this has been understood and around for some time: [XHTML2 had proposed a numberless <h> element](http://www.w3.org/TR/xhtml2/mod-structural.html#edef_structural_h) that would have helped achieve the same goal, but for whatever reasons (likely the simple aversion to XHTML2 as being “wrong”) the idea was not carried into the work of the HTML5 group. Despite the lack of support for this feature today however, the appropriate usage of headings to ‘chunked’ content is still an important requirement for users (and especially screenreader users) – even if the actual heading order in the DOM today is ‘incorrect’ screen readers can and do use headings to facilitate in-page navigation. Today, it’s just not pretty (and sometimes – often – incorrectly ‘stacked’), but useful still the same.

Sections and Articles are 2 elements that have not yet really seen any kind of actual implementation in the browsers (although I believe that Firefox 4 will start to support them ‘natively’), so at this time they are still in the “this is conceptually a good idea” stage for all practical purposes. However, for browsers that do not have native support for these elements, they treat them as non-semantic divs, and so by adding ARIA landmark roles today they can be made quite navigable/accessible to AT. As a forward looking best practice I think that it is one of the things that developers can start implementing today – just [don’t forget the ARIA landmark roles](http://www.w3.org/WAI/PF/aria-practices/).

### 7) One thing I really loved when I found it in the HTML5 specs is a definition of figures and captions. However, when you use them and you want support for assistive technology you need to use ARIA labeled-by and assign a unique ID for every figure to connect it logically with the caption. That is extra effort a lot of developers will not go through. I find a lot of ARIA things very verbose. Are there any efforts to streamline the communication between the different standard bodies?

Absolutely!

ARIA as a specification/technology has been with us for a long time – almost 10 years now – but it has only been within the past 3 to 5 years that we’ve seen any real support in tools such as screen readers. ARIA however was built as a bridging technology, and one that was designed as much for remediation as forward development: go back and add the following bits of stuff to make your existing widget accessible. Because of this, yes, sadly, it is hardly elegant or compact. It has been however a chicken and egg problem since it was first addressed.

One of the significant pieces of work that the W3C Accessibility TaskForce has focused on has been ensuring that ARIA functionality is being integrated and mapped back to emergent HTML5 elements and attributes. While this work is not yet completed, there is a commitment to ensure that it is completed before HTML5 (the markup language) becomes a full recommendation.

Looking at the 2 examples you pointed out – figures and captions – the longer range plan is that these will map directly to the browser parsers and on to the Accessibility APIs, so that down the road they will simply “work” as advertised on the tin.

Adding ARIA attributes today is a belt and suspenders approach to both future-proof your content, but also ensure that it is accessible today. In many ways, it is very similar to the [vendor prefixes used in CSS3](http://peter.sh/experiments/vendor-prefixed-css-property-overview/): the ideal is to simply declare the property, but because it is still emergent technology, today we need to prepend the property with a vendor prefix (as in, for example: -moz-margin-end, -webkit-margin-end – where you must declare it twice in your style sheet to target both browsers). Same basic idea: yes, more work for developers, but there is no easy answer.

### 8) What do you consider the biggest problem of HTML5 video and audio to date? Is it the lack of options to protect premium content? Or the lack of a supported format for subtitling and captioning? Encoding woes?

Actually, I think all of the above contribute to a lack of maturity today.

The encoding issue will remain (I believe) a complicated political dance for some time into the future, with the average content producer left with no choice but to encode twice if they want to use <video> natively for all browsers. HTML5 currently lacks a means to fully support [the identified needs of users with various need](http://www.w3.org/WAI/PF/HTML/wiki/Media_Accessibility_Requirements#Alternative_Content_Technologies), although the proposed <track> element is certainly going to help here (but AFAIK no browser is supporting it today,or the ability to extract <track> data via a native interface).

I fear that the time-stamp format is a debate not yet completed (despite WHAT WG’s overwhelming support for WebSRT, err WebVTT, or whatever they decide to call it next). I think this was all but guaranteed when the SMTPE (Society of Motion Picture and Television Engineers) announced their industry supported SMPTE Time Text Format, based upon TTML. When commercial content providers make up their own minds about a time format,one would suspect that the browser vendors (pressured by online content distributors) will pay attention (especially given the current mood towards web captioning in Washington). While no browser today has staked a firm either/or position here, I get a sense that at least Microsoft will likely support both.

Issues surrounding DRM and parental controls – admittedly unpopular with a generation used to Pirate Bay and torrent feeds – are both issues that should be addressed,but likely will not be any time soon, further retarding widespread implementation and uptake in my opinion: commercial content providers will want *some* form of DRM, even if it can be hacked – the hacking becoming as much the criminal act as taking the digital asset.

Meanwhile, alternative solutions to the native <video> solution, from Flash and Silverlight to QuickTime itself, are quietly developing and shipping DRM solutions to clients eager to have this form of protection for their content – just look at Netflix. What I find curious is that many of those loud voices decrying DRM have no issue buying MP3s from iTunes (which can only be shared on 3 machines registered with Apple).

### 9) Canvas seems to be another big accessibility issue. Do you know of anything that is being done to make the changes you plot onto a canvas element understandable to assistive technology? Does SVG suffer from the same drawbacks?

Yes, Canvas remains a tricky accessibility challenge. Sadly, I’ve not been as focused on that aspect as I have on the media stuff, but I have faith and trust in the accessibility folk who are working out the kinks. RichardS chwerdtfeger (IBM) is the chair of the Canvas Accessibility sub-team and is a very smart engineer, and all of the browser vendors are in active discussion in that sub-team. My understanding is that there is a general consensus on the subtree DOM, although cross browser support for the solution is not yet there. There remains issues with caret focus and textMetrics interaction with screen magnifiers, as well as how to convey absolute positioning of all content to screen magnifiers and screenreaders who make use of Braille.

SVG, as a technology, is very different than Canvas and for the most part there are few accessibility issues with SVG. There’s [a good over-view of accessibility Features of SVG](http://www.w3.org/TR/SVG-access/) available.

### 10) The silver bullet for safely using new technologies seems to be object detection. You test if the browser supports something before you apply it. This never worked with assistive technology. Why is that the case? Why can’t we just say `if(window.screenreader)`

?

There are a number of reasons why this is not feasible.

For one, “screenreader” is a class of software tools that all behave slightly differently. Yes, today in the English speaking “Western” world,the JAWS software package holds a commanding share, but alternatives such as WindowEyes, Hal/Supernova, ZoomText and upstarts like [NVDA](http://www.nvda-project.org/) and Serotek’s [SAToGo](http://www.satogo.com/en/) are challenging the status quo. Yet none of these tools behave in exactly the same way, and at times their approach to user-interaction can differ greatly. Add foreign language tools such as the Korean [Sense Reader Professional](http://aheu.org/tag/sensereader/) and the Brazilian [Leitor de Telas](http://www.inclusaodigital.gov.br/noticia/leitor-de-telas-esta-disponivel-para-download-gratuito-no-portal-do-ministerio-das-comunicacoes) – to name but two – and sniffing for a screen reader becomes somewhat futile: if you know I am using SAToGo (for example), what does that mean to you as a developer, exactly?

Things get worse however, as not only do you need to account for ‘brand’ of screenreader, but also version. While WebAIM’s [Screen Reader Survey](http://webaim.org/projects/screenreadersurvey/) last year confirmed that most users keep their software up-to-date (74.6% within the first year), that still leaves almost 1 in 4 using software that can be as much as 3 years old or older. Developers need to remember as well that screenreaders are not part of the browser, but rather an OS level software tool that interacts not only with the browser, but also with other tools such as text editors, spread-sheet applications, and other productivity tools on their computers.

Finally what of VoiceOver? The OS level screen reading option from Apple is present on virtually every system they ship today, from OSx to iOS – there is no guarantee that simply because it is there, it is being used – or that the person using it is in fact blind. In fact many sighted users will have a legitimate need or desire to use screen reading technology, as VoiceOver has confirmed, so custom tailoring an ‘experience’ targeted to screen readers is sadly an effort not worth pursuing – you will continue to miss as often as you hit. (It kind of reminds me of web sites that will force an alternative version of their site targeted and optimized to mobile devices, and provide no means of getting to the actual desktop version of the site, even if the user wants that).

What I tell developers is this: code to standards, think about graceful degradation as well as progressive enhancement, and remember the original three legged stool approach to web development: the separation of content, design and scripting. I remind them that people with disabilities have a social reasonability to keep their software relatively up-to-date as well (no more or less so than any other user – who supports Netscape 4 today?) and/but as a designer/developer you must always be considering the “PlanB” for user interaction – if “Plan A” fails, what is “Plan B”?

Do you know anyone I should interview for “People of HTML5”? Tell me on Twitter: [@codepo8](http://twitter.com/codepo8)


## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 2 comments

Henri SivonenFebruary 21st, 2011 at 07:37JohnJune 4th, 2011 at 07:11