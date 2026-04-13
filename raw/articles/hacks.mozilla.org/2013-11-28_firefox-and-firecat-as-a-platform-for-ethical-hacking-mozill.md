---
title: Firefox and FireCAT as a Platform for Ethical Hacking – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/11/firefox-and-firecat-as-a-platform-for-ethical-hacking/
author: Maximiliano Soler
published: '2013-11-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Some years ago – in early 2007, while working as freelancers – we were challenged to do a penetration test on a web application. It was really simple but had a condition-based methodology, and therefore was impossible to use any automated tool; we could only use a web browser.

Our solution was to convert Firefox into a Platform for Ethical Hacking.

## How did we do it?

We searched the Web, looking for a solution that satisfied the requirements and obligations to not use automated tools. We found many, a lot of them being add-ons and extensions. Many of them were unknown, unnoticed and unofficial.

Having compiled some useful findings, our next challenge was to create something that maintained the essence of Mozilla Firefox: open, free and easy for everyone. The project was named [FireCAT (Firefox Catalog of Auditing exTensions)](http://firecat.toolswatch.org)

## What is FireCAT?

FireCAT is a mind map organized into different categories and subcategories with a variety of add-ons available. These are themed around application security auditing and assessment, adding news functionality, customizing your browser and providing the ability to adapt it to different user’s need.

### Current Status

The [latest version is 2.0](http://firecat.toolswatch.org/news.html), and was presented at Black Hat Arsenal during 2011. From the web site it is possible to list the content and browse the categories, directly accessing the add-ons on [Mozilla Add-ons](https://addons.mozilla.org/en-US/firefox/); you can also download the entire mind map with the categories:

### What’s New?

- Current Version: 2.0
- Add-ons: > 90
- Categories: 7
- Subcategories: 19

FireCAT v2.0 – [Firefox Catalog of Auditing exTensions
](http://firecat.toolswatch.org/the_catalog.html)

- Information Gathering
- Whois
- Location Info
- Enumeration & Fingerprint
- Data Mining
- Googling & Spidering

- Proxies & Web Utilities
- Editors
- Network Utilities
- Intrusion Detection System
- Sniffers
- Wireless
- Passwords
- Protocols & Applications

- Misc
- Tweaks & Hacks
- Encryption / Hashing
- Antivirus & Malware Scanner
- Anti Spoof
- Anti-phishing / Pharming / Jacking
- Automation
- Logs / History
- Backup & Synchronization
- Protection

- IT Security Related
- Application Auditing

## What can we find in the categories?

The 7 main categories are as follows:

### Information Gathering

An important part of the process of conducting vulnerability assessment or penetration testing is related to obtaining information in a passive or active way about our objective, to be analyzed later.

From the Firefox platform, we could identify IP addresses, query DNS, verify HTTP headers, generate reports of domains via Whois, use different search engines, and identify applications and versions from Web Server, modules, etc.

#### Example

![](../../assets/a95c2101941ac422.png)


“Show IP” shows the IP address(es) of the current page in the status bar. It also allows querying of custom services by IP (right mouse button) and hostname (left mouse button), like whois, netcraft, etc.

### Proxies & Web Utilities

Sometimes it’s necessary to use proxies to connect with different hosts or through networks for exaple using TOR to hide our real IP, analyze time responses, detect load balancer, etc.

#### Example

The User Agent Switcher extension adds a menu and a toolbar button to switch the user agent of the browser:

![](../../assets/566862ceeca821dc.png)


### Editors

From the ubiquitous FireBug to different JavaScript or XML editors, the available editors can help us to visualize and modify content as required.

#### Example

![](../../assets/daed25db946f0bf3.png)


The JavaScript Deobfuscator will show you what JavaScript gets to run on a web page, even if it is obfuscated and generated on the fly.

### Network Utilities

In this section you can use and connect with applications and services such as FTP, DNS and databases in real time.

### Miscellaneous

This section contains a lot of useful add-ons, for example tools to convert your ASCII into md5, sha1, base64, hex, etc., and methods to identify the WOT (Web of Trust) in a web site, guage reputation and ratings, modify your HTTP Referer, automate actions through Macros, and make backups of your configuration and installed addons.

#### Example

![](../../assets/3a6560156c0fa3aa.png)


The Certificate Patrol add-on reveals when certificates are updated, so you can ensure it was a legitimate change.

### IT Security Related

Sometimes it is necessary to use search engines to find information within some Web sites, content related to errors, configurations, and news vulnerabilities by CVE.

### Application Auditing

The HackBar is probably the best known addon in this group, but I recommend you take a deeper look because many of them are useful. For example, Exploit-Me’s suite to perform vulnerability analysis of cross-site scripting and SQL Injection.

#### Example

The SQLite Manager allows you to manage any SQLite database on your computer.

## Recommended add-ons

The top ten recommended add-ons would be:

[Firebug](https://addons.mozilla.org/en-US/firefox/addon/1843)[Web Developer](https://addons.mozilla.org/en-US/firefox/addon/60)[HackBar](https://addons.mozilla.org/en-US/firefox/addon/3899)[FoxyProxy](https://addons.mozilla.org/en-US/firefox/addon/2464)[Exploit Me](http://labs.securitycompass.com/index.php/exploit-me)[Tamper Data](https://addons.mozilla.org/en-US/firefox/addon/966)[iMacros for Firefox](https://addons.mozilla.org/en-US/firefox/addon/3863)[SQLite Manager](https://addons.mozilla.org/en-US/firefox/addon/5817)[Live HTTP Headers](https://addons.mozilla.org/en-US/firefox/addon/3829)[PassiveRecon](https://addons.mozilla.org/en-US/firefox/addon/6196)

## Final Words

I invite you to explore the different add-ons and extensions available, identifying which ones are most interesting and helpful for your work, and their relative performance and compatibilities. Firefox was a great help during our work!

If you decide to install a large amount of add-ons, memory usage might be a problem: consider this carefully.

Feel free to send us your comments and recommendations for new options to add to the mind map!

## About Maximiliano Soler

Security Researcher & Enthusiast. FireCAT | OWASP Mantra | #ToolsWatch | #EKOParty Fan

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

dotnetCarpenterNovember 29th, 2013 at 00:55Robert Nyman [Editor]November 29th, 2013 at 01:49