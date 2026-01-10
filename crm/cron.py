import datetime

def log_crm_heartbeat():
    """
    Logs a heartbeat message to verify the CRM application's health.
    """
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"
    
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(message)

