import re

# Define a string
text = "Amor: alejará a gente entrometida para proteger a la pareja. La relación comenzará a estar sólida. Salud: un estudio resultará bien. Sorpresa: críticas interesadas."

original = re.split(r"\.", text)

grupos = []
grupo_actual = []

for x, item in enumerate(original):
    item_limpio = item.strip()
    print(item_limpio)
    if not item_limpio:
        continue  # Ignorar strings vacíos
    if ':' in item_limpio:
        # if grupo_actual is not None:
        #     grupos.append(grupo_actual)
        grupo_actual.append(item_limpio)
    else:
       print(x)
       grupo_actual[x-1].append(item_limpio)

# Añadir el último grupo si existe
# if grupo_actual is not None:
#     grupos.append(grupo_actual)

print(grupo_actual)