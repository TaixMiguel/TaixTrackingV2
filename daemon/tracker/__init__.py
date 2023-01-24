import logging

from TaixTracking.kTaixTracking import Tracking as KTracking
from tracking.models import Tracking
from daemon.tracker.abstractTracker import AbstractTracker
from daemon.tracker.trackerGlobalCainiao import TrackerGlobalCainiao


def get_instance_tracker(track: Tracking) -> AbstractTracker:
    if track.track_type == KTracking.Types.CAINIAO:
        return TrackerGlobalCainiao(track)
    else:
        logging.error(f'No se encuentra un tracker para el código {track.track_type}')
