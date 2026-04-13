---
title: The JavaScript Specification has a New License – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2022/06/the-specification-for-javascript-has-a-new-license/
author: Yulia Startsev
published: '2022-06-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Ecma International recently approved the 2022 standard of ECMAScript. There is something new in this edition that hasn’t been part of prior editions, but this isn’t a new programming feature.

In March of this year, Ecma International accepted a proposal led by Mozilla for a new alternative license. On June 22nd, the first requests to adopt this license were granted to TC39 and applied to the following documents: ECMA-262 (ECMAScript, the official name for JavaScript) and ECMA-402 (the Internationalization API for ECMAScript).

The ECMAScript specification is developed at Ecma International, while other web technologies like HTML and CSS are being developed at W3C. These institutions have different default license agreements, which creates two problems. First, having different licenses increases the overhead of legal review for participants. This can create a speed bump for contributing across different specifications. Second, the default ECMA license contains some restrictions against creating derivative works, in contrast to W3C. These provisions haven’t been a problem in practice, but they nevertheless don’t reflect how we think Open Source should work, especially for something as foundational as JavaScript. Mozilla wants to make it easy for everyone to participate in evolving the Web, so we took the initiative of introducing an alternative license for Ecma International specifications.

**What is the alternative license?**

The full alternative license text may be found on the[ Ecma License FAQ](https://www.ecma-international.org/policies/by-ipr/ecma-text-copyright-policy/). Ecma now provides two licenses, which can be adopted depending on the needs of a given technical committee. The default Ecma International license provides a definitive document and location for work on a given standard, with the intention of preventing forking. The license has provisions that allow inlining a given standard into source text, as well as reproduction in part or full.

The new alternative license seeks to align with the work of the W3C, and the text is largely based on the W3C’s[ Document and Software License](https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document). This license is more permissive regarding derivative works of a standard. This provides a legal framework and an important guarantee that the development of internet infrastructure can continue independent of any organization. By applying the alternative license to a standard as significant as ECMAScript, Ecma International has demonstrated its stewardship of a fundamental building block of the web. In addition, this presents a potential new home for standardization projects with similar licensing requirements.

**Standards and Open Source**

Standardization arises from the need of multiple implementers to align on a common design. Standardization improves collaboration across the industry, and reduces replicated solutions to the same problem. It also provides a way to gather feedback from users or potential users. Both Standards and Open Source produce technical solutions through collaboration. One notable distinction between standardization and an Open Source project is that the latter often focuses on developing solutions within a single implementation.

Open source has led the way with permissive licensing of projects. Over the years, different licenses such as the BSD, Creative Commons, GNU GPL & co, MIT, and MPL have sought to allow open collaboration with different focuses and goals. Standardizing bodies are gradually adopting more of the techniques of Open Source. In 2015,[ W3C adopted its Document and Software License](https://www.w3.org/blog/news/archives/4743), and in doing so moved many of the specifications responsible for the Web such as CSS and HTML. Under this new license, W3C ensured that the ability to build on past work would exist regardless of organizational changes.

**Mozilla’s Role**

As part of our work to ensure a free and open web, we worked together with Ecma International, and many partners to write a License inspired by the W3C Document and Software License. Our goal was that JavaScript’s status would align with other specifications of the Web. In addition, with this new license available to all TCs at Ecma International, this will provide other organizations to approach standardization with the same perspective.

Changes like this come from the work of many different participants and we thank everyone at TC39 who helped with this effort. In addition, I’d like also thank my colleagues at Mozilla for their excellent work: Zibi Braniecki and Peter Saint-Andre, who supported me in writing the document drafts and the Ecma International discussions; Daniel Nazer, Eric Rescorla, Bobby Holley and Tantek Çelik for their advice and guidance of this project.