from st2reactor.sensor.base import PollingSensor
from requests import get
from io import BytesIO
from zipfile import ZipFile
import urllib3
import datetime


class DownloadSensor(PollingSensor):
    def __init__(self, sensor_service, config, poll_interval):
        super(DownloadSensor, self).__init__(sensor_service=sensor_service, config=config, poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)

    def setup(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._url = self._config['base_url'] 
        self._key = self._config['license_key'] 


    def poll(self):        
        self._logger.debug('DownloadSensor dispatching trigger...')
        date=datetime.datetime.today().strftime('%Y%m%d')
        payload = {}
        request = get(self._url + '&date=' + date + '&suffix=zip&license_key=' + self._key, verify=False)
        self._logger.debug('response {} '.format(request))
        if request.status_code == 200:         
            zip_file = ZipFile(BytesIO(request.content))
            files = zip_file.namelist()
            zip_file.extractall("./etc")
            payload['files']=files
        payload['date']=date   


    def cleanup(self):
        pass

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass