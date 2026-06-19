import json
import io

try:
    with io.open('backup_mascotasnet.json', 'r', encoding='latin-1') as f:
        data = json.load(f)
        
    # filter out contenttypes and permissions which might cause conflicts
    filtered_data = [d for d in data if not d['model'].startswith('contenttypes') and not d['model'].startswith('auth.permission') and not d['model'].startswith('sessions')]
    
    with io.open('backup_mascotasnet_utf8.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)
    print("Fixed encoding.")
except Exception as e:
    print(f"Error: {e}")
