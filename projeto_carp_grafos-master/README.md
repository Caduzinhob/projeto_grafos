Este é um trabalho da disciplina de Algoritmos em Grafos - GCC218

- Ministrado pelo: Professor Mayron César de Oliveira Moreira.
- Realizado pelos alunos:
- Lucca Guedes Batistela - 202320985
- Carlos Eduardo Borges de Sousa - 202020296



# Graph Visualization for CARP Instances

## Overview
This module provides a Jupyter Notebook (`visualizacao_resultados.ipynb`) for visualizing graph metrics and statistics derived from CARP (Capacitated Arc Routing Problem) instances. The notebook generates a detailed table of metrics and a bar chart for numerical data, helping users analyze the structure and properties of the graph.

## Features
The visualization includes:
1. **Graph Metrics Table**:
   - Total number of vertices, edges, and arcs.
   - Number of required vertices, edges, and arcs.
   - Graph density, minimum and maximum vertex degrees.
   - Average path length and graph diameter.
   - Betweenness centrality (intermediation) for each vertex.

2. **Bar Chart**:
   - Displays numerical metrics for quick comparison.

## File Structure
- `grafos.py` : Main project file.
- `visualizacao_resultados.ipynb`: The main notebook for graph visualization.
- `selected_instances/`: Folder containing `.dat` files with CARP instances.

## How to Use
1. **Open the Notebook**:
   - Launch Jupyter Notebook and open `visualizacao_resultados.ipynb`.

2. **Load a CARP Instance**:
   - Modify the `arquivo` variable in the notebook to point to the desired `.dat` file:
     ```python
     arquivo = r"d:\Meus arquivos\Documentos\GitHub\projeto_carp_grafos\selected_instances\BHW1.dat"
     ```

3. **Run the Notebook**:
   - Execute all cells to generate the metrics table and bar chart.

4. **Analyze the Results**:
   - The notebook will display:
     - A table with graph metrics.
     - A separate table for betweenness centrality (intermediation) values.
     - A bar chart for numerical metrics.

## Example Output
### Metrics Table
| Metric                     | Value     |
|----------------------------|-----------|
| Total de Vértices          | 56        |
| Total de Arestas           | 16        |
| Total de Arcos             | 31        |
| Vértices Requeridos        | 16        |
| Arestas Requeridas         | 16        |
| Arcos Requeridos           | 31        |
| Densidade                  | 0.015260  |
| Grau Mínimo                | 0         |
| Grau Máximo                | 5         |
| Caminho Médio              | 2.345678  |
| Diâmetro                   | 10        |

### Intermediation Table
| Vertex   | Intermediation |
|----------|----------------|
| 1        | 18       |
| 2        | 20       |
| 3        | 32       |
| ...      | ...            |

### Bar Chart
A bar chart is generated to visualize numerical metrics such as density, average path length, and vertex degrees.

## Requirements
- Python 3.x
- Libraries:
  - `pandas`
  - `matplotlib`
  - `os`

Install the required libraries using:
```bash
pip install pandas matplotlib
