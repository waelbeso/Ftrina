from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app  # noqa
#print "celery app is imported"
#print dir(celery_app)
#print celery_app.task

#default_app_config  = 'dashboard.apps.DashboardConfig'