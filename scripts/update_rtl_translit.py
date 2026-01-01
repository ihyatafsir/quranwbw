import json
import os

def update_rtl_translit():
    # Load RETRANSLIT.txt
    with open('/home/absolut7/Documents/RETRANSLIT.txt', 'r', encoding='utf-8') as f:
        new_translit_lines = [line.strip() for line in f.readlines()]

    print(f"Loaded {len(new_translit_lines)} lines from RETRANSLIT.txt")

    total_words_json = 0
    words_processed = 0
    
    # Iterate through all 114 Surahs
    for surah_num in range(1, 115):
        json_path = f'/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/surahs/data/{surah_num}.json'
        
        if not os.path.exists(json_path):
            print(f"JSON not found: {json_path}")
            continue

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Count words first
        surah_words = 0
        
        # Traverse verses in order
        # Keys are strings "1", "2", etc.
        # Use str(i) for 1 to len(data) if keys are strict, but better to iterate sorted numeric keys
        sorted_keys = sorted([int(k) for k in data.keys() if k.isdigit()])
        
        for verse_id in sorted_keys:
            verse_data = data[str(verse_id)]
            if 'w' in verse_data:
                for word in verse_data['w']:
                    # Update 'e' field (Middle/Bottom line which is now RTL)
                    if words_processed < len(new_translit_lines):
                        new_val = new_translit_lines[words_processed]
                        # Only update if new_val is not empty, OR if we want to force empty?
                        # User said "replicate". But file has 27k empty lines.
                        # Assuming empty means "no data available", so keep old.
                        if new_val:
                            word['e'] = new_val
                        words_processed += 1
                    else:
                        print(f"Error: Ran out of translit lines at Surah {surah_num}, Verse {verse_id}")
                        break
                    
                    surah_words += 1
        
        total_words_json += surah_words
        
        # Save updated JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

    print(f"Total Words in JSON: {total_words_json}")
    print(f"Total Translit Lines Used: {words_processed}")
    
    if total_words_json != len(new_translit_lines):
        print("WARNING: Word count mismatch!")
        print(f"Diff: {total_words_json - len(new_translit_lines)}")

if __name__ == "__main__":
    update_rtl_translit()
