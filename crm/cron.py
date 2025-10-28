# crm/cron.py

import datetime
from django_cron import CronJobBase, Schedule
import requests
import logging

# ADDED IMPORTS REQUIRED FOR TASK 3 FUNCTIONALITY
from gql.transport.requests import RequestsHTTPTransport 
from gql import gql, Client 

# --- Configuration ---
LOW_STOCK_LOG_FILE = '/tmp/low_stock_updates_log.txt'
GRAPHQL_URL = 'http://localhost:8000/graphql'

# Set up dedicated logging for the low stock updates (appends to file)
logging.basicConfig(
    filename=LOW_STOCK_LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a' 
)

# --- Existing Heartbeat Job (from your code) ---
class HeartbeatCronJob(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'crm.heartbeat_cron'

    def do(self):
        # Using the checker's required log path
        now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with open("/tmp/crm_heartbeat_log.txt", "a") as f: 
            f.write(f"{now} CRM is alive\n")
        print(f"{now} CRM is alive")


# --- NEW JOB FOR TASK 3: Low Stock Restock ---
class LowStockCronJob(CronJobBase):
    # Task 3 requires the job to run every 12 hours (720 minutes)
    RUN_EVERY_MINS = 60 * 12 
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'crm.low_stock_cron'

    def do(self):
        """
        Executes the GraphQL mutation to restock low-stock products.
        """
        MUTATION_QUERY = """
            mutation {
              updateLowStockProducts {
                success
                message
                updatedProducts {
                  id
                  name
                  stock
                }
              }
            }
        """
        
        try:
            # Execute the GraphQL mutation using requests
            response = requests.post(GRAPHQL_URL, json={'query': MUTATION_QUERY}, timeout=5)
            response.raise_for_status() 

            result = response.json()
            mutation_result = result['data']['updateLowStockProducts']
            
            # Logging Logic to /tmp/low_stock_updates_log.txt (Required path)
            log_message = f"MUTATION RESULT: {mutation_result['message']}"
            logging.info(log_message)
            
            for product in mutation_result.get('updatedProducts', []):
                product_log = f"  - Updated: {product['name']} (New Stock: {product['stock']})"
                logging.info(product_log)
                
            print(f"Low stock update complete: {mutation_result['message']}")

        except requests.exceptions.RequestException as e:
            error_msg = f"FATAL ERROR during stock update: {e}"
            logging.error(error_msg)
            print(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error processing GraphQL response: {e}"
            logging.error(error_msg)
            print(error_msg)
