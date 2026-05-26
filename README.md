# Call Transcrition Using Google STT




## Criar a chave de licença no Google Cloud Platform
Criar licenças no google cloud para poder utilizar o serviço de STT. 

```
Passo 1 - Acessar o consiole do Google Cloud - https://console.cloud.google.com
Passo 2 - Clicar em Selecionar Projeto > Novo Projeto
Passo 3 - Definir um nome (asterisk-transcricao)
Passo 4 - Clicar em Criar
Passo 5 - Ativar Faturamento no Menu Faturamento (somente para habilitar, não será cobrado)

Passo 6 - Abrir a opção Speech-to-Text API 
Passo 7 - Clicar em Ativar

Passo 8 - Clicar em IAM e Administração > Contas de Serviços
Passo 9 - Clicar em Criar Conta de Serviço
Passo 10 - Preencher os Dados Nome: asterisk-stt e ID: asterisk-stt
Passo 11 - Clicar em Criar e Continuar

Passo 12 - Em permissões Adicione Cloud Speech Client
Passo 13 - Clique em Contionuar

Passo 14 - Clique em Chaves > Adicionar chave > Criar nova chave  
Passo 15 - Escolha JSON
Passo 16 - CLique em Criar
Passo 17 - Será feito o downlaod de da chave de licença com extensão json
```

## Salvar a chave de licença na pasta

Salvar as credenciais criadas dentro da pasta /opt/google.

```
mkdir /opt/google

export GOOGLE_APPLICATION_CREDENTIALS="/opt/google/credencial.json"

echo 'GOOGLE_APPLICATION_CREDENTIALS="/opt/google/credencial.json"' >> /etc/environment

systemctl restart asterisk
```

## Testar a chave

Caso queira fazer o teste da chave de licença

```
EXECUTE: python3

EM SEGUIDA:
from google.cloud import speech

client = speech.SpeechClient()

print("OK")

```

Caso a resposta seja OK, a chave de licença esta correta


## Instalar o Google Cloud Platform no Debian

Instalar bibliotecas no Debian. 

```
pip3 install google-cloud-speech pyst2 --break-system-packages
```

## Baixar e salvar o arquivo de Transcrição

Baixe, salve e dê permissão no arquivo de transcrição

```
git https://github.com/cogodaniel/transcricao

cp transcreve.py /var/lib/asterisk/agi-bin/

chmod +x /var/lib/asterisk/agi-bin/transcreve.py
chown asterisk:asterisk /var/lib/asterisk/agi-bin/transcreve.py
```

## Passo : Criar conexto

Neste contexto, primeramente é criado o parametro para a criação do nome do arquivo, que contem a data e hora e o nome dos ramais que irão participar da gravação. 
Em seguida é feita a gravação da chjamada com MixMonitor(), quando a chamada é encerrada (h), a gravação é encerrada com SyopMixMonitor(), e em seguida o System() chama o sript que vai fazer a transcrição da chamada e slava na mesma pasta da gravação com o memso noe, porem a extensão é txt. 

```
[interno]
exten => _X.,1,NoOp(Chamada para ${EXTEN})
exten => _X.,n,Set(DATA=${STRFTIME(${EPOCH},,%Y%m%d-%H%M%S)})
exten => _X.,n,Set(__FILE_NAME=${DATA}-${CALLERID(num)}-${EXTEN})
exten => _X.,n,MixMonitor(${FILE_NAME}.wav,bi(MXMON_ID))
exten => _X.,n,NoOp(ID DA GRAVACAO = ${MXMON_ID})
exten => _X.,n,Dial(PJSIP/${EXTEN},30)
exten => _X.,n,Hangup()

exten => h,1,NoOp(INICIANDO TRANSCRICAO DE CHAMADA)
exten => h,n,NoOp(TRANSCREVENDO O ARQUIVO ${FILE_NAME}.wav)
exten => h,n,StopMixMonitor(${MXMON_ID})
exten => h,n,System(/usr/bin/python3 /var/lib/asterisk/agi-bin/transcricao.py /var/spool/asterisk/monitor/${FILE_NAME}.wav > /tmp/erro_transcricao.log 2>&1 &)
```

## Passo : Configrar os ramais PJSIP

Segue dois exemplode ramais a serem criados no arquivo /etc/astrisk/pjsip.conf


```
; =========================
; TRANSPORT UDP
; =========================

[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0

; =========================
; RAMAL 8002
; =========================

[8002]
type=endpoint
context=interno
transport=transport-udp
disallow=all
allow=ulaw,alaw
auth=8002
aors=8002
callerid=Ramal 8002 <8002>

[8002]
type=auth
auth_type=userpass
username=8002
password=Senha8002

[8002]
type=aor
max_contacts=1

; =========================
; RAMAL 8003
; =========================

[8003]
type=endpoint
context=interno
transport=transport-udp
disallow=all
allow=ulaw,alaw
auth=8003
aors=8003
callerid=Ramal 8003 <8003>

[8003]
type=auth
auth_type=userpass
username=8003
password=Senha8003

[8003]
type=aor
max_contacts=1
```


