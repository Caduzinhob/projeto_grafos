from greedy_constructor import criar_lista_adjacencia, dijkstra_com_cache, calcular_custo_rota

def salvar_solucao(rotas, grafo, capacidade, nome_arquivo_saida, deposito='1'):
    # Cria estruturas auxiliares para cálculo de caminhos mínimos
    adj = criar_lista_adjacencia(grafo)
    shortest_path = dijkstra_com_cache(adj, grafo.vertices)
    
    # Cálculo dos totais
    custo_total = 0
    total_rotas = len(rotas)
    # Para simplificação, clocks são fictícios
    clocks = 0
    clocks_melhor_sol = 0
    linhas_rotas = []
    
    for idx, rota in enumerate(rotas, 1):
        # Calcula demanda e custo total da rota (incluindo deslocamentos)
        demanda_rota = sum(s['demanda'] for s in rota)
        custo_rota = calcular_custo_rota(rota, grafo, deposito, shortest_path)
        custo_total += custo_rota
        
        # Número de visitas (serviços + depósito no início e fim)
        visitas = len(rota) + 1
        
        # Gera linha da rota
        linha = f" 0 1 {idx} {demanda_rota} {custo_rota}  {visitas} (D 0,1,1)"
        for s in rota:
            linha += f" (S 0,{s['u']},{s['v']})"
        linha += " (D 0,1,1)"
        linhas_rotas.append(linha)
    
    # Salva o arquivo
    with open(nome_arquivo_saida, 'w') as f:
        f.write(f"{custo_total}\n")
        f.write(f"{total_rotas}\n")
        f.write(f"{clocks}\n")
        f.write(f"{clocks_melhor_sol}\n")
        for linha in linhas_rotas:
            f.write(linha + '\n') 