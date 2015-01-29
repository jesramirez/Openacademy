
{
    "name": "OpenAcademy",
    "version": "1.0",
    "depends": [
        "base",
        "mail",
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
        'openacademy_menu.xml',
        'openacademy_workflow.xml',
        'security/openacademy_security.xml',
        'security/ir.model.access.csv',
        'wizards/openacademy_wizards_view.xml',
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
