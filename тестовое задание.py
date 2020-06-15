import string
import re
import pandas as pd
def function(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        content = file.read()
    lst=content.split('\n')
    #вытаскиваем хэштеги из строк
    heshtegs={}
    for i in lst:
        a=re.findall(r'[ ][#][^ ]*', i)
        for heshteg in a:
            if heshteg[1:] in heshtegs:
                heshtegs[heshteg[1:]]+=1
            else:
                heshtegs[heshteg[1:]]=1
        heshteg=re.match(r'[#][^ ]*', i)
        if heshteg!=None:
            if heshteg[0] in heshtegs:
                heshtegs[heshteg[0]]+=1
            else:
                heshtegs[heshteg[0]]=1
    #преобразуем словарь в датафрейм вначале сортируем по алфавиту потом по частоте встречаемости.
    #столбец 0 это название столбца с количеством хеэштегов
    df=pd.DataFrame( pd.Series(heshtegs))
    df['name_heshteg']=list(df.index)
    df=df.sort_values('name_heshteg', ascending=True)
    df=df.sort_values(0, ascending=False)
    heshtegs=list(df.head(10)['name_heshteg'])
    #соединяем все тексты в один, с одинаковыми хэштегами
    words={}
    for i in heshtegs:
        words[i]=''
    for i in range(len(lst)):
        for j in heshtegs:
            if lst[i].find(j)!=-1:
                words[j]+=' '+' '.join(w for w in lst[i].split(' ') if not w.startswith('#'))
    #делаем фильтрацию по заданным условиям и считаем количество слов
    result={}
    for name_heshteg in words.keys():
        significant_words={}
        words[name_heshteg]=(re.sub(r'[!"$%&\'()*,./:;<=>?@\\^_`{|}~]', "", words[name_heshteg])).lower()#убираем знаки препинанания чтобы например слово "кот" и "кот," не были разными
        a=re.findall(r'[\s][A-Zа-яa-zА-Я][^\s]*',words[name_heshteg])#фильтруем чтобы слово начиналось с буквы
        b=[]
        for i in a:
            if len(re.findall(r'[1234567890]', i))==0:#убираем слова внутри которых есть цифры
                b.append(i[1:])
        for significant_word in b:
            if significant_word in significant_words:
                significant_words[significant_word]+=1
            else:
                significant_words[significant_word]=1
    #   преобразуем словарь в датафрейм вначале сортируем по алфавиту потом по частоте встречаемости.
    #   столбец 0 это название столбца с количеством хэштегов
        df=pd.DataFrame( pd.Series(significant_words))
        df['word']=list(df.index)
        df=df.sort_values('word', ascending=True)
        df=df.sort_values(0, ascending=False)
        significant_words=list(df.head(5)['word'])
        result[name_heshteg]=significant_words
    return heshtegs, result
print(function("in.txt"))