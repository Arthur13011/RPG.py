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
    "Tape un chiffre (1-12) : ": "Type a number (1-12): ",
    "11. Fabriquer un objet": "11. Craft an item",
    "12. Voir les succès": "12. View achievements",
    "=== SUCCÈS ===": "=== ACHIEVEMENTS ===",
    "Succès débloqué : {name} !": "Achievement unlocked: {name}!",
    "Succès : {unlocked}/{total}": "Achievements: {unlocked}/{total}",
    "[Débloqué] {name} - {description}": "[Unlocked] {name} - {description}",
    "[Verrouillé] {name} - {description}": "[Locked] {name} - {description}",
    "Première victoire": "First Victory",
    "Gagne ton premier combat.": "Win your first battle.",
    "Chasseur de boss": "Boss Hunter",
    "Vaincs un boss.": "Defeat a boss.",
    "Tueur de dragon": "Dragon Slayer",
    "Vaincs le Dragon enflammé.": "Defeat the Flaming Dragon.",
    "Niveau 5": "Level 5",
    "Atteins le niveau 5.": "Reach level 5.",
    "Artisan": "Craftsperson",
    "Fabrique ton premier objet.": "Craft your first item.",
    "Archer": "Archer",
    "Tire une flèche avec un arc.": "Shoot an arrow with a Bow.",
    "Haha very funny": "Haha, very funny.",
    "\n{loc}": "\n{loc}",
    "\n   Connexions:": "\n   Connections:",
    "     • {dest} ({dir}){locked}": "     • {dest} ({dir}){locked}",
    "\nCette porte est verrouillée!": "\nThis door is locked!",
    "\nTu utilises {quant} {item}(s) pour ouvrir la porte!": "\nYou use {quant} {item}(s) to open the door!",
    "\n  Tu voyages vers le {direction}...": "\n  You travel to the {direction}...",
    "nord": "north",
    "sud": "south",
    "est": "east",
    "ouest": "west",
    " [Verrouillé]": " [LOCKED]",
    "Sauvegarde chargée: {name}": "Save loaded: {name}",
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
    "\nSauvegardes disponibles:": "\nAvailable saves:",
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
    "Boire une bière (5 pièces d'or) - Restaure 10 PV": "Have a beer (5 gold) - Restores 10 HP",
    "Manger un peu de pain (5 pièces d'or) - Restaure 10 PV": "Eat some bread (5 gold) - Restores 10 HP",
    "Demander des informations sur la région": "Ask for information about the region",
    "Dormir à l'auberge (100% PV, sauvegarde auto)": "Sleep at the inn (100% HP, auto-save)",
    "Bienvenue chez le marchand! Voici ce que j'ai en stock:": "Welcome to the merchant! Here's what I have in stock:",
    "Améliorer l'attaque (+2 ATK, 20 or)": "Improve attack (+2 ATK, 20 gold)",
    "Améliorer la défense (+1 DEF, 15 or)": "Improve defense (+1 DEF, 15 gold)",
    "Dormir (restaure 50% PV, 10 or)": "Sleep (restores 50% HP, 10 gold)",
    "Dormir complètement (100% PV, 20 or)": "Sleep fully (100% HP, 20 gold)",
    "Conseil sur la quête (+ indice)": "Quest advice (+ hint)",
    "Bénédiction (+5 PV max temporaire, 30 or)": "Blessing (+5 temporary max HP, 30 gold)",
    "Vendre un objet volé (double prix)": "Sell a stolen item (double price)",
    "Quête secondaire : Voler un objet (récompense 50 or)": "Side quest: Steal an item (50 gold reward)",
    "Acheter un livre de sagesse (+10 XP, 25 or)": "Buy a book of wisdom (+10 XP, 25 gold)",
    "Histoire du monde": "World history",
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
    "Potion supérieure": "Superior Potion",
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
    "Bout d'acier": "Steel Tip",
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
            locked_str = tr(" [Verrouillé]") if locations[destination].get("locked") else ""
            tprint("     • {dest} ({dir}){locked}", dest=name_tr(destination), dir=tr(direction), locked=locked_str)
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
    tprint("\n  Tu voyages vers le {direction}...", direction=tr(direction))
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
        "achievements": joueur.achievements,
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
    joueur.achievements = donnees.get("achievements", [])
    
    # Recréer la quête si elle existe
    if donnees["quete"]["nom"]:
        quete_data = next((q for q in quetes_possibles if q["nom"] == donnees["quete"]["nom"]), None)
        if quete_data:
            joueur.quete = Quete(quete_data["nom"], quete_data["objectif"], quete_data["recompense"])
            joueur.quete.progression = donnees["quete"]["progression"]
            joueur.quete.terminee = donnees["quete"]["terminee"]
    
    tprint("Sauvegarde chargée: {name}", name=nom_sauvegarde)
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

