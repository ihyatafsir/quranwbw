
import re

def verify_1_html():
    with open('/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/surahs/1.html', 'r') as f:
        content = f.read()
    
    # Check Home Link
    if 'href="../index.html">Home</a>' not in content:
        print("FAIL: Home link not fixed in 1.html")
    else:
        print("PASS: Home link fixed in 1.html")

    # Check Next Surah Link
    # Should point to 2.html
    # The snippet: <a class="surah-nav-links" ... href="2.html">
    match = re.search(r'href="2.html"', content)
    if match:
        print("PASS: Next surah link points to 2.html")
    else:
        print("FAIL: Next surah link incorrect in 1.html")

if __name__ == "__main__":
    verify_1_html()
