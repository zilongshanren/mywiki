---
title: Stack Overflow Dashboard – check engagement, metrics and more – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2014/06/stack-overflow-dashboard-check-engagement-metrics-and-more/
author: Robert Nyman
published: '2014-06-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Recently I put together a little [Mozilla tags on Stack Overflow dashboard](http://robnyman.github.io/mozilla-stackoverflow/) to check the engagement and numbers for [the tags we sponsor](http://stackoverflow.com/r/mozilla). I liked the idea and wanted to create a general purpose [dashboard for Stack Overflow](http://robnyman.github.io/stackoverflow-dashboard/), and share the feature, code and thinking with you.

## Features

Numbers and developer behavior are always interesting areas, especially to spot trends, common questions, related areas and more. As Stack Overflow is one of the de facto channels where developers ask questions to solve problems I find it very interesting to look at those numbers and see possible correlations.

You can filter the data based on dates and time periods (different data is available through one or the other option), and the areas the dashboard offers information for are:

- Questions:
- # with activity
- # of unanswered
- Percentage of unanswered questions (
*Note that a question must have at least one upvoted answer to be considered answered*) - List of unanswered questions
- Frequently asked questions

- Top answerers
- Top askers
- Related tags

## The approach

My thinking was to use the [Stack Exchange API](http://api.stackexchange.com/docs/) and do simple requests for various tags end the engagement around them. I also wanted to make it easy for the user and autocomplete values for the tag criteria field. Given how many tags there are on Stack Overflow, though, to avoid massive overload I only get the 100 most popular tags and put them in a `<datalist>`

element, connected to the `<input>`

element where the user enters the tag to look for data for. This is being done directly on page load.

### General mindset

The general mindset when building up the dashboard:

- Create a simple HTML form with tag, date period input
- Use a simple XMLHttpRequest to get the most popular tags for the
`<datalist>`

element - For any request, use the basic XHR to get the data directly in JSON
- Depending on the requested data – multiple requests are needed to fill the dashboard – parse the returned JSON and present the results

### API methods being used

The other API methods that are being called are:

[http://api.stackexchange.com/docs/tags](http://api.stackexchange.com/docs/tags)[http://api.stackexchange.com/docs/search](http://api.stackexchange.com/docs/search)[http://api.stackexchange.com/docs/unanswered-questions](http://api.stackexchange.com/docs/unanswered-questions)[http://api.stackexchange.com/docs/top-answerers-on-tags](http://api.stackexchange.com/docs/top-answerers-on-tags)[http://api.stackexchange.com/docs/top-askers-on-tags](http://api.stackexchange.com/docs/top-askers-on-tags)[http://api.stackexchange.com/docs/faqs-by-tags](http://api.stackexchange.com/docs/faqs-by-tags)[http://api.stackexchange.com/docs/related-tags](http://api.stackexchange.com/docs/related-tags)

### Request throttling

Note that the [limit for each IP number is 300 requests](http://api.stackexchange.com/docs/throttle) per 24 hours (unless you have an access_token, then the limit is 10,000).

## Code

The [code is available on GitHub](https://github.com/robnyman/stackoverflow-dashboard) and the idea has been to keep it as simple and free of dependencies as possible. It doesn’t use any JavaScript libraries as I see the use cases here, and where we are right now with HTML5, competent enough not to need that.

### Pre-populating the <datalist> element

As an example, this is (trimmed-down) version of the code to get the most popular tags as JSON through the Stack Exchange API and polulate the `<datalist>`

:

```
function getPopularTags () {
getItems("popularTags", "http://api.stackexchange.com/2.2/tags?pagesize=100&order=desc&sort=popular&site=stackoverflow");
}
// Run automatically at page load to pre-populate the <datalist> element
getPopularTags();
function getItems(type, url) {
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function () {
if (xhr.readyState === 4) {
var response = xhr.response;
if (response.error_message) {
// Show errors
}
else {
addResults(type);
}
}
};
xhr.open("GET", url, true);
xhr.responseType = "json";
xhr.send(null);
};
function addResults (type) {
// Popular tags, for filling the <datalist> element
if (type === "popularTags") {
var popularTagsList = document.querySelector("#popular-tags"),
popularTags = questions.popularTags.items,
popularTagsResults = "";
for (var i=0,l=popularTags.length, tag; i<l; i++) {
tag = popularTags[i];
popularTagsResults += '<option value="' + tag["name"] + '">';
}
popularTagsList.innerHTML = popularTagsResults;
}
}
```

## Give feedback & hack it

I hope you find this interesting, and a good point to evaluate which areas to focus on and learn more! Also feel more than welcome to [use the dashboard](http://robnyman.github.io/stackoverflow-dashboard/), check out [the code](https://github.com/robnyman/stackoverflow-dashboard) and issue pull requests, suggest features and more!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.