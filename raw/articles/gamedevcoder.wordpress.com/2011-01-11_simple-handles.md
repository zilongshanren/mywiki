---
title: Simple handles
url: https://gamedevcoder.wordpress.com/2011/01/11/simple-handles/
published: '2011-01-11'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

So, here’s my first post – hello everyone out there!

Today I’m going to show you an extremely simple (and some may say hardcore!) way of managing user side handles to objects such as particle effects, sounds or animation instances in a typical C/C++ game engine. Specifically, this applies to any object types that once instantiated by the user might get destroyed by the system when the object’s life comes to an end, not necessarily when user decides to destroy it.

My main motivation for this post was trying to point out that you don’t always need a complex handle system (for example slot/age based one) whenever you deal with objects that may get destroyed without direct user action. The simpler, the better.

Particle effects, for example, often have some finite life time defined by the artist. When their life is over, we want particle system to destroy an effect. But we also want user who holds handle to an effect to have some way of knowing whether an effect is still valid. Or, in other words, we want to know whether the handle still points to a valid object.

Now, there’s probably few ways to accomplish this but I’m just going to focus on a simplest one. The idea is to use C/C++ pointers directly and have the system NULL the pointer when object is destroyed – hence we must somewhere store pointer to the pointer to an object. Now, to check whether handle is still valid all we have to do is a simple NULL check!

While this may sound like a potentially dangerous thing to do, in real life it’s okay. The main limitation of this approach is that you can’t have multiple handles to same object. This may or may not be a problem, depending on game’s needs. If it is, you must use a different approach. From my experience it wasn’t a problem with objects such as mentioned particle effects, sounds or animation instances. For all these we typically only need to store single handle inside some (parent) gameplay object.

Another limitation of proposed solution that I should point out is that you can’t just copy the handle. This is because pointer to it is stored inside handled object itself! This shouldn’t be a big problem but it means you should be clear about who is the owner of managed object.

Below C/C++ code snippet shows described approach for (particle) effect:

typedef Effect* EffectHandle; // This is our handle type // This is our particle effect class class Effect { public: static Effect* Create(EffectHandle* outHandle) { Effect* effect = new Effect(); // Create an effect effect->m_handlePtr = outHandle; // Store pointer to handle *outHandle = effect; // Set handle to point to an effect return effect; } static void Destroy(Effect* effect) { // Invalidate handle if (effect->m_handlePtr) *effect->m_handlePtr = NULL; // Delete the object delete effect; } // This allows us to change effect owner; in particular this allows for // detaching effect from owning object by passing NULL as a handle ptr void SetHandle(EffectHandle* handlePtr) { // Unlink previous owner if (m_handlePtr) *m_handlePtr = NULL; // Link new owner m_handlePtr = handlePtr; if (m_handlePtr) *m_handlePtr = this; } void SetPosition(float x, float y, float z) { /* ... */ } private: EffectHandle* m_handlePtr; // Pointer to handle that points to this effect };

Now, typically there’s also some particle system that manages all effects. Such system, during its update typically destroys effects whose life time is over – in our case it would be calling `Effect::Destroy()`

to do so.

And here’s what user side code to handle effects might look like:

class GameplayObject { public: GameplayObject() { Effect::Create(&m_handle); } ~GameplayObject() { if (m_handle) // Always check if valid Effect::Destroy(m_handle); } void Update() { if (m_handle) // Always check if valid { m_handle->SetPosition(0.0f, 0.0f, 0.0f); // Some gameplay condition that decides whether // to detach an effect if (...some condition...) // Note: this will also set our GameplayObject::m_handle to NULL m_handle->SetHandle(NULL); } } private: EffectHandle m_handle; };

What I like about this approach is its simplicity. It could be dangerous if not used properly but to me this still seems like best way to go where applicable (i.e. wherever up to one handle to an object is okay).

At the end I’d like to mention an extension to presented solution for when it’s desirable that the handled object gets destroyed automatically when its handle gets destroyed. To do that, we can simply replace our `void*`

pointer typedef’ed handle with a simple `EffectHandle`

class which triggers object destruction in its destructor:

class EffectHandle { public: inline EffectHandle() : m_effect(NULL) {} inline ~EffectHandle() { if (m_effect) m_effect->Destroy(); } inline Effect* GetEffect() const { return m_effect; } private: Effect* m_effect; };

Another bonus of implementing handle as a class is it gets initialized to NULL at construction time which makes for a cleaner and safer code.