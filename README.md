
---

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
exten => h,n,System(/usr/bin/python3 /var/lib/asterisk/agi-bin/transcricao.py />


---

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

---
