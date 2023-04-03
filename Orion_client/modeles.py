from __future__ import annotations

from random import choice, randint


class Ressource(dict):
    """Classe Ressource représentant les ressources du jeu.

    La classe contient des pierres, des métaux et de l'énergie.

    Paramètres
    ----------
    dict : dict[str, int]
        dictionnaire contenant les types de ressources
    pierre : int, optional
        quantité de pierres, 0 par défaut
    metal : int, optional
        quantité de métaux, 0 par défaut
    energie : int, optional
        quantité d'énergie, 0 par défaut
    """

    def __init__(self, pierre: int = 0, metal: int = 0, energie: int = 0):
        """Constructeur de Ressource"""
        
        self['pierre'] = int(pierre)
        self['metal'] = int(metal)
        self['energie'] = int(energie)

    def __add__(self, other: Ressource | dict[str, int]) -> Ressource:
        """Additionne deux ressources"""
        
        return Ressource(
            self['pierre'] + other['pierre'],
            self['metal'] + other['metal'],
            self['energie'] + other['energie']
        )

    def __sub__(self, other: Ressource | dict[str, int]) -> Ressource:
        """Soustrait deux ressources"""
       
        return Ressource(
            self['pierre'] - other['pierre'],
            self['metal'] - other['metal'],
            self['energie'] - other['energie']
        )
        
    def __mul__(self, other: int) -> Ressource: 
        """Multiplie les ressources"""
        
        return Ressource(
            self['pierre'] * other,
            self['metal'] * other,
            self['energie'] * other
        )


class Artefact:
       
    @classmethod
    def activate_bonus(cls, planete, joueur):
        type_bonus = {
            'mine': Mine(planete, joueur),
            'cdr': Centrale(planete, joueur),
            'usine': Usine(planete, joueur),
            'ressource': Ressource(randint(10, 1000), randint(10, 1000), randint(10, 1000))
        }
        
        key, value = choice(list(type_bonus.items()))
        
        if key == 'ressource':
            k = choice(list(planete.ressources))
            res = planete.ressource[k]
            nb_res = type_bonus[key][k]
            res += nb_res
            print(f'Vous avez gagné {nb_res} {res}s')
        else:
            planete.batiments[key][value.id] = value
            print(f'Vous avez gagné une nouvelle {type_bonus[key].__name__}')

# TEST    
if __name__ == '__main__':
    
    r1 = Ressource(1, 2, 3)
    r2 = Ressource(4, 5, 6)

    print(r1 + r2)
    print(r1 - r2)
    
    r = Ressource(10, 20, 30) * 5
