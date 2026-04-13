---
title: C++, ownership and shared_ptr
url: https://anteru.net/blog/2011/c-ownership-and-shared-ptr
published: '2011-09-12'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I’m a big fan of C++ `shared_ptr`

– or I should rather say, I used to be a big fan. Lately I ran into some issues where the “shared ownership” model promoted by liberate use of `shared_ptr`

started to make the code more complex and error prone. Let’s start with the actual code in question and take a look at a a possible solution.

A bit of context before we start: The code sample will consist of two classes, `Draw2D`

and `Draw2DText`

. The classes themselves don’t matter too much, but the relationship is important. On creation, `Draw2D`

allocates some hardware context in order to draw elements. This hardware context should be released when the `Draw2D`

instance is destroyed to free resources. All text instances created by a particular `Draw2D`

instance are bound to that hardware context. That means that once the `Draw2D`

instance is destroyed, all elements created by it are practically useless as the only operation that can be performed on them safely is destruction.

An additional complication is not crucial to the discussion, but is necessary to understand the first design. The `Draw2D`

instance must be able to iterate over all items it has created when the window size changes to re-layout them. I know that this can be solved with container classes and callbacks, but for the sake of simplicity there is only `Draw2D`

and the `Draw2DText`

, so `Draw2D`

must keep some kind of link to its children. We will have to take care of this for the first design, but it will follow “naturally” for the later designs.

Without much further ado, the original implementation:

```
class Draw2D
{
std::shared_ptr<Draw2DText> CreateText (...)
{
auto text = new Draw2DText;
auto ptr = std::shared_ptr<Draw2DText> (text,
std::bind (&Draw2D::Release, this, _1));
// Add ptr to elements_
return ptr;
}
void Draw (const Draw2DText& text)
{
// Use the Draw2D state to draw the text
}
void Update ()
{
// Loop over all elements, call element->Update()
// If element is expired, add to free list
// Remove all items from the free list
}
void Release (Draw2DText* e)
{
// Find e in elements_
// Remove the corresponding pointer if found
}
std::vector<std::weak_ptr<Draw2DText>> elements_;
};
```


This approach does work, but has a few hidden drawbacks:

- Probably the smallest problem, but by default, a lot of
`shared_ptr`

copying happens here, which is not really “free” due to lots of atomic instructions. The real problem is deeper: We’re doing as-if the`shared_ptr`

has ownership of the object, while it hasn’t. - The
`Draw2D`

instance must perform garbage collection on its end, even though it is responsible for its created items. There is an ownership relation between`Draw2D`

and its children, which is nowhere to be found in the code. - We’re creating a function object per
`shared_ptr`

which doesn’t do much interesting stuff. - Iterating over the items requires us to lock before use and keep track of the items ready for garbage collection (yes, we can remove them while iterating, but it’s still something we have to handle.)

Overall, the problem stems from the fact that while there are many good uses for `shared_ptr`

, expressing ownership is not. In this case, the `Draw2D`

instance “owns” its `Draw2DText`

instances as those become invalid when the `Draw2D`

instance is destroyed. Moreover, the client, who has ownership of the `Draw2D`

instance has clearly knowledge when he lets loose of the `Draw2DText`

instances as the current design already does not allow using the `Draw2DText`

instances after the Draw2D instance is destroyed.

Ok, so what can do? The first change we can add is to destroy the `Draw2DText`

instances from the `Draw2D`

destructor. This is possible as the shared_ptr goes through the Release indirection, which means we can safely remove the objects without notifying the `shared_ptr`

. With this change in place, the user cannot use the text elements for sure as they are now pointing to invalid memory, but the user couldn’t use them before either. In addition, we can easily check if the user tries to use a stale object by checking first if the object is registered with this particular `Draw2D`

instance.

Let’s look closer now at what we have: All child instance lifetimes are now directly bound to the owner, so we actually don’t have to free them manually unless we choose to do so. This is good, but during the lifetime of the `Draw2D`

instance we now force the user to do manual memory management.

Can we get the same thing easier? Yes, we can, by ditching all `shared_ptr`

usage in Draw2D/Draw2DText and only provide them as an option. Let’s see, if we use plain pointers now, we are still able to delete all instances when the `Draw2D`

instance is destroyed. Nothing lost here. Giving out plain pointers to the user indicates that there is an ownership question that the user should look up in the documentation. Fortunately, if the user does not read it, we’re not leaking memory still as we are going to release the memory at the end. This leaves us with a single problem: The user cannot use the comfort provided by the old system. This can be easily resolved though by introducing a custom function which produces exactly the same `shared_ptr`

as before, i.e. with a custom deleter calling `Release ()`

. The new implementation:

```
class Draw2D
{
~Draw2D ()
{
// Loop over all elements, delete element
}
Draw2DText* CreateText (...)
{
auto text = new Draw2DText;
// No further magic required here
// Add text to elements_
return text;
}
void Draw (const Draw2DText& text)
{
// Use the Draw2D state to draw the text
}
void Update ()
{
// Loop over all elements, call element->Update()
// No free list management here
}
void Release (Draw2DText* e)
{
// Find e in elements_
// Remove the corresponding pointer if found
}
std::vector<Draw2DText*> elements_;
};
```


Assuming that `Draw2D`

is marked as non-copyable, it’s just as safe to use as before. The ownership is more visible than before while the user can opt-in to a slow, but simple reference counting via `shared_ptr`

.

As we have seen, `shared_ptr`

s don’t always lead to simpler or easier to understand code, and in some cases, they actually obfuscate the relationship and lifetime between objects. Its also interesting to see that this case couldn’t have been handled easily in managed languages: Either you would wind up with circular references (`Draw2D`

to `Draw2DElement`

and back), which only get released once all references to the `Draw2D`

instance and it’s children is unreachable, or you have an explicit method like “Dispose” on the `Draw2D`

instance which releases the underlying hardware context and simply renders everything unusable.

I’m curious if there is a better way to design this code to completely resolve this issue. Of course, keeping the hardware context alive would be the easiest, but we explicitly want to allow the user to manage the lifetime of this manually. Given the constraints, I have the strong feeling that this approach is the way to go.

Having implemented this, I’m also starting to get the impression that explicit lifetime management is often easier than expected. In many cases, there is a clear relationship between objects. As long as the release method is explicitly tied to the parent object, it is always clear when the lifetime of an object ends. While I’m still using `shared_ptr`

in many places, I’m more aware of the potential problems they bring.