def wordCloud(jobTitle, location):
    # %%
    # importing all necessary modules
    from wordcloud import WordCloud, STOPWORDS
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import os

    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    from collections import Counter
    import logging
    #nltk.download('punkt')
    #nltk.download('stopwords')

    # Configura il logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Starting Word Cloud..")

    # %%
    stopwords_tech = [
        'experience', 'skills', 'work', 'team', 'development', 'knowledge', 'ability', 'years', 'design',
        'software', 'working', 'technical', 'strong', 'degree', 'ability', 'responsibilities', 'required',
        'ability', 'technology', 'systems', 'understanding', 'programming', 'tools', 'environment', 'projects',
        'good', 'languages', 'education', 'requirements', 'engineer', 'excellent', 'communication', 'programming',
        'years', 'develop', 'implementation', 'process', 'web', 'platforms', 'technical', 'engineering', 'design',
        'code', 'development', 'implement', 'solutions', 'testing', 'designing', 'languages', 'technologies',
        'knowledge', 'strong', 'experience', 'team', 'working', 'project', 'responsibilities', 'role', 'software',
        'developing', 'design', 'implementation', 'experience', 'technical', 'engineering', 'coding', 'skills',
        'tools', 'platforms', 'ability', 'experience', 'engineering', 'requirements', 'solutions', 'testing',
        'communication', 'understanding', 'designing', 'knowledge', 'web', 'languages', 'technology', 'systems',
        'working', 'software', 'ability', 'tools', 'development', 'experience', 'years', 'responsibilities',
        'knowledge', 'strong', 'skills', 'technical', 'programming', 'ability', 'development', 'working', 'team',
        'languages', 'platforms', 'solutions', 'code', 'requirements', 'environment', 'experience', 'education',
        'engineer', 'design', 'software', 'developing', 'implementation', 'process', 'web', 'platforms', 'technical', 
        'job','description','customer', 'service',"'",
        'including','using', 'support',
        'whitin', 'hands' ,'services','sexual','orientation','wage'
        # Aggiungi altre parole chiave specifiche del tuo settore o di interesse
    ] + [jobTitle,location]

    stopwords_italian_tech = [
        'esperienza', 'abilità', 'lavoro', 'team', 'sviluppo', 'conoscenza', 'abilità', 'anni', 'design',
        'software', 'lavorando', 'tecnico', 'forte', 'laurea', 'abilità', 'responsabilità', 'richiesto',
        'tecnologia', 'sistemi', 'comprensione', 'programmazione', 'strumenti', 'ambiente', 'progetti',
        'buono', 'linguaggi', 'istruzione', 'requisiti', 'ingegnere', 'eccellente', 'comunicazione', 'programmazione',
        'anni', 'sviluppare', 'implementazione', 'processo', 'web', 'piattaforme', 'tecnico', 'ingegneria', 'design',
        'codice', 'sviluppo', 'implementare', 'soluzioni', 'test', 'progettazione', 'linguaggi', 'tecnologie',
        'conoscenza', 'forte', 'esperienza', 'team', 'lavorando', 'progetto', 'responsabilità', 'ruolo', 'software',
        'sviluppo', 'design', 'implementazione', 'esperienza', 'tecnico', 'ingegneria', 'codifica', 'abilità',
        'strumenti', 'piattaforme', 'esperienza', 'ingegneria', 'requisiti', 'soluzioni', 'test', 'comunicazione',
        'comprensione', 'progettazione', 'conoscenza', 'web', 'linguaggi', 'tecnologia', 'sistemi', 'lavorando',
        'software', 'abilità', 'strumenti', 'sviluppo', 'esperienza', 'anni', 'responsabilità',
        'conoscenza', 'forte', 'abilità', 'tecnico', 'programmazione', 'abilità', 'sviluppo', 'lavorando', 'team',
        'linguaggi', 'piattaforme', 'soluzioni', 'codice', 'requisiti', 'ambiente', 'esperienza', 'istruzione',
        'ingegnere', 'design', 'software', 'sviluppo', 'implementazione', 'processo', 'web', 'piattaforme', 'tecnico'
        # Aggiungi ulteriori parole chiave specifiche del tuo settore o di interesse
    ] + [jobTitle,location]

    # Aggiungi altre parole chiave specifiche del tuo settore o di interesse
    custom_stopwords_italian = [
        'parola_specifica1', 'parola_specifica2', 'parola_specifica3',
        # Aggiungi ulteriori parole chiave specifiche del tuo settore
    ] + [jobTitle,location]

    # Combinazione di stopwords di base e personalizzate
    all_stopwords_italian = stopwords_italian_tech + custom_stopwords_italian

    # Aggiungi altre parole chiave specifiche del tuo settore o di interesse
    custom_stopwords = [
        'specific_word1', 'specific_word2', 'specific_word3',
        # Aggiungi ulteriori parole chiave specifiche del tuo settore
    ] + [jobTitle,location]

    # Combinazione di stopwords di base e personalizzate
    all_stopwords = stopwords_tech + custom_stopwords + all_stopwords_italian


    # %%
    #Lettura file job_offer/sydney/nurse
    jobTitle =  '_'.join([ word.lower() for word in jobTitle.split(" ")])
    path=f'job_offer/{location}/{jobTitle}'
    total_doc=''
    for doc in  os.listdir(path):
        if doc[0]=='.':
            continue
        else:
            file=open(path+'/'+doc)
            lines = file.readlines()
            total_doc+=lines[0].lower().strip()


    def pulisci_testo(testo):
        wordList=[]
        # Rimuovi caratteri speciali, numeri e punteggiatura
        testo_pulito = re.sub(r'[^a-zA-Z\s]', ' ', testo)

        # Converti tutto in minuscolo
        testo_pulito = [i.lower() for i in testo_pulito.split(' ')]

        # Rimuovi spazi extra
        #testo_pulito = ' '.join(testo_pulito)

        for word in testo_pulito:
            word_clean = word.replace("'","")
            if word_clean not in all_stopwords:
                wordList.append(word_clean)

        return ' '.join(wordList)

    def estrai_keyword(testo):
        parole = word_tokenize(testo.lower())
        parole_filtrate = [parola for parola in parole if parola not in stopwords.words('english')]
        return ' '.join(parole_filtrate)

    total_doc = pulisci_testo(total_doc)
    total_doc = estrai_keyword(total_doc)
    

    # Carica le stop words
    stop_words = set(stopwords.words('english'))

    def filter_keywords(description):
        # Tokenizzazione del testo
        words = word_tokenize(description.lower())

        # Rimuovere le stop words e parole di lunghezza inferiore a 3 caratteri
        filtered_words = [word for word in words if word.isalpha() and word not in stop_words and len(word) > 3]

        return filtered_words

    # Esempio di utilizzo
    filtered_keywords = filter_keywords(total_doc)
    #print(filtered_keywords)

    # %%

    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = STOPWORDS,
                    min_font_size = 5).generate(str(filtered_keywords))
    
    # plot the WordCloud image                       
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig(f"static/Images/{location}_{jobTitle}.png") 
    #plt.show()

    return '200'

    # %%
#wordCloud("nurse", "sydney")
# %%
if __name__ =='__main__':
    wordCloud('nurse', 'sydney')
