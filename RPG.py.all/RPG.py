#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import sys
import webbrowser
import time
import json
import os

# Langue par défaut ("fr" ou "en")
LANG = "fr"

# Traductions : clé = texte français original, valeur = texte anglais
TRANSLATIONS_EN = {
    "CARTE DU MONDE": "WORLD MAP",
    "Légende:": "Legend:",
    "  @ = Ta position": "  @ = Your position",
    "  VI = Village | FR = Forêt | ST = Souterrain": "  VI = Village | FR = Forest | ST = Underground",
    "  CH = Château | MM = Marais Maudit | VF = Volcan de Feu": "  CH = Castle | MM = Cursed Swamp | VF = Fire Volcano",
    "  TI = Tour Interdite | CT = Chambre du Trésor": "  TI = Forbidden Tower | CT = Treasure Chamber",
    "Erreur: localisation inconnue!": "Error: unknown location!",
    "Cette porte est verrouillée!": "This door is locked!",
    "Tu as besoin de {quant} {item}(s) pour l'ouvrir.": "You need {quant} {item}(s) to open it.",
    "Tu en possèdes: {have}/{need}": "You have: {have}/{need}",
    "Tu utilises {quant} {item}(s) pour ouvrir la porte!": "You use {quant} {item}(s) to open the door!",
    "  Tu voyages vers le {direction}...": "  You travel {direction}...",
    "Bienvenue à {destination}!": "Welcome to {destination}!",
    "Sauvegarde créée: {name}": "Save created: {name}",
    "Sauvegarde '{name}' non trouvée!": "Save '{name}' not found!",
    "Veux-tu recommencer ? (oui/non) : ": "Do you want to restart? (yes/no): ",
    "Le jeu se fermera dans 5 secondes...": "The game will close in 5 seconds...",
    "Choix invalide. Réponds par oui ou non.": "Invalid choice. Answer yes or no.",
    "Un combat commence contre {enn} !": "A battle begins against {enn}!",
    "Choisis ton action (a=attaque, e=inventaire, d=dodge, u=objet, r=repos, f=fuite, end=fin) : ": "Choose your action (a=attack, e=inventory, d=dodge, u=item, r=rest, f=flee, end=quit): ",
    "Inventaire :": "Inventory :",
    "=== MENU PRINCIPAL ===": "=== MAIN MENU ===",
    "Localisation: {loc}": "Location: {loc}",
    "Niveau: {lvl} | PV: {pv}/{pvmax} | ATK: {atk} | DEF: {defn} | XP: {cur}/{req}": "Level: {lvl} | HP: {pv}/{pvmax} | ATK: {atk} | DEF: {defn} | XP: {cur}/{req}",
    "1. Combattre un ennemi": "1. Fight an enemy",
    "2. Affronter un boss (si disponible)": "2. Face a boss (if available)",
    "3. Affronter le SUPERBOSS": "3. Face the SUPERBOSS",
    "4. Voir inventaire": "4. View inventory",
    "5. Voir quête active": "5. View active quest",
    "6. Voir la carte": "6. View map",
    "7. Voyager vers une autre région": "7. Travel to another region",
    "8. Sauvegarder la progression": "8. Save progress",
    "9. Quitter": "9. Quit",
    "Tape un chiffre (1-9) : ": "Type a number (1-9): ",
    "Choix invalide": "Invalid choice",
    "Aucun ennemi disponible ici!": "No enemy available here!",
    "Aucun boss disponible ici!": "No boss available here!",
    "Aucune quête active.": "No active quest.",
    "Aucune destination accessible!": "No accessible destinations!",
    "Nom de la sauvegarde (défaut: 'save') : ": "Save name (default: 'save'): ",
    "Fin de la partie.": "End of the game.",
    "BIENVENUE DANS RPG.txt": "WELCOME TO RPG.txt",
    "Choisir (1 ou 2) : ": "Choose (1 or 2): ",
    "Sauvegardes disponibles:": "Available saves:",
    "Quelle sauvegarde charger? (numéro) : ": "Which save to load? (number): ",
    "Merci d'avoir joué !": "Thanks for playing!",
    "Tu ne peux pas aller dans cette direction!": "You can't go that way!",
    "Choisir une destination (numéro) : ": "Choose a destination (number): ",
    "Choix invalide!": "Invalid choice!",
    "Entrée invalide!": "Invalid input!",
}

def tr(template, **kwargs):
    """Translate a French template to the active language and format with kwargs."""
    if LANG.lower().startswith('en'):
        eng = TRANSLATIONS_EN.get(template, template)
        try:
            return eng.format(**kwargs)
        except Exception:
            return eng
    else:
        try:
            return template.format(**kwargs)
        except Exception:
            return template

def tprint(template, **kwargs):
    """Print a translated template."""
    print(tr(template, **kwargs))

def tinput(prompt, **kwargs):
    """Input with translated prompt."""
    return input(tr(prompt, **kwargs))

