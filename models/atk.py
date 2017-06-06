from openerp import models, fields, api
import datetime


class Departement(models.Model):
	_name = "atk.departement"

	name = fields.Char(required=True, string="Departement")

class company(models.Model):
	_name = "atk.company"

	name = fields.Char(required=True, string="Perusahaan")

class Employee(models.Model):
	_name = "atk.employee"

	name = fields.Char(required=True, string="Nama Karyawan")
	company_id = fields.Many2one('atk.company', string="Perusahaan", ondelete="set null", required=True)
	departement_id = fields.Many2one('atk.departement', string="Departement", ondelete="set null")
	StockIn_ids = fields.One2many('atk.stock.in', 'employee_id', string="Stock In")
	StockOut_ids = fields.One2many('atk.stock.out', 'employee_id', string="Stock Out")
	count_stockin_ids = fields.Integer(string="Transaksi Masuk", compute="_compute_count_stockin_ids")
	count_stockout_ids = fields.Integer(string="Transaksi Keluar", compute="_compute_count_stockout_ids")
	@api.one
	def _compute_count_stockin_ids(self):
		self.count_stockin_ids = 0
		if self.id:
			obj_stock_in = self.env['atk.stock.in']
			self.count_stockin_ids = obj_stock_in.search_count([('employee_id','=',self.id)])

	@api.one
	def _compute_count_stockout_ids(self):
		self.count_stockout_ids = 0
		if self.id:
			obj_stock_out = self.env['atk.stock.out']
			self.count_stockout_ids = obj_stock_out.search_count([('employee_id','=',self.id)])

class ItemCategory(models.Model):
	_name = "atk.item.category"

	name = fields.Char(required=True, string="Kategori")
	item_ids = fields.One2many('atk.item', 'item_category_id', string="Item List")


class Items(models.Model):
	_name = "atk.item"

	name = fields.Char(required=True, string="Nama Item")
	item_category_id = fields.Many2one('atk.item.category', string="Kategori", ondelete="set null", required=True)
	StockIn_ids = fields.One2many('atk.stock.in', 'item_id', string="Stock In")
	StockOut_ids = fields.One2many('atk.stock.out', 'item_id', string="Stock Out")
	count_stock = fields.Integer(string="Stok Tersisa", compute="_compute_count_stock")

	@api.one
	def _compute_count_stock(self):
		self.count_stock = 0
		if self.id:
			obj_stock_out = self.env['atk.stock.out']
			obj_stock_in = self.env['atk.stock.in']

			sum_stock_out = 0
			stock_out_datas = obj_stock_out.search([('item_id','=',self.id)])
			for data in stock_out_datas :
				sum_stock_out += data.qty
			# print '======================='
			# print sum_stock_out
			# print '======================='

			sum_stock_in = 0
			stock_in_datas = obj_stock_in.search([('item_id','=',self.id)])
			for data in stock_in_datas :
				sum_stock_in += data.qty
			# print '======================='
			# print sum_stock_in
			# print '======================='

			# print '================================'
			# print obj_stock_in.search_count([('item_id.id','=',self.id)])
			# print '================================'
			# print obj_stock_out.search_count([('item_id.id','=',self.id)])
			# print '================================'
			# self.count_stock = obj_stock_in.search_count([('item_id','=',self.id)]) - obj_stock_out.search_count([('item_id','=',self.id)])
			self.count_stock = sum_stock_in - sum_stock_out

class Transaction(models.Model):
	_name = "atk.transaction"

	name = fields.Date(required=True, string="Tanggal Transaksi")
	StockIn_ids = fields.One2many('atk.stock.in', 'transaction_id', string="Stock In")
	StockOut_ids = fields.One2many('atk.stock.out', 'transaction_id', string="Stock Out")
	count_stockin_ids = fields.Integer(string="Transaksi Masuk", compute="_compute_count_stockin_ids")
	count_stockout_ids = fields.Integer(string="Transaksi Keluar", compute="_compute_count_stockout_ids")
	date_transaction = fields.Char(string='Tgl Transaksi', size=64, readonly=True, compute="_get_date_transaction")

	_order = 'id desc'

	@api.one
	def _compute_count_stockin_ids(self):
		self.count_stockin_ids = 0
		if self.id:
			obj_stock_in = self.env['atk.stock.in']
			self.count_stockin_ids = obj_stock_in.search_count([('transaction_id','=',self.id)])

	@api.one
	def _compute_count_stockout_ids(self):
		self.count_stockout_ids = 0
		if self.id:
			obj_stock_out = self.env['atk.stock.out']
			self.count_stockout_ids = obj_stock_out.search_count([('transaction_id','=',self.id)])

	@api.one
	def _get_date_transaction(self):
		self.date_transaction = datetime.datetime.strptime(self.name, '%Y-%m-%d').strftime('%d %B %Y')

