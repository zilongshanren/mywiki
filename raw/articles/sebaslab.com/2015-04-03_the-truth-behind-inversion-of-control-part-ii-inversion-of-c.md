---
title: The truth behind Inversion of Control – Part II – Inversion of Control - Seba's
  Lab
url: https://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/
author: Sebastiano Mandalà
published: '2015-04-03'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

If you got here from my previous articles, you may have still many questions unanswered, with one possibly being: why is an IoC container called *Inversion Of Control* Container?

The first answer is: because someone chose historically a bad name** [1]**. The serious answer is: IoC containers take away the responsibility to create objects from the user and shift it to the framework. In this sense, they “invert” the control over the creation of dependencies.

*Inversion of Control* is another concept that turns out to be simple once it is fully understood and internalised. While using an IoC container to invert the creation of dependencies is easy to understand, visualising how to invert the control on the flow of the code execution is another matter. The process of adaptation is not straightforward since the entire code paradigm will have to change. In order to try to explain this paradigm, I will need to introduce the concept of code abstraction. The following definitions will be explored in more detail in the next articles, so come back here if they won’t be grasped immediately.

The inversion of control cannot be applied successfully without designing the application with multiple layers of abstraction. The higher the abstraction, the more generic the scope of the code. For example, a rendering module is part of the highest levels of abstraction since it could be used by whatever type of application that requires rendering. A module that enables entities to have health belongs to a more specialised layer as it would be useful to a smaller set of games that require entities to have health. More specialised modules may or may not depend on generic modules.

If we think of our code structure in terms of layers of abstraction, Inversion of control is all about giving control to the more abstracted modules instead than the specialised ones. You may ask: control of what? The idea is that framework classes should control both the *dependency* *creation***(Inversion Of Creation Control)** and the *logic***execution ****(Inversion of Flow Control)** of more specialised objects.

How can the object creation be inverted? Classes that follow the Inversion of Creation Control never use the **new **keyword explicitly to create dependencies. All the dependencies are always injected from the **Composition Root**, which I have already mentioned in my previous articles.

If you wonder how to create dynamic objects at run time without using the **new **keyword, like objects that must be spawned at run-time, you asked yourself a good question. These objects are always created by factories and factories are always created and passed as a dependency from the Composition Root.

Simply put, the **new **operator should be used only in the Composition Root or inside Factories. An IoC container hides this process, creating and passing all the dependencies automatically instead to force the user to pass them by constructors or setters. The application-agnostic IoC container code takes control of the creation of all the dependencies. Of course, dynamic allocation will still be used to allocate data structures, but data structures are not dependencies.

Why is inverting the creation control important? Mainly for the following three reasons:

- the code becomes independent from the constructor implementation. A dependency can, therefore, be passed by the interface, effectively removing all the coupling between the implementation of classes.
- Because of 1, your code will be dependent only on the abstraction of a class and not its implementation. In this way, it’s possible to swap implementations without changing the code.
- the object injected comes already created with its dependencies resolved. If the code had to create the instance of the object, those dependencies must have been known as well.
- the flow of the code can change according to the context. Without changing the code is possible to change its behaviour just by passing different implementations of the same interface.

The first point is fundamental to be able to mock up implementations when unit tests are written, but if unit tests are not part of your development process, the third point can lead to cleaner code when is time to implement different code paths.

**Manual Inversion of Creation Control Example:**

Can Inversion of Creation Control be achieved without using an IoC container? Absolutely, let’s see how simply using manual dependencies injection:

