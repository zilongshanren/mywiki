---
title: Making actors transparent when they block the Camera in Unreal Engine (See-through)
url: https://alfredbaudisch.com/unreal-engine/unreal-engine-actors-transparent-block-camera-occlusion-see-through/
author: Alfred Reinold Baudisch
published: '2022-05-13'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

I created a quick and simple solution in Unreal Engine to make actors and static meshes transparent (see-through) when the character is behind or occluded by them and when the camera has no collisions enabled, for example, for a top down camera.

There's no need to change the static meshes in the scene, and neither no need to change existing actors. The solution all happens with a single material that will serve as the see-through material (it can be any material you set) and a custom Player Controller that I wrote with C++, which I call **Occlusion Aware Player Controller**.

![](../../assets/d9afae79a95aae8b.gif)


The code detects actors with static meshes blocking the player field of view and then caches the list of materials contained in these meshes. Then, switches the meshes materials with the transparent material.

If the mesh is not obstructing the camera anymore, the Occlusion Aware Player Controller automatically switches the original materials back into the mesh.

A derived Player Controller from Occlusion Aware Player Controller either by C++ or Blueprint must call `SyncOccludedActors`

constantly (I set it with a timer in Blueprint, see the example below).

## Setup

### 1. Create a new C++ class that inherits from PlayerController

