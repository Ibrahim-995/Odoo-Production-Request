{
    'name': 'Production Request',
    'summary': 'Food Production Request',
    'description': """
        This module will help to manage Food Production Request With 3 approvals.
    """,
    'version': '1',
    'category': 'stock',
    "author": "Ibrahim Khalil Ullah & Md Rasel Ali",
    'company': 'Daffodil Computers Limited',
    'website': "https://daffodil-bd.com",
    'depends': ['stock'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/default_data.xml',
        'views/ccl_food_production_request_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu_item.xml',
        'reports/report.xml',
    ],
    # 'icon': "/dsl_food_production_request/static/description/icon.png",
    'installable': True,
    'application': True,
    "auto_install": False,
    'sequence': 1,
    "license": "LGPL-3",
    'price':50,
    'currency':"USD", 
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
