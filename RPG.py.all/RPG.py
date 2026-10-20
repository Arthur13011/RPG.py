
# Licensed under CC BY-ND 4.0
# You may use and share this code, but you may not modify it.

# -*- coding: utf-8 -*-
import random
import sys
import webbrowser
import time
import json
import os
# Langue par défaut ("fr" ou "en") carte
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
    "  Tu voyages vers le {direction}...": "  You travel to the {direction}...",
    "Bienvenue à {destination}!": "Welcome to {destination}!",
    "Sauvegarde créée: {name}": "Save created: {name}",
    "Sauvegarde '{name}' non trouvée!": "Save '{name}' not found!",
    "Veux-tu recommencer ? (oui/non) : ": "Do you want to restart? (yes/no): ",
    "Le jeu se fermera dans 5 secondes...": "The game will close in 5 seconds...",
    "rejoignez-nous sur Discord pour plus de contenu et d'aide : {url}": "join us on Discord for more content and help: {url}",
    "Il n'y a pas de chemin vers cette destination depuis ici.": "There is no path to that destination from here.",
    "Rejoignez ma communauté sur Reddit : {url}": "Join my community on Reddit: {url}",
    "Choix invalide. Réponds par oui ou non.": "Invalid choice. Answer yes or no.",
    "Choix invalide.": "Invalid choice.",
    "Achat effectué!": "Purchase complete!",
    "Quête : {name} | Objectif : {target} ({state})": "Quest: {name} | Objective: {target} ({state})",
    "1. Nouveau jeu": "1. New game",
    "2. Charger une sauvegarde": "2. Load save",
    "1. Combattre un ennemi": "1. Fight an enemy",
    "2. Affronter un boss (si disponible)": "2. Face a boss (if available)",
    "3. Affronter le SUPERBOSS": "3. Face the SUPERBOSS",
    "4. Voir inventaire": "4. View inventory",
    "5. Voir quête active": "5. View active quest",
    "6. Voir la carte": "6. View map",
    "7. Voyager vers une autre région": "7. Travel to another region",
    "8. Sauvegarder la progression": "8. Save progress",
    "9. Quitter": "9. Quit",
    "10. Interagir avec les habitants (en devloppement)": "10. Interact with the locals (in development)",
    "Objet invalide ou indisponible.": "Invalid or unavailable item.",
    "Action invalide, tu perds ton tour.": "Invalid action, you lose your turn.",
    "le jeu se fermera dans 5 secondes...": "The game will close in 5 seconds...",
    "Un combat commence contre {enn} !": "A battle begins against {enn}!",
    "Choisis ton action (a=attaque, e=inventaire, d=dodge, u=objet, r=repos, f=fuite, end=fin) : ": "Choose your action (a=attack, e=inventory, d=dodge, u=item, r=rest, f=flee, end=quit): ",
    "Inventaire :": "Inventory:",
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
    "Tape un chiffre (1-11) : ": "Type a number (1-11): ",
    "11. Fabriquer un objet": "11. Craft an item",
    "Que veux-tu fabriquer ?": "What would you like to craft?",
    "Fabriquer un arc (3 ficelles)": "Craft a bow (3 String)",
    "Fabriquer une dague (3 barres d'acier, 1 lanière de cuir, 1 marteau)": "Craft a dagger (3 Steel Rods, 1 Leather Strap, 1 Hammer)",
    "Pas assez de ficelle pour fabriquer un arc (3 requis).": "Not enough string to craft a bow (3 required).",
    "Arc fabriqué ! Il inflige +5 dégâts.": "Bow crafted! It adds +5 damage.",
    "Il faut 3 barres d'acier, 1 lanière de cuir et 1 marteau pour fabriquer une dague.": "You need 3 Steel Rods, 1 Leather Strap, and 1 Hammer to craft a dagger.",
    "Dague fabriquée ! Elle inflige +2 dégâts. Le marteau est rendu.": "Dagger crafted! It adds +2 damage. The Hammer is returned.",
    "Fabriquer une épée longue (10 barres d'acier, 2 lanières de cuir, 1 marteau, 1 joyau du Dragon)": "Craft a longsword (10 Steel Rods, 2 Leather Straps, 1 Hammer, 1 Dragon Jewel)",
    "Il faut 10 barres d'acier, 2 lanières de cuir, 1 marteau et 1 joyau du Dragon.": "You need 10 Steel Rods, 2 Leather Straps, 1 Hammer, and 1 Dragon Jewel.",
    "Épée longue fabriquée ! Elle inflige +7 dégâts. Le marteau est rendu.": "Longsword crafted! It adds +7 damage. The Hammer is returned.",
    "Fabriquer {item} ({ingredients})": "Craft {item} ({ingredients})",
    "Il manque des matériaux pour fabriquer {item}.": "Not enough materials to craft {item}.",
    "{item} fabriqué ! Bonus de dégâts : +{damage}.": "{item} crafted! Damage bonus: +{damage}.",
    "Il ne te reste plus de flèches pour tirer avec l'arc.": "You have no arrows left to shoot the bow.",
    "Choix invalide": "Invalid choice",
    "Aucun ennemi disponible ici!": "No enemy available here!",
    "Aucun boss disponible ici!": "No boss available here!",
    "Aucune quête active.": "No active quest.",
    "Aucune destination accessible!": "No accessible destinations!",
    "Nom de la sauvegarde (défaut: 'save') : ": "Save name (default: 'save'): ",
    "Fin de la partie.": "End of the game.",
    "BIENVENUE DANS RPG.txt": "WELCOME TO RPG.txt",
    "Choisir (1 ou 2) : ": "Choose (1 or 2): ",
    "Choisir la langue / Choose language (fr/en) [fr]: ": "Choose language / Choisir la langue (fr/en) [fr]: ",
    "Sauvegardes disponibles:": "Available saves:",
    "Quelle sauvegarde charger? (numéro) : ": "Which save to load? (number): ",
    "1. Nouveau jeu": "1. New game",
    "2. Charger une sauvegarde": "2. Load save",
    "Merci d'avoir joué !": "Thanks for playing!",
    "Tu ne peux pas aller dans cette direction!": "You can't go that way!",
    "Choisir une destination (numéro) : ": "Choose a destination (number): ",
    "Choix invalide!": "Invalid choice!",
    "Entrée invalide!": "Invalid input!",
    "10. Interagir avec les habitants (en devloppement)": "10. Interact with the locals (in development)",
    "Aucun PNJ disponible ici!": "No NPCs available here!",
    "Choisir un habitant (numéro) : ": "Choose a villager (number): ",
    "Choisir un PNJ (numéro) : ": "Choose an NPC (number): ",
    # NPC Dialogues
    "Bienvenue à la taverne! Que puis-je vous servir?": "Welcome to the tavern! What can I get for you?",
    "1. Boire une bière (5 pièces d'or) - Restaure 10 PV": "1. Have a beer (5 gold) - Restores 10 HP",
    "2. Manger un peu de pain (5 pièces d'or) - Restaure 10 PV": "2. Eat some bread (5 gold) - Restores 10 HP",
    "3. Demander des informations sur la région": "3. Ask for information about the region",
    "4. Dormir à l'auberge (100% PV, sauvegarde auto)": "4. Sleep at the inn (100% HP, auto-save)",
    "0. Partir": "0. Leave",
    "Vous vous sentez revigoré! +10 PV": "You feel refreshed! +10 HP",
    "Tu n'as pas assez d'or!": "You don't have enough gold!",
    "Le vin vous revigore complètement! +25 PV": "The wine fully restores you! +25 HP",
    "Le tavernier vous raconte des histoires sur les monstres des environs...": "The innkeeper tells you stories about the monsters nearby...",
    "- La forêt est infestée de plantes carnivores et de spectres": "- The forest is infested with carnivorous plants and specters",
    "- Le château abrite des vampires et des sorciers corrompus": "- The castle is home to vampires and corrupted sorcerers",
    "- Le marais maudit est le domaine du Roi du Marais": "- The cursed swamp is the domain of the Swamp King",
    "- Et attention au Tyran de Feu dans le volcan!": "- And beware the Fire Tyrant in the volcano!",
    "Tu as dormi à l'auberge : PV restaurés et sauvegarde automatique.": "You slept at the inn: HP restored and auto-saved.",
    "{name} obtient : {item} x{qty} {stars}": "{name} gains: {item} x{qty} {stars}",
    "Nouvelle quête : {quest} (objectif : {qty} {target})": "New quest: {quest} (objective: {qty} {target})",
    "Quête terminée : {name}": "Quest completed: {name}",
    "Votre choix : ": "Your choice: ",
    "Bienvenue chez l'apothicaire! J'ai les meilleures potions de la région.": "Welcome to the apothecary! I have the best potions in the region.",
    "1. Acheter une potion (5 pièces d'or)": "1. Buy a potion (5 gold)",
    "2. Acheter un élixir (15 pièces d'or)": "2. Buy an elixir (15 gold)",
    "3. Acheter une potion de soin supérieure (25 pièces d'or) - Restaure 50 PV": "3. Buy a superior healing potion (25 gold) - Restores 50 HP",
    "Vous avez acheté une potion!": "You bought a potion!",
    "Vous avez acheté un élixir!": "You bought an elixir!",
    "Vous avez acheté une potion de soin supérieure!": "You bought a superior healing potion!",
    "Bonjour {player.name()}!": "Hello, {player.name()}!",
    "Voici ce que j'ai en stock:": "Here is what I have in stock:",
    "Prix: {price} or": "Price: {price} gold",
    "Que veux-tu acheter? (numéro ou 0 pour quitter) : ": "What do you want to buy? (number or 0 to quit): ",
    "Achat effectué!": "Purchase complete!",
    "Objet invalide!": "Invalid item!",
    "Bienvenue chez le forgeron! J'améliore vos armes et armures.": "Welcome to the blacksmith! I improve your weapons and armor.",
    "1. Améliorer l'attaque (+2 ATK, 20 or)": "1. Improve attack (+2 ATK, 20 gold)",
    "2. Améliorer la défense (+1 DEF, 15 or)": "2. Improve defense (+1 DEF, 15 gold)",
    "Votre attaque a été améliorée! +2 ATK": "Your attack has been improved! +2 ATK",
    "Votre défense a été améliorée! +1 DEF": "Your defense has been improved! +1 DEF",
    "Bienvenue à l'auberge! Reposez-vous ici.": "Welcome to the inn! Rest here.",
    "1. Dormir (restaure 50% PV, 10 or)": "1. Sleep (restores 50% HP, 10 gold)",
    "2. Dormir complètement (100% PV, 20 or)": "2. Sleep completely (100% HP, 20 gold)",
    "Vous vous reposez. +50% PV": "You rest. +50% HP",
    "Vous dormez complètement. PV restaurés.": "You sleep completely. HP restored.",
    "Les étoiles me parlent... Que cherchez-vous?": "The stars speak to me... What are you looking for?",
    "1. Conseil sur la quête (+ indice)": "1. Quest advice (+ hint)",
    "2. Bénédiction (+5 PV max temporaire, 30 or)": "2. Blessing (+5 max HP temporary, 30 gold)",
    "Votre quête vous mènera vers {cible}. Soyez prudent.": "Your quest will lead you to {cible}. Be careful.",
    "Vous n'avez pas de quête active.": "You have no active quest.",
    "Vous recevez une bénédiction! +5 PV max": "You receive a blessing! +5 max HP",
    "Psst... Besoin d'aide discrète?": "Psst... Need discreet help?",
    "1. Vendre un objet volé (double prix)": "1. Sell a stolen item (double price)",
    "2. Quête secondaire : Voler un objet (récompense 50 or)": "2. Side quest: Steal an item (reward 50 gold)",
    "Quel objet vendez-vous? (nom exact)": "What item are you selling? (exact name)",
    "Objet : ": "Item: ",
    "Vendu pour {prix} or!": "Sold for {prix} gold!",
    "Objet non trouvé.": "Item not found.",
    "Quête acceptée : Volez une potion au vendeur. Revenez avec.": "Quest accepted: Steal a potion from the seller. Come back with it.",
    "Quête terminée! +50 or": "Quest completed! +50 gold",
    "Bienvenue dans ma bibliothèque. La connaissance est pouvoir.": "Welcome to my library. Knowledge is power.",
    "1. Acheter un livre de sagesse (+10 XP, 25 or)": "1. Buy a book of wisdom (+10 XP, 25 gold)",
    "2. Histoire du monde": "2. History of the world",
    "Vous apprenez de nouvelles choses! +10 XP": "You learn new things! +10 XP",
    "Il y a longtemps, le monde était en paix... Mais les dragons ont apporté le chaos.": "Long ago, the world was at peace... But dragons brought chaos.",
    "{name} gagne {amount} XP (total: {total}).": "{name} gains {amount} XP (total: {total}).",
    "{name} monte au niveau {level} ! ATK+2, DEF+1, PVmax+10.": "{name} reaches level {level}! ATK +2, DEF +1, HP max +10.",
    "Progression XP: {current}/{required} vers le niveau {next_level}.": "XP progress: {current}/{required} toward level {next_level}.",
    "{name} souffre du poison (-3 PV).": "{name} suffers from poison (-3 HP).",
    "{name} est brûlé (-2 PV).": "{name} is burned (-2 HP).",
    "\n{name} : {hp}/{maxhp} PV | ATK {atk} | DEF {defn}": "\n{name} : {hp}/{maxhp} HP | ATK {atk} | DEF {defn}",
    "{name} est étourdi et ne peut pas agir ce tour !": "{name} is stunned and cannot act this turn!",
    "Choisis ton action (a=attaque, e=inventaire, d=dodge, u=objet, r=repos, f=fuite, end=fin) : ": "Choose your action (a=attack, e=inventory, d=dodge, u=item, r=rest, f=flee, end=quit): ",
    "Fin de la partie.": "End of the game.",
    "Inventaire :": "Inventory:",
    "{name} tente d'esquiver...": "{name} tries to dodge...",
    "Esquive réussie ! Aucun dégât subi ce tour.": "Dodge successful! No damage taken this turn.",
    "Esquive ratée !": "Dodge failed!",
    "Quel objet veux-tu utiliser ? ": "Which item do you want to use? ",
    "{name} utilise une Potion (+20 PV).": "{name} uses a Potion (+20 HP).",
    "{name} utilise un Élixir (+5 ATK).": "{name} uses an Elixir (+5 ATK).",
    "Objet invalide ou indisponible.": "Invalid or unavailable item.",
    "{name} se repose et récupère {heal} PV.": "{name} rests and recovers {heal} HP.",
    "{name} réussit à fuir le combat !": "{name} successfully escapes the fight!",
    "Fuite ratée !": "Escape failed!",
    "Action invalide, tu perds ton tour.": "Invalid action, you lose your turn.",
    "{name} mord {target}, inflige {damage} dégâts et récupère {heal} PV !": "{name} bites {target}, deals {damage} damage and recovers {heal} HP!",
    "{name} devient intangible et évite d'attaquer frontalement ce tour.": "{name} becomes intangible and avoids attacking head-on this turn.",
    "{name} empoisonne {target} ! Poison pendant 3 tours (dégâts subis: {damage}).": "{name} poisons {target}! Poison for 3 turns (damage taken: {damage}).",
    "{name} brûle {target} ! Brûlure pendant 3 tours (dégâts subis: {damage}).": "{name} burns {target}! Burning for 3 turns (damage taken: {damage}).",
    "{name} étourdit {target} ! Tu perdras ton prochain tour.": "{name} stuns {target}! You will lose your next turn.",
    "{name} frappe brutalement, ignore une partie de la DEF et inflige {damage} dégâts.": "{name} strikes brutally, bypasses part of the DEF and deals {damage} damage.",
    "{name} réussit une attaque critique !": "{name} lands a critical hit!",
    "{name} attaque {target} et inflige {degats} dégâts.": "{name} attacks {target} and deals {degats} damage.",
    "{name} attaque et inflige {damage} dégâts.": "{name} attacks and deals {damage} damage.",
    "{name} charge avec rage et inflige {damage} dégâts !": "{name} charges with rage and deals {damage} damage!",
    "{name} écrase et éclabousse : {damage}+{splash} dégâts.": "{name} crushes and splashes: {damage}+{splash} damage.",
    "{name} lance un sort de feu : {damage} dégâts et brûlure (2 tours).": "{name} casts a fire spell: {damage} damage and burning (2 turns).",
    "{name} gèle {target} : {damage} dégâts et étourdissement.": "{name} freezes {target}: {damage} damage and stun.",
    "{name} invoque les ombres et inflige {damage} dégâts occultes.": "{name} summons shadows and deals {damage} occult damage.",
    "{name} a vaincu {target} !": "{name} defeats {target}!",
    "Victoire. . .": "Victory...",
    "Victoire contre un Boss !": "Victory over a Boss!",
    "Victoire contre un Mini-boss !": "Victory over a Mini-boss!",
    "Victoire contre un ennemi classique.": "Victory over a regular enemy.",
    "{name} a été vaincu par {target}...": "{name} has been defeated by {target}...",
    "Héros": "Hero",
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
    time.sleep(0.05)

