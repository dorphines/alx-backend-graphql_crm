import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

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
    url = "http://127.0.0.1:8000/graphql"
    transport = RequestsHTTPTransport(url=url, verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file_path = '/tmp/low_stock_updates_log.txt'

    try:
        # Execute the UpdateLowStockProducts mutation
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    products {
                        name
                        stock
                    }
                    message
                }
            }
        """)
        
        result = client.execute(mutation)
        
        with open(log_file_path, 'a') as f:
            data = result.get('updateLowStockProducts', {})
            products = data.get('products', [])
            message = data.get('message', '')
            
            f.write(f"[{timestamp}] {message}\n")
            if products:
                for product in products:
                    f.write(f"[{timestamp}] Updated {product['name']} - New Stock: {product['stock']}\n")
            else:
                f.write(f"[{timestamp}] No low stock products found to update.\n")
                
    except Exception as e:
        with open(log_file_path, 'a') as f:
            f.write(f"[{timestamp}] Error during cron job: {str(e)}\n")
