import os
import glob
import time

def bust_cache():
    timestamp = int(time.time())
    base_dir = '/home/absolut7/Documents/ihyatafsirwebsite_2/quranwbw'
    
    files = glob.glob(os.path.join(base_dir, '*.html')) + glob.glob(os.path.join(base_dir, 'surahs', '*.html'))
    
    print(f"Busting cache for {len(files)} files with timestamp {timestamp}...")
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace style.css
        # style.css" -> style.css?v=123"
        # Handle existing query params?
        # Simple replace for now, assuming standard naming
        
        new_content = content
        if 'style.css"' in new_content:
            new_content = new_content.replace('style.css"', f'style.css?v={timestamp}"')
        
        if 'main.js"' in new_content:
            new_content = new_content.replace('main.js"', f'main.js?v={timestamp}"')
            
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
    print("Cache busting complete.")

if __name__ == "__main__":
    bust_cache()
