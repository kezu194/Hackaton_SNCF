from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

def detect_locations(sentence):
    # Charger le tokenizer et le modèle NER
    tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
    model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")
    
    # Créer un pipeline NER avec le modèle et le tokenizer
    nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    
    # Utiliser le pipeline pour effectuer la reconnaissance d'entités nommées sur le texte
    result = nlp(sentence)
    
    # Initialiser une liste pour stocker les informations sur les localisations détectées
    locations = []
    
    # Parcourir la liste des entités nommées identifiées
    for entity in result:
        # Vérifier si l'entité est une localisation
        if entity['entity_group'] == 'LOC':
            # Stocker les informations sur la localisation dans la liste
            location_info = {
                'word': entity['word'],
                'start': entity['start'],
                'end': entity['end'],
                'score': entity['score']
            }
            locations.append(location_info)
    
    return locations

# Test de la fonction avec une phrase
sentence = "Apple est créée le 1er avril 1976 dans le garage de la maison d'enfance de Steve Jobs à Los Altos en Californie par Steve Jobs, Steve Wozniak et Ronald Wayne14, puis constituée sous forme de société le 3 janvier 1977 à l'origine sous le nom d'Apple Computer, mais pour ses 30 ans et pour refléter la diversification de ses produits, le mot « computer » est retiré le 9 janvier 2015."
locations = detect_locations(sentence)

# Afficher les informations sur les localisations détectées
for location in locations:
    print(f"Localisation: {location['word']}")
    print(f"Début: {location['start']}, Fin: {location['end']}")
    print(f"Score de confiance: {location['score']}")
    print()
