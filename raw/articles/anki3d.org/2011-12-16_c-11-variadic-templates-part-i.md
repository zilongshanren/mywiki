---
title: 'C++11: Variadic templates. Part I'
url: https://anki3d.org/cxx11-variadic-templates-part1/
author: Panagiotis Christopoulos Charitos
published: '2011-12-16'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

**UPDATE: Adding a new concept**

**UPDATE 24/Apr/2013: Fixing concept 3**

The new C++ standard, namely C++11, is here at last; offering many additions to the language’s core as well as in the companion library, the STL. Without doubt it will change the way we think and work but nobody can predict if it is for better or worst. The experimentation period is nearly over, only a handful of features missing from GCC and clang and the C++ engineers will have to learn and master the new tricks in both fronts (core and STL). For those familiar with boost library the second front should be an easy transaction to the new STL, for the first though we need tutorials and lots of them. This little article is one tutorial that extends the already published ones.

One of the new cool features is the variadic templates, simply put, templates with variable number of template parameters. To put it into context this is a variadic template:

template<typename... Types> struct Foo{};


In this article we will not present the basic usage of variadic templates. You can find great publications online (the wikipedia’s to name one) with an introduction and first steps, its not my intention to repeat the same in here. The present article’s purpose is to expand the wikipedia’s one by presenting a few cool things that now are doable. So, before proceeding please take a look at this first [http://en.wikipedia.org/wiki/Variadic_template](http://en.wikipedia.org/wiki/Variadic_template).

# Concept 1: Creating a visitor class

I’m not sure how the C++ scientists name that technique but because its pretty useful for all the examples I will call it “three way” technique. This technique has the word “three” because it utilizes three things. A forward declaration, a declaration and a partial template specialization. It’s purpose is to use the variadic parameters to do repetitive things.

This example explains an easy way to implement the visitor pattern. To construct a visitor we use the “three way”:

// Forward declaration (1st part) template<typename... Types> struct ConstVisitor; // Declaration (2nd part) template<typename First, typename... Types> struct ConstVisitor<First, Types...>: ConstVisitor<Types...> { using ConstVisitor<Types...>::visit; virtual void visit(const First&) = 0; }; // Specialized for one (3rd part) template<typename First> struct ConstVisitor<First> { virtual void visit(const First&) = 0; };

The declaration of ConstVisitor is recursive (second part) as the class inherits itself. This recursiveness needs to be stopped so we need a specialization for the single template parameter (third part). The forward declaration is there to satisfy the compiler. The above code defines the pure virtual visitor() methods for a number of types. Now lets see the class Base and its derived MyDouble and MyInt that utilize the visitor pattern.

// Forwards struct MyDouble; struct MyInt; /// Base class struct Base { typedef ConstVisitor<MyDouble, MyInt> MyConstVisitor; virtual void accept(MyConstVisitor&) = 0; }; /// Double struct MyDouble: Base { double x; void accept(Base::MyConstVisitor& v) { v.visit(*this); } }; /// Int struct MyInt: Base { int x; void accept(Base::MyConstVisitor& v) { v.visit(*this); } }; /// A visitor that does something struct PrintVisitor: Base::MyConstVisitor { void visit(const MyDouble& x) { std::cout << "I am a MyDouble: " << x.x << std::endl; } void visit(const MyInt& x) { std::cout << "I am a MyInt: " << x.x << std::endl; } };

The Base::MyConstVisitor is abstract and it contains two pure virtual methods, one for const MyDouble& and the second for const MyInt&. We used the Base::MyConstVisitor to create the PrintVisitor, a visitor that actually does something. The main may look like this:

int main(int, char**) { PrintVisitor vis; MyDouble md; md.x = 123.456; MyInt mi; mi.x = 987; Base* b = &md; b->accept(vis); b = &mi; b->accept(vis); }

And the output:

I am a MyDouble: 123.456 I am a MyInt: 987

The “variandic template way” to define a visitor does not do anything super smart or super useful. Its only a good way to save us from typing and nothing more.

# Concept 2: Getting the nth type of the variadic template class

Having a variadic template class we want to access the type of the nth template parameter. Once again using the “tree way” technique this is doable.

template<typename... Types> struct GetTypeUsingId { // Forward declaration template<int id, typename... Types_> struct Helper; // Declaration template<int id, typename TFirst, typename... Types_> struct Helper<id, TFirst, Types_...>: Helper<id - 1, Types_...> {}; // Specialized template<typename TFirst, typename... Types_> struct Helper<0, TFirst, Types_...> { typedef TFirst DataType; }; template<int id> using DataType = typename Helper<id, Types...>::DataType; }; int main(int, char**) { typedef GetTypeUsingId<double, int, std::string> MyFoo; MyFoo::DataType<0> a(1.23); MyFoo::DataType<1> b(123); MyFoo::DataType<2> c("Hello"); std::cout << a << " " << b << " " << c << std::endl; }

The GetTypeUsingId::Helper uses the “three way” to define a type, it takes as template argument an integer indicating the position of the template parameter. As you can see this id is getting decreased starting from N and it stops in the specialized GetTypeUsingId::Helper where the type is defined. In the main() the MyFoo::DataType

The output of main is:

1.23 123 Hello

# Concept 3: Getting the position of type in variadic template

Rationale: Imagine we have a variadic template class *Foo* that accepts a number of types and the typedef *MyFoo* that accepts tree common types. For example:

template<typename... Types> struct Foo {}; typedef Foo<int, float, std::string> MyFoo;

What we want is to get the type ID of one of the types at compile time. For example the:

std::cout << MyFoo::getTypeId<int>() << " " << MyFoo::getTypeId<float>() << " " << MyFoo::getTypeId<std::string>() << std::endl;

We want to output this:

0 1 2

To do that we will use the “three way” once more like this:

// Forward template<typename Type, typename... Types> struct GetVisitableId; // Declaration template<typename Type, typename First, typename... Types> struct GetVisitableId<Type, First, Types...>: GetVisitableId<Type, Types...> {}; // Specialized template<typename Type, typename... Types> struct GetVisitableId<Type, Type, Types...> { static const int ID = sizeof...(Types); };

This smart structure given a Type and a list of types defines a const integer indicating the Type’s position from the back of the list. The integer is named ID.

The last step is to add the getTypeId() in the Foo:

template<typename... Types> struct Foo { /// Using the GetVisitableId get the id of the @a T template<typename T> static constexpr int getTypeId() { return sizeof...(Types) - GetVisitableId<T, Types...>::ID - 1; } };

Once again with the recursive “tree way” technique we are able to do magic.

# Bottom line

After reading this you will be ready for the second part where it implements a variant-like structure. A concept that is complex and not that easy to understand. All the above concepts are needed to create a very fast and abstract class that behaves in almost the same way as the boost::variant.