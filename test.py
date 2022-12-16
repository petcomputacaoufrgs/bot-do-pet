from splinter import Browser
import time

url = "https://www.fnde.gov.br/consulta-publica/pagamento-bolsa-executado/#/app/consultar//"
cpf = '05410539060'

browser = Browser('chrome')
browser.visit(url)
browser.fill('filter', cpf)
browser.find_by_xpath('/html/body/div/section/div/div[2]/div/form/div/div/div/div/span[2]/button').click()
time.sleep(1)
browser.find_by_xpath('/html/body/div/section/div/div[3]/div[2]/div/table/tbody/tr/td[3]/a').click()
time.sleep(2)

data = browser.find_by_text('12/2022')

if(data.is_empty()):
    print('tamo pobre')
else:
    print('bolsa caiu')