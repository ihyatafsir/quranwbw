import json
import os
import re

# Chronological Surah Order (Egyptian Tradition)
CHRONOLOGICAL_ORDER = [
    96, 68, 73, 74, 1, 111, 81, 87, 92, 89, 93, 94, 103, 100, 108, 102, 107, 109, 105, 113, 114, 112, 53, 80, 97, 91, 85, 95, 106, 101, 75, 104, 77, 50, 90, 86, 54, 38, 7, 72, 36, 25, 35, 19, 20, 56, 26, 27, 28, 17, 10, 11, 12, 15, 6, 37, 31, 34, 39, 40, 41, 42, 43, 44, 45, 46, 51, 88, 18, 16, 71, 14, 21, 23, 32, 52, 67, 69, 70, 78, 79, 82, 84, 30, 29, 83, 2, 8, 3, 33, 60, 4, 99, 57, 47, 13, 55, 76, 65, 98, 59, 24, 22, 63, 58, 49, 66, 64, 61, 62, 48, 5, 9, 110
]

CHRONO_MAP = {surah_id: index for index, surah_id in enumerate(CHRONOLOGICAL_ORDER)}

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

def extract_book_id(source):
    # Vol1-book-1.doc -> 1
    match = re.search(r'book-(\d+)', source)
    if match:
        return match.group(1)
    
    # j2-k01.doc -> 11
    # j3-k01.doc -> 21
    # j4-k01.doc -> 31
    match = re.search(r'j(\d+)-k(\d+)', source)
    if match:
        vol = int(match.group(1))
        kitab = int(match.group(2))
        return str((vol - 1) * 10 + kitab)
    
    return "0"

def generate_verse_index():
    master_v3_path = '/home/absolut7/Documents/ihya_love/ihya_tafsir_master_v3.json'
    haleem_json_path = '/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/assets/data/en_haleem.json'
    output_path = '/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/cyber/data/verse_index.json'

    if not os.path.exists(master_v3_path):
        print(f"Error: {master_v3_path} not found.")
        return

    with open(master_v3_path, 'r', encoding='utf-8') as f:
        master_data = json.load(f)

    with open(haleem_json_path, 'r', encoding='utf-8') as f:
        haleem_data = json.load(f)

    verse_map = {}

    for item in master_data:
        s_id = str(item.get('surah', ''))
        a_id = str(item.get('ayah', ''))
        verse_key = item.get('verse_key', '')

        if not s_id.isdigit():
             if ':' in verse_key:
                 parts = verse_key.split(':')
                 s_part = parts[0].strip()
                 a_part = parts[1].strip()
                 if s_part in ARABIC_SURAH_MAP:
                     s_id = ARABIC_SURAH_MAP[s_part]
                     a_id = a_part
                 elif s_part.isdigit():
                     s_id = int(s_part)
                     a_id = a_part
        else:
            s_id = int(s_id)

        if isinstance(s_id, int):
            try:
                if '-' in str(a_id):
                    a_start = int(str(a_id).split('-')[0])
                else:
                    # Clean a_id if it's like "201, 9"
                    a_clean = str(a_id).split(',')[0].strip()
                    a_start = int(a_clean)
                
                clean_key = f"{s_id}:{a_start}"
                haleem_key = f"{s_id}_{a_start}"
                
                if clean_key not in verse_map:
                    verse_map[clean_key] = {
                        "verse_key": clean_key,
                        "surah": s_id,
                        "ayah": a_start,
                        "haleem_text": haleem_data.get(haleem_key, ""),
                        "mentions": []
                    }
                
                book_id = extract_book_id(item.get('book_source', ''))
                
                mention = {
                    "book_id": book_id,
                    "arabic_text": item.get('commentary_arabic', item.get('arabic_commentary', '')),
                    "english_text": item.get('commentary_english', item.get('english_commentary', ''))
                }
                verse_map[clean_key]["mentions"].append(mention)

            except (ValueError, IndexError):
                continue

    verse_list = list(verse_map.values())
    
    def sort_key(v):
        chrono_idx = CHRONO_MAP.get(v['surah'], 999)
        return (chrono_idx, v['ayah'])

    verse_list.sort(key=sort_key)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(verse_list, f, ensure_ascii=False, indent=2)

    print(f"Index generated with {len(verse_list)} verses.")

if __name__ == "__main__":
    generate_verse_index()
