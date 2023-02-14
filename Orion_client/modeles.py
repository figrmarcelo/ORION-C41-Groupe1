from __future__ import annotations


class Ressource(dict):
    """Classe **Ressource** représentant les ressources du jeu.

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

    def __sub__(self, other: Ressource | dict) -> Ressource:
        """Soustrait deux ressources"""
        return Ressource(
            self['pierre'] - other['pierre'],
            self['metal'] - other['metal'],
            self['energie'] - other['energie']
        )


# test
r1 = Ressource(1, 2, 3)
r2 = Ressource(4, 5, 6)

print(r1 + r2)
print(r1 - r2)
