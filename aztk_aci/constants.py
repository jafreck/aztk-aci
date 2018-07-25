import re

RESOURCE_ID_PATTERN = re.compile('^/subscriptions/(?P<subscription>[^/]+)'
                                 '/resourceGroups/(?P<resourcegroup>[^/]+)'
                                 '/providers/[^/]+'
                                 '/[^/]+Accounts/(?P<account>[^/]+)$')