# Traductions de noms (ennemis, objets, lieux, quêtes)
NAME_TRANSLATIONS_EN = {
    # Ennemis
    "Gobelin": "Goblin",
    "Plante carnivore": "Carnivorous Plant",
    "Squelette": "Skeleton",
    "Dragonnet": "Wyrmling",
    "Bandit": "Bandit",
    "Slime géant": "Giant Slime",
    "Spectre": "Specter",
    "Minotaure": "Minotaur",
    "Harpie": "Harpy",
    "Golem de pierre": "Stone Golem",
    "Vampire": "Vampire",
    "Sorcier corrompu": "Corrupted Sorcerer",
    "Reine Araignée": "Spider Queen",
    "Dragon Ancien": "Ancient Dragon",
    "Tyran de Feu": "Fire Tyrant",
    "Seigneur des Ombres": "Lord of Shadows",
    "Le Sorcier Immortel": "The Immortal Sorcerer",
    "Roi du Marais": "Swamp King",
    "Chef Bandit": "Bandit Chief",
    "Esprit Ancien": "Ancient Spirit",
    "Garde Souterrain": "Underground Guard",
    "Capitaine Noir": "Black Captain",
    "Traqueur du Marais": "Swamp Stalker",
    "Géant de Magma": "Magma Giant",
    "Magicien Maudit": "Cursed Mage",

    # Objets
    "Potion": "Potion",
    "Élixir": "Elixir",
    "Épée magique": "Magic Sword",
    "Bouclier": "Shield",
    "Anneau de Force": "Ring of Strength",
    "Cape d'Invisibilité": "Cloak of Invisibility",
    "Grimoire ancien": "Ancient Grimoire",
    "Amulette de Vie": "Amulet of Life",
    "Couronne des Ombres": "Crown of Shadows",
    "Écaille du Dragon Ancien": "Ancient Dragon Scale",
    "Clé Mystique": "Mystic Key",
    "Or": "Gold",

    # Lieux
    "Village": "Village",
    "Forêt": "Forest",
    "Souterrain": "Underground",
    "Château": "Castle",
    "Marais Maudit": "Cursed Swamp",
    "Volcan de Feu": "Fire Volcano",
    "Tour Interdite": "Forbidden Tower",
    "Chambre du Trésor": "Treasure Chamber",

    # Quêtes
    "Chasser les gobelins": "Hunt the Goblins",
    "Trouver un grimoire ancien": "Find an Ancient Grimoire",
    "Vaincre le Tyran de Feu": "Defeat the Fire Tyrant",
}

DESCRIPTION_TRANSLATIONS_EN = {
    "Un petit village paisible": "A small peaceful village",
    "Une forêt dense et mystérieuse": "A dense and mysterious forest",
    "Un souterrain sombre et profond": "A dark and deep underground",
    "Un château majestueux mais sinistre": "A majestic but sinister castle",
    "Un marais sombre rempli de créatures monstrueuses": "A dark swamp filled with monstrous creatures",
    "Un volcan actif rempli de lave et de cratères! ": "An active volcano filled with lava and craters!",
    "Une tour ancienne remplie de magie noire": "An ancient tower filled with dark magic",
    "Une chambre secrète scintillante de richesses! ": "A secret chamber sparkling with riches! ",
}

def name_tr(name):
    if LANG.lower().startswith('en'):
        return NAME_TRANSLATIONS_EN.get(name, name)
    return name

def desc_tr(text):
    if LANG.lower().startswith('en'):
        return DESCRIPTION_TRANSLATIONS_EN.get(text, text)
    return text
# --- Carte du monde ---
locations = {
    "Village": {
        "description": "Un petit village paisible",
        "ennemis": ["Gobelin", "Bandit"],
        "boss": None,
        "connections": {"Forêt": "est", "Château": "nord"},
        "locked": False
    },
    "Forêt": {
        "description": "Une forêt dense et mystérieuse",
        "ennemis": ["Plante carnivore", "Spectre", "Harpie"],
        "boss": None,
        "connections": {"Village": "ouest", "Souterrain": "sud"},
        "locked": False
    },
    "Souterrain": {
        "description": "Un souterrain sombre et profond",
        "ennemis": ["Squelette", "Slime géant", "Golem de pierre"],
        "boss": ("Reine Araignée", 100, 15, 7),
        "connections": {"Forêt": "nord", "Château": "est"},
        "locked": False
    },
    "Château": {
        "description": "Un château majestueux mais sinistre",
        "ennemis": ["Vampire", "Sorcier corrompu", "Dragonnet"],
        "boss": ("Dragon Ancien", 120, 25, 8),
        "connections": {"Village": "sud", "Souterrain": "ouest", "Tour Interdite": "nord", "Marais Maudit": "est"},
        "locked": False
    },
    "Marais Maudit": {
        "description": "Un marais sombre rempli de créatures monstrueuses",
        "ennemis": ["Minotaure", "Vampire", "Sorcier corrompu", "Spectre"],
        "boss": ("Roi du Marais", 150, 22, 9),
        "connections": {"Château": "ouest", "Volcan de Feu": "est"},
        "locked": False
    },
    "Volcan de Feu": {
        "description": "Un volcan actif rempli de lave et de cratères! ",
        "ennemis": ["Dragonnet", "Sorcier corrompu", "Golem de pierre", "Minotaure"],
        "boss": ("Tyran de Feu", 140, 26, 10,"Dragon enflammé", 150, 25, 11),
        "connections": {"Marais Maudit": "ouest"},
        "locked": False
    },
    "Tour Interdite": {
        "description": "Une tour ancienne remplie de magie noire",
        "ennemis": ["Sorcier corrompu", "Spectre"],
        "boss": ("Seigneur des Ombres", 100, 20, 10),
        "connections": {"Château": "sud"},
        "locked": False
    },
    "Chambre du Trésor": {
        "description": "Une chambre secrète scintillante de richesses! ",
        "ennemis": [],
        "boss": ("Le Sorcier Immortel", 1000, 50, 20),
        "connections": {"Tour Interdite": "ouest"},
        "locked": True,
        "requirement": ("Clé Mystique", 5)
    }
}

