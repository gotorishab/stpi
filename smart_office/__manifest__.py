# -*- coding: utf-8 -*-
{
    'name': "Smart Office",

    'summary': """
            Smart Office
             """,

    'description': """
        Smart Office
    """,

    'author': "Sachin Burnawal",
    'website': "https://theerpstore.com/",
    'category': 'Smart Office',
    'version': '0.1',

    'depends': ['mail', 'muk_dms', 'muk_dms_actions', ],

    'data': [
        'data/data.xml',
        # 'views/load_ifrme_widget.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'data/doc_receive_type.xml',
        'data/dem_file.xml',
        # 'security/ir_rule.xml',
        'wizard/filewizard.xml',
        'wizard/folderwizard.xml',
        'wizard/pull_into.xml',
        'wizard/outgoing_letters.xml',
        'wizard/incoming_letters.xml',
        'wizard/create_folder_wizard.xml',
        'views/file_tracking_information.xml',
        'views/add_letter.xml',
        'views/in_out_letter_view.xml',
        # 'views/letters_view.xml',
        'views/add_files.xml',
        'views/folder.xml',
        'views/files_view.xml',
        'views/wizard.xml',
        'views/templates.xml',
        'views/master.xml',
        'views/see_file.xml',
        'views/outgoing_files.xml',
        'views/incoming_files.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [
    ],
    # 'installable': True,
    'application': True,
}
