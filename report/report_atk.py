from openerp import api, models

class ReportAtk(models.AbstractModel):
	_name = 'report.prasetia.report_atk_prasetia'

	def query_stock_remaining(self,condition):
		query = """
					SELECT
					"public".atk_item."id" as item_id,
					COALESCE("c".qty_in,0) - COALESCE("d".qty_out,0) as stock_remaining
					FROM
					"public".atk_item
					LEFT JOIN (
						SELECT
							"public".atk_item."id" AS item_id,
							SUM ("public".atk_stock_in.qty) AS qty_in
						FROM
							"public".atk_transaction
						LEFT JOIN "public".atk_stock_in ON "public".atk_transaction."id" = "public".atk_stock_in.transaction_id
						LEFT JOIN "public".atk_item ON "public".atk_stock_in.item_id = "public".atk_item."id"
						WHERE
							%s
						GROUP BY
							"public".atk_item."id"
					) AS "c" ON "public".atk_item."id" = "c".item_id
					LEFT JOIN (
						SELECT
							"public".atk_item."id" AS item_id,
							SUM ("public".atk_stock_out.qty) AS qty_out
						FROM
							"public".atk_transaction
						LEFT JOIN "public".atk_stock_out ON "public".atk_transaction."id" = "public".atk_stock_out.transaction_id
						LEFT JOIN "public".atk_item ON "public".atk_stock_out.item_id = "public".atk_item."id"
						WHERE
							%s
						GROUP BY
							"public".atk_item."id"
					) AS d ON "public".atk_item."id" = "d".item_id
					LEFT JOIN "public".atk_item_category ON
					"public".atk_item.item_category_id = "public".atk_item_category."id"
					WHERE
					"d".qty_out IS NOT NULL OR
					"c".qty_in IS NOT NULL
				""" % (condition,condition)
		return query

	def query_tahunan(self,data):
		stock_remaining_condition = """
									"public".atk_transaction."name" <= '%s'
									""" % (str(data.get('year_filter'))+"-12-31")

		query = """
				SELECT
				"public".atk_item."id",
				"public".atk_item."name",
				"public".atk_item_category."name" as "category_name",
				COALESCE("c".qty_in,0) as qty_in,
				COALESCE("d".qty_out,0) as qty_out,
				COALESCE("e".stock_remaining,0) as stock_remaining
				FROM
				"public".atk_item
				LEFT JOIN (
					SELECT
						"public".atk_item."id" AS item_id,
						SUM ("public".atk_stock_in.qty) AS qty_in
					FROM
						"public".atk_transaction
					LEFT JOIN "public".atk_stock_in ON "public".atk_transaction."id" = "public".atk_stock_in.transaction_id
					LEFT JOIN "public".atk_item ON "public".atk_stock_in.item_id = "public".atk_item."id"
					WHERE
						EXTRACT(YEAR FROM "public".atk_transaction."name") = """+ str(data.get('year_filter')) +"""
					GROUP BY
						"public".atk_item."id"
				) AS "c" ON "public".atk_item."id" = "c".item_id
				LEFT JOIN (
					SELECT
						"public".atk_item."id" AS item_id,
						SUM ("public".atk_stock_out.qty) AS qty_out
					FROM
						"public".atk_transaction
					LEFT JOIN "public".atk_stock_out ON "public".atk_transaction."id" = "public".atk_stock_out.transaction_id
					LEFT JOIN "public".atk_item ON "public".atk_stock_out.item_id = "public".atk_item."id"
					WHERE
						EXTRACT(YEAR FROM "public".atk_transaction."name") = """+ str(data.get('year_filter')) +"""
					GROUP BY
						"public".atk_item."id"
				) AS d ON "public".atk_item."id" = "d".item_id
				LEFT JOIN "public".atk_item_category ON
				"public".atk_item.item_category_id = "public".atk_item_category."id"
				LEFT JOIN (%s) as e ON
				"public".atk_item."id" = "e".item_id
				WHERE
				"d".qty_out IS NOT NULL OR
				"c".qty_in IS NOT NULL
				ORDER BY
				category_name ASC,
				"public".atk_item."name" ASC
				""" % (self.query_stock_remaining(stock_remaining_condition))
		return query

	def query_bulanan(self,data):
		month_converter = { 1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31 }

		month_vals = 0		
		if data.get('month_filter'):
			if(data.get('month_filter') == 2):
				month_vals = 29 if (data.get('year_filter')%4 == 0) else 28
			else :
				month_vals = month_converter[data.get('month_filter')]
		

		stock_remaining_condition = """
									"public".atk_transaction."name" <= '%s'
									""" % (str(data.get('year_filter'))+"-"+str(data.get('month_filter'))+"-"+ str(month_vals))

		query = """
				SELECT
				"public".atk_item."id",
				"public".atk_item."name",
				"public".atk_item_category."name" as "category_name",
				COALESCE("c".qty_in,0) as qty_in,
				COALESCE("d".qty_out,0) as qty_out,
				COALESCE("e".stock_remaining,0) as stock_remaining
				FROM
				"public".atk_item
				LEFT JOIN (
					SELECT
						"public".atk_item."id" AS item_id,
						SUM ("public".atk_stock_in.qty) AS qty_in
					FROM
						"public".atk_transaction
					LEFT JOIN "public".atk_stock_in ON "public".atk_transaction."id" = "public".atk_stock_in.transaction_id
					LEFT JOIN "public".atk_item ON "public".atk_stock_in.item_id = "public".atk_item."id"
					WHERE
						EXTRACT(MONTH FROM "public".atk_transaction."name") = """+ str(data.get('month_filter')) +""" AND
						EXTRACT(YEAR FROM "public".atk_transaction."name") = """+ str(data.get('year_filter')) +"""
					GROUP BY
						"public".atk_item."id"
				) AS "c" ON "public".atk_item."id" = "c".item_id
				LEFT JOIN (
					SELECT
						"public".atk_item."id" AS item_id,
						SUM ("public".atk_stock_out.qty) AS qty_out
					FROM
						"public".atk_transaction
					LEFT JOIN "public".atk_stock_out ON "public".atk_transaction."id" = "public".atk_stock_out.transaction_id
					LEFT JOIN "public".atk_item ON "public".atk_stock_out.item_id = "public".atk_item."id"
					WHERE
						EXTRACT(MONTH FROM "public".atk_transaction."name") = """+ str(data.get('month_filter')) +""" AND
						EXTRACT(YEAR FROM "public".atk_transaction."name") = """+ str(data.get('year_filter')) +"""
					GROUP BY
						"public".atk_item."id"
				) AS d ON "public".atk_item."id" = "d".item_id
				LEFT JOIN "public".atk_item_category ON
				"public".atk_item.item_category_id = "public".atk_item_category."id"
				LEFT JOIN (%s) as e ON
				"public".atk_item."id" = "e".item_id
				WHERE
				"d".qty_out IS NOT NULL OR
				"c".qty_in IS NOT NULL
				ORDER BY
				category_name ASC,
				"public".atk_item."name" ASC
				""" % (self.query_stock_remaining(stock_remaining_condition))
		return query

	def query_harian(self,data):
		stock_remaining_condition = """
									"public".atk_transaction."name" <= '%s'
									""" % (str(data.get('date_filter')))

		query = """
				SELECT
				"public".atk_item."id",
				"public".atk_item."name",
				"public".atk_item_category."name" as "category_name",
				COALESCE("c".qty_in,0) as qty_in,
				COALESCE("d".qty_out,0) as qty_out,
				COALESCE("e".stock_remaining,0) as stock_remaining
				FROM
				"public".atk_item
				LEFT JOIN (
					SELECT
						"public".atk_item."id" AS item_id,
						SUM ("public".atk_stock_in.qty) AS qty_in
					FROM
						"public".atk_transaction
					LEFT JOIN "public".atk_stock_in ON "public".atk_transaction."id" = "public".atk_stock_in.transaction_id
					LEFT JOIN "public".atk_item ON "public".atk_stock_in.item_id = "public".atk_item."id"
					WHERE
						"public".atk_transaction."name" = '"""+ str(data.get('date_filter')) +"""'
					GROUP BY
						"public".atk_item."id"
				) AS "c" ON "public".atk_item."id" = "c".item_id
				LEFT JOIN (
					SELECT
						"public".atk_item."id" AS item_id,
						SUM ("public".atk_stock_out.qty) AS qty_out
					FROM
						"public".atk_transaction
					LEFT JOIN "public".atk_stock_out ON "public".atk_transaction."id" = "public".atk_stock_out.transaction_id
					LEFT JOIN "public".atk_item ON "public".atk_stock_out.item_id = "public".atk_item."id"
					WHERE
						"public".atk_transaction."name" = '"""+ str(data.get('date_filter')) +"""'
					GROUP BY
						"public".atk_item."id"
				) AS d ON "public".atk_item."id" = "d".item_id
				LEFT JOIN "public".atk_item_category ON
				"public".atk_item.item_category_id = "public".atk_item_category."id"
				LEFT JOIN (%s) as e ON
				"public".atk_item."id" = "e".item_id
				WHERE
				"d".qty_out IS NOT NULL OR
				"c".qty_in IS NOT NULL
				ORDER BY
				category_name ASC,
				"public".atk_item."name" ASC
				""" % (self.query_stock_remaining(stock_remaining_condition))
		return query		

	def _get_atk_list(self, data):
		lines = []

		process_report = {
			'Tahunan' : self.query_tahunan(data),
           	'Harian' : self.query_harian(data),
           	'Bulanan' : self.query_bulanan(data)
           	}
		
		query = process_report[data.get('report_type')]
		self.env.cr.execute(query)
		res = self.env.cr.dictfetchall()
		for r in res :
			lines.append(r)
		return lines

	def _get_atk_datas(self,data):
		atk_transaction_obj = self.env['atk.transaction']		
		datas = atk_transaction_obj.search([('id','=',2017)])
		return datas

	@api.multi
	def render_html(self,data):
		self.model = self.env.context.get('active_model')
		docs = self.env[self.model].browse(self.env.context.get('active_ids',[]))

		atk_list = self._get_atk_list(data.get('form'))	

		docargs = {
			'doc_ids' : self.ids,
			'doc_model' : self.model,
			'data' : data['form'],
			'docs' : docs,
			'atk_list' : atk_list,
			'report_type': data.get('form').get('report_type'),
			'date_filter' : data.get('form').get('date_filter'),
			'bulan_filter' : data.get('form').get('month_filter'),
			'tahun_filter' : data.get('form').get('year_filter'),
			'transactions' : self._get_atk_list(data.get('form'))
		}

		return self.env['report'].render('prasetia.report_atk_prasetia', docargs)