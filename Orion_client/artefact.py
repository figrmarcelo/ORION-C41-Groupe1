from random import choice, randint

from orion_modele import Mine, Centrale, Ressource, Usine

class Artefact:
    """Liste de noms de bonus qu'un artéfact peut avoir"""
    noms = ['mine', 'cdr', 'usine', 'ressource'] 
    
    def __init__(self):
        self.nom = 'Artefact ' + choice(Artefact.noms)
    
    def activate_bonus(self, planete, joueur):
        type_bonus = {
            'mine': Mine(planete, joueur),
            'cdr': Centrale(planete, joueur),
            'usine': Usine(planete, joueur),
            'ressource': Ressource(randint(10, 1000), randint(10, 1000), randint(10, 1000))
        }
        
        nom, bonus = self._get_nom_and_bonus(type_bonus)
        
        if nom == 'ressource':
            k = choice(list(planete.ressources))
            res = planete.ressource[k]
            nb_res = type_bonus[nom][k]
            res += nb_res
            print(f'Vous avez gagné {nb_res} {res}s')
        else:
            planete.batiments[nom][bonus.id] = bonus
            print(f'Vous avez gagné une nouvelle {type_bonus[nom].__name__}')
            

    def _get_nom_and_bonus(self, liste_bonus: dict) -> tuple[str, any(Mine, Centrale, Ressource, Usine)]:
        return self.nom[9:], liste_bonus.get(self.nom[9:])