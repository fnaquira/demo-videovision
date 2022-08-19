# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

import logging
log = logging.getLogger(__name__)

import base64

class WizardHrPrevired(models.TransientModel):
	_name = 'wizard.hr.previred'
	_description = 'Wizard Crear orden de compra desde listas de materiales'

	company_id = fields.Many2one(string='Compañia', comodel_name='res.company', required=True, default=lambda self: self.env.company.id)
	date_from = fields.Date('Desde', required=True)
	date_to = fields.Date('Hasta', required=True)

	def get_output_lines(self):
		lines = []
		# employees = {} # No se usa
		payslips = self.env['hr.payslip'].search([('state','=','done'),('date_from','>=',self.date_from),('date_to','>=',self.date_to)],order="employee_id asc")
		for payslip in payslips:
			# emp_id = str(payslip.employee_id.id) # No se usa

			# =================== APARTADO 1 - DATOS DEL TRABAJADOR (NRO 1 AL 25) ===================

			# rut = payslip.employee_id.identification_id
			rut = payslip.employee_id.identification_id[:-2]
			# dv = rut[:-1]
			dv = rut[-1:]
			#appat = payslip.employee_id.appat
			#appat = ''
			appat = payslip.employee_id.last_name
			#apmat = ''
			apmat = payslip.employee_id.mother_last_name if payslip.employee_id.mother_last_name else ''
			#nomb = payslip.employee_id.name
			nomb = payslip.employee_id.first_name
			gender = payslip.employee_id.gender[:1].upper() if payslip.employee_id.gender in ['male', 'female'] else 'M'
			country = '0' if payslip.employee_id.country_id.code == 'CL' else '1'
			# payment_type = 'Normal'
			payment_type = '01'
			# date_from = payslip.date_from
			_tmp_df = datetime.strftime(payslip.date_from, '%d-%m-%Y').split("-")
			date_from = _tmp_df[1] + _tmp_df[2]
			# date_to = payslip.date_to
			_tmp_dt = datetime.strftime(payslip.date_to, '%d-%m-%Y').split("-")
			date_to = _tmp_dt[1] + _tmp_dt[2]

			reg_previ = payslip.employee_id.contract_id.l10n_cl_pension_system if payslip.employee_id.contract_id.l10n_cl_pension_system else 'SIP'
			tipo_trab = payslip.employee_id.contract_id.l10n_cl_worker_type if payslip.employee_id.contract_id.l10n_cl_worker_type else '0'
			dias_trab = int(payslip.worked_days_line_ids.filtered(lambda wd: wd.name == 'Asistencia').number_of_days)
			tipo_linea = '00'
			cod_mov_pers = 0
			fecha_desde = datetime.strftime(payslip.employee_id.contract_id.date_start, '%d-%m-%Y') if payslip.employee_id.contract_id.date_start else ''
			fecha_hasta = datetime.strftime(payslip.employee_id.contract_id.date_end, '%d-%m-%Y') if payslip.employee_id.contract_id.date_end else ''
			tramo_asig_fam = 'Sin Información'
			nro_cargas_simp = ''
			nro_cargas_mater = ''
			nro_cargas_inval = ''
			asig_fam = 0.0
			asig_fam_retro = 0.0 # Aplica solo para empresas adheridas a CCAF
			reintegro_cargas_fam = 0.0 # Aplica solo para empresas adheridas a CCAF
			sol_trab_joven = 'N'

			result = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (rut,dv,appat,apmat,nomb,gender,country,payment_type,date_from,date_to,reg_previ,tipo_trab,dias_trab,tipo_linea,cod_mov_pers,fecha_desde,fecha_hasta,tramo_asig_fam,nro_cargas_simp,nro_cargas_mater,nro_cargas_inval,asig_fam,asig_fam_retro,reintegro_cargas_fam,sol_trab_joven)

			# =================== APARTADO 2 - DATOS DE LA AFP (NRO 26 AL 39) ===================

			# Prueba
			afp = payslip.employee_id.contract_id.afp_id.codigo if payslip.employee_id.contract_id.afp_id else '00'
			renta_imp_afp = payslip.line_ids.filtered(lambda line: line.code == 'PREV').total if payslip.line_ids.filtered(lambda line: line.code == 'PREV') else 0.0
			coti_obli_afp = 0.0
			coti_sis = 0.0
			cta_ahorro_volun_afp = 0.0
			renta_imp_susti_afp = 0.0
			tasa_pactada = ''
			aporte_indem = 0.0
			nro_periodos = 0
			periodo_desde = ''
			periodo_hasta = ''
			puesto_trab_pesado = ''
			porcen_cot_trab_pesado = ''
			cot_trab_pesado = 0.0

			result += ";%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (afp,renta_imp_afp,coti_obli_afp,coti_sis,cta_ahorro_volun_afp,renta_imp_susti_afp,tasa_pactada,aporte_indem,nro_periodos,periodo_desde,periodo_hasta,puesto_trab_pesado,porcen_cot_trab_pesado,cot_trab_pesado)

			# =================== APARTADO 3 - DATOS AHORRO PREVISIONAL VOLUNTARIO INDIVIDUAL (NRO 40 AL 44) ===================

			cod_inst_apvi = '0' + payslip.employee_id.contract_id.afp_id.codigo if payslip.employee_id.contract_id.afp_id else '000'
			nro_contra_apvi = ''
			forma_pago_apvi = 1
			coti_apvi = 0.0
			coti_depos_conve = 0.0

			result += ";%s;%s;%s;%s;%s" % (cod_inst_apvi,nro_contra_apvi,forma_pago_apvi,coti_apvi,coti_depos_conve)

			# =================== APARTADO 4 - DATOS AHORRO PREVISIONAL VOLUNTARIO COLECTIVO (NRO 45 AL 49) ===================

			cod_inst_autor_apvc = '0' + payslip.employee_id.contract_id.afp_id.codigo if payslip.employee_id.contract_id.afp_id else '000'
			nro_contra_apvc = ''
			forma_pago_apvc = 1
			coti_trab_apvc = 0.0
			coti_emple_apvc = 0.0

			result += ";%s;%s;%s;%s;%s" % (cod_inst_autor_apvc,nro_contra_apvc,forma_pago_apvc,coti_trab_apvc,coti_emple_apvc)

			# =================== APARTADO 5 - DATOS AFILIADO VOLUNTARIO (NRO 50 AL 61) ===================

			rut_afi_vol = ''
			dv_afi_vol = ''
			appat_vol = ''
			apmat_vol = ''
			nomb_vol = ''
			cod_mov_pers_vol = ''
			date_from_vol = ''
			date_to_vol = ''
			cod_afp_vol = ''
			monto_cap_volun = 0.0
			monto_ahorro_volun = 0.0
			num_peri_cot = 0

			result += ";%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (rut_afi_vol,dv_afi_vol,appat_vol,apmat_vol,nomb_vol,cod_mov_pers_vol,date_from_vol,date_to_vol,cod_afp_vol,monto_cap_volun,monto_ahorro_volun,num_peri_cot)

			# =================== APARTADO 6 - DATOS IPS - ISL - FONASA (NRO 62 AL 74) ===================

			cod_ex_caja_reg = ''
			tasa_cot_ex_caja_prev = ''
			renta_imp_ips = 0.0
			cot_obli_ips = 0.0
			renta_imp_desah = ''
			cod_ex_caja_reg_desah = ''
			tasa_cot_desah_ex_cajas_prev = ''
			cot_desah = 0.0
			cot_fonasa = payslip.line_ids.filtered(lambda line: line.code == 'FONASA').total if payslip.line_ids.filtered(lambda line: line.code == 'FONASA') else 0.0
			cot_acc_trab = 0.0
			bonif_ley = payslip.line_ids.filtered(lambda line: line.code == 'PROD').total if payslip.line_ids.filtered(lambda line: line.code == 'PROD') else 0.0
			desc_cargas_fam_ips = 0.0
			bonos_gob = 0.0

			result += ";%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (cod_ex_caja_reg,tasa_cot_ex_caja_prev,renta_imp_ips,cot_obli_ips,renta_imp_desah,cod_ex_caja_reg_desah,tasa_cot_desah_ex_cajas_prev,cot_desah,cot_fonasa,cot_acc_trab,bonif_ley,desc_cargas_fam_ips,bonos_gob)

			# =================== APARTADO 7 - DATOS SALUD (NRO 75 AL 82) ===================

			cod_inst_salud = payslip.employee_id.contract_id.isapre_id.codigo if payslip.employee_id.contract_id.isapre_id else '00'
			num_fun = payslip.employee_id.contract_id.l10n_cl_hr_isapre_fun if payslip.employee_id.contract_id.l10n_cl_hr_isapre_fun else '0'
			renta_imp_isapre = 0.0
			mon_plan_pac_isapre = 1
			cot_pac = 0.0
			cot_obli_isapre = 0.0
			cot_adi_isapre = 0.0
			monto_garan_expli_salud_GES = 0.0

			result += ";%s;%s;%s;%s;%s;%s;%s;%s" % (cod_inst_salud,num_fun,renta_imp_isapre,mon_plan_pac_isapre,cot_pac,cot_obli_isapre,cot_adi_isapre,monto_garan_expli_salud_GES)

			# =================== APARTADO 8 - DATOS CAJA DE COMPENSACION (NRO 83 AL 95) ===================

			cod_ccaf = ''
			renta_imp_ccaf = 0.0
			cred_perso_ccaf = 0.0
			desc_dental_ccaf = 0.0
			desc_leasing = 0.0
			desc_seguro_vida_ccaf = 0.0
			otros_desc_ccaf = 0.0
			cot_ccaf_no_afi_isapres = 0.0
			desc_cargas_fam_ccaf = 0.0
			otros_desc_ccaf_1 = 0.0
			otros_desc_ccaf_2 = 0.0
			bonos_gob_ccaf = 0.0
			cod_sucur = ''

			result += ";%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (cod_ccaf,renta_imp_ccaf,cred_perso_ccaf,desc_dental_ccaf,desc_leasing,desc_seguro_vida_ccaf,otros_desc_ccaf,cot_ccaf_no_afi_isapres,desc_cargas_fam_ccaf,otros_desc_ccaf_1,otros_desc_ccaf_2,bonos_gob_ccaf,cod_sucur)

			# =================== APARTADO 9 - DATOS MUTUALIDAD (NRO 96 AL 99) ===================

			cod_mutuali = '00'
			renta_imp_mutuali = 0.0
			cot_acc_trab_mutual = 0.0
			sucur_pago_mutuali = ''

			result += ";%s;%s;%s;%s" % (cod_mutuali,renta_imp_mutuali,cot_acc_trab_mutual,sucur_pago_mutuali)

			# =================== APARTADO 10 - DATOS ADMINISTRADORA DE SEGURO DE CESANTIA (NRO 100 AL 102) ===================

			renta_imp_seguro_cesantia = payslip.line_ids.filtered(lambda line: line.code == 'SECE').total if payslip.line_ids.filtered(lambda line: line.code == 'SECE') else 0.0
			aporte_trab_seguro_cesantia = 0.0
			aporte_emple_seguro_cesantia = 0.0

			result += ";%s;%s;%s" % (renta_imp_seguro_cesantia,aporte_trab_seguro_cesantia,aporte_emple_seguro_cesantia)

			# =================== APARTADO 11 - DATOS PAGADOR DE SUBSIDIOS (NRO 103 AL 104) ===================

			# emp_subsidios {
			# 	1: ['96572800-7', 'Banmédica'],
			# 	2: ['96856780-2', 'Consalud'],
			# 	3: ['96502530-8', 'Vida Tres'],
			# 	4: ['76296619-0', 'Colmena'],
			# 	5: ['96501450-0', 'Isapre Cruz Blanca S.A.'],
			# 	6: ['96936100-0', 'Esencial'],
			# 	7: ['61603000-0', 'Fonasa'],
			# 	8: ['96504160-5', 'Nueva Masvida'],
			# 	9: ['76334370-7', 'Isapre de Codelco Ltda.'],
			# 	10: ['71235700-2', 'Isapre Banco Estado'],
			# 	11: ['79906120-1', 'Cruz del Norte'],
			# 	12: ['70360100-6', 'Asociación Chilena de Seguridad (ACHS)'],
			# 	13: ['70285100-9', 'Mutual de Seguridad CCHC'],
			# 	14: ['70015580-3', 'Instituto de Seguridad del Trabajo I.S.T'],
			# 	15: ['61533000-0', 'Instituto de Seguridad Laboral I.S.L.']
			# }

			rut_pagadora_subsi = ''
			dv_pagadora_subsi = ''

			result += ";%s;%s" % (rut_pagadora_subsi,dv_pagadora_subsi)

			# =================== APARTADO 12 - DATOS OTROS DATOS DE LA EMPRESA (NRO 105) ===================

			centro_costos = ''

			result += ";%s" % (centro_costos)

			#verificacion de primera linea
			# first_line = '0' # No se usa
			# if emp_id in employees: # No se usa
			# 	first_line = '1' # No se usa
			# result = '%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' % (rut,dv,appat,apmat,nomb,gender,country,payment_type,date_from,date_to)
			lines.append(result)
		return lines

	def create_previred_txt(self):
		FileSave = self.env['wizard.file_save']
		for record in self:
			if record.date_from == record.date_to:
				raise UserError('La fecha de inicio no puede ser igual a la fecha de fin')
			if record.date_from > record.date_to:
				raise UserError('La fecha de inicio no puede ser mayor a la fecha de fin')

			encoded_lines = [l.encode('utf-8') for l in record.get_output_lines()]
			encoded_output_file = base64.b64encode(b'\r\n'.join(encoded_lines))
			period_str = str(record.date_from).split('-')
			file_name = 'PREVIRED_'+str(record.company_id.vat)+'_'+str(period_str[0])+str(period_str[1])+'.txt'

			vals = {
				'output_name': file_name,
				'output_file': encoded_output_file or '===',
			}
			sfs_id = FileSave.create(vals)
			
			return {
				'name': "Guardar Archivo de Salida",
				'view_mode': 'form',
				'view_type': 'form',
				'res_model': 'wizard.file_save',
				'res_id': sfs_id.id,
				'type': 'ir.actions.act_window',
				'nodestroy': True,
				'target': 'new',
				'domain': "",
				'context': dict(self._context)
			}