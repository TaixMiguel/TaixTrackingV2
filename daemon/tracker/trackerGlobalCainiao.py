from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import PageElement

from daemon.tracker import AbstractTracker
from tracking.models import Tracking, TrackingDetail


class TrackerGlobalCainiao(AbstractTracker):

    _headDetail: str
    _textDetail: str
    _date_gmt: datetime = None

    def __init__(self, tracking: Tracking):
        super().__init__(tracking)

    def _get_url_page(self, track_order: str) -> str:
        return "https://global.cainiao.com/newDetail.htm?mailNoList=" + track_order

    def _search_data(self, soup: BeautifulSoup) -> None:
        last_detail: PageElement = soup.find("div", {"class": "TrackingDetail--firstStep--dSIAnAW"})
        self._headDetail = last_detail.findNext("span", {"class": "TrackingDetail--head--20GpNSP"}).get_text()
        self._textDetail = last_detail.findNext("span", {"class": "TrackingDetail--text--3Odqdxz"}).get_text()
        time_gmt: str = last_detail.findNext("span", {"class": "TrackingDetail--timeText--3x08R3x"}).get_text()

        if len(time_gmt) >= 25:
            if len(time_gmt) == 26:
                time_gmt = time_gmt + ':00'
            elif len(time_gmt) == 25:
                time_gmt = time_gmt[0:24] + '0' + time_gmt[24:25] + ':00'
            self._date_gmt = datetime.strptime(time_gmt, '%Y-%m-%d %H:%M:%S %Z%z')
        else:
            from django.utils import timezone
            time_gmt = time_gmt[0:19]
            self._date_gmt = datetime.strptime(time_gmt, '%Y-%m-%d %H:%M:%S')
            self._date_gmt = timezone.make_aware(self._date_gmt, timezone.get_current_timezone())

    def is_new_detail(self) -> bool:
        last_detail = self._get_last_detail()
        if (not last_detail) or ((last_detail[0].detail_head is not self._headDetail) or (last_detail[0].detail_text
           is not self._textDetail) or (last_detail[0].audit_time != self._date_gmt)):
            return True
        return False

    def _save_new_detail(self) -> TrackingDetail:
        aux_detail: TrackingDetail = TrackingDetail(id_tracking_fk=self._get_tracking(), detail_head=self._headDetail,
                                                    detail_text=self._textDetail, audit_time=self._date_gmt)
        aux_detail.save()
        return aux_detail