# Map drawing constants (reused to avoid reallocating on each call)
MAP_WIDTH = 60
MAP_HEIGHT = 10
MAP_POSITIONS = {
    "Tour Interdite": (25, 1),
    "Chambre du Trésor": (35, 1),
    "Village": (15, 4),
    "Château": (25, 4),
    "Marais Maudit": (35, 4),
    "Volcan de Feu": (45, 4),
    "Forêt": (15, 6),
    "Souterrain": (25, 6)
}

def afficher_carte(joueur):
    print("\n" + "="*60)
    print(tr("CARTE DU MONDE"))
    print("="*60)
    
    # Use module-level constants to avoid recreating these structures repeatedly
    positions = MAP_POSITIONS

    # Créer une grille
    largeur = MAP_WIDTH
    hauteur = MAP_HEIGHT
    grille = [['.' for _ in range(largeur)] for _ in range(hauteur)]
    
    # Placer les lieux
    for lieu, (x, y) in positions.items():
        if y < hauteur and x < largeur:
            if lieu == "Tour Interdite":
                grille[y][x:x+2] = ['T', 'I']
            elif lieu == "Chambre du Trésor":
                grille[y][x:x+2] = ['C', 'T']
            elif lieu == "Village":
                grille[y][x:x+2] = ['V', 'L']
            elif lieu == "Château":
                grille[y][x:x+2] = ['C', 'H']
            elif lieu == "Marais Maudit":
                grille[y][x:x+2] = ['M', 'M']
            elif lieu == "Volcan de Feu":
                grille[y][x:x+2] = ['V', 'F']
            elif lieu == "Forêt":
                grille[y][x:x+2] = ['F', 'R']
            elif lieu == "Souterrain":
                grille[y][x:x+2] = ['S', 'T']
    
    # Placer le joueur
    if joueur.localisation in positions:
        px, py = positions[joueur.localisation]
        if py < hauteur and px < largeur:
            grille[py][px] = '@'  # Point pour le joueur (@ = Player)
    
    # Afficher la grille
    for ligne in grille:
        print(''.join(ligne))
    
    print("\n" + "-"*60)
    print(tr("Légende:"))
    print(tr("  @ = Ta position"))
    print(tr("  VI = Village | FR = Forêt | ST = Souterrain"))
    print(tr("  CH = Château | MM = Marais Maudit | VF = Volcan de Feu"))
    print(tr("  TI = Tour Interdite | CT = Chambre du Trésor"))
    print("-"*60)
    
    # Afficher les infos du lieu
    if joueur.localisation in locations:
        lieu = locations[joueur.localisation]
        print(tr("\n{loc}", loc=name_tr(joueur.localisation)))
        print(f"   {desc_tr(lieu['description'])}")
        print(tr("\n   Connexions:"))
        for destination, direction in lieu["connections"].items():
            locked_str = " [LOCKED]" if locations[destination].get("locked") else ""
            print(tr("     • {dest} ({dir}){locked}", dest=name_tr(destination), dir=direction, locked=locked_str))
    print("="*60 + "\n")

def voyager(joueur, destination):
    if joueur.localisation not in locations:
        print(tr("Erreur: localisation inconnue!"))
        return False
    
    lieu_actuel = locations[joueur.localisation]
    if destination in lieu_actuel["connections"]:
        # Vérifier si la destination est verrouillée
        if locations[destination].get("locked"):
            item_req, quantite_req = locations[destination].get("requirement")
            quantite_possedee = joueur.inventaire.get(item_req, 0)
            if quantite_possedee < quantite_req:
                print(tr("\nCette porte est verrouillée!"))
                print(tr("Tu as besoin de {quant} {item}(s) pour l'ouvrir.", quant=quantite_req, item=item_req))
                print(tr("Tu en possèdes: {have}/{need}", have=quantite_possedee, need=quantite_req))
                return False
            else:
                print(tr("\nTu utilises {quant} {item}(s) pour ouvrir la porte!", quant=quantite_req, item=item_req))
                joueur.inventaire[item_req] -= quantite_req
        
        direction = lieu_actuel["connections"][destination]
        joueur.localisation = destination
        # reset du dernier spawn quand on change de zone (nouvelle zone = nouvelles rencontres)
        joueur.last_spawned_enemy = None
        print(tr("\n  Tu voyages vers le {direction}...", direction=direction))
        print(tr("Bienvenue à {destination}!", destination=destination))
        afficher_carte(joueur)
        return True
    else:
        print(tr("Tu ne peux pas aller dans cette direction!"))
        return False

# --- Système de Sauvegarde ---
SAVE_DIR = "saves"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def sauvegarder_jeu(joueur, nom_sauvegarde="save"):
    """Sauvegarde la progression du joueur"""
    donnees = {
        "nom": joueur.nom,
        "pv": joueur.pv,
        "pv_max": joueur.pv_max,
        "attaque": joueur.attaque,
        "defense": joueur.defense,
        "inventaire": joueur.inventaire,
        "xp": joueur.xp,
        "niveau": joueur.niveau,
        "localisation": joueur.localisation,
        "quete": {
            "nom": joueur.quete.nom if joueur.quete else None,
            "progression": joueur.quete.progression if joueur.quete else 0,
            "terminee": joueur.quete.terminee if joueur.quete else False
        }
    }
    
    chemin_fichier = os.path.join(SAVE_DIR, f"{nom_sauvegarde}.json")
    with open(chemin_fichier, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)
    print(tr("Sauvegarde créée: {name}", name=nom_sauvegarde))

