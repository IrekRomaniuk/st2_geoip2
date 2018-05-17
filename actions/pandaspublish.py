from st2actions.runners.pythonrunner import Action

class pandas_publish(Action):
       
    def run(self, file):
        #_tag = self.config['date']
        self.logger.info('file: {}\ntype: {}'.format(file, type(file)))
        list = file.split(',')
        return list