from datetime import datetime, timedelta

# Definir rango nocturno: de 22:00 a 06:00
NOCTURNIDAD_INICIO = 22  # 22:00
NOCTURNIDAD_FIN = 6      # 06:00
VALOR_MINUTO = 0.5       # ejemplo: 0.5 €/minuto

def calcular_nocturnidad_global(registros):
    detalle = []
    total_minutos = 0
    total_importe = 0.0

    for r in registros:
        try:
            hi = datetime.strptime(r["hi"], "%H:%M")
            hf = datetime.strptime(r["hf"], "%H:%M")
        except Exception:
            continue

        # Si la hora final es menor que la inicial, significa que cruza medianoche
        if hf <= hi:
            hf += timedelta(days=1)

        minutos_nocturnos = 0

        # Iterar minuto a minuto para comprobar si cae en nocturnidad
        actual = hi
        while actual < hf:
            hora = actual.hour
            if hora >= NOCTURNIDAD_INICIO or hora < NOCTURNIDAD_FIN:
                minutos_nocturnos += 1
            actual += timedelta(minutes=1)

        importe = minutos_nocturnos * VALOR_MINUTO

        detalle.append({
            "fecha": r["fecha"],
            "hi": r["hi"],
            "hf": r["hf"],
            "minutos": minutos_nocturnos,
            "importe": round(importe, 2)
        })

        total_minutos += minutos_nocturnos
        total_importe += importe

    return {
        "detalle": detalle,
        "total_minutos": total_minutos,
        "total_importe": round(total_importe, 2)
    }
