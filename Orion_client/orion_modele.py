# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd
from __future__ import annotations
from msilib.schema import Class
import random
import ast
from random import choice, randint
import time
from collections import defaultdict

from id import *
from helper import Helper as hlp
from threading import Timer

from ressource import Ressource

class Artefact:
    """Liste de noms de bonus qu'un artéfact peut avoir"""
    noms = ['mine', 'ressource'] 
    
    def __init__(self):
        self.nom = 'Artefact ' + choice(Artefact.noms)
    
    def activate_bonus(self, etoile: Etoile, joueur: Joueur) -> None:
        liste_bonus = {
            'mine': Mine(etoile, joueur),
            'ressource': Ressource(randint(10, 1000), randint(10, 1000), 
                                   randint(10, 1000))
        }
        
        nom, bonus = self.nom[9:], self._get_bonus(liste_bonus)
        
        if nom == 'ressource':
            if randint(0, 10) <= 1:
                for k, v in etoile.ressources.values():
                    v += liste_bonus[nom][k]
                joueur.ressources += liste_bonus[nom]
            else:
                k, v = choice(list(etoile.ressources.items()))
                nb_res = liste_bonus[nom][k]
                v += nb_res
                print(f'Vous avez gagné {nb_res} {k}s')
                joueur.ressources[k] += nb_res
        else:
            etoile.batiments[nom][bonus.id] = bonus
            print(f'Vous avez gagné une nouvelle {liste_bonus[nom].__class__.__name__}')
            

    def _get_bonus(self, liste_bonus: dict) -> tuple[str, Mine | Ressource]:
        return liste_bonus.get(self.nom[9:])

class Batiment():
    """
    Classe batiment --> classe parent pour les batiments d'une planete. 
    
    Parameters
    ----------
    id : int
        ID d'un batiment. Generation d'ID avec la methode 'get_prochain_id()'
    planete : objet planete
        Sert a identifier dans quel planete le batiment est construit
        
    pdv : int
        Point de vie d'un batiment. Sert lorsque la planete ce fait attaquer.
        
    niveau : int
        Niveau d'un batiment.
        
    proprietaire : objet Joueur
        Proprietaire du batiment.
        
    id_batiment : int
        Sert a identifier le type de batiment
        
    """

    def __init__(self, planete, proprietaire):
        self.id = get_prochain_id()
        self.proprietaire = proprietaire
        self.planete = planete
        self.niveau = 1

class Extraction(Batiment):
    """
    Classe Extraction --> classe qui sert de parent aux classe Centrale, MineMetal et MinePierre
    
    Parameters
    ----------
    ressource_max : int
        ...
        
    taux_extraction : int
        Quantité de ressoure generé par seconde
    
    Args:
    ----------
        Batiment: Child de la classe Parent Batiment
    """

    def __init__(self, planete, proprietaire):
        super().__init__(planete, proprietaire)

        self.ressources = Ressource()

        self.ressources_max = Ressource()

    def generer(self,planete, bat):
        taux = self.niveau * 0.1
        if bat == 'centrale' :
            if planete.ressources["energie"] > 0:
                self.ressources["energie"] += taux / 2
                planete.ressources["energie"] -= taux / 2
        elif bat == "mine":
            if planete.ressources["pierre"] > 0:
                self.ressources["pierre"] += taux / 2
                planete.ressources["pierre"] -= taux / 2
            if planete.ressources["metal"] > 0:
                self.ressources["metal"] += taux / 2
                planete.ressources["metal"] -= taux / 2


    def recolte(self):
        """
        Cette methode s'occupe de recolter les ressources produite
        dans la Centrale et les transferer au joueur proprietaire
        Args:
            proprietaire (Objet Joueur): Sert à savoir à qui appartient le batiment et ainsi pouvoir transferer les ressources au joueur
        """
        p = Ressource();
        p += self.ressources
        self.ressources = {
            "energie": 0,
            "pierre": 0,
            "metal": 0
        }

        return p


