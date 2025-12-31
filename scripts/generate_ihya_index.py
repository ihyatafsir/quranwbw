import json
import os
import re

# Paths
WWW_PATH = '/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw'
MASTER_DATA_PATH = '/home/absolut7/Documents/ihya_love/ihya_tafsir_master.json'
BOOK_METADATA_PATH = '/home/absolut7/Documents/ihya_love/book_metadata.json'
INDEX_HTML_PATH = os.path.join(WWW_PATH, 'index.html')
OUTPUT_PATH = os.path.join(WWW_PATH, 'assets/data/ihya_index.json')

def get_surah_mapping():
    mapping = {}
    with open(INDEX_HTML_PATH, 'r') as f:
        content = f.read()
    
    # regex to find <span class="index-surah-no">NO</span>...<span class="index-surahname-ar">NAME</span>
    # Note: index.html is minified or very dense, so we search globally
    matches = re.finditer(r'<span class="index-surah-no">(\d+)</span>.*?<span class="index-surahname-ar">(.*?)</span>', content)
    for m in matches:
        no = int(m.group(1))
        name = m.group(2).strip()
        mapping[name] = no
    return mapping

def generate_index():
    # Load data
    with open(MASTER_DATA_PATH, 'r') as f:
        master_data = json.load(f)
    
    with open(BOOK_METADATA_PATH, 'r') as f:
        book_metadata = json.load(f)

    surah_map = get_surah_mapping()
    index = []
    
    for entry in master_data:
        # Some entries might have empty commentary
        if not entry.get('english_commentary') or entry['english_commentary'].strip() == "":
            continue
            
        book_key = entry.get('book_source')
        book_name = "Tafsir Al-Ihya"
        if book_key in book_metadata:
            book_name = book_metadata[book_key].get('english_title', book_name)
        
        surah_val = entry['surah']
        if isinstance(surah_val, str) and not surah_val.isdigit():
            surah_num = surah_map.get(surah_val)
            if not surah_num:
                print(f"Warning: Could not map surah name '{surah_val}' for verse {entry['verse_key']}")
                continue
        else:
            surah_num = int(surah_val)

        ayah_val = entry['ayah']
        
        index.append({
            "verse_key": entry['verse_key'],
            "surah": surah_num,
            "ayah": ayah_val,
            "book": book_name,
            "arabic": entry.get('arabic_commentary', ""),
            "english": entry.get('english_commentary', "")
        })

    # Sort by surah and ayah (numerically)
    def sort_key(x):
        surah = x['surah']
        ayah_str = str(x['ayah'])
        if '-' in ayah_str:
            ayah = int(ayah_str.split('-')[0])
        else:
            try:
                ayah = int(ayah_str)
            except ValueError:
                ayah = 0 # Fallback
        return (surah, ayah)

    index.sort(key=sort_key)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"Index generated with {len(index)} entries at {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_index()
