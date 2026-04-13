---
title: One Weird Trick to Write Better Code
url: https://etodd.io/2015/09/28/one-weird-trick-better-code/
published: '2015-09-28'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# One Weird Trick to Write Better Code

Developers hate him!

We'll cover some standard tips and tricks here, but we're not really interested in those. We're looking for the One Weird Trick to rule them all. Hopefully each trick we encounter brings us closer to coding Mecca.

### In the beginning

The first video game I ever wrote was called *Ninja Wars.*

![](../../assets/303abd9dd2dd1b95.png)

Yes, that is an HTML table of images. I changed the src attribute to move stuff around.

The top of the Javascript file looked like this:

```
var x = 314;
var y = 8;
var prevy= 1;
var prevx= 1;
var prevsw= 0;
var row= 304;
var endrow= 142;
var sword= 296;
var yrow = 0;
var yendrow = 186;
var I = 0;
var e = 0;
var counter = 0;
var found = 0;
var esword = 26;
var eprevsw = 8;
var bluehealth = 40;
var redhealth = 40;
var n = 0;
var you = 'ninja';
var bullet = 'sword';
var enemy = 'enemy';
var ebullet = 'enemysword';
var besieged = 0;
var siegecount = 0;
var esiegecount = 0;
var ebesieged = 0;
var healthcount = 0;
var player = 0;
var starcount = 0;
var infortress = false;
var prevyou = you;
var einfortress = false;
var prevenemy = enemy;
var previmg = "";
var prevbullet= "";
var eprevbullet= "";
var randnum = 0;
var randnum2 = 0;
var randnum3 = 0;
var randnum4 = 0;
var buildcount = 0;
var characters = new Array(4);
characters = ['ninja','tank','heli','builder'];
var bullets = new Array(3);
bullets = ['sword','bullet','5cal','sword'];
var echaracters = new Array(3);
echaracters = ['enemy','tank2','eheli','ebuilder'];
var ebullets = new Array(3);
ebullets = ['enemysword','bullet2','e5cal','enemysword'];
var health = new Array(4);
health = [40,30,20,10];
var prevorb = 0;
var prevnum = 0;
```


Hopefully this looks somewhat familiar, and I'm not the only one to start out writing code like this. Regardless, this debacle demonstrates our first trick:

### Trick #1: globals are evil

At this point, we don't even know why they're evil, we just intuitively know.

*edit: I should clarify that I'm no longer against globals. But that's
getting ahead of ourselves.*

Pretty soon we learn about objects. We can group our variables:

```
class Ninja
{
int x, y;
int previousX, previousY;
int health = 100;
}
class Sword
{
int x, y;
int previousX, previousY;
int sharpness = 9000;
}
```


We can even use inheritance to avoid copy-pasting:

```
class Movable
{
int x, y;
int previousX, previousY;
}
class Ninja : public Movable
{
int health = 100;
}
class Sword : public Movable
{
int sharpness = 9000;
}
```


Inheritance is nice! Nice enough to serve as our next trick:

### Trick #2: object-oriented programming

