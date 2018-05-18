from st2actions.runners.pythonrunner import Action
import pandas as pd

class pandas_publish(Action):
       
    def run(self, path):
        # path i.e. GeoIP2-Country-CSV_20180515
        # self.logger.info('date of type: {}'.format(type(date)))   
        _countries = self.config['countries']
        _ips = self.config['ips']
        _loc = self.config['loc']
        
        block_countries=_countries.split(',')
        print(block_countries[0], _ips,_loc) 
        IPs=pd.read_csv("/opt/stackstorm/packs/geoip2/"+path+'/'+_ips)         
        IPs.drop(['registered_country_geoname_id','represented_country_geoname_id','is_anonymous_proxy','is_satellite_provider'],axis=1,inplace=True)
        # print(IPs.head(3))
        loc=pd.read_csv("/opt/stackstorm/packs/geoip2/"+path+'/'+_loc)
        loc.drop(['locale_code','continent_code','is_in_european_union','continent_name'],axis=1,inplace=True)
        # print(loc.head(3))
        result=IPs.merge(loc,left_on='geoname_id',right_on='geoname_id',how='outer')
        print(result.head(3))
        # print(IPs.shape,loc.shape,result.shape)
        block_subnets_pd=result[result['country_name'].isin(block_countries)]['network']
        # print(block_subnets_pd.head(3))
        response = block_subnets_pd.to_csv('/opt/stackstorm/static/webui/GeoIP2.txt', encoding='utf-8', index=False, header=False)
        return response