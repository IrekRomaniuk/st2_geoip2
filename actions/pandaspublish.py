from st2actions.runners.pythonrunner import Action
import pandas as pd

class pandas_publish(Action):
       
    def run(self, path):
        # path i.e. GeoIP2-Country-CSV_20180515
        #self.logger.info('date of type: {}'.format(type(date)))   
        _countries = self.config['countries']
        _ips = self.config['ips']
        _loc = self.config['loc']
        
        block_countries=_countries.split(',')
        IPs=pd.read_csv(_ips) 
        print(block_countries)
        print(_ips)
        print(_loc)
        print(IPs.head(3))  
        return path