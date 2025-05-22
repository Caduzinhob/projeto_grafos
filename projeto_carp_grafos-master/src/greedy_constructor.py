import os
import sys
from heapq import heappush, heappop
from collections import defaultdict
from functools import lru_cache

def criar_lista_adjacencia(grafo):
    # Cria lista de adjacência para acessar vizinhos mais rapidamente
    adj = defaultdict(list)
    # Pré-calcula todos os vizinhos de uma vez
    for (u, v), peso in grafo.arestas.items():
        adj[u].append((v, peso))
        adj[v].append((u, peso))  # Arestas são bidirecionais
    for (u, v), peso in grafo.arcos.items():
        adj[u].append((v, peso))
    # Ordena vizinhos por peso para otimizar Dijkstra
    for u in adj:
        adj[u].sort(key=lambda x: x[1])
    return adj

def dijkstra_com_cache(adj, vertices):
    # Decorator para cachear resultados do Dijkstra
    @lru_cache(maxsize=1000)
    def dijkstra(origem):
        dist = {v: float('inf') for v in vertices}
        dist[origem] = 0
        pq = [(0, origem)]
        visitados = set()
        
        while pq:
            d, u = heappop(pq)
            if u in visitados:
                continue
            visitados.add(u)
            
            for v, peso in adj[u]:
                if v not in visitados:
                    nova_dist = d + peso
                    if nova_dist < dist[v]:
                        dist[v] = nova_dist
                        heappush(pq, (nova_dist, v))
        return dist
    return dijkstra

def calcular_custo_rota(rota, grafo, deposito, shortest_path):
    """Calcula o custo total de uma rota incluindo deslocamentos"""
    if not rota:
        return 0
    
    custo_total = 0
    pos_atual = deposito
    
    # Custo para ir do depósito ao primeiro serviço
    primeiro_servico = rota[0]
    custo_total += shortest_path(deposito)[primeiro_servico['u']]
    
    # Custo dos serviços e deslocamentos entre eles
    for i, servico in enumerate(rota):
        # Custo do serviço
        custo_total += servico['custo']
        
        # Se não é o último serviço, adiciona custo até o próximo
        if i < len(rota) - 1:
            proximo = rota[i + 1]
            custo_total += shortest_path(servico['v'])[proximo['u']]
    
    # Custo para voltar ao depósito do último serviço
    ultimo_servico = rota[-1]
    custo_total += shortest_path(ultimo_servico['v'])[deposito]
    
    return custo_total

def encontrar_servico_mais_proximo(pos_atual, servicos_disponiveis, shortest_path):
    """Encontra o serviço mais próximo da posição atual"""
    melhor_servico = None
    menor_distancia = float('inf')
    
    for s in servicos_disponiveis:
        # Calcula distância até o início do serviço
        dist = shortest_path(pos_atual)[s['u']]
        if dist < menor_distancia:
            menor_distancia = dist
            melhor_servico = s
            
    return melhor_servico, menor_distancia

def greedy_constructor(grafo, capacidade, deposito='1'):
    print(f"  Iniciando construção gulosa (capacidade: {capacidade})")
    
    # Cria estruturas auxiliares
    adj = criar_lista_adjacencia(grafo)
    shortest_path = dijkstra_com_cache(adj, grafo.vertices)
    
    # Pré-processa serviços requeridos
    servicos = []
    
    # Processa vértices requeridos
    for v in grafo.vertices_req:
        # Usa a distância do depósito como custo base
        custo_base = shortest_path(deposito)[v]
        servicos.append({
            'u': v,
            'v': v,  # Mesmo vértice pois é uma visita
            'demanda': 1,  # Demanda padrão para visitar o vértice
            'custo': custo_base,
            'tipo': 'vertice'
        })
    
    # Processa arestas requeridas
    for (u, v), demanda in grafo.arestas_req.items():
        custo = grafo.get_peso(u, v)
        if custo is None:
            print(f"  Aviso: Aresta requerida ({u},{v}) não tem peso definido")
            continue
        if isinstance(custo, list):
            custo = custo[0]  # Pega o primeiro peso se for uma lista
        servicos.append({
            'u': u,
            'v': v,
            'demanda': demanda,
            'custo': custo,
            'tipo': 'aresta'
        })
    
    # Processa arcos requeridos
    for (u, v), demanda in grafo.arcos_req.items():
        custo = grafo.get_peso(u, v)
        if custo is None:
            print(f"  Aviso: Arco requerido ({u},{v}) não tem peso definido")
            continue
        if isinstance(custo, list):
            custo = custo[0]  # Pega o primeiro peso se for uma lista
        servicos.append({
            'u': u,
            'v': v,
            'demanda': demanda,
            'custo': custo,
            'tipo': 'arco'
        })
    
    print(f"  Total de serviços: {len(servicos)} ({len(grafo.vertices_req)} vértices, {len(grafo.arestas_req)} arestas, {len(grafo.arcos_req)} arcos)")
    
    if not servicos:
        print("  Nenhum serviço para processar!")
        return []
    
    # Usa set para operações O(1)
    servicos_disponiveis = set((s['u'], s['v'], s['tipo']) for s in servicos)
    servicos_por_chave = {(s['u'], s['v'], s['tipo']): s for s in servicos}
    rotas = []
    total_servicos = len(servicos_disponiveis)
    
    while servicos_disponiveis:
        rota = []
        carga = 0
        pos_atual = deposito
        servicos_na_rota = 0
        
        # Constrói a rota usando o serviço mais próximo
        while servicos_disponiveis:
            # Encontra o serviço mais próximo da posição atual
            servicos_candidatos = [servicos_por_chave[chave] for chave in servicos_disponiveis]
            proximo_servico, dist = encontrar_servico_mais_proximo(pos_atual, servicos_candidatos, shortest_path)
            
            if proximo_servico is None:
                break
                
            # Verifica se cabe na capacidade
            if carga + proximo_servico['demanda'] <= capacidade:
                # Calcula custo real da rota com o novo serviço
                rota_teste = rota + [proximo_servico]
                custo_atual = calcular_custo_rota(rota, grafo, deposito, shortest_path)
                custo_novo = calcular_custo_rota(rota_teste, grafo, deposito, shortest_path)
                
                # Só adiciona se o aumento no custo for razoável
                aumento_custo = custo_novo - custo_atual
                if len(rota) == 0 or aumento_custo <= 2 * proximo_servico['custo']:
                    rota.append(proximo_servico)
                    carga += proximo_servico['demanda']
                    servicos_disponiveis.remove((proximo_servico['u'], proximo_servico['v'], proximo_servico['tipo']))
                    servicos_na_rota += 1
                    pos_atual = proximo_servico['v']
                    continue
            
            # Se chegou aqui, não conseguiu adicionar o serviço
            break
        
        if servicos_na_rota > 0:
            rotas.append(rota)
            print(f"  Rota {len(rotas)} criada com {servicos_na_rota} serviços (restam {len(servicos_disponiveis)} de {total_servicos})")
        else:
            # Se não conseguiu adicionar nenhum serviço, provavelmente a capacidade é muito pequena
            print("  Aviso: Não foi possível adicionar mais serviços - capacidade insuficiente")
            break
    
    print(f"  Construção concluída: {len(rotas)} rotas criadas")
    return rotas 