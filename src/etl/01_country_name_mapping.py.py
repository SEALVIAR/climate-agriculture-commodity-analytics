import pandas as pd
from rapidfuzz import fuzz, process
def comparar_paises(set1, set2, umbral=50):
    coincidencias = []

    for pais1 in set1:
        mejor_match = process.extractOne(
            pais1,
            set2,
            scorer=fuzz.token_sort_ratio
        )

        pais2, score, _ = mejor_match

        if score >= umbral:
            coincidencias.append({
                "pais_set1": pais1,
                "pais_set2": pais2,
                "confianza": score
            })

    return coincidencias
def agrupar_sets(set1, set2):
    letras = {c[0].upper() for c in set1 | set2}
    return {
        l: {
            "set1": {c for c in set1 if c.startswith(l)},
            "set2": {c for c in set2 if c.startswith(l)}
        }
        for l in sorted(letras)
    }

datos = pd.read_csv('C:\Users\fserl\knime-workspace\0-DATA\Datos_FAOSTAT\Datos_FAOSTAT_All_Data_NOFLAG.csv') #Dataset de FAOSTAT

paises_berkeley = set([
  "Afghanistan","Albania","Algeria","American Samoa","Andorra","Angola",
  "Anguilla","Antarctica","Antigua and Barbuda","Argentina","Armenia",
  "Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain",
  "Baker Island", "Bangladesh","Barbados","Belarus","Belgium","Belize",
  "Benin","Bhutan","Bolivia","Bonaire, Saint Eustatius and Saba",
  "Bosnia And Herzegovina","Botswana","Brazil","British Virgin Islands",
  "Bulgaria","Burkina Faso","Burma","Burundi","Cambodia","Cameroon","Canada",
  "Cape Verde","Cayman Islands","Central African Republic","Chad","Chile",
  "China","Christmas Island","Colombia","Congo",
  "Congo (Democratic Republic of the)","Costa Rica","Croatia","Cuba",
  "Cyprus","Czech Republic","Denmark (Europe)", "Djibouti", "Dominica",
  "Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea",
  "Eritrea", "Estonia","Ethiopia","Falkland Islands (Islas Malvinas)", 
  "Faroe Islands", "Federated States of Micronesia", "Fiji", "Finland",
  "France","France (Europe)","French Guiana","French Polynesia",
  "French Southern and Antarctic Lands","Gabon","Gambia","Gaza Strip",
  "Georgia","Germany","Ghana","Greece","Greenland","Grenada","Guadeloupe",
  "Guam","Guatemala","Guernsey","Guinea","Guinea-Bissau","Guyana","Haiti",
  "Honduras","Hungary","India","Indonesia","Iran","Iraq","Ireland",
  "Isle of man","Israel","Italy","Jamaica","Japan","Jersey","Jordan",
  "Kazakhstan","Kenya","Kuwait","Kyrgyzstan","Laos","Lebanon","Lesotho",
  "Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau",
  "Macedonia","Madagascar","Malawi","Malaysia","Mali","Malta","Mauritania",
  "Mauritius","Mayotte","Mexico","Monaco","Mongolia","Montenegro","Morocco",
  "Mozambique","Namibia","Nepal","Netherlands","New Zealand","Nicaragua",
  "Niger","Nigeria","North Korea","Norway","Oman","Pakistan","Palestina",
  "Panama","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico",
  "Qatar","Reunion","Romania","Russia","Rwanda","San Marino","Saudi Arabia",
  "Senegal","Serbia","Singapore","Slovakia","Slovenia","Somalia",
  "South Africa","South Korea","Spain","Sri Lanka","Sudan","Suriname",
  "Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand",
  "Tunisia","Turkey","Uganda","Ukraine","United Arab Emirates",
  "United Kingdom (Europe)","United States","Uruguay","Uzbekistan",
  "Venezuela","Virgin Islands","Vietnam","Yemen","Zambia","Zimbabwe",
]) #Candidatos a descargar de Berkeley Eartg

paises_faostat = set(datos['Area'].unique()) #Paises de faostat

candidatos = paises_faostat.intersection(paises_berkeley) #Paises que si o si tienen su par en el otro dataset

analizar_faostat = paises_faostat.difference(candidatos) #Paises que no tienen un match
analizar_berkeley = paises_berkeley.difference(candidatos) #Paises que no tienen match

analizar_alfabeto = agrupar_sets(analizar_faostat,analizar_berkeley)

#Verificando incialmente letra por letra
for letra in analizar_alfabeto.keys():
    print(analizar_alfabeto[letra]['set1'])
    print("\n")
    print(analizar_alfabeto[letra]['set2'])
    print("\n")

#Clave ---- Faostat
#Valor ---- Berkeley

claves = set(['Bosnia and Herzegovina','Bolivia (Plurinational State of)','Cabo Verde','Czechia','Denmark','Iran (Islamic Republic of)',
          "Lao People's Democratic Republic",'North Macedonia','Netherlands (Kingdom of the)','Palestine','Türkiye','Russian Federation','Syrian Arab Republic',
          'United Republic of Tanzania','United States of America','United Kingdom of Great Britain and Northern Ireland','Viet Nam',
          'Venezuela (Bolivarian Republic of)','Micronesia (Federated States of)','Democratic Republic of the Congo','Réunion'])
valores = set(['Bosnia And Herzegovina','Bolivia','Cape Verde','Czech Republic','Denmark (Europe)','Iran','Laos','Macedonia','Netherlands','Palestina','Turkey',
           'Russia','Syria','Tanzania','United States','United Kingdom (Europe)','Vietnam', 'Venezuela','Federated States of Micronesia',
               'Congo (Democratic Republic of the)','Reunion'])


analizar_faostat2 = analizar_faostat.difference(claves) #Paises que no tienen un mathc
analizar_berkeley2 = analizar_berkeley.difference(valores) #Paises que no tienen mathc

diccionario = comparar_paises(analizar_faostat2, analizar_berkeley2, umbral=70)
print(diccionario)
print("\n")

candidatos = list(candidatos.union(valores))
print(candidatos)

