def verify_rut(rut):
    # Lógica de validación de RUT en base al dígito verificador (DV)
    rut = rut.replace(".", "").replace("-", "")
    reverse_digits = map(int, reversed(str(rut)))
    factors = [2, 3, 4, 5, 6, 7]
    s = sum(d * factors[i % 6] for i, d in enumerate(reverse_digits))
    dv_calculated = 11 - (s % 11)
    
    if dv_calculated == 11:
        return '0'
    elif dv_calculated == 10:
        return 'k'
    else:
        return str(dv_calculated)
