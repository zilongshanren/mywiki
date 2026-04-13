---
title: 'Nuevo en Firefox 77: Mejoras a las herramientas de desarrollo y a la plataforma
  web – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2020/06/nuevo-en-firefox-77/
author: Florian Scholz
published: '2020-06-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Tenemos ante nosotros una nueva versión estable de Firefox. La versión 77 viene con varias novedades para los desarrolladores web.

En este artículo se presenta simplemente un conjunto de los aspectos más destacados. Para conocer todos los detalles, consulte lo siguiente:

## Mejoras para las herramientas para desarrolladores

Comencemos por revisar las adiciones y mejoras más interesantes de las herramientas para desarrolladores de la versión 77. Si desea conocer más información del trabajo que se está realizando para darnos su opinión, puede descargar [Firefox Developer Edition](https://www.mozilla.org/firefox/developer/) para un acceso temprano a todo ello.

### Depuración de JavaScript más rápida y ágil

Las aplicaciones web de mayor tamaño pueden resultar todo un desafío para las herramientas de desarrollo, ya que deben gestionar los paquetes, la recarga en vivo y las dependencias de manera rápida y correcta. Con la versión 77, el depurador de Firefox ha aprendido algunos trucos más para poder centrarse en la depuración.

Después de mejorar el rendimiento de la depuración en muchas versiones, llegamos a quedarnos sin errores de alto impacto por corregir. Desde ese punto, para encontrar los últimos cuellos de botella que quedaban, hemos estado comunicándonos activamente con nuestra comunidad. Gracias a los muchos y detallados informes recibidos, pudimos alcanzar mejoras en el rendimiento que no solo aceleran las pausas y la ejecución por pasos, sino que también reducen el uso de memoria con el tiempo.

#### Mapas fuente JavaScript y CSS que funcionan como deben

Los mapas fuente han entrado dentro de este esfuerzo y han disfrutado de su propia parte del pastel en lo que a incrementos del rendimiento se refiere. En algunos casos, el tiempo de carga de mapas fuente en línea, se aceleró hasta 10 veces. Sin embargo, lo más importante es que hemos mejorado la fiabilidad para muchas más configuraciones de mapas fuente. Pudimos ajustar los valores de sustitución para el análisis y el mapeo gracias a sus informes sobre casos específicos de mapas fuente que se generaban de forma ligeramente incorrecta. En general, debería verse que algunos proyectos ahora, sencillamente, funcionan, mientras que antes no podían cargar el código original CSS y/o JavaScript/TypeScript/etc.

### Depurar JavaScript por pasos en el marco de pila seleccionado

Los pasos son una parte fundamental de la depuración, pero no resultan intuitivos. Es fácil perderse y dar pasos de más al entrar y salir de las funciones, o saltar entre las bibliotecas y el código propio.

Ahora, el depurador respetará la pila seleccionada actualmente al dar un paso. Esto resulta útil cuando se ha entrado en una llamada de función o al pausar en un método de biblioteca más abajo en la pila. Solo hay que seleccionar la función correcta en la pila de llamadas para saltar a la línea actualmente pausada y continuar desde allí.

Con esto esperamos que el paso por la ejecución del código sea más intuitivo, reduciendo la posibilidad de perderse una línea importante.

### Configuración de desbordamiento para la red y el depurador

Para crear una barra de herramientas más ágil, ahora los paneles de red y del depurador siguen el ejemplo de la consola, combinando casillas de verificación existentes y nuevas en un nuevo menú de ajustes. Esto pone potentes opciones al alcance de la mano, como “Desactivar JavaScript”, y deja espacio para otras opciones más en el futuro.

### Pausa en la lectura y escritura de propiedades

Comprender los cambios de estado es un problema que se suele investigar mediante los registros de consola durante la depuración. Los [watchpoints](https://wiki.developer.mozilla.org/en-US/docs/Tools/Debugger/How_to/Use_watchpoints), que aterrizaron junto con Firefox 72, pueden pausar la ejecución mientras un script lee o escribe una propiedad. Al pausar, se hace clic con el botón derecho en una propiedad en el panel Alcances para adjuntarlos.

La colaboradora [Janelle deMent](https://bugzilla.mozilla.org/user_profile?user_id=637866) simplificó el uso de los watchpoints con una nueva opción que combina get y set para que cualquier referencia al script active una pausa.

### Mejoras en la vista previa de los datos de red

Con cada nueva versión se han venido dando pasos para reorganizar los paneles de detalles de red. La antigua interfaz tenía errores a la hora de manejar eventos que provocaba que seleccionar y copiar texto resultara demasiado escabroso. Mientras estábamos en ello, también mejoramos el rendimiento para las entradas de datos de mayor tamaño.

Esto forma parte de una limpieza de interfaz mayor en el panel de red, la cual hemos estado preguntando a nuestra comunidad [a través de @FirefoxDevTools en Twitter](https://twitter.com/FirefoxDevTools) y [la comunidad Matrix de Mozilla](https://chat.mozilla.org/#/room/#devtools:mozilla.org). Únase a nosotros allí si quiere que se escuche su voz. Hay más aspectos del rediseño de la barra lateral del panel de red disponibles en [Firefox Developer Edition](https://www.mozilla.org/firefox/developer/) para un acceso temprano.

## Actualizaciones de la plataforma web

La plataforma web de Firefox 77 soporta unas cuantas características nuevas.

`String#replaceAll`


Firefox 67 presentó [ String#matchAll](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/matchAll), una forma más cómoda de iterar sobre coincidencias de resultados de

[expresiones regulares](https://en.wikipedia.org/wiki/Regular_expression). En Firefox 77 añadimos más comodidad:

[ayuda en el reemplazo de todas las ocurrencias de una cadena, una operación que, probablemente, sea una de esas cosas que ya ha buscado miles de veces en el pasado (¡gracias, StackOverflow, por ser tan útil!).](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/replaceAll)

`String#replaceAll`

Anteriormente, cuando había que reemplazar a todos los gatos con perros, hacía falta usar una expresión regular global

`.replace(/cats/g, 'dogs');`


`.split('cats').join('dogs');`


Ahora, gracias a [ String#replaceAll](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/replaceAll), esto resulta mucho más legible:

`.replaceAll('cats', 'dogs');`


### Solicitudes de cursor IndexedDB

Firefox 77 expone la solicitud de que un [IDBCursor](https://developer.mozilla.org/docs/Web/API/IDBCursor) se haya originado como un [atributo en ese cursor](https://developer.mozilla.org/docs/Web/API/IDBCursor/request). Se trata de una buena mejora que hace que sea más fácil escribir cosas como funciones de contenedor que “mejoran” las características de la base de datos. Anteriormente, para realizar una mejora tal en un cursor, había que pasar el objeto del cursor y el objeto de la solicitud desde el que se había originado, ya que el primero dependía del segundo. Con este cambio, ahora solo necesita pasar el objeto del cursor, ya que la solicitud está disponible en el mismo.

## Extensiones de Firefox 77: menos solicitudes de permisos y más

Desde Firefox 57, los usuarios ven los permisos a los que desea acceder una extensión durante la instalación o cuando se agregan nuevos permisos durante una actualización. La frecuencia de tales solicitudes puede resultar abrumadora, y el hecho de no aceptar una nueva solicitud de permiso durante la actualización de una extensión puede dejar a los usuarios varados en una versión anterior. Hacemos que sea más fácil para los desarrolladores de extensiones evitar la activación de tantas solicitudes aumentando los permisos disponibles como [ optional_permissions](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/optional_permissions). Los permisos opcionales no activan una solicitud de permiso durante la instalación o cuando se agregan a una actualización de extensión, y también se pueden

[solicitar en tiempo de ejecución](https://extensionworkshop.com/documentation/develop/request-the-right-permissions/?utm_source=blog.mozilla.org&utm_medium=blog&utm_campaign=hacks-fx-77#request-permissions-at-runtime)para que los usuarios vean qué permisos se solicitan en su contexto.

¡Visite el [blog de complementos](https://blog.mozilla.org/addons/) para conocer más actualizaciones a las extensiones en Firefox 77!

## Resumen

¡Esto es lo más destacado de Firefox 77! ¡Mira las nuevas funciones y diviértete probando! Como siempre, sientete libre de dar sus opiniones y formula tus preguntas en los comentarios.

## About
[
Florian Scholz ](https://developer.mozilla.org)

Florian is the Content Lead for MDN Web Docs, writes about Web platform technologies and researches browser compatibility data. He lives in Bremen, Germany.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.