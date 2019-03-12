# -*- coding: utf-8 -*-
import re

def check_run(run):
    # Check regex RUN
    regex="^0*(\d{1,3}(\.?\d{3})*)\-?([\dkK])$"
    if re.match(regex, run) is None:
        return False 

    run_sinpuntos = run.replace(".", "")
    separacion = run_sinpuntos.split("-")
    separacion[1] = separacion[1].lower()
    if int(separacion[0]) or int(separacion[1]) or str(separacion[1]) == "k":
        if len(separacion[1]) == 1:
            run_separado = run.split("-")
            run_thousand = '{0:,}'.format(int(separacion[0]))
            run_thousand = run_thousand.replace(",", ".")
            if run_separado[0] == run_thousand:
                value = 11 - sum([ int(a)*int(b)  for a,b in zip(str(separacion[0]).zfill(8), '32765432')])%11
                dv_check = {10: 'k', 11: '0'}.get(value, str(value))
                if separacion[1] == dv_check:
                    return True
            else:
                return False

def parse_run(run):
    run_parse = run.split("-")
    numero = int(run_parse[0].replace(".", ""))
    DV = run_parse[1].upper()
    return numero, str(DV)
