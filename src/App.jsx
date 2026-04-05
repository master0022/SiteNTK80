import React, { useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import { MapPin, Phone, MessageCircle, Mail } from 'lucide-react'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import './App.css'
import { lojas } from './data/lojas.js'

// Fix generic Leaflet icon missing in React implementations
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png'
});

function App() {
  
  // Filter valid shops with coordinates
  const markers = lojas.filter(l => l.lat && l.lng && !isNaN(l.lat) && !isNaN(l.lng));
  const centerSP = [-23.5505, -46.6333];

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-container">
          <div className="logo">
            <img src="https://yata-apix-5d35df81-0ec2-4c9d-b01f-2c3759d558cc.s3-object.locaweb.com.br/08764e3dc6af4e2c8ee5674d16bf79ef.png" alt="NTK80 Logo" />
          </div>
          <nav className="nav-links">
            <a href="#home">Home</a>
            <a href="#galeria">Produtos</a>
            <a href="#video">Conheça</a>
            <a href="#mapa">Onde Comprar</a>
            <a href="#contato">Contato</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section id="home" className="hero">
        <div className="hero-content">
          <h1>Limpeza Profunda e Eficiente</h1>
          <p>O melhor limpador universal para a sua casa ou empresa. Qualidade, rapidez e economia.</p>
          <a href="#mapa" className="btn-primary">Encontre uma Loja</a>
        </div>
      </section>

      {/* Galeria Section */}
      <section id="galeria" className="container" style={{paddingTop: '100px', paddingBottom: '40px'}}>
        <h2 className="section-title">Nossos Produtos</h2>
        <div style={{display: 'flex', gap: '30px', flexWrap: 'wrap', justifyContent: 'center'}}>
          <img 
            src="https://yata-apix-5d35df81-0ec2-4c9d-b01f-2c3759d558cc.s3-object.locaweb.com.br/879311fa44fe4e68a52b0984151e0360.png" 
            alt="Produto NTK80" 
            style={{maxWidth: '100%', height: 'auto', borderRadius: '20px', boxShadow: '0 10px 30px rgba(0,0,0,0.1)'}} 
          />
        </div>
      </section>

      {/* Video YouTube */}
      <section id="video" className="container" style={{paddingTop: '60px'}}>
        <h2 className="section-title">Veja em Ação</h2>
        <p style={{textAlign: 'center', marginBottom: '40px', fontSize: '1.1rem'}}>
          Acompanhe no nosso canal as aplicações reais do NTK80 Plus!
        </p>
        <div className="video-wrapper">
          <iframe 
            src="https://www.youtube.com/embed/dVh0UHZPA4I" 
            title="NTK80 Aplicacao" 
            allowFullScreen>
          </iframe>
        </div>
        <div style={{textAlign: 'center', marginTop: '30px'}}>
          <a href="https://www.youtube.com/NTK80" target="_blank" rel="noreferrer" className="btn-primary">
            Visitar Canal
          </a>
        </div>
      </section>

      {/* Mapa Section */}
      <section id="mapa" style={{backgroundColor: '#F8F9FA', marginTop: '80px'}}>
        <div className="container">
          <h2 className="section-title">Onde Comprar</h2>
          <p style={{textAlign: 'center', marginBottom: '40px'}}>
            Mais de {lojas.length} pontos de venda espalhados para te atender. Use o mapa para encontrar a loja mais perto de você.
          </p>

          <div className="map-container">
            <MapContainer 
              center={centerSP} 
              zoom={10} 
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; OpenStreetMap contributors'
              />
              {markers.map((loja, i) => (
                <Marker key={i} position={[loja.lat, loja.lng]}>
                  <Popup>
                    <strong>{loja.nome}</strong><br/>
                    {loja.endereco}<br/>
                    {loja.telefone && <span>📞 {loja.telefone}</span>}
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          </div>

          <div className="lojas-grid">
            {lojas.map((loja, i) => (
              <div className="loja-card" key={i}>
                <div className="loja-header">
                  <h3 className="loja-name">{loja.nome}</h3>
                  <small style={{color: '#666'}}>{loja.bairro} - {loja.cidade} / {loja.estado}</small>
                </div>
                {loja.endereco && loja.endereco !== "Localização no Mapa" && (
                  <div className="info-row">
                    <MapPin className="info-icon" size={20} />
                    <span>{loja.endereco}</span>
                  </div>
                )}
                {/* Fallback to link if we don't have text address */}
                {loja.endereco === "Localização no Mapa" && loja.gmaps_link && (
                   <div className="info-row">
                     <MapPin className="info-icon" size={20} />
                     <a href={loja.gmaps_link} target="_blank" rel="noreferrer" style={{color: 'var(--primary)', fontWeight: '500'}}>Abrir no Mapa</a>
                   </div>
                )}

                {loja.telefone && (
                  <div className="info-row">
                    <Phone className="info-icon" size={20} />
                    <span>{loja.telefone}</span>
                  </div>
                )}
                {loja.whatsapp && (
                  <div className="info-row">
                    <MessageCircle className="info-icon" size={20} />
                    <span>{loja.whatsapp}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contato">
        <div className="container">
          <div className="social-links">
            <a href="https://www.facebook.com/NTK80" target="_blank" rel="noreferrer" className="social-icon">
              <span>FB</span>
            </a>
            <a href="https://www.instagram.com/NTK80Plus" target="_blank" rel="noreferrer" className="social-icon">
              <span>IG</span>
            </a>
            <a href="https://www.youtube.com/NTK80" target="_blank" rel="noreferrer" className="social-icon">
              <span>YT</span>
            </a>
          </div>
          
          <div style={{marginBottom: '30px'}}>
             <Mail size={24} style={{color: 'var(--primary)', marginBottom: '10px'}} />
             <h3>
               <a href="mailto:contato@ntk80.com.br" style={{color: 'var(--primary)', textDecoration: 'none'}}>
                 contato@ntk80.com.br
               </a>
             </h3>
          </div>

          <p style={{color: '#888', fontSize: '0.9rem'}}>
            © {new Date().getFullYear()} NTK80 Detergentes Especiais. Todos os direitos reservados.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
