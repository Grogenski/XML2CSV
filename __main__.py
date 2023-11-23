import os
from bs4 import BeautifulSoup
import time
import warnings
from src.utils import CSVReader, CSVWriter, NFExtractor, TaxCalculator
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    # Pasta onde estará os arquivos XML
    path = 'input'

    n_xmls = 0
    for filename in os.listdir(path):
        if filename.endswith('.xml') or filename.endswith('.XML'):
            n_xmls += 1

    if len(os.listdir(path)) == 0:
    print("------------------------------------------------------------------------")
    print("Sem arquivos XML para processamento. Programa finalizado.")
    print("------------------------------------------------------------------------")
    exit()

    print("------------------------------------------------------------------------")
    print(f"{n_xmls} NFe(s) encontrada(s).")
    print(f"Iniciando processamento de NFes.")
    print("------------------------------------------------------------------------\n")

    # Controle do tempo de processamento
    start = time.time()

    # Percorrer cada arquivo contido na pasta de trabalho e identificar os arquivos XML
    resume = []
    for filename in os.listdir(path):
        if filename.endswith('.xml') or filename.endswith('.XML'):
            dfs = []
            dfs_simples = []
            dfs_iva = []

            file_path = os.path.join(path, filename)

            # Converter as notas XML para DataFrames
            nfe = NFExtractor(file_path)
            df = nfe.NfeInfo()

            resume.append(df)

            csv = CSVWriter()
            csv.saveONEnfe(df, file_path)

    collect = CSVWriter()
    collect.saveALLnfe(resume)

    end_time = time.time() - start

    print("------------------------------------------------------------------------")
    print(f"Programa Finalizado. {len(resume)} arquivo(s) processado(s).")
    print(f"Tempo de execução: {end_time:.2f} segundo(s)")
    print("------------------------------------------------------------------------")
