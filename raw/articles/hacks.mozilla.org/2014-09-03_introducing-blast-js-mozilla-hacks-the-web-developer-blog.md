---
title: Introducing Blast.js – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/09/introducing-blast-js/
author: Julian Shapiro
published: '2014-09-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

After releasing [Velocity.js](http://velocityjs.org), a highly performant web animation engine, I wanted to leverage that power for typographic manipulation. The question soon arose, How could I animate one letter, one word, or one sentence at a time without bloating my HTML with wrapper elements?

If I could figure this out, I could create beautiful typographic animation sequences (the kind you see in movie titles), and perform real-time textual analysis.

After researching lower-level DOM methods and polishing my RegEx skills, I built [Blast.js](http://julian.com/research/blast/): a jQuery/Zepto plugin that breaks apart text to enable hassle-free text manipulation. Follow that link to see a few demos.

Let’s jump right into a code example. If we were to Blast an element using the following syntax…

```
$("div").blast({ delimiter: "word" });
```

…and if our element initially looked like this…

```
Hello World
```

…our element would now look like this:

```
Hello
World
```

The div’s text was broken into individual span elements using the specified *word* delimiter. We could have used the *character*, *sentence*, or *element* delimiters instead.

For a breakdown of Blast’s API, refer to [its documentation](http://julian.com/research/blast/).

This article serves to explore the technical aspects that went into making Blast versatile and accurate: We’ll learn about very powerful, yet little-known, DOM traversal techniques plus how to maximally leverage RegEx for linguistic accuracy.

If you’re interested in the technical aspects of how rich motion design works or how to manipulate text, this article is for you.

## Versatility

Most DOM elements are composed of descendant text nodes. Blast traverses the entirety of the HTML element that it is targeted on, descending recursively until it’s found every descendant text node.

For example, if you Blast the following HTML:

`Hello World`

The containing **div** is an *element node*. This element node is composed of two children: 1) a text node (“Hello “) and 2) a **span** element node. The **span** element node contains one child: a text node of its own (“World”).

With each text node Blast finds, it executes the RegEx query associated with the chosen delimiter type (e.g. *character*, *word*, or *sentence*) in order to find submatches. For example, a text node of “World” blasted with the *character* delimiter will produce five submatches: “w”, “o”, “r”, “l”, and “d”. Blast wraps a new element node of a user-defined type (span is the default) around each of these submatches.

By traversing the DOM in this way, Blast can be applied safely to the entirety of an element without concern for breaking any of its descendant HTML or its associated event handlers. (Event handlers are never bound to text nodes, but rather to containing element nodes.)

In fact, let’s try just that — in real-time! [Click here](http://codepen.io/julianshapiro/pen/cqEtz/) to see Blast used on a CodePen page with the *word* delimiter. Notice how the generated wrapper elements are filtered with alternating colors. Next, click around. You’ll see that the page continues to work perfectly; all buttons, event handlers, and interactions remain fully intact. Nothing has been compromised.

This versatility is crucial when blasting user-generated content, which, by its nature, is not necessarily predictably structured. It can be dirtied with HTML.

## Reversal

When Blast generates wrappers around each of text node’s submatches, it assigns each wrapper a “blast” class. This class is later referenced when Blast is reversed.

Blast reversal is triggered by passing in *false* as Blast’s sole parameter. The reversal process works as follows: The DOM is traversed, but the elements it’s looking for are element nodes (not text nodes) that have been assigned the “blast” class. Each matched element node is then replaced with its inner HTML.

For example, reversing Blast on the following HTML…

```
Hello
World
```

… using the following syntax…

```
$("#helloWorld").blast(false);
```

…will result in Blast descending into #helloWorld, matching each element node individually, then substituting these element nodes with the text nodes that they contain — “Hello” and “World”, respectively.

After this process, our DOM is back to exactly where it was before we Blasted it. This ability to cleanly reverse allows us to jump into arbitrarily structured HTML, Blast it apart, run a series of typographic animations, then reverse Blast upon completion so that our markup remains clean and structured as originally intended.

Let’s do just that:

See the Pen [Blast.js – Command: Reverse](http://codepen.io/julianshapiro/pen/tDIlk/) by Julian Shapiro ([@julianshapiro](http://codepen.io/julianshapiro)) on [CodePen](http://codepen.io).

## Accuracy

We’ve established that Blast preserves HTML by touching only the relevant nodes (text nodes). Now let’s explore how Blast is able to pull off this next trick:

See the Pen [Blast.js TypeKit Article – Accuracy](http://codepen.io/julianshapiro/pen/kdEqb/) by Julian Shapiro ([@julianshapiro](http://codepen.io/julianshapiro)) on [CodePen](http://codepen.io).

Remember, when a descendant text node is found in an element node targeted by Blast, the chosen delimiter’s RegEx is executed against it. Let’s examine each delimiter, starting with the simplest: *character*.

(Note that you can follow along with these examples by clicking the demo buttons under the **Robustness Gallery** section of Blast’s [documentation](http://julian.com/research/blast/). You can also visit [RegEx101.com](http://regex101.com) to test the following RegEx queries against your own bodies of text.)

The RegEx for the character delimiter is simply `/(S)/`

, which treats every non-space character as a submatch (a submatch is the part of the text node that gets wrapped by a newly-generated element). Simple enough.

Next, the word delimiter uses this RegEx: `/s*(S+)s*/`

. This matches any non-space character surrounded by either a space or nothing (nothing is the edge case where a word appears at the beginning or ending of a text node). Specifically, **s*** means “optionally match a space character”, and the **S+** in the middle means “match as many non-space characters as possible.” Note that the word delimiter matches will include any punctuation that’s adjoined to the word, e.g. “Hey!” will be a full match. For the vast majority of use cases, this is more desirable than treating every adjoined punctuation as its own word.

Now things start to get more complex. It’s trivial to match characters and space-delimited words, but it’s tricky to robustly match *sentences* — especially in a multilingual manner. Blast’s sentence delimiter delimits phrases either 1) ending in Latin alphabet punctuation (linebreaks are not considered punctuation) or 2) located at the end of a body of text. The sentence delimiter’s RegEx looks like this:

```
(?=S)(([.]{2,})?[^!?]+?([.…!?]+|(?=s+$)|$)(s*[′’'”″“")»]+)*)
```

Below is an expanded view (with spacing) for better legibility:

```
(?=S) ( ([.]{2,})? [^!?]+? ([.…!?]+|(?=s+$)|$) (s*[′’'”″“")»]+)* )
```

Let’s break that down into its components:

`(?=S)`

The sentence must contain a non-space character.`([.]{2,})?`

The sentence may begin with a group of periods, e.g. “… that was a bad idea, Tom!”`[^!?]+?`

Grab everything that isn’t an unequivocally-terminating punctuation character, but stop when the following condition is reached…`([.…!?]+|(?=s+$)|$)`

…match the last occurrence of sentence-final punctuation or the end of the text (optionally with trailing spaces).`(s*[′’'”″“")»]+)*`

After the final punctuation is matched, also include any and all pairs of (optionally space-delimited) quotes and parentheses.

That’s quite a bit to to digest, but if you refer to those RegEx components while revisiting the sentence matching behavior from the top of this section (re-embedded below for convenience), you’ll start to see how the larger pieces come together.

See the Pen [Blast.js TypeKit Article – Accuracy](http://codepen.io/julianshapiro/pen/kdEqb/) by Julian Shapiro ([@julianshapiro](http://codepen.io/julianshapiro)) on [CodePen](http://codepen.io).

(Click on the HTML tab to modify the HTML and see how Blast behaves on different bodies of text.)

We still haven’t explained why that embedded demo’s errant periods aren’t falsely triggering the end of a sentence match: The trick is to perform a pre-pass on each text node — *prior* to the primary RegEx execution — in which likely false positives are rendered inert by temporary encoding them into non-matching strings. Then, after the sentence RegEx is executed, the likely false positives are decoded back to their original characters.

The false positive encoding process consists of replacing a punctuation character with its ASCII equivalent inside double curly brackets. For example, a likely false positive period (e.g. one found in the title “Mr. Johnson”) will be turned into “Mr{{46}} Johnson”. Then, when the sentence delimiter’s RegEx is executed, it skips over the {{46}} block since curly braces aren’t considered Latin alphabet punctuation.

Here’s the logic behind this process:

```
text
/* Escape the following Latin abbreviations and English
titles: e.g., i.e., Mr., Mrs., Ms., Dr., Sr., and Jr. */
.replace(RegEx.abbreviations, function(match) {
return match.replace(/./g, "{{46}}");
})
/* Escape inner-word (non-space-delimited) periods.
For example, the period inside "Blast.js". */
.replace(RegEx.innerWordPeriod, function(match) {
return match.replace(/./g, "{{46}}");
});
```

So now you have an overview of Blast’s behavior, but you haven’t learned that much. Not to worry, the next two sections get super technical.

## Deep dive: Regex

This section is optional. This is a technical deep dive into how Blast’s RegEx queries are designed.

This is the RegEx code block that you can find at the top of [Blast’s source code](https://github.com/julianshapiro/blast/blob/master/jquery.blast.js):

```
var characterRanges = {
latinLetters: "\u0041-\u005A\u0061-\u007A\u00C0-\u017F\u0100-\u01FF\u0180-\u027F",
},
Reg = {
abbreviations: new RegExp("[^" + characterRanges.latinLetters + "](e\.g\.)|(i\.e\.)|(mr\.)|(mrs\.)|(ms\.)|(dr\.)|(prof\.)|(esq\.)|(sr\.)|(jr\.)[^" + characterRanges.latinLetters + "]", "ig"),
innerWordPeriod: new RegExp("[" + characterRanges.latinLetters + "].[" + characterRanges.latinLetters + "]", "ig"),
};
```

The first step is to define the UTF8 character ranges within which the letters used by all the Latin alphabet languages are contained. If that string looks like total gibberish to you, fear not: Character representation systems associate an ID with each of their displayable characters. RegEx simply allows us to define a range of ID’s (place a “-” between your first character’s ID and the last character’s ID). We take advantange of this by collating a bunch of ID ranges together in order to skip past ranges that contain characters that aren’t used in everyday language (e.g. emoticons, arrow symbols, etc.).

Once we know what all the acceptable characters are, we can use them to create RegEx queries:

**The abbreviations RegEx** looks for case-insensitive whitelisted abbreviations (e.g. Mr., Dr. Jr.) that are not immediately preceded by one of the accepted characters. In other words, it wants to find where these abbreviations are preceded by either nothing, a space, or a non-letter character. For example, we don’t want to match “ms.” in “grams.”, but we want to match “ms.” in “→Ms. Piggy”. Likewise, the RegEx query ensures that the abbreviation is also not immediately *followed* by a letter. For example, we don’t want to match “e.g.” in a corporation’s name abbreviation such as “E.G.G.S.”. But, we do want to match “e.g.” in “… farm animals, e.g. cows, bigs, etc.”

**The inner-word period RegEx** looks for any period that’s sandwiched immediately between a whitelisted Latin alphabet letters on either side. So, the period inside “Blast.js” successfully matches, but the period at the end of “This is is a short sentence.” successfully does not.

## Deep dive: DOM traversal

This section is optional. This is a deep dive into how text node traversal works.

Let’s take a look at the recursive DOM traversal code:

```
if (node.nodeType === 1 && node.hasChildNodes()
&& !Reg.skippedElements.test(node.tagName)
&& !Reg.hasPluginClass.test(node.className)) {
/* Note: We don't cache childNodes' length since it's a live nodeList (which changes dynamically with the use of splitText() above). */
for (var i = 0; i < node.childNodes.length; i++) {
Element.nodeBeginning = true;
i += traverseDOM(node.childNodes[i], opts);
}
}
```

Above, we check that the node...

- Has a nodeType of 1 (which is the ID associated with an element node).
- Has child nodes for us to crawl.
- Is not one of the blacklisted element node tags (script, textarea, and select), which contain text nodes, but not that typical kind that users likely want to be blasted.
- Isn't already assigned the "blast" class, which Blast uses to keep track of which elements it's currently being used on.

If the above conditions aren't true and if the nodeType is instead returning a value of 3, then we know we've hit an actual text node. In this case, we proceed with submatch and element wrapping logic. Refer to the inlined comments for a thorough walkthrough:

```
/* Find what position in the text node that our
delimiter's RegEx returns a match. */
matchPosition = textNode.data.search(delimiterRegex);
/* If there's a RegEx match in this text node, proceed
with element wrapping. */
if (matchPosition !== -1) {
/* Return the match. */
var match = node.data.match(delimiterRegex),
/* Get the node's full text. */
matchText = match[0],
/* Get only the match's text. */
subMatchText = match[1] || false;
/* RegEx queries that can return empty strings (e.g ".*")
produce an empty matchText which throws the entire
traversal process into an infinite loop due to the
position index not incrementing. Thus, we bump up
the position index manually, resulting in a zero-width
split at this location followed by the continuation
of the traversal process. */
if (matchText === "") {
matchPosition++;
/* If a RegEx submatch is produced that is not
identical to the full string match, use the submatch's
index position and text. This technique allows us to
avoid writing multi-part RegEx queries for submatch finding. */
} else if (subMatchText && subMatchText !== matchText) {
matchPosition += matchText.indexOf(subMatchText);
matchText = subMatchText;
}
/* Split this text node into two separate nodes at the
position of the match, returning the node that begins
after the match position. */
var middleBit = node.splitText(matchPosition);
/* Split the newly-produced text node at the end of the
match's text so that middleBit is a text node that
consists solely of the matched text. The other
newly-created text node, which begins at the end
of the match's text, is what will be traversed in
the subsequent loop (in order to find additional
matches in the containing text node). */
middleBit.splitText(matchText.length);
/* Over-increment the loop counter so that we skip
the extra node (middleBit) that we've just created
(and already processed). */
skipNodeBit = 1;
/* Create the wrapped node. Note: wrapNode code
is not shown, but it simply consists of creating
a new element and assigning it an innerText value. */
var wrappedNode = wrapNode(middleBit);
/* Then replace the middleBit text node with its
wrapped version. */
middleBit.parentNode.replaceChild(wrappedNode, middleBit);
}
```

This process isn't tremendously performant when used on a large bodies of text with a delimiter that produces a lot of small matches (namely, the *character* delimiter), but it's phenomenally robust and reliable.

## Wrapping up

Go forth and blast shit up ;-) If you create something cool, please post it on [CodePen](http://codepen.io) and share it in the comments below.

Follow [me on Twitter](http://twitter.com/shapiro) for tweets about UI manipulation.

## About
[
Julian Shapiro ](http://julian.com/)

Julian Shapiro is a technical founder. His first startup, NameLayer.com, was acquired by Techstars. His current focus is on UI animation. He's working to bring us one step closer to Minority Report. Read more at Julian.com.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 6 comments

Brett ZamirSeptember 3rd, 2014 at 12:46Jeff JonesSeptember 3rd, 2014 at 14:00Robert Nyman [Editor]September 3rd, 2014 at 14:46Rajat GargSeptember 3rd, 2014 at 21:39ElegSeptember 12th, 2014 at 10:51Julian ShapiroSeptember 14th, 2014 at 11:51