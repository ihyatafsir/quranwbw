import json
import os

# Mapping of Arabic Surah Names to Numbers
ARABIC_SURAH_MAP = {
    "الفاتحة": 1, "البقرة": 2, "آل عمران": 3, "النساء": 4, "المائدة": 5, "الأنعام": 6, "الأعراف": 7, "الأنفال": 8, "التوبة": 9, "يونس": 10,
    "هود": 11, "يوسف": 12, "الرعد": 13, "ابراهيم": 14, "إبراهيم": 14, "الحجر": 15, "النحل": 16, "الإسراء": 17, "الكهف": 18, "مريم": 19, "طه": 20,
    "الأنبياء": 21, "الحج": 22, "المؤمنون": 23, "النور": 24, "الفرقان": 25, "الشعراء": 26, "النمل": 27, "القصص": 28, "العنكبوت": 29, "الروم": 30,
    "لقمان": 31, "السجدة": 32, "الأحزاب": 33, "سبأ": 34, "فاطر": 35, "يس": 36, "الصافات": 37, "ص": 38, "الزمر": 39, "غافر": 40,
    "فصلت": 41, "الشورى": 42, "الزخرف": 43, "الدخان": 44, "الجاثية": 45, "الأحقاف": 46, "محمد": 47, "الفتح": 48, "الحجرات": 49, "ق": 50,
    "الذاريات": 51, "الطور": 52, "النجم": 53, "القمر": 54, "الرحمن": 55, "الواقعة": 56, "الحديد": 57, "المجادلة": 58, "الحشر": 59, "الممتحنة": 60,
    "الصف": 61, "الجمعة": 62, "المنافقون": 63, "التغابن": 64, "الطلاق": 65, "التحريم": 66, "الملك": 67, "القلم": 68, "الحاقة": 69, "المعارج": 70,
    "نوح": 71, "الجن": 72, "المزمل": 73, "المدثر": 74, "القيامة": 75, "الانسان": 76, "الإنسان": 76, "المرسلات": 77, "النبأ": 78, "النازعات": 79, "عبس": 80,
    "التكوير": 81, "الانفطار": 82, "المطففين": 83, "الانشقاق": 84, "البروج": 85, "الطارق": 86, "الأعلى": 87, "الغاشية": 88, "الفجر": 89, "البلد": 90,
    "الشمس": 91, "الليل": 92, "الضحى": 93, "الشرح": 94, "التين": 95, "العلق": 96, "القدر": 97, "البينة": 98, "الزلزلة": 99, "العاديات": 100,
    "القارعة": 101, "التكاثر": 102, "العصر": 103, "الهمزة": 104, "الفيل": 105, "قريش": 106, "الماعون": 107, "الكوثر": 108, "الكافرون": 109, "النصر": 110,
    "المسد": 111, "الاخلاص": 112, "الإخلاص": 112, "الفلق": 113, "الناس": 114
}

def generate_index():
    # Load Master JSON
    with open('/home/absolut7/Documents/ihya_love/ihya_tafsir_master.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Load Book Metadata
    meta_path = '/home/absolut7/Documents/ihya_love/book_metadata.json'
    print(f"Loading {meta_path}...")
    book_meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            book_meta = json.load(f)

    # Filter and Sort
    # We want to group by verse key and sort by Surah/Ayah order
    
    # Helper to parse key
    def parse_key(item):
        s_id = str(item.get('surah', ''))
        a_id = str(item.get('ayah', ''))
        verse_key = item.get('verse_key', '')

        if not s_id.isdigit():
             if ':' in verse_key:
                 parts = verse_key.split(':')
                 s_part = parts[0].strip()
                 a_part = parts[1].strip()
                 if s_part in ARABIC_SURAH_MAP:
                     s_id = str(ARABIC_SURAH_MAP[s_part])
                     a_id = a_part
                 elif s_part.isdigit():
                     s_id = s_part
                     a_id = a_part
        
        if not s_id.isdigit() and s_id in ARABIC_SURAH_MAP:
            s_id = str(ARABIC_SURAH_MAP[s_id])
            
        if s_id.isdigit():
            try:
                s_num = int(s_id)
                if '-' in str(a_id):
                    a_num = int(str(a_id).split('-')[0])
                else:
                    a_num = int(a_id)
                return s_num, a_num, f"{s_num}:{a_num}"
            except ValueError:
                pass
        return 999, 999, "Unknown"

    processed_items = []
    
    for item in data:
        s, a, k = parse_key(item)
        if k == "Unknown":
            continue
            
        item['sort_key'] = (s, a)
        item['clean_key'] = k
        processed_items.append(item)
        
    # Sort
    processed_items.sort(key=lambda x: x['sort_key'])
    
    print(f"Processed {len(processed_items)} valid entries.")

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ihya Tafsir Index</title>
    <link rel="stylesheet" href="assets/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        body { background-color: #f8f9fa; padding-top: 20px; }
        .commentary-card { background: #fff; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .verse-key { color: #d4af37; font-weight: bold; }
        .book-badge { font-size: 0.8em; opacity: 0.8; }
        .preview-text { color: #555; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row mb-4">
            <div class="col-12 text-center">
                <h1 class="display-4">Ihya 'Ulum al-Din Tafsir Index</h1>
                <p class="lead">Chronological index of verse commentaries by Imam Al-Ghazali</p>
                <a href="index.html" class="btn btn-outline-primary">Back to Quran</a>
            </div>
        </div>
        
        <div class="row">
            <div class="col-12">
"""

    for item in processed_items:
        key = item['clean_key']
        s_num, a_num = item['sort_key']
        
        
        book_src_raw = item.get('book_source', 'Unknown Book')
        book_src_display = book_src_raw
        
        if book_src_raw in book_meta:
            book_info = book_meta[book_src_raw]
            book_src_display = book_info.get('english_title', book_src_raw)
            vol = book_info.get('vol', '')
            if vol:
                book_src_display = f"Vol {vol}: {book_src_display}"
        else:
             book_src_display = book_src_raw.replace('.doc', '').replace('-', ' ')
             
        comm_text = item.get('english_commentary', '')
        if not comm_text:
            comm_text = "See Arabic commentary."
            
        html_content += f"""
                <div class="commentary-card">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="mb-1 verse-key">Verse {key}</h5>
                        <span class="badge badge-secondary book-badge">{book_src_display}</span>
                    </div>
                    <p class="preview-text">{comm_text[:200]}...</p>
                    <a href="surahs/{s_num}.html#{a_num}" class="btn btn-sm btn-gold mt-2">Go to Verse</a>
                </div>
        """

    html_content += """
            </div>
        </div>
    </div>
</body>
</html>"""

    with open('/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/ihya-index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Generated ihya-index.html with {len(processed_items)} entries.")

if __name__ == "__main__":
    generate_index()
