from st2reactor.sensor.base import PollingSensor
import requests
from requests import get
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from io import BytesIO
from zipfile import ZipFile
# import urllib3
import datetime


class DownloadSensor(PollingSensor):
    def __init__(self, sensor_service, config, poll_interval):
        super(DownloadSensor, self).__init__(sensor_service=sensor_service, config=config, poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)

    def setup(self):        
        self._url = self._config['base_url'] 
        self._key = self._config['license_key'] 
        self._date = self._config['license_key'] 


    def poll(self):        
        self._logger.debug('#### DownloadSensor dispatching trigger...')
        if self._date:
            date = self._date
        else:    
            date=datetime.datetime.today().strftime('%Y%m%d')
        payload = {}        
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        request = get(self._url + '&date=' + date + '&suffix=zip&license_key=' + self._key, verify=False)
        self._logger.debug('#### Response {} '.format(request.status_code))
        if request.status_code == 200:         
            zip_file = ZipFile(BytesIO(request.content))
            files = zip_file.namelist()
            zip_file.extractall("./etc")
            payload['files']=files      
        payload['date']=date 
        payload['response']=request.status_code  
        #requests.get("https://hchk.io/f48b4815-cb37-417b-ae93-fafb6faec53f")
        self.sensor_service.dispatch(trigger=self.trigger, payload=payload)


    def cleanup(self):
        pass

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass