import json
import os
from collections import defaultdict

def inject_tafsir():
    # 1. Load Master Data
    master_path = '/home/absolut7/Documents/ihya_love/ihya_tafsir_master.json'
    print(f"Loading {master_path}...")
    with open(master_path, 'r', encoding='utf-8') as f:
        master_data = json.load(f)

    # 2. Group by Verse Key (surah:ayah)
    # Be careful with verse_keys. Some are "2:255", some might vary.
    # We will use numeric surah and ayah for robust matching.
    
    verse_map = defaultdict(list)
    
    print("Grouping commentaries...")
    for item in master_data:
        s_id = item.get('surah')
        a_id = item.get('ayah')
        
        if not s_id or not a_id:
            continue
            
        # Handle ayah ranges if needed, or just map to start ayah?
        # User said "fix ihyatafsir", usually mapped to specific verse.
        # If 'ayah' is '255', it maps to verse 255.
        # If 'ayah' is '20-22', we might map to 20? 
        # For now, let's map to the string found in JSON. 
        # But JSON keys are strings "1", "2".
        
        # Normalize keys
        try:
            s_num = int(s_id)
            # handle ayah ranges by taking the first one for injection target
            if '-' in str(a_id):
                a_start = int(str(a_id).split('-')[0])
            else:
                a_start = int(a_id)
            
            key = (s_num, a_start)
            verse_map[key].append(item)
        except ValueError:
            print(f"Skipping invalid key: {s_id}:{a_id}")
            continue

    print(f"Found commentaries for {len(verse_map)} unique verses.")

    # 3. Inject into Surah JSONs
    total_injected = 0
    
    for surah_num in range(1, 115):
        json_path = f'/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/surahs/data/{surah_num}.json'
        
        if not os.path.exists(json_path):
            continue
            
        with open(json_path, 'r', encoding='utf-8') as f:
            surah_data = json.load(f)
            
        modified = False
        
        # surah_data keys are "1", "2", etc representing Ayah number
        for ayah_key in list(surah_data.keys()):
            if not ayah_key.isdigit():
                continue
                
            ayah_num = int(ayah_key)
            target_key = (surah_num, ayah_num)
            
            if target_key in verse_map:
                commentaries = verse_map[target_key]
                
                # Build HTML
                html_parts = []
                html_parts.append("<div class='ihya-container' style='margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-left: 4px solid #d4af37; border-radius: 4px;'>")
                html_parts.append("<h4 style='color: #d4af37; margin-bottom: 15px; font-family: \"Cinzel\", serif;'>Ihya 'Ulum al-Din Commentary</h4>")
                
                for idx, comm in enumerate(commentaries):
                    book_src = comm.get('book_source', 'Unknown Book').replace('.doc', '').replace('-', ' ')
                    text = comm.get('english_commentary', '')
                    
                    if idx > 0:
                        html_parts.append("<hr style='border-top: 1px dashed #ddd; margin: 15px 0;'>")
                        
                    html_parts.append(f"<div class='ihya-entry'>")
                    html_parts.append(f"<span class='badge badge-light' style='color: #666; border: 1px solid #ddd; margin-bottom: 8px;'>{book_src}</span>")
                    html_parts.append(f"<div class='ihya-text' style='font-size: 1.1em; line-height: 1.6; color: #333;'>{text}</div>")
                    html_parts.append("</div>")
                
                html_parts.append("</div>")
                
                full_html = "".join(html_parts)
                
                # Inject
                if 'a' not in surah_data[ayah_key]:
                    surah_data[ayah_key]['a'] = {}
                
                # Overwrite or set
                surah_data[ayah_key]['a']['ihya'] = full_html
                modified = True
                total_injected += 1
        
        if modified:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(surah_data, f, ensure_ascii=False, separators=(',', ':'))
                
    print(f"Injection complete. Injected commentaries into {total_injected} verses.")

if __name__ == "__main__":
    inject_tafsir()
