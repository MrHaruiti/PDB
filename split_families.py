import json
import os

# ==========================
# CONFIGURAÇÃO
# ==========================
# Caminho base do seu projeto
base_path = r"C:\Users\Elaine Cristina\Desktop\Pokedex"

# Nome da região (ex: "kanto", "johto", etc.)
region_name = "kanto"

# Caminhos automáticos
input_file = os.path.join(base_path, f"{region_name}.json")
output_folder = os.path.join(base_path, region_name, "families")

# ==========================
# EXECUÇÃO
# ==========================

# Lê o JSON original
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Cria o diretório de saída se não existir
os.makedirs(output_folder, exist_ok=True)

# Mapa nome → Pokémon
name_map = {p["nome"]: p for p in data}

# Descobre famílias (quem não é evolução de ninguém)
all_evolved = {p["evolucao"]["proximo"] for p in data if p["evolucao"]["proximo"]}
families = [p for p in data if p["nome"] not in all_evolved]

familia_index = []
total_pokemon = 0

for base in families:
    chain = []
    current = base

    # Percorre cadeia evolutiva
    while current:
        chain.append(current)
        next_name = current["evolucao"]["proximo"]
        if not next_name or next_name not in name_map:
            break
        current = name_map[next_name]

    total_pokemon += len(chain)
    family_name = base["nome"].lower().replace(" ", "-")

    familia_index.append(family_name)
    family_data = {"family": base["nome"], "members": chain}

    # Cria arquivo individual
    out_path = os.path.join(output_folder, f"{family_name}.json")
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(family_data, out, ensure_ascii=False, indent=2)

# Cria index.json
index_data = {"families": familia_index}
with open(os.path.join(output_folder, "index.json"), "w", encoding="utf-8") as index_file:
    json.dump(index_data, index_file, ensure_ascii=False, indent=2)

print(f"✅ {len(familia_index)} famílias criadas em: {output_folder}")
print(f"📊 Total de Pokémon processados: {total_pokemon}")
