import os
import sys
import time
import signal
import gc
from contextlib import contextmanager
from multiprocessing import Pool, cpu_count
from utils_grafo import ler_arquivo_dat
from solucao_writer import salvar_solucao
from greedy_constructor import greedy_constructor

def processar_arquivo(args):
    nome_arq, caminho_instancia, pasta_saida = args
    try:
        print(f"\nProcessando {nome_arq}")
        
        # Lê o grafo e libera memória não utilizada
        grafo, capacidade = ler_arquivo_dat(caminho_instancia)
        print(f"Arquivo lido: {len(grafo.vertices)} vértices, {len(grafo.arestas)} arestas, {len(grafo.arcos)} arcos")
        
        # Constrói a solução
        rotas = greedy_constructor(grafo, capacidade)
        if not rotas:
            return False, nome_arq, "Nenhuma rota criada"
        
        # Salva a solução
        nome_saida = f"sol-{os.path.splitext(nome_arq)[0]}.dat"
        caminho_saida = os.path.join(pasta_saida, nome_saida)
        salvar_solucao(rotas, capacidade, caminho_saida)
        
        # Libera memória explicitamente
        del grafo
        del rotas
        gc.collect()
        
        return True, nome_arq, None
        
    except Exception as e:
        return False, nome_arq, f"Erro: {str(e)}"

def main():
    # Usando caminhos absolutos baseados na localização do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_instancias = os.path.abspath(os.path.join(script_dir, '..', 'selected_instances'))
    pasta_saida = os.path.abspath(os.path.join(script_dir, 'solucoes'))
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Lista todos os arquivos .dat e ordena por tamanho
    arquivos = []
    for nome_arq in os.listdir(pasta_instancias):
        if nome_arq.endswith('.dat'):
            caminho = os.path.join(pasta_instancias, nome_arq)
            tamanho = os.path.getsize(caminho)
            arquivos.append((nome_arq, caminho, tamanho))
    
    # Ordena por tamanho (processa os menores primeiro)
    arquivos.sort(key=lambda x: x[2])
    
    # Prepara argumentos para processamento paralelo
    args = [(arq[0], arq[1], pasta_saida) for arq in arquivos]
    total_arquivos = len(args)
    
    # Usa menos cores para evitar sobrecarga de memória
    num_cores = max(1, cpu_count() - 1)
    print(f"\nIniciando processamento de {total_arquivos} arquivos usando {num_cores} cores")
    print("Arquivos ordenados por tamanho (processando menores primeiro)")
    
    # Inicializa contadores
    inicio = time.time()
    arquivos_processados = 0
    arquivos_com_erro = 0
    
    # Processa em paralelo com menos workers
    with Pool(processes=num_cores) as pool:
        try:
            for i, (sucesso, nome_arq, erro) in enumerate(pool.imap_unordered(processar_arquivo, args), 1):
                if sucesso:
                    arquivos_processados += 1
                    print(f"[{i}/{total_arquivos}] ✓ {nome_arq}")
                else:
                    arquivos_com_erro += 1
                    print(f"[{i}/{total_arquivos}] ✗ {nome_arq}: {erro}")
                
                # Mostra progresso
                porcentagem = (i / total_arquivos) * 100
                tempo_decorrido = time.time() - inicio
                tempo_medio = tempo_decorrido / i
                tempo_restante = tempo_medio * (total_arquivos - i)
                
                print(f"Progresso: {porcentagem:.1f}% | "
                      f"Tempo decorrido: {tempo_decorrido:.1f}s | "
                      f"Tempo restante estimado: {tempo_restante:.1f}s")
                
                # Força liberação de memória periodicamente
                if i % 5 == 0:
                    gc.collect()
                
        except KeyboardInterrupt:
            print("\nProcessamento interrompido pelo usuário")
            pool.terminate()
        except Exception as e:
            print(f"\nErro no processamento: {str(e)}")
            pool.terminate()
    
    tempo_total = time.time() - inicio
    
    print(f"\nResumo do processamento:")
    print(f"Total de arquivos .dat: {total_arquivos}")
    print(f"Arquivos processados com sucesso: {arquivos_processados}")
    print(f"Arquivos com erro: {arquivos_com_erro}")
    print(f"Tempo total: {tempo_total:.1f}s")
    print(f"Tempo médio por arquivo: {tempo_total/total_arquivos:.1f}s")

if __name__ == '__main__':
    main() 