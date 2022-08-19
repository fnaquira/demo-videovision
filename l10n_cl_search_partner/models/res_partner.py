# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

import requests
import json

import logging
log = logging.getLogger(__name__)

URL = 'https://siichile.herokuapp.com/consulta'


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('vat')
    def _onchange_search_by_vat(self):
        if not self.vat or self.vat == '' or self.l10n_latam_identification_type_id.name != 'RUT':
            return
        vat = self.vat
        vat = vat.replace('.','')
        if len(vat) >= 10:
            vat_parts = vat.split('-')
            if len(vat_parts) == 2:
                rut, dv = vat_parts[0], vat_parts[1]
                result = self.cl_search_data_vat(self.vat)
                if result[0]:
                    data = json.loads(result[1].decode())
                    self.name = data.get('razon_social', data.get('error', ''))


    def cl_search_data_vat(self, vat, url=URL):
        vat = vat.replace('.','')
        vat_parts = vat.split('-')
        if len(vat_parts) != 2:
            return (False, 0)
        rut, dv = vat_parts[0], vat_parts[1]
        session = requests.Session()
        try:
            send_url = "%s?rut=%s-%s" % (url, rut, dv)
            response = session.get(send_url)
        except requests.exceptions.RequestException as e:
            return (False, e)
        if response.status_code == 200:
            return (True, response.content)
