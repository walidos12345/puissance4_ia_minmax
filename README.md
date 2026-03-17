# puissance4_ia_minmax
Jeu de Puissance 4 avec interface Pygame. IA basée sur l'algorithme Minimax et l'élagage Alpha-Bêta.
Ce projet est une implémentation du Puissance 4 en Python. J'ai développé une IA capable d'anticiper les coups du joueur pour proposer un défi réel, en utilisant des concepts fondamentaux de l'Intelligence Artificielle de décision.

# Fonctionnalités
- Interface Graphique : Jeu fluide réalisé avec `Pygame`.
- IA Stratégique : Algorithme Minimax avec élagage Alpha-Bêta.
- Analyse Prédictive : L'IA anticipe jusqu'à 6 coups à l'avance.

# La fonction Score

La partie la plus intéressante de ce projet est la manière dont l'IA évalue le plateau. Comme elle ne peut pas simuler toutes les possibilités jusqu'à la fin de la partie, elle utilise une fonction de "scoring" pour juger si une position est avantageuse ou dangereuse à chaque tour.

Voici ma logique de priorité :
1. Le contrôle du centre :** Dans mon code, l'IA cherche d'abord à placer ses jetons dans la colonne centrale car elle a plus de possibilités d'alignements que de rester sur les bords.
2. L'analyse des opportunités :L'IA scanne le plateau pour trouver des "fenêtres" de 4 cases. Elle s'attribue des points bonus si elle a 2 ou 3 jetons alignés avec des cases vides, car cela prépare une victoire future. ces point bonus ont été choisi apres plusieur test.
3. Le réflexe de défense :** L'IA n'est pas seulement offensive. Si elle voit que le joueur humain a 3 jetons alignés, elle considère cela comme une menace critique et priorise le blocage pour éviter de perdre au tour suivant.

# Algorithme et Optimisation
Pour que l'ordinateur ne mette pas plusieurs minutes à réfléchir, j'ai implémenté l'élagage Alpha-Bêta. Cette technique permet à l'IA d'ignorer les mauvaises branches de l'arbre de décision dès qu'elle réalise qu'un coup est moins bon qu'un autre déjà analysé. Cela rend le programme beaucoup plus rapide et efficace.
