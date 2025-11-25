import pdfplumber

def parse_pdf(file):
    registros = []
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if not table:
                    continue

                header = table[0]
                idx_hi = header.index("HI")
                idx_hf = header.index("HF")

                # recorrer filas
                for row in table[1:]:
                    fecha = row[0]
                    hi_cell = row[idx_hi] if len(row) > idx_hi else None
                    hf_cell = row[idx_hf] if len(row) > idx_hf else None

                    # si la fecha está vacía pero la fila es continuación → usar última fecha
                    if not fecha and registros:
                        fecha = registros[-1]["fecha"]

                    if hi_cell and hf_cell:
                        hi_list = hi_cell.split()
                        hf_list = hf_cell.split()
                        # emparejar cada HI con cada HF
                        for hi, hf in zip(hi_list, hf_list):
                            registros.append({
                                "fecha": fecha.strip(),
                                "hi": hi.strip(),
                                "hf": hf.strip()
                            })
    except Exception as e:
        print("Error al leer PDF:", e)

    print("Registros extraídos:", registros)  # 🔎 debug
    return registros
