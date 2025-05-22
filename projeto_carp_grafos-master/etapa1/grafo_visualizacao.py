def mostra_arestas(self):
    print("\nTodas as arestas:")
    for (u, v), pesos in self.arestas.items():
        print(f"{u} — {v}: {pesos}")
    print("\nArestas requeridas:")
    for (u, v), peso in self.arestas_req.items():
        print(f"{u} — {v}: {peso}")

def mostra_arcos(self):
    print("\nTodos os arcos:")
    for (u, v), pesos in self.arcos.items():
        print(f"{u} → {v}: {pesos}")
    print("\nArcos requeridos:")
    for (u, v), peso in self.arcos_req.items():
        print(f"{u} → {v}: {peso}")

def contar(self):
    print("\nEstatísticas do Grafo:")
    print(f"Total de Vértices: {len(self.vertices)}")
    print(f"Total de Arestas: {len(self.arestas)}")
    print(f"Total de Arcos: {len(self.arcos)}")
    print(f"Vértices Requeridos: {len(self.vertices_req)}")
    print(f"Arestas Requeridas: {len(self.arestas_req)}")
    print(f"Arcos Requeridos: {len(self.arcos_req)}")
    print(f"Densidade: {self.densidade_grafo():.4f}")
    print(f"Componentes Conectados: {self.componentes_conectados()}")
    print(f"Grau Mínimo: {self.grau_minimo()}")
    print(f"Grau Máximo: {self.grau_maximo()}")
    print(f"Caminho Médio: {self.caminho_medio():.2f}")
    print(f"Diâmetro: {self.diametro()}")

def mostra_intermediacao(self):
    _, intermed = self.floyd_warshall_intermediacao()
    print("\nIntermediação:")
    for no, score in sorted(intermed.items()):
        print(f"Nó {no}: {score}") 