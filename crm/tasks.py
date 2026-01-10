from celery import shared_task
from datetime import datetime
import requests
from schema import schema

@shared_task
def generate_crm_report():
    query = """
    {
        allCustomers {
            totalCount
        }
        allOrders {
            totalCount
        }
    }
    """
    # Note: total revenue (sum of totalamount) is not directly available in the standard schema 
    # without aggregations which might not be exposed. 
    # I will calculate it by fetching all orders and summing up.
    
    query_full = """
    {
        allCustomers {
            totalCount
        }
        allOrders {
            totalCount
            edges {
                node {
                    totalAmount
                }
            }
        }
    }
    """

    result = schema.execute(query_full)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file_path = '/tmp/crmreportlog.txt'
    
    if result.errors:
        log_message = f"{timestamp} - Report generation failed: {result.errors}\n"
    else:
        data = result.data
        total_customers = data.get('allCustomers', {}).get('totalCount', 0)
        orders_data = data.get('allOrders', {})
        total_orders = orders_data.get('totalCount', 0)
        
        # Calculate revenue
        revenue = 0.0
        edges = orders_data.get('edges', [])
        for edge in edges:
            node = edge.get('node', {})
            amount = node.get('totalAmount')
            if amount:
                revenue += float(amount)
        
        log_message = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {revenue} revenue.\n"

    # Use requests to simulate sending the report to an external service
    try:
        # Placeholder for an actual endpoint
        requests.post("http://localhost:8000/api/report-log", json={"message": log_message})
    except requests.exceptions.RequestException:
        pass

    with open(log_file_path, 'a') as f:
        f.write(log_message)
