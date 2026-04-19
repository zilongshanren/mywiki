---
title: Open questions - my two rules
url: https://c0de517e.blogspot.com/2011/10/open-questions-my-two-rules.html
published: '2011-10-28'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

As

[I wrote here](http://c0de517e.blogspot.com/2011/10/open-questions.html), there are some fundamental questions in realtime rendering that I wish I knew more about. I do have though two rules I apply when thinking about rendering techniques- Reduce variance: It's better to be consistent at a lower quality than have glitches/flickering artifacts at a higher quality.
- Postulate: all graphical effects should be reviewed in motion, crossing quality boundaries
- Less is more: It's better to not have a given effect than have it at a too low quality level.

As an example we can analyze shadows. The first rule tells us that it's better to have stable cascades at a lower resolution than having perspective shadowmaps at high resolution.

The second rule tells us that it's better to have lower filtering and cull shadows from some objects or limit the shadowing maximum distance, than having bad shadows everywhere.



Unrelated, I just saw this as a job opening at




Unrelated, I just saw this as a job opening at

[Valve](http://www.valvesoftware.com/jobs/job_postings.html)... Smart guys!Psychologist

We believe that the more we know about human behavior, about how and why people do what they do, the better our products will be. All game designers are, in a sense, experimental psychologists. That’s why we’re looking for a experimental psychologist to apply knowledge and methodologies from psychology to game design and all aspects of Valve’s operations. We want to exploit your experience with experimental design, research methods, statistics, and human behavior to help craft even more compelling gameplay experiences for future Valve titles. We’d also expect you to research and weigh in on any and all topics that are relevant to improving the experiences of our customers, partners, and employees.

Duties:

- Provide relevant insight into human behavior in order to shape gameplay and customer experience.
- Perform statistical analyses on all aspects of Valve’s operations: gameplay, financial, and company data.
- Research compelling new hardware technologies.
- Design experiments to evaluate various gameplay hypotheses and design choices.
- Improve existing playtesting methodologies while incorporating novel techniques to improve best practices.
- Develop innovative ways of acquiring relevant data to answer open questions about all aspects of Valve’s products and business practices.

Requirements:

- Graduate degree in Psychology (or equivalent) field
- Advanced knowledge of statistics
- Familiarity with one or more of the following pieces of data analysis software: SPSS, Systat, Matlab, R, (or equivalent)
- Four years experience with:
- Experimental design/research methods
- Relevant research in cognitive, social, human factors, and related disciplines in psychology


Recommended:

- Proficiency in one or more of the following programming languages: C++, SQL, PHP, (or equivalent)

## 2 comments:

This:




"it's better to have lower filtering and cull shadows from some objects or limit the shadowing maximum distance, than having bad shadows everywhere."

seems to contradict your 1st rule at least and maybe even your 2nd one. Limiting maximum distance (with some proper fading) can work, but certainly only shading some objects will look poor on account of too much variance?

In my very limited experience, it's all about subtlety and art direction. When properly directed a game with mediocre assets & techniques can look much, much better than a game that goes all out on one or two effects.

Not really, my point is that it's harder to spot missing shadows if they are consistent (i.e. fade to no shadow happens at a distance and with a smoothness that makes it not evident) than even having shadows everywhere but with glitchy cascades (i.e. very hard transitions between the first and the second cascade).


I'm really talking about higher quality but with small glitches versus lower quality but consistent here.

Post a Comment