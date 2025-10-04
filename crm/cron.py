from datetime import datetime
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    
    # Log heartbeat to the required file
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{timestamp} CRM is alive\n")
    
    # Optional: Verify GraphQL endpoint using gql client
    try:
        # Configure GraphQL client
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Query the hello field
        query = gql("""
            query {
                hello
            }
        """)
        
        result = client.execute(query)
        
        # Log successful GraphQL response
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} GraphQL endpoint is responsive: {result.get('hello', 'No hello field')}\n")
            
    except Exception as e:
        # Log GraphQL check failure
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} GraphQL endpoint check failed: {str(e)}\n")

def update_low_stock():
    """Update low stock products - Task 3"""
    try:
        # Configure GraphQL client
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Mutation to update low stock products
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    success
                    message
                    updatedProducts
                }
            }
        """)
        
        result = client.execute(mutation)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Log the results
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"[{timestamp}] Low Stock Update:\n")
            update_result = result.get('updateLowStockProducts', {})
            f.write(f"Success: {update_result.get('success', False)}\n")
            f.write(f"Message: {update_result.get('message', 'No message')}\n")
            
            updated_products = update_result.get('updatedProducts', [])
            if updated_products:
                f.write("Updated Products:\n")
                for product in updated_products:
                    f.write(f"  {product}\n")
            else:
                f.write("No products updated\n")
            f.write("\n")
            
    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"[{timestamp}] Exception in update_low_stock: {str(e)}\n")            with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                f.write(f"[{timestamp}] Error: HTTP {response.status_code}\n")
                
    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"[{timestamp}] Exception: {str(e)}\n")
