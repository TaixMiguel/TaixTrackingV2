import logging
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from tracking.models import Tracking, TrackingDetail


class AbstractTracker(ABC):

    __tracking: Tracking

    def __init__(self, tracking: Tracking):
        self.__tracking = tracking

    def search_last_detail(self) -> None:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page_path = self._get_url_page(self.__tracking.track_code)

            page.goto(page_path)
            page_content = page.content()

            soup = BeautifulSoup(page_content, "html.parser")
            self._search_data(soup)
            browser.close()

    @abstractmethod
    def is_new_detail(self) -> bool:
        pass

    def add_new_detail(self) -> TrackingDetail:
        from django.db import IntegrityError
        try:
            detail: TrackingDetail = self._save_new_detail()
            # TODO: avisar al usuario del nuevo detalle
        except IntegrityError as e:
            logging.info(f'Se ha tratado de insertar dos veces una misma situación asociada al tracking '
                         f'{self._get_tracking().__str__()}')

    @abstractmethod
    def _save_new_detail(self) -> TrackingDetail:
        pass

    @abstractmethod
    def _get_url_page(self, track_order: str) -> str:
        pass

    @abstractmethod
    def _search_data(self, soup: BeautifulSoup) -> None:
        pass

    def _get_tracking(self) -> Tracking:
        return self.__tracking

    def _get_last_detail(self) -> TrackingDetail:
        return TrackingDetail.objects.filter(id_tracking_fk=self._get_tracking()).order_by('-audit_time')[:1]
