from collections import defaultdict

def agregar_resumen(resultados_por_pdf):
    resumen = {
        "por_mes": defaultdict(lambda: {"minutos": 0, "importe": 0.0, "dias": 0}),
        "global": {"minutos": 0, "importe": 0.0, "dias": 0}
    }

    for doc in resultados_por_pdf:
        for d in doc["dias"]:
            minutos = d["minutos_nocturnos"]
            importe = float(d["importe"])
            fecha = d["fecha"]

            if minutos > 0:
                try:
                    mes, anio = fecha.split("/")[1], fecha.split("/")[2]
                    clave = f"{mes}/{anio}"
                except Exception:
                    clave = "desconocido"

                resumen["por_mes"][clave]["minutos"] += minutos
                resumen["por_mes"][clave]["importe"] += importe
                resumen["por_mes"][clave]["dias"] += 1

                resumen["global"]["minutos"] += minutos
                resumen["global"]["importe"] += importe
                resumen["global"]["dias"] += 1

    return resumen
