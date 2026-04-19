---
title: Chips and Cheese State of the Union
url: https://chipsandcheese.com/p/chips-and-cheese-state-of-the-union
author: Chips; Cheese
published: '2024-05-09'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Chips and Cheese State of the Union

In December of 2020, a group of friends came together to form Chips & Cheese. It started out as a simple outlet for our in-depth investigations into hardware but quickly turned into a much bigger project altogether.

In 2021, we jokingly said that getting 10,000 visitors and 20,000 views that year would be ambitious. That goal was shattered with a total of 56,649 visitors and 97,084 views. The following year of 2022, we had an optimistic goal of 100,000 visitors and around 250,000 views. Once again those goals were completely and utterly decimated with a total of 242,267 visitors and 430,004 views. In 2023, this trend continued with a grand total of 531,682 visitors and 911,369 views in that year. Well beyond any expectations we could have had. We can’t thank everyone enough for their support.

This growth in the past three and a half years means we have decided to make some changes.

## The Changes

The biggest change that has happened is that Chips and Cheese (Formally Chips and Cheese Technology Publications) is now a 509(a)(2) with 501(c)(3) status. Or in plain English, we are a tax-exempt non-profit charity which means that any donations that you send us are tax deductible.

Forming a nonprofit organization entails a lengthy and tedious process consisting of a lot of paperwork, a lengthy waiting period, and the formation of a Board of Directors to act as a guiding force for the non-profit in order to fulfill its mission statement.

The specific purposes for which this corporation is formed are to educate the public on technical topics, to build and maintain a set of in-house tools to test and evaluate technological products, to release a useful set of these tools as Open-Source Software to inspire curiosity in our audience.

Mission Statement of Chips and Cheese


As for the members of the board:

George J. Cozma: President and Chairman

Dr. Ian Cutress: Vice President

Ryan Mull: Treasurer

Tristiano Agostino: Secretary

Chester Lam: Board Member

Joshua Gregory: Board Member

Zachary Monchamp: Board Member

Felix LeClair: Advisor to the Board

Philipp Munkes: Advisor to the Board

Usman Liaqat: Advisor to the Board


In pursuit of that mission statement, there have been several projects that we have been working on in the background that we would like to bring y’all up to speed on.

### A Call to Action

The first project we have been working on is a new microbenchmark framework. This new framework will hopefully allow for standardization between different tests to keep things as consistent as possible. In the short term, this will also allow folks other than the Chips and Cheese team to add to the Chips and Cheese test suite.

In the long term, we hope that this framework will allow for more tests to be written than the current Chips and Cheese team could ever write on its own, along with diversifying test authors. The vast majority of our current benchmarks were written by Clam and having a single person writing the majority of our tests is not sustainable long term. We hope that this will let Clam to move into sort of an Editor-in-Chief of the Chips and Cheese benchmarks as we grow and expand.

