"""
Olho na Lente — protótipo preliminar (Sprint 1)
Challenge Motiva x FIAP · PCP (Python) · Turma 1CCPR

O que este script faz (tudo com IMAGENS SINTÉTICAS, desenhadas pelo próprio código):
1. Desenha uma cena de rodovia vista por 3 câmeras vizinhas (km 40, 42 e 44).
2. Simula problemas na lente: barro, teia, desfoque, e condições do tempo: neblina e sol.
3. Mede a "saúde" da imagem com duas métricas de visão computacional:
   - nitidez = variância do Laplaciano, medida só nas partes fixas da cena (placa, faixas, defensa);
   - contraste = desvio-padrão dos tons de cinza;
   - textura no céu = bordas onde a cena deveria ser lisa (pega teia e trincas na lente);
   - saturação = % de pixels "estourados" de branco (pega sol batendo na lente).
4. Aplica o motor de regras: compara com a referência da própria câmera, com as câmeras
   vizinhas e com a estação meteorológica para decidir REAL, AMBIENTAL ou NORMAL.

Não usa imagem real da Motiva. Serve só para mostrar que a lógica funciona.
Como rodar:  pip install opencv-python numpy   e depois   python prototipo_olho_na_lente.py
"""
import csv
import cv2
import numpy as np

LARG, ALT = 640, 360
LIMITE_NITIDEZ = 0.45   # abaixo de 45% da nitidez de referência = imagem degradada
LIMITE_CONTRASTE = 0.60  # abaixo de 60% do contraste de referência = imagem degradada
LIMITE_CEU = 30.0        # textura no céu acima disso = algo na frente da lente (teia)
LIMITE_SATURADOS = 0.10  # mais de 10% dos pixels estourados = ofuscamento


