import os
import re

SURAH_DIR = '/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw/surahs'

def fix_surah_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Fix Home link: href="./" -> href="../index.html"
    # The current link might be href="./" because it's inside surahs/ dir
    # wait, looking at surahs/1.html: <a class="nav-link" href="./">Home</a>
    # correct relative path to index from surahs/1.html is ../index.html
    new_content = content.replace('href="./">Home</a>', 'href="../index.html">Home</a>')
    
    # Also the brand link: <a class="navbar-brand" href="./">
    new_content = new_content.replace('class="navbar-brand" href="./"', 'class="navbar-brand" href="../index.html"')

    # Fix Next/Prev Surah links in bottom nav
    # Pattern: href="../{number}" (without .html)
    # Target: href="{number}.html"
    # Example in 1.html: <a class="surah-nav-links" style="font-size: 15px;" href="../2">
    
    # We use regex to carefully match only these links
    # Matches href="../NNN" or href="../N"
    # We want to change it to href="NNN.html"
    # Note: These links are relative to `surahs/` directory, so `../2` means `quranwbw/2` which doesn't exist as a file, it expects a directory or rewrite rule. 
    # But files are flat in `surahs/`. So from `surahs/1.html`, `2.html` is just `2.html`.
    
    def replacer(match):
        num = match.group(1)
        return f'href="{num}.html"'

    # Regex for href="../digits"
    new_content = re.sub(r'href="\.\./(\d+)"', replacer, new_content)

    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    count = 0
    for filename in os.listdir(SURAH_DIR):
        if filename.endswith('.html'):
            if fix_surah_file(os.path.join(SURAH_DIR, filename)):
                count += 1
    print(f"Updated {count} files.")

if __name__ == "__main__":
    main()
