# Informations préalables
chemin_1 = "liste_des_articles.csv" # Chemin vers la base de données des articles
separateur_1 = ","
chemin_2 = "liste_des_recherches.csv" # Chemin vers la base de données de l'historique des recherches
separateur_2 = ","
recherche = "computer"

# Importation des modules
import pandas as pd
import numpy as np

# Lecture de la base de donnée contenant les information sur les articles------------------
def get_liste_articles(chemin_1,separateur_1):
    """
    La fonction prend en entrée une base de donnée d'articles.
    Elle renvoie une liste de dictionnaire. Chaque dictionnaire représente une ligne de la base(un article) 
    et contient l'id, le nom et la description de l'article
    """
    base_donnees = pd.read_csv(chemin_1, separateur_1)
    base_donnees = base_donnees.fillna("")

    liste_articles = []

    for curseur_1 in range(0, len(base_donnees)):
        element = {}                                                                            
        element['id'] = base_donnees['id'].iloc[curseur_1]                      
        element['nom'] = base_donnees['name'].iloc[curseur_1]                   
        element['description'] = base_donnees['description'].iloc[curseur_1]

        liste_articles.append(element)

    return liste_articles

liste_articles = get_liste_articles(chemin_1, separateur_1)

# Lecture de la base de donnée contenant les information sur les articles recherchés--------
def get_liste_historiques(chemin_2,separateur_2):
    """
    La fonction prend en entrée l'historique des anciennes recherches sous forme de base de données.
    Elle renvoie une liste de dictionnaire. Chaque dictionnaire représente une ligne de la base(un article) et 
    contient le mot cherche et l'ID de l'article sur lequel l'utiliisateur a cliqué.
    """
    base_donnees = pd.read_csv(chemin_2, separateur_2)
    base_donnees = base_donnees.fillna("")

    liste_historiques = []

    for curseur_2 in range(0, len(base_donnees)):
        historique = {}                                                                            
        historique['mot_cherche'] = base_donnees['search_text'].iloc[curseur_2]                      
        historique['article_1'] = base_donnees['clicked_article_1'].iloc[curseur_2]                   

        liste_historiques.append(historique)

    return liste_historiques

liste_historiques = get_liste_historiques(chemin_2, separateur_2)

def get_mot_cherche(liste_historique):
    return liste_historique.get('mot_cherche')

def get_article_1(liste_historique):
    return liste_historique.get('article_1')

# Tokenisation----------------------------------------------------------------------------- 
def tokenisation(phrase):
    """
    La fonction prend en entrée une chaine de caractère à découper. 
    Elle renvoi une liste des chaines de caractere séparée par un espace ou les symboles suivant:
    "-", ".", "/", ",", ";", "'" dans l'élément pris en entrée.
    """
    jonctions = ["-", ".", "/", ",", ";", "'"]

    for jonction in jonctions:
        if jonction in phrase:
            phrase = phrase.replace(jonction, " ")
    
    phrase = phrase.split(" ")
    while '' in phrase:
        del phrase[phrase.index('')]
    
    return phrase
# print(tokenisation("Le courage n'est pas l'absence de peur, mais la capacité de vaincre ce qui fait peur."))

# Ignorer la casse-------------------------------------------------------------------------
def casse(phrase):
    """
    La fonction prend en entrée une liste de mots.
    Elle renvoie la liste de mots pris en entrée mais avec tous les caractères en minuscule.
    """
    #phrase = [mot.lower() for mot in phrase]
    for mot in phrase:
        minuscules = mot.lower()
        phrase[phrase.index(mot)] = minuscules
    return phrase
# print(casse(['boolVO', 'FJFJ', 'lkk']))

# Caractères spéciaux---------------------------------------------------------------------------------
def special_symb(phrase):
    """
    La fonction prend en entrée une liste de chaine de caractère.
    Elle renvoi la liste prise en entrée mais après avoir remplacé les symboles avec accent ou cédille avec des symboles sans
    """
    accents = {}
    accents['o'] = 'ô', 'ö'
    accents['a'] = 'à', 'â', 'ä'
    accents['e'] = 'é', 'è', 'ê', 'ë'
    accents['i'] = 'î', 'ï'
    accents['u'] = 'ù', 'û', 'ü' 
    accents['c'] = 'ç'

    for mot in range(0, len(phrase)):

        for curseur_2 in accents['o']:
            if curseur_2 in phrase[mot]:
                accentless = phrase[mot].replace(curseur_2,'o')
                phrase[mot] = accentless

        for curseur_2 in accents['a']:
            if curseur_2 in phrase[mot]:
                accentless = phrase[mot].replace(curseur_2,'a')
                phrase[mot] = accentless

        for curseur_2 in accents['e']:
            if curseur_2 in phrase[mot]:
                accentless = phrase[mot].replace(curseur_2,'e')
                phrase[mot] = accentless

        for curseur_2 in accents['i']:
            if curseur_2 in phrase[mot]:
                accentless = phrase[mot].replace(curseur_2,'i')
                phrase[mot] = accentless

        for curseur_2 in accents['u']:
            if curseur_2 in phrase[mot]:
                accentless = phrase[mot].replace(curseur_2,'u')
                phrase[mot] = accentless

        for curseur_2 in accents['c']:
            if curseur_2 in phrase[mot]:
                accentless = phrase[mot].replace(curseur_2,'c')
                phrase[mot] = accentless

    return phrase
# print(special_symb(['français', 'écrivain', 'où', 'forçé']))

