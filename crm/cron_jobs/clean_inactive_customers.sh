#!/bin/bash
cd /home/dorfin/alx/repos/alx-backend-graphql_crm || exit

output=$(python3 manage.py shell <<EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(orders__order_date__gte=one_year_ago)
count = inactive_customers.count()
if count > 0:
    inactive_customers.delete()
print(count)
EOF
)

echo "$(date): Deleted $output customers" >> /tmp/customer_cleanup_log.txt
