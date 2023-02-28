# -*- coding: utf-8 -*-
# version 2022 14 mars - jmd
from __future__ import annotations

import random
import ast
from id import *
from helper import Helper as hlp


from modeles import Ressource


class Astre():
    def __init__(self, parent: Modele, x: int, y: int, taille: int):
        self.id: int = get_prochain_id()
        self.parent = parent
        self.x = x
        self.y = y
        self.taille = taille


class PorteDeVers(Astre):
    def __init__(self, parent, x: int, y: int, couleur: str, taille: str):
        super().__init__(parent, x, y, taille)
        self.pulse = random.randrange(taille)
        self.couleur = couleur

    def jouer_prochain_coup(self) -> None:
        self.pulse += 1
        if self.pulse >= self.taille:
            self.pulse = 0


class TrouDeVers():
    def __init__(self, x1, y1, x2, y2):
        self.id = get_prochain_id()

        taille = random.randrange(6, 20)

        self.portes = (
            PorteDeVers(self, x1, y1, "red", taille),
            PorteDeVers(self, x2, y2, "orange", taille)
        )

        # pour mettre les vaisseaux qui ne sont plus dans l'espace
        # mais maintenant l'hyper-espace
        self.liste_transit = []

    def jouer_prochain_coup(self) -> None:
        for porte in self.portes:
            porte.jouer_prochain_coup()


class Etoile(Astre):
    def __init__(self, parent: Modele, x: int, y: int):
        super().__init__(parent, x, y, random.randrange(4, 8))
        self.proprietaire: str = ""
        self.ressources: Ressource = Ressource(
            random.randint(100, 500),
            random.randint(100, 500),
            random.randint(100, 500)
        ) * self.taille


class Nuage(Astre):
    def __init__(self, parent: Modele, x: int, y: int):
        super().__init__(parent, x, y, random.randint(20, 30))
        self.couleur = "green"


class Vaisseau():
    def __init__(self, parent: Joueur, nom: str, x: int, y: int,
                 energie: int = 100, taille: int = 5, vitesse: int = 2):
        self.parent = parent
        self.id: int = get_prochain_id()
        self.proprietaire = nom
        self.x = x
        self.y = y
        self.energie = energie
        self.taille: int = taille
        self.vitesse: int = vitesse
        self.cible: int = 0
        self.type_cible: str = None
        self.angle_cible: float = 0
        self.arriver: dict[str, callable] = {
            "Etoile": self.arriver_etoile,
            "PorteDeVers": self.arriver_porte
        }

    def jouer_prochain_coup(self, trouver_nouveau=0) -> None:
        if self.cible != 0:
            return self.avancer()
        elif trouver_nouveau:
            cible = random.choice(self.parent.parent.etoiles)
            self.acquerir_cible(cible, "Etoile")

    def acquerir_cible(self, cible, type_cible) -> None:
        self.type_cible = type_cible
        self.cible = cible
        self.angle_cible = hlp.calcAngle(
            self.x, self.y, self.cible.x, self.cible.y)

    def avancer(self) -> list:
        if self.cible != 0:
            x = self.cible.x
            y = self.cible.y
            self.x, self.y = hlp.getAngledPoint(
                self.angle_cible, self.vitesse, self.x, self.y)
            if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                type_obj = type(self.cible).__name__
                rep = self.arriver[type_obj]()
                return rep

    def arriver_etoile(self) -> list[str, int]:
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant,
             "Etoile", self.id, self.cible.id, self.cible.proprietaire]
        )
        if not self.cible.proprietaire:
            self.cible.proprietaire = self.proprietaire
        cible = self.cible
        self.cible = 0
        return ["Etoile", cible]

    def arriver_porte(self) -> list[str, int]:
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant,
             "Porte", self.id, self.cible.id, ]
        )
        cible = self.cible
        trou: TrouDeVers = cible.parent
        if cible == trou.portes[0]:
            self.x = trou.portes[1].x + random.randrange(6) + 2
            self.y = trou.portes[1].y
        elif cible == trou.portes[1]:
            self.x = trou.portes[0].x - random.randrange(6) + 2
            self.y = trou.portes[0].y
        self.cible = 0
        return ["Porte_de_ver", cible]


