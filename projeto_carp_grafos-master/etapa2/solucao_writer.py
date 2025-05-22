def salvar_solucao(rotas, capacidade, nome_arquivo_saida, deposito='1'):
    # Cálculo dos totais
    custo_total = 0
    total_rotas = len(rotas)
    # Para simplificação, clocks são fictícios
    clocks = 0
    clocks_melhor_sol = 0
    linhas_rotas = []
    for idx, rota in enumerate(rotas, 1):
        demanda_rota = sum(s['demanda'] for s in rota)
        custo_rota = sum(s['custo'] for s in rota)
        custo_total += custo_rota
        visitas = len(rota) + 1  # ida e volta ao depósito
        linha = f" 0 1 {idx} {demanda_rota} {custo_rota}  {visitas} (D 0,1,1)"
        for s in rota:
            linha += f" (S 0,{s['u']},{s['v']})"
        linha += " (D 0,1,1)"
        linhas_rotas.append(linha)
    with open(nome_arquivo_saida, 'w') as f:
        f.write(f"{custo_total}\n")
        f.write(f"{total_rotas}\n")
        f.write(f"{clocks}\n")
        f.write(f"{clocks_melhor_sol}\n")
        for linha in linhas_rotas:
            f.write(linha + '\n') 