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
    SMTP_GMAIL = 'smtp.gmail.com'  # for gmail
    PORT_GMAIL = 587
    FROM = ''
    PASSWD = ''

    SMTP = 'localhost'

    TO_LIST = [
        'ankit.singh@imaginea.com',
        # 'adithya.p@imaginea.com',
        'raghava.kumar@imaginea.com',
        # 'sibaprasad.mahapatra@imaginea.com',
        # 'raghava.kumar@imaginea.com'
    ]
    # if USE_LOCALHOST is true, it will send using gmail , we need to configure smtp and port
    # accordingly
    USE_LOCALHOST = True

    # Formatter configuration
    REPORT_HEADER = ['name', 'host_status', 'service_status', 'service_info']
    MAIL_HEADING = 'Icinga Host & Service Status Report'
    MAX_SERVICE_COUNT = {
        'prdcontrapp': 13,
        'prdcontrdb': 12,
        'prdcontr': 18
    }
    SERVICE_COUNT_THRESHOLD = 5
    DEFAULT_SERIVCE_MESSAGE = 'Some Message'

    EMPTY_REPORT_MESSAGE = 'No data to show'
