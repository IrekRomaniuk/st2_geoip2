from st2actions.runners.pythonrunner import Action

class pandas_publish(Action):
       
    def run(self, date):
        #_tag = self.config['date']
        #self.logger.info('date of type: {}'.format(type(date)))        
        return date