# -*- coding: utf-8 -*-
{
    'name': "vit_product_request_form_pr",

    'summary': """
        Field Description, Requester ID, Approval""",

    'description': """
        Field Description, Requester ID, Approval
    """,

    'author': "Richard Angga",
    'website': "richard.angga51@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','vit_budget_product_request','vit_product_request'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}