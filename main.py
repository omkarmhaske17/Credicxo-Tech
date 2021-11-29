from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import json

options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

def getIpPort():
    # url = "https://www.freeproxylists.net/?c=US&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0"  # This url is for US only proxies, but they are not working with this website.
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'D:\\Dowloads\\chromedriver_win32\\chromedriver.exe')
    driver.get("https://www.freeproxylists.net/?c=&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0")
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    ip_port_list = list()
    for rows in soup.find_all('tr', attrs={'class':'Odd'}):
            try:
                ip = rows.find('a')
                # print(proxy.string)
                port = rows.find_all('td')
                p = port[1]
                if ip != None:
                    ip_port_list.append(f"{ip.string}:{p.text}")
            except:
                continue

    for rows in soup.find_all('tr', attrs={'class':'Even'}):
        try:
            ip = rows.find('a')
            # print(a.string)
            port = rows.find_all('td')
            p =port[1]
            if ip != None:
                ip_port_list.append(f"{ip.string}:{p.text}")
        except:
            continue

    # print(ip_port_list)
    # print(len(ip_port_list))
    driver.close()
    return ip_port_list

def getProductInfo():

    proxy = getIpPort()
    for i in range(0,len(proxy)):
        try:
            print("Proxy selected: {} |{}/{}".format(proxy[i]),i,len(proxy))
            options = webdriver.ChromeOptions()
            options.add_argument('--proxy-server={}'.format(proxy[i]))

            driver = webdriver.Chrome(options=options, executable_path=r'D:\\Dowloads\\chromedriver_win32\\chromedriver.exe')
            driver.get("https://www.midsouthshooterssupply.com/dept/reloading/primers?itemsperpage=60&=c")
            driver.set_page_load_timeout(5)
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
            
        except Exception:
                print('ERROR!!!')
                driver.quit()
        #print("Proxy Invoked!")
        
    return products_list

def saveFile():
    out = getProductInfo()
    with open('output.json', 'w') as f:
        print(f"writing...")
        json.dump(out, f)
    print(f"saved successfully.")

if __name__ == '__main__':
    saveFile()
        