class Cargo(Vaisseau):
    def __init__(self, parent: Joueur, nom: str, x: int, y: int):
        super().__init__(parent, nom, x, y, 500, 6, 1)
        self.espace = 1000


class Joueur():
    def __init__(self, parent: Modele, nom: str,
                 etoilemere: Etoile, couleur: str):
        self.id: int = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.etoilemere = etoilemere
        self.etoilemere.proprietaire = nom
        self.couleur = couleur
        self.log = []
        self.etoilescontrolees: list[Etoile] = [self.etoilemere]
        self.flotte: dict[str, dict[int, callable]] = {
            "Vaisseau": {},
            "Cargo": {},
            "Starfighter": {}
        }

        self.actions: list[str, callable] = {
            "creervaisseau": self.creervaisseau,
            "ciblerflotte": self.ciblerflotte
        }

    def creervaisseau(self, params: list[str, int]) -> Vaisseau:
        """Crée un des trois types de vaisseaux disponible
        sur la planète dont il y a une création

        Args:
            params (list[str, int]): le type de vaisseau et le id

        Returns:
            Vaisseau: vaisseau créé
        """
        type_vaisseau: str = params[0]
        etoile = self.parent.cible
        # TODO: changer les paramètres de self.etoilemere et peut-être dict?
        if type_vaisseau == "Cargo":
            v = Cargo(self, self.nom, self.etoilemere.x +
                      10, self.etoilemere.y)
        else:
            v = Vaisseau(self, self.nom, self.etoilemere.x +
                         10, self.etoilemere.y)
        self.flotte[type_vaisseau][v.id] = v

        if self.nom == self.parent.parent.mon_nom:
            self.parent.parent.lister_objet(type_vaisseau, v.id)
        return v

    def ciblerflotte(self, ids):
        idori, iddesti, type_cible = ids
        ori = None
        for i in self.flotte.keys():
            if idori in self.flotte[i]:
                ori = self.flotte[i][idori]

        if ori:
            if type_cible == "Etoile":
                for j in self.parent.etoiles:
                    if j.id == iddesti:
                        ori.acquerir_cible(j, type_cible)
                        return
            elif type_cible == "Porte_de_ver":
                cible = None
                for j in self.parent.trou_de_vers:
                    if j.portes[0].id == iddesti:
                        cible = j.portes[0]
                    elif j.portes[1].id == iddesti:
                        cible = j.portes[1]
                    if cible:
                        ori.acquerir_cible(cible, type_cible)
                        return

    def jouer_prochain_coup(self):
        self.avancer_flotte()

    def avancer_flotte(self, chercher_nouveau=0):
        for i in self.flotte:
            for j in self.flotte[i]:
                j = self.flotte[i][j]
                rep = j.jouer_prochain_coup(chercher_nouveau)
                if rep:
                    if rep[0] == "Etoile":
                        # ? est-ce qu'on doit retirer l'etoile de
                        # ? la liste du modele
                        # ? quand on l'attribue aux etoilescontrolees
                        # ? et que ce passe-t-il si l'etoile a un proprietaire

                        self.etoilescontrolees.append(rep[1])
                        self.parent.parent.afficher_etoile(self.nom, rep[1])
                    elif rep[0] == "Porte_de_ver":
                        pass


# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self, parent, nom, etoilemere, couleur):
        Joueur.__init__(self, parent, nom, etoilemere, couleur)
        self.cooldownmax = 1000
        self.cooldown = 20

    def jouer_prochain_coup(self):
        # for i in self.flotte:
        #     for j in self.flotte[i]:
        #         j=self.flotte[i][j]
        #         rep=j.jouer_prochain_coup(1)
        #         if rep:
        #             self.etoilescontrolees.append(rep[1])
        self.avancer_flotte(1)

        if self.cooldown == 0:
            v = self.creervaisseau(["Vaisseau"])
            cible = random.choice(self.parent.etoiles)
            v.acquerir_cible(cible, "Etoile")
            self.cooldown = random.randrange(
                self.cooldownmax) + self.cooldownmax
        else:
            self.cooldown -= 1


