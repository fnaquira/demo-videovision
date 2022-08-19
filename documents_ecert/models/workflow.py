# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import logging
import requests

url_gestdoc_create = 'https://flow.gestdoc.cl/api/documento'
url_gestdoc_upload = 'https://flow.gestdoc.cl/api/documento/upload'
url_gestdoc_update = 'https://flow.gestdoc.cl/api/documento'
headers = {
	'Content-Type': 'application/json'
}

class WorkflowActionRule(models.Model):
	_inherit = "documents.workflow.rule"

	ecert_valid = fields.Boolean(string='Genera validación E-cert', default=False, required=True)
	ecert_bpmn = fields.Char(string='ID de BPMN a utilizar', default='')
	ecert_interface = fields.Char(string='ID de interfaz a utilizar', default='')

	def apply_actions(self, document_ids):
		res = super(WorkflowActionRule, self).apply_actions(document_ids=document_ids)
		if self.ecert_valid:
			if self.ecert_bpmn == '':
				raise UserError('Debe configurar el BPMN a utilizar en la acción')
			if self.ecert_interface == '':
				raise UserError('Debe configurar la interfaz de conexión a utilizar en la acción')
			if len(document_ids) != 1:
				raise UserError('Solamente puede validar en E-cert un documento a la vez')
			documents = self.env['documents.document'].browse(document_ids)
			for document in documents:
				is_pdf = True if document.name[-3:] == 'pdf' else False
				if is_pdf == False:
					raise UserError('Debe enviar un PDF a validar')
				
				ir_action = self.sudo().env['ir.actions.actions'].search([('binding_type','=','action'),
					('type','=','ir.actions.act_window'),
					('name','=','Documents')])
				url_system = self.sudo().env['ir.config_parameter'].search([('key','=','web.base.url')])
				returl_url = '%s/web#action=%s&model=documents.document&view_type=kanban' % (url_system.value, ir_action.id)

				try:
					r = requests.post(url_gestdoc_create, json={
						'bpmn': self.ecert_bpmn,
						'returnData': {
							'url': returl_url,
							'res': document.id,
							'interface': self.ecert_interface
						}
					}, headers=headers)
					if not r.json()['_id']:
						return False
					response = r.json()
				except Exception as e:
					logging.info("exeption 1.1 {}".format(e))
				except requests.exceptions.RequestException as e:
					logging.info("exeption 1.2 {}".format(e))

				procedure_id = response['id']
				current_stage = response['gestores'][0]['current']
				document.write({
					'gestdoc_valid': True,
					'gestdoc_url': procedure_id
				})
				
				file_content = base64.b64decode(document.attachment_id.datas)
				try:
					r = requests.post('%s/%s' % (url_gestdoc_upload, procedure_id), files={
						'file': file_content
					})
					if not r.json()['url']:
						return False
					new_response = r.json()
				except Exception as e:
					logging.info("exeption 1.1 {}".format(e))
				except requests.exceptions.RequestException as e:
					logging.info("exeption 1.2 {}".format(e))
				
				aws_url = new_response['url']
				try:
					r = requests.put('%s/%s' % (url_gestdoc_update, procedure_id), json={
						'data': {
							'type': 'upload',
							'titleStage': 'Subida personalizada desde Odoo',
							'notification': False,
							'upload': aws_url
						},
						'current': current_stage
					}, headers=headers)
					if not r.json()['id']:
						return False
					last_response = r.json()
				except Exception as e:
					logging.info("exeption 1.1 {}".format(e))
				except requests.exceptions.RequestException as e:
					logging.info("exeption 1.2 {}".format(e))
				logging.info(last_response)
			
			return {
				'name'     : 'Go to website',
				'res_model': 'ir.actions.act_url',
				'type'     : 'ir.actions.act_url',
				'target'   : 'new',
				'url'      : 'https://flow.gestdoc.cl/procedure/%s' % (procedure_id)
			}
		return res