def charger_jeu(nom_sauvegarde="save"):
    """Charge la progression du joueur"""
    chemin_fichier = os.path.join(SAVE_DIR, f"{nom_sauvegarde}.json")
    
    if not os.path.exists(chemin_fichier):
        print(tr("Sauvegarde '{name}' non trouvée!", name=nom_sauvegarde))
        return None
    
    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        donnees = json.load(f)
    
    joueur = Personnage(donnees["nom"], donnees["pv"], donnees["attaque"], donnees["defense"], donnees["pv_max"])
    joueur.pv = donnees["pv"]
    joueur.inventaire = donnees["inventaire"]
    joueur.xp = donnees["xp"]
    joueur.niveau = donnees["niveau"]
    joueur.localisation = donnees["localisation"]
    
    # Recréer la quête si elle existe
    if donnees["quete"]["nom"]:
        quete_data = next((q for q in quetes_possibles if q["nom"] == donnees["quete"]["nom"]), None)
        if quete_data:
            joueur.quete = Quete(quete_data["nom"], quete_data["objectif"], quete_data["recompense"])
            joueur.quete.progression = donnees["quete"]["progression"]
            joueur.quete.terminee = donnees["quete"]["terminee"]
    
    print(f"Sauvegarde chargée: {nom_sauvegarde}") 
    return joueur

def lister_sauvegardes():
    """Liste toutes les sauvegardes disponibles"""
    if not os.path.exists(SAVE_DIR):
        return []
    fichiers = [f[:-5] for f in os.listdir(SAVE_DIR) if f.endswith('.json')]
    return fichiers

def recommencer():
    while True:
        choix = tinput("Veux-tu recommencer ? (oui/non) : ").strip().lower()
        if choix == "oui":
            # relance le menu avec un nouveau héros
            joueur = Personnage("Héros", 100, 15, 5, pv_max=100)
            joueur.loot("Or", 10)
            menu_principal(joueur)
            break  # on sort de la boucle après relance
        elif choix == "non":
            print(tr("Le jeu se fermera dans 5 secondes..."))
            time.sleep(2)
            reddit_url="https://www.reddit.com/r/FreePython/"
            print:("follow me non reddit at {reddit_url}")
            time.sleep(3)
            sys.exit()
        else:
            print(tr("Choix invalide. Réponds par oui ou non."))
# --- Définition des raretés ---
raretes = {
    "Potion": "★",
    "Élixir": "★",
    "Épée magique": "★★",
    "Bouclier": "★★",
    "Anneau de Force": "★★★",
    "Cape d'Invisibilité": "★★★",
    "Grimoire ancien": "★★★",
    "Amulette de Vie": "★★★",
    "Couronne des Ombres": "★★★",
    "Écaille du Dragon Ancien": "★★★",
    "Clé Mystique": "",
    "Or": ""
}

# --- Classe Personnage ---
def total_xp_for_level(level):
    """Retourne le total d'XP requis pour atteindre `level` depuis le niveau 1.

    Formule adoptée: courbe exponentielle croissante
    total_xp(level) = int(40 * (level - 1)^2.2)
    Cela donne des paliers qui deviennent plus rapidement longs.
    """
    return int(40 * (level - 1)**2.2)

class Personnage:
    __slots__ = ('nom', 'pv_max', 'pv', 'attaque', 'defense', 'inventaire', 'xp', 'niveau', 'quete', 'localisation', 'last_spawned_enemy')
    def __init__(self, nom, pv, attaque, defense, pv_max=None):
        self.nom = nom
        self.pv_max = pv if pv_max is None else pv_max
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.inventaire = {}
        self.xp = 0
        self.niveau = 1
        self.quete = None  # quête active
        self.localisation = "Village"  # position sur la carte
        # évite de faire apparaître le même ennemi deux fois de suite
        self.last_spawned_enemy = None

    def est_vivant(self):
        return self.pv > 0

    def subir_degats(self, degats):
        self.pv -= degats
        if self.pv < 0:
            self.pv = 0

    def attaquer(self, cible):
        degats = max(1, self.attaque - cible.defense)  # minimum 1 dégât
        cible.subir_degats(degats)
        print(f"{self.nom} attaque {cible.nom} et inflige {degats} dégâts.")

    def loot(self, objet, quantite=1):
        self.inventaire[objet] = self.inventaire.get(objet, 0) + quantite
        etoiles = raretes.get(objet, "")
        print(f"{self.nom} obtient : {name_tr(objet)} x{quantite} {etoiles}")
        verifier_quete(self, loot=objet)

    def gagner_xp(self, montant):
        # Ajoute l'XP et applique la courbe de leveling (peut monter plusieurs niveaux)
        self.xp += montant
        print(f"{self.nom} gagne {montant} XP (total: {self.xp}).")

        leveled = False
        # Tant que l'XP totale dépasse le palier du niveau suivant, on monte
        while self.xp >= total_xp_for_level(self.niveau + 1):
            self.niveau += 1
            self.attaque += 2
            self.defense += 1
            self.pv_max += 10
            self.pv = self.pv_max
            print(f"{self.nom} monte au niveau {self.niveau} ! ATK+2, DEF+1, PVmax+10.")
            leveled = True

        if not leveled:
            current_into_level = self.xp - total_xp_for_level(self.niveau)
            required = total_xp_for_level(self.niveau + 1) - total_xp_for_level(self.niveau)
            print(f"Progression XP: {current_into_level}/{required} vers le niveau {self.niveau + 1}.")

