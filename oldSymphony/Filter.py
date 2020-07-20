
import json
import contextlib

@contextlib.contextmanager
def write_to(filename, ops='a'):
    f = open(filename, ops)
    yield f
    f.close()

# file=open('FnOIds.txt', 'w')
# file.write('SymbolName, ExchangeInstrumentID'+'\n')
# file.close()
with open('master.json', 'r') as f:
    for line in (f):
        data=json.loads(line)
    # print(type(data))
# j=0
file1='OptionIds.txt'
with write_to(file1) as f:
    for i in range (len(data['result'])):
        if data['result'][i]['ExchangeSegment']==2 and data['result'][i]['Series']=='OPTIDX':
            if data['result'][i]['DisplayName'][:9]=='BANKNIFTY' or data['result'][i]['DisplayName'][:5]=='NIFTY':
                data['result'][i]['DisplayName']=data['result'][i]['DisplayName'].replace(" ", '')
                data['result'][i]['DisplayName']=data['result'][i]['DisplayName'].replace("2019", '19')
                data['result'][i]['DisplayName'] = data['result'][i]['DisplayName'][:-7] + data['result'][i]['DisplayName'][-5:] + data['result'][i]['DisplayName'][-7:-5]
                # print(data['result'][i]['DisplayName'])
                L=str(data['result'][i]['ExchangeInstrumentID'])+','+str(data['result'][i]['DisplayName'])+'\n'#+','+str(data['result'][i]['Series'])+','+str(data['result'][i]['ExchangeSegment'])+','+str(data['result'][i]['LotSize'])+','+'\n'
                f.write(L)

# file=open(r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\SymphonyDataFilter\FuturesId.txt', 'w')
# file.write('ExchangeInstrumentID, DisplayName, LotSize'+'\n')
# file.close()

file1=r'FuturesIdS.txt'
with write_to(file1) as f:
    for i in range (len(data['result'])):
        if data['result'][i]['ExchangeSegment']==2 and (data['result'][i]['Series']=='FUTSTK' or data['result'][i]['Series']=='FUTIDX'):
            L=str(str(data['result'][i]['ExchangeInstrumentID'])+','+ data['result'][i]['Description']) + '\n' #',' +str(data['result'][i]['LotSize'])+'\n'#','+str(data['result'][i]['ExchangeSegment'])+','+str(data['result'][i]['LotSize'])+','+'\n'
            f.write(L)
