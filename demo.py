from PIL import Image, ImageDraw, ImageFont
from ambiente import episodio, bloccata, LARGHEZZA, ALTEZZA
from rete import carica_pesi, scegli_azione

RIGA_PARTENZA = 4
CELLA = 36
MARGINE = 30
TESTA = 50

versioni = []
for nome, didascalia_fine in [("v0", "v0: blocked by the wall"), ("v1", "v1: gets past the wall")]:
    carica_pesi(f"versioni/{nome}.json")
    ok, percorso = episodio(scegli_azione, RIGA_PARTENZA)
    versioni.append((nome, didascalia_fine, ok, percorso))

lato = LARGHEZZA * CELLA
larghezza_img = 2 * lato + 3 * MARGINE
altezza_img = TESTA + ALTEZZA * CELLA + MARGINE
font = ImageFont.load_default(size=18)
passi = max(len(p) for _, _, _, p in versioni)


def disegna(passo):
    img = Image.new("RGB", (larghezza_img, altezza_img), "white")
    d = ImageDraw.Draw(img)
    for k, (nome, didascalia_fine, ok, percorso) in enumerate(versioni):
        x0 = MARGINE + k * (lato + MARGINE)
        y0 = TESTA
        visibile = percorso[: passo + 1]
        finito = passo >= len(percorso) - 1
        d.text((x0, 15), didascalia_fine if finito else nome, fill="black", font=font)
        for x in range(LARGHEZZA):
            for y in range(ALTEZZA):
                riquadro = [x0 + x * CELLA, y0 + y * CELLA, x0 + (x + 1) * CELLA, y0 + (y + 1) * CELLA]
                colore = "#444444" if bloccata(x, y) else "white"
                d.rectangle(riquadro, fill=colore, outline="#dddddd")
        for x, y in visibile[:-1]:
            c = [x0 + x * CELLA + 12, y0 + y * CELLA + 12, x0 + (x + 1) * CELLA - 12, y0 + (y + 1) * CELLA - 12]
            d.ellipse(c, fill="#9ec5f0")
        x, y = visibile[-1]
        c = [x0 + x * CELLA + 6, y0 + y * CELLA + 6, x0 + (x + 1) * CELLA - 6, y0 + (y + 1) * CELLA - 6]
        schianto = finito and not ok
        d.ellipse(c, fill="#d33" if schianto else "#1f6fd1")
    return img


fotogrammi = [disegna(p) for p in range(passi)]
durate = [400] * (passi - 1) + [2500]
fotogrammi[0].save("demo.gif", save_all=True, append_images=fotogrammi[1:], duration=durate, loop=0)
print("salvato demo.gif")
