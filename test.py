from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")

# Créer un pipeline NER avec le modèle et le tokenizer
nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Utiliser le pipeline pour effectuer la reconnaissance d'entités nommées sur le texte
result = nlp("Apple est créée le 1er avril 1976 dans le garage de la maison d'enfance de Steve Jobs à Los Altos en Californie par Steve Jobs, Steve Wozniak et Ronald Wayne14, puis constituée sous forme de société le 3 janvier 1977 à l'origine sous le nom d'Apple Computer, mais pour ses 30 ans et pour refléter la diversification de ses produits, le mot « computer » est retiré le 9 janvier 2015.")
#result = nlp("Je reviens vers les voyageurs à destination de Beauvais. Départ 18h07. Votre TER est maintenant en cours de préparation en gare et sera affichée dans quelques minutes. le TER à destination de Beauvais départ 18h07 est en cours de préparation hier.")
#print(result)
# Parcourir la liste des entités nommées identifiées
for entity in result:
    print(f"Entité: {entity['word']}")
    print(f"Type: {entity['entity_group']}")
    print(f"Début: {entity['start']}, Fin: {entity['end']}")
    print(f"Score de confiance: {entity['score']}")
    print()

