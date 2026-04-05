import os
import glob

# Create custom CSS
css_content = """
/* Import modern font */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

/* Global Reset & Typography */
body, h1, h2, h3, h4, h5, h6, p, a, div, span, li {
    font-family: 'Montserrat', 'Open Sans', sans-serif !important;
}

body {
    background-color: #FAFAFA !important;
    color: #333333 !important;
}

/* Header & Menu - Glassmorphism */
header, .cs-menu {
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05) !important;
    position: sticky !important;
    top: 0;
    z-index: 1000;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3) !important;
    transition: all 0.3s ease;
}

.cs-menu-items a {
    color: #444 !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 10px 15px !important;
    border-radius: 8px;
    transition: all 0.3s ease !important;
}

.cs-menu-items a:hover {
    background: #F5D020 !important;
    color: #000 !important;
    box-shadow: 0 5px 15px rgba(245, 208, 32, 0.4) !important;
    transform: translateY(-2px);
}

/* Buttons */
.cs-button {
    background: linear-gradient(135deg, #F5D020 0%, #D4B215 100%) !important;
    color: #111 !important;
    border-radius: 50px !important;
    padding: 12px 30px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    box-shadow: 0 10px 20px rgba(245, 208, 32, 0.3) !important;
    transition: all 0.3s ease !important;
    border: none !important;
    letter-spacing: 0.5px;
}

.cs-button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 15px 25px rgba(245, 208, 32, 0.5) !important;
}

/* Images & Sections */
img {
    border-radius: 15px;
    transition: transform 0.4s ease;
}
img:hover {
    transform: scale(1.02);
}

/* Map specific styling */
#map {
    border-radius: 16px !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1) !important;
    border: none !important;
    overflow: hidden;
}

/* Dynamic Lojas List Styling */
#lojas-list-dynamic {
    max-width: 1200px !important;
}

#lojas-list-dynamic > ul {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

#lojas-list-dynamic li {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.05) !important;
    border-radius: 16px !important;
    padding: 25px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.03) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    display: flex;
    flex-direction: column;
}

#lojas-list-dynamic li:hover {
    transform: translateY(-8px) !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08) !important;
    border-color: #F5D020 !important;
}

#lojas-list-dynamic h4 {
    color: #111 !important;
    font-size: 1.1rem !important;
    margin-bottom: 15px !important;
    border-bottom: 2px solid #F5D020;
    padding-bottom: 10px;
    display: inline-block;
}

#lojas-list-dynamic p {
    color: #555 !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
}

#lojas-list-dynamic p strong {
    color: #222 !important;
}

/* Footer modernizations */
footer, .cs-section-full[id="59f37f97-18a0-45e2-a931-cb54012606b7"] {
    background: #111 !important;
    color: #eee !important;
    border-top: 5px solid #F5D020;
}

.cs-social-colors a svg {
    fill: #F5D020 !important;
    transition: transform 0.3s ease;
}

.cs-social-colors a:hover svg {
    transform: scale(1.2) rotate(5deg);
}

/* Forms */
input, textarea {
    border-radius: 8px !important;
    border: 1px solid #ddd !important;
    padding: 10px 15px !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}

input:focus, textarea:focus {
    border-color: #F5D020 !important;
    box-shadow: 0 0 0 3px rgba(245, 208, 32, 0.2) !important;
    outline: none !important;
}
"""

os.makedirs('assets', exist_ok=True)
with open('assets/custom.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

# Inject custom.css into all html files
html_files = glob.glob("*.html")
for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'assets/custom.css' not in content:
        # inject just before </head>
        inject_str = '<link type="text/css" rel="stylesheet" href="assets/custom.css">\n</head>'
        content = content.replace('</head>', inject_str)
        
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(content)
            
print("Custom CSS injected successfully into", html_files)