Object-oriented is so great that it forms the core of many classic games,
including Doom 3. Which, coincidentally, [is open source](https://github.com/id-Software/DOOM-3-BFG).

Doom 3 loves inheritance. Don't believe me? Here's a small subset of its class hierarchy:

idClass idEntity idAnimatedEntity idWeapon idAFEntity_Base idAFEntity_ClawFourFingers idAFEntity_VehicleidAFEntity_VehicleFourWheelsidAFEntity_VehicleSixWheels idAFEntity_Gibbable idAFEntity_WithAttachedHead idActoridPlayeridAI

Imagine you're an employee at id Software. This inheritance hierarchy works great for a few months. Then, one fateful Monday, disaster strikes. The boss comes in and says "Hey, change of plans. The player is now a car."

Look at idPlayer and
idAFEntity_VehicleFourWheels in the hierarchy.
Big Problem #1: we need to move a *lot* of code.

Big Problem #2: the boss comes to his senses and calls off the "player is a car" idea. Instead, we're adding turrets to everything. The car is becoming a Halo Warthog, and the player is getting a giant turret mounted on his back.

As lazy programmers, we decide to use inheritance again to avoid copy-pasting. But look at the hierarchy. Where can we put the turret code? The only ancestor shared by idPlayer and idAFEntity_VehicleFourWheels is idAFEntity_Base.

We'll probably put the code in idAFEntity_Base and add a boolean flag called turret_is_active. We'll only set it true for the car and the player. This works, but the terrible, logical conclusion is that our base classes end up loaded with tons of cruft. Here's the source code for idEntity.

Go ahead, scroll through it. You don't have to read it all.

```
class idEntity : public idClass {
public:
static const int MAX_PVS_AREAS = 4;
static const uint32 INVALID_PREDICTION_KEY = 0xFFFFFFFF;
int entityNumber; // index into the entity list
int entityDefNumber; // index into the entity def list
idLinkList<idEntity> spawnNode; // for being linked into spawnedEntities list
<idEntity> activeNode; // for being linked into activeEntities list
<idEntity> aimAssistNode; // linked into gameLocal.aimAssistEntities
idLinkList<idEntity> snapshotNode; // for being linked into snapshotEntities list
int snapshotChanged; // used to detect snapshot state changes
int snapshotBits; // number of bits this entity occupied in the last snapshot
bool snapshotStale; // Set to true if this entity is considered stale in the snapshot
idStr name; // name of entity
// key/value pairs used to spawn and initialize entity
// contains all script defined data for this entity
int thinkFlags; // TH_? flags
int dormantStart; // time that the entity was first closed off from player
bool cinematic; // during cinematics, entity will only think if cinematic is set
renderView_t * renderView; // for camera views from this entity
* cameraTarget; // any remoteRenderMap shaders will use this
idList< idEntityPtr<idEntity>, TAG_ENTITY > targets; // when this entity is activated these entities entity are activated
int health; // FIXME: do all objects really need health?
struct entityFlags_s {
bool notarget :1; // if true never attack or target this entity
bool noknockback :1; // if true no knockback from hits
bool takedamage :1; // if true this entity can be damaged
bool hidden :1; // if true this entity is not visible
bool bindOrientated :1; // if true both the master orientation is used for binding
bool solidForTeam :1; // if true this entity is considered solid when a physics team mate pushes entities
bool forcePhysicsUpdate :1; // if true always update from the physics whether the object moved or not
bool selected :1; // if true the entity is selected for editing
bool neverDormant :1; // if true the entity never goes dormant
bool isDormant :1; // if true the entity is dormant
bool hasAwakened :1; // before a monster has been awakened the first time, use full PVS for dormant instead of area-connected
bool networkSync :1; // if true the entity is synchronized over the network
bool grabbed :1; // if true object is currently being grabbed
bool skipReplication :1; // don't replicate this entity over the network.
int timeGroup;
bool noGrab;
renderEntity_t xrayEntity;
qhandle_t xrayEntityHandle;
const idDeclSkin * xraySkin;
void DetermineTimeGroup( bool slowmo );
void SetGrabbedState( bool grabbed );
bool IsGrabbed();
public:
ABSTRACT_PROTOTYPE( idEntity );
idEntity();
~idEntity();
void Spawn();
void Save( idSaveGame *savefile ) const;
void Restore( idRestoreGame *savefile );
const char * GetEntityDefName() const;
void SetName( const char *name );
const char * GetName() const;
virtual void UpdateChangeableSpawnArgs( const idDict *source );
int GetEntityNumber() const { return entityNumber; }
// clients generate views based on all the player specific options,
// cameras have custom code, and everything else just uses the axis orientation
virtual renderView_t * GetRenderView();
// thinking
virtual void Think();
bool CheckDormant(); // dormant == on the active list, but out of PVS
virtual void DormantBegin(); // called when entity becomes dormant
virtual void DormantEnd(); // called when entity wakes from being dormant
bool IsActive() const;
void BecomeActive( int flags );
void BecomeInactive( int flags );
void UpdatePVSAreas( const idVec3 &pos );
void BecomeReplicated();
// visuals
virtual void Present();
virtual renderEntity_t *GetRenderEntity();
virtual int GetModelDefHandle();
virtual void SetModel( const char *modelname );
void SetSkin( const idDeclSkin *skin );
const idDeclSkin * GetSkin() const;
void SetShaderParm( int parmnum, float value );
virtual void SetColor( float red, float green, float blue );
virtual void SetColor( const idVec3 &color );
virtual void GetColor( idVec3 &out ) const;
virtual void SetColor( const idVec4 &color );
virtual void GetColor( idVec4 &out ) const;
virtual void FreeModelDef();
virtual void FreeLightDef();
virtual void Hide();
virtual void Show();
bool IsHidden() const;
void UpdateVisuals();
void UpdateModel();
void UpdateModelTransform();
virtual void ProjectOverlay( const idVec3 &origin, const idVec3 &dir, float size, const char *material );
int GetNumPVSAreas();
const int * GetPVSAreas();
void ClearPVSAreas();
bool PhysicsTeamInPVS( pvsHandle_t pvsHandle );
// animation
virtual bool UpdateAnimationControllers();
bool UpdateRenderEntity( renderEntity_s *renderEntity, const renderView_t *renderView );
static bool ModelCallback( renderEntity_s *renderEntity, const renderView_t *renderView );
virtual idAnimator * GetAnimator(); // returns animator object used by this entity
// sound
virtual bool CanPlayChatterSounds() const;
bool StartSound( const char *soundName, const s_channelType channel, int soundShaderFlags, bool broadcast, int *length );
bool StartSoundShader( const idSoundShader *shader, const s_channelType channel, int soundShaderFlags, bool broadcast, int *length );
void StopSound( const s_channelType channel, bool broadcast ); // pass SND_CHANNEL_ANY to stop all sounds
void SetSoundVolume( float volume );
void UpdateSound();
int GetListenerId() const;
idSoundEmitter * GetSoundEmitter() const;
void FreeSoundEmitter( bool immediate );
// entity binding
virtual void PreBind();
virtual void PostBind();
virtual void PreUnbind();
virtual void PostUnbind();
void JoinTeam( idEntity *teammember );
void Bind( idEntity *master, bool orientated );
void BindToJoint( idEntity *master, const char *jointname, bool orientated );
void BindToJoint( idEntity *master, jointHandle_t jointnum, bool orientated );
void BindToBody( idEntity *master, int bodyId, bool orientated );
void Unbind();
bool IsBound() const;
bool IsBoundTo( idEntity *master ) const;
idEntity * GetBindMaster() const;
jointHandle_t GetBindJoint() const;
int GetBindBody() const;
idEntity * GetTeamMaster() const;
idEntity * GetNextTeamEntity() const;
void ConvertLocalToWorldTransform( idVec3 &offset, idMat3 &axis );
idVec3 GetLocalVector( const idVec3 &vec ) const;
idVec3 GetLocalCoordinates( const idVec3 &vec ) const;
idVec3 GetWorldVector( const idVec3 &vec ) const;
idVec3 GetWorldCoordinates( const idVec3 &vec ) const;
bool GetMasterPosition( idVec3 &masterOrigin, idMat3 &masterAxis ) const;
void GetWorldVelocities( idVec3 &linearVelocity, idVec3 &angularVelocity ) const;
// physics
// set a new physics object to be used by this entity
void SetPhysics( idPhysics *phys );
// get the physics object used by this entity
* GetPhysics() const;
// restore physics pointer for save games
void RestorePhysics( idPhysics *phys );
// run the physics for this entity
bool RunPhysics();
// Interpolates the physics, used on MP clients.
void InterpolatePhysics( const float fraction );
// InterpolatePhysics actually calls evaluate, this version doesn't.
void InterpolatePhysicsOnly( const float fraction, bool updateTeam = false );
// set the origin of the physics object (relative to bindMaster if not NULL)
void SetOrigin( const idVec3 &org );
// set the axis of the physics object (relative to bindMaster if not NULL)
void SetAxis( const idMat3 &axis );
// use angles to set the axis of the physics object (relative to bindMaster if not NULL)
void SetAngles( const idAngles &ang );
// get the floor position underneath the physics object
bool GetFloorPos( float max_dist, idVec3 &floorpos ) const;
// retrieves the transformation going from the physics origin/axis to the visual origin/axis
virtual bool GetPhysicsToVisualTransform( idVec3 &origin, idMat3 &axis );
// retrieves the transformation going from the physics origin/axis to the sound origin/axis
virtual bool GetPhysicsToSoundTransform( idVec3 &origin, idMat3 &axis );
// called from the physics object when colliding, should return true if the physics simulation should stop
virtual bool Collide( const trace_t &collision, const idVec3 &velocity );
// retrieves impact information, 'ent' is the entity retrieving the info
virtual void GetImpactInfo( idEntity *ent, int id, const idVec3 &point, impactInfo_t *info );
// apply an impulse to the physics object, 'ent' is the entity applying the impulse
virtual void ApplyImpulse( idEntity *ent, int id, const idVec3 &point, const idVec3 &impulse );
// add a force to the physics object, 'ent' is the entity adding the force
virtual void AddForce( idEntity *ent, int id, const idVec3 &point, const idVec3 &force );
// activate the physics object, 'ent' is the entity activating this entity
virtual void ActivatePhysics( idEntity *ent );
// returns true if the physics object is at rest
virtual bool IsAtRest() const;
// returns the time the physics object came to rest
virtual int GetRestStartTime() const;
// add a contact entity
virtual void AddContactEntity( idEntity *ent );
// remove a touching entity
virtual void RemoveContactEntity( idEntity *ent );
// damage
// returns true if this entity can be damaged from the given origin
virtual bool CanDamage( const idVec3 &origin, idVec3 &damagePoint ) const;
// applies damage to this entity
virtual void Damage( idEntity *inflictor, idEntity *attacker, const idVec3 &dir, const char *damageDefName, const float damageScale, const int location );
// adds a damage effect like overlays, blood, sparks, debris etc.
virtual void AddDamageEffect( const trace_t &collision, const idVec3 &velocity, const char *damageDefName );
// callback function for when another entity received damage from this entity. damage can be adjusted and returned to the caller.
virtual void DamageFeedback( idEntity *victim, idEntity *inflictor, int &damage );
// notifies this entity that it is in pain
virtual bool Pain( idEntity *inflictor, idEntity *attacker, int damage, const idVec3 &dir, int location );
// notifies this entity that is has been killed
virtual void Killed( idEntity *inflictor, idEntity *attacker, int damage, const idVec3 &dir, int location );
// scripting
virtual bool ShouldConstructScriptObjectAtSpawn() const;
virtual idThread * ConstructScriptObject();
virtual void DeconstructScriptObject();
void SetSignal( signalNum_t signalnum, idThread *thread, const function_t *function );
void ClearSignal( idThread *thread, signalNum_t signalnum );
void ClearSignalThread( signalNum_t signalnum, idThread *thread );
bool HasSignal( signalNum_t signalnum ) const;
void Signal( signalNum_t signalnum );
void SignalEvent( idThread *thread, signalNum_t signalnum );
// gui
void TriggerGuis();
bool HandleGuiCommands( idEntity *entityGui, const char *cmds );
virtual bool HandleSingleGuiCommand( idEntity *entityGui, idLexer *src );
// targets
void FindTargets();
void RemoveNullTargets();
void ActivateTargets( idEntity *activator ) const;
// misc
virtual void Teleport( const idVec3 &origin, const idAngles &angles, idEntity *destination );
bool TouchTriggers() const;
idCurve_Spline<idVec3> *GetSpline() const;
virtual void ShowEditingDialog();
enum {
EVENT_STARTSOUNDSHADER,
EVENT_STOPSOUNDSHADER,
EVENT_MAXEVENTS
};
// Called on clients in an MP game, does the actual interpolation for the entity.
// This function will eventually replace ClientPredictionThink completely.
virtual void ClientThink( const int curTime, const float fraction, const bool predict );
virtual void ClientPredictionThink();
virtual void WriteToSnapshot( idBitMsg &msg ) const;
void ReadFromSnapshot_Ex( const idBitMsg &msg );
virtual void ReadFromSnapshot( const idBitMsg &msg );
virtual bool ServerReceiveEvent( int event, int time, const idBitMsg &msg );
virtual bool ClientReceiveEvent( int event, int time, const idBitMsg &msg );
void WriteBindToSnapshot( idBitMsg &msg ) const;
void ReadBindFromSnapshot( const idBitMsg &msg );
void WriteColorToSnapshot( idBitMsg &msg ) const;
void ReadColorFromSnapshot( const idBitMsg &msg );
void WriteGUIToSnapshot( idBitMsg &msg ) const;
void ReadGUIFromSnapshot( const idBitMsg &msg );
void ServerSendEvent( int eventId, const idBitMsg *msg, bool saveEvent, lobbyUserID_t excluding = lobbyUserID_t() ) const;
void ClientSendEvent( int eventId, const idBitMsg *msg ) const;
void SetUseClientInterpolation( bool use ) { useClientInterpolation = use; }
void SetSkipReplication( const bool skip ) { fl.skipReplication = skip; }
bool GetSkipReplication() const { return fl.skipReplication; }
bool IsReplicated() const { return GetEntityNumber() < ENTITYNUM_FIRST_NON_REPLICATED; }
void CreateDeltasFromOldOriginAndAxis( const idVec3 & oldOrigin, const idMat3 & oldAxis );
void DecayOriginAndAxisDelta();
uint32 GetPredictedKey() { return predictionKey; }
void SetPredictedKey( uint32 key_ ) { predictionKey = key_; }
void FlagNewSnapshot();
idEntity* GetTeamChain() { return teamChain; }
// It is only safe to interpolate if this entity has received two snapshots.
enum interpolationBehavior_t {
USE_NO_INTERPOLATION,
USE_LATEST_SNAP_ONLY,
USE_INTERPOLATION
};
interpolationBehavior_t GetInterpolationBehavior() const { return interpolationBehavior; }
unsigned int GetNumSnapshotsReceived() const { return snapshotsReceived; }
protected:
renderEntity_t renderEntity; // used to present a model to the renderer
int modelDefHandle; // handle to static renderer model
// used to present sound to the audio engine
idVec3 GetOriginDelta() const { return originDelta; }
idMat3 GetAxisDelta() const { return axisDelta; }
private:
idPhysics_Static defaultPhysicsObj; // default physics object
* physics; // physics used for this entity
* bindMaster; // entity bound to if unequal NULL
// joint bound to if unequal INVALID_JOINT
int bindBody; // body bound to if unequal -1
* teamMaster; // master of the physics team
* teamChain; // next entity in physics team
bool useClientInterpolation; // disables interpolation for some objects (handy for weapon world models)
int numPVSAreas; // number of renderer areas the entity covers
int PVSAreas[MAX_PVS_AREAS]; // numbers of the renderer areas the entity covers
signalList_t * signals;
int mpGUIState; // local cache to avoid systematic SetStateInt
uint32 predictionKey; // Unique key used to sync predicted ents (projectiles) in MP.
// Delta values that are set when the server or client disagree on where the render model should be. If this happens,
// they resolve it through DecayOriginAndAxisDelta()
idMat3 axisDelta;
interpolationBehavior_t interpolationBehavior;
unsigned int snapshotsReceived;
private:
void FixupLocalizedStrings();
bool DoDormantTests(); // dormant == on the active list, but out of PVS
// physics
// initialize the default physics
void InitDefaultPhysics( const idVec3 &origin, const idMat3 &axis );
// update visual position from the physics
void UpdateFromPhysics( bool moveBack );
// get physics timestep
virtual int GetPhysicsTimeStep() const;
// entity binding
bool InitBind( idEntity *master ); // initialize an entity binding
void FinishBind(); // finish an entity binding
void RemoveBinds(); // deletes any entities bound to this object
void QuitTeam(); // leave the current team
void UpdatePVSAreas();
// events
void Event_GetName();
void Event_SetName( const char *name );
void Event_FindTargets();
void Event_ActivateTargets( idEntity *activator );
void Event_NumTargets();
void Event_GetTarget( float index );
void Event_RandomTarget( const char *ignore );
void Event_Bind( idEntity *master );
void Event_BindPosition( idEntity *master );
void Event_BindToJoint( idEntity *master, const char *jointname, float orientated );
void Event_Unbind();
void Event_RemoveBinds();
void Event_SpawnBind();
void Event_SetOwner( idEntity *owner );
void Event_SetModel( const char *modelname );
void Event_SetSkin( const char *skinname );
void Event_GetShaderParm( int parmnum );
void Event_SetShaderParm( int parmnum, float value );
void Event_SetShaderParms( float parm0, float parm1, float parm2, float parm3 );
void Event_SetColor( float red, float green, float blue );
void Event_GetColor();
void Event_IsHidden();
void Event_Hide();
void Event_Show();
void Event_CacheSoundShader( const char *soundName );
void Event_StartSoundShader( const char *soundName, int channel );
void Event_StopSound( int channel, int netSync );
void Event_StartSound( const char *soundName, int channel, int netSync );
void Event_FadeSound( int channel, float to, float over );
void Event_GetWorldOrigin();
void Event_SetWorldOrigin( idVec3 const &org );
void Event_GetOrigin();
void Event_SetOrigin( const idVec3 &org );
void Event_GetAngles();
void Event_SetAngles( const idAngles &ang );
void Event_SetLinearVelocity( const idVec3 &velocity );
void Event_GetLinearVelocity();
void Event_SetAngularVelocity( const idVec3 &velocity );
void Event_GetAngularVelocity();
void Event_SetSize( const idVec3 &mins, const idVec3 &maxs );
void Event_GetSize();
void Event_GetMins();
void Event_GetMaxs();
void Event_Touches( idEntity *ent );
void Event_SetGuiParm( const char *key, const char *val );
void Event_SetGuiFloat( const char *key, float f );
void Event_GetNextKey( const char *prefix, const char *lastMatch );
void Event_SetKey( const char *key, const char *value );
void Event_GetKey( const char *key );
void Event_GetIntKey( const char *key );
void Event_GetFloatKey( const char *key );
void Event_GetVectorKey( const char *key );
void Event_GetEntityKey( const char *key );
void Event_RestorePosition();
void Event_UpdateCameraTarget();
void Event_DistanceTo( idEntity *ent );
void Event_DistanceToPoint( const idVec3 &point );
void Event_StartFx( const char *fx );
void Event_WaitFrame();
void Event_Wait( float time );
void Event_HasFunction( const char *name );
void Event_CallFunction( const char *name );
void Event_SetNeverDormant( int enable );
void Event_SetGui( int guiNum, const char *guiName);
void Event_PrecacheGui( const char *guiName );
void Event_GetGuiParm(int guiNum, const char *key);
void Event_GetGuiParmFloat(int guiNum, const char *key);
void Event_GuiNamedEvent(int guiNum, const char *event);
};
```


The point is, that's a lot of code. Notice how every single entity — down to the last piece of physics debris — has a concept of a team, and of getting killed. Clearly not ideal.

If you're a Unity developer, you already know the solution: components! Here's what they look like:

![](../../assets/2e9f389e3711f253.jpg)

Rather than inheriting functionality, Unity entities are just bags of components. This solves our earlier turret problem easily: just add a turret component to the player and car entities.

Here's what Doom 3 might look like if it used components:

idPlayer idTransform idHealth idAnimatedModel idAnimator idRigidBody idBipedalCharacterController idPlayerController idAFEntity_VehicleFourWheels idTransform idAnimatedModel idRigidBody idFourWheelController ...

What have we learned?

### Trick #3: in general, favor composition over inheritance

Take a moment to review the tricks we've covered so far: global variables bad, objects good, components better.

*You won't believe what happens next!*

Let's take a small detour into the world of low-level performance with a very simple question: which function is faster?

```
double a(double x)
{
return Math.sqrt(x);
}
static double[] data;
double b(int x)
{
return data[x];
}
```


We'll hand-wave a lot of complexity away and just assume that these two functions eventually compile down to one x86 instruction each. Function a will probably compile to sqrtps, and function b might compile to some kind of mov instruction.

sqrtps takes about 14 CPU cycles on a modern
Intel processor, according to [Intel's manual](http://www.intel.com/content/www/us/en/architecture-and-technology/64-ia-32-architectures-optimization-manual.html).
What about movq?

The answer is "it's complicated". It depends on where we load data from.

| Registers | ~40 per core, sort of | 0 cycles | |
| L1 | 32KB per core | 64B line | 4 cycles |
| L2 | 256KB per core | 64B line | 11 cycles |
| L3 | 6MB | 64B line | 40-75 cycles |
| Main memory | 8GB | 4KB page | 100-300 cycles |

That last number is important. **100-300 cycles** to hit main memory!
This means in any given situation, our biggest bottleneck is probably
memory access. And from the looks of it, we can improve this by using
L1, L2, and L3 cache more often. How do we do that?

Let's return to Doom 3 for a real-life example. Here's the Doom 3 update loop:

```
for ( idEntity* ent = activeEntities.Next();
ent != NULL;
ent = ent->activeNode.Next() )
{
if ( g_cinematic.GetBool() && inCinematic && !ent->cinematic )
{
ent->GetPhysics()->UpdateTime( time );
continue;
}
timer_singlethink.Clear();
timer_singlethink.Start();
RunEntityThink( *ent, cmdMgr );
timer_singlethink.Stop();
ms = timer_singlethink.Milliseconds();
if ( ms >= g_timeentities.GetFloat() )
Printf( "%d: entity '%s': %.1f ms\n", time, ent->name.c_str(), ms );
num++;
}
```


From an object-oriented perspective, this code is pretty clean and generic. I'm assuming RunEntityThink calls some virtual Think() method where we could do just about anything. Very extensible.

Uh oh, here comes the boss again. He has some questions.

**What's executing?**Er... sorry boss, it depends on what entities are active at the time. We don't really know.**In what order is it executing?**No idea. We add and remove entities to the list at random times during gameplay.**How can we parallelize this?**Gee boss, that's a tough one. Since the entities execute randomly, they may be accessing each other's state. If we split them up between threads, who knows what might happen.

In short:

![](../../assets/92a08f1eda91a9fa.gif)

But wait, there's more! If we look closely, we see the entities are stored in a linked list. Here's how that might look in memory:

![](../../assets/6ce70936914be702.png)

This makes our L1, L2, and L3 cache very sad. When we access the first item in the list, the cache thinks, "hey, I bet the next thing they'll want is nearby", and it pulls in the next 64 bytes after our initial memory access. But then we immediately jump to a completely different location in memory, and the cache has to wipe out those 64 bytes and pull in new data from RAM.

### Trick #4: line up data in memory for huge performance gains

Like this:

```
for (int i = 0; i < rigid_bodies.length; i++)
rigid_bodies[i].update();
for (int i = 0; i < ai_controllers.length; i++)
ai_controllers[i].update();
for (int i = 0; i < animated_models.length; i++)
animated_models[i].update();
// ...
```


An object-oriented programmer might be infuriated at this. It's not generic enough! But look, now we're iterating over a set of contiguous arrays (not arrays of pointers, mind you). Here's what it looks like in memory:

![](../../assets/95c40aee6daee21b.png)

Everything is all lined up in order. The cache is happy. As a side bonus, this version allows us to answer all those pesky questions the boss had. We know what's executing and in what order, and it looks much easier to parallelize.

*edit: Don't get too hung up on cache optimization. There's a lot more
to it than just throwing everything in an array. I only bring it up to
prove a point, and I'm only qualified to give the basic introduction.
Check out the links at the bottom for more info.*

Time to wrap this up and get to the point. What's the One Weird Trick? What do tricks 1-4 (and many more) all have in common?

### The One Weird Trick: data first, not code first

Why were globals so evil (trick #1)? Because they allowed us to get away with lazy data design.

Why did objects help us (trick #2)? Because they helped us organize our data better.

Why did components help us even more (trick #3)? Because they modeled our data better by matching the structure of reality better.

Even the CPU likes it when we organize our data correctly (trick #4).

### No really, what is the trick actually

Let's break it down in practical terms. Here's a representation of a typical Unity-like component-based game design.

![](../../assets/fdfc63094f08c28b.png)

Each component is an object. It has some state variables listed at the top, and then some methods to do stuff with those variables.

This is a well-designed object-oriented system, so the variables are private. The only code that can access them is the object's own methods. This is called "encapsulation".

![](../../assets/9b822b2f16bca453.png)

Each object has a certain amount of complexity. But fear not! OOP promises that as long as we keep the state private, that complexity will stay encapsulated within the object, and won't spread to the other objects.

Unfortunately, this is a lie.

![](../../assets/8cd0f122264cdff6.jpg)

Sometimes, we need a function to access two or three objects. We end up either splitting the function between those objects, or writing a bunch of getters and setters so our function can access what it needs. Neither solution is very satisfying.

Here is the truth. Some things cannot be represented as objects very well. I propose an alternate paradigm, one which represents every program perfectly:

![](../../assets/e8d1d3177233f04c.png)

Once we separate process from data, things start to make more sense.

Object-oriented helps us write good code because it encourages us to encapsulate complexity (i.e. state). But it forces us to do so in a certain way. Why not instead encapsulate like this, if it makes sense within our problem space?

![](../../assets/df27489b752c01af.png)

In summary, design data structures to match your specific problem. Don't shoehorn a single concept into a bunch of separate, encapsulated objects.

Next, write functions that leave the smallest possible footprint on that data. If possible, write pure stateless functions.

That's the trick.

### Conclusion

If this struck a chord with you, it's because I stole most of it. Get it straight from the source:

Thanks for reading! Please let me know your thoughts in the comments.