import azure.functions as func

app = func.FunctionApp()

@app.queue_trigger(arg_name="msg", queue_name="ingestionqueue", connection="SERVER_BUS_CONNECTION_STRING")
def QueueTrigger(msg: func.QueueMessage):
    print("Queue message:", msg.get_body().decode())
