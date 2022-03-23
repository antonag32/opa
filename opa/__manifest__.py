{
    'name': 'Open Academy',
    'summary': 'Manage your academy.',
    'author': 'Vauxoo',
    'website': 'https://vauxoo.com',
    'category': 'Services',
    'version': '15.0.1.0.0',
    'depends': ['base'],
    'data': [
        'security/ir_module_category.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/res_users.xml',
        'views/course_views.xml',
        'views/session_views.xml',
        'views/ir_ui_menu.xml'
        'views/res_partner_views.xml',
        'data/res_partner_category.xml',
    ],
    'demo': ['demo/course_demo.xml'],
    'application': True,
    'license': 'LGPL-3'
}
