from bs4 import BeautifulSoup
import lxml

file_name = "systecnet_catxml_de-de_to_en-GB_280121-113333.xml"
infile = open(file_name,"r", encoding='utf8')



contents = infile.read()
soup = BeautifulSoup(contents,'xml')
datas = soup.find_all('data')
for data in datas:
    if isinstance(data, BeautifulSoup.CData):
        print(data.type)



