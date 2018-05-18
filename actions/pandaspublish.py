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
        IPs=pd.read_csv("/opt/stackstorm/packs/geoip2/"+path+'/'+_loc) 
        #print(block_countries, _ips,_loc)
        print(IPs.head(3))  
        return path