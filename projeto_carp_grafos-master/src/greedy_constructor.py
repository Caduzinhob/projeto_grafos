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
            
            # Como os vizinhos já estão ordenados por peso, podemos parar antes
            for v, peso in adj[u]:
                if v not in visitados:
                    nova_dist = d + peso
                    if nova_dist < dist[v]:
                        dist[v] = nova_dist
                        heappush(pq, (nova_dist, v))
        return dist
    return dijkstra

def greedy_constructor(grafo, capacidade, deposito='1'):
    print(f"  Iniciando construção gulosa (capacidade: {capacidade})")
    
    # Pré-processa serviços requeridos com seus custos
    servicos = []
    
    # Processa vértices requeridos
    for v in grafo.vertices_req:
        demanda = 1  # Demanda padrão para visitar o vértice
        custo = 1    # Custo padrão para visitar o vértice
        servicos.append({
            'u': v,
            'v': v,  # Mesmo vértice pois é uma visita
            'demanda': demanda,
            'custo': custo,
            'tipo': 'vertice',
            'ratio': custo / demanda
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
            'tipo': 'aresta',
            'ratio': custo / demanda if demanda > 0 else float('inf')
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
            'tipo': 'arco',
            'ratio': custo / demanda if demanda > 0 else float('inf')
        })
    
    print(f"  Total de serviços: {len(servicos)} ({len(grafo.vertices_req)} vértices, {len(grafo.arestas_req)} arestas, {len(grafo.arcos_req)} arcos)")
    
    if not servicos:
        print("  Nenhum serviço para processar!")
        return []
    
    # Ordena serviços por ratio (custo/demanda)
    servicos.sort(key=lambda s: s['ratio'])
    
    # Usa set para operações O(1)
    nao_atendidos = set((s['u'], s['v'], s['tipo']) for s in servicos)
    rotas = []
    total_servicos = len(nao_atendidos)
    
    # Função para verificar se um serviço pode ser adicionado à rota atual
    def pode_adicionar_servico(servico, carga_atual):
        return servico['demanda'] + carga_atual <= capacidade
    
    while nao_atendidos:
        rota = []
        carga = 0
        servicos_na_rota = 0
        
        # Tenta adicionar serviços à rota atual
        for s in servicos:
            if (s['u'], s['v'], s['tipo']) not in nao_atendidos:
                continue
                
            if pode_adicionar_servico(s, carga):
                rota.append(s)
                carga += s['demanda']
                nao_atendidos.remove((s['u'], s['v'], s['tipo']))
                servicos_na_rota += 1
        
        if servicos_na_rota > 0:
            rotas.append(rota)
            print(f"  Rota {len(rotas)} criada com {servicos_na_rota} serviços (restam {len(nao_atendidos)} de {total_servicos})")
        else:
            # Se não conseguiu adicionar nenhum serviço, provavelmente a capacidade é muito pequena
            print("  Aviso: Não foi possível adicionar mais serviços - capacidade insuficiente")
            break
    
    print(f"  Construção concluída: {len(rotas)} rotas criadas")
    return rotas 