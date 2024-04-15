def scrapingLinkedin(jobTitle,location):
    # %%
    # PSW AND USER DEFINITION
    #jobTitle = 'Data engineer'
    #location = 'Sydney'


    # %%
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys

    import time
    import os
    import logging
    import requests
    import re
    # %%
    jobTitleURL="%20".join(jobTitle.split(" "))
    locationURL="%20".join(location.split(" "))
    url=f'https://www.linkedin.com/jobs/search/?keywords={jobTitleURL}&location={locationURL}&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'

    # Configura il logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Starting app..")
    # %%
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("enable-automation")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    options.add_argument("enable-features=NetworkServiceInProcess")


    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()),options=options)
    driver.get(url)
    actions = ActionChains(driver)
    logging.info('Waititng for the page to open...')
    time.sleep(5)
    #Scorro fra le pagine
    for j in range(5):
        for  i in range(5):
            y = 4000*i*j
            driver.execute_script(f"window.scrollTo(0, {y})")
            time.sleep(1)
        #clicca il bottone vedi più offerte
        try:
            logging.info('Clicco bottone')
            moreOfferButton= driver.find_element("xpath",'//*[@id="main-content"]/section[2]/button')
            moreOfferButton.click()
        except:
            continue


    # %%
    html = driver.page_source  #prendo html della pagina con tutte le offerte
    regex="https:\/\/[a-zA-Z]+.linkedin.com\/.+"
    id_job_list=re.findall(regex,html)
    #puliamo la lista
    id_list=[]
    for l in id_job_list:
        final_id=re.search('https:.+"',l)
        id_list.append(final_id.group().split(" ")[0])
    #logging.info('ID lIST: ',id_list)
    # %%
    # Devo ottenere la descrizione del lavoro (le prime 2 sono da balzare)
    jobTitle=jobTitle.replace(" ","_")
    dest_path_location =f"job_offer/{location}/"
    if not os.path.exists(dest_path_location):
        os.makedirs(dest_path_location) # creo la cartella con la location
    dest_path_job = f'{dest_path_location}/{jobTitle}'
    logging.info('dest_path_location')
    if not os.path.exists(dest_path_job):
        logging.info('New job and location')
        os.makedirs(dest_path_job) 
        offer_count=0
        for i,id in enumerate(id_list):
            logging.info(offer_count)
            logging.info(id)
            r=requests.get(id)
            try:
                jobDescription=re.search('<div class="core-section-container__content break-words">.*<button class="show-more-less-html',r.text.replace('\n',''))
                cleaned_text = re.sub('<[^>]*>', '', jobDescription.group())
                cleaned_text = re.sub('<button class="show-more-less-html', '', cleaned_text)
                cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)
                with open(os.path.join(dest_path_job, f'{i}.txt'),'w' )  as f:   
                    f.write(cleaned_text)
                    f.close()
                offer_count+=1
            except Exception as e:
                logging.info(f'Error on link: {id}')
            if offer_count >10:
                break
            time.sleep(2)
        logging.info("All Job id has been searched")
    else:
        logging.info("Research already done for this location and job")

    driver.quit()
# %%
if __name__ == "__main__":
    scrapingLinkedin('Data Engineer','Sydney')