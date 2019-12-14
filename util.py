import logging
import datetime

from model.StatusModel import StatusModel

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_latest_statuses(locations):
    log.debug(f'Retrieving statuses for: {locations}')
    statuses = dict()
    for loc in locations:
        res = StatusModel.query(
            loc,
            limit=1,
            scan_index_forward=False
        )

        try:
            res = res.next()
        except:
            res = StatusModel(pk=loc, sk=get_time(), status='closed')

        statuses[res.pk] = res.status

    return statuses
