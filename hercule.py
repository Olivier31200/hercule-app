# hercule.py

def calculer_variation(prix_actuel, prix_veille):
    """Calcule la variation en pourcentage entre deux prix."""
    if prix_veille == 0:
        return 0
    return ((prix_actuel - prix_veille) / prix_veille) * 100

def generer_affichage_sticker(prix_actuel, prix_veille):
    variation = calculer_variation(prix_actuel, prix_veille)
    
    # Codes couleurs pour le terminal (ANSI)
    VERT = '\033[42m\033[37m'  # Fond vert, texte blanc
    ROUGE = '\033[41m\033[37m' # Fond rouge, texte blanc
    GRIS = '\033[47m\033[30m'  # Fond gris, texte noir
    RESET = '\033[0m'          # Reset couleur

    # Choix du signe et de la couleur
    if variation > 0:
        sticker = f"{VERT} +{variation:.2f}% {RESET}"
    elif variation < 0:
        sticker = f"{ROUGE} {variation:.2f}% {RESET}"
    else:
        sticker = f"{GRIS} 0.00% {RESET}"

    print(f"Prix : {prix_actuel:.2e}€/g  {sticker}")

# --- Test du script ---
if __name__ == "__main__":
    PRIX_DU_JOUR = 2.46
    PRIX_HIER = 2.30
    
    generer_affichage_sticker(PRIX_DU_JOUR, PRIX_HIER)
