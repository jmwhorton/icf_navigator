oc exec deployment/navigator -c navigator -- ./manage.py dumpdata --exclude auth.permission --exclude contenttypes > prod_data.json
