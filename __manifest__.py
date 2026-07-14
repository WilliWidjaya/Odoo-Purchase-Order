{
    'name' : 'Purchase Order PT',
    'version' : '1.0',
    'author' : 'William Widjaya',
    'depends' : ['base'],
    'data' : [
        'views/po_views.xml',
        'views/po_menus.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_frontend': [
            'purchase_order/static/src/css/po_stylesheet.css',
            'purchase_order/static/src/css/request_stylesheet.css',
        ],
        'web.assets_backend': [
            'purchase_order/static/src/css/po_stylesheet.css',
            'purchase_order/static/src/css/request_stylesheet.css',
        ]
    },
    'application' : True,
}