using System; using System.Collections.Generic; class Program { static void Main(string[] args) { var levelManager = new LevelManager(); var rand = new Random(); var player = new Player(rand); var enemyAFactory = new EnemyFactory<EnemyA>(rand); var enemyBFactory = new EnemyFactory<EnemyB>(rand); var level1EnemySpawner = new Level1EnemySpawner(enemyAFactory); var level2EnemySpawner = new Level2EnemySpawner(enemyAFactory, enemyBFactory); var level1 = new Level("Level 1", level1EnemySpawner, player); var level2 = new Level("Level 2", level2EnemySpawner, player); levelManager.Add(level1); levelManager.Add(level2); levelManager.Start(); while (levelManager.GameOver() == false) levelManager.Update(); } } class Level2EnemySpawner: IEnemySpawner { public Level2EnemySpawner(IEnemyFactory enemyAFactory, IEnemyFactory enemyBFactory) { _enemyAFactory = enemyAFactory; _enemyBFactory = enemyBFactory; } public IEnemy[] GenerateEnemies() { return new IEnemy[] { _enemyAFactory.Build(), _enemyBFactory.Build(), _enemyBFactory.Build() }; } IEnemyFactory _enemyAFactory; IEnemyFactory _enemyBFactory; } class Level1EnemySpawner: IEnemySpawner { public Level1EnemySpawner(IEnemyFactory enemyFactory) { _enemyFactory = enemyFactory; } public IEnemy[] GenerateEnemies() { return new IEnemy[] { _enemyFactory.Build(), _enemyFactory.Build() }; } IEnemyFactory _enemyFactory; } class EnemyFactory<T>:IEnemyFactory where T : IEnemy, new() { public EnemyFactory(Random rand) { _rand = rand; } public IEnemy Build() { var enemy = new T(); enemy.rand = _rand; return enemy; } Random _rand; } class EnemyA : IEnemy { public Random rand { private get; set; } public int energy { get { return _energy; } } public int Attack() { return rand.Next(0, 5); } public void Damage(int damageValue) { _energy -= damageValue; } int _energy = 10; } class EnemyB : IEnemy { public Random rand { private get; set; } public int energy { get { return _energy; } } public int Attack() { return rand.Next(0, 10); } public void Damage(int damageValue) { _energy -= damageValue; } int _energy = 10; } class Player { public Player(Random rand) { _rand = rand; } public int Attack() { return _rand.Next(1, 10); } public void Damage(int damageValue) { _energy -= damageValue; } public bool IsDead() { return _energy <= 0; } Random _rand; int _energy = 50; } class LevelManager { public void Add(ILevel level) { _levels.Add(level); } public void Start() { _levels[0].Start(); } public bool GameOver() { return _gameOver; } public void Update() { var level = _levels[_currentLevel]; if (level.isEnded == false) level.Update(); else if (_currentLevel < _levels.Count - 1) _levels[++_currentLevel].Start(); else _gameOver = true; } List<ILevel> _levels = new List<ILevel>(); int _currentLevel; bool _gameOver; } class Level : ILevel { public bool isEnded { get { return _isEnded || _player.IsDead(); } } public Level(string name, IEnemySpawner spawner, Player player) { _name = name; _spawner = spawner; _player = player; } public void Start() { Console.WriteLine(_name + " started"); _enemies = _spawner.GenerateEnemies(); } public void Update() { bool enemyAttacked = false; for (int i = 0; i <_enemies.Length; i++) { var enemy = _enemies[i]; if (enemy.energy > 0) { var damageE = enemy.Attack(); Console.WriteLine("enemy " + i + " inflicts damage: " + damageE); var damageP = _player.Attack(); Console.WriteLine("player attacks enemy " + i + " inflicts damage: " + damageE); enemy.Damage(damageP); _player.Damage(damageE); enemyAttacked = true; } } if (_player.IsDead()) { Console.WriteLine("Player Dead, GameOver"); Console.ReadKey(); } else if (enemyAttacked == false) { _isEnded = true; Console.WriteLine("Game Won, Congratulation"); } } string _name; bool _isEnded; IEnemy[] _enemies; IEnemySpawner _spawner; Player _player; } interface IEnemyFactory { IEnemy Build(); } interface ILevel { bool isEnded { get; } void Start(); void Update(); } interface IEnemy { int energy { get; } Random rand { set; } int Attack(); void Damage(int damage); } interface IEnemySpawner { IEnemy[] GenerateEnemies(); }

while I am not really good with examples, it’s not simple to find a compact one that is also meaningful. However, I think the above example includes all the discussed points.

*Main* is our simple Composition Root. It’s where all the dependencies are created and initially injected. If you try to run this code, it will actually work. It will run a dumb, not interactive simulation of a Player fighting Enemies.

All the game logic is encapsulated inside the *Level* class. Since the Level class uses the **Strategy Pattern [2]** in order to implement the functions needed by the

*LevelManager*class to manage a

*Level*, is possible to extend the logic of the game by creating new

*Level*classes. However adding

*Level*instances inside the

