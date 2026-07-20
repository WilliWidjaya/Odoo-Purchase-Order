{
    'name' : 'PO SAP',
    'version' : '1.0',
    'author' : 'William Widjaya',
    'depends' : ['base'],
    'data' : [
        'security/ir.model.access.csv',
        'views/po_views.xml',
        'views/po_menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'purchase_order/static/src/css/po_stylesheet.css',
            'purchase_order/static/src/css/request_stylesheet.css',
            'purchase_order/static/src/css/item_stylesheet.css',
        ],
        'web.assets_backend': [
            'purchase_order/static/src/css/po_stylesheet.css',
            'purchase_order/static/src/css/request_stylesheet.css',
            'purchase_order/static/src/css/item_stylesheet.css',
        ]
    },
    'application' : True,
}