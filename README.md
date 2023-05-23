# ORION-C41-Groupe1

## But du jeu:
Chaque joueur commence avec une planète mère, cette planète à des ressources exploitables générés de facon aléatoire: Roche, Metal et Energie. Ces ressources servent à construire des batiments dans une planète. Le premier qui construit _"l'accelerateur de particule"_ gagne la partie.

## Comment jouer

En debut de partie et sur chaque nouvelle planete conquise, la premiere mine et la premiere centrale sont gratuite pour permettre au joueur de commencer a recuperer des ressources. 
Apres cela, le but est de construire une usine afin de pouvoir commencer a explorer l'univers grace au vaisseaux qu'elle permet de construire. Il faut ensuite conquerir le plus de planete afin de se developper rapidement et de devenir le premier joueur a avoir un accelerateur de particules.

## Déroulement du jeu
Quand on click sur la planète mère, un boutton construction apparait. Lorsque ce boutton est appuyé, un menu apparait a droite de l'interface et affiche les batiments qui sont disponible a construire.

<img src=Images/constructionPNG.PNG alt="Boutton construction">
<img src=Images/menu_construction.PNG alt="Menu construction">

Quand on click sur un des bouttons dans le menu a droite, un batiment est alors construit (On assume que l'utilisateur a assez de ressource, si il n'a pas assez de ressource le batiment n'est pas construit). Quand un batiment est construit, une notification en haut a gauche confirme que le batiment à été construit: 

<img src=Images/notification.PNG alt="Notification">

### Batiments
- Mine
- Centrale 
- Usine
- Canon
- AccelerateurParticule

Les mines sont responsable de l'extraction de Roche et de Metal d'une planete. Une fois une ressource extraite, elle est donné au joueur et enlevé de la planete.

Les centrales sont responasable de l'extraction de l'energie d'une planete. Une fois une ressource extraite, elle est donné au joueur et enlevé de la planete.

Les usines sont responsable de la construction de vaisseau (Cargo, Explorer et Combat). La construction de batiments sur d'autres planetes, autre que la planete mère est uniquement disponible avec le cargo.

Les canons permettent aux planetes de gagner des points de défenses, ces points servent a determiner lors d'une attaque si la planete est en mesure de se defendre ou se fait capturer (le plus grand nombre de point l'emporte). 

L'accelerateur de particule est le dernier batiment possible de construire, il represente la finalite du developpement de la civilisation du joueur. Le premier joueur a construire ce batiment remporte la partie. 

