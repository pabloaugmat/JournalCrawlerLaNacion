import shutil

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LaNacionCrawler:

    def __init__(self, termo, periodo):
        self.termos_da_pesquisa = termo
        self.periodo = periodo
        self.driver = None
        self.lista_de_links: list = []
        self.contador_termo = 0

    def iniciar_pesquisa(self):
        url = ("https://www.lanacion.com.ar/buscador/?query={}".format(self.termos_da_pesquisa))

        profile = webdriver.FirefoxProfile()
        profile.set_preference("javascript.enabled", True)
        self.driver = webdriver.Firefox(profile)
        self.driver.get(url)

        campo_data_inicio = self.driver.find_element(By.ID, 'datepicker_from')
        campo_data_inicio.send_keys(self.periodo["inicio"])

        campo_data_fim = self.driver.find_element(By.ID, "datepicker_to")
        campo_data_fim.send_keys(self.periodo["fim"])

        botao_aplicar_data = self.driver.find_element(By.ID, 'pubDate_filter')
        botao_aplicar_data = botao_aplicar_data.find_element(By.TAG_NAME, 'button')
        botao_aplicar_data.click()

    def capturar_noticias(self):

        carregar_noticias = WebDriverWait(self.driver, 10). \
            until(EC.presence_of_element_located((By.CLASS_NAME, 'queryly_item_row')))

        noticias = self.driver.find_elements(By.CLASS_NAME, 'queryly_item_row')

        for noticia in noticias:
            print(noticia.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            self.lista_de_links.append(noticia.find_element(By.TAG_NAME, 'a').get_attribute('href'))

        try:
            botao_seguinte = self.driver.find_element(By.CLASS_NAME, 'next_btn')
            botao_seguinte.click()
            self.capturar_noticias()
        except:
            self.driver.quit()

    def raspar_noticia(self):

        profile = webdriver.FirefoxProfile()
        profile.set_preference("javascript.enabled", False)
        self.driver = webdriver.Firefox(profile)

        for link in self.lista_de_links:
            self.driver.get(link)
            self.criar_arquivo(link)

        self.driver.close()

    def criar_arquivo(self, link):

        import re

        link_sem_caracteres_especiais = re.sub('[^0-9a-zA-Z]+', '_', link)
        print(link_sem_caracteres_especiais)

        data = WebDriverWait(self.driver, 10). \
            until(EC.presence_of_element_located((By.CLASS_NAME, 'mod-date')))
        data = data.find_element(By.CLASS_NAME, 'com-date')
        data = data.get_attribute('textContent')
        data = self.formatar_data(data)

        # exemplo 2020-02-29-https___oglobo.globo.com_mundo_erdogan-
        # pede-putin-que-se-afaste-da-guerra-na-siria-1-24279490

        titulo = "{}-{}".format(data, link_sem_caracteres_especiais)

        paragrafos = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'p'))
        )

        paragrafos = self.driver.find_elements(By.TAG_NAME, 'p')

        texto = ''

        for paragrafo in paragrafos:
            print(paragrafo.get_attribute('textContent'), "\n")
            texto = texto + "{}\n".format(paragrafo.get_attribute('textContent'))

        try:
            arquivo = open('{}.txt'.format(titulo), 'w+', encoding="utf-8")
            arquivo.write(texto)
            arquivo.close
            shutil.move('{}.txt'.format(titulo), "./{}".format(self.termos_da_pesquisa))
            self.contador_termo += texto.count(self.termos_da_pesquisa)
        except:
            pass

    def formatar_data(self, data):

        # data = '10 de agosto de 2022'

        meses = {
            'ener': '01',
            'febr': '02',
            'marz': '03',
            'abri': '04',
            'mayo': '05',
            'juni': '06',
            'juli': '07',
            'agos': '08',
            'sept': '09',
            'octu': '10',
            'novi': '11',
            'dici': '12'
        }

        ano = data[-4:]
        dia = data[0:2]

        if int(dia) < 10:
            mes_palavra = data[5:9]
        else:
            mes_palavra = data[6:10]

        print(mes_palavra)
        mes_numero = 0
        for mes in meses:
            if mes_palavra == mes:
                mes_numero = meses[mes]

        data = '{}-{}-{}'.format(ano, mes_numero, dia)

        return data

    def contador_ocorrencias(self):

        arquivo = open('contador_ocorrencias_termo.txt', 'w+', encoding="utf-8")
        arquivo.write(str(self.contador_termo))
        arquivo.close
        shutil.move("contador_ocorrencias_termo.txt", "./{}".format(self.termos_da_pesquisa))
