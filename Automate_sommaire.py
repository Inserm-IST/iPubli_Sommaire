"""
Script qui permet, pour un fichier csv contenant les métadonnées de communiqués de presse de former le sommaire
en HTML correspondant sous la forme d'une structure thématique/Sous-thématique et dates
Auteur:Juliette Janes
Date:13/04/2023
"""

import pandas as pd
from lxml import etree as ET
import click
import os
import re
from difflib import SequenceMatcher
import sys


def create_df_cat(df, categorie):
    """
    Fonction qui récupère la liste des catégories accessibles dans le csv
    :param df: dataframe
    :return: liste des catégories
    """
    # stockage dans une variable liste_cat des valeurs dans la colonne catégorie
    liste_cat = df[str(categorie)].tolist()
    unique_liste_cat = list(dict.fromkeys(liste_cat))
    return unique_liste_cat

def creation_sommaire(df, details):
    cat_date = create_df_cat(df, "dc.date.issued[fr]")
    for date in cat_date:
        df_date = df.loc[df['dc.date.issued[fr]'] == date]
        df_date = df_date.reset_index(drop=True)
        racine_date, details_date = creation_titre(details, str(date), 2)
        for n in range(len(df_date)):
            df_line = df_date.iloc[n]
            # création des balises html pour l'article traité
            div1_html = ET.SubElement(details_date, "div")
            div1_html.attrib['class'] = 'artifact-description'
            div2_html = ET.SubElement(div1_html, "div")
            # création de la valeur class qui a pour valeur artifact title
            div2_html.attrib['class'] = 'artifact-title'
            # stockage dans la valeur handle de la valeur de la cellule identifier
            handle = df_line['dc.identifier.uri']
            # suppression d'url pour conserver uniquement le handle
            handle_propre = "https://www.ipubli.inserm.fr/handle/10608/"+handle[-5:]
            print(handle_propre)
            ul_html = ET.SubElement(div2_html, "ul")
            # création de la balise a qui contient le handle et permet de faire le lien avec la page de l'article. Ajout
            # de la valeur handle dans l'attribut handle et de l'attribut onclick permettant de création un lien
            a_html = ET.SubElement(ul_html, "a", href=handle_propre,
                                   onclick="window.open(this.href,'_blank');return false;")
            # création des balises suivantes
            li_div_html = ET.SubElement(a_html, "li")
            li_div_html.attrib['class'] = "som-titre-niveau2"
            # ajout du texte dans la cellule titre dans la balise titre
            li_div_html.text = df_line["dc.title[fr]"]
    return details

def creation_titre(racine, titre, niveau):
    details_html = ET.SubElement(racine, "details")
    summary_html = ET.SubElement(details_html, "summary", style="cursor:pointer;")
    cat_html = ET.SubElement(summary_html, "li")
    cat_html.attrib['class'] = "som-titre-niveau"+str(niveau)
    cat_html.text = str(titre)
    return racine, details_html

