import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../etapa1'))
from utils_grafo import ler_arquivo_dat

# Função principal do algoritmo construtivo Path-Scanning

def path_scanning(grafo, capacidade, deposito='1'):
    # Lista de serviços requeridos: [(u, v, demanda, custo, tipo)]
    servicos = []
    for (u, v), demanda in grafo.arestas_req.items():
        custo = min(grafo.arestas.get((u, v), grafo.arestas.get((v, u), [demanda])))
        servicos.append({'u': u, 'v': v, 'demanda': demanda, 'custo': custo, 'tipo': 'aresta'})
    for (u, v), demanda in grafo.arcos_req.items():
        custo = min(grafo.arcos.get((u, v), [demanda]))
        servicos.append({'u': u, 'v': v, 'demanda': demanda, 'custo': custo, 'tipo': 'arco'})
    nao_atendidos = set((s['u'], s['v'], s['tipo']) for s in servicos)

    rotas = []
    while nao_atendidos:
        rota = []
        carga = 0
        custo_rota = 0
        pos = deposito
        while True:
            # Candidatos que cabem na capacidade
            candidatos = [s for s in servicos if (s['u'], s['v'], s['tipo']) in nao_atendidos and s['demanda'] + carga <= capacidade]
            if not candidatos:
                break
            # Critério: menor custo de deslocamento do pos até u
            # Usa floyd_warshall_intermediacao para matriz de distâncias
            dist_matrix, _ = grafo.floyd_warshall_intermediacao()
            idx = {v: i for i, v in enumerate(sorted(grafo.vertices))}
            def custo_total(s):
                return dist_matrix[idx[pos]][idx[s['u']]] + s['custo']
            prox = min(candidatos, key=custo_total)
            rota.append(prox)
            carga += prox['demanda']
            custo_rota += custo_total(prox)
            nao_atendidos.remove((prox['u'], prox['v'], prox['tipo']))
            pos = prox['v']
        rotas.append(rota)
    return rotas 