def tinput(prompt, **kwargs):
    """Input with translated prompt."""
    return input(tr(prompt, **kwargs))

def tprints(*lines):
    for line in lines:
        tprint(line)

def choose_int(prompt, minval=0, maxval=None):
    try:
        valeur = int(tinput(prompt))
        return valeur if (maxval is None or minval <= valeur <= maxval) else None
    except ValueError:
        return None

def can_pay(joueur, montant):
    return joueur.inventaire.get("Or", 0) >= montant

def spend(joueur, montant):
    if not can_pay(joueur, montant):
        tprint("Tu n'as pas assez d'or!")
        return False
    joueur.inventaire["Or"] -= montant
    return True

def service_menu(joueur, title, options):
    tprint(tr(title))
    for i, (label, action) in enumerate(options, 1):
        tprint(f"{i}. {tr(label)}")
    tprint(tr("0. Partir"))
    choix = choose_int(tr("Votre choix : "), 0, len(options))
    if choix is None:
        tprint(tr("Entrée invalide!"))
        return
    if choix == 0:
        return
    options[choix - 1][1]()

# Traductions de noms (ennemis, objets, lieux, quêtes)
NAME_TRANSLATIONS_EN = {
    # Personnages / personnages
    "Héros": "Hero",

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
    "Capitaine Noir": "Dark Captain",
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
    "Bâton": "Stick",
    "Dague": "Dagger",
    "Ficelle": "String",
    "Flèche": "Arrow",
    "Bout d'acier": "Steel Bit",
    "Arc": "Bow",
    "Barre d'acier": "Steel Rod",
    "Lanière de cuir": "Leather Strap",
    "Marteau": "Hammer",
    "Joyau du Dragon": "Dragon Jewel",
    "Épée longue": "Longsword",
    "Dragon enflammé": "Flaming Dragon",

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
    "Trouver une piece d'or": "Find a Gold Piece",
    "Trouver un grimoire ancien": "Find an Ancient Grimoire",
    "Vaincre le dragon ancien": "Defeat the Ancient Dragon",
    "Vaincre le Tyran de Feu": "Defeat the Fire Tyrant",
    "Vaincre le Roi du Marais": "Defeat the Swamp King",

    # PNJs
    "Tavernier du village": "Village Tavern Keeper",
    "Vendeur de potions": "Potion Seller",
    "Marchand": "Merchant",
    "Forgeron": "Blacksmith",
    "Aubergiste": "Innkeeper",
    "Mystique": "Mystic",
    "Contact de la Guilde des Voleurs": "Thieves' Guild Contact",
    "Savant": "Scholar",
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
        "locked": False,
        "npcs": ["Tavernier du village", "Vendeur de potions", "Marchand", "Forgeron", "Aubergiste", "Mystique", "Contact de la Guilde des Voleurs", "Savant"]
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
        "boss": (("Tyran de Feu", 140, 26, 10), ("Dragon enflammé", 150, 25, 11)),
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
    tprints(
        "\n" + "="*60,
        tr("CARTE DU MONDE"),
        "="*60,
    )

    positions = MAP_POSITIONS
    largeur = MAP_WIDTH
    hauteur = MAP_HEIGHT
    grille = [['.' for _ in range(largeur)] for _ in range(hauteur)]

    for lieu, (x, y) in positions.items():
        if y < hauteur and x < largeur:
            codes = {
                "Tour Interdite": ['T', 'I'],
                "Chambre du Trésor": ['C', 'T'],
                "Village": ['V', 'L'],
                "Château": ['C', 'H'],
                "Marais Maudit": ['M', 'M'],
                "Volcan de Feu": ['V', 'F'],
                "Forêt": ['F', 'R'],
                "Souterrain": ['S', 'T'],
            }
            grille[y][x:x+2] = codes.get(lieu, ['?', '?'])

    if joueur.localisation in positions:
        px, py = positions[joueur.localisation]
        if py < hauteur and px < largeur:
            grille[py][px] = '@'

    for ligne in grille:
        print(''.join(ligne))
        time.sleep(0.05)

    tprints(
        "\n" + "-"*60,
        tr("Légende:"),
        tr("  @ = Ta position"),
        tr("  VI = Village | FR = Forêt | ST = Souterrain"),
        tr("  CH = Château | MM = Marais Maudit | VF = Volcan de Feu"),
        tr("  TI = Tour Interdite | CT = Chambre du Trésor"),
        "-"*60,
    )

    if joueur.localisation in locations:
        lieu = locations[joueur.localisation]
        tprint(tr("\n{loc}", loc=name_tr(joueur.localisation)))
        tprint(f"   {desc_tr(lieu['description'])}")
        tprint(tr("\n   Connexions:"))
        for destination, direction in lieu["connections"].items():
            locked_str = " [LOCKED]" if locations[destination].get("locked") else ""
            tprint("     • {dest} ({dir}){locked}", dest=name_tr(destination), dir=direction, locked=locked_str)
    tprint("="*60 + "\n")

def voyager(joueur, destination):
    if joueur.localisation not in locations:
        tprint("Erreur: localisation inconnue!")
        return False

    lieu_actuel = locations[joueur.localisation]
    if destination not in lieu_actuel["connections"]:
        tprint(tr("Il n'y a pas de chemin vers cette destination depuis ici."))
        return False

    if locations[destination].get("locked"):
        item_req, quantite_req = locations[destination].get("requirement")
        quantite_possedee = joueur.inventaire.get(item_req, 0)
        if quantite_possedee < quantite_req:
            tprint("\nCette porte est verrouillée!")
            tprint("Tu as besoin de {quant} {item}(s) pour l'ouvrir.", quant=quantite_req, item=item_req)
            tprint("Tu en possèdes: {have}/{need}", have=quantite_possedee, need=quantite_req)
            return False
        joueur.inventaire[item_req] -= quantite_req
        tprint("\nTu utilises {quant} {item}(s) pour ouvrir la porte!", quant=quantite_req, item=item_req)

    direction = lieu_actuel["connections"][destination]
    joueur.localisation = destination
    joueur.last_spawned_enemy = None
    tprint("\n  Tu voyages vers le {direction}...", direction=direction)
    tprint("Bienvenue à {destination}!", destination=destination)
    afficher_carte(joueur)
    return True
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
        "defeated_bosses": joueur.defeated_bosses,
        "quete": {
            "nom": joueur.quete.nom if joueur.quete else None,
            "progression": joueur.quete.progression if joueur.quete else 0,
            "terminee": joueur.quete.terminee if joueur.quete else False
        }
    }
    
    chemin_fichier = os.path.join(SAVE_DIR, f"{nom_sauvegarde}.json")
    with open(chemin_fichier, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)
    tprint(tr("Sauvegarde créée: {name}", name=nom_sauvegarde))

