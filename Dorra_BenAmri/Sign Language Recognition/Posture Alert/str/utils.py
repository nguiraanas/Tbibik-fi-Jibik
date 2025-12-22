# Fonctions utilitaires supplémentaires
def distance(p1, p2):
    import numpy as np
    return np.linalg.norm(np.array(p1) - np.array(p2))
