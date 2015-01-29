
{
    "name": "OpenAcademy",
    "version": "1.0",
    "depends": [
        "base",
        "mail",
        "report_webkit",
    ],
    "author": "Carlos Contreras",
    "category": "Academic",
    "description": """
OpenAcademy
===========

Este módulo permite la gestión de centros educativos.
""",
    'data': [
        'openacademy_view.xml',
        'openacademy_board.xml',
        'openacademy_menu.xml',
        'openacademy_workflow.xml',
        'security/openacademy_security.xml',
        'security/ir.model.access.csv',
        'wizards/openacademy_wizards_view.xml',
        'openacademy_report.xml',
        #all other data files, except demo data and tests
        ],
    'demo': [
        #files containg demo data
    ],
    'test': [
        #files containg tests
    ],
    'installable': True,
    'auto_install': False,
}