def charger_jeu(nom_sauvegarde="save"):
    """Charge la progression du joueur"""
    chemin_fichier = os.path.join(SAVE_DIR, f"{nom_sauvegarde}.json")
    
    if not os.path.exists(chemin_fichier):
        tprint(tr("Sauvegarde '{name}' non trouvée!", name=nom_sauvegarde))
        return None
    
    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        donnees = json.load(f)
    
    joueur = Personnage(donnees["nom"], donnees["pv"], donnees["attaque"], donnees["defense"], donnees["pv_max"])
    joueur.pv = donnees["pv"]
    joueur.inventaire = donnees["inventaire"]
    joueur.xp = donnees["xp"]
    joueur.niveau = donnees["niveau"]
    joueur.localisation = donnees["localisation"]
    joueur.defeated_bosses = donnees.get("defeated_bosses", [])
    
    # Recréer la quête si elle existe
    if donnees["quete"]["nom"]:
        quete_data = next((q for q in quetes_possibles if q["nom"] == donnees["quete"]["nom"]), None)
        if quete_data:
            joueur.quete = Quete(quete_data["nom"], quete_data["objectif"], quete_data["recompense"])
            joueur.quete.progression = donnees["quete"]["progression"]
            joueur.quete.terminee = donnees["quete"]["terminee"]
    
    tprint(f"Sauvegarde chargée: {nom_sauvegarde}")
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
            break  # on sort de la boucle après relance
        elif choix == "non":
            tprint(tr("Le jeu se fermera dans 5 secondes..."))
            time.sleep(5)
            tprint(tr("rejoignez-nous sur Discord pour plus de contenu et d'aide : {url}", url="https://discord.gg/8CmNRjJHnk"))
            sys.exit()
        else:
            tprint(tr("Choix invalide. Réponds par oui ou non."))
