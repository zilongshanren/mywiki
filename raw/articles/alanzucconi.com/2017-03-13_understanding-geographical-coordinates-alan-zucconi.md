---
title: Understanding Geographical Coordinates - Alan Zucconi
url: https://www.alanzucconi.com/2017/03/13/understanding-geographical-coordinates/
author: Alan Zucconi
published: '2017-03-13'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This series introduces the concept of **trilateration**. This technique can be applied to a wide range of problems, from *indoor localisation* to *earthquake detection*. This first post provides a general introduction to the concept of geographical coordinates, and how they can be effectively manipulated. The second post in the series, [Positioning and Trilateration](https://www.alanzucconi.com/2017/03/13/localisation-and-trilateration/), will cover the actual techniques used to identify the position of an object given independent distance readings. Most trilateration tutorials require the measures from the sensors to be precise and consistent. The approach here presented, instead, is highly robust and can tolerate inaccurate readings.

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[Understanding Geographical Coordinates](https://www.alanzucconi.com#part1) - Part 2.
[Local Geographical Distance](https://www.alanzucconi.com#part2) - Part 3.
[Great-Circle Distance](https://www.alanzucconi.com#part3) [Conclusion](https://www.alanzucconi.com#conclusion)

There is a basic fact that permeates Engineering: sensors are imprecise. Whether you are using a temperature sensor or a camera, your measures will always have a finite accuracy. A simple way to overcome this limitation is to average out multiple readings from the same sensor. This often allows to cancel out the noise that is poisoning your readings.

If multiple sensors are available for you to use, it is often possible to merge their readings not just to refine your measurements, but to discover entirely new pieces of information. **Sensor fusion** ([Wikipedia](https://en.wikipedia.org/wiki/Sensor_fusion)) is the umbrella term that is generally used to describe this family of techniques. They find many practical applications: **GPS,** **earthquake detection**, and **indoor positioning **are just few of them.

If you are unfamiliar with the concept, GPS ([Global Positioning System](https://en.wikipedia.org/wiki/Global_Positioning_System)) is a technology that allows to localise a device on the surface of the planet. It relies on a network of intercommunicating satellites, which are orbiting the planet. When your device establishes a connection with a satellite, the latter is unable to calculate your position. In a nutshell, the only information that each satellite knows is your distance. No single satellite knows your position. However, merging the data from multiple satellites allows to identify your exact location.

If we want to locate an object on the surface of the planet, we first have to understand how** geographical coordinates** work. Throughout history there have been many attempts to solve the insidious problem of mapping Earth. The most common solution nowadays assigns three coordinates to each point on the surface of Earth: *latitude*, *longitude* and *altitude* (namely, ![Rendered by QuickLaTeX.com \phi](../../assets/5894f23fcbaa6c26.png)

![Rendered by QuickLaTeX.com \lambda](../../assets/e4664a784ffb986a.png)

![Rendered by QuickLaTeX.com h](../../assets/5b0f1268bf785a2d.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)


![](../../assets/85b74ff9f046fc5c.png)

To measure latitude, the following conventions hold:

- The equator has latitude

; - The North pole has latitude

; - The South pole has latitude

.

Loosely speaking, latitude contributes to the ![Rendered by QuickLaTeX.com y](../../assets/6cc181d8f36d0fd4.png)

*vertical*) component of a map. Conversely, longitude measures the ![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)

*horizontal*) component. The imaginary line that connects the poles and passes through Greenwich is called the **prime meridian**:

- The prime meridian has longitude

; - Moving East increases

, up to the antipodal prime meridian which has longitude

; - Moving West decreases

, up to the antipodal prime meridian which has longitude

.

Both ![Rendered by QuickLaTeX.com \lambda=180^{\circ}](../../assets/6b136218654d31dd.png)

![Rendered by QuickLaTeX.com \lambda=-180^{\circ}](../../assets/e85511e65de91be0.png)


On a small scale, Earth can be assumed to be locally flat. When you measure distances within a small city, for instance, you do not need to take into account the curvature of the planet. Let’s assume you want to calculate the geographical distance ![Rendered by QuickLaTeX.com D](../../assets/81012a1469029eac.png)

![Rendered by QuickLaTeX.com P=\left(\phi_1, \lambda_1\right)](../../assets/472d7883c916c0b2.png)

![Rendered by QuickLaTeX.com Q=\left(\phi_2, \lambda_2\right)](../../assets/84e570b9bce4b48c.png)


![Rendered by QuickLaTeX.com \[D=R \cdot \sqrt{{\Delta \phi}^2 + \left(\cos\phi_m\Delta \lambda\right)^2 }\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-857357646ca96a04e4046ca5b20b77ce_l3.png)


where:


is the radius of the Earth;

;

;

.

For this equation to work, all quantities must be expressed in *radians*, rather than degrees.

def geographical_distance (latitudeA, longitudeA, latitudeB, longitudeB): # Degrees to radians delta_latitude = math.radians(latitudeB - latitudeA) delta_longitude = math.radians(longitudeB - longitudeA) mean_latitude = math.radians((latitudeA + latitudeB) / 2.0 ) R = 6371.009 # Km # Spherical Earth projected to a plane return \ R * math.sqrt \ ( math.pow ( delta_latitude, 2 ) + math.pow ( math.cos(mean_latitude) * delta_longitude, 2 ) )

#### Great-Circle Distance

The Euclidean distance provides a good approximation for the distance between two geographical points only when they are relatively close. For larger distances, one has to take into account the curvature of the planet.

If you imagine Earth as a perfect sphere, the distance between two points is the length of a the shortest piece of strings that connects them. That string will naturally follow the curvature of the sphere, much like the distance we have to calculate. This concept is known as **great-circle distance**, and is explained in detail on this [Wikipedia article](https://en.wikipedia.org/wiki/Great-circle_distance).

![](../../assets/1e14c85d371de810.png)

Mathematically speaking, the shortest distance between two points on a sphere can be calculated using the** spherical law of cosines** ([Wikipedia](https://en.wikipedia.org/wiki/Spherical_law_of_cosines)):

![Rendered by QuickLaTeX.com \[D = R \Delta \sigma\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5b1c23d9af4f5b01bc82306455e28f92_l3.png)


where ![Rendered by QuickLaTeX.com \Delta \sigma](../../assets/55a8239608c8994b.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com Q](../../assets/3ebcaf72a3239e06.png)

**central angle**:

![Rendered by QuickLaTeX.com \[\Delta \sigma = \arccos\left(\sin\phi_1 \cdot \sin\phi_2 + \cos\phi_1 \cdot \cos \phi_2 \cdot \cos \Delta \lambda\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-57425657b947090cdaba93b010daf3d7_l3.png)


![](../../assets/5a576ef39e9125d1.png)

While the above mentioned equation is mathematically correct, it is also *numerically unstable*. This means that rounding errors can have a negative effect on the precision of the final result. A more accurate formula what works well with floating point arithmetic is:

![Rendered by QuickLaTeX.com \[\Delta \sigma = \arctan\frac{\sqrt{\left(\cos \phi_2 \cdot \sin\Delta\lambda\right)^2+\left(\cos \phi_1 \cdot \sin \phi_2 -\sin \phi_1 \cdot \cos\phi_2 \cdot \cos \Delta\lambda\right) ^2}}{\sin \phi_1 \cdot \sin \phi_2 + \cos\phi_1 \cdot \cos\phi_2 \cdot \cos\Delta\lambda}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7b3658c03bdaa93a212d4740467e360e_l3.png)


This translates into the following Python code:

def great_circle_distance (latitudeA, longitudeA, latitudeB, longitudeB): # Degrees to radians phi1 = math.radians(latitudeA) lambda1 = math.radians(longitudeA) phi2 = math.radians(latitudeB) lambda2 = math.radians(longitudeB) delta_lambda = math.fabs(lambda2 - lambda1) central_angle = \ math.atan2 \ ( # Numerator math.sqrt ( # First math.pow ( math.cos(phi2) * math.sin(delta_lambda) , 2.0 ) + # Second math.pow ( math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda) , 2.0 ) ), # Denominator ( math.sin (phi1) * math.sin(phi2) + math.cos (phi1) * math.cos(phi2) * math.cos(delta_lambda) ) ) R = 6371.009 # Km return R * central_angle

The function `math.atan2`

is used to calculate the correct sign of ![Rendered by QuickLaTeX.com \Delta\sigma](../../assets/bbc3ea9d5c7aa888.png)


### 📚 Recommended Books

This post introduced the concept of geographical coordinates, and the challenges that arise when trying to manipulate them. The next post will show how it is possible to use multiple distance readings to correctly locate objects.

**Part 1. Understanding Geographical Coordinates**- Part 2.
[Positioning and Trilateration](https://www.alanzucconi.com/2017/03/13/positioning-and-trilateration/)

## Leave a Reply Cancel reply