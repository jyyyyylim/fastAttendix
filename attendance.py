import requests
import json
from datetime import datetime

#>> INITIALIZING SESSION
s=requests.Session()
ContentType='application/x-www-form-urlencoded'

#>> initializing loop flags
authStatus,resubmitLoop,code,validFlag='nul',1,'',0

#>> init logfile if not present, lazy code reuse
requirements=['hist.log']
for files in requirements:
    try:
        name=open(files,'r')
        pass
        name.close()
    except IOError:
        with open(files,'x') as name:
            pass

#>> CREDENTIALS POST SENT. TGT CREATED ON N201. CRED ENCODING DISREGARDED
try:
    credCheck=open('./settings.json','r')
    pass
    credCheck.close()
except IOError: 
    if authStatus=='nul': print('settings.json not found. Defaulting to manual entry\n')
    while authStatus!=int(201):
        usr=str(input('Enter your TP. no...   '))
        pwd=str(input('Enter your password...   '))
        HTTPPost=s.post('https://cas.apiit.edu.my/cas/v1/tickets',data={"username": usr, "password": pwd})
        authStatus=HTTPPost.status_code
        if authStatus!=201: print('\n\nSomething went wrong. Try again.'+'\n<'+'RESPONSE-'+ str(HTTPPost.status_code)+'>'  )
        else: print('\nSuccess!')
    credentials={"secrets":{"usr": usr,"pwd": pwd}}
    with open('settings.json','w') as optFile:
        optFile.write(json.dumps(credentials))
    print('Credentials saved.')
else:
    with open('settings.json','r') as optFile:
        usr=json.load(optFile)['secrets']['usr']
    with open('settings.json','r') as optFile:
        pwd=json.load(optFile)['secrets']['pwd']
    # apparently the fileObject closes itself after every read lmfao
    
    HTTPPost=s.post('https://cas.apiit.edu.my/cas/v1/tickets',data={'username': usr, 'password': pwd})
    print('Previous session detected, reusing saved credentials.')

#>> CREDENTIALS APPROVED, TGT CREATED 
#>> ADVANCING THROUGH DOUBLE AUTH HANDSHAKE
logonTicket=json.loads(str(HTTPPost.headers).replace("'", '"'))["Location"]
initHandshake=s.post(logonTicket,headers= {"content-type": ContentType},params= {'service': 'https://cas.apiit.edu.my'})
authTicket=s.get('https://cas.apiit.edu.my/cas/p3/serviceValidate',params={'format': 'json', 'service': 'https://cas.apiit.edu.my', 'ticket': initHandshake.text})
print('Logged in as: '+str(json.loads(authTicket.text)['serviceResponse']['authenticationSuccess']['attributes']['givenName']).replace("'",'')+'\n\n')

#>> logon successful, build HTTP request with graphQL P/L.
endpoint='https://attendix.apu.edu.my/graphql'
graphqlContent='application/json'

ins, o= str('hm>!hz9n}exi|nh>|ana{x;giugjk8'), 12
ek= "".join(chr(o^ord(n)) for n in ins)
accessCtlReqHeaders='content-type,ticket,x-amz-user-agent,x-api-key'
accessCtlReqMethod='POST'
CtlReq=s.options(endpoint,headers={"host": 'attendix.apu.edu.my',"path": '/graphql' , "sec-fetch-dest": 'empty', "sec-fetch-mode": 'cors', "sec-fetch-site": 'same-site', "access-control-request-headers": accessCtlReqHeaders, "access-control-request-method": accessCtlReqMethod})
agent='aws-amplify/1.0.1'

## catch invalid attendance code, saving invalid http calls. breaks on valid hit
while resubmitLoop==1:
    while validFlag!=1:
        try:
            code=str(input('Enter the 3-digit passcode. '))
            if len(str(code))!=3:
                raise lenError("Input chars >3")
            break
        except:
            print('Invalid response!\n')

    # the fuck is this? at least it works only after this POST
    attendix=s.post(logonTicket,headers={"content-type": ContentType},params={'service': 'https://api.apiit.edu.my/attendix'}).text
    payload={"operationName":"updateAttendance","variables":{"otp":code},"query": "mutation updateAttendance($otp: String!) {\n  updateAttendance(otp: $otp) {\n    id\n    attendance\n    classcode\n    date\n    startTime\n    endTime\n    classType\n    __typename\n  }\n}\n"}
    attendUpdate=s.post(endpoint,headers={"host": 'attendix.apu.edu.my', "path": '/graphql', "content-type": graphqlContent, "sec-fetch-dest": 'empty', "sec-fetch-mode": 'cors', "sec-fetch-site": 'same-site', "ticket": attendix, "x-amz-user-agent": agent, "x-api-key": ek},json=payload)
    try:
        feedbackMessage=((json.loads(str(attendUpdate.text))['errors'])[0])
        print(feedbackMessage['message']+'\n')
    except:
        classtyp=str(json.loads(attendUpdate.text)['data']['updateAttendance']['classType'])
        feedbackMessage="Success: Logged attendance for "+classtyp+': '+json.loads(str(attendUpdate.text))['data']['updateAttendance']['classcode']
        with open('hist.log','a') as log:
            log.write(str(datetime.now())+'\n'+feedbackMessage+'\n\n')
        print(feedbackMessage)
        exit()
