import pygame
import numpy as np
import math
import sys
from random import choice

#LES CONSTANTES
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)

LIGNE = 6
COLONNE = 7
TAILLE_CASE = 100
RAYON = 40


HUMAIN = 1
IA = 2

PROFONDEUR_IA = 6

class Grille:
    def __init__(self):
        self.grille = np.zeros((LIGNE, COLONNE), dtype=int)

    def col_valide(self, col):
        return self.grille[0][col] == 0

    def obtenir_cols_valides(self):
        return [c for c in range(COLONNE) if self.col_valide(c)]

    def remplir(self, col, joueur):
        if not self.col_valide(col):
            return False
        for r in range(LIGNE - 1, -1, -1):
            if self.grille[r][col] == 0:
                self.grille[r][col] = joueur
                return True
        return False
    
    def annuler_coup(self, col):
        for r in range(LIGNE):
            if self.grille[r][col] != 0:
                self.grille[r][col] = 0
                return

    def verifier_gagnant(self, piece):
        #horizontal
        for c in range(COLONNE - 3):
            for r in range(LIGNE):
                if self.grille[r][c] == piece and self.grille[r][c+1] == piece and \
                   self.grille[r][c+2] == piece and self.grille[r][c+3] == piece:
                    return True
        #verticale
        for c in range(COLONNE):
            for r in range(LIGNE - 3):
                if self.grille[r][c] == piece and self.grille[r+1][c] == piece and \
                   self.grille[r+2][c] == piece and self.grille[r+3][c] == piece:
                    return True
        #diagonale droite
        for c in range(COLONNE - 3):
            for r in range(LIGNE - 3):
                if self.grille[r][c] == piece and self.grille[r+1][c+1] == piece and \
                   self.grille[r+2][c+2] == piece and self.grille[r+3][c+3] == piece:
                    return True
        #diagonale gauche
        for c in range(COLONNE - 3):
            for r in range(3, LIGNE):
                if self.grille[r][c] == piece and self.grille[r-1][c+1] == piece and \
                   self.grille[r-2][c+2] == piece and self.grille[r-3][c+3] == piece:
                    return True
        return False



def evaluer_fenetre(fenetre, piece):
    score = 0
    piece_adv = HUMAIN if piece == IA else IA

    if fenetre.count(piece) == 4:
        score += 100
    elif fenetre.count(piece) == 3 and fenetre.count(0) == 1:
        score += 5
    elif fenetre.count(piece) == 2 and fenetre.count(0) == 2:
        score += 2

    if fenetre.count(piece_adv) == 3 and fenetre.count(0) == 1:
        score -= 4 

    return score

