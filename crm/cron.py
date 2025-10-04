import requests
from datetime import datetime

def update_low_stock():
    mutation = """
    mutation {
        updateLowStockProducts {
            success
            message
            updatedProducts
        }
    }
    """
    
    try:
        response = requests.post(
            'http://localhost:8000/graphql',
            json={'query': mutation},
            headers={'Content-Type': 'application/json'}
        )
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('data', {}).get('updateLowStockProducts', {})
            
            with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                f.write(f"[{timestamp}] Low Stock Update:\n")
                f.write(f"Success: {result.get('success', False)}\n")
                f.write(f"Message: {result.get('message', 'No message')}\n")
                if result.get('updatedProducts'):
                    for product in result['updatedProducts']:
                        f.write(f"  {product}\n")
                f.write("\n")
        else:
            with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                f.write(f"[{timestamp}] Error: HTTP {response.status_code}\n")
                
    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"[{timestamp}] Exception: {str(e)}\n")
