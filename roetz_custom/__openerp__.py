# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Opener B.V. (<https://opener.am>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Various customizations",
    "category": "Custom",
    "version": "8.0.1.1.0",
    "author": "Opener B.V.",
    "website": 'https://opener.am',
    "depends": [
        'web',
        'stock_account',
        'mrp',
        'payment_buckaroo',
        'payment_paypal',
        'sale_order_dates',
        'website_sale',
        'website_google_map',
        'website_crm_partner_assign',
    ],
    'data': [
        'views/product.xml',
        'views/sale_order.xml',
        'views/templates.xml',
    ],
}
