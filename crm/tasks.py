from celery import shared_task
import datetime
from schema import schema

@shared_task
def generatecrmreport():
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
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

    with open(log_file_path, 'a') as f:
        f.write(log_message)