def creation_html(categorie, df, racine, souscategorie):
    """
    Fonction qui, à partir d'un dataframe pour une catégorie, met à jour l'arbre xml en y ajouter les balises et texte pour chaque article
    :param categorie: catégorie traitée
    :param df: dataframe de travail
    :param racine: arbre xml
    :return: arbre xml racine mis à jour avec les nouveaux articles traités pour 1 catégorie
    """
    df_categorie = df.loc[df['thematique'] == categorie]
    # réorganisation de l'index du dataframe obtenu
    df_categorie = df_categorie.reset_index(drop=True)
    # création des balises et insertion du nom de la catégorie
    racine,details_categorie = creation_titre(racine, categorie, 1)
    if categorie == "Actualité institutionnelle":
        sous_cat = create_df_cat(df_categorie, "sous_thematique")
        for el in sous_cat:
            df_sous_cat = df_categorie.loc[df_categorie['sous_thematique'] == el]
            df_sous_cat = df_sous_cat.reset_index(drop=True)
            racine_sous_cat, details_sous_cat = creation_titre(details_categorie, el, 3)
            cat_date = create_df_cat(df_sous_cat, "dc.date.issued[fr]")
            for date in cat_date:
                df_date = df_sous_cat.loc[df_sous_cat['dc.date.issued[fr]'] == date]
                df_date = df_date.reset_index(drop=True)
                racine_date, details_date = creation_titre(details_sous_cat, str(date), 4)
                for n in range(len(df_date)):
                    df_line = df_date.iloc[n]
                    li_html = ET.SubElement(details_date, "li")
                    li_html.attrib['class']="som-titre-niveau2"

                    # stockage dans la valeur handle de la valeur de la cellule identifier
                    handle = df_line['dc.identifier.uri']
                    # suppression d'url pour conserver uniquement le handle
                    handle_propre ="https://www.ipubli.inserm.fr/handle/10608/"+ handle[-5:]
                    # création de la balise a qui contient le handle et permet de faire le lien avec la page de l'article. Ajout
                    # de la valeur handle dans l'attribut handle et de l'attribut onclick permettant de création un lien
                    a_html = ET.SubElement(li_html, "a", href=handle_propre,
                                           onclick="window.open(this.href,'_blank');return false;")
                    # ajout du texte dans la cellule titre dans la balise titre
                    a_html.text = df_line["dc.title[fr]"]
    elif categorie=="Résultat de recherche" and souscategorie==True:
        sous_cat = create_df_cat(df_categorie, "sous_thematique")
        for el in sous_cat:
            df_sous_cat = df_categorie.loc[df_categorie['sous_thematique'] == el]
            df_sous_cat = df_sous_cat.reset_index(drop=True)
            racine_sous_cat, details_sous_cat = creation_titre(details_categorie, el, 3)
            cat_date = create_df_cat(df_sous_cat, "dc.date.issued[fr]")
            for date in cat_date:
                df_date = df_sous_cat.loc[df_sous_cat['dc.date.issued[fr]'] == date]
                df_date = df_date.reset_index(drop=True)
                racine_date, details_date = creation_titre(details_sous_cat, str(date), 4)
                for n in range(len(df_date)):
                    df_line = df_date.iloc[n]
                    li_html = ET.SubElement(details_date, "li")
                    li_html.attrib['class'] = "som-titre-niveau2"

                    # stockage dans la valeur handle de la valeur de la cellule identifier
                    handle = df_line['dc.identifier.uri']
                    # suppression d'url pour conserver uniquement le handle
                    handle_propre = "https://www.ipubli.inserm.fr/handle/10608/" + handle[-5:]
                    # création de la balise a qui contient le handle et permet de faire le lien avec la page de l'article. Ajout
                    # de la valeur handle dans l'attribut handle et de l'attribut onclick permettant de création un lien
                    a_html = ET.SubElement(li_html, "a", href=handle_propre,
                                           onclick="window.open(this.href,'_blank');return false;")
                    # ajout du texte dans la cellule titre dans la balise titre
                    a_html.text = df_line["dc.title[fr]"]
    else:
        cat_date = create_df_cat(df_categorie, "dc.date.issued[fr]")
        for date in cat_date:

            df_date = df_categorie.loc[df_categorie['dc.date.issued[fr]'] == date]
            df_date = df_date.reset_index(drop=True)
            racine_date, details_date = creation_titre(details_categorie, str(date), 4)
            for n in range(len(df_date)):
                df_line = df_date.iloc[n]
                # création des balises html pour l'article traité
                li_html = ET.SubElement(details_date, "li")
                li_html.attrib['class'] = "som-titre-niveau2"

                # stockage dans la valeur handle de la valeur de la cellule identifier
                handle = df_line['dc.identifier.uri']
                # suppression d'url pour conserver uniquement le handle
                handle_propre = "https://www.ipubli.inserm.fr/handle/10608/"+handle[-5:]
                # création de la balise a qui contient le handle et permet de faire le lien avec la page de l'article. Ajout
                # de la valeur handle dans l'attribut handle et de l'attribut onclick permettant de création un lien
                a_html = ET.SubElement(li_html, "a", href=handle_propre,
                                       onclick="window.open(this.href,'_blank');return false;")
                # ajout du texte dans la cellule titre dans la balise titre
                a_html.text = df_line["dc.title[fr]"]
    # tant que le nombre d'itération de la boucle n'est pas égale au nombre de ligne dans le dataframe, on réitère les
    # opérations suivantes
    # la fonction retourne l'arbre xml mis à jour
    return racine


