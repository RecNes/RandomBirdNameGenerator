"""
Django logging settings
"""
import os

log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs/')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        # 'special': {
        #     '()': 'project.logging.SpecialFilter',
        #     'foo': 'bar',
        # },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_path, 'django.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        # 'mail_admins': {
        #     'level': 'INFO',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'formatter': 'verbose'
        #     # 'filters': ['special']
        # }
    },
    'loggers': {
        'django': {
            'handlers': ['django', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
