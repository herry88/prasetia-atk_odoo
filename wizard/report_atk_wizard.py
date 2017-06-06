from openerp import models, fields, api, _
from openerp.osv import orm
from openerp.exceptions import UserError
from datetime import datetime

class report_atk(orm.TransientModel):
	_name = "rekap.atk"
	_description = "Rekap ATK"

	report_type = fields.Selection(selection=[('Harian', 'Harian'),('Bulanan', 'Bulanan'), ('Tahunan', 'Tahunan')], required=True, string="Report Type", default="Bulanan")	
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
		records = self.env[data['model']].browse(data.get('ids',[]))
		# return self.env['report'].with_context(landscape=False).get_action(records,'prasetia.report_atk_prasetia', data=data)
		return self.env['report'].with_context(landscape=False).get_action(records,'prasetia.report_atk_prasetia', data=data)

	@api.multi
	def check_report(self):
		self.ensure_one()
		self_obj = self.env.context

		data = {}
		data['ids'] = self_obj.get('active_ids', [])
		data['model'] = self_obj.get('active_model', 'ir.ui.menu')
		data['form'] = self.read(['report_type','month_filter','year_filter','date_filter'])[0]
		return self._print_report(data)