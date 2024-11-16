import numpy as np

# Matriz de custos, capacidades e demandas
custos = np.array([
    [125, 132, 201],
    [122, 299, 172],
    [126, 140, 104],
    [123, 112, 202],
    [206, 174, 156]
], dtype=float)

capacidades = np.array([35, 90, 20, 60, 70], dtype=float)
demandas = np.array([80, 115, 65], dtype=float)

# Verifica o balanceamento
capacidade_total = np.sum(capacidades)
demanda_total = np.sum(demandas)

# Variável de controle para verificar se o nó fictício foi adicionado
adicionou_no_ficticio = False

# Adiciona o nó fictício se for necessário
if capacidade_total < demanda_total:
    deficit = demanda_total - capacidade_total
    capacidades = np.append(capacidades, deficit)
    custos = np.vstack([custos, np.zeros(len(demandas))])
    adicionou_no_ficticio = True
    print(f"Adicionando nó fictício com capacidade de {deficit} para balanceamento.")

def metodo_vogel(custos, capacidades, demandas):
    alocacao = np.zeros_like(custos)
    custo_total = 0
    num_itens = np.sum(capacidades > 0) + np.sum(demandas > 0)
    while np.any(capacidades > 0) and np.any(demandas > 0):
        penalidades_linhas = []
        for row in custos:
            valid_costs = row[np.isfinite(row)]
            if len(valid_costs) >= 2:
                penalidades_linhas.append(np.partition(valid_costs, 1)[:2])
            else:
                penalidades_linhas.append([0, 0])
        penalidades_linhas = np.array([pen[1] - pen[0] for pen in penalidades_linhas])
        penalidades_colunas = []
        for col in custos.T:
            valid_costs = col[np.isfinite(col)]
            if len(valid_costs) >= 2:
                penalidades_colunas.append(np.partition(valid_costs, 1)[:2])
            else:
                penalidades_colunas.append([0, 0])
        penalidades_colunas = np.array([pen[1] - pen[0] for pen in penalidades_colunas])
        if np.max(penalidades_linhas) > np.max(penalidades_colunas):
            i = np.argmax(penalidades_linhas)
            j = np.argmin(custos[i, :])
        else:
            j = np.argmax(penalidades_colunas)
            i = np.argmin(custos[:, j])
        quantidade = min(capacidades[i], demandas[j])
        alocacao[i, j] = quantidade

        # Ajusta o cálculo do custo total para ignorar valores inf ou NaN
        if np.isfinite(custos[i, j]):
            custo_total += quantidade * custos[i, j]

        capacidades[i] -= quantidade
        demandas[j] -= quantidade

        if capacidades[i] <= 0:
            capacidades[i] = 0
            custos[i, :] = np.inf
        if demandas[j] <= 0:
            demandas[j] = 0
            custos[:, j] = np.inf

        # Verifica se teve mudança nas capacidades ou demandas para evitar loop infinito
        num_itens_novos = np.sum(capacidades > 0) + np.sum(demandas > 0)
        if num_itens == num_itens_novos:
            print("Nenhuma alocação possível, o loop está sendo interrompido.")
            break
        num_itens = num_itens_novos
    return alocacao, custo_total

# Aplicação do Método de Vogel
alocacao, custo_total = metodo_vogel(custos, capacidades, demandas)

print("\nUsando Método de Aproximação de Vogel")
print("Alocação de transporte:")

for i in range(alocacao.shape[0]):
    for j in range(alocacao.shape[1]):
        if alocacao[i, j] > 0:
            if adicionou_no_ficticio and i == len(capacidades) - 1:
                print(f"Nó fictício -> Construtora C{j + 1}: {alocacao[i, j]} unidades")
            else:
                print(f"Filial F{i + 1} -> Construtora C{j + 1}: {alocacao[i, j]} unidades")

print(f"\nCusto Total: {custo_total}")