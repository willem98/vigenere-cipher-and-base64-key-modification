import base64
import matplotlib.pyplot as plt
from decimal import *
import numpy as np
import os

Text = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/+"

"""Buat List angka"""
Num = []
for i in range(0,len(Text)): Num.append(i)

""" Buat Dictionary atau kamus dari karakter ke bilangan angka """
text_dec = dict(zip(Text, Num))
dec_text = dict(zip(Num, Text))

def decrypt_base64(teks):
    base64_text = teks+"==" #menambahkan teks == ke dalam teks base64 
    message = base64_text.encode('ascii')  # teks base64 diubah/di encode ke ascii code
    text = base64.b64decode(message) # teks base64 di dekripsi
    text1 = text.decode('ascii') # hasil dekripsi teks base64 di decode dari ascii code atau diubah lagi ke teks biasa
    return text1

def kunci_to_base64(kunci):
    return base64.b64encode(kunci.encode()).decode()

def toDec(text):
    result = []
    for i in range(0,len(text)):
        if text[i] != " ": result.append(text_dec[text[i]])
        else : result.append("")
    return result

#untuk mengubah bilangan angka ke text
def toText(textEnc):
    result = []
    for i in range(0,len(textEnc)):
        if textEnc[i] == "" : result.append(" ")
        else : result.append(dec_text[textEnc[i]])
    return result

#pengolahan kunci
def olahKunci(text,kunci):
    key = ""
    panjang = len(kunci)
    i = 0
    while(len(key) != len(text)):
        if(i >= panjang):
            i = 0
        key += dec_text[(kunci[i])]
        i += 1
        if(len(key)==len(text)):
            break
    kunci += toDec(kunci_to_base64(key).replace("=",""))
    return kunci

# Untuk meng enkripsi plaintext ke chipertext
def ciphertext(text, kunci, n):
    chipertext = []
    i = 0
    k = 0
    for j in range(len(text)):
        if text[i] != "" : 
            chipertext.append((text[i]+kunci[k])%n)
            i += 1
            k += 1
        else :
            i += 1
            chipertext.append("")
    return chipertext

# untuk dekripsi chipertext
def dekripter(chipertext, kunci, n):
    dekripter = []
    i = 0
    k = 0
    for j in range(len(chipertext)):
        if chipertext[i] != "" :
            dekripter.append((chipertext[i]-kunci[k])%n)
            i += 1
            k += 1
        else :
            i += 1
            dekripter.append("")
    return dekripter

# untuk menyambung huruf dari list huruf ke string teks
def sambungHuruf(text):
    result = ''.join(text)
    return result

#Proses enkripsi Vigenere Cipher
def encode(key, message):
    plaintext = toDec(message)
    kunci6 = kunci_to_base64(key).replace("==","")
    kunci64 = kunci6.translate({ord('='): None})
    kunci64_dec = toDec(kunci64)
    kunci_diolah = olahKunci(plaintext,kunci64_dec)
    cipher = ciphertext(plaintext, kunci_diolah, 64)
    chiperText = toText(cipher)
    return ''.join(chiperText)

#Proses deskripsi Vigenere Cipher   
def decode(key, enc):
    plaintext = toDec(enc)
    kunci6 = kunci_to_base64(key).replace("==","")
    kunci64 = kunci6.translate({ord('='): None})
    kunci64_dec = toDec(kunci64)
    kunci_diolah = olahKunci(plaintext,kunci64_dec)
    ciphertext2 = dekripter(plaintext, kunci_diolah, 64)
    ciphertext2_dec = toText(ciphertext2)
    return sambungHuruf(ciphertext2_dec)

#analisis frekuensi
def analisa(text):
    data = []
    for i in text:
        if i != " ":data.append(i)
    panjang = len(data)
    huruf = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '1','2','3','4','5','6','7','8','9','/','+']
    tabel1 = []
    for a in huruf:
        frekuensi = 0
        for b in data:
            if b == a : frekuensi += 1
        rate = (frekuensi / panjang)*100 
        tabel1.append({"huruf":a,"frekuensi":frekuensi,"persentase":str("%.2f"%(rate))+"%"})
    return {"data":tabel1,"len":panjang}

def plot(plain,cipher):
    huruf = ['A', 'B', "C", 'D', 'E', "F", 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','1','2','3','4','5','6','7','8','9','/','+']
    bad = []
    for i in huruf :
        for j in plain:
            if j['huruf'] == i:
                p = j['frekuensi']
        for k in cipher:
            if k['huruf'] == i:
                c = k['frekuensi']
        if (p+c) == 0 : bad.append(i)
    for i in bad:
        huruf.remove(i)
    pp = []
    pc = []
    for j in plain:
        if j['huruf'] in huruf:
            pp.append(Decimal(j['persentase'].replace('%','')))
    for j in cipher:
        if j['huruf'] in huruf:
            pc.append(Decimal(j['persentase'].replace('%','')))
    x = np.arange(len(huruf))
    fig, ax = plt.subplots()
    ax.plot(x, pp, color='r', label='Plain')
    ax.plot(x, pc, color='g', label='Cipher')
    ax.set_ylabel("PERSENTASE (%)")
    ax.set_title("Analisa Kemunculan Huruf")
    ax.set_xticks(x, huruf)
    ax.set_yticks([20,40,60,80,100])
    ax.legend()
    f = plt.gcf()
    f.set_size_inches((12,4),forward=False)
    f.tight_layout()
    name = [0]
    for i in os.walk(os.path.join(os.getcwd(),"static","plots")):
        for j in i[2]:
            name.append(int((j.replace("Chart","")).replace(".png","")))
    fn = f"Chart{str(max(name)+1)}.png"
    f.savefig(os.path.join(os.getcwd(),"static","plots",fn),dpi=650)
    return fn

def Save(res,type):
    name = [0]
    for i in os.walk(os.path.join(os.getcwd(),"static","txt")):
        for j in i[2]:
            name.append(int((j.replace("SavedTxt","")).replace(".txt","")))
    names = f"SavedTxt{str(max(name)+1)}.txt"
    with open(os.path.join(os.getcwd(),"static","txt",names),"+w") as txt:
        if type == 'des':txt.write("~~~~~ CipherText Result ~~~~~"+"\n"+res)
        else :txt.write("~~~~~ PlainText Result ~~~~~"+"\n"+res)
    return names