def creation_css(filename):
    """
    Fonction qui créé le css et l'ajoute en tête du document XML créé
    :param filename: nom du fichier
    :type filename: str
    :return: document XML avec css
    """
    xml_css = """<head>
    <style>
    p   {
    font-size:16px; 
    text-align:justify;
    }
  
    ul {
    list-style-type: none;
    } 
    

    li.som-titre-niveau1 { 
     font-size:20px; 
            font-style: italic;
            font-weight: light bold;
display: block;
margin: 6px;
text-decoration: none;
    color: #e75406
}
li.som-titre-niveau1:hover{
color: black;
  }
li.som-titre-niveau1::before{
  content: "•";
  padding-right: 8px;
  }
    li.som-titre-niveau2 { 
    font-size:15.5px; 
margin: 5.5px;
    
  }
li.som-titre-niveau2::before{
    content: "•";
  padding-right: 8px;
}
li.som-titre-niveau3 { 
    font-size: 18px; 
    font-weight: light bold;
margin: 5.5px;
   margin-left: 80px;
    color:#6B8E23;
    }
 li.som-titre-niveau3:hover{
 text-decoration: underline;
  }
li.som-titre-niveau4 { 
    font-size: 15px; 
    font-weight: bold;
margin: 6px;
margin-left: 80px;
    }
li.som-titre-niveau4:hover{
 text-decoration: underline;

  }
    summary style:-webkit-details-marker { display: none }
</style>
</head>
        """
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(xml_css.rstrip('\r\n') + '\n' + content)


@click.command()
@click.argument("csv_file", type=str)
@click.option("-s", "--souscat", "souscategorie", is_flag=True, default=False)
def creation_sommaire(csv_file, souscategorie):
    """
    Fonction qui, à partir d'un csv, retourne un fichier xml contenant le sommaire html Medecine\Science
    :return: fichier xml sommaire.xml
    """
    # lecture du fichier csv et stockage dans une variable df
    df = pd.read_csv(csv_file,encoding="utf-8")
    print("Traitement du csv lancé")
    # la variable list_div mobilise la fonction create_df_cat qui récupère la liste des différentes catégories présentes dans
    # le csv
    liste_div = create_df_cat(df, "thematique")
    # Création de l'élément xml racine du html sommaire
    racine = ET.Element("div")
    sommaire = ET.SubElement(racine, "h3")
    sommaire.text = "Sommaire par thématique"
    ul = ET.SubElement(racine, "ul")
    # pour chaque catégorie de la liste list_div les actions suivantes sont réalisées
    for categorie in liste_div:
        #affichage de la catégorie traitée
        print("Traitement de la catégorie "+categorie)
        # récupération des lignes du df qui font parti de la catégorie traitée

        # mobilisation de la fonction creation_html qui, pour toutes les lignes du csv catégorie traitée, créé les balises
        # html correspondantes et y ajoute le texte et les valeurs d'attributs extraites du csv
        ul = creation_html(categorie, df, ul, souscategorie)

    # transformation de l'élément xml racine en arbre xml
    racine = ET.ElementTree(racine)

    # impression de l'arbre xml dans un fichier xml
    racine.write("sommaire.html", encoding="utf-8")
    # ajout du css en tête de fichier:
    #creation_css("sommaire.html")
    print("Le sommaire a bien été généré, vous pouvez le retrouver dans le fichier sommaire.xml disponible dans votre dossier de traitement")


if __name__ == "__main__":
    creation_sommaire()
