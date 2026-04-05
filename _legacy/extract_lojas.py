import urllib.request
import re
from bs4 import BeautifulSoup
import json
import os

html_path = "onde-comprar.html"
with open(html_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

lojas = []
current_estado = "SP"
current_cidade = ""
current_bairro = ""

# Look for text to find structure
for element in soup.find_all(['h4', 'h5', 'ul', 'p']):
    if element.name == 'h4':
        text = element.get_text(strip=True)
        if text in ['SP', 'MG', 'RJ']:
            current_estado = text
        elif 'Cidades' in text or 'Cidades:' in text:
            pass # just a header
        elif text:
            # Maybe it's a cidade
            pass
            
    elif element.name == 'h5':
        # could be cidade or bairro
        a_tag = element.find('a')
        if a_tag:
            class_list = a_tag.get('class', [])
            if 'LinkCidade' in class_list:
                current_cidade = a_tag.get_text(strip=True).replace('\xa0', ' ').strip()
            elif 'LinkBairro' in class_list:
                current_bairro = a_tag.get_text(strip=True).replace('\xa0', ' ').strip()
            elif 'LinkUF' in class_list:
                current_estado = a_tag.get_text(strip=True).replace('\xa0', ' ').strip()
            else:
                if 'SP' not in current_cidade: # heuristic
                    # just assign it to bairro if we have a cidade
                    current_bairro = element.get_text(strip=True)
        else:
            current_bairro = element.get_text(strip=True)
            
    elif element.name == 'ul':
        li_tag = element.find('li')
        if li_tag:
            # the next 'p' often has the data
            loja_nome = li_tag.get_text(strip=True).replace('\xa0', ' ')
            lojas.append({
                "nome": loja_nome,
                "estado": current_estado,
                "cidade": current_cidade,
                "bairro": current_bairro,
                "endereco": "",
                "telefone": "",
                "whatsapp": "",
                "gmaps_link": "",
                "lat": "",
                "lng": "",
                "p_node": element.find_next_sibling('p')
            })

for loja in lojas:
    p_node = loja.get("p_node")
    if p_node:
        text = p_node.get_text(separator="|", strip=True)
        # Extract phone
        import re
        phones = re.findall(r'\(\d{2}\)\s*\d{4,5}-\d{4}', text)
        if phones:
            loja["telefone"] = phones[0]
        
        # WhatsApp link
        wa_link = p_node.find('a', href=re.compile(r'whatsapp', re.IGNORECASE))
        if wa_link:
            loja["whatsapp"] = wa_link.get_text(strip=True)
            
        gmaps = p_node.find('a', href=re.compile(r'google\.com/maps'))
        if gmaps:
            loja["gmaps_link"] = gmaps.get('href')
            # Extract Address from the text of the link
            loja["endereco"] = gmaps.get_text(strip=True)
            
            # Extract lat/lng
            # e.g. !2d-46.564904899999995!3d-23.5425999
            m_lat = re.search(r'!3d(-?\d+\.\d+)', loja["gmaps_link"])
            m_lng = re.search(r'!2d(-?\d+\.\d+)', loja["gmaps_link"])
            if m_lat and m_lng:
                loja["lat"] = float(m_lat.group(1))
                loja["lng"] = float(m_lng.group(1))
        
        if not loja["endereco"]:
            # fallback to text lines
            lines = text.split("|")
            for line in lines:
                if 'Whatsapp' not in line and 'Localização' not in line and not re.match(r'.*\(\d{2}\).*', line):
                    if len(line) > 5 and 'R.' in line or 'Av.' in line or 'Estr.' in line:
                        loja["endereco"] = line.strip()
                        break
    del loja["p_node"]

# filter out empty ones
lojas = [l for l in lojas if l["nome"] and (l["endereco"] or l["telefone"])]

os.makedirs('data', exist_ok=True)
js_content = "const lojas = " + json.dumps(lojas, indent=2, ensure_ascii=False) + ";\n"
with open("data/lojas.js", "w", encoding="utf-8") as f:
    f.write(js_content)
print(f"Extracted {len(lojas)} lojas")