*LevelManager*is not Dependency Injection, so it is irrelevant to our exercise (

*LevelManager*doesn’t strictly need

*Level*instances injected to work, the class is still functional even without any

*Level*object added).

Each *Level* needs two dependencies. An implementation of an *IEnemySpawner* and the *Player object. *Note that the level name is not actually a dependency. A dependency is always an instance of a class needed by another class.

*level1* and *level2* are different because of the number and type of enemies created. *level1* contains only two enemies of type A, *level2* contains one enemy of type A and two enemies of Type B. Type B can be more powerful than type A when inflicts damage to the Player. However, the *Level implementation actually doesn’t change. The different behaviour is just due to the different implementation of the IEnemySpawner interface passed as a *parameter. Injecting two different *IEnemySpawner* objects changes the level gameplay, without changing the *Level* code.

*EnemySpawner* doesn’t build directly enemies, because is not its responsibility. The *Enemyspawner *just decides which enemies are spawned and how, but doesn’t need to be aware of what an enemy needs to be created.

As you can see both *EnemyA* and *EnemyB* depend on the implementation of the class *Random* to work, but *EnemySpawner* doesn’t need to know this dependency at all. Therefore we can use a factory both to encapsulate the operator *new* and pass the dependency *Random* directly from the composition root.

My explanation is probably more complicated than the example itself, where it’s clear that all the dependencies are created and passed through the constructor from inside the Composition Root. The only exception is when the EnemyFactory injects the Random implementation by the setter.

In this example, I haven’t used an Inversion of Control container but the control of the creation of the objects has been nevertheless inverted. The composition root and factories take away the responsibility of creating dependencies from the other objects, dependencies can be passed by the interface, and the flow of the code changes according to which implementation has been injected.

So the questions I am asking myself lately are: do we really need an IoC container to implement Inversion of Creation control? Are the side effects of using an IoC container more relevant than the benefits of using such a tool? Searching for an answer to these questions is what led me to start writing these articles.

I can give the first answer though: manual Dependency Injection is very hard to achieve with the Unity framework. As I have already widely explained in my past articles, due to the Unity framework nature, dependencies can be injected only through the use of singletons or the use of reflection. C# reflection abilities are what actually enables mine and other IoC containers to inject dependencies in an application made with Unity. So how can we possibly adopt manual dependency injection in Unity? One possible solution is to reinterpret the meaning of the Monobehaviour class in order to never need to inject dependencies into it. Is it possible? As we soon find out, if we change our coding paradigm, it’s not just possible, but also convenient to do.

For the time being, keep in mind that if the code is designed without really knowing what Inversion of Control is, an IoC container merely becomes a tool to simplify the tedious work of injecting dependencies; a tool that is very prone to be abused. An IoC container cannot be used efficiently without knowing how to design code that inverts creation and flows control.

But wait, so far I talked mainly about Inversion of Creation control although I mentioned several times the concept of Inversion of Flow Control, therefore I need to give a first explanation before concluding this article.

What is **Inversion of Flow Control**? Quoting Wikipedia:

*“**inversion of control** (**IoC**) describes a design in which custom-written portions of a **computer program** receive the **flow of control** from a generic, **reusable library**. A **software architecture* *with this design inverts control as compared to traditional **procedural programming**: in traditional programming, the custom code that expresses the purpose of the program **calls into** reusable libraries to take care of generic tasks, but with inversion of control, it is the reusable code that calls into the custom, or task-specific, code.”*

With normal procedure programming, the user objects use directly the functions/dependencies provided by more generic libraries.

With inverted flow control, the user objects are instead registered to and handled by the more generic libraries.

Inversion of Flow control is even more important than Inversion of Creation Control and I will explore the reasons in detail in my [next article](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/).

[1] [ http://martinfowler.com/articles/injection.html#InversionOfControl](http://martinfowler.com/articles/injection.html#InversionOfControl) (but read all of it)

I strongly suggest to read all my articles on the topic:

[http://www.sebaslab.com/ioc-container-for-unity3d-part-1/](http://www.sebaslab.com/ioc-container-for-unity3d-part-1/)[http://www.sebaslab.com/ioc-container-for-unity3d-part-2/](http://www.sebaslab.com/ioc-container-for-unity3d-part-2/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-i-dependency-injection/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-ii-inversion-of-control/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/)[http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/](http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/)[http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/](http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/)