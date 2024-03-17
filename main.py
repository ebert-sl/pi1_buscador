import re
import sys
from urllib.parse import urljoin

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


def main():
    url = input("Digite a URL desejada: ")
    termo = input("Digite o termo que deseja buscar: ")
    links_visitados = set()

    if re.match(r"^\s*$", termo):
        # ^ início da string | \s* zero ou mais espaços em branco | $ final da string
        print("O termo está vazio ou contém apenas espaços em branco.\n")
        menu_continuar()

    try:
        requests_cache.install_cache("./cache/banco")
        response = requests.get(url, verify=True)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                href = urljoin(url, href)

                if href not in links_visitados:
                    links_visitados.add(href)
                    link_response = requests.get(href, verify=True)
                    link_soup = BeautifulSoup(link_response.text, "html.parser")
                    
                    print()
                    print("-----------------------")
                    print(f"\nPontuando a página: {href}")
                    print("\n-----------------------")
                    total = (
                        autoridade(link_soup)
                        + frequencia_termos(link_soup, termo)
                        + uso_em_tags(link_soup, termo)
                        + auto_referencia(link_soup, url)
                        + frescor(link_soup)
                    )
                    print(f"Total: {total} pontos")
                    print("-----------------------\n")
    except Exception:
        print(
            "----------------------------------------\n"
            "URL inválida ou digitada incorretamente!\n"
            "----------------------------------------\n"
        )

    menu_continuar()


def menu_continuar():
    continuar = input("Deseja continuar usando o programa?\n1 - Sim\n2 - Não\n")
    if continuar == "1":
        print("")
        main()
    elif continuar == "2":
        print("\nAté logo!")
        sys.exit()
    else:
        print("-----------------\nComando inválido!\n-----------------\n")
        menu_continuar()


main()
