import json
import os
import glob

def load_allwords(path):
    print(f"Loading allwords from {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Index by (sura, ayah) -> list of words sorted by word index
    grouped = {}
    for entry in data:
        sura = entry.get('sura')
        ayah = entry.get('ayah')
        word_idx = entry.get('word')
        
        if sura is None or ayah is None or word_idx is None:
            continue
            
        key = (sura, ayah)
        if key not in grouped:
            grouped[key] = []
        
        grouped[key].append(entry)
        
    # Sort each list by word index to ensure 1, 2, 3... order
    for key in grouped:
        grouped[key].sort(key=lambda x: x['word'])
        
    print(f"Loaded allwords data for {len(grouped)} verses.")
    return grouped

def update_surah_files(data_dir, allwords_map):
    files = glob.glob(os.path.join(data_dir, "*.json"))
    print(f"Found {len(files)} surah files in {data_dir}")
    
    for file_path in files:
        filename = os.path.basename(file_path)
        # Extract surah number from filename "1.json" -> 1
        try:
            surah_num = int(filename.split('.')[0])
        except ValueError:
            print(f"Skipping {filename}, not a number.")
            continue
            
        print(f"Processing Surah {surah_num}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            surah_data = json.load(f)
            
        modified = False
        
        # Iterate over ayahs in the surah file
        # surah_data structure: {"1": {"w": [...], "a": ...}, "2": ...}
        for ayah_key, content in surah_data.items():
            ayah_num = int(ayah_key)
            w_list = content.get('w', [])
            
            allwords_entries = allwords_map.get((surah_num, ayah_num))
            
            if not allwords_entries:
                # print(f"Warning: No allwords data for {surah_num}:{ayah_num}")
                continue
                
            if len(w_list) != len(allwords_entries):
                print(f"Mismatch {surah_num}:{ayah_num} - Existing words: {len(w_list)}, New words: {len(allwords_entries)}")
                # We will try to update as many as match, taking the min length
            
            limit = min(len(w_list), len(allwords_entries))
            
            for i in range(limit):
                existing_word = w_list[i]
                new_data = allwords_entries[i]
                
                # Verify indices match (optional, but good for sanity)
                # new_data['word'] should ideally be i+1
                
                # Update fields
                # 'd' (transliteration) <- 'en' from allwords
                # 'e' (meaning) <- 'in' from allwords
                # Update transliteration (d)
                if 'en' in new_data:
                    existing_word['d'] = new_data['en']
                    modified = True
                
                # Update translation (e) - User requested 'en' column (replacing previous 'in')
                if 'en' in new_data:
                    existing_word['e'] = new_data['en'] # Use EN for translation as well
                    modified = True
                    
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(surah_data, f, ensure_ascii=False, separators=(',', ':'))
            # print(f"Updated {filename}")
        else:
            print(f"No changes for {filename}")

if __name__ == "__main__":
    allwords_path = "/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/allwords.json"
    surah_data_dir = "/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/surahs/data"
    
    if not os.path.exists(allwords_path):
        print(f"Error: {allwords_path} not found.")
        exit(1)
        
    allwords_map = load_allwords(allwords_path)
    update_surah_files(surah_data_dir, allwords_map)
