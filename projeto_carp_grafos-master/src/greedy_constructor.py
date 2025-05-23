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
        if isinstance(peso, list):
            peso = peso[0]
        adj[u].append((v, peso))
        adj[v].append((u, peso))  # Arestas são bidirecionais
    for (u, v), peso in grafo.arcos.items():
        if isinstance(peso, list):
            peso = peso[0]
        adj[u].append((v, peso))
    return adj

def dijkstra(grafo, origem, destino=None):
    """Implementa Dijkstra para encontrar caminhos mais curtos"""
    dist = {v: float('inf') for v in grafo.vertices}
    dist[origem] = 0
    prev = {v: None for v in grafo.vertices}
    pq = [(0, origem)]
    visitados = set()
    
    # Cria lista de adjacência local
    adj = criar_lista_adjacencia(grafo)

    while pq:
        d, u = heappop(pq)
        
        if u in visitados:
            continue
            
        visitados.add(u)
        
        if destino and u == destino:
            break
            
        # Verifica vizinhos
        for v, peso in adj[u]:
            if v not in visitados:
                novo_custo = d + peso
                if novo_custo < dist[v]:
                    dist[v] = novo_custo
                    prev[v] = (u, 'aresta' if (u, v) in grafo.arestas or (v, u) in grafo.arestas else 'arco')
                    heappush(pq, (dist[v], v))
    
    return dist, prev

def reconstruir_caminho(prev, origem, destino, grafo):
    """Reconstrói o caminho a partir do dicionário de predecessores"""
    if destino not in prev or prev[destino] is None:
        return [], float('inf')
        
    caminho = []
    custo = 0
    atual = destino
    
    while atual != origem:
        anterior, tipo = prev[atual]
        caminho.append((anterior, atual, tipo))
        # Adiciona custo do deslocamento
        if tipo == 'aresta':
            peso = grafo.get_peso(anterior, atual)
            if isinstance(peso, list):
                peso = peso[0]
            custo += peso
        else:  # arco
            peso = grafo.get_peso(anterior, atual)
            if isinstance(peso, list):
                peso = peso[0]
            custo += peso
        atual = anterior
        
    return list(reversed(caminho)), custo

@lru_cache(maxsize=1024)
def calcular_distancia_entre_vertices(grafo, origem, destino, deposito):
    """Calcula e armazena em cache a distância entre dois vértices"""
    dist, prev = dijkstra(grafo, origem)
    if destino not in dist:
        return float('inf'), None
    return dist[destino], prev

def calcular_custo_rota(rota, grafo, deposito):
    """Calcula o custo total de uma rota considerando todos os custos"""
    if not rota:
        return 0
    
    custo_total = 0
    
    # Custo para ir do depósito ao primeiro serviço
    primeiro_servico = rota[0]
    dist_inicial, prev_inicial = calcular_distancia_entre_vertices(grafo, deposito, primeiro_servico['u'], deposito)
    if dist_inicial == float('inf'):
        return float('inf')
    custo_total += dist_inicial
    
    # Custo dos serviços e deslocamentos entre eles
    for i, servico in enumerate(rota):
        # Adiciona custo do serviço
        if servico['tipo'] == 'aresta':
            # Para arestas, podemos atender em qualquer direção
            custo_total += servico['custo']
        else:  # arco
            # Para arcos, precisamos respeitar a direção
            if not grafo.tem_arco(servico['u'], servico['v']):
                return float('inf')  # Caminho impossível
            custo_total += servico['custo']
        
        # Se não é o último serviço, adiciona custo até o próximo
        if i < len(rota) - 1:
            proximo = rota[i + 1]
            dist, _ = calcular_distancia_entre_vertices(grafo, servico['v'], proximo['u'], deposito)
            if dist == float('inf'):
                return float('inf')
            custo_total += dist
    
    # Custo para voltar ao depósito do último serviço
    ultimo_servico = rota[-1]
    dist_final, _ = calcular_distancia_entre_vertices(grafo, ultimo_servico['v'], deposito, deposito)
    if dist_final == float('inf'):
        return float('inf')
    custo_total += dist_final
    
    return custo_total

def encontrar_servicos_proximos(servico, servicos_disponiveis, grafo, max_dist=float('inf')):
    """Encontra serviços próximos que podem ser atendidos em conjunto"""
    proximos = []
    for s in servicos_disponiveis:
        if s == servico:
            continue
        # Calcula distância entre o fim do serviço atual e início do próximo
        dist, _ = calcular_distancia_entre_vertices(grafo, servico['v'], s['u'], None)
        if dist != float('inf'):
            proximos.append((s, dist))
    return sorted(proximos, key=lambda x: x[1])

