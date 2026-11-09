import sys
from rete import carica_pesi, scegli_azione
from ambiente import valuta
from llm import chiedi, costruisci_prompt, estrai_pesi

n = int(sys.argv[1])
vecchio = f"versioni/v{n}.json"
nuovo = f"versioni/v{n+1}.json"

carica_pesi(vecchio)
prima = valuta(scegli_azione)
prompt = costruisci_prompt(vecchio, scegli_azione)
ragionamento, risposta = chiedi(prompt)

if not risposta.strip().endswith("}"):
    print("\n\n[risposta incompleta, chiedo solo i pesi]\n")
    _, risposta = chiedi(prompt + "\n\nYOUR ANALYSIS SO FAR\n" + ragionamento
                         + "\n\nNow reply with ONLY the complete new weights as JSON.", pensa=False)

with open(f"versioni/log_v{n+1}.txt", "w") as f:
    f.write(prompt + "\n\n=== RAGIONAMENTO ===\n" + ragionamento + "\n\n=== RISPOSTA ===\n" + risposta)

estrai_pesi(risposta, nuovo)
carica_pesi(nuovo)
dopo = valuta(scegli_azione)
print(f"v{n}: {prima}/10  ->  v{n+1}: {dopo}/10")
