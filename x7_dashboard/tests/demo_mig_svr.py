"""
X7 mq server function
"""
from x7_mq import MqServer

mw2sDict = { 'X7_Q':'X7_Q_MW2S', 'X7_E':'X7_E_MW2S', 'X7_RK':'X7_PK_MW2S' }

#: This is the callback applied when a message is received.
def handle_message( pkg, message):
    print("Received message: %r" % (pkg, ))
    message.ack()

if __name__ == '__main__':
    mq_server = MqServer( handle_message, mw2sDict )
    mq_server.connect()
    mq_server.run(once=False)



