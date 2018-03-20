from __future__ import absolute_import, unicode_literals
import time
import logging
from celery import shared_task


log = logging.getLogger('file')


@shared_task(bind=True)
def send_to_credorg(task, order, user):
    """
    Enqueued task
    :param task: 
    :param order: 
    :param user: 
    :return: 
    """
    t = time.time()
    time.sleep(2)
    log.warning('test send_to_credorg: {}\n{}\n{}\n{}\n'.format(
        time.time() - t, task, order, user))
