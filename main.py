import csv
import glob
import os
import re
import sys
from datetime import datetime
from urllib.parse import urljoin

import pandas as pd
import requests
import requests_cache
from bs4 import BeautifulSoup
from funcoes_pontuacao import (
    auto_referencia,
    autoridade,
    frequencia_termos,
    frescor,
    uso_em_tags,
)

links_visitados = set()

def process_url(href, soup, termo, writer):
    print()
    print("-----------------------")
    print(f"\nPontuando a página: {href}")
    print("\n-----------------------")

    autoridade_val = autoridade(soup)
    frequencia_termos_val = frequencia_termos(soup, termo)
    uso_em_tags_val = uso_em_tags(soup, termo)
    auto_referencia_val = auto_referencia(soup, href)
    frescor_val = frescor(soup)

    total = (
        autoridade_val
        + frequencia_termos_val
        + uso_em_tags_val
        + auto_referencia_val
        + frescor_val
    )

    listado = ""
    if (frequencia_termos_val == 0):
        listado = "Não"
    else:
        listado = "Sim"

    print(f"Total: {total} pontos")
    print("-----------------------\n")
    writer.writerow([
        href, 
        autoridade_val, 
        frequencia_termos_val, 
        uso_em_tags_val, 
        auto_referencia_val, 
        frescor_val, 
        total,
        listado
    ])

def main():
    links_visitados.clear()
    url = input("Digite a URL desejada: ")
    termo = input("Digite o termo que deseja buscar: ")

    if re.match(r"^\s*$", termo):
        # ^ início da string | \s* zero ou mais espaços em branco | $ final da string
        print("O termo está vazio ou contém apenas espaços em branco.\n")
        menu_continuar()

    try:
        requests_cache.install_cache("./cache/banco")
        response = requests.get(url, verify=True)
        if response.status_code != 200:
            raise Exception

        soup = BeautifulSoup(response.text, "html.parser")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Criar o nome do arquivo com o timestamp
        filename = f"data_{timestamp}.csv"

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            if not os.path.exists('data.csv') or os.stat('data.csv').st_size == 0:
                writer.writerow([
                    "URL", 
                    "Autoridade", 
                    "Frequencia Termos", 
                    "Uso em Tags", 
                    "Auto Referencia", 
                    "Frescor", 
                    "Total",
                    "Listado"
                ])

            if url not in links_visitados:
                links_visitados.add(url)
                process_url(url, soup, termo, writer)

            for link in soup.find_all("a"):
                href = link.get("href")
                if href:
                    href = urljoin(url, href)

                    if href not in links_visitados:
                        links_visitados.add(href)
                        link_response = requests.get(href, verify=True)
                        link_soup = BeautifulSoup(link_response.text, "html.parser")
                        process_url(href, link_soup, termo, writer)

    except Exception:
        print(
            "----------------------------------------\n"
            "URL inválida ou digitada incorretamente!\n"
            "----------------------------------------\n"
        )

    menu_continuar()

def csv_para_excel():
    csv_files = glob.glob("data_*.csv")
    csv_files.sort(key=os.path.getmtime, reverse=True)
    if csv_files:
        data = pd.read_csv(csv_files[0])
        data_ordenada = data.sort_values("Total", ascending=False)
        data_ordenada.to_excel("data_ordenada.xlsx", index=False)
    else:
        print("Nenhum arquivo CSV encontrado.")

def menu_continuar():
    continuar = input("Deseja continuar usando o programa?\n1 - Sim\n2 - Não\n")
    if continuar == "1":
        print("")
        main()
    elif continuar == "2":
        print("\nAté logo!")
        csv_para_excel()
        sys.exit()
    else:
        print("-----------------\nComando inválido!\n-----------------\n")
        menu_continuar()

main()