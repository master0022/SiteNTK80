import os
from bs4 import BeautifulSoup

with open("onde-comprar.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Find the section containing the map
# <iframe name=GMaps src="...">...
iframe = soup.find("iframe", {"name": "GMaps"})
if iframe:
    center_tag = iframe.parent
    if center_tag.name == 'center':
        map_container = soup.new_tag("div", id="map", style="width: 100%; height: 500px; border: 1px solid #ccc; border-radius: 5px;")
        center_tag.replace_with(map_container)

# We want to remove the large list. The list starts at the widget with "SP", "Cidades" etc.
# But it's easier to find the widgets and empty them. Let's find the section that has the list.
# We will look for all div elements with class "cs-box" or "cs-widget" that contain our state/city nodes.
# Let's remove elements from where the list begins ("<h4 style=\"text-align:center\"><a class=\"LinkUF\" href=\"#uSP\" name=\"uSP\">")
# to the end where the footer begins.

for widget in soup.find_all("div", class_="cs-widget"):
    if widget.find("a", class_="LinkUF") or widget.find("a", class_="LinkCidade") or widget.find("a", class_="LinkBairro"):
        if widget.has_attr("id") and widget["id"] != "1e36e0a8-15a3-42e4-8fc4-1f845bf9de1d":
            widget.clear()

        
# Let's inject Leaflet CSS and JS, our data, and the initializing script.
head = soup.find('head')
if head:
    leaflet_css = soup.new_tag("link", rel="stylesheet", href="https://unpkg.com/leaflet/dist/leaflet.css")
    head.append(leaflet_css)

body = soup.find('body')
if body:
    leaflet_js = soup.new_tag("script", src="https://unpkg.com/leaflet/dist/leaflet.js")
    data_js = soup.new_tag("script", src="data/lojas.js")
    
    # We will also insert a container for the list right after the map.
    list_container = soup.new_tag("div", id="lojas-list-dynamic", style="max-width: 1000px; margin: 20px auto; padding: 20px; font-family: 'Open Sans', sans-serif;")
    
    script_logic = soup.new_tag("script")
    script_logic.string = """
document.addEventListener("DOMContentLoaded", function() {
    // Initialize map
    var map = L.map('map').setView([-23.5505, -46.6333], 10); // Center at SP by default
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    var listContainer = document.getElementById("lojas-list-dynamic");
    var html = "<h3 style='text-align:center;'>Nossos Pontos de Venda</h3><ul style='list-style-type: none; padding: 0;'>";

    lojas.forEach(function(loja) {
        if(loja.lat && loja.lng) {
            L.marker([loja.lat, loja.lng]).addTo(map)
             .bindPopup("<b>" + loja.nome + "</b><br>" + loja.endereco + "<br>" + loja.telefone);
        }
        
        html += "<li style='margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px;'>";
        html += "<h4 style='margin: 0 0 10px 0; color: #333;'>" + loja.nome + "</h4>";
        html += "<p style='margin: 5px 0;'><strong>Endereço:</strong> " + loja.endereco + "</p>";
        if(loja.telefone) html += "<p style='margin: 5px 0;'><strong>Tel:</strong> " + loja.telefone + "</p>";
        if(loja.whatsapp) html += "<p style='margin: 5px 0;'><strong>WhatsApp:</strong> " + loja.whatsapp + "</p>";
        html += "<p style='margin: 5px 0;'><small>" + loja.bairro + " - " + loja.cidade + " / " + loja.estado + "</small></p>";
        html += "</li>";
    });
    
    html += "</ul>";
    listContainer.innerHTML = html;
    
    // Fit map bounds to show all markers
    if(lojas.length > 0 && lojas[0].lat){
         var bounds = new L.LatLngBounds(lojas.filter(l => l.lat && l.lng).map(l => [l.lat, l.lng]));
         map.fitBounds(bounds);
    }
});
    """
    
    # insert dynamic list after the map section
    # Let's find the section that contains the map.
    map_div = soup.find("div", id="map")
    if map_div:
        section = map_div.find_parent("section")
        if section:
            section.append(list_container)
    
    body.append(leaflet_js)
    body.append(data_js)
    body.append(script_logic)

with open("onde-comprar.html", "w", encoding="utf-8") as f:
    f.write(str(soup))
