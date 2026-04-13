---
title: 2020 MDN Web Developer Needs Assessment now available – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2020/12/2020-mdn-web-developer-needs-assessment-now-available/
author: Chris Mills
published: '2020-12-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The 2020 MDN Web Developer Needs Assessment (DNA) report is now available! This post takes you through what we’ve accomplished in 2020 based on the findings in the inaugural report, key takeaways of the 2020 survey, and what our next steps are as a result.

## What We’ve Accomplished

In December 2019, [Mozilla released](https://insights.developer.mozilla.org/) the first Web Developer Needs Assessment survey report. This was a very detailed study of web developers globally and their main pain points with the web platform, designed with input from nearly 30 stakeholders representing [product advisory board](https://developer.mozilla.org/en-US/docs/MDN/MDN_Product_Advisory_Board) member organizations (and others) including browser vendors, the W3C, and industry. You can find a full list in the [report itself](https://mdn-web-dna.s3-us-west-2.amazonaws.com/MDN-Web-DNA-Report-2019.pdf) (PDF, 1.4MB download).

We learned that while more than 3/4 of respondents are very satisfied or satisfied with the Web platform, their 4 biggest frustrations included having to support specific browsers (e.g., IE11), dealing with outdated or inaccurate documentation for frameworks and libraries, avoiding or removing a feature that doesn’t work across browsers, and testing across browsers.

Mozilla and other web industry orgs took action based on these results, for example:

- MDN prioritized documentation projects that were most needed by the industry.
- Mozilla’s engineering team incorporated the findings into future browser engineering team planning and prioritisation work.
- A cross-industry effort improved cross-browser support for Flexbox (see
[Closing the gap (in flexbox)](https://blogs.igalia.com/svillar/2020/10/01/closing-the-gap-in-flexbox/)for more details). - Google used the results to help understand and prioritize the key areas of developer frustration, and used the developer satisfaction scores as a success metric going forward.
- The results provided valuable input to several standardization and pre-standardization discussions at W3C’s annual TPAC meeting.
- Microsoft used the Web DNA as one of their primary research tools when planning investments in the web platform and the surrounding ecosystem of content and tools (for example
[webhint.io](https://webhint.io/)), and it directly impacted how they now think about areas like cross-browser testing, legacy browser compatibility, best practices hinting, and more.

## The 2020 Survey Results

The inaugural results were so useful that in 2020 we decided to run it again, with the same level of collaboration between browser vendors and other stakeholders.

This year we expanded the survey to include some new questions about accessibility tools and web testing, which were requested by some of the survey stakeholders as key areas of interest that should be explored more this time round. We also hired an experienced data scientist to conduct analysis and employ data science best practices.

We ran the survey from October 12 through November 2, 2020 and secured a similarly wide distribution of respondents.

Browser compatibility remains the top pain point, and it is also interesting to note that overall satisfaction with the platform hasn’t changed much, with 77.7% being very satisfied or satisfied with the Web in 2020.

New for this year are the results of our segmentation analysis of the needs which yielded seven, distinct segments. Each one has wildly different needs that surface as the most frustrating when compared to the overall mean scores:

**Documentation Disciples**— Their top frustrations are outdated documentation for frameworks and libraries and outdated documentation for HTML, CSS, and JavaScript, as well as supporting specific browsers.**Browser Beaters**— Their top frustrations are clustered around issues with browser compatibility, design and layout. Like Document Disciples, they also find having to support specific browsers more frustrating than the overall mean.**Progressive Programmers**— Their top frustrations are clustered around lack of APIs, lack of support for Progressive Web Apps (PWAs), and using web technologies. For them, browser related needs were typically less frustrating than the overall mean.**Testing Technicians**— Needs statements relating to testing, whether end-to-end, front-end, or testing across browsers, caused the most frustration for this segment. Their top frustrations are clustered around issues with browser compatibility, design and layout. Like Progressive Pros, this segment also finds browser compatibility needs less frustrating than the overall mean, with the exception of testing across browsers.**Keeping Currents**— The need statements that this segment found most frustrating were keeping up with a large number of new and existing tools and frameworks and keeping up with changes to the web platform. Sticking with the themes from 2019, this segment is concerned with the Pace of Change of the web platform.**Performance Pushers**— Needs statements relating to performance and bugs are the top frustrations for this segment. Needs related to testing were rated as less frustrating than the overall mean, but discovering bugs not caught during testing is higher than the overall mean, though the pinpointing performance issues and implementing performance optimization are the top frustrations.**Regulatory Wranglers**— This is the more eclectic segment, with a bigger assortment of needs rating higher than the overall mean. However, compliance with laws and regulations for managing user data is the most frustrating need. Closely following that are needs relating to security measures with tracking protection, data storage, and authentication causing frustrations.

## What’s Next

We are aiming to follow up on key findings with further research in the next few months. This will involve picking some key areas to focus on, and then performing user interviews and further analysis to allow us to drill down into key areas of frustration to see what the way forward is to mitigating them.

Potential areas to research include qualitative studies about:

- Testing
- Documentation
- The pace of change on the web platform
- Frustrations around design and layout issues across browsers

## Get the report!

To get the full report, see [https://insights.developer.mozilla.org/](https://insights.developer.mozilla.org/) for HTML and PDF versions, and more besides. The 2019 report and our Browser Compatibility follow-up report are still available if you want to compare and contrast.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.