class UnitMeasure(models.Model):
	_name = "atk.uom"

	name = fields.Char(required=True, string="Kategori")


class StockIn(models.Model):
	_name = "atk.stock.in"

	transaction_id = fields.Many2one('atk.transaction', string="Tanggal", ondelete="set null", required=True)
	item_category_id = fields.Many2one('atk.item.category', string="Kategori", ondelete="set null", required=True)	
	item_id = fields.Many2one('atk.item', string="Nama Item", ondelete="set null", required=True)
	employee_id = fields.Many2one('atk.employee', string="Nama Karyawan", ondelete="set null", required=True)
	company_id = fields.Many2one('atk.company', string="Perusahaan", ondelete="set null", required=True)
	departement_id = fields.Many2one('atk.departement', string="Departement", ondelete="set null", required=True)
	unit_measure_id = fields.Many2one('atk.uom', string="Satuan", ondelete="set null", required=True)
	qty = fields.Integer(string="Quantity", required=True)
	price = fields.Float(string="Harga Satuan", required=True)
	remark = fields.Text(string="Keterangan")

class StockOut(models.Model):
	_name = "atk.stock.out"

	transaction_id = fields.Many2one('atk.transaction', string="Tanggal", ondelete="set null", required=True)
	item_category_id = fields.Many2one('atk.item.category', string="Kategori", ondelete="set null", required=True)	
	item_id = fields.Many2one('atk.item', string="Nama Item", ondelete="set null", required=True)
	employee_id = fields.Many2one('atk.employee', string="Nama Karyawan", ondelete="set null", required=True)
	company_id = fields.Many2one('atk.company', string="Perusahaan", ondelete="set null", required=True)
	departement_id = fields.Many2one('atk.departement', string="Departement", ondelete="set null", required=True)
	unit_measure_id = fields.Many2one('atk.uom', string="Satuan", ondelete="set null", required=True)
	qty = fields.Integer(string="Quantity", required=True)
	remark = fields.Text(string="Keterangan")

class StationaryRequest(models.Model):
	_name = "atk.stationary.request"

	nik = fields.Char(required=True, string="NIK")
	name = fields.Char(required=True, string="Nama Karyawan")
	queue = fields.Char(string="Queue")
	date_request = fields.Date(string="Tanggal Request", default=fields.Date.today)
	company_id = fields.Many2one('atk.company', string="Perusahaan", ondelete="set null", required=True)
	departement_id = fields.Many2one('atk.departement', string="Departement", ondelete="set null", required=True)
	stationary_request_line_ids = fields.One2many('atk.stationary.request.line', 'stationary_request_id',
												  string="List Request ATKs")
	state = fields.Selection([
		('draft', 'Draft'),
        ('submit', 'Waiting'),
        ('cancel', 'Cancel'),
        ('done','Done'),
    ], string="Status")
	
	@api.multi
	def action_draft(self):
		self.state = 'draft'
	
	@api.multi
	def action_submit(self):
		self.state = 'submit'

	@api.multi
	def action_cancel(self):
		self.state = 'cancel'

	@api.multi
	def action_done(self):
		self.state = 'done'
    
class StationaryRequestLine(models.Model):
	_name = "atk.stationary.request.line"

	stationary_request_id = fields.Many2one('atk.stationary.request', string="Stationary Request", ondelete="cascade", required=True)	
	item_category_id = fields.Many2one('atk.item.category', string="Kategori", ondelete="set null", required=True)	
	item_id = fields.Many2one('atk.item', string="Nama Item", ondelete="set null", required=True)
	qty = fields.Integer(string="Quantity", required=True)
	unit_measure_id = fields.Many2one('atk.uom', string="Satuan", ondelete="set null", required=True)
	qty_out = fields.Integer(string="Quantity Out")
	unit_measure_id_out = fields.Many2one('atk.uom', string="Satuan Out", ondelete="set null")
	remark = fields.Text(string="Keterangan")