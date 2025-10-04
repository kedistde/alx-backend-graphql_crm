#!/bin/bash

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Execute Django shell command to delete inactive customers
DELETE_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Order

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(
    orders__isnull=True,
    date_joined__lt=one_year_ago
) | Customer.objects.filter(
    orders__order_date__lt=one_year_ago
).distinct()

count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the result
echo "[$TIMESTAMP] Deleted $DELETE_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