class Centrale(Extraction):
    """
    Classe Centrale --> Classe du batiment Centrale. S'occupe de generer ressource 'energie'
    
    Parameters
    ----------
    nb.energie : int
        Nombre d'energie produite et stocké dans le batiment Centrale
    Args:
    ----------
        Extraction : Child de la classe Extraction
    """

    def __init__(self, planete, proprietaire):
        super().__init__(planete, proprietaire)

    def upgrade(self, ressources):
        cost = (100 * pow(self.niveau, 2)) + (50 * self.niveau) + 25

        return cost


class Mine(Extraction):
    """
    Classe MineMetal --> Classe du batiment Mine de metal. S'occupe de generer ressource 'metal'
    
    Parameters
    ----------
    nb.metal : int
        Nombre de metal produit et stocké dans le batiment Centrale
    Args:
        Extraction : Child de la classe Extraction
    """

    def __init__(self, planete, proprietaire):
        super().__init__(planete, proprietaire)

    def upgrade(self):
        cost = (100 * pow(self.niveau, 2)) + (50 * self.niveau) + 25
        return cost

class Usine(Batiment):

    def __init__(self, planete, proprietaire):
        super().__init__(planete, proprietaire)


class Canon(Batiment):  # defenses
    def __init__(self, planete, proprietaire):
        super().__init__(planete, proprietaire)

        self.puissance = self.niveau * 1.5

    def tir_defense(self, vaisseau):
        while vaisseau.pdv > 0:
            ...


class Balise(Batiment):
    def __init__(self, planete, proprietaire, position):
        super().__init__(planete, proprietaire)

        self.position = position

    def get_position(self):
        return self.position


class CentreRecherche(Batiment):
    def __init__(self, planete, proprietaire):
        super().__init__(planete, proprietaire)

    def upgrade(self, batiment, ressourceUpgrade):
        if batiment.proprietaire == self.proprietaire:
            if self.proprietaire.ressource["metal"] >= ressourceUpgrade["metal"] & self.proprietaire.ressource[
                "pierre"] >= ressourceUpgrade["pierre"]:
                pass  # upgrade batiment.niveau... etc


class AccelerateurParticule(Batiment):
    def __init__(self, planete, proprietaire):
        super().__init__(planete, proprietaire)

    def end_game(self):
        pass


class Porte_de_vers():
    def __init__(self, parent, x, y, couleur, taille):
        self.parent = parent
        self.id = get_prochain_id()
        self.x = x
        self.y = y
        self.pulsemax = taille
        self.pulse = random.randrange(self.pulsemax)
        self.couleur = couleur

    def jouer_prochain_coup(self):
        self.pulse += 1
        if self.pulse >= self.pulsemax:
            self.pulse = 0


class Trou_de_vers():
    def __init__(self, x1, y1, x2, y2):
        self.id = get_prochain_id()
        taille = random.randrange(6, 20)
        self.porte_a = Porte_de_vers(self, x1, y1, "red", taille)
        self.porte_b = Porte_de_vers(self, x2, y2, "orange", taille)
        self.liste_transit = []  # pour mettre les vaisseaux qui ne sont plus dans l'espace mais maintenant l'hyper-espace

    def jouer_prochain_coup(self):
        self.porte_a.jouer_prochain_coup()
        self.porte_b.jouer_prochain_coup()


class Astre():
    def __init__(self, parent: Modele, x: int, y: int, taille: int):
        self.id = get_prochain_id()
        self.parent = parent
        self.x = x
        self.y = y
        self.taille = taille

    def getId(self):
        return self.id


