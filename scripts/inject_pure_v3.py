
import json
import os
import re
from collections import defaultdict

# Mapping of Arabic Surah Names to Numbers for legacy parsing if needed
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

DEEPSEEK_V3_RESULTS = '/home/absolut7/Documents/ihyalovesecond/deepseek_analysis_results.jsonl'
BOOK_META_FILE = '/home/absolut7/Documents/ihya_love/book_metadata.json'
SURAH_DATA_DIR = '/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/surahs/data'
BOOKS_DIR = '/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/books'

def normalize_filename(filename):
    """Normalize 'vol1_Vol1-book-9.doc.txt' to 'Vol1-book-9.doc'"""
    if not filename: return ""
    base = filename.split('_')[-1]
    if base.endswith('.txt'): base = base[:-4]
    return base

def find_book_file(book_source_raw):
    clean_src = book_source_raw.replace('.doc', '')
    if not os.path.exists(BOOKS_DIR): return None
    for fname in os.listdir(BOOKS_DIR):
        if clean_src in fname: return fname
    return None

def main():
    print(f"Loading Pure V3 Results from {DEEPSEEK_V3_RESULTS}...")
    
    # Load Metadata
    book_meta = {}
    if os.path.exists(BOOK_META_FILE):
        with open(BOOK_META_FILE, 'r') as f:
            book_meta = json.load(f)

    verse_map = defaultdict(list)
    results_count = 0
    tafsir_count = 0
    
    with open(DEEPSEEK_V3_RESULTS, 'r') as f:
        for line in f:
            try:
                res = json.loads(line)
                results_count += 1
                if res['status'] == 'success' and res['analysis']['analysis_type'] == 'tafsir':
                    tafsir_count += 1
                    vk = res['custom_id']
                    # Parse vk (e.g., "73:7")
                    if ':' in vk:
                        s_part, a_part = vk.split(':')
                        s_num = int(s_part)
                        # Handle range like "39-40"
                        if '-' in a_part:
                            a_num = int(a_part.split('-')[0])
                        else:
                            a_num = int(a_part)
                        
                        verse_map[(s_num, a_num)].append({
                            'arabic': res['analysis']['arabic_snippet'],
                            'english': res['analysis']['english_text'],
                            'file': res.get('file', '')
                        })
            except Exception as e:
                pass

    print(f"Found {tafsir_count} pure tafsir entries for {len(verse_map)} unique verses.")

    # Reset Website Data (Clear old injections)
    print("Clearing old Ihya commentaries and injecting Pure V3...")
    for s_num in range(1, 115):
        json_path = os.path.join(SURAH_DATA_DIR, f"{s_num}.json")
        if not os.path.exists(json_path): continue
        
        with open(json_path, 'r', encoding='utf-8') as f:
            surah_data = json.load(f)
        
        modified = False
        for ayah_key in list(surah_data.keys()):
            if not ayah_key.isdigit(): continue
            ayah_num = int(ayah_key)
            
            # ALWAYS clear existing 'ihya' field to ensure purity
            if 'a' in surah_data[ayah_key] and 'ihya' in surah_data[ayah_key]['a']:
                del surah_data[ayah_key]['a']['ihya']
                modified = True
            
            target_key = (s_num, ayah_num)
            if target_key in verse_map:
                comms = verse_map[target_key]
                
                html_parts = []
                html_parts.append("<div class='ihya-container' style='margin-top: 20px; padding: 15px; background-color: #fcfaf2; border-left: 4px solid #d4af37; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>")
                html_parts.append("<h4 style='color: #d4af37; margin-bottom: 15px; font-family: \"Cinzel\", serif; font-size: 1.2em;'>Ihya 'Ulum al-Din <span style='font-size: 0.8em; color: #888;'>(Verbatim V3)</span></h4>")
                
                for idx, c in enumerate(comms):
                    file_norm = normalize_filename(c['file'])
                    book_display = file_norm.replace('.doc', '').replace('-', ' ')
                    
                    # Metadata lookup
                    meta_key = next((k for k in book_meta if file_norm in k), None)
                    if meta_key:
                        info = book_meta[meta_key]
                        book_display = info.get('english_title', book_display)
                        vol = info.get('vol', '')
                        if vol: book_display = f"Vol {vol}: {book_display}"
                    
                    book_file = find_book_file(file_norm)
                    book_link = f"../books/{book_file}" if book_file else "#"

                    if idx > 0:
                        html_parts.append("<hr style='border-top: 1px dashed #e0d0a0; margin: 20px 0;'>")

                    html_parts.append("<div class='ihya-entry'>")
                    html_parts.append(f"<div style='margin-bottom: 12px;'>")
                    html_parts.append(f"<a href='{book_link}' target='_blank' class='badge' style='background-color: #f4ecd8; color: #8a6d3b; border: 1px solid #d0c090; padding: 5px 10px; font-weight: 500;'>📖 {book_display}</a>")
                    html_parts.append("</div>")
                    
                    html_parts.append(f"<div class='ihya-text' style='font-size: 1.15em; line-height: 1.7; color: #2c3e50; margin-bottom: 12px; font-family: \"Georgia\", serif;'>{c['english']}</div>")
                    html_parts.append(f"<div class='ihya-arabic' style='font-size: 1.35em; line-height: 2; color: #1a1a1a; text-align: right; direction: rtl; font-family: \"Traditional Arabic\", \"Noorehuda\", serif; background: #fff; padding: 15px; border-radius: 6px; border: 1px solid #e8e0c8;'>{c['arabic']}</div>")
                    html_parts.append("</div>")

                html_parts.append("</div>")
                
                if 'a' not in surah_data[ayah_key]: surah_data[ayah_key]['a'] = {}
                surah_data[ayah_key]['a']['ihya'] = "".join(html_parts)
                modified = True

        if modified:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(surah_data, f, ensure_ascii=False, separators=(',', ':'))

    print("Website updated with Pure V3 data.")

if __name__ == "__main__":
    main()