Elaborating further, our goal is to provide more tools for the community, developed by the community. Previously, the tools we provided on our Github were almost entirely code written by Clam. While these tools are not going away, they were written for Clam own direct use, not for the community. To that end, we are aiming for this new suite to be focused on community engagement. We are aiming for a 2 tier model: A framework that will standardize and abstract some of the common elements of the tests being written, as well as a curated set of tests distributed directly by us. Once the framework is released, we encourage the community to design and build their own tests. Additionally, we are actively seeking out contributors to help us build out the [Chips and Cheese Github](https://github.com/ChipsandCheese) with more in-house code.

In a similar vein, Clam is also writing most of the articles on Chips and Cheese and that is also not sustainable long term. We hope that we can get people who are willing to write articles of high quality, if not the same length, as what we currently publish.

To that effect, this State of the Union will also double as a Call to Action. We are looking for new authors, code contributors, and other enthusiast community members to help shoulder the workload that keeps Chips and Cheese running smoothly. Anybody is welcome, so don’t feel discouraged. Our goal is to diversify the contributions going in, so that the community is as involved as they can be. The more of us that help, the stronger Chips and Cheese can become.

### Feedback Needed

We’ve been considering moving over to Substack and want to know how readers feel about this before we make a decision. **We want to be clear that a move to Substack would not involve pay-walling any of our current content output or future articles.** There are upsides and downsides, here’s how it looks from our perspective:

Upsides:

Integrated email newsletter makes it simpler and easier for folks to be notified of and read new articles

Easier linking between our own articles and articles from other Substack outlets (e.g.

[More Than Moore](https://morethanmoore.substack.com)by Dr. Ian Cutress)Better discoverability so that more folks can read our articles and learn from them

Clean, responsive, cross-platform reading experience (a significant improvement over the current layout, but see downsides)

Increased security versus current WordPress setup

Decreased monthly cost compared to the current WordPress + Cloudflare setup

More ways for readers to contribute beyond PayPal and Patreon (which are not available in some countries)


Downsides:

Much less control over site design/layout and platform technical details

Substack operates on a percentage-of-revenue fee model so may work out to be significantly more expensive in the future

No automated external backups of content (an externally-hosted service is required to achieve this)

No support for tables; would have to work around this with image or SVG tables


There are several alternative options that we are also exploring which include a significant redesign of the site to improve the user experience across different devices as well as looking into new solutions for improving our current newsletter service.

### Minecraft Testing Suite

Alongside the new microbenchmark framework we have been working on, we have been also working on a new Minecraft testing suite created by TitanicFreak.

Being our most requested title for us to benchmark while also being very customizable and expandable, Minecraft is the perfect fit for our benchmarking purposes.

We will be targeting the server software side in particular because that’s where most of the heavy lifting in Minecraft is located. Even in single player, you are still playing on an internal server which has to simulate the world 20 times a second.

We do have some overall goals of this benchmark suite, which are:

Create a wide array of tests targeting different parts of the game, two examples are

Time it takes to generate a world from scratch to a 2,500 block radius world

The milliseconds per tick (MSPT) it takes the server to simulate a late game base (any higher than 50 MSPT results in some degree of ‘lag’)


Make all tests scalable to show off architecture and cache differences better

Every test will scale until the server takes 1000 milliseconds per tick (MSPT) to simulate everything or the CPU is completely saturated across all threads. This will show us the capabilities of a particular CPU while also showing how much faster or slower relatively it is with smaller test sizes.


Make the benchmark suite portable across Windows, macOS, and popular Linux distributions.

Bake in expandability from the start so that we cover popular Minecraft modding APIs such as Paper, Fabric, and Forge in the future.

Provide ample documentation to allow for easy setup and configuration

For various important reasons we will not be redistributing the Minecraft server software and any code that isn’t our own. We will have links to acquire all of the software you will need to get setup however. Hence the big focus on documentation.



All of this will take substantial time for us to create. But as we complete individual tests we will have articles discussing it so everyone can follow along the development process to completion.

Since we are Chips and Cheese, we are going include some preliminary data on chunk generation speed comparing the AMD Ryzen 9 7950X and Intel Core i9 14900K. The data was collected with the following configuration:

Stock power limits for both Intel and AMD CPUs

14900K: 253W PL1 / 253W PL2 / 307a Iccmax

7950X: 170W TDP / 230W PPT


The following memory

4x32GB of ECC DDR5 running @ 3600MT/s JEDEC


The following versions

Debian 12.5 (kernel 6.1.0-20)


The following configuration

Seed: 503

Radius: 1000 block radius from coordinates X: 0 Z: 0 with the square shape



Thanks to Paper having a scalable and configurable chunk generation system that far exceeds the capabilities of the vanilla system, we are able to see how the different architectures scale when you give more the server software more cores to work with. In this case it shows that the heterogenous approach of the 14900K’s core configuration has put it at no disadvantage compared to the 7950X. In the end the 14900K is actually faster with a peak generation speed of 509 chunks per second vs 474 chunks per second on the 7950X.

This is just one example of what we are trying to accomplish with our Minecraft Benchmark Suite and we can’t wait to show off more in the future. But it’s time to wrap this up now.

## Conclusion

There have been 1,008,797 visitors and 1,760,828 views as of the time writing this article.

All we can say is wow. When we started this site we could never imagine getting over 25,000 visitors and 50,000 views let alone over a million each. That is all thanks to the help of you, our wonderful readers, and the valuable members of the Chips and Cheese community. Our goal with all of these changes has been to set up Chips and Cheese for a stable, long term future, so that it can continue to enrich the tech community with deep architectural insight, analysis, and data.

Expect the articles to continue uninterrupted, but with new names, faces, and topics as we engage and bring in our community. Thank you for the continued support, and back to our regularly scheduled…Chips and Cheese.