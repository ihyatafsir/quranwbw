import json
import os

def parse_abdel_haleem(input_path, output_path):
    print(f"Reading from {input_path}")
    
    translations = {}
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split('|')
            if len(parts) >= 3:
                surah = parts[0]
                ayah = parts[1]
                # Join the rest in case there are pipe characters in the text
                text = '|'.join(parts[2:])
                
                key = f"{surah}_{ayah}"
                translations[key] = text
        
        print(f"Parsed {len(translations)} verses.")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully wrote JSON to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    input_file = "/home/absolut7/Documents/ghazali/ihyatafsir/data/translations/abdel_haleem.txt"
    output_file = "/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/assets/data/en_haleem.json"
    
    parse_abdel_haleem(input_file, output_file)