# --- Définition des raretés ---
raretes = {
    "Potion": "★",
    "Épée magique": "★★",
    "Bouclier": "★★",
    "Anneau de Force": "★★★",
    "Cape d'Invisibilité": "★★★",
    "Grimoire ancien": "★★★",
    "Amulette de Vie": "★★★",
    "Couronne des Ombres": "★★★",
    "Écaille du Dragon Ancien": "★★★",
    "Clé Mystique": "",
    "Bâton": "",
    "Dague": "★",
    "Ficelle": "",
    "Arc": "★★",
    "Barre d'acier": "",
    "Lanière de cuir": "",
    "Marteau": "",
    "Joyau du Dragon": "★★★",
    "Épée longue": "★★★",
    "Flèche": "",
    "Bout d'acier": "",
    "Or": "",
}

CRAFTING_RECIPES = {
    "bow_recipe": {"Ficelle": 3},
    "dagger_recipe": {"Barre d'acier": 3, "Lanière de cuir": 1, "Marteau": 1},
    "longsword_recipe": {
        "Barre d'acier": 10,
        "Lanière de cuir": 2,
        "Marteau": 1,
        "Joyau du Dragon": 1,
    },
    "arrow_recipe": {"Bout d'acier": 1, "Ficelle": 1},
    "metal_bit_recipe": {"Barre d'acier": 1, "Marteau": 1},
}

