import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def send_updates(diffs):
    for location, prev, curr in diffs:
        log.debug(f'{location} changed from {prev} to {curr}')

