import sys
from ambiente import episodio, bloccata, LARGHEZZA, ALTEZZA
from rete import carica_pesi, scegli_azione

carica_pesi(sys.argv[1])
ok, percorso = episodio(scegli_azione, int(sys.argv[2]))

for y in range(ALTEZZA):
    riga = ""
    for x in range(LARGHEZZA):
        if (x, y) == percorso[-1] and not ok:
            riga += "X "
        elif (x, y) in percorso:
            riga += "o "
        elif bloccata(x, y):
            riga += "# "
        else:
            riga += ". "
    print(riga)
