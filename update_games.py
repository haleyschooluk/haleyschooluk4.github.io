import json
import os
import re

def get_game_data(base_path):
    category_dirs = []
    # Find all directories that look like "XX.category-name"
    pattern = re.compile(r'^(\d{2})\.(.+)$')
    
    # Get all items in the directory
    try:
        items = os.listdir(base_path)
    except OSError:
        return []

    for d in sorted(items):
        match = pattern.search(d)
        if match:
            category_dirs.append((d, match.group(2)))

    data = []
    for dir_name, category_display_name in category_dirs:
        category_path = os.path.join(base_path, dir_name)
        if not os.path.isdir(category_path):
            continue
            
        games_in_category = []
        
        # Check subdirectories for index.html
        try:
            sub_items = os.listdir(category_path)
        except OSError:
            continue

        for sub_d in sorted(sub_items):
            sub_path = os.path.join(category_path, sub_d)
            if os.path.isdir(sub_path):
                if os.path.exists(os.path.join(sub_path, "index.html")):
                    # Create clean game name from folder name
                    game_name = sub_d.replace("-", " ").replace("_", " ").title()
                    game_url = f"http://4.haleyschool.uk/{dir_name}/{sub_d}/index.html"
                    logo_url = f"http://4.haleyschool.uk/{dir_name}/{sub_d}/logo.png"
                    
                    games_in_category.append({
                        "name": game_name,
                        "url": game_url,
                        "logo": logo_url
                    })
        
        if games_in_category:
            data.append({
                "category": category_display_name.replace("-", " ").title(),
                "games": games_in_category
            })
    return data

base = "/Volumes/1M$/GitHub/haleyschooluk4.github.io"
game_data = get_game_data(base)

# Write to game.json (new file)
with open(os.path.join(base, "game.json"), "w", encoding="utf-8") as f:
    json.dump(game_data, f, indent=2, ensure_ascii=False)

print(f"Successfully created a clean game.json with {len(game_data)} categories.")
