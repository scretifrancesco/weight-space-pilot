import copy
import json
import os
import tempfile
from rete import carica_pesi, scegli_azione
from ambiente import valuta

v0 = json.load(open("versioni/v0.json"))
v1 = json.load(open("versioni/v1.json"))
file_tmp = os.path.join(tempfile.gettempdir(), "ablazione.json")


def punteggio(pesi):
    with open(file_tmp, "w") as f:
        json.dump(pesi, f)
    carica_pesi(file_tmp)
    return valuta(scegli_azione)


def posizioni_cambiate():
    cambiate = []
    for nome in v0:
        for i, riga in enumerate(v0[nome]):
            if isinstance(riga, list):
                for j, valore in enumerate(riga):
                    if valore != v1[nome][i][j]:
                        cambiate.append((nome, i, j))
            elif riga != v1[nome][i]:
                cambiate.append((nome, i, None))
    return cambiate


def copia_valore(da, a, nome, i, j):
    if j is None:
        a[nome][i] = da[nome][i]
    else:
        a[nome][i][j] = da[nome][i][j]


print(f"v0: {punteggio(v0)}/10   v1: {punteggio(v1)}/10")
for nome, i, j in posizioni_cambiate():
    solo = copy.deepcopy(v0)
    copia_valore(v1, solo, nome, i, j)
    senza = copy.deepcopy(v1)
    copia_valore(v0, senza, nome, i, j)
    etichetta = f"{nome}[{i}]" + (f"[{j}]" if j is not None else "")
    print(f"{etichetta:16} solo questo su v0: {punteggio(solo)}/10   v1 senza questo: {punteggio(senza)}/10")
