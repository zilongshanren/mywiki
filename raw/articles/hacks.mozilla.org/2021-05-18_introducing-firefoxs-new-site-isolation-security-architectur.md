---
title: Introducing Firefox’s new Site Isolation Security Architecture – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2021/05/introducing-firefox-new-site-isolation-security-architecture/
author: Anny Gakhokidze
published: '2021-05-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Like any web browser, Firefox loads code from untrusted and potentially hostile websites and runs it on your computer. To protect you against new types of attacks from malicious sites and to meet the security principles of Mozilla, we set out to redesign Firefox on desktop.

Site Isolation builds upon a new security architecture that extends current protection mechanisms by separating (web) content and loading each site in its own operating system process.

This new security architecture allows Firefox to completely separate code originating from different sites and, in turn, defend against malicious sites trying to access sensitive information from other sites you are visiting.

In more detail, whenever you open a website and enter a password, a credit card number, or any other sensitive information, you want to be sure that this information is kept secure and inaccessible to malicious actors.

As a first line of defence Firefox enforces a variety of security mechanisms, e.g. the [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) which prevents adversaries from accessing such information when loaded into the same application.

Unfortunately, the web evolves and so do the techniques of malicious actors. To fully protect your private information, a modern web browser not only needs to provide protections on the application layer but also needs to entirely separate the memory space of different sites – the new Site Isolation security architecture in Firefox provides those security guarantees.

## Why separating memory space is crucial

