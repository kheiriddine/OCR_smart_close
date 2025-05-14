import os
import together

#os.environ["TOGETHER_API_KEY"] = "559efbb750f226382afa21e1fabf91dfde8e4f3854d854a889949037220c8d1b"  
with open("ocr_output_1.md", "r", encoding="utf-8") as f:
    content = f.read()

prompt = f"""
Tu es un agent intelligent qui extrait des informations financières structurées depuis des documents OCR.

Voici le texte extrait :

{content}

Ta tâche est de retourner un objet JSON avec trois champs :
1. `company_name` : le nom de la société émettrice (trouvé dans l'en-tête/logo, généralement en haut de chaque page)
2. `payment_info` : les infos de paiement, comme dans l'exemple ci-dessous.
3. `table` : une table combinée extraite à partir de toutes les tables visibles dans le texte , au format JSON (type pandas DataFrame).

Exemple de format :

{{  "Nom Societe":"...", // nom de la société émettrice (pas le fournisseur)
    "payment_info": {{
        "Nom Fournisseur": "...",  // Nom exact du fournisseur bénéficiaire
        "Adresse Fournisseur": "...",
        ...,
        "Total":...
    }},
    "table": [
        {{ "Colonne1": "valeur1", "Colonne2": "valeur2", ... }},
        ...
    ]
}}
Règles de formatage STRICTES :
1. Nombres/montants : 
   - Toujours en format float (point comme séparateur décimal)
   - Supprimer les séparateurs de milliers
   - Exemple : "378 885,00 €" → 378885.00

2. Dates :
   - Toujours en format ISO français (JJ/MM/AAAA)

3. Numéros de référence :
   - Garder exactement comme dans le texte original
   - Ne pas modifier les tirets ou espaces
   - Exemple : "XXX-XXX-000-TOG-2867" → "XXX-XXX-000-TOG-2867"

4. Adresses :
   - Garder la casse originale
   - Ne pas modifier la ponctuation

Retourne uniquement le JSON & concatenater les deux tables des differents page existe dans le fichier .md .
"""

client = together.Together()
response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70b-Instruct-Turbo-Free",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=3000,
    temperature=0,
    stop=["\n\n"]
)

output = response.choices[0].message.content.strip()
output_file_path="extracted_output_1.json"
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(output)
print("Le contenu a été sauvegardé dans 'extracted_output_1.json'.")