def score_position(grille, piece):
    score = 0
    matrice = grille.grille
    
    #centre
    centre = [matrice[r][COLONNE//2] for r in range(LIGNE)]
    score += centre.count(piece) * 3

    #horizontal
    for r in range(LIGNE):
        ligne = list(matrice[r, :])
        for c in range(COLONNE - 3):
            fenetre = ligne[c:c+4]
            score += evaluer_fenetre(fenetre, piece)

    #vertical
    for c in range(COLONNE):
        col = list(matrice[:, c])
        for r in range(LIGNE - 3):
            fenetre = col[r:r+4]
            score += evaluer_fenetre(fenetre, piece)

    #diagonales
    for r in range(LIGNE - 3):
        for c in range(COLONNE - 3):
            fenetre = [matrice[r+i][c+i] for i in range(4)]
            score += evaluer_fenetre(fenetre, piece)
    for r in range(3, LIGNE):
        for c in range(COLONNE - 3):
            fenetre = [matrice[r-i][c+i] for i in range(4)]
            score += evaluer_fenetre(fenetre, piece)

    return score

def minimax(grille, profondeur, alpha, beta, maximisant):
    valid_col = grille.obtenir_cols_valides()
    terminal = grille.verifier_gagnant(HUMAIN) or grille.verifier_gagnant(IA) or len(valid_col) == 0

    if profondeur == 0 or terminal:
        if terminal:
            if grille.verifier_gagnant(IA): return (None, 1000000)
            elif grille.verifier_gagnant(HUMAIN): return (None, -1000000)
            else: return (None, 0)
        else:
            return (None, score_position(grille, IA))

    if maximisant:
        valeur = -math.inf
        meilleure_col = choice(valid_col)  #pour que l'ia evite de repeter les meme coup quand bcp de coup ont le meme score 
        for col in valid_col:
            grille.remplir(col, IA)
            nouv_score = minimax(grille, profondeur - 1, alpha, beta, False)[1]
            grille.annuler_coup(col)
            if nouv_score > valeur:
                valeur = nouv_score
                meilleure_col = col
            alpha = max(alpha, valeur)
            if alpha >= beta: break
        return meilleure_col, valeur
    else:
        valeur = math.inf
        meilleure_col = choice(valid_col)
        for col in valid_col:
            grille.remplir(col, HUMAIN)
            nouv_score = minimax(grille, profondeur - 1, alpha, beta, True)[1]
            grille.annuler_coup(col)
            if nouv_score < valeur:
                valeur = nouv_score
                meilleure_col = col
            beta = min(beta, valeur)
            if alpha >= beta: break
        return meilleure_col, valeur



def dessiner_grille(screen, grille):
    screen.fill(BLANC)
    for c in range(COLONNE):
        for r in range(LIGNE):
            pos_x = c * TAILLE_CASE + TAILLE_CASE // 2
            pos_y = r * TAILLE_CASE + TAILLE_CASE // 2
            
            if grille.grille[r][c] == HUMAIN:
                pygame.draw.circle(screen, ROUGE, (pos_x, pos_y), RAYON)
            elif grille.grille[r][c] == IA:
                pygame.draw.circle(screen, BLEU, (pos_x, pos_y), RAYON)
    
    # dessin des  lignes de la grille juste pour faire beau 
    for x in range(COLONNE + 1):
        pygame.draw.line(screen, NOIR, (x * TAILLE_CASE, 0), (x * TAILLE_CASE, LIGNE * TAILLE_CASE), 3)
    for y in range(LIGNE + 1):
        pygame.draw.line(screen, NOIR, (0, y * TAILLE_CASE), (COLONNE * TAILLE_CASE, y * TAILLE_CASE), 3)
    
    pygame.display.update()

def jouer():
    pygame.init()
    screen = pygame.display.set_mode((COLONNE * TAILLE_CASE, LIGNE * TAILLE_CASE))
    pygame.display.set_caption("Puissance 4 Humain vs IA_Minimax")
    font = pygame.font.Font(None, 60)

    grille = Grille()
    dessiner_grille(screen, grille)
    
    game_over = False
    tour = HUMAIN # je me donne un avantage haha

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and tour == HUMAIN:
                pos_x = event.pos[0]
                col = pos_x // TAILLE_CASE

                if grille.col_valide(col):
                    grille.remplir(col, HUMAIN)
                    dessiner_grille(screen, grille)

                    if grille.verifier_gagnant(HUMAIN):
                        label = font.render("J'AI GAGNE", 1, ROUGE)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True
                    else:
                        tour = IA
        if tour == IA and not game_over:
            col, minimax_score = minimax(grille, PROFONDEUR_IA, -math.inf, math.inf, True)
            if col is not None and grille.col_valide(col):
                grille.remplir(col, IA)
                dessiner_grille(screen, grille)

                if grille.verifier_gagnant(IA):
                    label = font.render("L'IA A GAGNE", 1, BLEU)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    game_over = True
                else:
                    tour = HUMAIN
            else:
                # Match nul si colonne None
                game_over = True
                label = font.render("MATCH NULL", 1, BLEU)

    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    jouer()