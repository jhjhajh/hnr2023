import random

words = ["time","year","people","way","day","man","thing","woman","life","child","world","school","state","family","student","group","country","problem","hand","part","place","case","week","company","system","program","question","work","government","number","night","point","home","water","room","mother","area","money","story","fact","month","lot","right","study","book","eye","job","word","business","issue","side","kind","head","house","service","friend","father","power","hour","game","line","end","member","law","car","city","community","name","president","team","minute","idea","kid","body","information","back","parent","face","others","level","office","door","health","person","art","war","history","party","result","change","morning","reason","research","girl","guy","moment","air","teacher","force","education"]
index = random.randint(0,99)


    # # populate words array from config file
    # try:
    #     if os.path.isfile('data.txt'):
    #         with open('data.txt', 'r') as f:
    #             tempFile = f.read()
    #             tempFile = tempFile.splitlines()
    #             x = 0
    #             while x < len(tempFile):
    #                 config.words += [tempFile[x]]
    #                 x+=1
    #     for word in config.words:
    #         print(word)
    # except Exception as e:
    #     first_name = update_obj.message.from_user['first_name']
    #     print("unable to read file. check the format of data file")
    #     print (e.msg)
    #     update_obj.message.reply_text(f"Unable to load bot. See you {first_name}!, bye")
