import os
import airflow.configuration as conf
from airflow.config_templates.airflow_local_settings import (
    DEFAULT_LOGGING_CONFIG,
    LOG_LEVEL,
    FILENAME_TEMPLATE,
    BASE_LOG_FOLDER,
    PROCESSOR_LOG_FOLDER,
    PROCESSOR_FILENAME_TEMPLATE
)
from copy import deepcopy

LOGGING_CONFIG = deepcopy(DEFAULT_LOGGING_CONFIG)
S3_LOG_FOLDER = conf.get('core', 'remote_base_log_folder')

if S3_LOG_FOLDER:
    LOGGING_CONFIG['handlers'].update({
        's3.task': {
            'class': 'airflow.utils.log.s3_task_handler.S3TaskHandler',
            'formatter': 'airflow.task',
            'base_log_folder': os.path.expanduser(BASE_LOG_FOLDER),
            's3_log_folder': S3_LOG_FOLDER,
            'filename_template': FILENAME_TEMPLATE,
        },
        's3.processor': {
            'class': 'airflow.utils.log.s3_task_handler.S3TaskHandler',
            'formatter': 'airflow.processor',
            'base_log_folder': os.path.expanduser(PROCESSOR_LOG_FOLDER),
            's3_log_folder': S3_LOG_FOLDER,
            'filename_template': PROCESSOR_FILENAME_TEMPLATE,
        },
    })
    LOGGING_CONFIG['loggers'].update({
        'airflow.task': {
            'handlers': ['s3.task'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'airflow.task_runner': {
            'handlers': ['s3.task'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    })