# --- Quêtes ---
quetes_possibles = [
    {"nom": "Chasser les gobelins", "objectif": ("Gobelin", 3), "recompense": ("Or", 30)},
    {"nom": "Trouver un grimoire ancien", "objectif": ("Grimoire ancien", 1), "recompense": ("XP", 50)},
    {"nom": "Vaincre le Tyran de Feu", "objectif": ("Tyran de Feu", 1), "recompense": ("Cape d'Invisibilité", 1)},
]

class Quete:
    __slots__ = ('nom', 'cible', 'quantite', 'recompense', 'progression', 'terminee')
    def __init__(self, nom, objectif, recompense):
        self.nom = nom
        self.cible, self.quantite = objectif
        self.recompense = recompense
        self.progression = 0
        self.terminee = False

    def avancer(self, ennemi=None, loot=None):
        if ennemi and ennemi.nom == self.cible:
            self.progression += 1
        if loot and loot == self.cible:
            self.progression += 1
        if self.progression >= self.quantite:
            self.terminee = True
            print(f"Quête terminée : {self.nom}")
            return self.recompense
        return None

def donner_quete(joueur):
    quete_data = random.choice(quetes_possibles)
    quete = Quete(quete_data["nom"], quete_data["objectif"], quete_data["recompense"])
    joueur.quete = quete
    print(f"Nouvelle quête : {name_tr(quete.nom)} (objectif : {quete.quantite} {name_tr(quete.cible)})")

def verifier_quete(joueur, ennemi=None, loot=None):
    if joueur.quete and not joueur.quete.terminee:
        recompense = joueur.quete.avancer(ennemi, loot)
        if recompense:
            type_r, valeur = recompense
            if type_r == "XP":
                joueur.gagner_xp(valeur)
            elif type_r == "Or":
                joueur.loot("Or", valeur)
            else:
                joueur.loot(type_r, valeur)

# --- Bosses ---
boss_possibles = [
    ("Dragon Ancien", 120, 25, 8),
    ("Seigneur des Ombres", 100, 20, 10),
    ("Reine Araignée", 100, 15, 7),
    ("Tyran de Feu", 140, 26, 10)
]
# Precompute name sets for fast membership checks (avoids allocating small lists repeatedly)
boss_names = {b[0] for b in boss_possibles}

# --- SUPERBOSS ---
superboss_possibles = [
    ("Le Sorcier Immortel", 1000, 50, 20)
]
superboss_names = {s[0] for s in superboss_possibles}

# --- Ennemis ---
ennemis_possibles = [
    ("Gobelin", 30, 10, 2),
    ("Plante carnivore", 25, 8, 3),
    ("Squelette", 40, 12, 4),
    ("Dragonnet", 60, 15, 5),
    ("Bandit", 35, 11, 3),
    ("Slime géant", 50, 9, 6),
    ("Spectre", 45, 13, 4),
    ("Minotaure", 70, 18, 7),
    ("Harpie", 55, 14, 5),
    ("Golem de pierre", 80, 20, 10),
    ("Vampire", 65, 17, 6),
    ("Sorcier corrompu", 75, 15, 8)
]

# --- Minibosses par localisation ---
minibosses_by_location = {
    "Village": ("Chef Bandit", 60, 15, 5, 0.06),
    "Forêt": ("Esprit Ancien", 80, 16, 6, 0.06),
    "Souterrain": ("Garde Souterrain", 90, 18, 8, 0.07),
    "Château": ("Capitaine Noir", 100, 20, 9, 0.06),
    "Marais Maudit": ("Traqueur du Marais", 110, 19, 9, 0.06),
    "Volcan de Feu": ("Géant de Magma", 130, 22, 11, 0.05),
    "Tour Interdite": ("Magicien Maudit", 95, 20, 9, 0.05)
}

# Jeu rapide : set pour détection dans les récompenses
miniboss_names = {v[0] for v in minibosses_by_location.values()}

