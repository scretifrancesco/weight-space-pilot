from ambiente import episodio, valuta, ALTEZZA, MURO_X, MURO_INIZIO, MURO_FINE
import json
import urllib.request

MODELLO = "qwen3:14b"

def chiedi(prompt, pensa=True):
    dati = {
        "model": MODELLO,
        "prompt": prompt,
        "stream": True,
        "think": pensa,
        "options": {"temperature": 0, "seed": 42, "num_ctx": 12288, "num_predict": 8000},
    }
    richiesta = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(dati).encode(),
        headers={"Content-Type": "application/json"},
    )
    ragionamento, risposta = "", ""
    with urllib.request.urlopen(richiesta, timeout=300) as r:
        for riga in r:
            pezzo = json.loads(riga)
            ragionamento += pezzo.get("thinking", "")
            risposta += pezzo.get("response", "")
            print(pezzo.get("thinking", "") + pezzo.get("response", ""), end="", flush=True)
    return ragionamento, risposta


def descrivi_comportamento(scegli_azione):
    righe = []
    for y in range(ALTEZZA):
        ok, percorso = episodio(scegli_azione, y)
        esito = "REACHED THE END" if ok else "CRASHED INTO THE WALL"
        righe.append(f"start row {y}: {esito}, path {percorso}")
    return "\n".join(righe)

def costruisci_prompt(file_pesi, scegli_azione):
    with open(file_pesi) as f:
        pesi = f.read()
    return f"""You edit the weights of a small neural network that steers an agent on a 10x10 grid.

GAME RULES (fixed, you cannot change them)
The agent starts in column 0 at some row y (rows 0..9, row 0 is the top).
At every step it moves one column to the right and picks an action:
0 = up (y-1), 1 = straight, 2 = down (y+1). It cannot leave the grid.
A wall occupies column {MURO_X}, rows {MURO_INIZIO} to {MURO_FINE}. Entering a wall cell is a crash.
Success means reaching column 9 without crashing.

NETWORK (4 inputs, 4 tanh neurons, 3 action scores; the highest score is chosen)
Inputs, in this order:
i0 = y / 10
i1 = ({MURO_X} - x) / 10
i2 = ({MURO_INIZIO} - y) / 10
i3 = ({MURO_FINE} - y) / 10
hidden = tanh(W0 * inputs + b0), with W0 = "0.weight" (4x4) and b0 = "0.bias"
scores = W2 * hidden + b2, with W2 = "2.weight" (3x4) and b2 = "2.bias"
Row i of a weight matrix belongs to output neuron i; column j multiplies input j.

CURRENT WEIGHTS
{pesi}

CURRENT BEHAVIOUR (one attempt from every start row)
{descrivi_comportamento(scegli_azione)}
Score: {valuta(scegli_azione)}/10

TASK
Change the weights so the agent reaches the end from as many start rows as possible.
Reason about what each weight does. Do not write code.
Reply with ONLY the complete new weights as JSON, same keys and shapes as above."""

def estrai_pesi(risposta, file):
    inizio = risposta.index("{")
    fine = risposta.rindex("}") + 1
    pesi = json.loads(risposta[inizio:fine])
    with open(file, "w") as f:
        json.dump(pesi, f)
