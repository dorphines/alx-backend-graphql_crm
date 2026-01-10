import datetime
import logging

def log_crm_heartbeat():
    """
    Logs a heartbeat message to verify the CRM application's health.
    """
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"
    
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(message)

def update_low_stock():
    """
    Executes the UpdateLowStockProducts mutation via the GraphQL endpoint
    and logs the updates.
    """
    # Import here to avoid circular imports or loading issues at startup
    from schema import schema
    
    mutation = """
        mutation {
            updateLowStockProducts {
                products {
                    name
                    stock
                }
                message
            }
        }
    """
    
    result = schema.execute(mutation)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file_path = '/tmp/low_stock_updates_log.txt'
    
    with open(log_file_path, 'a') as f:
        if result.errors:
            f.write(f"[{timestamp}] Error executing mutation: {result.errors}\n")
        else:
            data = result.data.get('updateLowStockProducts', {})
            products = data.get('products', [])
            message = data.get('message', '')
            
            f.write(f"[{timestamp}] {message}\n")
            if products:
                for product in products:
                    f.write(f"[{timestamp}] Updated {product['name']} - New Stock: {product['stock']}\n")
            else:
                f.write(f"[{timestamp}] No low stock products found to update.\n")