import os
import sys
from utils_grafo import ler_arquivo_dat
from path_scanning import path_scanning
from solucao_writer import salvar_solucao
from greedy_constructor import greedy_constructor

def main():
    # Usando caminhos absolutos baseados na localização do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_instancias = os.path.abspath(os.path.join(script_dir, '..', 'selected_instances'))
    pasta_saida = os.path.abspath(os.path.join(script_dir, 'solucoes'))
    os.makedirs(pasta_saida, exist_ok=True)
    capacidade = 15  # Ajuste conforme necessário para cada instância
    algoritmo = 'greedy'  # padrão
    if len(sys.argv) > 1:
        algoritmo = sys.argv[1].lower()
    for nome_arq in os.listdir(pasta_instancias):
        if not nome_arq.endswith('.dat'):
            continue
        caminho_instancia = os.path.join(pasta_instancias, nome_arq)
        grafo = ler_arquivo_dat(caminho_instancia)
        if algoritmo == 'path':
            rotas = path_scanning(grafo, capacidade)
        else:
            rotas = greedy_constructor(grafo, capacidade)
        nome_saida = f"sol-{os.path.splitext(nome_arq)[0]}.dat"
        caminho_saida = os.path.join(pasta_saida, nome_saida)
        salvar_solucao(rotas, capacidade, caminho_saida)
        print(f"Solução salva em {caminho_saida} usando {algoritmo}")

if __name__ == '__main__':
    main() 