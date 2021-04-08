oc rsh -c navigator deployment/navigator python manage.py dumpdata --exclude auth.permission --exclude contenttypes > prod.json
