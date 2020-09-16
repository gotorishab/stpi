# -*- coding: utf-8 -*-
###################################################################################
#    A part of OpenHRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Anusha P P (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Loan Close - STPI',
    'version': '12.0.2.0.0',
    'summary': 'Manage Loan Requests closing Loans',
    'description': """
        Helps you to manage Loan Requests of your company's staff and for Closing the Loan Amount.
        """,
    'category': 'Human Resources',
    'author': "RGupta(Dexciss Technology Pvt. Ltd,Pune)",
    'company': 'Dexciss Technology Pvt. Ltd,Pune',
    'maintainer': 'Dexciss Technology Pvt. Ltd,Pune',
    'website': "https://www.dexciss.com",
    'depends': [
        'base', 'ohrms_loan'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/multi_approve.xml',
        'views/loan_close.xml'
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
