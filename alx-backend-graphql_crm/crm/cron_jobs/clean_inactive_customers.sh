#!/bin/bash

# --- Script: clean_inactive_customers.sh ---

# 1. Define the absolute path to your Django project's root
PROJECT_ROOT="/c/Users/T/Desktop/alx-backend-graphql_crm"
MANAGE_PY="$PROJECT_ROOT/manage.py"

# 2. Define the absolute path to the Python interpreter (Verified by your 'which python' command)
PYTHON_BIN="/c/Users/T/Desktop/alx-backend-graphql_crm/venv/Scripts/python"

# 3. Define the log file path as required
LOG_FILE="/tmp/customer_cleanup_log.txt"

# 4. The Python command to execute via the Django shell (delete logic)
# NOTE: This is the core task logic. It assumes:
# a) You have a 'crm' Django app.
# b) There is a 'Customer' model inside crm.models.
# c) The Customer model has a field 'last_order_date' (or similar for filtering).
PYTHON_COMMAND='from crm.models import Customer; from datetime import timedelta; from django.utils import timezone; one_year_ago = timezone.now() - timedelta(days=365); deleted_count, _ = Customer.objects.filter(last_order_date__lt=one_year_ago).delete(); print(f"Deleted customers: {deleted_count}")'

# --- Execution Block ---
echo "=========================================" >> "$LOG_FILE"
echo "Start cleanup at $(date)" >> "$LOG_FILE"

# Execute the Django management command
# We change directory (cd) first to ensure manage.py finds settings
cd "$PROJECT_ROOT" && "$PYTHON_BIN" "$MANAGE_PY" shell --command="$PYTHON_COMMAND" 2>&1 | tee -a "$LOG_FILE"

echo "Finish cleanup at $(date)" >> "$LOG_FILE"
echo "=========================================" >> "$LOG_FILE"

exit 0

