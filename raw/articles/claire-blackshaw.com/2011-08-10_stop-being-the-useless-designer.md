---
title: Stop being the Useless Designer
url: https://claire-blackshaw.com/blog/2011/08/stop-being-the-useless-designer/
author: Claire Blackshaw
published: '2011-08-10'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Stop being the Useless Designer](../../assets/4e402aebc4c1a4e8.png)

### Part 1: Excel & Formulas

![](/images/Blog/lazydesign-300x300.png)

Let’s face it, there is nothing more annoying than being bossed about by someone who is useless.[?](https://claire-blackshaw.com#foot1)

So here are three simple rules.

- Work with them in the trenches.
- Everyone in the trenches has to be useful.
- Supplement don’t Replace
[?](https://claire-blackshaw.com#foot2)

[?](https://claire-blackshaw.com#foot3)

Though I encourage you to jump into your own tunnels of exploration. I hope this is the first of a multi-part post focusing on various tools or hard skills for designers. Introducing a tool or skill, then getting you interested.

**THE BEST PLACE TO START IS YOUR IN-HOUSE TOOLS!!!**

### Part 1: Excel & Formulas

Excel is the brick and mortar tool for the designer. Through really any decent spreadsheet software will do and have most the features I list, so pardon the Excel centric explanations.

With Excel you can build entire complex systems and mimic game systems. Allowing you to not only prototype systems but also balance and analyze them.

#### Formula Introduction

Equations are the bread and butter for Excel. So here is a crash course introduction.=10 + 5 + C2 - SUM($A$1:D10)+Sheet2!A2


| = | must be the first character to indicate it’s a formula. |
| 10 | You can use “magic numbers”
|

[More help here](http://office.microsoft.com/en-gb/starter-help/create-or-change-a-cell-reference-HP010342370.aspx)[Excel Introduction](http://office.microsoft.com/en-gb/excel-help/quick-start-create-a-formula-HA010370615.aspx)

#### Named Cells

Things without a name or context are extremely frustrating. Often a design workbook can become massive. So if a cell is used in many places or referenced on different sheets then NAME IT! It goes without saying your sheets should be named as well. This is the most common tip I give for Excel.**Naming a Sheet**: Double click on the sheet name - [Further Guidance](http://office.microsoft.com/en-gb/excel-help/rename-a-worksheet-HA010377063.aspx)

**Naming a Cell**: Click the cell name to the left of the formula bar. -

[Further Guidance](http://office.microsoft.com/en-gb/excel-help/define-named-cell-references-or-ranges-HP005201536.aspx)

**Naming a Range**: Same as cell but selects a range.

#### Random Numbers

Random numbers are always needed.Generates a random float between [0:1] from which all your calculations can flow.=Rand()


Gotcha / Quick Tip: The random number changes every time Excel does an evaluation pass which you can force by pressing F9.

#### VLOOKUP is your friend

VLOOKUP allows you to find data matching your request in a range of data. It’s the backbone of many of my formulas. The most common use case for this I found is when I have data from a separate source and I want to perform a bunch of lookups to bring data together on another sheet to add meaning.Using the lookup_value it finds the row in the table array then returns the Nth item in that row relative to the start of the table, based on col_index_num. range_loopup which allows you to have fuzzy matches.VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])


One Gotcha is that the look_up value must be in the first column of the data, so sometimes you need to rejig you data a bit.

[Further Guidance](http://office.microsoft.com/en-gb/excel-help/vlookup-function-HP010343011.aspx)

#### The Power of Pivot Tables

Ah, the best kept secret of excel. You can either select a bunch of data already in Excel and go Insert -> Pivot Table or you can just import from a Data Source like SQL.Then you can group and reformat your data in ways which are so useful. Now I grabbed some sample data from [contextures.com](http://www.contextures.com/xlsampledata01.html). It’s a bunch of sales data for multiple stores. Here is a sample cut out.

|
OrderDate |
Region | Rep | Item | Units | Unit Cost | Total |
| 1/6/10 | Quebec | Jones | Pencil | 95 | 1.99 | 189.05 |
| 1/23/10 | Ontario | Kivell | Binder | 50 | 19.99 | 999.50 |

You can quickly pull out summaries and analysis on data with this tool. I strongly encourage you explore it further as entire books have been written on the topic. Feel the power of pivot ;-)

[Further Guidance](http://office.microsoft.com/en-us/excel-help/pivottable-reports-101-HA001034632.aspx)

#### Cell Formatting

Humans like colour, seeing a page of number means very little to us. So wherever possible get things into graphs or charts. Though sometimes that’s not appropriate. In these cases conditional cell formatting is your friend. It can quickly highlight highs / lows, relative values or just point out the bottom or top 10% for example. This kind of quick visual reference point will often highlight problem areas in your game systems.**Quick Tip**: Setting your numbers to the same colour as the background preserves the data but brings forward the formatting icons, letting you shrink the cells.

[Further Guidance](http://office.microsoft.com/en-us/excel-help/quick-start-apply-conditional-formatting-HA010370614.aspx)

#### Bins and Frequency

Using data bins is a common trick in data analysis. By breaking things into discrete chunks for analysis you can speed up calculations and perform analyses which otherwise would be difficult or impossible. For instance, say you are looking at a bunch of kill data for players which has the exact position and time of death. By breaking the timeline into chunks (or bins) and turning the map into a grid (breaking x & y into bins) you have group the data into manageable chunks.First thing you will need to do is define your bin size and range. I recommend making a named cell for size (or step), minimum and maximum, then using relative formulas to make a range of bins. Lastly, select the cells which will have the result and use this formula.

Gotcha: This is an ARRAY formula so be sure to press CTRL + SHIFT + ENTER when finishing the formula. If you’ve done it right your numbers will appear and { } will surround it to indicate an array formula.=FREQUENCY(data_array,bins_array)


## Conclusion

I hope your palate is whetted by this sample of the power of Excel. With a bit of thought you should be able to model prototypes, mode balance systems, analyze your systems, process information and help out in the trenches.A last word of warning, do not try build your game in excel. Such way leads to madness and wasted time, instead model individual systems. When looking to plug those systems together often a data sample export / import is your friend. :)

At the end of the day all your game mechanics boil down to numbers. Getting those numbers right, improving your systems and optimising is one of the best things you can do for your game and Excel is one of the most fundamental tools in that arsenal.

## Footnotes

[#Please note: I’m not dismissing high-level design or the need to get an overview on the project but too often useless people use these as shields to hide incompetence.]

[#You have a team of specialists who will always have more time and expertise than you in many things. Look to understand their work, support them, and refine the design with your increased knowledge but never try do their job.]

[#Hard in terms of based on solid fact, brick and mortar stuff, as opposed to soft skills like communication and developing a feel for a product which can often be more difficult to master.]

[#Magic Number is a constant number used in line in a formula or code. Referred to as such because it has no context or reference. So anyone else looking at your work is immediate lost as to its source or context.]