   
"""
X7 mq server function
"""
from x7_mq import MqServer

hw2sDict = { 'X7_Q':'X7_Q_HW2S', 'X7_E':'X7_E_HW2S', 'X7_RK':'X7_PK_HW2S' }

#: This is the callback applied when a message is received.
def handle_message( pkg, message):
    print("Received message: %r" % (pkg, ))
    message.ack()

if __name__ == '__main__':
    mq_server = MqServer( handle_message, hw2sDict )
    mq_server.connect()
    mq_server.run(once=False)



