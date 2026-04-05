import os
import urllib.request
import re

base_url = "https://ntk80.com.br"
pages = {
    "index.html": "/",
    "produtos.html": "/produtos",
    "onde-comprar.html": "/onde-comprar",
    "contato.html": "/contato",
    "sobre.html": "/sobre"
}

assets = [
    "/assets/criadordesites.css?2e9d38b5-72bd-468f-bcc1-10b4b3a10983",
    "/assets/criadordesites.js?2e9d38b5-72bd-468f-bcc1-10b4b3a10983"
]

os.makedirs("assets", exist_ok=True)

for path in assets:
    url = f"{base_url}{path}"
    # remove query string for local save
    local_path = path.split("?")[0].lstrip("/")
    print(f"Downloading {url} to {local_path}")
    urllib.request.urlretrieve(url, local_path)

for filename, path in pages.items():
    url = f"{base_url}{path}"
    print(f"Downloading {url} to {filename}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        continue
    
    # Fix links
    html = html.replace('href="/"', 'href="index.html"')
    html = html.replace('href="/produtos"', 'href="produtos.html"')
    html = html.replace('href="/onde-comprar"', 'href="onde-comprar.html"')
    html = html.replace('href="/contato"', 'href="contato.html"')
    html = html.replace('href="/sobre"', 'href="sobre.html"')
    
    # Fix asset links
    html = re.sub(r'href="/assets/criadordesites\.css[^"]*"', 'href="assets/criadordesites.css"', html)
    html = re.sub(r'src="/assets/criadordesites\.js[^"]*"', 'src="assets/criadordesites.js"', html)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
