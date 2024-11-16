import pulp


custos = {
    ('F1', 'C1'): 125, ('F1', 'C2'): 132, ('F1', 'C3'): 201,
    ('F2', 'C1'): 122, ('F2', 'C2'): 299, ('F2', 'C3'): 172,
    ('F3', 'C1'): 126, ('F3', 'C2'): 140, ('F3', 'C3'): 104,
    ('F4', 'C1'): 123, ('F4', 'C2'): 112, ('F4', 'C3'): 202,
    
}

capacidades = {'F1': 35, 'F2': 90, 'F3':  20, 'F4': 60}

demandas = {'C1': 80, 'C2': 115, 'C3': 65}


capacidade_total = sum(capacidades.values())
demanda_total = sum(demandas.values())


if capacidade_total < demanda_total:
    diferenca = demanda_total - capacidade_total
    print(f"Diferença (demandas_total - capacidades_total): {diferenca}")

    capacidades['F0'] = diferenca
    custos[('F0', 'C1')] = 0
    custos[('F0', 'C2')] = 0
    custos[('F0', 'C3')] = 0

else:
    print("A soma das capacidades das filiais é suficiente para atender à demanda, sem necessidade de nó fictício.")


prob = pulp.LpProblem("Problema_de_Transporte", pulp.LpMinimize)

x = pulp.LpVariable.dicts("Transporte", (capacidades.keys(), demandas.keys()), lowBound=0, cat='Continuous')

prob += pulp.lpSum(custos[i, j] * x[i][j] for i in capacidades for j in demandas), "Custo_Total"


for i in capacidades:
    prob += pulp.lpSum(x[i][j] for j in demandas) <= capacidades[i], f"Capacidade_{i}"


for j in demandas:
    prob += pulp.lpSum(x[i][j] for i in capacidades) == demandas[j], f"Demanda_{j}"

prob.solve()


print("Status da Solução:", pulp.LpStatus[prob.status])
print("Custo Total:", pulp.value(prob.objective))


for i in capacidades:
    filial_usada = False
    for j in demandas:
        if x[i][j].varValue > 0:
            print(f"Filial {i} -> Construtora {j}: {x[i][j].varValue} unidades")
            filial_usada = True

    if i == 'F0' and not filial_usada:
        print(f"Nó Fictício {i} não foi utilizado. A demanda foi balanceada.")

    if not filial_usada and i != 'F0':
        print(f"Filial {i} é uma filial 'fantasma' (não foi utilizada).")


if 'F0' in capacidades:
    print(f"O nó fictício F0 foi utilizado para balanceamento com {capacidades['F0']} unidades ajustadas.")
