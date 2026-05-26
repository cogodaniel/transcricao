# Call Transcrition Using Google STT




## Criar a chave de licença no Google Cloud Platform
Criar licenças no google cloud para poder utilizar o serviço de STT. 

```
Passo 1
Passo 2
Passo 3
Passo 4
Passo 5
Passo 6
Passo 7
Passo 8
Passo 9
Passo 10
Passo 11
Passo 12
Passo 13
```

## Salvar a chave de licença na pasta

Salvar as credenciais criadas dentro da pasta /opt/google.

```
mkdir /opt/google

export GOOGLE_APPLICATION_CREDENTIALS="/opt/google/credencial.json"

echo 'GOOGLE_APPLICATION_CREDENTIALS="/opt/google/credencial.json"' >> /etc/environment
```

## Instalar o Google Cloud Platform no Debian

Instalar bibliotecas no Debian. 

```
pip3 install google-cloud-speech pyst2 --break-system-packages
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


