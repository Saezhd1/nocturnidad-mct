import pdfplumber
from datetime import datetime

PRECIO_1 = 0.05   # €/min hasta 25/04/2025
PRECIO_2 = 0.062  # €/min desde 26/04/2025
FECHA_INICIO = datetime(2022, 3, 30)
FECHA_CAMBIO = datetime(2025, 4, 26)

def _normalize_hour(h):
    h = h.strip()
    if not h or ":" not in h:
        return h
    hh, mm = h.split(":")
    hh, mm = int(hh), int(mm)
    if hh == 0 and mm == 59:
        return "24:59"
    if hh >= 24:
        hh -= 24
        return f"{hh:02d}:{mm:02d}"
    return f"{hh:02d}:{mm:02d}"

def _to_minutes(h):
    if not h or ":" not in h:
        return None
    hh, mm = h.split(":")
    return int(hh) * 60 + int(mm)

def nocturnity_minutes(hi, hf):
    hi_min = _to_minutes(_normalize_hour(hi))
    hf_min = _to_minutes(_normalize_hour(hf))
    if hi_min is None or hf_min is None:
        return 0
    if hf_min < hi_min:
        hf_min += 24 * 60
    nocturnity_ranges = [(240, 360), (1320, 1440), (1440, 1500)]
    total = 0
    for start, end in nocturnity_ranges:
        overlap_start = max(hi_min, start)
        overlap_end = min(hf_min, end)
        if overlap_end > overlap_start:
            total += overlap_end - overlap_start
    return total

def calcular_dinero(fecha_str, minutos):
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
    except Exception:
        return 0.0
    if fecha < FECHA_INICIO:
        return 0.0
    elif fecha < FECHA_CAMBIO:
        return minutos * PRECIO_1
    else:
        return minutos * PRECIO_2

def parse_pdf(file):
    registros = []
    try:
        with pdfplumber.open(file) as pdf:
            last_fecha = None
            for page in pdf.pages:
                words = page.extract_words(x_tolerance=2, y_tolerance=2, use_text_flow=False)
                lines = {}
                for w in words:
                    y_key = round(w["top"], 1)
                    lines.setdefault(y_key, []).append(w)
                for y in sorted(lines.keys()):
                    row_words = sorted(lines[y], key=lambda k: k["x0"])
                    fecha_tokens = [w["text"] for w in row_words if "/" in w["text"]]
                    hora_tokens = [w["text"] for w in row_words if ":" in w["text"]]
                    fecha_val = fecha_tokens[0] if fecha_tokens else last_fecha
                    if fecha_val:
                        last_fecha = fecha_val
                    hi_val = hora_tokens[0] if hora_tokens else ""
                    hf_val = hora_tokens[-1] if hora_tokens else ""
                    minutos = nocturnity_minutes(hi_val, hf_val)
                    dinero = calcular_dinero(fecha_val, minutos)
                    registros.append({
                        "fecha": fecha_val,
                        "hi": hi_val,
                        "hf": hf_val,
                        "nocturnidad_minutos": minutos,
                        "dinero": round(dinero, 2),
                        "linea_completa": " ".join([w["text"] for w in row_words])
                    })
    except Exception as e:
        print(f"[parser] Error al leer PDF {file}:", e)
    return registros

def parse_multiple_pdfs(files):
    return {f: parse_pdf(f) for f in files}
