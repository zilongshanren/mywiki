---
title: Finding Mom and Dad
url: http://hacksoflife.blogspot.com/2010/11/finding-mom-and-dad.html
author: Benjamin Supnik
published: '2010-11-10'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

There may be cases where I have an object O with sub-parts S1, S2, etc. where the implementation of S1/S2 could be made more efficient if part of their data could be pushed out to O. An example would be an object containing several intrinsic linked lists. The linked lists can be made faster by maintaining a stack of unused nodes, like this:

struct node {Our object contains two lists, but only one common stack pool.

node * next;

...

};

struct O {

node * S1_list_head;

node * S2_list_head;

node * free_stack_top;

};

We can use templates to safely hide away the maintenance of this code, sort of, e.g.

templateThere's just one problem: if we call pop_front and reverse the argument order for our head and free list, we are going to create a world of hurt. What we really want is something like S1_head_list.pop_front();

void pop_front(node *& head_list, node *& free_list)

{

* k = head_list;

head_list = head_list->next;

k->next = free_list;

free_list = k;

}

What I can't seem to find is a way to turn S1 and S2 into objects that have knowledge of their contained parts. In the above case, we would have to template S1 and S2 based on their byte offset from themselves to the location of their common section in the parent. That's something the compiler knows, but won't tell us, and we don't want to figure out by hand.

The best real alternative I suppose would be to wrap the templated list function in something inside O and then make the lists private, limiting the number of cases where a usage error of the template functions can occur.

The traditional work-around for this would be to include a pointer to O inside S1 and S2. This is clean and fool-proof, but also increases the storage requirements of S1 and S2; if we are storage sensitive to O, this isn't acceptable.

## No comments:

## Post a Comment