# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

class DocumentsDocument(models.Model):
	_inherit = "documents.document"

	gestdoc_valid = fields.Boolean(string='PDF enviado a Gestdoc', default=False, required=True)
	gestdoc_url = fields.Char(string='ID de Gestdoc para validación')

	@api.model
	def ecert_upd_pdf(self, res_id, file_content):
		document = self.sudo().browse(int(res_id))
		if document == False:
			raise UserError('El ID de documento es invalido')
		document.attachment_id.write({
			'datas': file_content
		})
		return True