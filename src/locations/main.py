from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

from .text_comparaison.compare import compare_sentences

#from src.text_comparaison.libs import remove_stop_words, list_words, count_words, calculate_similarities

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

def compare_locations_with_dataset(locations, dataset):
    # Initialiser une liste pour stocker les pourcentages de similarité
    similarities = []
    
    # Comparer chaque localisation avec les localisations de l'ensemble de données
    for location in locations:
        # Comparer la localisation avec chaque localisation de l'ensemble de données
        similarity_scores = compare_sentences(location['word'], dataset)
        
        # Ajouter le pourcentage de similarité le plus élevé à la liste des similarités
        max_similarity = max(similarity_scores)
        similarities.append(max_similarity)
    
    return similarities

# Test de la fonction avec une phrase
sentence = "Apple est créée le 1er avril 1976 dans le garage de la maison d'enfance de Steve Jobs à Los Altos en Californie par Steve Jobs, Steve Wozniak et Ronald Wayne14, puis constituée sous forme de société le 3 janvier 1977 à l'origine sous le nom d'Apple Computer, mais pour ses 30 ans et pour refléter la diversification de ses produits, le mot « computer » est retiré le 9 janvier 2015."
locations = detect_locations(sentence)

# Exemple de dataset de localisations à comparer
dataset = ["Los Altos", "Californie", "Beauvais", "Paris"]

# Comparer les localisations détectées avec le dataset
similarities = compare_locations_with_dataset(locations, dataset)

# Afficher les résultats
for i, location in enumerate(locations):
    print(f"Localisation: {location['word']}")
    print(f"Début: {location['start']}, Fin: {location['end']}")
    print(f"Score de confiance: {location['score']}")
    print(f"Pourcentage de similarité avec le dataset: {similarities[i]}%")
    print()
