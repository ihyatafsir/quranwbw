
import json
import os

DEEPSEEK_V3_RESULTS = '/home/absolut7/Documents/ihyalovesecond/deepseek_analysis_results.jsonl'
BOOK_META_FILE = '/home/absolut7/Documents/ihya_love/book_metadata.json'
OUTPUT_INDEX = '/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/ihya-index.html'

def normalize_filename(filename):
    if not filename: return ""
    base = filename.split('_')[-1]
    if base.endswith('.txt'): base = base[:-4]
    return base

def main():
    print("Generating Pure V3 Index...")
    
    book_meta = {}
    if os.path.exists(BOOK_META_FILE):
        with open(BOOK_META_FILE, 'r') as f:
            book_meta = json.load(f)

    entries = []
    with open(DEEPSEEK_V3_RESULTS, 'r') as f:
        for line in f:
            try:
                res = json.loads(line)
                if res['status'] == 'success' and res['analysis']['analysis_type'] == 'tafsir':
                    vk = res['custom_id']
                    if ':' in vk:
                        s_part, a_part = vk.split(':')
                        s_num = int(s_part)
                        a_sort = int(a_part.split('-')[0]) if '-' in a_part else int(a_part)
                        
                        entries.append({
                            'key': vk,
                            's': s_num,
                            'a': a_sort,
                            'eng': res['analysis']['english_text'],
                            'file': res.get('file', '')
                        })
            except: pass

    entries.sort(key=lambda x: (x['s'], x['a']))

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ihya Tafsir Pure V3 Index</title>
    <link rel="stylesheet" href="assets/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        body { background-color: #fcfaf2; padding-top: 50px; }
        .commentary-card { background: #fff; padding: 25px; margin-bottom: 25px; border-radius: 12px; border: 1px solid #e8e0c8; box-shadow: 0 4px 15px rgba(0,0,0,0.03); }
        .verse-key { color: #d4af37; font-weight: 700; font-family: 'Cinzel', serif; }
        .book-badge { background-color: #f4ecd8; color: #8a6d3b; border: 1px solid #d0c090; }
        .preview-text { color: #34495e; font-size: 1.05em; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="container" style="max-width: 900px;">
        <div class="text-center mb-5">
            <h1 class="display-4" style="color: #333; font-family: 'Cinzel', serif;">Ihya 'Ulum al-Din</h1>
            <p class="lead" style="color: #888;">Pure DeepSeek V3 Scholarly Index</p>
            <a href="index.html" class="btn btn-outline-gold">Return to Quran</a>
        </div>
        <div>
"""
    for e in entries:
        file_norm = normalize_filename(e['file'])
        book_display = file_norm.replace('.doc', '').replace('-', ' ')
        meta_key = next((k for k in book_meta if file_norm in k), None)
        if meta_key:
            info = book_meta[meta_key]
            book_display = info.get('english_title', book_display)
            if info.get('vol'): book_display = f"Vol {info['vol']}: {book_display}"

        html += f"""
            <div class="commentary-card">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="verse-key mb-0">Verse {e['key']}</h5>
                    <span class="badge book-badge">{book_display}</span>
                </div>
                <p class="preview-text">{e['eng'][:250]}...</p>
                <div class="text-right">
                    <a href="surahs/{e['s']}.html#{e['a']}" class="btn btn-sm btn-gold">View Full Commentary</a>
                </div>
            </div>
        """

    html += "</div></div></body></html>"
    with open(OUTPUT_INDEX, 'w') as f:
        f.write(html)
    print(f"Index generated with {len(entries)} entries.")

if __name__ == "__main__":
    main()
