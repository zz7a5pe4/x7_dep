import simplejson
from x7_mq import MqReader
import sys

#mw2sDict = { 'X7_Q':'X7_Q_MW2S', 'X7_E':'X7_E_MW2S', 'X7_RK':'X7_PK_MW2S' }

if len(sys.argv) != 2 :
    print "need key name \nuseage: " + sys.argv[0] + " MW2S \nMW2S is key name of { 'X7_Q':'X7_Q_MW2S', 'X7_E':'X7_E_MW2S', 'X7_RK':'X7_PK_MW2S' } "
    sys.exit()

kn = sys.argv[1]
hs2wDict = { }
hs2wDict['X7_Q'] = 'X7_Q_' + kn
hs2wDict['X7_E'] = 'X7_E_' + kn
hs2wDict['X7_RK'] = 'X7_PK_' + kn

reader = MqReader( hs2wDict )
reader.connect()

while True:
    mesg = reader.get()
    if mesg is not None:
        print( "clear message:" + simplejson.dumps( mesg.payload ) )
    else:
        break
print "clear complete!"
