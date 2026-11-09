import json 
import torch
import torch.nn as nn

torch.manual_seed(0)

rete = nn.Sequential(
    nn.Linear(4, 4),   # 4 input -> 4 neuroni nascosti
    nn.Tanh(),
    nn.Linear(4, 3),   # 4 neuroni -> 3 azioni (su, dritto, giù)
)

def scegli_azione(osservazione):
    with torch.no_grad():
        punteggi = rete(torch.tensor(osservazione))
    return int(punteggi.argmax())   # 0 su, 1 dritto, 2 giù

def salva_pesi(file):
    pesi = {nome: p.double().round(decimals=3).tolist() for nome, p in rete.state_dict().items()}
    with open(file, "w") as f:
        json.dump(pesi, f)

def carica_pesi(file):
    with open(file) as f:
        pesi = json.load(f)
    rete.load_state_dict({nome: torch.tensor(v) for nome, v in pesi.items()})
