#parse dataset from telegram archive 

import re
import pandas as pd

topics = ['economics', 'politics', 'sports', 'entertainment', 'technology']
files = {
    0 : ['business_ua', 'bankinvest', 'vistieconomiky'],
    1 : ['politikosmos', 'yzheleznyak', 'politikosmosnews'],
    2 : ['sportsuspilne', 'footballuaonline'],
    3 : ['Lutsk_zahody', 'kyiv_afisha', 'afisha_kyiva', 'davai_skhodymo'],
    4 : ['startup_ukr', 'onedaymedia_ua', 'ITCUA', ]
}
letters = list(pd.read_csv("letters.txt"))
letters.extend(' ')
ban_letters = ['ё', 'ы', 'э', 'ъ']

dataset_file = open('messages_dataset.csv', 'w', encoding='utf-8')
dataset_file = open('messages_dataset.csv', 'a', encoding='utf-8')
dataset_file.write('message,topic\n')
for topic in files.keys():
    for channel_name in files.get(topic):
        print(channel_name)
        data = pd.read_json('dumps/' + channel_name + ".json", encoding='utf-8')
        file = open('messages/' + channel_name + '.csv', 'w', encoding='utf-8')
        file.close()
        file = open('messages/' + channel_name + '.csv', 'a+', encoding='utf-8')
        file.write('message,topic\n')
        for i in data.messages:
            message_str = ''.join([x['text'] for x in i['text_entities']])
            clean_message = []
            for word in message_str.split(' '):
                if 'http' in word:
                    continue
                if len(word) > 30:
                    continue
                clean_message.append(word)
            message_str = ' '.join(clean_message).replace('"', '""')
            for rl in ban_letters:
                if rl in message_str:
                    message_str = ''    
            if len(message_str) > 200:
                dataset_file.write('"' + re.sub(' +', ' ', message_str).strip() + '",' + str(topic) + '\n')
                file.write('"' + re.sub(' +', ' ', message_str).strip() + '",' + str(topic))
                file.write('\n')


