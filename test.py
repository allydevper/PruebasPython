import re

# Define a string
text = "Amor: alejará a gente entrometida para proteger a la pareja. La relación comenzará a estar sólida. Salud: un estudio resultará bien. Sorpresa: críticas interesadas."

original = re.split(r"\.", text)

grupo_actual = []

for x, item in enumerate(original):
    item_limpio = item.strip()
    print(item_limpio)
    if not item_limpio:
        continue
    if ':' in item_limpio:
        grupo_actual.append(item_limpio)
    else:
       print(x)
       grupo_actual[-1] += " " + item_limpio

print(grupo_actual)