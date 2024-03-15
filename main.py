import requests
import requests_cache
import re # Expressão regular
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from funcoes_pontuacao import *

def main():
  url = input("Digite a URL desejada: ")
  termo = input("Digite o termo que deseja buscar: ")

  if re.match(r'^\s*$', termo): 
    # ^ início da string | \s* zero ou mais espaços em branco | $ final da string
    print("O termo está vazio ou contém apenas espaços em branco.\n")
    menu_continuar()

  try:
    requests_cache.install_cache('./cache/banco')
    response = requests.get(url, verify=True)
    soup = BeautifulSoup(response.text, 'html.parser')
  except Exception as e:
    print(f"----------------------------------------\n"
          f"URL inválida ou digitada incorretamente!\n"
          f"----------------------------------------\n"
    ) 
    menu_continuar()

  print("\n-----------------------")
  total = autoridade(soup) + frequencia_termos(soup, termo) + uso_em_tags(soup, termo) + auto_referencia(soup, url) + frescor(soup)
  print(f"Total: {total} pontos")
  print("-----------------------\n")
  menu_continuar()

def menu_continuar():
  continuar = input("Deseja continuar usando o programa?\n1 - Sim\n2 - Não\n")
  if (continuar == "1"):
    print("")
    main()
  elif (continuar == "2"):
    print("\nAté logo!")
    sys.exit()
  else:
    print("-----------------\nComando inválido!\n-----------------\n")
    menu_continuar()

main()