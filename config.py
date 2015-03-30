class Config():
    # file read modes
    START = 'start'
    BLOCK = 'block'
    END = 'end'

    BLOCK_HEADERS = ['hoststatus', 'servicestatus']
    LOOKUP_VALUES = ['host_name', 'active_checks_enabled',
                     'notifications_enabled', 'service_description']
    FILTERS = [
        {'host_name': 'prdcontr'},
        {'active_checks_enabled': '0',
         'notifications_enabled': '0'}
    ]
    HEADER_KEY = 'host_name'

    # Email configuration
    SMTP = "smtp.gmail.com"
    PORT = 587
    FROM = ''
    SUBJECT = 'Status Report'
    GMAIL_PWD = ''
