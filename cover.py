import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64


def get_dominant_colors(img, num_colors=2):
    img = img.resize((100, 100))
    colors = img.getcolors(10000)

    # ordenar por frequência (mais comuns primeiro)
    colors.sort(reverse=True, key=lambda x: x[0])

    dominant = []
    for _, color in colors:
        if color not in dominant:
            dominant.append(color)
        if len(dominant) == num_colors:
            break

    # fallback seguro
    while len(dominant) < 2:
        dominant.append((29, 185, 84))  # verde Spotify

    return dominant


def create_vertical_gradient(size, top_color, bottom_color):
    width, height = size
    gradient = Image.new("RGB", (width, height), top_color)
    draw = ImageDraw.Draw(gradient)

    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return gradient


def create_cover_image(date, artist_name, artist_image_url):
    # descarregar imagem do artista
    response = requests.get(artist_image_url, timeout=10)
    artist_img = Image.open(BytesIO(response.content)).convert("RGB")
    artist_img = artist_img.resize((500, 500))

    # extrair cores dominantes
    color1, color2 = get_dominant_colors(artist_img)

    # criar gradiente
    gradient = create_vertical_gradient((500, 500), color1, color2)

    # misturar imagem com gradiente
    blended = Image.blend(artist_img, gradient, alpha=0.55)

    draw = ImageDraw.Draw(blended)

    # fontes
    try:
        title_font = ImageFont.truetype("arial.ttf", 38)
        small_font = ImageFont.truetype("arial.ttf", 22)
    except:
        title_font = small_font = ImageFont.load_default()

    # sombra para legibilidade
    def shadow_text(x, y, text, font):
        draw.text((x+2, y+2), text, fill="black", font=font)
        draw.text((x, y), text, fill="white", font=font)

    shadow_text(20, 380, date, title_font)
    shadow_text(20, 425, "Billboard Hot 100", small_font)
    shadow_text(20, 455, f"feat. {artist_name}", small_font)

    # exportar para base64
    buffer = BytesIO()
    blended.save(buffer, format="JPEG", quality=85, optimize=True)

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


