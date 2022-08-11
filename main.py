# coding=utf8
#TODO:1 - abrir a página de busca com os termos e datas desejados
#exemplos de termos:
#Turquia e imigrantes
#Turquia e refugiados
#TODO:2 - varrer a página de busca mostrando todos os links
#TODO:3 - chegar até o fim das páginas de busca (botão carregar mais ou pŕoxima página)
#TODO:4 - abrir cada link do item 2
#TODO:4.1 - conseguir pegar a periodo da matéria
#TODO:4.2 - conseguir pegar o texto da matéria
#TODO:4.3 - salvar a matéria em um arquivo com nome periodo+link (link sem caracteres especiais)
#exemplo 2020-02-29-https___oglobo.globo.com_mundo_erdogan-pede-putin-que-se-afaste-da-guerra-na-siria-1-24279490
import os
import shutil

from LaNacionCrawler import LaNacionCrawler

termos_da_pesquisa = ["Conflicto israelí-palestino",
                      "Enfrentamientos israelíes y palestinos",
                      "Enfrentamientos árabes y judíos",
                      "Jerusalém",
                      "Faixa de Gaza",
                      "Ramadán",
                      "Palestina ataques",
                      "Israel ataques",
                      "Hamas"]
periodo = {
    'inicio' : '05/04/2021',
    'fim' : '30/05/2021'
}

for termo in termos_da_pesquisa:
    crawler = LaNacionCrawler(termo, periodo)

    os.makedirs("./{}".format(termo))
    crawler.iniciar_pesquisa()
    try:
        crawler.capturar_noticias()
        crawler.raspar_noticia()
        crawler.contador_ocorrencias()
    except:
        pass