class Modele():
    bordure: int = 10
    couleurs: list[str] = ["red", "blue", "lightgreen", "yellow",
                           "lightblue", "pink", "gold", "purple"]
    couleursia: list[str] = ["orange", "green", "cyan",
                             "SeaGreen1", "turquoise1", "firebrick1"]

    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur: int = 9000
        self.hauteur: int = 9000
        self.nb_etoiles: int = int((self.hauteur * self.largeur) / 500000)
        self.joueurs = {}
        self.actions_a_faire = {}
        self.etoiles: list[Etoile] = []
        self.nuages: list[Nuage] = []
        self.trou_de_vers: list[TrouDeVers] = []
        self.cadre_courant = None
        self.creeretoiles(joueurs, 1)
        self.creer_nuages()
        nb_trous: int = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trous)

    def _get_rand_pos(self) -> tuple(int, int):
        """Retourne une position cartésienne aléatoire.

        Returns
        -------
        tuple(int, int)
            Position cartésienne aléatoire
        """
        return (
            random.randrange(self.largeur - (2 * Modele.bordure))
            + Modele.bordure,
            (random.randrange(self.hauteur - (2 * Modele.bordure))
             + Modele.bordure))

    def creer_troudevers(self, n):
        for i in range(n):
            x1, y1 = self._get_rand_pos()
            x2, y2 = self._get_rand_pos()
            self.trou_de_vers.append(TrouDeVers(x1, y1, x2, y2))

    def creer_nuages(self):
        for i in range(100):
            for j in range(len(self.etoiles)):
                x, y = self._get_rand_pos()
                if x == self.etoiles[j].x and y == self.etoiles[j].y:
                    j = 0
            self.nuages.append(Nuage(self, x, y))

    def creeretoiles(self, joueurs, ias=0):
        for i in range(self.nb_etoiles):
            x, y = self._get_rand_pos()
            self.etoiles.append(Etoile(self, x, y))

        nb_joueurs_total: int = len(joueurs) + ias
        etoiles_occupees: list[Etoile] = []

        while nb_joueurs_total:
            p = random.choice(self.etoiles)
            self.etoiles.remove(p)
            etoiles_occupees.append(p)
            nb_joueurs_total -= 1
                  
        for i in joueurs:
            etoile: Etoile = etoiles_occupees.pop(0)
            self.joueurs[i] = Joueur(self, i, etoile, Modele.couleurs.pop(0))

            dist = 500
            x = random.randrange(x - dist, etoile.x + dist)
            y = random.randrange(y - dist, etoile.y + dist)
            self.etoiles.append(Etoile(self, x, y))

        # IA- creation des ias
        for i in range(ias):
            self.joueurs["IA_" + str(i)] = IA(
                self, "IA_" +
                str(i), etoiles_occupees.pop(0),
                Modele.couleursia.pop(0)
            )

    def jouer_prochain_coup(self, cadre):
        #  NE PAS TOUCHER LES LIGNES SUIVANTES  ################
        self.cadre_courant = cadre
        # insertion de la prochaine action demandée par le joueur
        if cadre in self.actions_a_faire:
            for i in self.actions_a_faire[cadre]:
                self.joueurs[i[0]].actions[i[1]](i[2])
                """
                i a la forme suivante [nomjoueur, action, [arguments]
                alors self.joueurs[i[0]] -> trouve l'objet représentant
                le joueur de ce nom
                """
            del self.actions_a_faire[cadre]
        # FIN DE L'INTERDICTION #################################

        # demander aux objets de jouer leur prochain coup
        # aux joueurs en premier
        for i in self.joueurs:
            self.joueurs[i].jouer_prochain_coup()

        # NOTE si le modele (qui représente l'univers !!! )
        #      fait des actions - on les activera ici...
        for i in self.trou_de_vers:
            i.jouer_prochain_coup()

    def creer_bibittes_spatiales(self, nb_bibittes=0):
        pass

    ##########################################################################
    # ATTENTION : NE PAS TOUCHER
    def ajouter_actions_a_faire(self, actionsrecues):
        cadrecle = None
        for i in actionsrecues:
            cadrecle = i[0]
            if cadrecle:
                if (self.parent.cadrejeu - 1) > int(cadrecle):
                    print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                action = ast.literal_eval(i[1])

                if cadrecle not in self.actions_a_faire.keys():
                    self.actions_a_faire[cadrecle] = action
                else:
                    self.actions_a_faire[cadrecle].append(action)
    # NE PAS TOUCHER - FIN
##############################################################################
