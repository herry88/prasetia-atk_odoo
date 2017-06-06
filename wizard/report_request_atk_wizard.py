from datetime import datetime

from openerp import models, fields, api, _
from openerp.osv import orm

class report_request_atk(orm.TransientModel):
	_name = "rekap.request.atk"
	_description = "Rekap Request ATK"

	company_id = fields.Many2one('atk.company', string="Perusahaan", ondelete="set null", required=True)
	report_type = fields.Selection(selection=[('Harian', 'Harian'),('Bulanan', 'Bulanan'), ('Tahunan', 'Tahunan')],
								   required=True, string="Report Type", default="Bulanan")
	date_filter = fields.Date(string="Tanggal", default=datetime.now())
	month_filter = fields.Selection(selection=[
		(1, 'Januari'),
		(2, 'Februari'),
		(3, 'Maret'),
		(4, 'April'),
		(5, 'Mei'),
		(6, 'Juni'),
		(7, 'Juli'),
		(8, 'Agustus'),
		(9, 'September'),
		(10, 'Oktober'),
		(11, 'November'),
		(12, 'Desember')
		], string="Bulan")
	year_filter = fields.Integer(string="Tahun", default=datetime.now().year)

	def _print_report(self, data):
		records = self.env[data['model']].browse(data.get('ids', []))
		return self.env['report'].with_context(landscape=False).get_action(records,'prasetia.report_atk_request_prasetia', data=data)

	@api.multi
	def check_report(self):

		# TODO: For PDF Print
		# self.ensure_one()
		# self_obj = self.env.context
        #
		# data = {}
		# data['ids'] = self_obj.get('active_ids', [])
		# data['model'] = self_obj.get('active_model', 'ir.ui.menu')
		# data['form'] = self.read(['report_type', 'month_filter', 'year_filter', 'date_filter', 'company_id'])[0]
        #
		# return self._print_report(data)

		context = self._context
		datas = {'ids': context.get('active_ids', [])}
		datas['model'] = 'atk.stationary.request'
		datas['form'] = self.read()[0]
		datas['company_name'] = self.read()[0]['company_id'][1]
		for field in datas['form'].keys():
			if isinstance(datas['form'][field], tuple):
				datas['form'][field] = datas['form'][field][0]
		return {'type': 'ir.actions.report.xml',
				'report_name': 'prasetia.atk.xls.xlsx',
				'datas': datas,
				'name': 'Request ATK Report'
				}