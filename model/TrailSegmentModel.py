import os

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class TrailSegmentModel(Model):
    """
    Literally just stores the name of a trail segment.
    """

    class Meta:
        table_name = f"RiverTrailAlertsTable-{os.getenv('DEPLOYMENT_STAGE', 'dev')}"

    # Always set the partition key to TRAIL_SEGMENT so that we can retrieve the names of 
    # all trail segments with a query on pk=TRAIL_SEGMENT
    pk = UnicodeAttribute(hash_key=True)  # TRAIL_SEGMENT
    sk = UnicodeAttribute(range_key=True) # Trail segment name

