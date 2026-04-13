---
title: On Commands and Events - Seba's Lab
url: https://www.sebaslab.com/on-commands-and-events/
author: Sebastiano Mandalà
published: '2012-12-01'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

Events and Commands are two communication tools that I use really often. I have planned more exhaustive articles on the topic, but now I want to write a short post about one rule I apply when I use them. Sometimes it occurs to me the question: should the listener class know the dispatcher class or the dispatcher class know the listener class?

Generally I answer in this way:

If I use event listeners, I inject the dispatcher inside the class which defines the method callback, ie:

class IListenSomething:IoC.IInitialize { [IoC.Inject] public IDispatcher dispatcher { private get; set; } public void OnInject() { dispatcher.OnSomething += Callback; } private void Callback() { } }

In this way I do not need to expose the private members of the listener.

On the other way around, if I use the command pattern to achieve object communication (and I do it at lot), I usually invert the logic.

public class DoSomething: IDoSomething { public void Do() {} } public class DoSomethingCommand:ICommand { [IoC.Inject] public IDoSomething doer; public void Execute() { doer.do(); } } public class Dispacher { [Inject] internal ICommandFactory commandFactory {private get; set;} public void OnSomethingHappened() { var someCommand = commandFactory.Build<DoSomethingCommand>(); someCommand.Execute(); } }

This because the Command Pattern add an extra layer of abstraction that does not let the dispatch and the listener know each other directly.

Using this rule I often end up with tidy code, so I hope it can help you as well.


Short yet interesting article! This is a topic that is often overlooked, even being so important to game programming. I’ve been using the command pattern for a while in games, and it helped me keeping the code more organized, centralizing actions’ codes in a single place. I also implemented (sort of) a command pattern on my dependency injection container (https://github.com/intentor/adic#using-commands), and I’d like your input on the way commands are dispatched (not necessarily about the container, but more in a general sense). The pattern states that we should have an invoker class, just like in your example. However, to make… Read more »

Hello, I now use generics as well. I also don’t remember what that CommandDispatcher was, I am going to remove it from the example. I don’t use middle classes to dispatch, but I do use a CommandFactory. Knowing the type of a command is not a problem for coupling, it doesn’t make much sense to abstract commands. Some IoC containers use Command Maps, mapping events to commands, but I don’t like this solution to be part of a framework.

Thanks for the reply!

Now I accept in peace of mind that my approach is ok!