# ---------- 1. cena sintética ----------
def desenhar_cena(deslocamento=0):
    """Desenha uma rodovia simples. 'deslocamento' muda um pouco a cena de cada câmera."""
    img = np.zeros((ALT, LARG, 3), np.uint8)
    for y in range(150):                                   # céu em degradê
        img[y, :] = (235 - y // 2, 200 - y // 3, 150 - y // 4)
    img[150:, :] = (70, 110, 80)                           # grama
    pista = np.array([[250 + deslocamento, 150], [390 + deslocamento, 150], [620, ALT], [20, ALT]])
    cv2.fillPoly(img, [pista], (60, 60, 60))               # asfalto
    for i in range(6):                                     # faixa central tracejada
        y1 = 160 + i * 35
        cv2.line(img, (320 + deslocamento // 2, y1), (320 + deslocamento // 2, y1 + 18), (240, 240, 240), 3)
    cv2.line(img, (250 + deslocamento, 150), (20, ALT), (230, 230, 230), 2)    # bordas da pista
    cv2.line(img, (390 + deslocamento, 150), (620, ALT), (230, 230, 230), 2)
    cv2.rectangle(img, (470, 70), (580, 120), (40, 120, 30), -1)               # placa verde
    cv2.putText(img, "KM 42", (482, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.line(img, (525, 120), (525, 190), (120, 120, 120), 4)                  # poste da placa
    for x in range(0, 230, 22):                                                # defensa metálica
        cv2.line(img, (x, 250 + x // 8), (x, 280 + x // 8), (200, 200, 200), 2)
    cv2.line(img, (0, 255), (230, 284), (210, 210, 210), 3)
    return img


# ---------- 2. problemas simulados ----------
def barro(img):
    out = img.copy()
    rng = np.random.default_rng(1)
    camada = out.copy()
    for _ in range(14):
        c = (int(rng.integers(0, LARG)), int(rng.integers(0, ALT)))
        cv2.circle(camada, c, int(rng.integers(30, 80)), (60, 85, 110), -1)
    out = cv2.addWeighted(camada, 0.75, out, 0.25, 0)
    return cv2.GaussianBlur(out, (21, 21), 0)

def teia(img):
    out = cv2.GaussianBlur(img, (9, 9), 0)
    centro = (200, 140)
    for ang in range(0, 360, 25):
        p = (int(centro[0] + 400 * np.cos(np.radians(ang))), int(centro[1] + 400 * np.sin(np.radians(ang))))
        cv2.line(out, centro, p, (225, 225, 225), 1)
    for r in range(25, 300, 30):
        cv2.circle(out, centro, r, (225, 225, 225), 1)
    return cv2.addWeighted(out, 0.6, np.full_like(out, 200), 0.4, 0)

def desfoque(img):
    return cv2.GaussianBlur(img, (31, 31), 0)

def neblina(img):
    cinza = np.full_like(img, 205)
    return cv2.GaussianBlur(cv2.addWeighted(img, 0.35, cinza, 0.65, 0), (7, 7), 0)

def sol(img):
    yy, xx = np.mgrid[0:ALT, 0:LARG]
    brilho = np.clip(255 * np.exp(-((xx - 560) ** 2 + (yy - 40) ** 2) / (2 * 170 ** 2)), 0, 255)
    out = img.astype(np.float32) + brilho[..., None] * 1.3
    return np.clip(out, 0, 255).astype(np.uint8)


# ---------- 3. métricas ----------
MASCARA = np.zeros((ALT, LARG), np.uint8)       # só as partes FIXAS da cena (sem carros)
cv2.rectangle(MASCARA, (460, 60), (590, 195), 255, -1)     # placa
cv2.rectangle(MASCARA, (300, 150), (345, 360), 255, -1)    # faixa central
cv2.rectangle(MASCARA, (0, 245), (235, 310), 255, -1)      # defensa

CEU = np.zeros((ALT, LARG), np.uint8)           # região que deveria ser lisa
cv2.rectangle(CEU, (0, 0), (440, 140), 255, -1)

def medir(img):
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(cinza, cv2.CV_64F)
    nitidez = float(lap[MASCARA > 0].var())
    contraste = float(cinza.std())
    textura_ceu = float(lap[CEU > 0].var())
    saturados = float((cinza >= 250).mean())
    return nitidez, contraste, textura_ceu, saturados

def degradada(img, referencia):
    """Compara a imagem com a referência limpa DA MESMA câmera."""
    n, c, ceu, sat = medir(img)
    n0, c0 = referencia[0], referencia[1]
    ruim = (n / n0 < LIMITE_NITIDEZ or c / c0 < LIMITE_CONTRASTE
            or ceu > LIMITE_CEU or sat > LIMITE_SATURADOS)
    return ruim, n / n0, c / c0, ceu, sat


# ---------- 4. motor de regras ----------
def classificar(alvo_ruim, vizinhas_ruins, chuva_ou_neblina_na_sca, horas_ruim):
    """Regra do Olho na Lente para a câmera-alvo."""
    if not alvo_ruim:
        return "NORMAL", "imagem dentro do padrão"
    if vizinhas_ruins or chuva_ou_neblina_na_sca:
        return "AMBIENTAL", "vizinhas também ruins ou SCA indica tempo ruim → aguardar"
    if horas_ruim < 2:
        return "AGUARDAR", "ruim há pouco tempo (pode ser sol passageiro) → reavaliar"
    return "REAL", "só esta câmera piorou, sem chuva, há 2 h ou mais → abrir chamado"


def main():
    cams = {"km40": desenhar_cena(-20), "km42": desenhar_cena(0), "km44": desenhar_cena(20)}
    ref = {k: medir(v) for k, v in cams.items()}           # referência = imagem limpa de cada câmera

    efeitos = {"limpa": lambda x: x, "barro": barro, "teia": teia,
               "desfoque": desfoque, "neblina": neblina, "sol": sol}

    # cenários: (nome, efeito na km42, efeito nas vizinhas, SCA indica chuva/neblina?, horas ruim)
    cenarios = [
        ("A - lente com barro", "barro", "limpa", False, 6),
        ("B - teia de aranha", "teia", "limpa", False, 3),
        ("C - desfoque", "desfoque", "limpa", False, 12),
        ("D - neblina na região", "neblina", "neblina", True, 3),
        ("E - sol na lente", "sol", "limpa", False, 0.5),
        ("F - tudo normal", "limpa", "limpa", False, 0),
    ]

    linhas, quadros = [], []
    for nome, ef_alvo, ef_viz, sca, horas in cenarios:
        img_alvo = efeitos[ef_alvo](cams["km42"])
        ruim, rn, rc, ceu, sat = degradada(img_alvo, ref["km42"])
        viz_ruins = any(degradada(efeitos[ef_viz](cams[k]), ref[k])[0] for k in ("km40", "km44"))
        classe, motivo = classificar(ruim, viz_ruins, sca, horas)
        linhas.append([nome, f"{rn:.2f}", f"{rc:.2f}", f"{ceu:.1f}", f"{sat:.1%}", "sim" if ruim else "não",
                       "sim" if viz_ruins else "não", "sim" if sca else "não", horas, classe, motivo])
        q = cv2.resize(img_alvo, (320, 180))
        cv2.rectangle(q, (0, 0), (320, 26), (20, 20, 20), -1)
        cv2.putText(q, f"{nome[:24]} -> {classe}", (5, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        quadros.append(q)

    cab = ["cenario", "nitidez_rel", "contraste_rel", "textura_ceu", "saturados", "km42_degradada", "vizinha_degradada",
           "sca_tempo_ruim", "horas_ruim", "classificacao", "motivo"]
    with open("resultados_prototipo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cab)
        w.writerows(linhas)
    grade = np.vstack([np.hstack(quadros[0:3]), np.hstack(quadros[3:6])])
    cv2.imwrite("cenarios_prototipo.png", grade)

    print(f"{'Cenário':28}{'nit.':>6}{'contr.':>8}{'céu':>8}{'sat.':>8}  classificação")
    for l in linhas:
        print(f"{l[0]:28}{l[1]:>6}{l[2]:>8}{l[3]:>8}{l[4]:>8}  {l[9]}")


if __name__ == "__main__":
    main()