class Etoile(Astre):
    def __init__(self, parent: Modele, x: int, y: int):
        super().__init__(parent, x, y, random.randrange(4, 8))
        self.proprietaire: str = ""
        self.ressources = Ressource(
            random.randint(100, 500),
            random.randint(100, 500),
            random.randint(100, 500)
        ) * self.taille

        self.ressources_dispo = {
            "pierre": 0,
            "metal": 0,
            "energie": 0}

        # Pour chaque bat, faire un dict de bat comme pour les vaisseau
        self.batiments = {
            "centrale": {},
            "mine": {},
            "usine":{},
            "canon": {},
            "balise": {},
            "centreRecherche": {},
        }

        self.artefact = self._add_artefact()

    def getRessources(self):
        return self.ressources.get()
    
    def _add_artefact(self) -> Artefact | None:
        num = random.randint(0, 10)
        return Artefact() if num < 10 else None


class Nuage(Astre):
    def __init__(self, parent: Modele, x: int, y: int):
        super().__init__(parent, x, y, random.randrange(12, 8))


class Vaisseau():
    def __init__(self, parent: Joueur, nom: str, x: int, y: int, vaisseau = Class):
        self.type_vaisseau = vaisseau
        self.parent = parent
        self.id: int = get_prochain_id()
        self.proprietaire = nom
        self.x = x
        self.y = y
        self.taille: int = 5
        self.vitesse: int = 2
        self.cible: int = 0
        self.type_cible = None
        self.angle_cible = 0
        self.arriver = {"Etoile": self.arriver_etoile,
                        "Porte_de_vers": self.arriver_porte}

        self.niveau = 1  # ajout de niveau du vaisseau

        self.pdv = 100 * self.niveau  # ajout de point de vie du vaisseau
        

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.cible != 0:
            return self.avancer()
        elif trouver_nouveau:
            cible = random.choice(self.parent.parent.etoiles)
            self.acquerir_cible(cible, "Etoile")

    def acquerir_cible(self, cible, type_cible):
        self.type_cible = type_cible
        self.cible = cible
        self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

    def avancer(self):
        if self.cible != 0:
            x = self.cible.x
            y = self.cible.y
            self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)
            if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                type_obj = type(self.cible).__name__
                rep = self.arriver[type_obj]()
                return rep

    def arriver_etoile(self):
        #mettre methode construire batiment -------------------------*****************************----------------------------------
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant, "Etoile", self.id, self.cible.id, self.cible.proprietaire])
        if not self.cible.proprietaire:
            self.cible.proprietaire = self.proprietaire
        cible = self.cible
        self.cible = 0
        #if type de vaisseau == cargo ALORS afficher construction
        if self.type_vaisseau == Cargo:
            self.parent.parent.parent.afficher_construction()
        return ["Etoile", cible]

    def arriver_porte(self):
        self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant, "Porte", self.id, self.cible.id, ])
        cible = self.cible
        trou = cible.parent
        if cible == trou.porte_a:
            self.x = trou.porte_b.x + random.randrange(6) + 2
            self.y = trou.porte_b.y
        elif cible == trou.porte_b:
            self.x = trou.porte_a.x - random.randrange(6) + 2
            self.y = trou.porte_a.y
        self.cible = 0
        return ["Porte_de_ver", cible]


class Combat(Vaisseau):

    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y, Combat)
        self.combatpoints = 0
        self.taille: int = 5
        self.vitesse: int = 2
        self.cible: int = 0
        self.type_cible = None
        self.angle_cible = 0


class Explorer(Vaisseau):

    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y, Explorer)
        self.taille: int = 5
        self.vitesse: int = 2
        self.cible: int = 0
        self.type_cible = None
        self.angle_cible = 0


class Cargo(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y, Cargo)
        self.cargo = 1000
        self.taille = 6
        self.vitesse = 1
        self.cible = 0
        self.ang = 0
        self.idPlanete = 0


