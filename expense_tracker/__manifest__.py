{
    'name': 'Expense Tracker',
    'version': '1.0',
    'summary': 'Track user expenses and budgets',
    'category': 'Tools',
    'author': 'Nayera',

    'depends': ['base'],

    'data': [
        'reports/monthly_report_template.xml',
        'security/ir.model.access.csv',
        'views/expense_user_views.xml',
        'views/base_menu.xml',
        'views/expense_views.xml',
        'views/dashboard_views.xml',
        'wizard/monthly_report_wizard.xml'
    ],

    'installable': True,
    'application': True,
}