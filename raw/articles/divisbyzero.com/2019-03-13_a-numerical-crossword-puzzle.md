---
title: A Numerical Crossword Puzzle
url: https://divisbyzero.com/2019/03/13/a-numerical-crossword-puzzle/
author: Dave Richeson
published: '2019-03-13'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I recently made [my first crossword puzzle](https://divisbyzero.com/2019/01/05/my-first-crossword-puzzle/). It was great fun. It had some mathematical clues, but it was not mathematical. So for my second crossword puzzle, I decided to make one that was 100% mathematical. Download my [numerical crossword puzzle](https://divisbyzero.com/wp-content/uploads/2019/03/clues-2.pdf) in which each cell contains a decimal point ” . ” or a digit 0 through 9. I have also created a [pdf of the solution](https://divisbyzero.com/wp-content/uploads/2019/03/crossnumberpuzzlesolutions.pdf).

Enjoy!

[Update 3/20: I changed a few of the clues.]

![Screen Shot 2019-03-13 at 6.49.10 PM.png](../../assets/081042cba229ee38.png)


![Screen Shot 2019-03-13 at 6.49.01 PM](../../assets/d7b35cf15b1e8dcc.png)


Hi Mr. Richerson,

We are two students of Tatyana Finkelstein at William Diamond Middle School. We finished the crossword puzzle, By the Numbers, today. It is an incredibly interesting puzzle to see how all the parts fit together and we learned quite a lot. However, upon finishing, checking and rechecking our answers and the answer key, we noticed two errors. The first is the clue for 41 across. Instead of the smallest number whose square has seven digits, it should be the smallest number whose square has eight digits. The second is the last digit of four down or the fourth digit of 20 across. Instead of 1, it should be a two. Again, these statements have only been made after many times of checking our work and confirmation. We really had fun completing this puzzle, and are really excited to see more of your work.

Sincerely,

Jaime Y. and Tara M,

Jaime and Tara,

I’m so glad you enjoyed the puzzle! That makes me very happy! I also appreciate you checking and double checking my work. I did not have anyone test out the puzzle before I posted it, so I was a little worried that I missed something. As for your two corrections: You are absolutely correct that “seven” should be “eight” in 41 across. I will fix that and upload a new puzzle page. Your second correction is that the “1” should be a “2” in the 4,4 cell of the puzzle. But I think it is already a 2 in the solution. Perhaps you mean that it should be a “1” and not a “2.” But the sequence of squares is 9, 16, 25, 36,… (20 across) and ceiling(sinh(9))=ceiling(4051.541…)=4052 (4 down) https://www.wolframalpha.com/input/?i=ceiling(sinh(9)). If I’m misunderstanding your correction, please let me know. Thanks again!

I thought that all the values were meant to be truncated not rounded, so my original answer for 4 down was also 4051.

The answer to 4 down is an integer. That bracket notation is called the ceiling function. It spits out the smallest integer greater than or equal to the value inside. See: https://www.wolframalpha.com/input/?i=ceiling(sinh(9))

Oh, right I didn’t see the ceiling. All good then!