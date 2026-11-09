LARGHEZZA = 10  # caselle oriz
ALTEZZA = 10    # caselle vert

MURO_X = 5
MURO_INIZIO = 3
MURO_FINE = 6

def bloccata(x, y):
    return x == MURO_X and MURO_INIZIO <= y <= MURO_FINE

def muovi(x, y, azione):
    y = y + azione - 1                  # 0 = su, 1 = dritto, 2 = giù
    y = max(0, min(ALTEZZA - 1, y))
    return x + 1, y

def osserva(x, y):
    return [
        y / ALTEZZA,                      # dove sono in verticale
        (MURO_X - x) / LARGHEZZA,         # quanto manca al muro
        (MURO_INIZIO - y) / ALTEZZA,      # inizio muro rispetto a me
        (MURO_FINE - y) / ALTEZZA,        # fine muro rispetto a me
    ]


def episodio(scegli_azione, y_partenza=5):
    x, y = 0, y_partenza
    percorso = [(x, y)]
    while x < LARGHEZZA - 1:
        azione = scegli_azione(osserva(x, y))
        x, y = muovi(x, y, azione)
        percorso.append((x, y))
        if bloccata(x, y):
            return False, percorso   # sbattuto contro il muro
    return True, percorso            # arrivato in fondo


def valuta(scegli_azione):
    arrivati = 0
    for y in range(ALTEZZA):
        ok, _ = episodio(scegli_azione, y)
        arrivati += ok
    return arrivati   # da 0 a 10
