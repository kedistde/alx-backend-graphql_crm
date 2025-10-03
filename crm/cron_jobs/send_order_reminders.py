#!/usr/bin/env python3

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append('/path/to/your/django/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def send_order_reminders():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # GraphQL query to get recent orders
    query = gql("""
    query {
        orders(last: 100) {
            edges {
                node {
                    id
                    orderDate
                    customer {
                        email
                    }
                }
            }
        }
    }
    """)
    
    # Configure GraphQL client
    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql',
        use_json=True
    )
    
    try:
        client = Client(transport=transport, fetch_schema_from_transport=True)
        result = client.execute(query)
        
        # Process orders from last 7 days
        one_week_ago = datetime.now() - timedelta(days=7)
        
        with open('/tmp/order_reminders_log.txt', 'a') as log_file:
            log_file.write(f"[{timestamp}] Order Reminders:\n")
            
            for edge in result.get('orders', {}).get('edges', []):
                order = edge['node']
                order_date = datetime.fromisoformat(order['orderDate'].replace('Z', ''))
                
                if order_date >= one_week_ago:
                    log_entry = f"Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n"
                    log_file.write(log_entry)
            
            log_file.write("\n")
        
        print("Order reminders processed!")
        
    except Exception as e:
        with open('/tmp/order_reminders_log.txt', 'a') as log_file:
            log_file.write(f"[{timestamp}] ERROR: {str(e)}\n")

if __name__ == "__main__":
    send_order_reminders()
