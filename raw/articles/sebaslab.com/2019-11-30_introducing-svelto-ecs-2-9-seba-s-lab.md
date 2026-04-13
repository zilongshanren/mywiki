---
title: Introducing Svelto ECS 2.9 - Seba's Lab
url: https://www.sebaslab.com/introducing-svelto-ecs-2-9/
author: Sebastiano Mandalà
published: '2019-11-30'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

Being busy on multiple fronts, I recently went AWOL from this blog, but Svelto is keeping up well with the new technologies (read Unity DOTS) and we are actively developing it for our new game [Gamecraft](https://store.steampowered.com/app/1078000/Gamecraft/). I am also spending my little spare time to develop Svelto 3.0, which will introduce new exciting features. Until then I won’t able to write the ECS related articles I have been meaning to write for a while now.

While Svelto 3.0 will introduce new group types to fill some gaps of the current logic and add total compatibility with Unity jobs (read: I am going to use unmanaged memory for internal data structures), Svelto 2.9 has been released mainly to introduce many new serialisation related features. There is a lot I like about the new features and a few things I don’t. This means that the serialisation code will very likely improve/evolve with the next versions of Svelto. Biggest missing feature is the possibility to serialise (read dump) an entire EnginesRoot with a single function. This is partially due to a design choice that may not seem logical at first: the serialisation logic is not driven by the entity components (entity structs), but is driven by the entity IDs. With the ECS memory layout, it would be logic to serialise the entity structs as they are found in the arrays in memory. This is an option that I may introduce later on (it’s not hard), but currently entities are serialised/deserialised through their entity descriptors/IDs. This makes simple to serialise an entity coherently.

I have written some tests for the purpose to check the serialisation features, you can find them at the [Svelto.ECS.Tests repository](https://github.com/sebas77/Svelto.ECS.Tests). The new tests are found in the new file **SveltoTestSerialization.cs** where I will show the most important 2.9 features.

## Serialise Entities with Entity Structs only

**Test: **TestSerializingToByteArrayNewEnginesRoot

With Svelto ECS 2.9, new classes have been introduced. Let’s start from the **SerializableEntityDescriptor**. I thought for a long time if I actually needed this class or not. At this point in time I reckon it’s necessary as it helps to identify the entity descriptor through a serialisable hash. The reason why the hash is not automatically assigned based on the name of the class is obvious: just renaming the class would break existing serialised files.

This is currently how a **SerializableEntityDescriptor **is normally declared.

```
class SerializableEntityDescriptor : SerializableEntityDescriptor<
SerializableEntityDescriptor.DefaultPatternForEntityDescriptor>
{
[HashName("DefaultPatternForEntityDescriptor")]
internal class DefaultPatternForEntityDescriptor : IEntityDescriptor
{
public IEntityBuilder[] entitiesToBuild => _entitiesToBuild;
static readonly IEntityBuilder[] _entitiesToBuild = {
new EntityBuilder<EntityStructNotSerialized>(),
new SerializableEntityBuilder<EntityStructSerialized>(),
new SerializableEntityBuilder<EntityStructSerialized>
((SerializationType.Storage, new DefaultSerializer<EntityStructSerialized>()) ,
(SerializationType.Network, new DefaultSerializer<EntityStructSerialized>())),
new SerializableEntityBuilder<EntityStructPartiallySerialized>
((SerializationType.Storage, new PartialSerializer <EntityStructPartiallySerialized>())
)
};
}
}
```


I hope you find the code self-explanatory.

The **HashName **attribute is mandatory. A run-time exception will be launched if not used. Changing its value will break serialisation compatibility, so it should be set once for ever. Uncoupling it from the name of the class would allow safe renaming.

A **SerializableEntityDescriptor **allows the serialization of standard **EntityDescriptor **that has a **HashName **and that uses **SerializableEntityBuilders**. Using a **SerializableEntityBuilder **on a standard **EntityDescriptor **won’t cause any problem. However the serialisation logic will serialise only *unmanaged* entity structs that are built through a **SerializableEntityBuilder**.

When a **SerializableEntityBuilder **is used without parameters, the serializers are initialised with the *DefaultSerializer*. If parameters are used, they define a touple formed by a **SerializationType **and an **ISerializer **implementation. Any **SerializationType** value not used is automatically set as *DontSerialize*.

The **SerializationType **is part of the framework at the moment, but it shouldn’t be, not on this form at least. However I am pleased by the **ISerializer **implementation idea, it’s flexible and allows any kind of serialisation you have in mind. You can, of course, implement your **ISerializer**, so that you can cover all the cases, like optimising data (through compression and or quantization) or serialising to different formats.

This code shows an example of how to use the serialization framework:

```
[TestCase]
public void TestSerializingToByteArrayNewEnginesRoot()
{
var init = _entityFactory.BuildEntity<SerializableEntityDescriptor>(0, NamedGroup1.Group);
init.Init(new EntityStructSerialized() { value = 5 });
init.Init(new EntityStructSerialized2() { value = 4 });
init.Init(new EntityStructPartiallySerialized() { value1 = 3 });
init = _entityFactory.BuildEntity<SerializableEntityDescriptor>(1, NamedGroup1.Group);
init.Init(new EntityStructSerialized() { value = 4 });
init.Init(new EntityStructSerialized2() { value = 3 });
init.Init(new EntityStructPartiallySerialized() { value1 = 2 });
_simpleSubmissionEntityViewScheduler.SubmitEntities();
FasterList<byte> bytes = new FasterList<byte>();
var generateEntitySerializer = _enginesRoot.GenerateEntitySerializer();
var simpleSerializationData = new SimpleSerializationData(bytes);
generateEntitySerializer.SerializeEntity(new EGID(0, NamedGroup1.Group),
simpleSerializationData, SerializationType.Storage);
generateEntitySerializer.SerializeEntity(new EGID(1, NamedGroup1.Group),
simpleSerializationData, SerializationType.Storage);
_enginesRoot.Dispose();
var newEnginesRoot = new EnginesRoot(_simpleSubmissionEntityViewScheduler);
newEnginesRoot.AddEngine(_neverDoThisIsJustForTheTest);
simpleSerializationData.Reset();
generateEntitySerializer = newEnginesRoot.GenerateEntitySerializer();
generateEntitySerializer.DeserializeNewEntity(new EGID(0, NamedGroup1.Group), simpleSerializationData,
SerializationType.Storage);
generateEntitySerializer.DeserializeNewEntity(new EGID(1, NamedGroup1.Group), simpleSerializationData,
SerializationType.Storage);
_simpleSubmissionEntityViewScheduler.SubmitEntities();
Assert.That(_neverDoThisIsJustForTheTest.entitiesDB.QueryEntity<EntityStructSerialized>(0, NamedGroup1.Group).value, Is.EqualTo(5));
Assert.That(_neverDoThisIsJustForTheTest.entitiesDB.QueryEntity<EntityStructSerialized2>(0, NamedGroup1.Group).value, Is.EqualTo(4));
Assert.That(_neverDoThisIsJustForTheTest.entitiesDB.QueryEntity<EntityStructPartiallySerialized>(0, NamedGroup1.Group).value1, Is.EqualTo(3));
Assert.That(_neverDoThisIsJustForTheTest.entitiesDB.QueryEntity<EntityStructSerialized>(1, NamedGroup1.Group).value, Is.EqualTo(4));
Assert.That(_neverDoThisIsJustForTheTest.entitiesDB.QueryEntity<EntityStructSerialized2>(1, NamedGroup1.Group).value, Is.EqualTo(3));
Assert.That(_neverDoThisIsJustForTheTest.entitiesDB.QueryEntity<EntityStructPartiallySerialized>(1, NamedGroup1.Group).value1, Is.EqualTo(2));
}
```


In these examples I show only file serialisation, but this kind of implementation can be used for any kind of serialisation, for example we currently use it in *Gamecraft *also to serialize entities over the network. Registering a different kind of Serialiser per **SerializationType **does the trick, giving the possibility to change serialisation strategies according the **SerializationType**.

## Serialise Entities with Versioning

**Test: **TestSerializingWithEntityStructsWithVersioning

Versioning is also possible and simple to implement. Just duplicate the involved Entity Descriptors and Entity Structs and use a new hashname for the new version, maintaining the old one for the previous version. The system will automatically identify the previous version, but it will be built as the new version once serialised again which works through the use of a custom factory. A **DefaultVersioningFactory **is provided for this purpose, which will cover most of the cases. Check the test **TestSerializingWithEntityStructsWitVersioning** to understand how it works.

## Serialise Entities with Entity View Structs

**Test: **TestSerializingWithEntityViewStructsAndFactories

Entity Structs are simpler to serialise, being *unmanaged struct* . Entity View Structs contain references instead, therefore cannot be serialised as they are. I could have taken the decision to let the user create custom serialisers for **EntityViewStruct**, but eventually I found it unnecessary. The only issue remains about serialising strings, but since strings are tricky, I left to the user solving the problem. However **ECSString **can be used to let an Entity Struct reference a string and therefore a specialised serialiser can be written to serialise the string it points to. The interesting part about handling Entity view structs is the deserialization as entities with Entity view structs cannot be automatically created. They need, in fact, at least a reference to an *implementor *object. For this reason the Svelto ECS framework supports the registration of deserializing factories. Those are factories that are pre-registered and called during the serialization.

Attempting to deserialize an entity with Entity View Structs without registering a factory, will result in to run-time exceptions, unless the **EnginesRoot **is created with the flag *isDeserializationOnly *set to true (which is useful to deserialize data in order to query it rather than actually using it)

## Other changes (random order of importance):

- more thorough disposing of the
*EnginesRoot* - an
*EnginesRoot*reference should never be held, unless it’s a weak reference. The code changed to stick to this rule (it actually was already like that previously) *IReactOnAddAndRemove*callbacks are now guaranteed to be called after all the entity structs generated by the same entity have been added and before any is removed. both functions pass the EGID of the analysing entity by parameter now, so that the entity struct won’t need to implement*INeedEGID*for this sole purpose.- The
*IReactOnSwap***MovedFrom**method has been removed, it is now redundant. - Entities built or removed during the
*IReactOnAddAndRemove*callbacks are now added and removed immediately and not on the next submission like used to happen. This avoid some awkward checks that were previously needed inside engines. *EntityStreams*can get (optionally) the**EGID**of the entity published, so that the*EntityStruct*won’t need an INeedEGID for this sole purpose.- Groups are not trimmed anymore when they are emptied to avoid allocations.
- Removed a bunch of run-time allocations that weren’t supposed to happen in Release and/or when the Profile define is used in editor
*(for debugging reasons Svelto.ECS may need to use strings at run-time, but Svelto.ECS is allocation zero in Release and when the Profile keyword is used)* - A improved the
**DynamicEntityDescriptor**and**ExtendibleEntityDescriptor**code and more notably, introduced the new method**ExtendedWith<>**to facilitate the writing of modular and reusable entity descriptors. - Several minor code design improvements/optimisations