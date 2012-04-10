"""
X7 mq client function
"""

from x7_mq import MqServer

#Message from web to server
hs2wDict = { 'X7_Q':'X7_Q_HS2W', 'X7_E':'X7_E_HS2W', 'X7_RK':'X7_PK_HS2W' }
server = MqServer( None, hs2wDict )
server.create_queue()



   
