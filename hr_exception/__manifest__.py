# -*- coding: utf-8 -*-
# © 2011 Raphaël Valyi, Renato Lima, Guewen Baconnier, Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{'name': 'Hr Exception',
 'summary': 'Custom exceptions on Hr',
 'version': '14.0.1',
 'category': 'Generic Module',

'author': "Dexciss Technology Pvt Ltd(RGupta)",
 'website': 'http://www.Dexciss.com',
 'depends': ['hr','base_exception_and_approval','health_portal'],
 'license': 'AGPL-3',
'description':"""
                Created by rgupta 18/12/20 add Exception
                 """,
 'data': [
          'security/ir.model.access.csv',
          'view/hr_leave_view.xml',
          'wizard/hr_leave_wizard_view.xml',
 ],
 'images': [],
 'installable': True,
 }
