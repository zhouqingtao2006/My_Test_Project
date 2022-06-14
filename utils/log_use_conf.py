import logging
import logging.config
# 读取日志配置文件内容
import os.path


logging.config.fileConfig(os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'config/logs.conf'))

# 创建一个日志器logger
logger = logging.getLogger('simpleExample')

# 日志输出
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')