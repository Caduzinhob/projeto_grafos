import os
import csv

def ler_solucao(caminho):
    with open(caminho, 'r') as f:
        linhas = f.readlines()
        custo_total = float(linhas[0].strip())
        num_rotas = int(linhas[1].strip())
        return custo_total, num_rotas

def ler_valores_referencia(caminho):
    valores = {}
    with open(caminho, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Pula o cabeçalho
        for linha in reader:
            nome = linha[0].strip()
            solucao = float(linha[1].strip())
            num_rotas = int(linha[2].strip())
            valores[nome] = (solucao, num_rotas)
    return valores

def main():
    # Caminhos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_solucoes = os.path.join(script_dir, 'solucoes')
    arquivo_referencia = os.path.join(script_dir, '..', 'padroes', 'reference_values.csv')
    
    # Lê valores de referência
    valores_ref = ler_valores_referencia(arquivo_referencia)
    
    # Compara resultados
    total_arquivos = 0
    total_melhores = 0
    total_piores = 0
    total_iguais = 0
    
    print("\nComparando resultados:")
    print("Nome, Custo (Nosso), Rotas (Nosso), Custo (Ref), Rotas (Ref), Diferença %")
    print("-" * 80)
    
    for arquivo in sorted(os.listdir(pasta_solucoes)):
        if not arquivo.startswith('sol-') or not arquivo.endswith('.dat'):
            continue
            
        nome = arquivo[4:-4]  # Remove 'sol-' e '.dat'
        if nome not in valores_ref:
            continue
            
        caminho_solucao = os.path.join(pasta_solucoes, arquivo)
        custo, rotas = ler_solucao(caminho_solucao)
        custo_ref, rotas_ref = valores_ref[nome]
        
        diferenca = ((custo - custo_ref) / custo_ref) * 100
        
        if diferenca < 0:
            status = "MELHOR"
            total_melhores += 1
        elif diferenca > 0:
            status = "PIOR"
            total_piores += 1
        else:
            status = "IGUAL"
            total_iguais += 1
            
        print(f"{nome}, {custo}, {rotas}, {custo_ref}, {rotas_ref}, {diferenca:.2f}% ({status})")
        total_arquivos += 1
    
    print("\nResumo:")
    print(f"Total de arquivos comparados: {total_arquivos}")
    print(f"Resultados melhores: {total_melhores} ({(total_melhores/total_arquivos)*100:.1f}%)")
    print(f"Resultados piores: {total_piores} ({(total_piores/total_arquivos)*100:.1f}%)")
    print(f"Resultados iguais: {total_iguais} ({(total_iguais/total_arquivos)*100:.1f}%)")

if __name__ == '__main__':
    main() 