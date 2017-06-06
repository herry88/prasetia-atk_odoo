# -*- coding: utf-8 -*-


{
    'name': "Aplikasi Prasetia",

    'summary': """
        Module yang dibuat untuk prasetia
        """,

    'description': """
        Description non for this time
    """,

    'author': "junifar",
    'website': "http://www.junifar.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'prasetia',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report'],

    # always loaded
    'data': [
        # 'views/views.xml',
        # 'views/templates.xml',
        'report/report_atk_xls.xml',
        'security/atk_security.xml',
        'security/ir.model.access.csv',
        'views/report_atk_request.xml',
        'views/report_atk.xml',
        'views/atk_workflows.xml',
        'views/atk_report.xml',
        'views/atk.xml',
        'wizard/report_atk_wizard.xml',
        'wizard/report_request_atk_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'auto_install': False,
}