ACHIEVEMENTS = {
    "first_victory": ("Première victoire", "Gagne ton premier combat."),
    "boss_hunter": ("Chasseur de boss", "Vaincs un boss."),
    "dragon_slayer": ("Tueur de dragon", "Vaincs le Dragon enflammé."),
    "level_5": ("Niveau 5", "Atteins le niveau 5."),
    "craft_first_item": ("Artisan", "Fabrique ton premier objet."),
    "first_bow_shot": ("Archer", "Tire une flèche avec un arc."),
}

def unlock_achievement(joueur, achievement_id):
    if achievement_id not in ACHIEVEMENTS or achievement_id in joueur.achievements:
        return False

    joueur.achievements.append(achievement_id)
    name, _description = ACHIEVEMENTS[achievement_id]
    tprint(tr("Succès débloqué : {name} !", name=tr(name)))
    return True

class Personnage:
    __slots__ = ('nom', 'pv_max', 'pv', 'attaque', 'defense', 'inventaire', 'xp', 'niveau', 'quete', 'localisation', 'last_spawned_enemy', 'loot_table', 'defeated_bosses', 'achievements')
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
        self.achievements = []
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
            unlock_achievement(self, "first_bow_shot")

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

        if self.niveau >= 5:
            unlock_achievement(self, "level_5")

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

    tprint(tr("Un combat commence contre {enn} !", enn=name_tr(ennemi.nom)))

    while joueur.est_vivant() and ennemi.est_vivant():
        # Statuts persistants
        if poison > 0:
            joueur.pv = max(0, joueur.pv - 3)
            poison -= 1
            tprint(tr("{name} souffre du poison (-3 PV).", name=name_tr(joueur.nom)))
        if brulure > 0:
            joueur.pv = max(0, joueur.pv - 2)
            brulure -= 1
            tprint(tr("{name} est brûlé (-2 PV).", name=name_tr(joueur.nom)))

        tprint(tr("\n{name} : {hp}/{maxhp} PV | ATK {atk} | DEF {defn}", name=name_tr(joueur.nom), hp=joueur.pv, maxhp=joueur.pv_max, atk=joueur.attaque, defn=joueur.defense))
        tprint(tr("\n{name} : {hp}/{maxhp} PV | ATK {atk} | DEF {defn}", name=name_tr(ennemi.nom), hp=ennemi.pv, maxhp=ennemi.pv_max, atk=ennemi.attaque, defn=ennemi.defense))

        # Tour du joueur
        if stun:
            print(tr("{name} est étourdi et ne peut pas agir ce tour !", name=name_tr(joueur.nom)))
            time.sleep(0.05)
            stun = False
        else:
            action = tinput(tr("Choisis ton action (a=attaque, e=inventaire, d=dodge, u=objet, r=repos, f=fuite, end=fin) : ")).strip().lower()
            if action == "a":
                joueur.attaquer(ennemi)
            elif action == "end":
                print(tr("Fin de la partie."))
                time.sleep(0.05)
                sys.exit()
            elif action == "e":
                print(tr("Inventaire :"), joueur.inventaire)
                time.sleep(0.05)
            elif action == "d":
                print(tr("{name} tente d'esquiver...", name=name_tr(joueur.nom)))
                time.sleep(0.05)
                if random.random() < 0.5:
                    print(tr("Esquive réussie ! Aucun dégât subi ce tour."))
                    time.sleep(0.05)
                    # saute le tour de l'ennemi
                    continue
                else:
                    print(tr("Esquive ratée !"))
                    time.sleep(0.05)
            elif action == "u":
                print(tr("Inventaire :"), joueur.inventaire)
                time.sleep(0.05)
                choix_objet = input(tr("Quel objet veux-tu utiliser ? ")).strip()
                if choix_objet == "Potion" and joueur.inventaire.get("Potion", 0) > 0:
                    joueur.inventaire["Potion"] -= 1
                    joueur.pv = min(joueur.pv_max, joueur.pv + 20)
                    print(tr("{name} utilise une Potion (+20 PV).", name=name_tr(joueur.nom)))
                    time.sleep(0.05)
                elif choix_objet == "Élixir" and joueur.inventaire.get("Élixir", 0) > 0:
                    joueur.inventaire["Élixir"] -= 1
                    joueur.attaque += 5
                    print(tr("{name} utilise un Élixir (+5 ATK).", name=name_tr(joueur.nom)))
                    time.sleep(0.05)
                else:
                    print(tr("Objet invalide ou indisponible."))
                    time.sleep(0.05)
            elif action == "r":
                soin = random.randint(5, 10)
                joueur.pv = min(joueur.pv_max, joueur.pv + soin)
                print(tr("{name} se repose et récupère {heal} PV.", name=name_tr(joueur.nom), heal=soin))
                time.sleep(0.05)
            elif action == "f":
                if random.random() < 0.5:
                    print(tr("{name} réussit à fuir le combat !", name=name_tr(joueur.nom)))
                    time.sleep(0.05)
                    return
                else:
                    print(tr("Fuite ratée !"))
                    time.sleep(0.05)
            else:
                print(tr("Action invalide, tu perds ton tour."))
                time.sleep(0.05)

        # Tour de l'ennemi
        if ennemi.est_vivant():
            if ennemi.nom == "Vampire":
                degats = max(1, ennemi.attaque - joueur.defense)
                joueur.subir_degats(degats)
                soin = degats // 2
                ennemi.pv = min(ennemi.pv_max, ennemi.pv + soin)
                print(tr("{name} mord {target}, inflige {damage} dégâts et récupère {heal} PV !", name=name_tr(ennemi.nom), target=name_tr(joueur.nom), damage=degats, heal=soin))
                time.sleep(0.05)

            elif ennemi.nom == "Spectre":
                # 20% de chance d'esquive sur ses propres tours (intangible)
                if random.random() < 0.2:
                    print(tr("{name} devient intangible et évite d'attaquer frontalement ce tour.", name=name_tr(ennemi.nom)))
                    time.sleep(0.05)
                else:
                    ennemi.attaquer(joueur)

            elif ennemi.nom == "Plante carnivore":
                degats = max(1, ennemi.attaque - joueur.defense)
                joueur.subir_degats(degats)
                poison = max(poison, 3)  # applique/rafraîchit 3 tours
                print(tr("{name} empoisonne {target} ! Poison pendant 3 tours (dégâts subis: {damage}).", name=name_tr(ennemi.nom), target=name_tr(joueur.nom), damage=degats))
                time.sleep(0.05)

            elif ennemi.nom == "Dragonnet":
                degats = max(1, ennemi.attaque - joueur.defense)
                joueur.subir_degats(degats)
                brulure = max(brulure, 3)  # applique/rafraîchit 3 tours
                print(tr("{name} brûle {target} ! Brûlure pendant 3 tours (dégâts subis: {damage}).", name=name_tr(ennemi.nom), target=name_tr(joueur.nom), damage=degats))
                time.sleep(0.05)

            elif ennemi.nom == "Harpie":
                if random.random() < 0.2:
                    stun = True
                    print(tr("{name} étourdit {target} ! Tu perdras ton prochain tour.", name=name_tr(ennemi.nom), target=name_tr(joueur.nom)))
                    time.sleep(0.05)
                else:
                    ennemi.attaquer(joueur)

            elif ennemi.nom == "Golem de pierre":
                # Ignore une partie de la DEF
                degats = max(1, ennemi.attaque - (joueur.defense // 2))
                joueur.subir_degats(degats)
                print(tr("{name} frappe brutalement, ignore une partie de la DEF et inflige {damage} dégâts.", name=name_tr(ennemi.nom), damage=degats))
                time.sleep(0.05)

            elif ennemi.nom == "Bandit":
                degats = max(1, ennemi.attaque - joueur.defense)
                if random.random() < 0.2:
                    degats *= 2
                    print(tr("{name} réussit une attaque critique !", name=name_tr(ennemi.nom)))
                    time.sleep(0.05)
                joueur.subir_degats(degats)
                print(tr("{name} attaque et inflige {damage} dégâts.", name=name_tr(ennemi.nom), damage=degats))
                time.sleep(0.05)

            elif ennemi.nom == "Minotaure":
                # Charge puissante mais se fatigue (-2 ATK pendant 2 tours simulés via message, pas de buff persistant ici)
                if random.random() < 0.3:
                    degats = max(1, (ennemi.attaque + 5) - joueur.defense)
                    joueur.subir_degats(degats)
                    print(tr("{name} charge avec rage et inflige {damage} dégâts !", name=name_tr(ennemi.nom), damage=degats))
                    time.sleep(0.05)
                else:
                    ennemi.attaquer(joueur)

            elif ennemi.nom == "Slime géant":
                # Attaque et renvoie un petit splash supplémentaire
                degats = max(1, ennemi.attaque - joueur.defense)
                splash = random.randint(0, 2)
                joueur.subir_degats(degats + splash)
                print(tr("{name} écrase et éclabousse : {damage}+{splash} dégâts.", name=name_tr(ennemi.nom), damage=degats, splash=splash))
                time.sleep(0.05)

            elif ennemi.nom == "Sorcier corrompu":
                # Sort aléatoire: feu (brulure), glace (stun), ombre (dégâts bruts)
                sort = random.choice(["feu", "glace", "ombre"])
                if sort == "feu":
                    degats = max(1, ennemi.attaque - joueur.defense)
                    joueur.subir_degats(degats)
                    brulure = max(brulure, 2)
                    print(tr("{name} lance un sort de feu : {damage} dégâts et brûlure (2 tours).", name=name_tr(ennemi.nom), damage=degats))
                    time.sleep(0.05)
                elif sort == "glace":
                    degats = max(1, ennemi.attaque - joueur.defense - 2)
                    joueur.subir_degats(degats)
                    stun = True
                    print(tr("{name} gèle {target} : {damage} dégâts et étourdissement.", name=name_tr(ennemi.nom), target=name_tr(joueur.nom), damage=degats))
                    time.sleep(0.05)
                else:
                    degats = max(2, ennemi.attaque - (joueur.defense // 3))
                    joueur.subir_degats(degats)
                    print(tr("{name} invoque les ombres et inflige {damage} dégâts occultes.", name=name_tr(ennemi.nom), damage=degats))
                    time.sleep(0.05)

            else:
                # Gobelin, Squelette, etc. comportement par défaut
                ennemi.attaquer(joueur)

    # Fin du combat
    if joueur.est_vivant():
        print(tr("{name} a vaincu {target} !", name=name_tr(joueur.nom), target=name_tr(ennemi.nom)))
        time.sleep(0.05)
        verifier_quete(joueur, ennemi=ennemi)
        unlock_achievement(joueur, "first_victory")
        if ennemi.nom in boss_names or ennemi.nom in superboss_names:
            unlock_achievement(joueur, "boss_hunter")
        if ennemi.nom == "Dragon enflammé":
            unlock_achievement(joueur, "dragon_slayer")
        if ennemi.nom in boss_names or ennemi.nom in superboss_names:
            if ennemi.nom not in joueur.defeated_bosses:
                joueur.defeated_bosses.append(ennemi.nom)
        bonus_xp = ennemi.pv_max // 10

        if ennemi.nom in superboss_names:
            joueur.gagner_xp(500 + bonus_xp)
            joueur.loot("Or", 100)
            joueur.loot("Clé Mystique", 0)  # pas de clé pour le superboss
            print(tr("Victoire. . ."))
            time.sleep(0.05)
        elif ennemi.nom in boss_names:
            joueur.gagner_xp(100 + bonus_xp)
            joueur.loot("Or", 50)
            joueur.loot("Clé Mystique", 1)  # 1 clé par boss régulier
            print(tr("Victoire contre un Boss !"))
            time.sleep(0.05)
        elif ennemi.nom in miniboss_names:
            # Récompenses de miniboss (entre ennemi classique et boss)
            joueur.gagner_xp(60 + bonus_xp)
            joueur.loot("Or", 30)
            # petite chance de drop rare / clé
            if random.random() < 0.20:
                rare = random.choice(["Épée magique", "Grimoire ancien", "Anneau de Force"])
                joueur.loot(rare, 1)
            if random.random() < 0.12:
                joueur.loot("Clé Mystique", 1)
            print(tr("Victoire contre un Mini-boss !"))
            time.sleep(0.05)
        else:
            joueur.gagner_xp(20 + bonus_xp)
            joueur.loot("Or", 10)
            print(tr("Victoire contre un ennemi classique."))
            time.sleep(0.05)

        for item, drop_chance in ennemi.loot_table:
            if random.random() < drop_chance:
                joueur.loot(item, 1)
    else:
        print(tr("{name} a été vaincu par {target}...", name=name_tr(joueur.nom), target=name_tr(ennemi.nom)))
        time.sleep(0.05)
        time.sleep(2)
        print(tr("Fin de la partie."))
        time.sleep(0.05)
        print(tr("Merci d'avoir joué !"))
        time.sleep(0.05)
        recommencer()
        reddit_url = "https://www.reddit.com/r/FreePython/"
        print(tr("Rejoignez ma communauté sur Reddit : {url}", url=reddit_url))
        time.sleep(0.05)
        print(tr("Le jeu se fermera dans 5 secondes..."))
        time.sleep(0.05)
        time.sleep(5)
        sys.exit()

def shop_handler(joueur, title, items):
    tprint(title)
    for i, (item, price) in enumerate(items, 1):
        tprint(f"{i}. {name_tr(item)} - {tr('Prix: {price} or', price=price)}")
    choix = choose_int(tr("Que veux-tu acheter? (numéro ou 0 pour quitter) : "), 0, len(items))
    if choix is None or choix == 0:
        return
    item, price = items[choix - 1]
    if not spend(joueur, price):
        return
    joueur.loot(item, 1)
    tprint(tr("Achat effectué!"))

def interagir_avec_pnj(joueur, npc_nom):
    def drink_beer():
        if spend(joueur, 2):
            joueur.pv = min(joueur.pv_max, joueur.pv + 10)
            tprint("Vous vous sentez revigoré! +10 PV")

    def eat_bread():
        if spend(joueur, 5):
            joueur.pv = min(joueur.pv_max, joueur.pv + 10)
            tprint("Le vin vous revigore complètement! +25 PV")

    def tavern_info():
        tprint("Le tavernier vous raconte des histoires sur les monstres des environs...")
        for line in [
            "- La forêt est infestée de plantes carnivores et de spectres",
            "- Le château abrite des vampires et des sorciers corrompus",
            "- Le marais maudit est le domaine du Roi du Marais",
            "- Et attention au Tyran de Feu dans le volcan!"
        ]:
            tprint(line)

    def sleep_inn():
        joueur.pv = joueur.pv_max
        tprint("Tu as dormi à l'auberge : PV restaurés et sauvegarde automatique.")
        sauvegarder_jeu(joueur, f"auto_sleep_{joueur.nom}")

    def improve_attack():
        if spend(joueur, 20):
            joueur.attaque += 2
            tprint("Votre attaque a été améliorée! +2 ATK")

    def improve_defense():
        if spend(joueur, 15):
            joueur.defense += 1
            tprint("Votre défense a été améliorée! +1 DEF")

    def rest_half():
        if spend(joueur, 10):
            joueur.pv = min(joueur.pv_max, joueur.pv + joueur.pv_max // 2)
            tprint("Vous vous reposez. +50% PV")

    def rest_full():
        if spend(joueur, 20):
            joueur.pv = joueur.pv_max
            tprint("Vous dormez complètement. PV restaurés.")

    def quest_advice():
        if joueur.quete:
            tprint("Votre quête vous mènera vers {cible}. Soyez prudent.", cible=name_tr(joueur.quete.cible))
        else:
            tprint("Vous n'avez pas de quête active.")

    def blessing():
        if spend(joueur, 30):
            joueur.pv_max += 5
            joueur.pv = min(joueur.pv_max, joueur.pv + 5)
            tprint("Vous recevez une bénédiction! +5 PV max")

    def sell_stolen():
        objet = tinput("Objet : ").strip()
        if objet in joueur.inventaire and joueur.inventaire[objet] > 0:
            joueur.inventaire[objet] -= 1
            joueur.inventaire["Or"] = joueur.inventaire.get("Or", 0) + 20
            tprint("Vendu pour {prix} or!", prix=20)
        else:
            tprint("Objet non trouvé.")

    def thief_quest():
        tprint("Quête acceptée : Volez une potion au vendeur. Revenez avec.")
        joueur.loot("Or", 50)
        tprint("Quête terminée! +50 or")

    def buy_book():
        if spend(joueur, 25):
            joueur.gagner_xp(10)
            tprint("Vous apprenez de nouvelles choses! +10 XP")

    def story():
        tprint("Il y a longtemps, le monde était en paix... Mais les dragons ont apporté le chaos.")

    menus = {
        "Tavernier du village": lambda: service_menu(joueur, "Bienvenue à la taverne! Que puis-je vous servir?", [
            ("Boire une bière (5 pièces d'or) - Restaure 10 PV", drink_beer),
            ("Manger un peu de pain (5 pièces d'or) - Restaure 10 PV", eat_bread),
            ("Demander des informations sur la région", tavern_info),
            ("Dormir à l'auberge (100% PV, sauvegarde auto)", sleep_inn),
        ]),
        "Vendeur de potions": lambda: shop_handler(joueur, "Bienvenue chez l'apothicaire! J'ai les meilleures potions de la région.", [
            ("Potion", 5),
            ("Élixir", 15),
            ("Potion supérieure", 25),
        ]),
        "Marchand": lambda: shop_handler(joueur, "Bienvenue chez le marchand! Voici ce que j'ai en stock:", [
            ("Épée magique", 50),
            ("Bouclier", 30),
            ("Anneau de Force", 40),
            ("Cape d'Invisibilité", 60),
            ("Amulette de Vie", 45),
        ]),
        "Forgeron": lambda: service_menu(joueur, "Bienvenue chez le forgeron! J'améliore vos armes et armures.", [
            ("Améliorer l'attaque (+2 ATK, 20 or)", improve_attack),
            ("Améliorer la défense (+1 DEF, 15 or)", improve_defense),
        ]),
        "Aubergiste": lambda: service_menu(joueur, "Bienvenue à l'auberge! Reposez-vous ici.", [
            ("Dormir (restaure 50% PV, 10 or)", rest_half),
            ("Dormir complètement (100% PV, 20 or)", rest_full),
        ]),
        "Mystique": lambda: service_menu(joueur, "Les étoiles me parlent... Que cherchez-vous?", [
            ("Conseil sur la quête (+ indice)", quest_advice),
            ("Bénédiction (+5 PV max temporaire, 30 or)", blessing),
        ]),
        "Contact de la Guilde des Voleurs": lambda: service_menu(joueur, "Psst... Besoin d'aide discrète?", [
            ("Vendre un objet volé (double prix)", sell_stolen),
            ("Quête secondaire : Voler un objet (récompense 50 or)", thief_quest),
        ]),
        "Savant": lambda: service_menu(joueur, "Bienvenue dans ma bibliothèque. La connaissance est pouvoir.", [
            ("Acheter un livre de sagesse (+10 XP, 25 or)", buy_book),
            ("Histoire du monde", story),
        ]),
    }

    handler = menus.get(npc_nom)
    if handler:
        handler()
    else:
        tprint("Choix invalide.")

def fabriquer_objet(joueur, item):
    item_data = ITEM_DATA.get(item)
    if not item_data or not item_data["canCraftItem"]:
        return False

    recipe = CRAFTING_RECIPES.get(item_data["canCraftWith"])
    if recipe is None:
        return False

    ingredients = recipe
    if any(joueur.inventaire.get(material, 0) < quantity for material, quantity in ingredients.items()):
        tprint(tr("Il manque des matériaux pour fabriquer {item}.", item=name_tr(item)))
        return False

    for material, quantity in ingredients.items():
        if material not in REUSABLE_CRAFTING_TOOLS:
            joueur.inventaire[material] -= quantity

    joueur.loot(item, item_data.get("craftQuantity", 1))
    unlock_achievement(joueur, "craft_first_item")
    tprint(tr("{item} fabriqué ! Bonus de dégâts : +{damage}.", item=name_tr(item), damage=item_data["damageBonus"]))
    return True

def fabriquer_arc(joueur):
    return fabriquer_objet(joueur, "Arc")

def fabriquer_dague(joueur):
    return fabriquer_objet(joueur, "Dague")

def fabriquer_epee_longue(joueur):
    return fabriquer_objet(joueur, "Épée longue")

def menu_fabrication(joueur):
    options = []
    for item, item_data in ITEM_DATA.items():
        if not item_data["canCraftItem"]:
            continue
        recipe = CRAFTING_RECIPES.get(item_data["canCraftWith"], {})
        ingredients = ", ".join(
            f"{quantity} {name_tr(material)}"
            for material, quantity in recipe.items()
        )
        label = tr("Fabriquer {item} ({ingredients})", item=name_tr(item), ingredients=ingredients)
        options.append((label, lambda item=item: fabriquer_objet(joueur, item)))
    service_menu(joueur, "Que veux-tu fabriquer ?", options)

def afficher_succes(joueur):
    tprint("=== SUCCÈS ===")
    for achievement_id, (name, description) in ACHIEVEMENTS.items():
        if achievement_id in joueur.achievements:
            tprint("[Débloqué] {name} - {description}", name=tr(name), description=tr(description))
        else:
            tprint("[Verrouillé] {name} - {description}", name=tr(name), description=tr(description))
    tprint("Succès : {unlocked}/{total}", unlocked=len(joueur.achievements), total=len(ACHIEVEMENTS))

# --- Menu principal ---
def menu_principal(joueur):
    donner_quete(joueur)  # donne une quête au début
    afficher_carte(joueur)  # affiche la carte au démarrage
    while joueur.est_vivant():
        print("\n" + tr("=== MENU PRINCIPAL ==="))
        time.sleep(0.05)
        print(tr("Localisation: {loc}", loc=joueur.localisation))
        time.sleep(0.05)
        current_into_level = joueur.xp - total_xp_for_level(joueur.niveau)
        required = total_xp_for_level(joueur.niveau + 1) - total_xp_for_level(joueur.niveau)
        print(tr("Niveau: {lvl} | PV: {pv}/{pvmax} | ATK: {atk} | DEF: {defn} | XP: {cur}/{req}", lvl=joueur.niveau, pv=joueur.pv, pvmax=joueur.pv_max, atk=joueur.attaque, defn=joueur.defense, cur=current_into_level, req=required))
        time.sleep(0.05)
        print()
        time.sleep(0.05)
        for opt in [
            "1. Combattre un ennemi",
            "2. Affronter un boss (si disponible)",
            "3. Affronter le SUPERBOSS",
            "4. Voir inventaire",
            "5. Voir quête active",
            "6. Voir la carte",
            "7. Voyager vers une autre région",
            "8. Sauvegarder la progression",
            "9. Quitter",
            "10. Interagir avec les habitants (en devloppement)",
            "11. Fabriquer un objet",
            "12. Voir les succès",
        ]:
            tprint(opt)

        choix = tinput("Tape un chiffre (1-12) : ").strip()

        choix_normalise = "".join(choix.casefold().split())
        if choix_normalise in {"anumber(1-10)", "anumber(1-10))"}:
            print(tr("Haha very funny"))
            continue

        if choix == "1":
            # Combat location-based (spawn aléatoire depuis la liste de la localisation)
            ennemi = spawn_enemy_for_location(joueur)
            if ennemi:
                combat(joueur, ennemi)
            else:
                print(tr("Aucun ennemi disponible ici!"))
                time.sleep(0.05)
        elif choix == "2":
            # Boss fight location-based
            lieu = locations.get(joueur.localisation, {})
            boss_options = lieu.get("boss")
            if boss_options:
                if isinstance(boss_options[0], str):
                    boss_options = (boss_options,)
                available_bosses = [boss for boss in boss_options if boss[0] not in joueur.defeated_bosses]
                if available_bosses:
                    nom, pv, atk, defn = random.choice(available_bosses)
                    boss = Personnage(nom, pv, atk, defn)
                    combat(joueur, boss)
                else:
                    print(tr("Aucun boss disponible ici!"))
                    time.sleep(0.05)
            else:
                print(tr("Aucun boss disponible ici!"))
                time.sleep(0.05)
        elif choix == "3":
            available_superbosses = [boss for boss in superboss_possibles if boss[0] not in joueur.defeated_bosses]
            if available_superbosses:
                nom, pv, atk, defn = random.choice(available_superbosses)
                superboss = Personnage(nom, pv, atk, defn)
                combat(joueur, superboss)
            else:
                print(tr("Aucun boss disponible ici!"))
                time.sleep(0.05)
        elif choix == "4":
            print(tr("Inventaire :"), joueur.inventaire)
            time.sleep(0.05)
        elif choix == "5":
            if joueur.quete:
                q = joueur.quete
                etat = "terminée" if q.terminee else f"{q.progression}/{q.quantite}"
                print(tr("Quête : {name} | Objectif : {target} ({state})", name=name_tr(q.nom), target=name_tr(q.cible), state=etat))
                time.sleep(0.05)
            else:
                print(tr("Aucune quête active."))
                time.sleep(0.05)
        elif choix == "6":
            afficher_carte(joueur)
        elif choix == "7":
            afficher_carte(joueur)
            lieu = locations.get(joueur.localisation, {})
            if lieu.get("connections"):
                destinations = list(lieu["connections"].keys())
                for i, dest in enumerate(destinations, 1):
                    print(f"{i}. {name_tr(dest)}")
                    time.sleep(0.05)
                try:
                    choix_voyage = int(tinput(tr("Choisir une destination (numéro) : ")))
                    if 1 <= choix_voyage <= len(destinations):
                        voyager(joueur, destinations[choix_voyage - 1])
                    else:
                        print(tr("Choix invalide!"))
                        time.sleep(0.05)
                except (ValueError, IndexError):
                    print(tr("Entrée invalide!"))
                    time.sleep(0.05)
            else:
                print(tr("Aucune destination accessible!"))
                time.sleep(0.05)
        elif choix == "8":
            nom_save = tinput("Nom de la sauvegarde (défaut: 'save') : ").strip()
            if not nom_save:
                nom_save = "save"
            sauvegarder_jeu(joueur, nom_save)
        elif choix == "9":
            print(tr("Fin de la partie."))
            time.sleep(0.05)
            print(tr("le jeu se fermera dans 5 secondes..."))
            time.sleep(4)
            sys.exit()
        elif choix == "10":
            lieu = locations.get(joueur.localisation, {})
            if lieu.get("npcs"):
                npcs = lieu["npcs"]
                for i, npc in enumerate(npcs, 1):
                    print(f"{i}. {name_tr(npc)}")
                    time.sleep(0.05)
                try:
                    choix_npc = int(tinput(tr("Choisir un habitant (numéro) : ")))
                    if 1 <= choix_npc <= len(npcs):
                        interagir_avec_pnj(joueur, npcs[choix_npc - 1])
                    else:
                        print(tr("Choix invalide!"))
                        time.sleep(0.05)
                except (ValueError, IndexError):
                    print(tr("Entrée invalide!"))
                    time.sleep(0.05)
            else:
                print(tr("Aucun PNJ disponible ici!"))
                time.sleep(0.05)
        elif choix == "11":
            menu_fabrication(joueur)
        elif choix == "12":
            afficher_succes(joueur)
        else:
            print(tr("Choix invalide."))
            time.sleep(0.05)

# --- Lancement du jeu ---
def launcher():
    """Écran de démarrage - Choisir nouveau jeu ou charger"""
    # Choix de la langue au lancement
    global LANG
    try:
        lang_choice = input(tr("Choisir la langue / Choose language (fr/en) [fr]: ")).strip().lower()
        if lang_choice.startswith('en'):
            LANG = 'en'
    except Exception:
        pass

    tprints(
        "\n" + "="*50,
        tr("BIENVENUE DANS RPG.txt"),
        "="*50,
    )

    sauvegardes = lister_sauvegardes()

    if sauvegardes:
        print(tr("1. Nouveau jeu"))
        print(tr("2. Charger une sauvegarde"))
        choix = tinput(tr("Choisir (1 ou 2) : ")).strip()

        if choix == "2":
            print(tr("\nSauvegardes disponibles:"))
            for i, save in enumerate(sauvegardes, 1):
                print(f"  {i}. {save}")
            try:
                choix_save = int(tinput(tr("Quelle sauvegarde charger? (numéro) : ")))
                if 1 <= choix_save <= len(sauvegardes):
                    joueur = charger_jeu(sauvegardes[choix_save - 1])
                    if joueur:
                        menu_principal(joueur)
                    return
                tprint(tr("Choix invalide!"))
            except ValueError:
                tprint(tr("Entrée invalide!"))
    
    joueur = Personnage("Héros", 100, 15, 5, pv_max=100)
    joueur.loot("Or", 10)  # or de départ
    joueur.loot("Bâton", 1)
    menu_principal(joueur)

if __name__ == "__main__":
    launcher()
#1674
