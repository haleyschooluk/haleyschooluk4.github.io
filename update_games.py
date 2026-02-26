import json
import os
import re

def get_game_data(base_path):
    category_dirs = []
    # Find all directories that look like "XX.category-name" (01 and above)
    pattern = re.compile(r'^(\d{2})\.(.+)$')
    for d in sorted(os.listdir(base_path)):
        match = re.search(pattern, d)
        if match:
            category_dirs.append((d, match.group(2)))

    data = []
    for dir_name, category_name in category_dirs:
        category_path = os.path.join(base_path, dir_name)
        games_in_category = []
        
        if not os.path.isdir(category_path):
            continue

        # Check subdirectories for index.html
        for sub_d in sorted(os.listdir(category_path)):
            sub_path = os.path.join(category_path, sub_d)
            if os.path.isdir(sub_path):
                if os.path.exists(os.path.join(sub_path, "index.html")):
                    game_url = f"http://4.haleyschool.uk/{dir_name}/{sub_d}/index.html"
                    logo_url = f"http://4.haleyschool.uk/{dir_name}/{sub_d}/logo.png"
                    games_in_category.append({
                        "name": sub_d,
                        "url": game_url,
                        "logo": logo_url
                    })
        
        if games_in_category:
            data.append({
                "category": category_name,
                "games": games_in_category
            })
    return data

def generate_index_html(data):
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Danh Sách Game - HaleySchool (4.haleyschool.uk)</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; color: #333; line-height: 1.6; background-color: #f8f9fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #1a73e8; text-align: center; margin-bottom: 40px; font-size: 2.5em; }}
        .category-section {{ margin-bottom: 50px; }}
        h2 {{ border-left: 5px solid #1a73e8; padding-left: 15px; margin-bottom: 20px; color: #202124; font-size: 1.8em; text-transform: capitalize; }}
        table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 10px; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; }}
        th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #e0e0e0; }}
        th {{ background-color: #f1f3f4; color: #5f6368; font-weight: 600; text-transform: uppercase; font-size: 0.9em; }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover {{ background-color: #f8f9fa; }}
        a {{ color: #1a73e8; text-decoration: none; word-break: break-all; font-weight: 500; transition: color 0.2s; }}
        a:hover {{ text-decoration: underline; color: #174ea6; }}
        .game-name {{ font-weight: bold; color: #202124; }}
        .game-logo {{ width: 40px; height: 40px; object-fit: cover; border-radius: 6px; border: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Danh Sách Game HaleySchool - 4.haleyschool.uk</h1>
"""
    for item in data:
        html += f"""
        <div class="category-section">
            <h2>Danh mục: {item['category'].replace('-', ' ')}</h2>
            <table>
                <thead>
                    <tr>
                        <th style="width: 25%;">Tên Game</th>
                        <th style="width: 45%;">Link Game</th>
                        <th style="width: 30%;">Link Logo</th>
                    </tr>
                </thead>
                <tbody>"""
        for game in item['games']:
            html += f"""
                    <tr>
                        <td><span class="game-name">{game['name']}</span></td>
                        <td><a href="{game['url']}" target="_blank">{game['url']}</a></td>
                        <td><a href="{game['logo']}" target="_blank">{game['logo']}</a></td>
                    </tr>"""
        html += """
                </tbody>
            </table>
        </div>"""
    
    html += """
    </div>
</body>
</html>"""
    return html

base = "/Volumes/1M$/GitHub/haleyschooluk4.github.io"
game_data = get_game_data(base)

with open(os.path.join(base, "game.json"), "w", encoding="utf-8") as f:
    json.dump(game_data, f, indent=2, ensure_ascii=False)

index_html = generate_index_html(game_data)
with open(os.path.join(base, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

print("Updated game.json and index.html successfully with all categories.")
