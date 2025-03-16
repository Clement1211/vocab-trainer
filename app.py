from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Fonction pour charger les mots depuis words.json
def load_words():
    with open('words.json', 'r', encoding='utf-8') as f:
        return json.load(f)

words_data = load_words()

@app.route('/')
def accueil():
    ds_list = list(words_data.keys())  # ✅ Récupère toutes les catégories (ex: 'chicago', 'series')
    return render_template('accueil.html', ds_list=ds_list)  # ✅ Affiche les catégories disponibles

@app.route('/get_subcategories/<category>')
def get_subcategories(category):
    if category not in words_data:
        return jsonify([])  # ✅ Retourne une liste vide si la catégorie n'existe pas

    subcategories = list(words_data[category].keys())  # ✅ Récupère les sous-catégories (ex: 'Nom', 'Verbe', etc.)
    return jsonify(subcategories)

@app.route('/revision/<category>/<subcategory>')
def revision(category, subcategory):
    if category not in words_data or subcategory not in words_data[category]:
        return render_template('revision.html', category=category, subcategory=subcategory, mots=[])

    mots = [{"word": entry["translation"], "translation": entry["word"]}  # Inversion ici : traduction d'abord
            for entry in words_data[category][subcategory] if "translation" in entry]

    return render_template('revision.html', category=category, subcategory=subcategory, mots=mots)

if __name__ == '__main__':
    app.run(debug=True)
