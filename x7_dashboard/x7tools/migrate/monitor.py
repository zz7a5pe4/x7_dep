"""
X7 live migration initiator and monitor
"""
import sys, os, subprocess
import time
from x7tools.x7_mq import MqClient,  MqServer

def handle_message( pkg, message):
    """callback function

    """
    print("Received message: %r" % (pkg, ))
    # kombu.transport.virtual.Message.ack():
    # Acknowledge this message as being processed. This will remove the message from the queue.
    message.ack()
    params = simplejson.loads( pkg )

    # start migration
    if(params['type'] <> 'cmd' or params['mesg'] <>'migrate'):
        return
    instance = params["instance"]
    host = params["host"]
    nova_cmd.live_migrate(instance,host)

    # check progress
    wait_time = 600                      # in seconds
    end_time = time.time() + wait_time    #
    interval = 2
    while True:
        vm = _get_vm(instance, host)
        if vm == None: continue
        state = vm["state"]
        if(state == "running"):   # TODO
            client.send( {"instance":instance, "mesg": "success","desc":"migration succeeded"} )
            break
        elif(state == "error"):  #TODO
            client.send( {"instance":instance, "mesg": "error","desc":"error"} )
            break
        elif(vm_state == "000"):
            client.send( {"instance":instance, "mesg": "success","desc":""} )
            
        else:
	    client.send( {"instance":instance, "mesg": "fail","desc":"unknown state"} )
            break
        time.sleep(interval)
        if time().time > end_time:
	    client.send( {"instance":instance, "mesg": "fail","desc":"time out"} )
            break
    else:
        pass

    return

def _get_vm(instance,host):
    """ get vm by instance id

    """
    vms = nova_cmd.vm_list(host)
    for vm in vms:
        if(instance == vm["instance"] ): return vm
    return None


if __name__ == '__main__':

    ms2wDict = { 'X7_Q':'X7_Q_MS2W', 'X7_E':'X7_E_MS2W', 'X7_RK':'X7_PK_MS2W' }
    client = MqClient( ms2wDict )
    client.connect()

    mw2sDict = { 'X7_Q':'X7_Q_MW2S', 'X7_E':'X7_E_MW2S', 'X7_RK':'X7_PK_MW2S' }
    mq_server = MqServer( handle_message, mw2sDict)
    mq_server.connect()
    message = mq_server.run()

