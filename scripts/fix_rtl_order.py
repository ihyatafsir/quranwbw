import json
import os
import glob

def unreverse_string(s):
    # This is a bit tricky if there are combining marks.
    # We should treat [Base + any following Marks] as a single cluster, then reverse the order of clusters.
    import unicodedata
    
    clusters = []
    current_cluster = ""
    
    for char in s:
        if unicodedata.combining(char) or ord(char) in [0x650, 0x652, 0x651, 0x644, 0x671, 0x64f, 0x64e, 0x654, 0x655]: # Arabic marks
             current_cluster += char
        else:
            if current_cluster:
                clusters.append(current_cluster)
            current_cluster = char
            
    if current_cluster:
        clusters.append(current_cluster)
        
    # Now reverse clusters
    return "".join(clusters[::-1])

def process_all():
    std_allwords_path = "/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/allwords.json"
    spec_allwords_path = "/home/absolut7/Documents/allwords.json"
    surah_data_dir = "/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/surahs/data"
    
    with open(std_allwords_path, 'r') as f:
        std_allwords = json.load(f)
    with open(spec_allwords_path, 'r') as f:
        spec_allwords = json.load(f)
        
    std_map = {}
    for row in std_allwords:
        std_map[(row['sura'], row['ayah'], row['word'])] = row['en']
        
    spec_map = {}
    for row in spec_allwords:
        spec_map[(row['sura'], row['ayah'], row['word'])] = unreverse_string(row['en'])

    files = glob.glob(os.path.join(surah_data_dir, "*.json"))
    for file_path in files:
        with open(file_path, 'r') as f:
            surah_data = json.load(f)
            
        surah_num = int(os.path.basename(file_path).split('.')[0])
        modified = False
        
        for ayah_key, content in surah_data.items():
            ayah_num = int(ayah_key)
            for i, word in enumerate(content.get('w', [])):
                key = (surah_num, ayah_num, i+1)
                
                # Update 'd' (Top Line) with UN-REVERSED Special RTL
                if key in spec_map:
                    word['d'] = spec_map[key]
                    modified = True
                    
                # Update 'e' (Bottom Line) with Standard Translit
                if key in std_map:
                    word['e'] = std_map[key]
                    modified = True
                    
        if modified:
            with open(file_path, 'w') as f:
                json.dump(surah_data, f, ensure_ascii=False, separators=(',', ':'))

if __name__ == "__main__":
    process_all()
    print("Done un-reversing and updating JSONs.")
