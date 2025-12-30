# 🎶 Time Machine Music Box

Uma **web app em Python** que permite viajar no tempo e criar automaticamente **playlists privadas no Spotify** com base no **Top 100 da Billboard** numa data à tua escolha.

> Escolhe uma data ➜ autentica no Spotify ➜ a playlist é criada com músicas, capa personalizada e histórico.

---

## ✨ Funcionalidades

- 📅 Escolha de uma data (YYYY-MM-DD)
- 🌐 Scraping do **Billboard Hot 100**
- 🔐 Autenticação Spotify (OAuth 2.0)
- 🎧 Criação automática de playlists privadas
- 📊 Progresso em tempo real (UI dinâmica)
- 🕘 Histórico de playlists criadas
- 🎨 **Capa personalizada automática**
  - baseada na imagem do artista
  - com gradiente gerado dinamicamente
- 💾 Persistência simples com JSON

---

## 🖼️ Preview

> _(Sugestão: adiciona aqui screenshots da UI e da playlist no Spotify)_  

Exemplo:
- Página inicial  
- Barra de progresso  
- Histórico  
- Playlist com capa no Spotify  

---

## 🛠️ Tecnologias Utilizadas

**Backend**
- Python 3
- Flask
- Spotipy (Spotify Web API)
- BeautifulSoup
- Requests
- Pillow (PIL)

**Frontend**
- HTML5
- CSS3
- JavaScript (fetch / polling)

**Outros**
- OAuth 2.0
- Threads (background tasks)
- Git & GitHub

---

## 🚀 Como Executar Localmente

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/Adwingen/TimeMachineMusicBox.git
cd TimeMachineMusicBox