def spawn_enemy_for_location(joueur):
    """Choisit aléatoirement un ennemi disponible dans la localisation du joueur,
    applique une petite variation aléatoire aux stats, peut générer une variante 'Élite'
    et, si la localisation a un miniboss, peut faire apparaître ce miniboss.
    Évite de renvoyer le même type d'ennemi deux fois de suite si possible."""
    lieu = locations.get(joueur.localisation, {})

    # 1) Vérifier miniboss lié à la zone (petite chance)
    mb = minibosses_by_location.get(joueur.localisation)
    if mb and random.random() < mb[4]:
        name, base_hp, base_atk, base_def, _chance = mb
        hp = max(1, int(base_hp * random.uniform(0.95, 1.10)))
        atk = max(1, int(base_atk * random.uniform(0.95, 1.05)))
        defn = max(0, int(base_def * random.uniform(0.95, 1.05)))
        # marquer comme dernier spawn pour éviter répétitions immédiates
        joueur.last_spawned_enemy = name
        return Personnage(name, hp, atk, defn)

    # 2) Spawn normal (location-based)
    noms_locaux = lieu.get("ennemis", [])
    templates = [e for e in ennemis_possibles if e[0] in noms_locaux]
    if not templates:
        return None

    # Si possible, exclure le dernier ennemi apparu pour éviter les répétitions
    base_names = [t[0] for t in templates]
    candidates = templates
    if joueur and getattr(joueur, 'last_spawned_enemy', None) in base_names and len(templates) > 1:
        candidates = [t for t in templates if t[0] != joueur.last_spawned_enemy]

    nom, base_hp, base_atk, base_def = random.choice(candidates)

    # Variation aléatoire des stats (+/-)
    hp = max(1, int(base_hp * random.uniform(0.9, 1.2)))
    atk = max(1, int(base_atk * random.uniform(0.9, 1.15)))
    defn = max(0, int(base_def * random.uniform(0.9, 1.15)))

    # Petite chance d'ennemi 'Élite' (boost de stats)
    is_elite = False
    if random.random() < 0.10:
        is_elite = True
        hp = int(hp * 1.35)
        atk = int(atk * 1.25)
        defn = int(defn * 1.2)

    # Conserver le nom de base pour le suivi (sans suffixe Elite)
    joueur.last_spawned_enemy = nom
    final_name = f"{nom} (Élite)" if is_elite else nom
    return Personnage(final_name, hp, atk, defn)