In early 2018, security researchers disclosed two major vulnerabilities, known as [Meltdown](https://en.wikipedia.org/wiki/Meltdown_(security_vulnerability)) and [Spectre](https://en.wikipedia.org/wiki/Spectre_(security_vulnerability)). The researchers exploited fundamental assumptions about modern hardware execution, and were able to demonstrate how untrusted code can access and read memory anywhere within a process’ address space, even in a language as high level as JavaScript (which powers almost every single website).

While band-aid countermeasures deployed by OS, CPU and major web browser vendors quickly neutralized the attacks, they came with a performance cost and were designed to be temporary. Back when the attacks were announced publicly, Firefox teams promptly [reduced the precision of high-precision timers and disabled APIs that allowed such timers to be implemented](https://blog.mozilla.org/security/2018/01/03/mitigations-landing-new-class-timing-attack/) to keep our users safe.

Going forward, it was clear that we needed to fundamentally re-architecture the security design of Firefox to mitigate future variations of such vulnerabilities.

Let’s take a closer look at the following example which demonstrates how an attacker can access your private data when executing a Spectre-like attack.

![Two hand-drawn diagrams, with the first labeled “Without Site Isolation, we might load both of these sites in the same process :( ”. Two browser windows with partially visible sites “attacker.com” and “my-bank” partial site, are loaded in the same process - process 16. On top of the banking window, there is a cartoon face that looks happy, personifying the browser. The attacker site window contains a face that is looking at the banking window, with a mischievous smile. In the second diagram, labeled “Attacker.com executes a sophisticated attack”, we see the same two browser windows loaded in process 16 and a 1 column table labelled “memory where my-bank’s data is stored in process 16” underneath the banking window. It has two entries: “credit card info” and “login password”. A hand extending from the malicious site reaches toward the table (aka memory of the second window), signifying that the malicious site is able to access sensitive data belonging to the banking window because it is in the same process. The personified browser character is looking towards the malicious site, and exhibits feelings of concern and worry, with exclamation marks floating around the face.](../../assets/8674eeccee1a5129.jpg)


Without Site Isolation, Firefox might load a malicious site in the same process as a site that is handling sensitive information. In the worst case scenario, a malicious site might execute a Spectre-like attack to gain access to memory of the other site.

Suppose you have two websites open – www.my-bank.com and www.attacker.com. As illustrated in the diagram above, with current web browser architecture it’s possible that web content from both sites ends up being loaded into the same operating system process. To make things worse, using a Spectre-like attack would allow attacker.com to query and access data from the my-bank.com website.

Despite existing security mitigations, the only way to provide memory protections necessary to defend against Spectre-like attacks is to rely on the security guarantees that come with isolating content from different sites using the operating system’s process separation.

## Background on Current Browser Architecture

Upon being launched, the Firefox web browser internally spawns one privileged process (also known as the parent process) which then launches and coordinates activities of multiple (web) content processes – the parent process is the most privileged one, as it is allowed to perform any action that the end-user can.

This multi-process architecture allows Firefox to separate more complicated or less trustworthy code into processes, most of which have reduced access to operating system resources or user files. As a consequence, less privileged code will need to ask more privileged code to perform operations which it itself cannot.

For example, a content process will have to ask the parent process to save a download because it does not have the permissions to write to disk. Put differently, if an attacker manages to compromise the content process it must additionally (ab)use one of the APIs to convince the parent process to act on its behalf.

In great detail, (as of April 2021) Firefox’s parent process launches a fixed number of processes: eight web content processes, up to two additional semi-privileged web content processes, and four utility processes for web extensions, GPU operations, networking, and media decoding.

While separating content into currently eight web content processes already provides a solid foundation, it does not meet the security standards of Mozilla because it allows two completely different sites to end up in the same operating system process and, therefore, share process memory. To counter this, we are targeting a Site Isolation architecture that loads every single site into its own process.

![A hand drawn diagram titled “Loading Sites with Current Browser Architecture”. On the left hand-side, from top to bottom, there are four browser windows with different sites loaded. The first window, www.my-bank.com, is loaded in process 3. The second window is loaded in process 4. The third window is loaded in process 5. The last window with a url - “www.attacker.com” - is loaded in process 3, same as the first window. On the right hand-side of the drawing, there is a table titled “List of Content Processes”. The table contains two columns: “site” and “pid”, which stands for process id. In the table, the first window, my-bank.com, and the last attacker.com window have the same PID.](../../assets/c684c90bee2b2160.jpg)


Without Site Isolation, Firefox does not separate web content into different processes and it’s possible for different sites to be loaded in the same process.

Imagine you open some websites in different tabs: www.my-bank.com, www.getpocket.com, www.mozilla.org and www.attacker.com. As illustrated in the diagram above, it’s entirely possible that my-bank.com and attacker.com end up being loaded in the same operating system process, which would result in them sharing process memory. As we saw in the previous example, with this separation model, an attacker could perform a Spectre-like attack to access my-bank.com’s data.

![A hand drawn diagram titled “Loading Subframes With Current Browser Architecture”. There is one browser window drawn. The window, www.attacker.com, embeds a page from a different site, www.my-bank.com. The top level page and the subframe are loaded in the same process - process 3.](../../assets/da2216e255c0da16.jpg)


Without Site Isolation, the browser will load embedded pages, such as a bank page or an ad, in the same process as the top level document.

While straightforward to understand sites being loaded into different tabs, it’s also possible that sites are embedded into other sites through so-called subframes – if you ever visited a website that had ads on it, those are probably subframes. If you ever had a personal website and you embedded a YouTube video with your favourite song within it, the YouTube video was embedded in a subframe.

In a more dangerous scenario, a malicious site could embed a legitimate site within a subframe and try to trick you into entering sensitive information. With the current architecture, if a page contains any subframes from a different site, they will generally be in the same process as the outer tab.

This results in both the page and all of its subframes sharing process memory, even if the subframes originate from different sites. In the case of a successful Spectre-like attack, a top-level site might access sensitive information it should not have access to from a subframe it embeds (and vice-versa) – the new Site Isolation security architecture within Firefox will effectively make it even harder for malicious sites to execute such attacks.

## How Site Isolation Works in Firefox

When enabling Site Isolation in Firefox for desktop, each unique site is loaded in a separate process. In more detail, loading “https://mozilla.org” and also loading “http://getpocket.com” will cause Site Isolation to separate the two sites into their own operating system process because they are not considered “same-site”.

Similarly, “https://getpocket.com” (note the difference between http and https) will also be loaded into a separate process – so ultimately all three sites will load in different processes.

For the sake of completeness, there are some domains such as “.github.io” or “.blogspot.com” that would be too general to identify a “site”. This is why we use a [community-maintained](https://github.com/publicsuffix/list) list of effective top level domains (eTLDs) to aid in differentiating between sites.

Since “github.io” is listed as an eTLD, “a.github.io” and “b.github.io” would load in different processes. In our running examples, websites “www.my-bank.com” and “www.attacker.com” are not considered “same-site” with each other and will be isolated in separate processes.

![Two hand-drawn diagrams, with the first labeled “With Site Isolation, we will load these sites in different processes”. It shows two browser windows, one www.attacker.com , loaded in process 5, and www.my-bank.com loaded in process 16. On top of the banking window, there is a cartoon face that looks happy, personifying the browser. In contrast, the webpage area of the www.attacker.com window, contains a face that is looking at the banking window, with a mischievous smile. In the second diagram, labeled “Attacker.com tries to execute a sophisticated attack”, we see the same two browser windows. There is a 1 column table labelled “memory where my-bank’s data is stored in process 16” underneath the banking window . It has two entries: “credit card info” and “login password”. A hand extending from the malicious site tries to reach towards the table (aka memory of the banking window), but is unable to reach it, due to the process boundary. The face of the malicious site is frowning and looks unhappy, while the face, representing the browser, continues to look happy and carefree. The second window’s data is safe from the malicious site.](../../assets/4139200cd07eaa0b.jpg)


With Site Isolation, Firefox loads each site in its own process, thereby isolating their memory from each other, and relies on security guarantees of the operating system.

Suppose now, you open the same two websites: www.attacker.com and www.my-bank.com, as seen in the diagram above. Site isolation recognizes that the two sites are not “same-site” and hence the site isolation architecture will completely separate content from attacker.com and my-bank.com into separate operating system processes.

This process separation of content from different sites provides the memory protections required to allow for a secure browsing experience, making it even harder for sites to execute Spectre-like attacks, and, ultimately, provide a secure browsing experience for our users.

![The window, www.attacker.com, embeds a page from a different site, www.my-bank.com. The top level page is loaded in process 3 and the subframe corresponding to the bank site is loaded in process 5. The two sites are, thus, isolated from each other in different operating system processes.](../../assets/0d00fa2d04fdd4b7.jpg)


With Site Isolation, Firefox loads subframes from different sites in their own processes.

Identical to loading sites into two different tabs is the separation of two different sites when loaded into subframes. Let’s revisit an earlier example where pages contained subframes, with Site Isolation, subframes that are not “same-site” with the top level page will load in a different process.

In the diagram above, we see that the page www.attacker.com embeds a page from www.my-bank.com and loads in a different process. Having a top level document and subframes from different sites loaded in their own processes ensures their memory is isolated from each other, yielding profound security guarantees.

## Additional Benefits of Site Isolation

With Site Isolation architecture in place, we are able to bring additional security hardening to Firefox to keep you and your data safe. Besides providing an extra layer of defence against possible security threats, Site Isolation brings other wins:

- By placing more pages into separate processes, we can ensure that doing heavy computation or garbage collection on one page will not degrade the responsiveness of pages in other processes.
- Using more processes to load websites allows us to spread work across many CPU cores and use the underlying hardware more efficiently.
- Due to the finer-grained separation of sites, a subframe or a tab crashing will not affect websites loaded in different processes, resulting in an improved application stability and better user experience.

## Going Forward

We are currently testing Site Isolation on desktop browsers Nightly and Beta with a subset of users and will be rolling out to more desktop users soon. However, if you already want to benefit from the improved security architecture now, you can enable it by downloading the Nightly or Beta browser from [here](https://www.mozilla.org/firefox/channel/desktop/) and following these steps:

**To enable Site Isolation on Firefox Nightly:**

- Navigate to about:preferences#experimental
- Check the “Fission (Site Isolation)” checkbox to enable.
- Restart Firefox.

**To enable Site Isolation on Firefox Beta or Release:**

- Navigate to about:config.
- Set `fission.autostart` pref to `true`.
- Restart Firefox.

For technical details on how we group sites and subframes together, you can check out our new process manager tool at “about:processes” (type it into the address bar) and follow the project at [https://wiki.mozilla.org/Project_Fission](https://wiki.mozilla.org/Project_Fission).

With Site Isolation enabled on Firefox for Desktop, Mozilla takes its security guarantees to the next level and protects you against a new class of malicious attacks by relying on memory protections of OS-level process separation for each site. If you are interested in contributing to Mozilla’s open-source projects, you can help us by filing bugs [here](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core&bug_type=defect&short_desc=%5bFission%5d&blocked=fission-dogfooding) if you run into any problems with Site Isolation enabled.

## Acknowledgements

Site Isolation (Project Fission), has been a massive multi-year project. Thank you to all of the talented and awesome colleagues who contributed to this work! It’s a privilege to work with people who are passionate about building the web we want: free, inclusive, independent and secure! In particular, I would like to thank Neha Kochar, Nika Layzell, Mike Conley, Melissa Thermidor, Chris Peterson, Kashav Madan, Andrew McCreight, Peter Van der Beken, Tantek Çelik and Christoph Kerschbaumer for their insightful comments and discussions. Finally, thank you to Morgan Rae Reschenberg for helping me craft alt-text to meet the high standards of our web accessibility principles and allow everyone on the internet to easily gather the benefits provided by Site Isolation.

## About Anny Gakhokidze

Senior Platform Engineer who works on Firefox's Site Isolation and DOM-related features.