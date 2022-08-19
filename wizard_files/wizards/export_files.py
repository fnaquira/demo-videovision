# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WizardFileSave(models.TransientModel):
	_name = 'wizard.file_save'
	_description = 'Asistente de archivos'

	output_name = fields.Char(string='Nombre de Salida', size=128)
	output_file = fields.Binary(string='Archivo de Salida', readonly=True, filename='output_name')