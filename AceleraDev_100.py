#!/usr/bin/env python
# coding: utf-8


###IMPORT DAS BIBLIOTECAS QUE SERÃO USADAS

import requests
import json
import hashlib

###REQUISIÇÃO HTTP

response = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=a4299254b61dec7ac5bf17b4c7f0fba487b5624e')

###VERIFICAÇÃO DO QUE TEM DENTRO DA REQUISIÇÃO

response.content

###SALVANDO O ARQUIVO OBTIDO

a = response.json()

with open('resp_text.json', 'w') as jsonFile:
    json.dump(a, jsonFile)

###CARREGAMENTO DO ARQUIVO

with open('resp_text.json', 'r') as jsonFile:
    answer = json.load(jsonFile)

###CÓDIGO PARA OBTER O TEXTO DECIFRADO

class Caesar:
    def __init__(self):
        self.__letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  
    def decrypt(self, texto_cifrado,  key = a['numero_casas']):
        ''' (Caesar, str, int) -> str
 
        Retorna em texto plano o texto decifrado com a cifra de Cesar, utilizando a chave
        '''
        plain_text = ''
        texto_cifrado = texto_cifrado.upper()
        for ch in texto_cifrado:
            if ch in self.__letters:
                idx = self.__letters.find(ch) - key
                plain_text += self.__letters[idx]
            else:
                idx = ch
                plain_text += idx    
        return plain_text.lower()

###OBTENÇÃO DO TEXTO DECIFRADO

decrypt = Caesar().decrypt(a['cifrado'])
print(decrypt)

###ATUALIZAÇÃO DO JSON

answer['decifrado'] = decrypt

###CONFERINDO A ATUALIZAÇÃO

answer

###CÓDIGO PARA OBTENÇÃO DO RESUMO ATRAVÉS DO SHA1

hash_object = hashlib.sha1(b'plan to throw one (implementation) away; you will, anyhow. fred brooks')

###OBTENÇÃO DO RESUMO

resumo = hash_object.hexdigest()
print(hash_object.hexdigest())

###ATUALIZAÇÃO DO JSON

answer['resumo_criptografico'] = resumo

###CONFERINDO A ATUALIZAÇÃO

answer

###SALVANDO O CONTEÚDO FINAL EM UM JSON

with open('answer.json', 'w') as jsonFile:
    json.dump(answer, jsonFile)

###URL DA API PARA A SUBMISSÃO DO ARQUIVO ATUALIZADO

url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token='+answer['token']


###SETANDO OS PARAMETROS EM FILES

files = {
    'answer': ('answer', open('answer.json','rb'), 'application/json'), 
    'Content-Type':'multipart/form-data; boundary=--------------------------665956835435877517162732'
}

###OBS: BOUNDARY OBTIDO ATRAVÉS DO PROGRAMA POSTMAN

###SUBMETENDO O ARQUIVO ATUALIZADO VIA POST PARA A API

r = requests.post(url, files=files)

###RESULTADO DA SUBMISSÃO

if r.status_code == 200:
    print('Parabéns! A requisição foi um sucesso :)')
    if r.text[-5:-2] == '100':
        print('O seu score foi: '+r.text[9:12]+'%')
    else:
        print('O seu score foi: '+r.text[9:11]+'%')
elif r.status_code == 429:
    print('Espere um pouco antes de enviar uma nova tentativa!') 
else:
    print('Cuidado! Existe algum erro no código enviado :(') 

