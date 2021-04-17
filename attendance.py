import requests
import json

s=requests.Session()
spoofAgent='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36'
ContentType='application/x-www-form-urlencoded'

## USER/PWD WHILE LOOP. ##
#>> AUTH HANDSHAKE PARTITION 
#1> CREDENTIALS POST SENT. TGT CREATED ON N201. CRED ENCODING DISREGARDED

authStatus='nul'
while authStatus!=int(201):
    usr=str(input('Enter your TP. no...   '))
    pwd=str(input('Enter your password...   '))
    HTTPPost=s.post('https://cas.apiit.edu.my/cas/v1/tickets',data={'username': usr, 'password': pwd})
    authStatus=HTTPPost.status_code
    if authStatus!=201: print('\n\nSomething went wrong. Try again.'+'\n<'+'RESPONSE-'+ str(HTTPPost.status_code)+'>'  )
    else: print('\nSuccess!')

#settingsJsonIOStream=open('settings.json','rt')



############# CREDENTIALS APPROVED, TGT LINK CREATED ##########################
logonTicket=json.loads(str(HTTPPost.headers).replace("'", '"'))['Location']
#print('logonTicket:'+ logonTicket)
###############################################################################

initHandshake=s.post(logonTicket,headers= {"content-type": ContentType},params= {'service': 'https://cas.apiit.edu.my'})
#print('initHandshake:'+ initHandshake)
authTicket=s.get('https://cas.apiit.edu.my/cas/p3/serviceValidate',params={'format': 'json', 'service': 'https://cas.apiit.edu.my', 'ticket': initHandshake.text})
print('Logged in as: '+str(json.loads(authTicket.text)['serviceResponse']['authenticationSuccess']['attributes']['givenName']).replace("'",'')+'\n\n')

##logon successful, build HTTP request with graphQL P/L. ##
endpoint='https://attendix.apu.edu.my/graphql'
graphqlContent='application/json'

accessCtlReqHeaders='content-type,ticket,x-amz-user-agent,x-api-key'
accessCtlReqMethod='POST'
CtlReq=s.options(endpoint,headers={"host": 'attendix.apu.edu.my',"path": '/graphql' , "sec-fetch-dest": 'empty', "sec-fetch-mode": 'cors', "sec-fetch-site": 'same-site', "access-control-request-headers": accessCtlReqHeaders, "access-control-request-method": accessCtlReqMethod})
#print(finCtl.headers)

# WIREFRAME CHECK
code='nul'
while code=='nul':
    try:
        code=int(input('Enter the 3-digit passcode. '))
    except: 
        print('Invalid response.')

############################### IN CASE OF E401, RECHECK. ####################################
agent='aws-amplify/1.0.1'
key='da2-dv5bqitepbd2pmbmwt7keykfg4'
payload={"operationName":"updateAttendance","variables":{"otp":code},"query": "mutation updateAttendance($otp: String!) {\n  updateAttendance(otp: $otp) {\n    id\n    attendance\n    classcode\n    date\n    startTime\n    endTime\n    classType\n    __typename\n  }\n}\n"}
##############################################################################################

#>> SERVICE QUERY
attendix=s.post(logonTicket,headers={"content-type": ContentType},params={'service': 'https://api.apiit.edu.my/attendix'}).text
#print('attendix:'+ attendix)

attendUpdate=s.post(endpoint,headers={"host": 'attendix.apu.edu.my', "path": '/graphql', "content-type": graphqlContent, "sec-fetch-dest": 'empty', "sec-fetch-mode": 'cors', "sec-fetch-site": 'same-site', "ticket": attendix, "x-amz-user-agent": agent, "x-api-key": key},json=payload)
feedbackMessage=((json.loads(str(attendUpdate.text))['errors'])[0])
#print(json.loads(str(attendUpdate.text)))
print(feedbackMessage['message'])

###!!! ON FAIL, RESUBMIT SERVICE QUERY (ATTENDIX)
