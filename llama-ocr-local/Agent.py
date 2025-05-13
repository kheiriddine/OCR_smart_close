import os
import together

#os.environ["TOGETHER_API_KEY"] = "559efbb750f226382afa21e1fabf91dfde8e4f3854d854a889949037220c8d1b"  
with open("ocr_output_1.md", "r", encoding="utf-8") as f:
    content = f.read()

prompt = f"""
Tu es un agent intelligent qui extrait des informations financières structurées depuis des documents OCR.

Voici le texte extrait :

{content}

Ta tâche est de retourner un objet JSON avec deux champs :
1. `payment_info` : les infos de paiement, comme dans l'exemple ci-dessous.
2. `table` : une table combinée extraite à partir de toutes les tables visibles dans le texte , au format JSON (type pandas DataFrame).

Exemple de format :

{{
    "payment_info": {{
        "Nom Fournisseur": "...",
        "Adresse Fournisseur": "...",
        ...,
        "Total":...
    }},
    "table": [
        {{ "Colonne1": "valeur1", "Colonne2": "valeur2", ... }},
        ...
    ]
}}

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
