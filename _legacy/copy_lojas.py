import os
import shutil

src_path = r"c:\Stuff\Projects\SiteNTK\data\lojas.js"
dest_dir = r"c:\Stuff\Projects\SiteNTK\web\src\data"
dest_path = os.path.join(dest_dir, "lojas.js")

os.makedirs(dest_dir, exist_ok=True)

with open(src_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace `const lojas =` with `export const lojas =`
content = content.replace("const lojas =", "export const lojas =")

with open(dest_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"File copied to {dest_path}")
