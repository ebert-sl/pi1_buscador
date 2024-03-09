import re

def autoridade(soup):
  # Autoridade - Quantidade de links na página - 10 pontos por link

  links = soup.find_all('a')
  autoridade = 0 

  for link in links:
    autoridade += 10

  print(f"Autoridade: {autoridade} pontos")

def frequencia_termos(soup, termo):
  # Frequência dos Termos - Quantidade de termos encontrados na página - 5 pontos por termo
  # Caso não seja encontrado o termo, a página não será listada

  termos = soup.find_all(string = re.compile(termo)) 
  frequencia_termos = 0

  for termo in termos:
    frequencia_termos += 5

  if (frequencia_termos == 0):
    print("A página não será listada pois não foi encontrado o termo.") 
  else:
    print(f"Frequência de Termos: {frequencia_termos} pontos")