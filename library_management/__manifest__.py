{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'library system managment',
    'category': 'Tools',
    'author': 'Nayera',

    'depends': ['base','expense_tracker','product','sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/library_book_views.xml',
        'views/library_member_views.xml',
        'views/borrow_record_views.xml',
        'views/sale_record_views.xml',
        'wizard/borrow_book_wizard.xml'
    ],

    'installable': True,
    'application': True,
}