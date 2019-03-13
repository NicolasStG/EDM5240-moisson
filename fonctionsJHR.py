def trouver_nom_du_prof(nom_du_prof):
    if nom_du_prof is None:
        return ""
    else:
        return nom_du_prof.strip()

def trouver_departement_prof(departement_prof):
    if departement_prof is None:
        return ""
    else:
        return departement_prof.find("a").text

def trouver_poste_prof(poste_prof):
    if poste_prof is None:
        return ""
    else:
        return poste_prof.text

def trouver_courriel_prof(courriel_prof):
    if courriel_prof is None:
        return ""
    else : 
        return courriel_prof.find("a").text

def trouver_telephone_prof(telephone_prof):
    if telephone_prof is None:
        return ""
    else :
        return telephone_prof[telephone_prof.find(":")+2:].strip() ### J'ai ajouté un strip ici

def trouver_expertise(expertise):
   if expertise:
       if ',' in expertise.find("ul").get_text():
         return "\n".join(expertise.find("ul").text.split(",")).replace(".","")
       else:
         return expertise.find("ul").text
   else:
       return ""

def parler_ou_non_media(entretenir_media):
    if entretenir_media is None:
        return ""
    else:
        return entretenir_media.text