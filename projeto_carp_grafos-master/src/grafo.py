class Grafo:
    def __init__(self):
        self.vertices = set()
        self.arestas = {}  # {(u,v): [custo, demanda]}
        self.arcos = {}    # {(u,v): [custo, demanda]}
        self.vertices_req = set()
        self.arestas_req = {}  # {(u,v): [custo, demanda]}
        self.arcos_req = {}    # {(u,v): [custo, demanda]}
        self.adj = {}  # Lista de adjacência para acesso rápido
    
    def add_vertice(self, v):
        self.vertices.add(v)
        if v not in self.adj:
            self.adj[v] = set()
    
    def add_vertice_req(self, v):
        self.add_vertice(v)
        self.vertices_req.add(v)
    
    def add_aresta(self, u, v, peso):
        """Adiciona uma aresta com custo e demanda"""
        self.add_vertice(u)
        self.add_vertice(v)
        if isinstance(peso, list):
            self.arestas[(u,v)] = peso
        else:
            self.arestas[(u,v)] = [peso, 0]  # Se não for lista, assume que é só custo
        self.adj[u].add(v)
        self.adj[v].add(u)
    
    def add_aresta_req(self, u, v, peso):
        """Adiciona uma aresta requerida com custo e demanda"""
        self.add_aresta(u, v, peso)
        if isinstance(peso, list):
            self.arestas_req[(u,v)] = peso
        else:
            self.arestas_req[(u,v)] = [peso, 0]
    
    def add_arco(self, u, v, peso):
        """Adiciona um arco com custo e demanda"""
        self.add_vertice(u)
        self.add_vertice(v)
        if isinstance(peso, list):
            self.arcos[(u,v)] = peso
        else:
            self.arcos[(u,v)] = [peso, 0]  # Se não for lista, assume que é só custo
        self.adj[u].add(v)
    
    def add_arco_req(self, u, v, peso):
        """Adiciona um arco requerido com custo e demanda"""
        self.add_arco(u, v, peso)
        if isinstance(peso, list):
            self.arcos_req[(u,v)] = peso
        else:
            self.arcos_req[(u,v)] = [peso, 0]
    
    def get_vizinhos(self, v):
        return self.adj[v]
    
    def get_peso(self, u, v):
        """Retorna o peso (custo) de uma aresta ou arco"""
        if (u,v) in self.arestas:
            peso = self.arestas[(u,v)]
            return peso[0] if isinstance(peso, list) else peso
        if (v,u) in self.arestas:  # Arestas são bidirecionais
            peso = self.arestas[(v,u)]
            return peso[0] if isinstance(peso, list) else peso
        if (u,v) in self.arcos:
            peso = self.arcos[(u,v)]
            return peso[0] if isinstance(peso, list) else peso
        return None
    
    def get_demanda(self, u, v):
        """Retorna a demanda de uma aresta ou arco"""
        if (u,v) in self.arestas:
            peso = self.arestas[(u,v)]
            return peso[1] if isinstance(peso, list) else 0
        if (v,u) in self.arestas:  # Arestas são bidirecionais
            peso = self.arestas[(v,u)]
            return peso[1] if isinstance(peso, list) else 0
        if (u,v) in self.arcos:
            peso = self.arcos[(u,v)]
            return peso[1] if isinstance(peso, list) else 0
        return 0
    
    def tem_arco(self, u, v):
        """Verifica se existe um arco de u para v no grafo"""
        return (u,v) in self.arcos or (u,v) in self.arcos_req
    
    def tem_aresta(self, u, v):
        """Verifica se existe uma aresta entre u e v no grafo"""
        return (u,v) in self.arestas or (v,u) in self.arestas or (u,v) in self.arestas_req or (v,u) in self.arestas_req
    
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