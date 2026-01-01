import json
import os

def generate_index():
    # Load Master JSON
    with open('/home/absolut7/Documents/ihya_love/ihya_tafsir_master.json', 'r', encoding='utf-8') as f:
        master_data = json.load(f)

    # Sort key: Surah then Ayah
    # Note: verse_key is "73:7". We need to parse.
    # Sort key: Surah then Ayah
    def sort_key(item):
        v_key = item.get('verse_key', '0:0')
        s_id = item.get('surah', '0')
        a_id = item.get('ayah', '0')
        
        # Try to parse numeric surah
        try:
            s_num = int(s_id)
        except ValueError:
            s_num = 0
        
        # Try to parse numeric ayah
        try:
            if isinstance(a_id, str) and '-' in a_id:
                a_id = a_id.split('-')[0]
            a_num = int(a_id)
        except ValueError:
            a_num = 0
            
        return (s_num, a_num)

    sorted_data = sorted(master_data, key=sort_key)

    # Generate HTML
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ihya Tafsir Index - QuranWBW</title>
    <link rel="stylesheet" href="assets/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        .index-container { max-width: 1200px; margin: 40px auto; padding: 20px; }
        .verse-row { border-bottom: 1px solid #eee; padding: 15px 0; }
        .verse-key { font-weight: bold; color: #d4af37; }
        .book-source { color: #666; font-size: 0.9em; }
        .commentary-preview { color: #444; margin-top: 5px; font-size: 0.95em; }
        .nav-link { color: #333; }
        .back-link { margin-bottom: 20px; display: inline-block; }
    </style>
</head>
<body data-theme="light">
    <div class="container index-container">
        <a href="index.html" class="back-link">&larr; Back to Home</a>
        <h1>Ihya Tafsir Index</h1>
        <p class="lead">Chronological list of Quranic verses mentioned in the Ihya 'Ulum al-Din.</p>
        
        <div class="list-group">
"""
    
    for item in sorted_data:
        key = item.get('verse_key')
        
        surah_id = item.get('surah')
        ayah_id = item.get('ayah')
        # Clean ayah range if exists
        ayah_start = ayah_id.split('-')[0] if '-' in ayah_id else ayah_id
        
        book_src = item.get('book_source', 'Unknown Book')
        eng_comm = item.get('english_commentary') or ''
        # Truncate commentary
        preview = (eng_comm[:200] + '...') if len(eng_comm) > 200 else eng_comm
        
        # Format Book Name (simple parse)
        # "Vol1-book-10.doc" -> "Vol 1, Book 10"
        vol = item.get('vol', '?')
        # Handle book_src being None
        if not book_src: book_src = "Unknown"
        book_clean = book_src.replace('.doc', '').replace('-', ' ')
        
        link = f"surahs/{surah_id}.html#{ayah_start}"
        
        html_content += f"""
        <div class="list-group-item verse-row">
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1 verse-key">Verse {key}</h5>
                <small class="book-source">{book_clean}</small>
            </div>
            <p class="mb-1 commentary-preview">{preview}</p>
            <a href="{link}" class="btn btn-sm btn-outline-warning mt-2">Go to Verse</a>
        </div>
"""

    html_content += """
        </div>
    </div>
</body>
</html>
"""

    with open('/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/ihya-index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Generated ihya-index.html with", len(sorted_data), "entries.")

if __name__ == "__main__":
    generate_index()
