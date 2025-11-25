import re
import pdfplumber

def parse_pdf(file):
    registros = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.splitlines():
                # Buscar fecha en formato DD/MM/AAAA
                fecha_match = re.search(r"\d{2}/\d{2}/\d{4}", line)
                if not fecha_match:
                    continue
                fecha = fecha_match.group(0)

                # Buscar todas las horas en la línea (ej. 05:00, 15:30)
                horas = re.findall(r"\d{1,2}:\d{2}", line)

                if len(horas) >= 2:
                    hi = horas[0]
                    hf = horas[1]

                    registros.append({
                        "fecha": fecha,
                        "hi": hi,
                        "hf": hf,
                        "principal": line.strip()
                    })

    print("[parser] Registros extraídos:", len(registros))
    return registros
