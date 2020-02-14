# This is a lame broker (or message dispatcher). When Gromacs enters a run, 
# it should choose a broker from here and dispatch messages through it.
#
# Depending on the broker, the messages may be just printed or something else

import datetime
import os

class Printing(object):
    def __init__(self):
        '''This is a proxy to put a message directly to the stdout through
        "print" command'''
        pass
    def dispatch(self, msg):
        '''Simply print the msg passed'''
        print msg

class DjangoDB(object):
    def __init__(self, *args, **kwargs):
        '''This is a proxy to save a message to a Database using Django ORM'''
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "http_settings")
        import http_settings
        import http_models

        self.pk = kwargs.get("pk")
        #TODO Test this, as importing * seems to not work
        self.queue_task = http_models.QueueTask.objects.get(pk = self.pk)

    def dispatch(self, msg):
        '''Put a message in the "last_message" column of the table'''

        self.queue_task.last_message = str(msg)
        self.queue_task.save()

        return True