# --- Combat ---
def combat(joueur, ennemi):
    poison = 0    # -3 PV par tour pendant N tours
    brulure = 0   # -2 PV par tour pendant N tours
    stun = False  # saute le tour du joueur

    print(tr("Un combat commence contre {enn} !", enn=name_tr(ennemi.nom)))
    if ennemi.nom == "Le Sorcier Immortel":
        print("Une musique épique résonne dans l'air...")
        try:
            webbrowser.open("https://www.youtube.com/watch?v=LmcQfdxpNLw")
        except:
            pass

    while joueur.est_vivant() and ennemi.est_vivant():
        # Statuts persistants
        if poison > 0:
            joueur.pv = max(0, joueur.pv - 3)
            poison -= 1
            print(f"{joueur.nom} souffre du poison (-3 PV).")
        if brulure > 0:
            joueur.pv = max(0, joueur.pv - 2)
            brulure -= 1
            print(f"{joueur.nom} est brûlé (-2 PV).")

        print(f"\n{joueur.nom} : {joueur.pv}/{joueur.pv_max} PV | ATK {joueur.attaque} | DEF {joueur.defense}")
        print(f"{ennemi.nom} : {ennemi.pv}/{ennemi.pv_max} PV | ATK {ennemi.attaque} | DEF {ennemi.defense}")

        # Tour du joueur
        if stun:
            print(f"{joueur.nom} est étourdi et ne peut pas agir ce tour !")
            stun = False
        else:
            action = tinput("Choisis ton action (a=attaque, e=inventaire, d=dodge, u=objet, r=repos, f=fuite, end=fin) : ").strip().lower()
            if action == "a":
                joueur.attaquer(ennemi)
            elif action == "end":
                print("Fin de la partie.")
                sys.exit()
            elif action == "e":
                print("Inventaire :", joueur.inventaire)
            elif action == "d":
                print(f"{joueur.nom} tente d'esquiver...")
                if random.random() < 0.5:
                    print("Esquive réussie ! Aucun dégât subi ce tour.")
                    # saute le tour de l'ennemi
                    continue
                else:
                    print("Esquive ratée !")
            elif action == "u":
                print("Inventaire :", joueur.inventaire)
                choix_objet = input("Quel objet veux-tu utiliser ? ").strip()
                if choix_objet == "Potion" and joueur.inventaire.get("Potion", 0) > 0:
                    joueur.inventaire["Potion"] -= 1
                    joueur.pv = min(joueur.pv_max, joueur.pv + 20)
                    print(f"{joueur.nom} utilise une Potion (+20 PV).")
                elif choix_objet == "Élixir" and joueur.inventaire.get("Élixir", 0) > 0:
                    joueur.inventaire["Élixir"] -= 1
                    joueur.attaque += 5
                    print(f"{joueur.nom} utilise un Élixir (+5 ATK).")
                else:
                    print("Objet invalide ou indisponible.")
            elif action == "r":
                soin = random.randint(5, 10)
                joueur.pv = min(joueur.pv_max, joueur.pv + soin)
                print(f"{joueur.nom} se repose et récupère {soin} PV.")
            elif action == "f":
                if random.random() < 0.5:
                    print(f"{joueur.nom} réussit à fuir le combat !")
                    return
                else:
                    print("Fuite ratée !")
            else:
                print("Action invalide, tu perds ton tour.")

        # Tour de l'ennemi
        if ennemi.est_vivant():
            if ennemi.nom == "Vampire":
                degats = max(1, ennemi.attaque - joueur.defense)
                joueur.subir_degats(degats)
                soin = degats // 2
                ennemi.pv = min(ennemi.pv_max, ennemi.pv + soin)
                print(f"{ennemi.nom} mord {joueur.nom}, inflige {degats} dégâts et récupère {soin} PV !")

            elif ennemi.nom == "Spectre":
                # 20% de chance d'esquive sur ses propres tours (intangible)
                if random.random() < 0.2:
                    print(f"{ennemi.nom} devient intangible et évite d'attaquer frontalement ce tour.")
                else:
                    ennemi.attaquer(joueur)

            elif ennemi.nom == "Plante carnivore":
                degats = max(1, ennemi.attaque - joueur.defense)
                joueur.subir_degats(degats)
                poison = max(poison, 3)  # applique/rafraîchit 3 tours
                print(f"{ennemi.nom} empoisonne {joueur.nom} ! Poison pendant 3 tours (dégâts subis: {degats}).")

            elif ennemi.nom == "Dragonnet":
                degats = max(1, ennemi.attaque - joueur.defense)
                joueur.subir_degats(degats)
                brulure = max(brulure, 3)  # applique/rafraîchit 3 tours
                print(f"{ennemi.nom} brûle {joueur.nom} ! Brûlure pendant 3 tours (dégâts subis: {degats}).")

            elif ennemi.nom == "Harpie":
                if random.random() < 0.2:
                    stun = True
                    print(f"{ennemi.nom} étourdit {joueur.nom} ! Tu perdras ton prochain tour.")
                else:
                    ennemi.attaquer(joueur)

            elif ennemi.nom == "Golem de pierre":
                # Ignore une partie de la DEF
                degats = max(1, ennemi.attaque - (joueur.defense // 2))
                joueur.subir_degats(degats)
                print(f"{ennemi.nom} frappe brutalement, ignore une partie de la DEF et inflige {degats} dégâts.")

            elif ennemi.nom == "Bandit":
                degats = max(1, ennemi.attaque - joueur.defense)
                if random.random() < 0.2:
                    degats *= 2
                    print(f"{ennemi.nom} réussit une attaque critique !")
                joueur.subir_degats(degats)
                print(f"{ennemi.nom} attaque et inflige {degats} dégâts.")

            elif ennemi.nom == "Minotaure":
                # Charge puissante mais se fatigue (-2 ATK pendant 2 tours simulés via message, pas de buff persistant ici)
                if random.random() < 0.3:
                    degats = max(1, (ennemi.attaque + 5) - joueur.defense)
                    joueur.subir_degats(degats)
                    print(f"{ennemi.nom} charge avec rage et inflige {degats} dégâts !")
                else:
                    ennemi.attaquer(joueur)

            elif ennemi.nom == "Slime géant":
                # Attaque et renvoie un petit splash supplémentaire
                degats = max(1, ennemi.attaque - joueur.defense)
                splash = random.randint(0, 2)
                joueur.subir_degats(degats + splash)
                print(f"{ennemi.nom} écrase et éclabousse : {degats}+{splash} dégâts.")

            elif ennemi.nom == "Sorcier corrompu":
                # Sort aléatoire: feu (brulure), glace (stun), ombre (dégâts bruts)
                sort = random.choice(["feu", "glace", "ombre"])
                if sort == "feu":
                    degats = max(1, ennemi.attaque - joueur.defense)
                    joueur.subir_degats(degats)
                    brulure = max(brulure, 2)
                    print(f"{ennemi.nom} lance un sort de feu : {degats} dégâts et brûlure (2 tours).")
                elif sort == "glace":
                    degats = max(1, ennemi.attaque - joueur.defense - 2)
                    joueur.subir_degats(degats)
                    stun = True
                    print(f"{ennemi.nom} gèle {joueur.nom} : {degats} dégâts et étourdissement.")
                else:
                    degats = max(2, ennemi.attaque - (joueur.defense // 3))
                    joueur.subir_degats(degats)
                    print(f"{ennemi.nom} invoque les ombres et inflige {degats} dégâts occultes.")

            else:
                # Gobelin, Squelette, etc. comportement par défaut
                ennemi.attaquer(joueur)

    # Fin du combat
    if joueur.est_vivant():
        print(f"{joueur.nom} a vaincu {name_tr(ennemi.nom)} !")
        verifier_quete(joueur, ennemi=ennemi)

        if ennemi.nom in superboss_names:
            joueur.gagner_xp(500)
            joueur.loot("Or", 100)
            joueur.loot("Clé Mystique", 0)  # pas de clé pour le superboss
            print("Victoire contre un SUPERBOSS ! Récompenses exceptionnelles.")
        elif ennemi.nom in boss_names:
            joueur.gagner_xp(100)
            joueur.loot("Or", 50)
            joueur.loot("Clé Mystique", 1)  # 1 clé par boss régulier
            print("Victoire contre un Boss !")
        elif ennemi.nom in miniboss_names:
            # Récompenses de miniboss (entre ennemi classique et boss)
            joueur.gagner_xp(60)
            joueur.loot("Or", 30)
            # petite chance de drop rare / clé
            if random.random() < 0.20:
                rare = random.choice(["Épée magique", "Grimoire ancien", "Anneau de Force"])
                joueur.loot(rare, 1)
            if random.random() < 0.12:
                joueur.loot("Clé Mystique", 1)
            print("Victoire contre un Mini-boss !")
        else:
            joueur.gagner_xp(20)
            joueur.loot("Or", 10)
            print("Victoire contre un ennemi classique.")
    else:
        print(f"{joueur.nom} a été vaincu par {ennemi.nom}...")
        time.sleep(2)
        print(tr("Fin de la partie."))
        print(tr("Merci d'avoir joué !"))
        recommencer()
        reddit_url = "https://www.reddit.com/r/FreePython/"
        print(f"Rejoignez ma communauté sur Reddit : {reddit_url}")
        print("Le jeu se fermera dans 5 secondes...")
        time.sleep(5)
        sys.exit()

# --- Menu principal ---
def menu_principal(joueur):
    donner_quete(joueur)  # donne une quête au début
    afficher_carte(joueur)  # affiche la carte au démarrage
    while joueur.est_vivant():
        print("\n" + tr("=== MENU PRINCIPAL ==="))
        print(tr("Localisation: {loc}", loc=joueur.localisation))
        current_into_level = joueur.xp - total_xp_for_level(joueur.niveau)
        required = total_xp_for_level(joueur.niveau + 1) - total_xp_for_level(joueur.niveau)
        print(tr("Niveau: {lvl} | PV: {pv}/{pvmax} | ATK: {atk} | DEF: {defn} | XP: {cur}/{req}", lvl=joueur.niveau, pv=joueur.pv, pvmax=joueur.pv_max, atk=joueur.attaque, defn=joueur.defense, cur=current_into_level, req=required))
        print()
        print(tr("1. Combattre un ennemi"))
        print(tr("2. Affronter un boss (si disponible)"))
        print(tr("3. Affronter le SUPERBOSS"))
        print(tr("4. Voir inventaire"))
        print(tr("5. Voir quête active"))
        print(tr("6. Voir la carte"))
        print(tr("7. Voyager vers une autre région"))
        print(tr("8. Sauvegarder la progression"))
        print(tr("9. Quitter"))

        choix = tinput("Tape un chiffre (1-9) : ").strip()

        if choix == "1":
            # Combat location-based (spawn aléatoire depuis la liste de la localisation)
            ennemi = spawn_enemy_for_location(joueur)
            if ennemi:
                combat(joueur, ennemi)
            else:
                print(tr("Aucun ennemi disponible ici!"))
        elif choix == "2":
            # Boss fight location-based
            lieu = locations.get(joueur.localisation, {})
            if lieu.get("boss"):
                nom, pv, atk, defn = lieu["boss"]
                boss = Personnage(nom, pv, atk, defn)
                combat(joueur, boss)
            else:
                print("Aucun boss disponible ici!")
        elif choix == "3":
            nom, pv, atk, defn = random.choice(superboss_possibles)
            superboss = Personnage(nom, pv, atk, defn)
            combat(joueur, superboss)
        elif choix == "4":
            print("Inventaire :", joueur.inventaire)
        elif choix == "5":
            if joueur.quete:
                q = joueur.quete
                etat = "terminée" if q.terminee else f"{q.progression}/{q.quantite}"
                print(f"Quête : {name_tr(q.nom)} | Objectif : {name_tr(q.cible)} ({etat})")
            else:
                print("Aucune quête active.")
        elif choix == "6":
            afficher_carte(joueur)
        elif choix == "7":
            afficher_carte(joueur)
            lieu = locations.get(joueur.localisation, {})
            if lieu.get("connections"):
                destinations = list(lieu["connections"].keys())
                for i, dest in enumerate(destinations, 1):
                    print(f"{i}. {dest}")
                try:
                    choix_voyage = int(tinput("Choisir une destination (numéro) : "))
                    if 1 <= choix_voyage <= len(destinations):
                        voyager(joueur, destinations[choix_voyage - 1])
                    else:
                        print(tr("Choix invalide!"))
                except (ValueError, IndexError):
                    print(tr("Entrée invalide!"))
            else:
                print(tr("Aucune destination accessible!"))
        elif choix == "8":
            nom_save = tinput("Nom de la sauvegarde (défaut: 'save') : ").strip()
            if not nom_save:
                nom_save = "save"
            sauvegarder_jeu(joueur, nom_save)
        elif choix == "9":
            print("Fin de la partie.")
            print("le jeu se fermera dans 5 secondes...")
            time.sleep(5)
            sys.exit()
        else:
            print("Choix invalide.")

# --- Lancement du jeu ---
def launcher():
    """Écran de démarrage - Choisir nouveau jeu ou charger"""
    # Choix de la langue au lancement
    global LANG
    try:
        lang_choice = input("Choisir la langue / Choose language (fr/en) [fr]: ").strip().lower()
        if lang_choice.startswith('en'):
            LANG = 'en'
    except Exception:
        pass

    print("\n" + "="*50)
    print(tr("BIENVENUE DANS RPG.txt"))
    print("="*50)
    
    sauvegardes = lister_sauvegardes()
    
    if sauvegardes:
        print("\n1. Nouveau jeu")
        print("2. Charger une sauvegarde")
        choix = tinput("Choisir (1 ou 2) : ").strip()
        
        if choix == "2":
            print("\nSauvegardes disponibles:")
            for i, save in enumerate(sauvegardes, 1):
                print(f"  {i}. {save}")
            try:
                choix_save = int(tinput("Quelle sauvegarde charger? (numéro) : "))
                if 1 <= choix_save <= len(sauvegardes):
                    joueur = charger_jeu(sauvegardes[choix_save - 1])
                    if joueur:
                        menu_principal(joueur)
                    return
                else:
                    print(tr("Choix invalide!"))
            except ValueError:
                print(tr("Entrée invalide!"))
    
    joueur = Personnage("Héros", 100, 15, 5, pv_max=100)
    joueur.loot("Or", 10)  # or de départ
    menu_principal(joueur)

if __name__ == "__main__":
    launcher()
