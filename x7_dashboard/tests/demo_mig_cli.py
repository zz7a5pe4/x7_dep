"""
X7 mq client function
"""

from x7_mq import MqClient

#Message from web to server
ms2wDict = { 'X7_Q':'X7_Q_MS2W', 'X7_E':'X7_E_MS2W', 'X7_RK':'X7_PK_MS2W' }
client = MqClient( ms2wDict )
client.connect()
client.send( {"instance": "Ubuntu-Server", "host": "host106", "mesg":"success", "desc":"success"} )      

   
