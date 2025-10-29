#!/c/Users/T/Desktop/alx-backend-graphql_crm/venv/Scripts/python
# NOTE: The shebang above points directly to your virtual environment Python interpreter

import os
import sys
import logging
from datetime import datetime, timedelta

# Ensure the project root is in the path so Django models/settings can be imported
PROJECT_ROOT = "/c/Users/T/Desktop/alx-backend-graphql_crm"
sys.path.append(PROJECT_ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings') # Replace 'alx_backend_graphql_crm' with your actual project name

try:
    import django
    django.setup()
except Exception as e:
    # Log initialization errors for debugging if Django setup fails
    print(f"Django setup error: {e}", file=sys.stderr)
    sys.exit(1)

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from django.utils import timezone # Using Django's timezone utility

# --- Configuration ---
GRAPHQL_URL = 'http://localhost:8000/graphql'
LOG_FILE = '/tmp/order_reminders_log.txt'

# --- GraphQL Query ---
# This query is a placeholder. Adapt it to your actual GraphQL schema.
QUERY = gql("""
    query getPendingOrders($startDate: Date!) {
      pendingOrders(startDate: $startDate) {
        id
        orderDate
        customer {
          email
        }
      }
    }
""")

# --- Logging Setup ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def send_reminders():
    """
    Queries the GraphQL endpoint for recent orders and logs them as reminders.
    """
    try:
        # Calculate the start date (7 days ago) in YYYY-MM-DD format
        seven_days_ago = timezone.now() - timedelta(days=7)
        start_date_str = seven_days_ago.strftime('%Y-%m-%d')

        # Set up the GraphQL client transport
        transport = RequestsHTTPTransport(
            url=GRAPHQL_URL,
            verify=True,
            retries=3,
        )

        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Execute the query with the calculated variable
        result = client.execute(
            QUERY, 
            variable_values={"startDate": start_date_str}
        )
        
        # Check if the query returned any orders
        orders = result.get('pendingOrders', [])
        
        if not orders:
            logging.info("No pending orders found in the last 7 days.")
            print("Order reminders processed! (No new reminders)")
            return

        logged_count = 0
        for order in orders:
            order_id = order.get('id')
            customer_email = order.get('customer', {}).get('email', 'N/A')
            
            log_message = f"REMINDER: Order ID {order_id} placed on {order.get('orderDate', 'N/A')} for customer {customer_email} is pending."
            logging.info(log_message)
            logged_count += 1
            
        print(f"Order reminders processed! Logged {logged_count} orders.")

    except Exception as e:
        # Log any unexpected errors during execution
        error_message = f"FATAL ERROR during reminder process: {e}"
        logging.error(error_message)
        print(error_message, file=sys.stderr)
        
if __name__ == "__main__":
    send_reminders()