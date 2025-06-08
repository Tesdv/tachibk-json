import json
import os
import glob

# sets all sibling json chapters to read

dir_path = os.path.dirname(os.path.abspath(__file__))

json_files = glob.glob(os.path.join(dir_path, '*.json'))

for file in json_files:
    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    for manga in data.get('backupManga', []):
        for chapter in manga.get('chapters', []):
            if 'name' in chapter:
                chapter.pop('read', None)
                items = list(chapter.items())
                name_idx = next((i for i, (k, _) in enumerate(items) if k == 'name'), None)
                if name_idx is not None:
                    new_items = (
                        items[:name_idx+1] +
                        [('read', True)] +
                        items[name_idx+1:]
                    )
                    chapter.clear()
                    chapter.update(new_items)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)