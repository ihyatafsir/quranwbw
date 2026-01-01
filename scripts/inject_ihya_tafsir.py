import json
import os
import re
from collections import defaultdict

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

def clean_book_filename(book_source):
    # Map "Vol1-book-10.doc" to "Vol1-Book-10.doc.txt" or similar found in books/
    # We copied files like "vol1_Vol1-book-10.doc.txt"
    # We should search the books dir for a match.
    
    # Simple heuristic: exact match in existing files
    base_name = book_source.replace('.doc', '.doc.txt')
    # Try with prefix "volX_" if needed, or just search
    return base_name

def find_book_file(book_source_raw):
    # book_source_raw e.g. "Vol1-book-10.doc"
    # target file e.g. "vol1_Vol1-book-10.doc.txt"
    
    # normalized search: lowercase, remove hyphens? 
    # Let's try to match "Vol1-book-10" part
    
    clean_src = book_source_raw.replace('.doc', '') # Vol1-book-10
    
    # List files in books dir
    books_dir = '/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/books'
    for fname in os.listdir(books_dir):
        if clean_src in fname:
            return fname
    return None

def inject_tafsir():
    master_path = '/home/absolut7/Documents/ihya_love/ihya_tafsir_master.json'
    print(f"Loading {master_path}...")
    with open(master_path, 'r', encoding='utf-8') as f:
        master_data = json.load(f)

    verse_map = defaultdict(list)
    
    print("Grouping and Mapping commentaries...")
    
    skipped_count = 0
    
    for item in master_data:
        s_id = str(item.get('surah', ''))
        a_id = str(item.get('ayah', ''))
        
        verse_key = item.get('verse_key', '')
        
        # Priority to Verse Key parsing if it's "Arabic: Num"
        if not s_id.isdigit():
             # Try parse from verse_key
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
        
        # If still not digit, try looking up s_id directly
        if not s_id.isdigit() and s_id in ARABIC_SURAH_MAP:
            s_id = str(ARABIC_SURAH_MAP[s_id])
            
        if not s_id.isdigit():
            # print(f"Skipping invalid key: {verse_key} (s={s_id})")
            skipped_count += 1
            continue
            
        try:
            s_num = int(s_id)
            if '-' in a_id:
                a_start = int(a_id.split('-')[0])
            else:
                a_start = int(a_id)
            
            key = (s_num, a_start)
            verse_map[key].append(item)
        except ValueError:
            skipped_count += 1
            continue

    print(f"Mapped {len(verse_map)} unique verses. Skipped {skipped_count} invalid entries.")

    total_injected = 0
    
    for surah_num in range(1, 115):
        json_path = f'/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/surahs/data/{surah_num}.json'
        
        if not os.path.exists(json_path):
            continue
            
        with open(json_path, 'r', encoding='utf-8') as f:
            surah_data = json.load(f)
            
        modified = False
        
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
                    book_src_raw = comm.get('book_source', 'Unknown Book')
                    book_src_display = book_src_raw.replace('.doc', '').replace('-', ' ')
                    english_text = comm.get('english_commentary', '')
                    arabic_text = comm.get('arabic_commentary', '')
                    
                    # Link to book
                    book_file = find_book_file(book_src_raw)
                    book_link = "#"
                    if book_file:
                        book_link = f"../books/{book_file}" # Relative to surah page (which is in surahs/ so go up ../books) NO: Surah pages are in surahs/. index is in root.
                        # Wait, surah pages are generated? No, main.js loads data.
                        # The HTML is rendered dynamically in main.js.
                        # If user is at /1.html (root) or /surahs/1.html?
                        # The file structure: quranwbw/surahs/1.html.
                        # So link should be: ../books/filename.
                    
                    if idx > 0:
                        html_parts.append("<hr style='border-top: 1px dashed #ddd; margin: 15px 0;'>")
                        
                    html_parts.append(f"<div class='ihya-entry'>")
                    
                    # Header: Badge + Link
                    html_parts.append(f"<div style='margin-bottom: 10px;'>")
                    if book_file:
                        html_parts.append(f"<a href='{book_link}' target='_blank' class='badge badge-light' style='color: #666; border: 1px solid #ddd; cursor: pointer; text-decoration: none;'>📖 {book_src_display}</a>")
                    else:
                        html_parts.append(f"<span class='badge badge-light' style='color: #666; border: 1px solid #ddd;'>{book_src_display}</span>")
                    html_parts.append("</div>") # End header
                    
                    # English Text
                    if english_text:
                        html_parts.append(f"<div class='ihya-text' style='font-size: 1.1em; line-height: 1.6; color: #333; margin-bottom: 10px;'>{english_text}</div>")
                    
                    # Arabic Text
                    if arabic_text:
                        html_parts.append(f"<div class='ihya-arabic' style='font-size: 1.2em; line-height: 1.8; color: #555; text-align: right; direction: rtl; font-family: \"Traditional Arabic\", serif; background: #fff; padding: 10px; border-radius: 4px; border: 1px solid #eee;'>{arabic_text}</div>")

                    html_parts.append("</div>")
                
                html_parts.append("</div>")
                
                full_html = "".join(html_parts)
                
                # Inject
                if 'a' not in surah_data[ayah_key]:
                    surah_data[ayah_key]['a'] = {}
                
                surah_data[ayah_key]['a']['ihya'] = full_html
                modified = True
                total_injected += 1
        
        if modified:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(surah_data, f, ensure_ascii=False, separators=(',', ':'))
                
    print(f"Injection complete. Injected commentaries into {total_injected} verses.")

if __name__ == "__main__":
    inject_tafsir()