ITEM_DATA = {
    item: {"canCraftItem": False, "canCraftWith": None, "damageBonus": 0, "craftQuantity": 1}
    for item in raretes
}
ITEM_DATA.update({
    "Arc": {
        "canCraftItem": True,
        "canCraftWith": "bow_recipe",
        "damageBonus": 5,
    },
    "Dague": {
        "canCraftItem": True,
        "canCraftWith": "dagger_recipe",
        "damageBonus": 2,
    },
    "Épée longue": {
        "canCraftItem": True,
        "canCraftWith": "longsword_recipe",
        "damageBonus": 7,
    },
    "Flèche": {
        "canCraftItem": True,
        "canCraftWith": "arrow_recipe",
        "damageBonus": 0,
    },
    "Bout d'acier": {
        "canCraftItem": True,
        "canCraftWith": "metal_bit_recipe",
        "damageBonus": 0,
        "craftQuantity": 60,
    },

})
REUSABLE_CRAFTING_TOOLS = {"Marteau"}

ENEMY_LOOT_TABLES = {
    "Gobelin": (("Potion", 0.25), ("Dague", 0.20), ("Lanière de cuir", 0.10)),
    "Plante carnivore": (("Potion", 0.20),),
    "Squelette": (("Potion", 0.15), ("Élixir", 0.05), ("Marteau", 0.05), ("Flèche", 0.40), ("Bout d'acier", 0.20)),
    "Dragonnet": (("Élixir", 0.25),),
    "Bandit": (("Potion", 0.20), ("Lanière de cuir", 0.20), ("Barre d'acier", 0.15)),
    "Slime géant": (("Potion", 0.20)),
    "Spectre": (("Élixir", 0.20),),
    "Minotaure": (("Élixir", 0.25),),
    "Harpie": (("Potion", 0.15),),
    "Golem de pierre": (("Bouclier", 0.12), ("Épée magique", 0.08)),
    "Vampire": (("Potion", 0.15), ("Élixir", 0.15)),
    "Sorcier corrompu": (("Élixir", 0.20), ("Grimoire ancien", 0.05)),
    "Chef Bandit": (("Épée magique", 0.10),),
    "Esprit Ancien": (("Grimoire ancien", 0.10),),
    "Garde Souterrain": (("Bouclier", 0.10),),
    "Capitaine Noir": (("Épée magique", 0.10),),
    "Traqueur du Marais": (("Amulette de Vie", 0.10),),
    "Géant de Magma": (("Écaille du Dragon Ancien", 0.10),),
    "Magicien Maudit": (("Grimoire ancien", 0.10),),
    "Reine Araignée": (("Anneau de Force", 0.15), ("Ficelle", 0.50)),
    "Dragon Ancien": (("Écaille du Dragon Ancien", 0.20),),
    "Tyran de Feu": (("Écaille du Dragon Ancien", 0.25),),
    "Dragon enflammé": (("Joyau du Dragon", 1.0),),
    "Seigneur des Ombres": (("Couronne des Ombres", 0.15),),
    "Roi du Marais": (("Amulette de Vie", 0.20),),
    "Le Sorcier Immortel": (("Couronne des Ombres", 0.50),),
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
    __slots__ = ('nom', 'pv_max', 'pv', 'attaque', 'defense', 'inventaire', 'xp', 'niveau', 'quete', 'localisation', 'last_spawned_enemy', 'loot_table', 'defeated_bosses')
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
        self.defeated_bosses = []
        base_name = nom.partition(" (Élite)")[0]
        self.loot_table = ENEMY_LOOT_TABLES.get(base_name, ())

    def est_vivant(self):
        return self.pv > 0

    def name(self):
        return self.nom

    def subir_degats(self, degats):
        self.pv -= degats
        if self.pv < 0:
            self.pv = 0

    def attaquer(self, cible):
        armes_possedees = [
            (item, item_data["damageBonus"])
            for item, item_data in ITEM_DATA.items()
            if item_data["damageBonus"] > 0 and self.inventaire.get(item, 0) > 0
        ]
        arme, bonus_arme = max(armes_possedees, key=lambda entry: entry[1], default=(None, 0))
        if arme == "Arc":
            if self.inventaire.get("Flèche", 0) < 1:
                tprint(tr("Il ne te reste plus de flèches pour tirer avec l'arc."))
                return
            self.inventaire["Flèche"] -= 1

        degats = max(1, self.attaque + bonus_arme - cible.defense)  # minimum 1 dégât
        cible.subir_degats(degats)
        tprint("{name} attaque {target} et inflige {degats} dégâts.", name=name_tr(self.nom), target=name_tr(cible.nom), degats=degats)
        time.sleep(0.05)

    def loot(self, objet, quantite=1):
        self.inventaire[objet] = self.inventaire.get(objet, 0) + quantite
        etoiles = raretes.get(objet, "")
        tprint("{name} obtient : {item} x{qty} {stars}", name=name_tr(self.nom), item=name_tr(objet), qty=quantite, stars=etoiles)
        time.sleep(0.05)
        verifier_quete(self, loot=objet)

    def gagner_xp(self, montant):
        # Ajoute l'XP et applique la courbe de leveling (peut monter plusieurs niveaux)
        self.xp += montant
        print(tr("{name} gagne {amount} XP (total: {total}).", name=name_tr(self.nom), amount=montant, total=self.xp))
        time.sleep(0.05)

        leveled = False
        # Tant que l'XP totale dépasse le palier du niveau suivant, on monte
        while self.xp >= total_xp_for_level(self.niveau + 1):
            self.niveau += 1
            self.attaque += 2
            self.defense += 1
            self.pv_max += 10
            self.pv = self.pv_max
            print(tr("{name} monte au niveau {level} ! ATK+2, DEF+1, PVmax+10.", name=name_tr(self.nom), level=self.niveau))
            time.sleep(0.05)
            leveled = True

        if not leveled:
            current_into_level = self.xp - total_xp_for_level(self.niveau)
            required = total_xp_for_level(self.niveau + 1) - total_xp_for_level(self.niveau)
            print(tr("Progression XP: {current}/{required} vers le niveau {next_level}.", current=current_into_level, required=required, next_level=self.niveau + 1))
            time.sleep(0.05)

# --- Quêtes ---
quetes_possibles = [
    {"nom": "Chasser les gobelins", "objectif": ("Gobelin", 3), "recompense": ("Or", 30)},
    {"nom": "Trouver une piece d'or", "objectif": ("Or", 1), "recompense": ("XP", 5)},
    {"nom": "Vaincre le dragon ancien", "objectif": ("Dragon Ancien", 1), "recompense": ("Cape d'Invisibilité", 1)},
    {"nom": "Vaincre le Roi du Marais", "objectif": ("Roi du Marais", 1), "recompense": ("Amulette de Vie", 1)},
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
            tprint("Quête terminée : {name}", name=self.nom)
            time.sleep(0.05)
            return self.recompense
        return None

def donner_quete(joueur):
    quete_data = random.choice(quetes_possibles)
    quete = Quete(quete_data["nom"], quete_data["objectif"], quete_data["recompense"])
    joueur.quete = quete
    tprint("Nouvelle quête : {quest} (objectif : {qty} {target})", quest=name_tr(quete.nom), qty=quete.quantite, target=name_tr(quete.cible))

def verifier_quete(joueur, ennemi=None, loot=None):
    """Check and advance the player's active quest when they defeat an enemy or obtain loot.

    If the quest completes, apply the reward to the player.
    """
    if not joueur or not getattr(joueur, 'quete', None):
        return None
    if joueur.quete.terminee:
        return None

    recompense = joueur.quete.avancer(ennemi, loot)
    if recompense:
        type_r, valeur = recompense
        if type_r == "XP":
            joueur.gagner_xp(valeur)
        elif type_r == "Or":
            joueur.loot("Or", valeur)
        else:
            joueur.loot(type_r, valeur)
        return recompense
    return None

# --- Bosses ---
boss_possibles = [
    ("Dragon Ancien", 120, 25, 8),
    ("Seigneur des Ombres", 100, 20, 10),
    ("Reine Araignée", 100, 15, 7),
    ("Tyran de Feu", 140, 26, 10),
    ("Dragon enflammé", 150, 25, 11)
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
