import logging
import datetime

from model.StatusModel import StatusModel
from model.TrailSegmentModel import TrailSegmentModel

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

def save(location, time, status):
    status_model = StatusModel(pk=location, sk=time, status=status)
    status_model.save()
    
    segment_model = TrailSegmentModel(pk='TRAIL_SEGMENT', sk=location)
    segment_model.save()

def get_all_trail_segments():
    segments = TrailSegmentModel.query('TRAIL_SEGMENT')
    return [segment.sk for segment in segments]

