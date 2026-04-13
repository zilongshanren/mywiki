---
title: 'Svelto MiniExamples: GUI and Services Layer with Unity - Seba''s Lab'
url: https://www.sebaslab.com/svelto-miniexamples-gui-and-services-layer/
author: Sebastiano Mandalà
published: '2019-07-30'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

## 2022 Update

I leave this article up for historical purposes, but almost everything written here is not recommended anymore. The publisher/consumer tool especially was designed to let separate **EnginesRoots** communicate with each other in a thread-safe way. Any other use of it is confirmed to be an abuse, including the examples below. The current recommendation is to use a proper UI framework and *sync-engines* to sync models with entities. A better approach would be the creation of a dedicated UI Framework that can interface with Svelto entities, but that is something that may never see the light.

## Introduction:

The **Svelto.ECS **methods designed to implement ECS based GUIs are simple and powerful, following the fundamental principles around the whole Svelto implementation. Their design doesn’t involve the use of callbacks, as it relies on the power of Svelto.Tasks (but you can achieve similar results with other patterns like async/await) and it uses a naive, but efficient way to bind GUI elements to specific entities. In this article, we will see how to achieve this with a simple, but feature-complete scenario. [Source code is available on github as usual.](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example3-Unity%20Hybrid-GUI)

### The Scene

I strongly recommend using nested prefabs to build GUIs. This because the code is designed to handle every functional piece of the GUI as a separate widget that can be composed through nested prefabs, making it simple to create GUIs that would be potentially working out of the box.

Labels and Buttons are the simplest widgets. A Gridbox can be made of GridBoxCell and Buttons widgets, but the Gridbox itself can be a widget on its own, reusable by other GUIs. All the widgets’ logic is fully encapsulated, therefore their reuse should be as simple as reusing their entities and engines already developed.

Our project includes 3 widgets: a localized label, an input localized label (field) and a button with localized text:

![](../../assets/b33ddb2040932e9f.png)

The main GUI is an interface to input a display name and looks like:

![](../../assets/19efa0e16a8c32d6.png)

and this is the hierarchy of the GUI:

![](../../assets/9a4c50ad4825011b.png)

When developing GUIs with Svelto, the prefab hierarchy must be seen just a way like another to serialize the GUI structure. It must not be seen any differently than using a XAML based GUI for instance.

In this example, the DisplayName GUI is directly placed on the scene, but I’d rather load the GUI at run-time using addressable assets as otherwise, the scene will rapidly become a container of many guis.

### The Composition Root

let’s focus first on how the Svelto Entities are built from the scene.

The **SveltoGUIHelper **will help for this purpose. For this case we (sort of) serialize the entities in the prefab hierarchy through the use of the **EntityDescriptorHolder **(as seen in the Survival example).

Each gameobject that generates a Svelto Entity has an EntityDescriptorHolder like:

![](../../assets/455acdb2df8c7212.png)

![](../../assets/f80c61438ad517ae.png)

![](../../assets/2c062e3b30767b3e.png)

and so on, they do not coincidentally appear on the root of each nested prefab in the hierarchy.

let’s study the following code

//create the main GUI widget and relative entity var holder = SveltoGUIHelper.Create<DisplayNameDescriptorHolder>( new EGID(0, ExclusiveGroups.DisplayName), (contextHolder as UnityContext).transform, generateEntityFactory); //extract all the entities from its nested widgets var index = SveltoGUIHelper.CreateAll<ButtonEntityDescriptorHolder>(1, ExclusiveGroups.DisplayName, holder.transform, generateEntityFactory); index = SveltoGUIHelper.CreateAll<LocalizedTextDescriptorHolder>(index, ExclusiveGroups.DisplayName, holder.transform, generateEntityFactory); index = SveltoGUIHelper.CreateAll<InputFieldDescriptorHolder>(index, ExclusiveGroups.DisplayName, holder.transform, generateEntityFactory); SveltoGUIHelper.CreateAll<DisplayNameFeedbackLabelDescriptorHolder>(index, ExclusiveGroups.DisplayName, holder.transform, generateEntityFactory);

