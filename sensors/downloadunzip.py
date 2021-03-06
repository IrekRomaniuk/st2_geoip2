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
        self._date = self._config['date'] 


    def poll(self):        
        self._logger.debug('#### DownloadSensor dispatching trigger...')
        if self._date:
            date = self._date
        else:    
            date=datetime.datetime.today().strftime('%Y%m%d')
        self._logger.debug('#### Date {} '.format(date))    
        payload = {}        
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        request = get(self._url + '&date=' + date + '&suffix=zip&license_key=' + self._key, verify=False)
        self._logger.debug('#### Response {} '.format(request.status_code))
        if request.status_code == 200:         
            zip_file = ZipFile(BytesIO(request.content))
            files = zip_file.namelist()
            zip_file.extractall("/opt/stackstorm/packs/geoip2/")
            payload['path']=files[0].split('/')[0]    
        payload['date']=date 
        payload['response']=request.status_code  
        #requests.get("")
        self.sensor_service.dispatch(trigger='geoip2.download_unzip', payload=payload)


    def cleanup(self):
        pass

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass