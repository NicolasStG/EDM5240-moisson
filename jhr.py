# coding : utf-8

### Très bon script, bien documenté!

import csv
import requests
from bs4 import BeautifulSoup
### Wow! Un fichier de fonctions externes! Bravo! :)
from uqam_function import * #permet de faire sortir tout ce que le document fonction contient.
from fonctionsJHR import * ### J'ai quelques corrections dans ton fichier de fonctions

fichier = "professeur_UQAM_JHR.csv" ### Je rebaptise pour faire mes tests

entete = {
    "User-Agent":"Nicolas St-Germain - 438/492-2926 : Étudiant en journalisme à L'UQAM",
    "From":"niikostg@gmail.com"
}

url = "https://professeurs.uqam.ca/liste-departements-ecoles/"
contenu = requests.get(url,headers=entete)
n = 0 #permet de garder le track quand le code roule, être certain que tout va bien.
page = BeautifulSoup(contenu.text,"html.parser") #pour analyser le code html
div_departements = page.find("div", class_="entry-content")
departements = div_departements.find_all("li")

with open(fichier,"w") as f2:
    creation_fichier = csv.writer(f2,)

    #Ici je suis à la première page et je veut accéder aux différents départements.
    for departement in departements:
        lien_departement = departement.find("a")["href"] #Trouver le lien qui mènent vers les départements
        
        #Ici je suis dans la page des différents départements et je veux accéder aux professeurs.
        contenu2 = requests.get(lien_departement,headers=entete) #Accéder à la page
        page_departement = BeautifulSoup(contenu2.text, "html.parser") #Lire la page
        professeurs = page_departement.find_all("div", class_="vignette")
        for professeur in professeurs:
            n +=1   
            url_href = professeur.find("a")["href"] #Trouver le lien qui mènent vers la page du prof.e
            if not "/QKM%252fbavKTxUIk141GN77Uw__/" in url_href: #cet URL était un page "Poste Vacant," c'était la seule qui causait problème. 
                url_enseignants = "https://professeurs.uqam.ca" + url_href #Compléter la page avec l'url précédent
                contenu3 = requests.get(url_enseignants,headers=entete) #Accéder à la page
                page_prof = BeautifulSoup(contenu3.text, "html.parser") #Lire la page
                universite = "Université du Québec à Montréal"
                #print("<>" * 40)

                #Nom de l'enseignant.e --->
                nom_du_prof = page_prof.find("header",class_="entry-header").find("h1").text
                prenom_nom_famille = trouver_nom_du_prof(nom_du_prof)

                #Département --->
                departement_prof = page_prof.find("div", class_="unite contenu_icone")
                type_depart = trouver_departement_prof(departement_prof)
                
                #Poste --->
                poste_prof = page_prof.find("div", class_="titre_professeur")
                prof_poste = trouver_poste_prof(poste_prof)

                ### Ajouter le genre aurait été possible, avec le titre, mais cela peut aussi être fait à posteriori

                #Courriel --->
                courriel_prof = page_prof.find("div", class_="courriel contenu_icone")
                adresse_courriel = trouver_courriel_prof(courriel_prof)

                #Téléphone --->
                telephone_prof = page_prof.find("div", class_="telephone contenu_icone").contents[2].
                numero_tel = trouver_telephone_prof(telephone_prof)

                #Champ d'expertise --->
                expertise = page_prof.find("div", id="expertises")
                domaine_expertise = trouver_expertise(expertise)

                #Entretien média :
                entretenir_media = page_prof.find("div", class_="messageMedia contenu_icone")
                parler_media = parler_ou_non_media(entretenir_media)
                
                print(n, "Le petit train travaille...") ### Rigolo! :) Mais je préfère un affichage plus explicite: la variable «infos»
                infos = [universite, prenom_nom_famille, type_depart, prof_poste, adresse_courriel, numero_tel, domaine_expertise, parler_media, url_enseignants]
                print(infos) ### C'est toujours mieux de voir vraiment ce que notre script moissonne afin de repérer rapidement d'éventuelles erreurs et de nous donner une idée de l'endroit où le petit train est rendu
                creation_fichier.writerow(infos)

#Le document .csv nécessite quand même un nettoyage après coup, parce que certains professeurs reviennent deux fois. ### Bonne remarque! Oui, on dirait que le travail n'est jamais terminé avec des données!