The first **Create **method builds the Svelto Entity found on the **DisplayNameDescriptorHolder **linked to the root *GameObject*. The following **CreateAll **build all the entities related to the nested widgets (prefabs) found in the GUI hierarchy.

Of course, these entities must be managed by the relative engines. For this example these are:

_enginesRoot.AddEngine(validateDisplayGuiInputEngine); _enginesRoot.AddEngine(new GenericGUIInteraction(entityStreamConsumerFactory)); _enginesRoot.AddEngine(new LocalizingTextEngine()); _enginesRoot.AddEngine(new ButtonClickingEventEngine()); _enginesRoot.AddEngine(new ClosingGUIEngine(entityStreamConsumerFactory));

GUI related svelto entities heavily rely on classic GameObjects and on the *Implementor-based* Object Oriented abstraction to abstract them, therefore Entity Descriptors are full of EntityViewStructs. Let’s see how they work in a few cases (the following explanation assumes that you know how [EntityViewStructs](https://github.com/sebas77/Svelto.ECS/wiki/EntityStructs-and-EntityViewStructs) and [Implementor](https://github.com/sebas77/Svelto.ECS/wiki/Why-Implementors%3F) work):

**LocalizedTextDescriptor **is an EntityDescriptor that generates an entity with a **LocalizedLabelEntityViewStruct** which holds an **ILabelText **label. The **ILabelText **is implemented by the implementor (*Monobehaviour*) **LabelTextProImplementor **to abstract **TextMeshProUGUI **objects. Of course, the implementor is found on the game object where the **TextMeshProUGUI **lies.

![](../../assets/f9ce8419aabff438.png)

**ILabelText textKey **receives an ID to identify the string to print. The key itself is a string just because theoretically it could be used as a key in a JSON file or similar text files.

the **LocalizedLabelEntityViewStruct** is managed by the **LocalizingTextEngine**. This engine reacts on add and when a **LocalizedLabelEntityViewStruct** is added, it switches its text from the selected key to a translated text. In this way, when the application starts, all the entities built with a label will automatically convert their keys into localized strings.

A naive **LocalizationService **is used to make the string localization ready. This static class doesn’t use the *Service Layer*, but shows how static classes could be used to hide away dependencies that are ECS-shy (I will discuss this more in-depth on another occasion).

**ValidateDisplayGUIInputEngine** is the main driver of the display name GUI logic. It has two responsibilities (hence it could have been split into two engines!): check that we are using a valid name and decide what to do when the submit button is clicked.

Let’s start with the validation as it shows some Svelto ECS features dedicated to the GUI-related logic. The first one is QueryUniqueEntity. This method, which can be useful in other contexts too, is a contract that guarantees that in the group chosen there must be only one entity. This shows the intention that we are using a group to identify a specific entity.

In this case, since we know that we have just one InputLabel, we fetch its entity through this code:

var inputField = entitiesDB.QueryUniqueEntity<InputFieldEntityViewStruct>(ExclusiveGroups.DisplayName) .inputField;

**ExclusiveGroups.DisplayName** is of course the group that identifies the entities that belong to the DisplayName GUI.

*In this method,* we also find an implementation of an official Svelto service layer. The Svelto Service is a much better abstraction of what can be provided by a simple static class like the LocalizationService.

The **IServiceFactory **maps service interfaces to their implementation. The implementation can change according to the context/composition root. For example in this case we are using a mock request, but the composition root could have created a real request, connecting to a real web server or whatever. Changing the service implementation won’t affect the code of the Engine that uses it.

This is how a ServiceFactory is implemented:

public class UserServicesFactoryMockup:ServiceRequestsFactory { public UserServicesFactoryMockup() { AddRelation<IUnifiedAuthVerifyDisplayNameService, UnifiedAuthVerifyDisplayNameService>(); //AddRelation<IAnotherService1, AnotherService1>(); //AddRelation<IAnotherService2, AnotherService2>(); } }

Service requests do not use callbacks but instead are fully integrated with Svelto.Tasks. In this case, we are using a service request that accepts an external dependency (the name to validate). The integration works in this way:

var unifiedAuthVerifyDisplayNameService = _serviceFactory.Create<IUnifiedAuthVerifyDisplayNameService>(); var checkNameValidity = unifiedAuthVerifyDisplayNameService.Inject(_currentString).Execute(); yield return checkNameValidity.Continue();

The service request implementation can be synchronous or asynchronous, as the *IEnumerator *will be able to handle both situations. The important thing to keep in mind is that *the next instruction after the yield will be executed only when the service completes its execution.*

**ValidateDisplayGUIInputEngine **assumes that the GUI can be opened and used only once, so it keeps its loop activated as long as the GUI is displayed.

The loop checks if the current string is different than the previous one checked, if so it asks the service layer to validate it and wait a second before checking again.

now the important bit: depending if the validation of the string has been successful or not, I need to write a different string into a specific label to give some feedback to the user. How would be possible to get hold of this specific label though?

The **EntityDescriptorHolder **has two optional fields: *Group Name and Id. *The **Group Name **is usually used more often together with **QueryUniqueEntity**. Setting a group name will build the specific entity in the specific group (and in case with a specific ID) overriding any other parameter. In this case, I am building the **NameError **label (I should have found a better name sorry) in the group named *DisplayName.FeedbackLabel* which is in fact **ExclusiveGroup.FeedbackLabel** (see code below)

![](../../assets/cdd9306814b74c50.png)

The trick is to map a *string *to a specific **ExclusiveGroup **using the new ExclusiveGroup constructor that accepts a string. In this case:

public static readonly ExclusiveGroup FeedbackLabel = new ExclusiveGroup("DisplayName.FeedbackLabel");

Which is used then as:

entitiesDB.QueryUniqueEntity<LocalizedLabelEntityViewStruct>(ExclusiveGroups.FeedbackLabel).label .text = unifiedAuthVerifyDisplayNameService.result == WebRequestResult.Success ? OnSuccess(unifiedAuthVerifyDisplayNameService.response) : OnFailure();

While all the DisplayName GUI unique entities can be found through the DisplayName ExclusiveGroup, the labels are not unique, therefore I use a new group to identify them. The EntityDescriptorHolder Group Name allows to glue of the Group to a specific label in the gameobject hierarchy.

The **CheckOKClicked** task waits for the **SubmitButton **to be clicked. If it’s clicked, it assumes that a valid name is found (which may be too naive as an approach, but OK for this example). Since the User has been validated, the UserEntity is moved to the group UserToRegister, which is irrelevant for this example, but shows how groups can be used as states too. A yield break will stop this task at this point.

IEnumerator CheckOKClicked() { while (entitiesDB.Exists<UserEntityStruct>(UniqueEGID.UserToValidate) == false) yield return Yield.It; using (var consumer = _buttonEntityConsumer.GenerateConsumer<ButtonEntityStruct>(ExclusiveGroups.DisplayName, "ValidateDisplayGUIInputEngine", 1)) { while (true) { while (consumer.TryDequeue(out var button)) { //User Is Now Validated if (button.message == ButtonEvents.OK) { _onScreenOpen = false; entitiesDB.QueryEntity<UserEntityStruct>(UniqueEGID.UserToValidate).name .Set(_validatedString); _entitiesFunction.SwapEntityGroup<UserEntityDescriptor>( UniqueEGID.UserToValidate, UniqueEGID.UserToRegister); yield break; } } yield return Yield.It; } } }

Let’s have a look at how the button logic works. The common GUI frameworks provide two basic GUI functionalities that are being assumed to be useful across all the GUIs:

**ButtonClickingEventEngine **reacts on **ButtonEntityViewStruct **entity add (which means when a Button entity is built and submitted) and registers the **DispatchOnSet **found inside the Button implementor to notify when a button has been pushed.

**DispatchOnSet **and **DispatchOnChange **use is much less relevant nowadays, but they haven’t been removed just because of the GUI pattern. Note that since their constructor needs now a valid EGID, it won’t be possible to instantiate them inside a monobehaviour. Hence their use has been slightly modified to be certain that they are used for valid reasons.

The **ButtonClickingEvent **Engine registers a listener to the Implementor **DispatchOnSet ***buttonEvent*. The implementor registers the listener to the UI.Button click event and dispatch a message back when the button is clicked. However, the new DispatchOnSet/Change cannot be used in multiple places and their new way to be used assumes that one and only one specific engine has the responsibility to handle their message. The consequence of handling this message can be modifying an entity as the only way to communicate with other engines.

public void Add(ref ButtonEntityViewStruct entityView) { entityView.buttonClick.buttonEvent = new DispatchOnSet<ButtonEvents>(entityView.ID); entityView.buttonClick.buttonEvent.NotifyOnValueSet(EnqueueButtonChange); }

What the publisher publishes is not custom data, but a copy of a modified **EntityStruct. ** In fact, the publisher/consumer pattern relies on an entity to be modified to work. This is why the** entitiesDB.PublishEntityChange** accepts only an **EGID**:

void EnqueueButtonChange(EGID egid, ButtonEvents value) { entitiesDB.QueryEntity<ButtonEntityStruct>(egid) = new ButtonEntityStruct(egid, value); entitiesDB.PublishEntityChange<ButtonEntityStruct>(egid); }

The publisher sends a warning if no consumers are registered, but doesn’t assume the number of consumers registered. *N consumers* can now register to a **ButtonEntityStruct **change and usually, the pattern is to have a consumer per Engine. The Engine is fully responsible to create the consumer and consume the data inside it. If a consumer is created, but no data is consumed, publishing will throw an exception.

We can now switch back to **ValidateDisplayGUIInputEngine** and see how the engine consumes **ButtonEntityStruct **changes:

using (var consumer = _buttonEntityConsumer.GenerateConsumer<ButtonEntityStruct>(ExclusiveGroups.DisplayName, "ValidateDisplayGUIInputEngine", 1)) { while (true) { while (consumer.TryDequeue(out var button)) { //User Is Now Validated if (button.message == ButtonEvents.OK) { _onScreenOpen = false; entitiesDB.QueryEntity<UserEntityStruct>(UniqueEGID.UserToValidate).name .Set(_validatedString); _entitiesFunction.SwapEntityGroup<UserEntityDescriptor>( UniqueEGID.UserToValidate, UniqueEGID.UserToRegister); yield break; } } yield return Yield.It; } }

The first thing to note is that we are creating a consumer that consumes only ButtonEntityStruct changes that come from the group ExclusiveGroups.DisplayName. This is important because we don’t want to listen to every button change. Note that the consumer has been created with a buffer of size 1: this is because we expect to consume at the same frequency of the publishing.

The Publisher/Consumer is the only Svelto.ECS class to be multi-thread safe (using fast locking), that because the pattern is useful also to let engines communicate between different threads. It’s also useful to let different EnginesRoots communicate together.

### Conclusion (what we have learned)

- Svelto ships with a subset of functionalities that help build GUIs. Svelto ECS-based GUI is strongly dependent on Gameobjects.
- Svelto ships with a set of methods that allow creating automatically ECS entities from game objects
- Monobehaviours as implementors are used to glue the GUI functionalities to the Svelto.ECS engines through the use of DispatchOnSet and DispatchOnChange
- Implementors fully abstract the OOP functionalities from the ECS ones. The engines are never aware of OO objects.
- The new ExclusiveGroup naming feature together with the EntityDescriptorHolder parameters allows binding specific entities to specific groups so that those entities can be used directly from Svelto.ECS engines. Changing the entity data will implicitly change the GUI data. (it’s a sort of databinding, but I don’t want to call it in this way as no events are involved)
- The new Service Layer interface/pattern allows to abstract services from ECS. It’s a useful design to follow for these cases.
- The Publisher/Consumer EnginesRoot functionality is powerful and can be used to let engines communicate with each other as a consequence of user events.