# Formatage du texte pris en entrée--------------------------------------------------------
def formatage(phrase):
    """
    La fonction transforme en chaine de caractères l'élément pris en entrée puis lui applique successivement les fonctions tokenisation, casse et special_symb
    """
    phrase = str(phrase)
    mots = tokenisation(phrase)
    accentless = casse(mots)
    phrase_formate = special_symb(accentless)

    return phrase_formate
# print(formatage("Le courage n'est pas l'absence de peur, mais la capacité de vaincre ce qui fait peur."))

# Distance de levenshtein------------------------------------------------------------------
# La distance entre deux mots
def get_distance_levenshtein(caracteres_1, caracteres_2):
    """
    La fonction prend en entrée deux mots et calacule la distance de levenshtein entre eux.
    """
    taille_colonne_1 = len(caracteres_1) + 1
    taille_colonne_2 = len(caracteres_2) + 1
    
    levenshtein_matrix = np.zeros ((taille_colonne_1, taille_colonne_2))

    for x in range(0, taille_colonne_1):
        levenshtein_matrix [x, 0] = x

    for y in range(0, taille_colonne_2):
        levenshtein_matrix [0, y] = y

    for x in range(1, taille_colonne_1):
        for y in range(1, taille_colonne_2):
            if caracteres_1[x - 1] == caracteres_2[y - 1]:
                levenshtein_matrix [x,y] = min(
                    levenshtein_matrix[x - 1, y] + 1,
                    levenshtein_matrix[x - 1, y - 1],
                    levenshtein_matrix[x, y - 1] + 1
                )
            else:
                levenshtein_matrix [x, y] = min(
                    levenshtein_matrix[x - 1, y] + 1,
                    levenshtein_matrix[x - 1, y - 1] + 1,
                    levenshtein_matrix[x , y - 1] + 1
                )
    return levenshtein_matrix[taille_colonne_1 - 1, taille_colonne_2 - 1]

# print(get_distance_levenshtein("bonjour", "bonjour"))
# print(get_distance_levenshtein("bonsoir", "bonjour"))
# print(get_distance_levenshtein("ruojnob", "bonjour"))
# print(get_distance_levenshtein("bon", "bonjour"))
# print(get_distance_levenshtein("catalogne", "bonjour"))

# Ratio de ressemeblance-------------------------------------------------------------------

def get_ratio_ressemblance(caracteres_1, caracteres_2):
    """
    La fonction calcule le ratio de ressemblance de deux mots en fesant 1 - leur ratio de dissemblance. 
    Le ratio de dissemblance étant donné par le quotient de la distance de levenshtein entre deux mots et la taille du plus grand des deux mots.
    """
    distance = get_distance_levenshtein(caracteres_1, caracteres_2)
    ratio_de_dissemblance = distance / max(len(caracteres_1), len(caracteres_2))
    ratio_ressemblance = 1 - (ratio_de_dissemblance)
    
    return ratio_ressemblance

# print(get_ratio_ressemblance("bonjour", "bonjour"))
# print(get_ratio_ressemblance("bonsoir", "bonjour"))
# print(get_ratio_ressemblance("ruojnob", "bonjour"))
# print(get_ratio_ressemblance("bon", "bonjour"))
# print(get_ratio_ressemblance("catalogne", "bonjour"))

# Indexation-------------------------------------------------------------------------------
# 
def get_recherche(phrase, liste_articles, liste_historiques):

    liste_historiques_pert = []
    liste_recherche = []
    liste_historiques_pertinant = []

    phrase_formate = formatage(phrase)

    # Obtenir la liste des recherches précédentes correspondantes à la recherche actuelle
    for mot in phrase_formate:
        for historiques in range(0, len(liste_historiques)):
            mot_forme = formatage(liste_historiques[historiques].get('mot_cherche'))          
            if mot in mot_forme:
                liste_historiques_pert.append(liste_historiques[historiques])
            else:
                for article in mot_forme:   
                    ratio_ressemblance = get_ratio_ressemblance(mot, article) 
                    if ratio_ressemblance >= 0.8:
                        liste_historiques_pert.append(liste_historiques[historiques])
    
    # Sortir les recherches pour lesquelles il n'y a aucun clic
    for ligne in range(0, len(liste_historiques_pert)):
        if (liste_historiques_pert[ligne]).get('article_1') != "":
            if liste_historiques_pert[ligne] not in liste_historiques_pertinant:
                liste_historiques_pertinant.append(liste_historiques_pert[ligne])

    # AJouter les articles pour lesquels il y a eu au moin une sélection à la liste finale
    for ligne in range(0, len(liste_historiques_pertinant)):
        for articles in range(0, len(liste_articles)):
            if liste_historiques_pertinant[ligne].get('article_1') == liste_articles[articles].get('nom'):
                if liste_articles[articles] not in liste_recherche:
                    liste_recherche.append(liste_articles[articles])
    
    # Chercher le mot dans la liste des articles
    for mot in phrase_formate:
        for articles in range(0,len(liste_articles)):
            nom_forme = formatage(liste_articles[articles].get('nom'))          
            for article in nom_forme:
                if mot in article:
                    if articles not in liste_recherche:
                        liste_recherche.append(liste_articles[articles])
                else:
                    ratio_ressemblance = get_ratio_ressemblance(mot, article) 
                    if ratio_ressemblance >= 0.8:
                        if articles not in liste_recherche:
                            liste_recherche.append(liste_articles[articles])

    return liste_recherche


resultat_recherche = get_recherche(recherche, liste_articles, liste_historiques)
print(resultat_recherche)
