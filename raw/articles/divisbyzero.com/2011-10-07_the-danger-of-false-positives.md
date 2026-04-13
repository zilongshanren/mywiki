---
title: The danger of false positives
url: https://divisbyzero.com/2011/10/07/the-danger-of-false-positives/
author: Dave Richeson
published: '2011-10-07'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

As I [mentioned earlier](https://divisbyzero.com/2011/08/30/advice-for-new-college-students/), I’m teaching a first-year seminar this semester called “Science or Nonsense?” On Monday and Wednesday this week we discussed some math/stats/numeracy topics. We talked about the [Sally Clark murder trial](http://en.wikipedia.org/wiki/Sally_Clark), the [prosecutor’s fallacy](http://en.wikipedia.org/wiki/Prosecutor%27s_fallacy), the use of DNA testing in law enforcement, [Simpson’s paradox](http://en.wikipedia.org/wiki/Simpson%27s_paradox), the danger of false positives, and the [2009 mammogram screening recommendations](http://www.uspreventiveservicestaskforce.org/uspstf/uspsbrca.htm).

I made a [GeoGebra applet](https://www.geogebra.org/m/bp4eqekh) to illustrate the dangers of false positives. So I thought I’d share that here. Here’s the statement of the problem.

Suppose Lenny Oiler visits his doctor for a routine checkup. The doctor says that he must test all patients (regardless of whether they have symptoms) for rare disease called *analysisitis.* (This horrible illness can lead to severe pain in a patient’s epsylawns and del-tahs. It should not to be confused with * analysis situs*.) The doctor says that the test is 99% effective when given to people who are ill (the probability the test will come back positive) and it is 95% effective when given to people who are healthy (it will come back negative).

Two days later the doctor informs Lenny that the test came back positive.

**Should Lenny be worried?**

Surprisingly, we do not have enough information to answer the question, and Lenny (being pretty good at math) realizes this. After a little investigating he finds out that approximately 1 in every 2000 people have analysisitis (about 0.05% of the population).

**Now should Lenny be worried?**

Obviously he should take notice because he tested positive. But he should not be too worried. It turns out that there is less than a 1% chance that he has analysisitis.

Notice that there are four possible outcomes for a person in Lenny’s position. A person is either ill or healthy and the test may come back positive or negative. The four outcomes are shown in the chart below.

| Test result | Ill | Healthy |
| Positive | true positive | false positive |
| Negative | false negative | true negative |

Obviously, the two red boxes are the ones to worry about because the test is giving the incorrect result. But in this case, because the test came back positive, we’re interested in the top row.

For simplicity, suppose the city that is being screened has a population of 1 million. Then approximately (1000000)(0.0005)=500 people have the illness. Of these (500)(.99)=495 will test positive and (500)(0.01)=5 will test negative. Of the 999,500 healthy people (999500)(.05)=49975 will test positive and (999500)(.95)=949525 will test negative. This is summarized in the following chart.

| Test result | Ill | Healthy |
| Positive | 495 | 49975 |
| Negative | 5 | 949525 |

Thus, 495+49975=50470 people test positive, and of these only 495 are ill. So the chance that a recipient of positive test result is sick is 495/50470=0.0098=0.98%. That should seem shockingly low! I wonder how many physicians are aware of this phenomenon.

You can try out this or other examples using [this GeoGebra applet](https://www.geogebra.org/m/bp4eqekh) that I made.

I really like the use of geogebra to illustrate this.

This is one of those questions (not uncommon in probability) where you are fighting against “common sense” (which sometimes turns out to be nonsense:).

I modeled a similar problem in Fathom for use with a senior high school class a few years back & describe it here: http://www.mathrecreation.com/2009/03/false-positives.html

Hi,

Your analysis reminds me of Bayes’ theory, does it not? But I really like your game-like table approach of explaining the problem. I have never thought of this.

I show this in my class as an application of Bayes’ rule – although now I am wondering if the formal algebraic manipulations actually do more to obscure rather than illuminate the intuitive reasons for this phenomena.

Leonard Mlodinow discusses the same thing in “The Drunkard’s Walk”, but this line of argument is a revelation of the ideas behind Baye’s Theorem. Finally, GeoGebra applet is a great idea.

can you please put download link for the geogebra worksheet as some of us do not have working Java.

Your analysis reminds me of Bayes’ theory, does it not?When I’ve written about this phenomenon, I’ve called the disease “Bayesianitis” !

Hi, I don’t understand why, in your conclusions, when you count people who test positive, you consider 500 + 49975 instead of 495 + 49975. Obviously the percentage concerning “the chance that a recipient of positive test result is sick” rises a little, but I would know if I was wrong!

Thank u, your posts are always a shaking reading.

Thanks for catching that. It is fixed now.