from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import re

def process_links(links):
    driver = webdriver.Chrome()  # Replace with the appropriate driver for your browser.
    emailurlslist=[]
    for link in links:
        driver.get(link)
        button_urls = []
        

        buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[@class='btn btn-primary btn-sm' and not(@id='connexion')]"))
            )

        for button in buttons:
                
                    # Extract the URL from the onclick attribute using execute_script
                    onclick_attr = button.get_attribute("onclick")
                    if onclick_attr:
                        start_index = onclick_attr.index("'/parrain_definit.php?id_par=") + len("'/")
                        end_index = onclick_attr.index("', '")
                        url_to_click = onclick_attr[start_index:end_index]
                        button_urls.append(url_to_click)

                        complete_url = 'https://www.1parrainage.com/' + url_to_click
                        emailurlslist.append(complete_url)

    listofpersons=[]                 
    #got the links of button   
    print(emailurlslist)
    data_list=[]
    for url in emailurlslist:
         response = requests.get(url)
         html_content = response.text
         soup = BeautifulSoup(html_content, 'html.parser')
         iframe = soup.find('iframe', {'id': 'offreDetail'})
         iframe_url = iframe['src']
         complete_iframe_url= complete_url = 'https://www.1parrainage.com' + iframe_url
         offerresponse=requests.get(complete_iframe_url)
         html_content_of_iframe = offerresponse.text
         soup2 = BeautifulSoup(html_content_of_iframe, 'html.parser')
         Soupstring=soup2.get_text()
         annonce='Annonce de Parrainage de'
         
         name=None
         email=None

         email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

         if annonce in Soupstring:
              index = Soupstring.find("Annonce de Parrainage de")
              if index != -1 and len(Soupstring) > index + len("Annonce de Parrainage de") + 10:
                   result = Soupstring[index + len("Annonce de Parrainage de"): index + len("Annonce de Parrainage de") + 15]
                   name=result

         email = re.findall(email_pattern, Soupstring)

         data_list.append({
            'Name': name,
            'Email': email[0] if email else None,
            'URL': complete_iframe_url
         })
         with open('output2.csv', mode='w', newline='') as csv_file:
            fieldnames = ['Name', 'Email', 'URL']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header row with column names
            writer.writeheader()

        # Write the data to the CSV file
            writer.writerows(data_list)
        

cleanedlinks=[]
filepath='2.csv'
with open(filepath,'r')as csv_file:


    s=[]
    csv_reader=csv.DictReader(csv_file)
    for row in csv_reader:
        s.append(row)
    all_values = [list(d.values()) for d in s]
    for i in all_values:
        for s in i:
             cleanedlinks.append(s)
    


process_links(cleanedlinks)