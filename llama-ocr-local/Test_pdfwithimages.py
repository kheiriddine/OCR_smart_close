import subprocess
import together
import os

def run_llama_ocr(pdf_dir, output_file, temp_images_dir, ocr_api_key):
    try:
        subprocess.run(["node", "llama_ocr_pdfsandimages.js", pdf_dir, output_file, temp_images_dir, ocr_api_key], check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None

def extract_info_from_ocr(ocr_output_file, together_api_key):
    if not ocr_output_file:
        print("No OCR output file provided.")
        return

    with open(ocr_output_file, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = f"""
    Tu es un agent intelligent qui extrait des informations financières structurées depuis des documents OCR.

    Voici le texte extrait :

    {content}

    Ta tâche est de retourner un objet JSON avec trois champs :
    1. `Nom Societe` : le nom de la société émettrice (trouvé dans l'en-tête/logo, généralement en haut de chaque page)
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

    client = together.Together(api_key=together_api_key)
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70b-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000,
        temperature=0,
        stop=["\n\n"]
    )

    output = response.choices[0].message.content.strip()
    output_file_path = "extracted_output_FF.json"
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Le contenu a été sauvegardé dans '{output_file_path}'.")

if __name__ == "__main__":
    pdf_dir = './Docs'
    output_file = 'ocr_output_FF.md'
    temp_images_dir = './temp_images'
    ocr_api_key = os.getenv('OCR_API_KEY')  # Set this environment variable
    together_api_key = os.getenv('TOGETHER_API_KEY')  # Set this environment variable

    if not ocr_api_key or not together_api_key:
        raise ValueError("API keys are not set. Please set the OCR_API_KEY and TOGETHER_API_KEY environment variables.")

    ocr_output_file = run_llama_ocr(pdf_dir, output_file, temp_images_dir, ocr_api_key)
    if ocr_output_file:
        extract_info_from_ocr(ocr_output_file, together_api_key)

