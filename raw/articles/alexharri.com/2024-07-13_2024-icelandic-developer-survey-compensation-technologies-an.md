---
title: '2024 Icelandic Developer Survey: Compensation, Technologies, and more'
url: https://alexharri.com/blog/icelandic-developer-survey-2024
published: '2024-07-13'
source_blog: Personal website | Alex Harri Jónsson
source_site: https://alexharri.com/
category: graphics
fetched: '2026-04-19'
---

# 2024 Icelandic Developer Survey: Compensation, Technologies, and more

A survey for Icelandic developers was conducted earlier this year by [Kolibri](https://www.kolibri.is/en). This survey was comprehensive, gathering data on compensation, programming language use, CI/CD practices, company size, industry, and so on alongside demographic information such as age, experience, and gender.

No large developer survey like this has been conducted in Iceland before—this survey is the first of its kind.

The results from this survey offer us unique insights into the Icelandic software industry. Which technologies are developers using? How are developers compensated? What cloud providers are popular? These are just some of the questions we’ll explore in this post.

There’s loads of data to look at, so let’s get to it!

## Demographics

425 developers responded to the survey. With only a few thousand software developers in Iceland, this constitutes a significant chunk of our developers.

### Age

Most respondents were aged 25 to 54. This chart shows the age distribution of the respondents.

### Gender

Of the respondents who specified their gender (397), 86.1% were men, 13.1% were women, and 0.8% were non-binary.

Despite the seemingly low proportion of women at 13.1% of respondents, this percentage is still significantly higher than in other global developer surveys I’ve looked at. [JetBrains’ 2023 developer ecosystem survey](https://www.jetbrains.com/lp/devecosystem-2023/demographics/#gender) respondents were 5% women, with [State of JS 2023](https://2023.stateofjs.com/en-US/demographics/#gender) at 4%, and [Stack Overflow’s 2022 developer survey](https://survey.stackoverflow.co/2022/#demographics-gender) at ~5%.

### Nationality

Of the 396 respondents who specified their nationality, 384 were Icelandic (96.9%). This low number of non-Iceland respondents is likely due to the survey primarily being circulated through an Icelandic Facebook group for software developers. I would estimate the real proportion of non-Icelandic software developers to be much higher than just 3%.

### Experience

The following chart shows the distribution of the respondents’ years of experience in software development.

This gets more interesting when we group the data on experience by age cohort. The below chart shows years of experience, grouped by age.

PS: Try hitting the ‘Normalize’ toggle on the top right. It allows you to switch from viewing the absolute counts to viewing percentages within each group. Every chart that groups data has this button.

Most developers aged 45 or above have over 20 years of experience, indicating that most older developers started their careers in their 20s. Looking at the younger age cohorts we can see that most of them started their career in their 20s as well, with a smaller percentage starting in their 30s or 40s.

### Developer types

Respondents were asked which type of developer they consider themselves to be. This was a multi-choice question, so they could pick more than one type.

Perhaps the most immediately obvious fact that jumps out is how many developers classify themselves as full-stack developers. Definitely more than I would have expected! I made one notable change to the data which contributed to that:

- If a developer classified themselves as both a front-end and back-end developer, I classified them as a full-stack developer (in case they had not done so themselves).
- After that, if a developer is classified as a full-stack developer, they are
*not*classified as a front-end or back-end developer.

This change means that front-end, back-end, and full-stack are *mutually exclusive* developer types. I feel that this gives a better sense of the real numbers of front-end vs back-end vs full-stack developers.

## Back-end programming languages

The survey asked which back-end programming languages respondents had used within the last year. Only respondents who classified themselves as back-end or full-stack developers were asked this question.

Note: The languages colored blue were provided as default options in the survey, while the languages colored green were typed in the “Other” field. Languages used by fewer than 3 respondents are not included.

The top back-end programming language in Iceland is C#, with 46.1% of Icelandic developers using it. After C#, we get TypeScript (40.4%), Python (38.6%), and JavaScript (32.6%). The next two languages, Go and Java, come in at 17.9% and 15.4% respectively.

Some observations:

- SQL at 1.3% usage is
*obviously*not accurate. I would expect most back-end and full-stack developers to have reported using it had it been provided as a default option. - C++ at 3.4% is far too low as well. I would guesstimate that C++ would be in the 8-15% range had it been included in the default options.

Aside from those obvious anomalies, the data seems accurate to me. C# is heavily used in Icelandic companies, with it being the go-to back-end development language for most Icelandic companies.

TypeScript, as the data shows, has been widely adopted in Iceland. In my experience, TypeScript is generally strongly preferred over plain JavaScript, though not universally. In this survey, 74% of those who use JavaScript also reported using TypeScript, while 60% of those using TypeScript reported also using JavaScript.

Python being heavily used is no surprise to me, and the usage of Rust is in line with what I would have expected. Go is used more than I would have thought.

### Comparison to Stack Overflow’s survey

Let’s compare this to the results of [Stack Overflow’s 2023 Developer Survey](https://survey.stackoverflow.co/2023/#most-popular-technologies-language-prof):

One obvious issue with this comparison is that the State of Iceland survey specifically asked about *back-end* languages, while Stack Overflow’s survey did not make that distinction. This may be part of the wide gap in usage between JavaScript in Iceland vs globally, and also why the percentages are generally higher in Stack Overflow’s survey

Still, a few key things stand out to me:

- C# is super popular in Iceland. Perhaps as a direct consequence, Java is much less used in Iceland than globally.
- TypeScript is more popular than JavaScript in Iceland, which is not the case globally.
- PHP is much less used in Iceland than globally.

### Programming languages used by years of experience

I was curious whether there would be a significant difference between the languages that experienced developers are using compared to less experienced ones, but that does not seem to be the case. The following chart shows language use by years of experience.

We can glean *some* patterns from this data, such as Java being used more by experienced developers. Still, I don’t see any dramatic differences that couldn’t be explained away by the small sample size.

## Salary

Icelandic developers are compensated well. Respondents were asked about their monthly salary in Icelandic króna (ISK), with the possible answers being one of six salary brackets:

| ISK | EUR | USD |
|---|---|---|
| 0 - 800,000 | 0 - 5,360 | 0 - 5,760 |
| 800,000 - 1,000,000 | 5,360 - 6,700 | 5,760 - 7,200 |
| 1,000,000 - 1,200,000 | 6,700 - 8,040 | 7,200 - 8,640 |
| 1,200,000 - 1,400,000 | 8,040 - 9,380 | 8,640 - 10,080 |
| 1,400,000 - 1,600,000 | 9,380 - 10,720 | 10,080 - 11,520 |
| Over 1,600,000 | Over 10,720 | Over 11,520 |

Note: The EUR and USD figures are using an exchange rate of ISK 1 = EUR 0.0067 and ISK 1 = USD 0.0072, measured on the 2nd of July 2024.

In Iceland, we generally discuss monthly salaries instead of yearly. But in the US, and other countries, yearly salary figures are more common. Here is the same table with yearly salary figures.

| ISK | EUR | USD |
|---|---|---|
| 0 - 9,600,000 | 0 - 64,320 | 0 - 69,120 |
| 9,600,000 - 12,000,000 | 64,320 - 80,400 | 69,120 - 86,400 |
| 12,000,000 - 14,400,000 | 80,400 - 96,480 | 86,400 - 103,680 |
| 14,400,000 - 16,800,000 | 96,480 - 112,560 | 103,680 - 120,960 |
| 16,800,000 - 19,200,000 | 112,560 - 128,640 | 120,960 - 138,240 |
| Over 19,200,000 | Over 128,640 | Over 138,240 |

The below chart shows monthly salaries for developers in Iceland, split by age bracket.

As a freshly minted developer, you can expect to earn under or around ISK 800K. Even though the first salary bracket goes to zero, I wouldn’t expect many developers to be earning less than 650K unless they’re entering the field without a degree.

With a few years of experience, most developers move from the <800K to the 800K-1.0M bracket. At 6 or more years of experience, a lot of developers move into the >1.0M brackets.

Summarizing this:

- Developers starting their careers can expect to earn under or around ISK 800K monthly (USD 70K yearly).
- Developers with 3-10 of experience generally earn ISK 800K to 1.2M monthly (USD 70K to 100K yearly).
- Developers with over 10 of experience generally earn ISK 1.0M to 1.4M monthly (USD 85K to 120K yearly).
- A significant number of highly experienced developers (10 to 20+ years of experience) earn 1.4M to >1.6M monthly (USD 120K to >140K yearly).

TL;DR: the typical developer in Iceland earns around USD 85K to 120K yearly.

Here is a different view of the same compensation data, which I feel shows the story of how developers move into the higher salary brackets as they gain more experience.

### Salary by programming language

The following chart shows monthly salary grouped by language:

There is not a great deal of difference across languages, though salaries for developers using PHP and JavaScript developers seem to skew lower. The handful of Scala developers are raking in cash.

### Salary by developer type

As mentioned earlier, developers were asked to select their developer type, such as whether they’re a front-end or a back-end developer. The following chart shows monthly salary, grouped by developer type.

### Gender differences in pay

I was curious as to whether there would be visible disparities in salaries across genders, but I can’t see any notable difference from the survey data. Still, here is the salary chart from earlier split by gender as well as years of experience so that you can see for yourself.

Note: For information on the gender pay gap in Iceland, see [“Unadjusted gender pay gap 9.1% in 2022”](https://www.statice.is/publications/news-archive/wages-and-income/unadjusted-gender-pay-gap-2022/) from Statistics Iceland

## Putting context to the salary numbers

Salary numbers are interesting, but there are other important factors that cannot be captured in raw salary numbers. The following chapters will discuss taxes, employer-provided benefits, and work-life balance in Iceland.

### Taxes

We’ve been looking at gross salaries so far. In figuring out net salaries we need to look at Icelandic taxes. In 2024, Iceland had three tax brackets:

| Income, per month | Tax rate |
|---|---|
| ISK 0 - 446,136 | 31.48% |
| ISK 446,137 - 1,252,501 | 37.98% |
| Over ISK 1,252,501 | 46.28% |

Source: [https://www.skatturinn.is/english/individuals/tax-liability/](https://www.skatturinn.is/english/individuals/tax-liability/)

There is a personal tax credit of ISK 64,926 per month, which lowers the effective tax rate. There are also other factors, such as the mandatory pension fund, union membership fees, and voluntary pension insurance premiums.

To take a rough example, a developer earning a monthly gross salary of ISK 1.2M (~104K USD, yearly) is likely to have a net salary of around 780K-800K ISK (~USD 67K-70K, yearly). Don’t take this number too seriously, it depends on a lot of factors.

### Employer-provided benefits

Developers in Iceland often receive employer-provided benefits. Common ones include:

- Subsidies for physical and/or mental wellness (e.g. gym membership or counseling)
- Home internet and phone plans
- Lunch and snacks
- Transportation subsidies (e.g. bus pass)
- Mobile phones
- Conferences (e.g. pick one yearly)

This of course varies by company, but most companies provide at least some of these. Every company I’ve worked for in Iceland has provided me with the first three benefits listed.

### Work-life balance and parental leave

With the obvious caveat of work-life balance varying by company, work-life balance for developers in Iceland is generally very good.

A notable factor is Iceland’s generous paid parental leave, which is 6 months for each parent with 2 of those months transferrable to the other parent. This corresponds to about 26 weeks of parental leave for each parent.

Payments during parental leave are 80% of the person’s salary, capped at ISK 700K. This means that payments during parental leave max out when earning ISK 875K or more, which applies to most developers in Iceland.

Note: For more information on paternal leave in Iceland, see [https://island.is/en/life-events/having-a-baby](https://island.is/en/life-events/having-a-baby)

### Salaries in Iceland

Icelandic developer salaries fall on the higher end of the salary spectrum. The following chart shows the distribution of total compensation in Iceland using data from Statistics Iceland:

Source: [https://statice.is/statistics/society/wages-and-income/wages/](https://statice.is/statistics/society/wages-and-income/wages/)

Converting this from monthly compensation in ISK to yearly compensation in USD, we get a chart that’s more easily understood by a global audience:

## Industries

The survey asked developers which industry they worked in. Here are the results.

### Salaries by industry

Here is the monthly salary data split by industry:

We can see that salaries in the public sector skew lower and salaries in banking and finance skew higher. Not terribly surprising.

### Programming language usage by industry

Respondents could pick multiple languages, but they could only pick a single industry. The following chart shows, for each language, which industry the respondent using the language works in.

We can see some patterns emerge:

- Developers working in banking, finance, and the public sector mostly use C#.
- Rust, TypeScript, Python, and Go are popular in startups.

### Startups

15.9% of developers—including myself—reported working in startups. Quite a high percentage!

Much of that can be attributed to Iceland’s strong support system for startups. [Klak](https://klak.is/en/) runs multiple startup accelerators like [Gulleggið](https://gulleggid.is/) and [Startup SuperNova](https://www.nova.is/hradleid/startupsupernova). There are many notable venture capital funds like [Brunnur](https://www.brunnurventures.com/), [Frumtak](https://frumtak.is/), and [Crowberry Capital](https://www.crowberrycapital.com/), in addition to the [Technology Development Fund](https://en.rannis.is/funding/research/technology-development-fund/) which provides free capital for early-stage startups.

In addition to that, companies may receive up to a 20% tax deduction for expenses related to research and innovation for expenses up to ISK 1,100M each year, or around USD 7.9M.

### Company size

With a population of around 380,000 people, Icelandic companies are generally small to medium-sized. Very few Icelandic companies, outside of municipalities and healthcare, reach over 1,000 employees.

The following chart shows the distribution of company sizes at which the respondents work.

A lot of Icelandic developers working at companies with more than 300 people! Here we can see the same data on company sizes, grouped by industry:

As one might expect, developers working in the public sector or banking/finance work at larger companies, while developers in startups tend to work at smaller companies.

## Technology stacks

We’ll now take a look at the technologies that Icelandic developers are using. We’ll cover front-end libraries, cloud providers, CI/CD, and developers’ OS of choice.

### Front-end libraries

The following chart shows the front-end libraries which respondents used in the last year.

Note: Like before, front-end libraries colored blue were provided as a default option in the survey, while the front-end libraries colored green were typed in the “Other” field.

React dominates the front-end scene in Iceland, with Vue and Angular in a distant second and third place. In my experience, this data is representative—React is incredibly popular here.

Some other observations:

- Next.js is very popular in Iceland. Had it been included as a default option it would likely have been
*much*higher. I would personally estimate that over 50% of developers in Iceland using React also use Next.js. - The survey only included JavaScript libraries as default options. With C# being as popular as it is in Iceland, a fair number of respondents mentioned C# front-end solutions in the “Other” field, of which Blazor seems to be most popular. Perhaps more people would have selected C#-related technologies had C# libraries been included as default options.

### Cloud providers

Note: Default survey options are colored blue, while options typed in the “Other” field are colored green. Origo, Advania, and 1984.is are local Icelandic cloud providers.

AWS at 52.5% is the most popular cloud provider in Iceland, with Azure in second place at 36.5%. Vercel and Cloudflare are also used by a significant number of developers, coming in at 22.6% and 17.6% respectively. Google Cloud is relatively far behind AWS and Azure with 16.2% of Icelandic developers using GCP.

Digital Ocean is the most notable cloud provider not included as a default option. Perhaps it would have ranked higher had it been one of the default options.

#### Programming language usage by cloud provider

The following chart shows the usage of programming languages by cloud providers. In other words: for developers using a given cloud provider, how many of them are using a given programming language?

Developers using Azure, Origo, and Advania are *much* more likely to use C# than developers using other cloud providers. Developers using Azure are around 2.5 times more likely to use C# compared to developers using AWS.

Usage of TypeScript and Python seems inversely correlated to the usage of C#.

### Continuous integration and continuous delivery (CI/CD)

The chart below shows which CI/CD providers developers reported using.

Note: Default survey options are colored blue, while options typed in the “Other” field are colored green.

Most respondents use GitHub actions for CI/CD (52.5%). GitLab and Azure are also fairly popular with 19.1% and 17.4% respectively.

### Code editors

A whopping 75.6% of Icelandic developers use Visual Studio Code for editing code.

Visual Studio (26.8%), Vim (22.7%) and IntelliJ (17.2%) see respectable usage. All other code editors are used by less than 10% of Icelandic developers.

### Operating system

Which operating systems are Icelandic developers using?

macOS, apparently! A lot are using Linux as well. I would have expected Windows to take the top spot.

#### Operating system by industry

Grouping the use of operating systems by industry, we see that Windows is most used within the public sector and finance/banking, while macOS is more popular in startups, the private sector, and with contractors.

## Final words

I want to thank [Telma Guðbjörg Eyþórsdóttir](https://www.linkedin.com/in/telmag92/) and [Jóhann Guðmundsson](https://www.linkedin.com/in/j%C3%B3hann-gu%C3%B0mundsson-935457b7/) (both software developers at Kolibri) for kickstarting and driving this survey! Additional thanks go to [Anna Signý Guðbjörnsdóttir](https://www.linkedin.com/in/annasigny/) (CEO at Kolibri) and the other people at [Kolibri](https://www.kolibri.is/en) that helped make this happen.

Kolibri is one of Iceland’s foremost digital agencies, providing services related to creating digital experiences, such as product and software development and design. I’m not formally affiliated with them in any way, but I have friends there.

![](../../assets/9ad15b2bd3343a4f.jpg)

Kolibri held an event where they presented the results of the study, which sparked lively discussions. The house was packed and it was a blast!

Getting to write up the results of the survey has been awesome! I hope I have the opportunity to do so again in the future.

Thanks for reading! I hope this was interesting.

— Alex Harri

To be notified of new posts, subscribe to my mailing list.