def encontrar_melhor_insercao(servicos_disponiveis, rota_atual, grafo, deposito, capacidade):
    """Encontra a melhor posição para inserir um novo serviço na rota"""
    melhor_servico = None
    melhor_posicao = None
    menor_custo_adicional = float('inf')
    
    carga_atual = sum(s['demanda'] for s in rota_atual)
    
    # Se a rota está vazia, escolhe o serviço mais próximo do depósito
    if not rota_atual:
        dist_deposito, prev_deposito = dijkstra(grafo, deposito)
        for s in servicos_disponiveis:
            if s['demanda'] > capacidade:
                continue
                
            # Para arcos, verifica se é possível atender na direção correta
            if s['tipo'] == 'arco' and not grafo.tem_arco(s['u'], s['v']):
                continue
                
            # Calcula custo total (ida + serviço + volta)
            dist_ida = dist_deposito[s['u']]
            if dist_ida == float('inf'):
                continue
                
            dist_volta, _ = calcular_distancia_entre_vertices(grafo, s['v'], deposito, deposito)
            if dist_volta == float('inf'):
                continue
                
            custo_total = dist_ida + s['custo'] + dist_volta
            if custo_total < menor_custo_adicional:
                menor_custo_adicional = custo_total
                melhor_servico = [s]
                melhor_posicao = 0
                
        return melhor_servico, melhor_posicao, menor_custo_adicional
    
    # Para rota não vazia, tenta inserir em cada posição
    custo_atual = calcular_custo_rota(rota_atual, grafo, deposito)
    
    for s in servicos_disponiveis:
        # Verifica capacidade
        if carga_atual + s['demanda'] > capacidade:
            continue
            
        # Para arcos, verifica se é possível atender na direção correta
        if s['tipo'] == 'arco' and not grafo.tem_arco(s['u'], s['v']):
            continue
            
        # Tenta inserir em cada posição da rota
        for i in range(len(rota_atual) + 1):
            nova_rota = rota_atual[:i] + [s] + rota_atual[i:]
            novo_custo = calcular_custo_rota(nova_rota, grafo, deposito)
            
            if novo_custo == float('inf'):
                continue  # Inserção impossível nesta posição
                
            custo_adicional = novo_custo - custo_atual
            
            # Favorece inserções que maximizam o uso da capacidade
            fator_capacidade = (carga_atual + s['demanda']) / capacidade
            custo_ajustado = custo_adicional * (1 - fator_capacidade * 0.1)
            
            if custo_ajustado < menor_custo_adicional:
                menor_custo_adicional = custo_ajustado
                melhor_servico = [s]
                melhor_posicao = i
    
    return melhor_servico, melhor_posicao, menor_custo_adicional

def greedy_constructor(grafo, capacidade, deposito='1'):
    """Constrói uma solução usando estratégia gulosa melhorada"""
    rotas = []
    servicos = []
    
    # Coleta todos os serviços (arestas e arcos requeridos)
    for (u, v), peso in grafo.arestas_req.items():  # Mudança: usa arestas_req em vez de arestas
        if isinstance(peso, list) and len(peso) > 1 and peso[1] > 0:  # Aresta requerida
            servicos.append({
                'u': u,
                'v': v,
                'tipo': 'aresta',
                'custo': peso[0],
                'demanda': peso[1]
            })
    
    for (u, v), peso in grafo.arcos_req.items():  # Mudança: usa arcos_req em vez de arcos
        if isinstance(peso, list) and len(peso) > 1 and peso[1] > 0:  # Arco requerido
            servicos.append({
                'u': u,
                'v': v,
                'tipo': 'arco',
                'custo': peso[0],
                'demanda': peso[1]
            })
    
    # Se não há serviços para atender, retorna lista vazia
    if not servicos:
        print("Nenhum serviço requerido encontrado no grafo")
        return []
        
    # Ordena serviços por demanda (decrescente) para tentar maximizar uso da capacidade
    servicos.sort(key=lambda x: x['demanda'], reverse=True)
    
    servicos_restantes = servicos.copy()
    rota_atual = []
    carga_atual = 0
    
    while servicos_restantes:
        # Encontra melhor serviço para inserir
        servicos_inserir, posicao, custo = encontrar_melhor_insercao(
            servicos_restantes, rota_atual, grafo, deposito, capacidade
        )
        
        # Se não encontrou serviço válido ou rota atual está cheia
        if not servicos_inserir or carga_atual + sum(s['demanda'] for s in servicos_inserir) > capacidade:
            if rota_atual:
                rotas.append(rota_atual)
            rota_atual = []
            carga_atual = 0
            continue
        
        # Insere serviços na rota
        for s in servicos_inserir:
            rota_atual = rota_atual[:posicao] + [s] + rota_atual[posicao:]
            servicos_restantes.remove(s)
            carga_atual += s['demanda']
            posicao += 1
    
    # Adiciona última rota se não estiver vazia
    if rota_atual:
        rotas.append(rota_atual)
    
    return rotas 