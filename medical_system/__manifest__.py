{
    'name': 'Medical System',
    'version': '1.0',
    'summary': 'medical system for paitents',
    'category': 'Tools',
    'author': 'Nayera',

    'depends': ['base','expense_tracker'],

    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/clinic_views.xml',
        'views/appointment_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/res_appointment_views.xml'
    ],

    'installable': True,
    'application': True,
}