class Joueur():  # **************************************************************** --- JOUEUR --- **********************************************************
    def __init__(self, parent, nom, etoilemere, couleur):
        self.id = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.etoilemere = etoilemere
        self.etoilemere.proprietaire = self.nom
        self.couleur = couleur
        self.log = []
        self.etoilescontrolees = [etoilemere]
        self.prix = []

        self.flotte = {"Combat": {},
                       "Explorer": {},
                       "Cargo": {}}
        self.ressources = Ressource(0, 0, 0)

        self.flotte = {"Vaisseau": {},
                       "Combat": {},
                       "Explorer": {},
                       "Cargo": {}}

        self.niveau_bat = {
            "mine": 0,
            "centrale": 0,
            "canon": 0,
            "usine": 0,
            "balise": 0,
            "centreRecherche": 0
        }

        self.experience = 0
        self.niveau = 1
        self.actions = {"creervaisseau": self.creervaisseau,
                        "cibleretoile": self.cibleretoile,
                        "creerbatiment": self.creerbatiment,
                        "upgradebatiment": self.upgradebatiment,
                        "recolterressources": self.recolterressources,
                        "updateprix": self.calcul_prix_construction}

    def recolterressources(self, params):  # methode pour recolter les ressources dans une planete
        id_planete = params
        for planete in self.etoilescontrolees:
            if planete.getId() != id_planete:
                continue
            else:
                for ressource in planete.ressources_dispo:
                    self.ressources["pierre"] += planete.ressource_dispo[ressource]
                    planete.ressource_dispo[ressource] = 0

    def creerbatiment(self, params):  # methode joueur pour creer un batiment dans une planete

        id_planete = params[0]
        type_batiment = params[1]
        type_batiment = type_batiment.lower()
        bat = None

        for planete in self.etoilescontrolees:
            if planete.getId() == id_planete:
                self.calcul_prix_construction(id_planete)
                if type_batiment == "mine" or type_batiment == "centrale":

                    if type_batiment == "mine" and self.ressources["pierre"] >= self.prix[0]:
                        costMP = self.prix[0]
                        self.ressources["pierre"] -= costMP
                        bat = Mine(id_planete, self.nom)
                        self.niveau_bat[type_batiment] += 1
                        self.experience += 100
                    elif type_batiment == "centrale" and self.ressources["metal"] >= self.prix[1]:
                        costMP = self.prix[1]
                        self.ressources["metal"] -= costMP
                        bat = Centrale(id_planete, self.nom)
                        self.niveau_bat[type_batiment] += 1
                        self.experience += 100
                elif type_batiment == "usine" or type_batiment == "canon":
                    if type_batiment == "usine":
                        cost = self.prix[2]
                    else:
                        cost = self.prix[3]

                    if self.ressources["metal"] >= cost and self.ressources["energie"] >= cost:
                        self.ressources["metal"] -= cost
                        self.ressources["energie"] -= cost

                        if type_batiment == "usine":
                            bat = Usine(id_planete, self.nom)
                        else:
                            bat = Canon(id_planete, self.nom)

                        self.niveau_bat[type_batiment] += 1
                        self.experience += 250
                elif type_batiment == "balise":
                    cost = self.prix[4]

                    if self.ressources["metal"] >= cost and self.ressources["energie"] >= cost:
                        self.ressources["metal"] -= cost
                        self.ressources["energie"] -= cost
                        bat = Balise(id_planete, self.nom)
                        self.experience += 175
                elif type_batiment == "cdr":
                    bat = CentreRecherche(id_planete, self.nom)
                    self.niveau_bat[type_batiment] += 1

                if bat != None:
                    planete.batiments[type_batiment][bat.id] = bat
                    print("batiment construit")
                    self.parent.parent.afficher_notif(1)
                    self.calcul_prix_construction(id_planete)
                else:
                    print(self.ressources)
                    print("Pas assez de ressource")
                    self.parent.parent.afficher_notif(2)


    def calcul_prix_construction(self, params):
        if isinstance(params, list):
            id = params[2]
        else:
            id = params
        self.prix.clear()
        for planete in self.etoilescontrolees:
            if planete.getId() == id:
                self.prix.append(len(planete.batiments["mine"]) * 100)
                self.prix.append(len(planete.batiments["centrale"]) * 100)
                self.prix.append((len(planete.batiments["usine"]) + 1) * 100)
                self.prix.append((len(planete.batiments["canon"]) + 1) * 150)
                self.prix.append((len(planete.batiments["balise"]) + 1) * 300)

        print(self.prix)
        self.parent.parent.update_prix_construction(self.prix)

        return self.prix

    def upgradebatiment(self, params):
        type = params[0].lower()
        upgrade = False

        if type == "mine" or type == "centrale":
            cost = (100 * pow(self.niveau_bat[type], 2)) + (50 * self.niveau_bat[type]) + 25

            if type == "mine" and self.ressources["pierre"] >= cost:
                self.ressources["pierre"] -= cost
                self.niveau_bat[type] += 1
                upgrade = True
                self.experience += 25
            elif type == "centrale" and self.ressources["metal"] >= cost:
                self.ressources["metal"] -= cost
                self.niveau_bat[type] += 1
                upgrade = True
                self.experience += 25
            if upgrade:
                for planete in self.etoilescontrolees:
                    for bat in planete.batiments[type]:
                        planete.batiments[type][bat].niveau += 1

    def creervaisseau(self, params):
        type_vaisseau = params[0]
        x, y = params[1], params[2]
        
        vaisseaux = {
            "Cargo": Cargo(self, self.nom, x + 10, y),
            "Combat": Combat(self, self.nom, x + 10, y),
            "Explorer": Explorer(self, self.nom, x + 10, y)
        }

        self.experience += 50

        if type_vaisseau in vaisseaux:
            v = vaisseaux.get(type_vaisseau)
        else:
            v = Explorer(self, self.nom, x + 10, y)
            
        self.flotte[type_vaisseau][v.id] = v

        if self.nom == self.parent.parent.mon_nom:
            self.parent.parent.lister_objet(type_vaisseau, v.id)
        return v

    def cibleretoile(self, ids):
        idori, iddesti, type_cible = ids
        print(idori) #id vaisseau (cargo par exemple)
        print(iddesti) #id destination (id de la planete ou du trou de vers par exemple)
        print(type_cible) #type cible en string ("Etoile") par exemple


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
                    if j.porte_a.id == iddesti:
                        cible = j.porte_a
                    elif j.porte_b.id == iddesti:
                        cible = j.porte_b
                    if cible:
                        ori.acquerir_cible(cible, type_cible)
                        return

    def jouer_prochain_coup(self):
        self.avancer_flotte()
        self.generer_res()
        self.levelUp()



    def levelUp(self):
        if self.niveau == 1 and self.experience >= 1000:
            self.niveau += 1
            self.parent.parent.afficher_notif(3)
        elif self.niveau == 2 and self.experience >= 2500:
            self.niveau += 1
            self.parent.parent.afficher_notif(3)
        elif self.niveau == 3 and self.experience >= 4500:
            self.niveau += 1
            self.parent.parent.afficher_notif(3)
        elif self.niveau == 4 and self.experience >= 7000:
            self.niveau += 1
            self.parent.parent.afficher_notif(3)
        elif self.niveau == 5 and self.experience >= 10000:
            self.niveau += 1
            self.parent.parent.afficher_notif(3)
    
    def avancer_flotte(self, chercher_nouveau=0):
        for i in self.flotte:
            for j in self.flotte[i]:
                j = self.flotte[i][j]
                rep = j.jouer_prochain_coup(chercher_nouveau)
                if rep:
                    if rep[0] == "Etoile" and i == "Combat" or i == "Explorer":
                        # NOTE  est-ce qu'on doit retirer l'etoile de la liste du modele
                        #       quand on l'attribue aux etoilescontrolees
                        #       et que ce passe-t-il si l'etoile a un proprietaire ???
                        self.etoilescontrolees.append(rep[1])
                        if rep[1].artefact:
                            rep[1].artefact.activate_bonus(rep[1], self)
                            
                        self.parent.parent.afficher_etoile(self.nom, rep[1])
                    elif rep[0] == "Porte_de_ver":
                        pass

    def generer_res(self):
        for etoile in self.etoilescontrolees:
            for bat in etoile.batiments:
                b = etoile.batiments[bat]
                if bat == "mine":
                    for mine in b:
                        b[mine].generer(etoile, bat)
                        # Recolte auto ---- TEMPORAIRE
                        if b[mine].ressources["metal"] > 1:
                            self.ressources += b[mine].recolte()
                elif bat == "centrale":
                    for centrale in b:
                        b[centrale].generer(etoile, bat)
                        # Recolte auto ---- TEMPORAIRE
                        if b[centrale].ressources["energie"] > 1:
                            self.ressources += b[centrale].recolte()



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
            v = self.creervaisseau(["Combat", random.randint(0, 5000), random.randint(0, 5000)])
            cible = random.choice(self.parent.etoiles)
            v.acquerir_cible(cible, "Etoile")
            self.cooldown = random.randrange(self.cooldownmax) + self.cooldownmax
        else:
            self.cooldown -= 1


