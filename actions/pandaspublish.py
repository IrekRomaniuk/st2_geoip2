from st2actions.runners.pythonrunner import Action

class pandas_publish(Action):
       
    def run(self, file):
        #_tag = self.config['date']
        self.logger.info('file of type: {}'.format(type(file)))
        # list = file.split(',')
        return file