from text_comparaison import compare_sentences, compare_words

text1 = """Flash, info, trafic, ligne EP, madame, monsieur, bonjour et bienvenue en gare. Il est 17h31, alors pour 
moi, je vais vous faire un point sur la circulation. Actuellement, le trafic est fini sur l'ensemble de la ligne, 
mais je vous rappelle que jusqu'au 27 août, il n'y a pas de service jusqu'au 20 août. Le trafic est interrompu entre 
Fontaine-Méchelon et Massif-Alejo. Et jusqu'au 25 août, le trafic est interrompu entre Boulogne et Néroposon. 
Poursuivons en temps réel l'évolution de votre ligne. Je vous invite à consulter les applications Ile-de-France 
Mobilité, les sites transsino.com, ratp.fr, sncfconnect ou votre appli de mobilité. Je vous souhaite à tous et à 
toutes une agréable journée et un bon voyage."""
text2 = """Flash info trafic ligne B Madame, Monsieur, Bonjour et bienvenue en gare. Il est 17 h 31 l'heure pour moi 
de vous faire un point sur la circulation. Actuellement le trafic est fluide sur l'ensemble de la ligne mais je vous 
rappelle que jusqu'au 27 août Bagne n'est pas desservie jusqu au 20 août, le trafic est interrompu entre Fontaine 
Michalon, Massy Palaiseau et jusqu'au 25 août, le trafic est interrompu entre  Blois,Rennes et Robinson  pour suivre 
en temps réel l'évolution de votre ligne, je vous invite à consulter les applications Île-de-France mobilités des 
site Transilien.com, ratp.fr SNCF connectant votre appli de Mobilités, je vous souhaite à tous et à toutes une 
agréable journée, un pour voyage."""

print(compare_sentences(text1, [text2]))

print(compare_words("Chien", ["Chat", "Oiseau", "Cheval", "Canard", "cHieN"]))

