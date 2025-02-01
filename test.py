import re

# Define a string
text = "Amor: alejará a gente entrometida para proteger a la pareja. La relación comenzará a estar sólida. Salud: un estudio resultará bien. Sorpresa: críticas interesadas."

original = re.split(r"\.", text)

grupo_actual = []

for x, item in enumerate(original):
    item_limpio = item.strip()
    if not item_limpio:
        continue
    if ':' in item_limpio:
        grupo_actual.append(item_limpio)
    else:
       grupo_actual[-1] += " " + item_limpio

tipos = []
contenidos = []

for linea in grupo_actual:
    if ':' in linea:

        tipo = linea.split(':')[0].strip()
        contenido = linea.split(':')[1].strip()

        tipos.append(tipo[:1].upper() + tipo[1:])
        contenidos.append(contenido[:1].upper() + contenido[1:])

print(tipos)
print(contenidos)
