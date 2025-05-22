class Grafo:
    def __init__(self):
        self.vertices = set()
        self.arestas = {}  # {(u,v): peso}
        self.arcos = {}    # {(u,v): peso}
        self.vertices_req = set()
        self.arestas_req = {}  # {(u,v): peso}
        self.arcos_req = {}    # {(u,v): peso}
        self.adj = {}  # Lista de adjacência para acesso rápido
    
    def add_vertice(self, v):
        self.vertices.add(v)
        if v not in self.adj:
            self.adj[v] = set()
    
    def add_vertice_req(self, v):
        self.add_vertice(v)
        self.vertices_req.add(v)
    
    def add_aresta(self, u, v, peso):
        self.add_vertice(u)
        self.add_vertice(v)
        self.arestas[(u,v)] = peso
        self.adj[u].add(v)
        self.adj[v].add(u)
    
    def add_aresta_req(self, u, v, peso):
        self.add_aresta(u, v, peso)
        self.arestas_req[(u,v)] = peso
    
    def add_arco(self, u, v, peso):
        self.add_vertice(u)
        self.add_vertice(v)
        self.arcos[(u,v)] = peso
        self.adj[u].add(v)
    
    def add_arco_req(self, u, v, peso):
        self.add_arco(u, v, peso)
        self.arcos_req[(u,v)] = peso
    
    def get_vizinhos(self, v):
        return self.adj[v]
    
    def get_peso(self, u, v):
        if (u,v) in self.arestas:
            return self.arestas[(u,v)]
        if (v,u) in self.arestas:  # Arestas são bidirecionais
            return self.arestas[(v,u)]
        if (u,v) in self.arcos:
            return self.arcos[(u,v)]
        return None
    
    def __str__(self):
        return f"Grafo com {len(self.vertices)} vértices, {len(self.arestas)} arestas e {len(self.arcos)} arcos"

from grafo_add import add_vertice, add_vertice_req, add_aresta, add_aresta_req, add_arco, add_arco_req
from grafo_analise import densidade_grafo, calcular_graus, grau_minimo, grau_maximo, floyd_warshall_intermediacao, caminho_medio, diametro, componentes_conectados
from grafo_visualizacao import mostra_arestas, mostra_arcos, contar, mostra_intermediacao

Grafo.add_vertice = add_vertice
Grafo.add_vertice_req = add_vertice_req
Grafo.add_aresta = add_aresta
Grafo.add_aresta_req = add_aresta_req
Grafo.add_arco = add_arco
Grafo.add_arco_req = add_arco_req
Grafo.densidade_grafo = densidade_grafo
Grafo.componentes_conectados = componentes_conectados
Grafo.calcular_graus = calcular_graus
Grafo.grau_minimo = grau_minimo
Grafo.grau_maximo = grau_maximo
Grafo.floyd_warshall_intermediacao = floyd_warshall_intermediacao
Grafo.caminho_medio = caminho_medio
Grafo.diametro = diametro
Grafo.mostra_arestas = mostra_arestas
Grafo.mostra_arcos = mostra_arcos
Grafo.contar = contar
Grafo.mostra_intermediacao = mostra_intermediacao

if __name__ == "__main__":
    from .utils_grafo import ler_arquivo_dat
    grafo = ler_arquivo_dat('selected_instances/BHW1.dat')
    grafo.contar()
    grafo.mostra_intermediacao()
#grafo.mostra_arestas()
#grafo.mostra_arcos()