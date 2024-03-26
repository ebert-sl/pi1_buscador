import re
from datetime import datetime


def autoridade(soup):
    # Autoridade - Quantidade de links na página - 10 pontos por link

    links = soup.find_all("a")
    autoridade = 0

    for link in links:
        autoridade += 10

    print(f"Autoridade: {autoridade} pontos")

    return autoridade


def frequencia_termos(soup, termo):
    # Frequência dos Termos - Quantidade de termos encontrados na página - 5 pontos por termo
    # Caso não seja encontrado o termo, a página não será listada

    tags = soup.find_all(string=re.compile(termo))
    meta_tags = soup.find_all("meta", attrs={"content": re.compile(termo)})
    frequencia_termos = 0

    for tag in tags:
        count = 0
        count += len(
            re.findall(termo, tag.text)
        )  # Faz a contagem de ocorrências do termo no texto da tag
        frequencia_termos += count * 5

    for meta in meta_tags:
        frequencia_termos += 5

    if frequencia_termos == 0:
        print("A página não será listada pois não foi encontrado o termo.")
    else:
        print(f"Frequência de Termos: {frequencia_termos} pontos")

    return frequencia_termos


def uso_em_tags(soup, termo):
    # Uso das Tags (head, h1, h2, p, a) para relevância
    # Uso de termos buscados em title e meta tags (+20 pontos cada), h1 (+15
    # pontos cada ocorrência), h2 (+10 pontos cada), p (+5 pontos cada), a (+2pontos)

    title = soup.find("title", string=re.compile(termo))
    meta_tags = soup.find_all("meta", attrs={"content": re.compile(termo)})
    h1_tags = soup.find_all("h1", string=re.compile(termo))
    h2_tags = soup.find_all("h2", string=re.compile(termo))
    p_tags = soup.find_all("p", string=re.compile(termo))
    a_tags = soup.find_all("a", string=re.compile(termo))

    pontuacao_title = 0
    pontuacao_meta = 0
    pontuacao_h1 = 0
    pontuacao_h2 = 0
    pontuacao_p = 0
    pontuacao_a = 0

    if title:
        pontuacao_title += 20

    for meta in meta_tags:
        pontuacao_meta += 20

    for h1 in h1_tags:
        count = 0
        count += len(re.findall(termo, h1.text))
        pontuacao_h1 += count * 15

    for h2 in h2_tags:
        count = 0
        count += len(re.findall(termo, h2.text))
        pontuacao_h2 += count * 10

    for p in p_tags:
        count = 0
        count += len(re.findall(termo, p.text))
        pontuacao_p += count * 5

    for a in a_tags:
        count = 0
        count += len(re.findall(termo, a.text))
        pontuacao_a += count * 2

    pontuacao_uso_em_tags = (
        pontuacao_title
        + pontuacao_meta
        + pontuacao_h1
        + pontuacao_h2
        + pontuacao_p
        + pontuacao_a
    )

    print(
        f"Uso dos Termos: {pontuacao_title} (title) + {pontuacao_meta} (meta) + {pontuacao_h1} (h1) + {pontuacao_h2} (h2) + {pontuacao_p} (p) + {pontuacao_a} (a) = {pontuacao_uso_em_tags} pontos"
    )

    return pontuacao_uso_em_tags


def auto_referencia(soup, url):
    # Penalização por auto-referência
    # Cada autoreferência resulta em uma penalidade de -20 pontos.

    links = soup.find_all("a")
    pontuacao_auto_ref = 0
    url_cortada = ""

    busca_html = re.search(r"/([^/]+)$", url)
    # Corta a url a partir da última barra (/) para coletar o nome do documento html
    # / busca a barra | ([^/]+) busca os caracteres após a barra | $ sinaliza a busca no fim da string
    if busca_html:
        url_cortada = busca_html.group(1)

    for link in links:
        href = link.get("href")
        if href == url_cortada:
            pontuacao_auto_ref -= 20

    print(f"Auto-referência: {pontuacao_auto_ref} pontos")

    return pontuacao_auto_ref


def frescor(soup):
    # Frescor do Conteúdo: Avaliado pela data de publicação da página.
    # Páginas publicadas no ano corrente recebem +30 pontos, com uma redução de -5 pontos para cada ano anterior.

    ano_atual = datetime.now().year
    p_tags = soup.find_all("p")
    pontuacao_frescor = 0

    for p in p_tags:
        match = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", p.text)
        # Busca a data de publicação no parágrafo do documento html
        # \b são barreiras de palavra | \d{numero} contam os digitos consecutivos | / barra da data
        if match:
            data = match.group(1)
            dia, mes, ano = data.split("/")
            ano = int(ano)
            if ano == ano_atual:
                pontuacao_frescor = 30
                print(f"Frescor: {pontuacao_frescor} pontos")
            else:
                pontuacao_frescor = 30 - (5 * (ano_atual - ano))
                print(f"Frescor: {pontuacao_frescor} pontos")

    return pontuacao_frescor
