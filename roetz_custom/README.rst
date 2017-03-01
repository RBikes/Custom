Various customizations for Roetz-bikes
======================================
This module contains legacy customizations for Roetz-bikes that have been
picked from a manually altered source code tree of Odoo.

* Allows move lines from various partners to be reconciled so that customer invoices can be reconciled with payments from a payment provider
* Allow date_planned on a production order to be modified after modification (reference purpose only)
? Tweak buckaroo return urls using hardcoded domain
? Filter out certain fields from buckaroo response (e.g. Brq_amount, Brq_returncancel, Brq_returnerror)
? Don't fetch return url from response but based on response status code.
* Add 'new commitment date' field on sale orders
* Change the computation of the commitment date to reflect the biggest lead time of all sold products instead of the smallest lead time
* Show sale order dates in the top right corner of the sale order form grid
* Load Google maps javascript interface code from custom module