class Modele():
    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur = 9000
        self.hauteur = 9000
        self.nb_etoiles = int((self.hauteur * self.largeur) / 500000)
        self.joueurs = {}
        self.actions_a_faire = {}
        self.etoiles = []
        self.trou_de_vers = []
        self.cadre_courant = None
        self.creeretoiles(joueurs, 1)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)

    def getEtoileById(self, id):
        for i in range(len(self.etoiles)):
            if id == self.etoiles[i].id:
                return self.etoiles[i]

    def creer_troudevers(self, n):
        bordure = 10
        for i in range(n):
            x1 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y1 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            x2 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y2 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.trou_de_vers.append(Trou_de_vers(x1, y1, x2, y2))

    def creeretoiles(self, joueurs, ias=0):
        bordure = 10
        for i in range(self.nb_etoiles):
            x = random.randrange(self.largeur - (2 * bordure)) + bordure
            y = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.etoiles.append(Etoile(self, x, y))
        np = len(joueurs) + ias
        etoile_occupee = []
        while np:
            p = random.choice(self.etoiles)
            if p not in etoile_occupee:
                etoile_occupee.append(p)
                self.etoiles.remove(p)
                np -= 1

        couleurs = ["red", "blue", "lightgreen", "yellow",
                    "lightblue", "pink", "gold", "purple"]
        for i in joueurs:
            etoile = etoile_occupee.pop(0)
            self.joueurs[i] = Joueur(self, i, etoile, couleurs.pop(0))
            x = etoile.x
            y = etoile.y
            dist = 500
            for e in range(5):
                x1 = random.randrange(x - dist, x + dist)
                y1 = random.randrange(y - dist, y + dist)
                self.etoiles.append(Etoile(self, x1, y1))
            self.joueurs[i].calcul_prix_construction(etoile.getId())

        # IA- creation des ias
        couleursia = ["orange", "green", "cyan",
                      "SeaGreen1", "turquoise1", "firebrick1"]
        for i in range(ias):
            self.joueurs["IA_" + str(i)] = IA(self, "IA_" + str(i), etoile_occupee.pop(0), couleursia.pop(0))

    ##############################################################################
    def jouer_prochain_coup(self, cadre):
        #  NE PAS TOUCHER LES LIGNES SUIVANTES  ################
        self.cadre_courant = cadre
        # insertion de la prochaine action demandée par le joueur
        if cadre in self.actions_a_faire:
            for i in self.actions_a_faire[cadre]:
                self.joueurs[i[0]].actions[i[1]](i[2])
                """
                i a la forme suivante [nomjoueur, action, [arguments]
                alors self.joueurs[i[0]] -> trouve l'objet représentant le joueur de ce nom
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

    def creer_bibittes_spatiales(self, nb_biittes=0):
        pass

    #############################################################################
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