- Name it OcclusionAwarePlayerController, or whatever name you prefer.
- The source-code is at the bottom of this post and also on
[GitHub](https://gist.github.com/alfredbaudisch/7978f1913e76640e2dc25b770ffa6ae1).

### 2. Create the transparent/see-through material

In my case I created a simple Dot Product Fresnel, Translucent material.

![](../../assets/62618703fef5614f.png)


![](../../assets/62618703fef5614f.png)

### 3. Create a Blueprint Player Controller

The Blueprint Player Controller should inherit from the C++ class that you created on step 1.

Since it inherits from our custom Player Controller, the Blueprint now has a section called "Camera Occlusion", where you have to configure the material to be used (plus some other parameters from our custom C++ class):

![](../../assets/77f0cc368ba96f23.png)


![](../../assets/77f0cc368ba96f23.png)

### 4. Create a Timer By Event to Sync Occluded Actors

In the Player Controller Blueprint that you created previously (that inherits from OcclusionAwarePlayerController), call Set Timer by Event in the BeginPlay event and **call Sync Occluded Actors**.

## 5. Game Mode and Camera Collision

- Update your Game Mode to use the new Player Controller Blueprint
- Disable Do Collision Test in your camera Spring Arm.

## Coffee, Coins and Thumbs Up

If you like my content or if you learned something from it, [buy me a coffee](https://ko-fi.com/alfredbaudisch) ☕, [be my Patreon](https://www.patreon.com/alfredbaudisch) or simply check [all of my links](https://linktr.ee/alfredbaudisch) 🔗 and follow me/subscribe/star my repositories/whatever you prefer. If you want to learn Godot, be sure to check [my courses](https://alfredbaudisch.com/projects/education/dynamic-inventory-system-and-user-interfaces-with-godot-course/) 📚!

**Or you can simply add my game to your Steam Wishlist – that helps GREATLY and it's easy and free 🙂**

## Source-Code

If you prefer, the code is on a [GitHub Gist](https://gist.github.com/alfredbaudisch/7978f1913e76640e2dc25b770ffa6ae1) as well.

### Header

```
// OcclusionAwarePlayerController.h
// By Alfred Reinold Baudisch (https://github.com/alfredbaudisch)
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "OcclusionAwarePlayerController.generated.h"
USTRUCT(BlueprintType)
struct FCameraOccludedActor
{
GENERATED_USTRUCT_BODY()
UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
const AActor* Actor;
UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
UStaticMeshComponent* StaticMesh;
UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
TArray<UMaterialInterface*> Materials;
UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
bool IsOccluded;
};
/**
*
*/
UCLASS()
class DACHSHUNDSPA_API AOcclusionAwarePlayerController : public APlayerController
{
GENERATED_BODY()
public:
AOcclusionAwarePlayerController();
protected:
// Called when the game starts
virtual void BeginPlay() override;
/** How much of the Pawn capsule Radius and Height
* should be used for the Line Trace before considering an Actor occluded?
* Values too low may make the camera clip through walls.
*/
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Camera Occlusion|Occlusion",
meta=(ClampMin="0.1", ClampMax="10.0") )
float CapsulePercentageForTrace;
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Camera Occlusion|Materials")
UMaterialInterface* FadeMaterial;
UPROPERTY(BlueprintReadWrite, Category="Camera Occlusion|Components")
class USpringArmComponent* ActiveSpringArm;
UPROPERTY(BlueprintReadWrite, Category="Camera Occlusion|Components")
class UCameraComponent* ActiveCamera;
UPROPERTY(BlueprintReadWrite, Category="Camera Occlusion|Components")
class UCapsuleComponent* ActiveCapsuleComponent;
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Camera Occlusion")
bool IsOcclusionEnabled;
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Camera Occlusion|Occlusion")
bool DebugLineTraces;
private:
TMap<const AActor*, FCameraOccludedActor> OccludedActors;
bool HideOccludedActor(const AActor* Actor);
bool OnHideOccludedActor(const FCameraOccludedActor& OccludedActor) const;
void ShowOccludedActor(FCameraOccludedActor& OccludedActor);
bool OnShowOccludedActor(const FCameraOccludedActor& OccludedActor) const;
void ForceShowOccludedActors();
__forceinline bool ShouldCheckCameraOcclusion() const
{
return IsOcclusionEnabled && FadeMaterial && ActiveCamera && ActiveCapsuleComponent;
}
public:
UFUNCTION(BlueprintCallable)
void SyncOccludedActors();
};
```


### Implementation

```
// OcclusionAwarePlayerController.cpp
// By Alfred Reinold Baudisch (https://github.com/alfredbaudisch)
#include "OcclusionAwarePlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Containers/Set.h"
AOcclusionAwarePlayerController::AOcclusionAwarePlayerController()
{
CapsulePercentageForTrace = 1.0f;
DebugLineTraces = true;
IsOcclusionEnabled = true;
}
void AOcclusionAwarePlayerController::BeginPlay()
{
Super::BeginPlay();
if (IsValid(GetPawn()))
{
ActiveSpringArm = Cast<
USpringArmComponent>(GetPawn()->GetComponentByClass(USpringArmComponent::StaticClass()));
ActiveCamera = Cast<UCameraComponent>(GetPawn()->GetComponentByClass(UCameraComponent::StaticClass()));
ActiveCapsuleComponent = Cast<UCapsuleComponent>(
GetPawn()->GetComponentByClass(UCapsuleComponent::StaticClass()));
}
}
void AOcclusionAwarePlayerController::SyncOccludedActors()
{
if (!ShouldCheckCameraOcclusion()) return;
// Camera is currently colliding, show all current occluded actors
// and do not perform further occlusion
if (ActiveSpringArm->bDoCollisionTest)
{
ForceShowOccludedActors();
return;
}
FVector Start = ActiveCamera->GetComponentLocation();
FVector End = GetPawn()->GetActorLocation();
TArray<TEnumAsByte<EObjectTypeQuery>> CollisionObjectTypes;
CollisionObjectTypes.Add(UEngineTypes::ConvertToObjectType(ECC_WorldStatic));
TArray<AActor*> ActorsToIgnore; // TODO: Add configuration to ignore actor types
TArray<FHitResult> OutHits;
auto ShouldDebug = DebugLineTraces ? EDrawDebugTrace::ForDuration : EDrawDebugTrace::None;
bool bGotHits = UKismetSystemLibrary::CapsuleTraceMultiForObjects(
GetWorld(), Start, End, ActiveCapsuleComponent->GetScaledCapsuleRadius() * CapsulePercentageForTrace,
ActiveCapsuleComponent->GetScaledCapsuleHalfHeight() * CapsulePercentageForTrace, CollisionObjectTypes, true,
ActorsToIgnore,
ShouldDebug,
OutHits, true);
if (bGotHits)
{
// The list of actors hit by the line trace, that means that they are occluded from view
TSet<const AActor*> ActorsJustOccluded;
// Hide actors that are occluded by the camera
for (FHitResult Hit : OutHits)
{
const AActor* HitActor = Cast<AActor>(Hit.Actor);
HideOccludedActor(HitActor);
ActorsJustOccluded.Add(HitActor);
}
// Show actors that are currently hidden but that are not occluded by the camera anymore
for (auto& Elem : OccludedActors)
{
if (!ActorsJustOccluded.Contains(Elem.Value.Actor) && Elem.Value.IsOccluded)
{
ShowOccludedActor(Elem.Value);
if (DebugLineTraces)
{
UE_LOG(LogTemp, Warning,
TEXT("Actor %s was occluded, but it's not occluded anymore with the new hits."), *Elem.Value.Actor->GetName());
}
}
}
}
else
{
ForceShowOccludedActors();
}
}
bool AOcclusionAwarePlayerController::HideOccludedActor(const AActor* Actor)
{
FCameraOccludedActor* ExistingOccludedActor = OccludedActors.Find(Actor);
if (ExistingOccludedActor && ExistingOccludedActor->IsOccluded)
{
if (DebugLineTraces) UE_LOG(LogTemp, Warning, TEXT("Actor %s was already occluded. Ignoring."),
*Actor->GetName());
return false;
}
if (ExistingOccludedActor && IsValid(ExistingOccludedActor->Actor))
{
ExistingOccludedActor->IsOccluded = true;
OnHideOccludedActor(*ExistingOccludedActor);
if (DebugLineTraces) UE_LOG(LogTemp, Warning, TEXT("Actor %s exists, but was not occluded. Occluding it now."), *Actor->GetName());
}
else
{
UStaticMeshComponent* StaticMesh = Cast<UStaticMeshComponent>(
Actor->GetComponentByClass(UStaticMeshComponent::StaticClass()));
FCameraOccludedActor OccludedActor;
OccludedActor.Actor = Actor;
OccludedActor.StaticMesh = StaticMesh;
OccludedActor.Materials = StaticMesh->GetMaterials();
OccludedActor.IsOccluded = true;
OccludedActors.Add(Actor, OccludedActor);
OnHideOccludedActor(OccludedActor);
if (DebugLineTraces) UE_LOG(LogTemp, Warning, TEXT("Actor %s does not exist, creating and occluding it now."), *Actor->GetName());
}
return true;
}
void AOcclusionAwarePlayerController::ForceShowOccludedActors()
{
for (auto& Elem : OccludedActors)
{
if (Elem.Value.IsOccluded)
{
ShowOccludedActor(Elem.Value);
if (DebugLineTraces) UE_LOG(LogTemp, Warning, TEXT("Actor %s was occluded, force to show again."), *Elem.Value.Actor->GetName());
}
}
}
void AOcclusionAwarePlayerController::ShowOccludedActor(FCameraOccludedActor& OccludedActor)
{
if (!IsValid(OccludedActor.Actor))
{
OccludedActors.Remove(OccludedActor.Actor);
}
OccludedActor.IsOccluded = false;
OnShowOccludedActor(OccludedActor);
}
bool AOcclusionAwarePlayerController::OnShowOccludedActor(const FCameraOccludedActor& OccludedActor) const
{
for (int matIdx = 0; matIdx < OccludedActor.Materials.Num(); ++matIdx)
{
OccludedActor.StaticMesh->SetMaterial(matIdx, OccludedActor.Materials[matIdx]);
}
return true;
}
bool AOcclusionAwarePlayerController::OnHideOccludedActor(const FCameraOccludedActor& OccludedActor) const
{
for (int i = 0; i < OccludedActor.StaticMesh->GetNumMaterials(); ++i)
{
OccludedActor.StaticMesh->SetMaterial(i, FadeMaterial);
}
return true;
}
```