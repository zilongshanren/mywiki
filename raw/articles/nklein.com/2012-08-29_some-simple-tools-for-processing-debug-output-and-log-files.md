---
title: 'Some simple tools for processing debug output and log files :: nklein software'
url: http://nklein.com/2012/08/some-simple-tools-for-processing-debug-output-and-log-files/
author: Pat
published: '2012-08-29'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

In my current job, we do a great deal of “ex post facto” debugging from debug data that we record during operations. To help me do off-the-cuff analysis of these, I make heavy use of egrep and sed. I have created three scripts that encapsulate the most common patterns where I had complicated sed lines before.

The three scripts are:

`clip`

– used to pluck out a particular portion of a line based on a regex of what comes before the portion and a regex of what comes after it`clipc`

– like clip except counts the number of occurrences of each unique plucked-out portion`clips`

– like clip but assumes the plucked out portion is numeric and outputs the sum of all of the plucked out portions

For example, if I had [a snippet of Apache log files](http://szabgab.com/talks/fundamentals_of_perl/apache-log-report-hosts.html):

127.0.0.1 - - [10/Apr/2007:10:39:11 +0300] "GET /favicon.ico HTTP/1.1" 200 766 "-" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

139.12.0.2 - - [10/Apr/2007:10:40:54 +0300] "GET / HTTP/1.1" 500 612 "-" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

139.12.0.2 - - [10/Apr/2007:10:40:54 +0300] "GET /favicon.ico HTTP/1.1" 200 766 "-" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

127.0.0.1 - - [10/Apr/2007:10:53:10 +0300] "GET / HTTP/1.1" 500 612 "-" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

127.0.0.1 - - [10/Apr/2007:10:54:08 +0300] "GET / HTTP/1.0" 200 3700 "-" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

127.0.0.1 - - [10/Apr/2007:10:54:08 +0300] "GET /style.css HTTP/1.1" 200 614 "http://pti.local/" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

127.0.0.1 - - [10/Apr/2007:10:54:08 +0300] "GET /img/pti-round.jpg HTTP/1.1" 200 17524 "http://pti.local/" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

127.0.0.1 - - [10/Apr/2007:10:54:21 +0300] "GET /unix_sysadmin.html HTTP/1.1" 200 3880 "http://pti.local/" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

217.0.22.3 - - [10/Apr/2007:10:54:51 +0300] "GET / HTTP/1.1" 200 34 "-" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

217.0.22.3 - - [10/Apr/2007:10:54:51 +0300] "GET /favicon.ico HTTP/1.1" 200 11514 "-" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

217.0.22.3 - - [10/Apr/2007:10:54:53 +0300] "GET /cgi/pti.pl HTTP/1.1" 500 617 "http:/contact.local/" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

127.0.0.1 - - [10/Apr/2007:10:54:08 +0300] "GET / HTTP/0.9" 200 3700 "-" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

217.0.22.3 - - [10/Apr/2007:10:58:27 +0300] "GET / HTTP/1.1" 200 3700 "-" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

217.0.22.3 - - [10/Apr/2007:10:58:34 +0300] "GET /unix_sysadmin.html HTTP/1.1" 200 3880 "http://pti.local/" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

217.0.22.3 - - [10/Apr/2007:10:58:45 +0300] "GET /talks/Fundamentals/read-excel-file.html HTTP/1.1" 404 311 "http://pti.local/unix_sysadmin.html" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.3) Gecko/20061201 Firefox/2.0.0.3 (Ubuntu-feisty)"

Then, I might like to quickly see how often different URLs are fetched. I could do this with:

1 /cgi/pti.pl

1 /img/pti-round.jpg

1 /style.css

1 /talks/Fundamentals/read-excel-file.html

2 /unix_sysadmin.html

3 /favicon.ico

7 /

If I want to see how often GET is done from various IP addresses, I could do this:

8 127.0.0.1

2 139.12.0.2

6 217.0.22.3

If I wanted to add up the number of bytes sent sending successful pages, do:

50078

The `clip`

program defaults to having the what-comes-before regex matching open paren, open bracket, double quote, single quote, or equal sign. It defaults to having the what-comes-after regex matching close paren, close bracket, double quote, single quote, comma, or whitespace. So, if I wanted just the first few dates from the above, I wouldn’t need any arguments:

10/Apr/2007:10:39:11

10/Apr/2007:10:39:11

10/Apr/2007:10:40:54

Or, I might be interested in my busiest minute:

8 10/Apr/2007:10:54

### Implementations of the Above Scripts

The `clip`

could be written simply in a few lines of Perl:

my $post = shift || '[,\s"\')\]]';

while ( my $line = <> ) {

# look for $pre followed by whitespace then the (non-greedy) portion to keep

# followed by some (non-greedy) amount of whitespace followed by $post.

print "$1\n" if ( $line =~ m{$pre\s*(.*?)\s*?$post}o );

}

From there, `clipc`

is simply:

clip "$@" | sort | uniq -c | sed -e 's/^ *//'

And, `clips`

is simply:

clip "$@" | awk '// { SUM += $1 } END { printf("%d\n", SUM) }'