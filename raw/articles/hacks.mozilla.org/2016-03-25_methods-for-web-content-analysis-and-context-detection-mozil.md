---
title: Methods for Web Content Analysis and Context Detection – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2016/03/methods-for-web-content-analysis-and-context-detection/
author: Jonathan Hasbun
published: '2016-03-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This project was part of Portland State University’s senior capstone program. It is the work of seven students over the course of six months. For the duration of the project we worked with a Mozilla adviser, [Dietrich Ayala](https://twitter.com/dietrich), to keep on track with the project’s original requirements. The team was composed of the following students:

[Abrahams, Katie](http://www.linkedin.com/in/katieabrahams): Research Lead[Finch, Donovan](https://linkedin.com/in/finchd): SQA Team / Research[Hanchett, Charles](https://www.linkedin.com/in/charles-hanchett-a6494b40): SQA Team / Research[Hasbun, Jonathan](http://www.linkedin.com/in/jhasbun): Team Lead / Dev Team / Research[Mierzwik, Bryan](https://www.linkedin.com/in/mierzwik): Dev Team / Research[Sorg, Tyler](https://www.linkedin.com/in/tylersorg): Dev Team / Research[Torkian, Kiarash](https://github.com/Kiarasht): Dev Team / Research

### Overview and Goals of the Project

This project was a research-intensive proof of concept for a feature that would expand the reader mode to content beyond articles, for one of many Mozilla projects. We set out to solve the problem of how to “put the internet back in the hands of the user”, as web pages are often bloated with unnecessary content that degrades the user experience.

In developing nations with low-powered smartphones and slow internet connections, this can incur a high computing cost on browsing and affect battery life. In our research we divided the problem into four main areas: the quality of the user’s internet connection, the target device of the user, what content is important to the user, and is the data accessible to those with disabilities.

For example, the graph below shows that the difference on one of the web pages tested with and without reader mode was **nearly 6mb**.

![Data Usage](../../assets/d0f5cf6d7517c492.png)


By understanding what part of a web page is content and what is not, we can limit data usage, by only downloading the relevant content. In addition, if we can grab only what’s necessary from a site, it opens the possibility of the user’s device optimizing the view of this data.

This transformation of the data for contextual presentation can be used to improve accessibility, or enable alternate browser models. We outline several possible efficient methods of content analysis. Ultimately, we found that currently available tools solve only a subset of the problems identified. However, by utilizing several of these tools and the concepts explored in our research paper, we believe it is possible to implement such a feature.

What does this mean for an everyday web developer? Imagine smarter tooling for content analysis, detection, and optimization that could be built as advanced features of the browser in the near future. Imagine developer tools that would make building website accessibility and platform-specific features far easier and less costly than it is today.

Read on to learn more about our findings and the research we designed to test our ideas.

### Installation & Usage

The process outlined in our paper is referred to as “Minimum Contextualization”, or contextualization for short. This process is split into three main phases: Content analysis, content filtration and content transformation. Each of these phases has several steps.

Phoenix-node is a command line application written in Node.js that we developed to analyze HTML document structure. It relies on Node.js 4.0+, the npm package manager, and the* jsdom* npm package and its dependencies.

- Install Node.js 4.0+ following the instructions for your environment:
[https://nodejs.org/](https://nodejs.org/) - Clone the Phoenix-node repository from
[https://github.com/cap7pdx/phoenix-node](https://github.com/cap7pdx/phoenix-node) - Install
*jsdom*into the source directory with ‘npm install jsdom’. A node_modules folder will be made. - Run phoenix-node parsing
[http://google.com](http://google.com)with ‘node alt.js’. This will print the DOM structure to the terminal.

![Phoenix Output](../../assets/c0ff84b8b32b207c.png)



### Research Findings

Our research identified three major phases in the contextualization process: content analysis, content filtration and content transformation. Our findings focus on content analysis. Content filtration and content transformation are not covered in our research.



![Contextualization](../../assets/73cce48b662e2465.png)


For content analysis, we recommend two distinct steps: The first step should identify which “Structure Group” a site falls into by utilizing cluster analysis of document structures. In the second step, one of several methods can be used to parse through the site to determine which content is essential for the user to understand its meaning. For example, if a site is placed into a cluster which is text-heavy and has little to no other content, then basic reader mode features are sufficient for this, such as shallow-text methods. Otherwise a more advanced method must be used, such as semantic segment detection (discussed further in our paper).

Through our research we were able to learn about the limitations inherent in modern reader mode techniques and the status of similar research. Our team’s recommended method for content analysis and context detection is to utilize a cluster analysis to group like pages in order to learn about the archetypal structure in a cluster and group sites with similar structures together.

Read the full paper here:

## 3 comments

André JaenischMarch 30th, 2016 at 13:20ZEE CenterApril 2nd, 2016 at 09:18EvanApril 12th, 2016 at 16:22