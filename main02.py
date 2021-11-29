import json
from bs4 import BeautifulSoup
from selenium import webdriver

def getInfo():
    url = "https://www.midsouthshooterssupply.com/dept/reloading/primers?itemsperpage=60&=c"

    driver = webdriver.Chrome("D:\\Dowloads\\chromedriver_win32\\chromedriver.exe")

    driver.get(url)
    sorc = driver.page_source
    soup = BeautifulSoup(sorc, 'lxml')

    products_list = list()
    products_dict = {}
    products_dict.clear()
    for info in soup.find_all('div', attrs={'class':'product'}):
        title = info.find('a', attrs={'class':'catalog-item-name'})
        #print(type(str(title.string)))
        title = str(title.string)

        brand = info.find('a', attrs={'class':'catalog-item-brand'})
        #print(type(str(brand.string)))
        brand = str(brand.string)
        
        price = info.find('span', attrs={'class':'price'})
        #print(price.text)
        prc = (price.text).replace("$","")
        prc = float(prc)
        #print(type(prc))
        #print(prc)
        
        status = info.find('span', attrs={'class':'status'})
        #print(type(status.text))
        sts = status.text
        if sts == 'Out of Stock':
            sts = False
        elif sts == 'In Stock':
            sts = True
        #print(type(sts))

        products_dict['Title'] = title
        products_dict['Manufacturer'] = brand
        products_dict['Price'] = f"${prc}"
        products_dict['Status'] = sts

        #print(products_dict)
        products_list.append(products_dict.copy())
    #print(products_list)
    return products_list

def saveFile():
    out = getInfo()
    with open('output.json', 'w') as f:
        print(f"writing...")
        json.dump(out, f)
    print(f"saved successfully.")

if __name__ == '__main__':
    #getInfo()
    saveFile()

    