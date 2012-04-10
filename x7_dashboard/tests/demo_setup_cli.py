"""
X7 mq client function
"""

from x7_mq import MqClient

#Message from web to server
hs2wDict = { 'X7_Q':'X7_Q_HS2W', 'X7_E':'X7_E_HS2W', 'X7_RK':'X7_PK_HS2W' }
client = MqClient( hs2wDict )
client.connect()

client.send({"type":"prog", "mesg":"100", "hostname": "cloudnode-1"})
client.send( {"type":"cmd", "mesg":"success", "hostname": "cloudnode-1"} ) 
client.send({"type":"prog", "mesg":"40", "hostname": "cloudnode-2"})
client.send({"type":"prog", "mesg":"50", "hostname": "cloudnode-3"})
client.send({"type":"log", "mesg":"Get:4 http://cn.archive.ubuntu.com oneiric Release [40.8 kB]", "hostname": "cloudnode-1"})
client.send({"type":"log", "mesg":"Get:4 http://cn.archive.ubuntu.com oneiric Release [40.8 kB]", "hostname": "cloudnode-2"})
client.send({"type":"log", "mesg":"Get:4 http://cn.archive.ubuntu.com oneiric Release [40.8 kB]", "hostname": "cloudnode-3"})
client.send({"type":"log", "mesg":"Get:4 http://cn.archive.ubuntu.com oneiric Release [40.8 kB]", "hostname": "cloudnode-1"})
client.send({"type":"log", "mesg":"Get:4 http://cn.archive.ubuntu.com oneiric Release [40.8 kB]", "hostname": "cloudnode-2"})
client.send({"type":"log", "mesg":"Get:4 http://cn.archive.ubuntu.com oneiric Release [40.8 kB]", "hostname": "cloudnode-2"})

