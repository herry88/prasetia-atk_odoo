from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx

class report_atk_xls(ReportXlsx):
    format_prasetia_header_table_center = None
    format_prasetia_data_table = None
    format_prasetia_1 = None

    def query_tahunan(self, company_id, year):
        query = """
            SELECT
            "public".atk_stationary_request.date_request,
            "public".atk_stationary_request.nik,
            "public".atk_stationary_request."name",
            "public".atk_departement."name" AS departement_name,
            "public".atk_item_category."name" AS category_name,
            "public".atk_item."name" AS item_name,
            "public".atk_stationary_request_line.qty_out,
            "public".atk_uom."name" AS uom
            FROM
            "public".atk_stationary_request_line
            LEFT JOIN "public".atk_stationary_request ON "public".atk_stationary_request_line.stationary_request_id = "public".atk_stationary_request."id"
            LEFT JOIN "public".atk_departement ON "public".atk_stationary_request.departement_id = "public".atk_departement."id"
            LEFT JOIN "public".atk_item_category ON "public".atk_stationary_request_line.item_category_id = "public".atk_item_category."id"
            LEFT JOIN "public".atk_item ON "public".atk_stationary_request_line.item_id = "public".atk_item."id"
            LEFT JOIN "public".atk_uom ON "public".atk_stationary_request_line.unit_measure_id_out = "public".atk_uom."id"
            WHERE
            "public".atk_stationary_request.company_id = %d AND
            EXTRACT(YEAR FROM "public".atk_stationary_request.date_request) = %s AND
            "public".atk_stationary_request."state" = 'done'
        """ % (company_id, year)
        return query

    def query_bulanan(self, company_id, year, month):
        month_converter = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

        month_vals = 0
        if month:
            if month == 2:
                month_vals = 29 if (year % 4 == 0) else 28
            else:
                month_vals = month_converter[month]

        query = """
            SELECT
            "public".atk_stationary_request.date_request,
            "public".atk_stationary_request.nik,
            "public".atk_stationary_request."name",
            "public".atk_departement."name" AS departement_name,
            "public".atk_item_category."name" AS category_name,
            "public".atk_item."name" AS item_name,
            "public".atk_stationary_request_line.qty_out,
            "public".atk_uom."name" AS uom
            FROM
            "public".atk_stationary_request_line
            LEFT JOIN "public".atk_stationary_request ON "public".atk_stationary_request_line.stationary_request_id = "public".atk_stationary_request."id"
            LEFT JOIN "public".atk_departement ON "public".atk_stationary_request.departement_id = "public".atk_departement."id"
            LEFT JOIN "public".atk_item_category ON "public".atk_stationary_request_line.item_category_id = "public".atk_item_category."id"
            LEFT JOIN "public".atk_item ON "public".atk_stationary_request_line.item_id = "public".atk_item."id"
            LEFT JOIN "public".atk_uom ON "public".atk_stationary_request_line.unit_measure_id_out = "public".atk_uom."id"
            WHERE
            "public".atk_stationary_request.company_id = %d AND
            EXTRACT(MONTH FROM "public".atk_stationary_request.date_request) = %s AND
            EXTRACT(YEAR FROM "public".atk_stationary_request.date_request) = %s AND
            "public".atk_stationary_request."state" = 'done'
        """ % (company_id, month, year)
        return query

    def query_harian(self, company_id, date):
        query = """
            SELECT
            "public".atk_stationary_request.date_request,
            "public".atk_stationary_request.nik,
            "public".atk_stationary_request."name",
            "public".atk_departement."name" AS departement_name,
            "public".atk_item_category."name" AS category_name,
            "public".atk_item."name" AS item_name,
            "public".atk_stationary_request_line.qty_out,
            "public".atk_uom."name" AS uom
            FROM
            "public".atk_stationary_request_line
            LEFT JOIN "public".atk_stationary_request ON "public".atk_stationary_request_line.stationary_request_id = "public".atk_stationary_request."id"
            LEFT JOIN "public".atk_departement ON "public".atk_stationary_request.departement_id = "public".atk_departement."id"
            LEFT JOIN "public".atk_item_category ON "public".atk_stationary_request_line.item_category_id = "public".atk_item_category."id"
            LEFT JOIN "public".atk_item ON "public".atk_stationary_request_line.item_id = "public".atk_item."id"
            LEFT JOIN "public".atk_uom ON "public".atk_stationary_request_line.unit_measure_id_out = "public".atk_uom."id"
            WHERE
            "public".atk_stationary_request.company_id = %d AND
            "public".atk_stationary_request.date_request = '%s' AND
            "public".atk_stationary_request."state" = 'done'
        """ % (company_id, date)
        return query

    def query_tahunan_stock_in(self, company_id, year):
        query = """
            SELECT
            "public".atk_transaction."name" AS tanggal,
            "public".atk_employee."name" AS employee_name,
            "public".atk_departement."name" AS dept_name,
            "public".atk_item_category."name" AS category_name,
            "public".atk_item."name" AS item_name,
            "public".atk_stock_in.qty,
            "public".atk_uom."name" AS uom
            FROM
            "public".atk_stock_in
            LEFT JOIN "public".atk_transaction ON "public".atk_stock_in.transaction_id = "public".atk_transaction."id"
            LEFT JOIN "public".atk_employee ON "public".atk_stock_in.employee_id = "public".atk_employee."id"
            LEFT JOIN "public".atk_departement ON "public".atk_stock_in.departement_id = "public".atk_departement."id"
            LEFT JOIN "public".atk_item_category ON "public".atk_stock_in.item_category_id = "public".atk_item_category."id"
            INNER JOIN "public".atk_item ON "public".atk_stock_in.item_id = "public".atk_item."id"
            LEFT JOIN "public".atk_uom ON "public".atk_stock_in.unit_measure_id = "public".atk_uom."id"
            WHERE
            "public".atk_stock_in.company_id = %d AND
            EXTRACT(YEAR FROM "public".atk_transaction."name") = %s
        """ % (company_id, year)
        return query

    def query_bulanan_stock_in(self, company_id, year, month):
        query = """
                    SELECT
                    "public".atk_transaction."name" AS tanggal,
                    "public".atk_employee."name" AS employee_name,
                    "public".atk_departement."name" AS dept_name,
                    "public".atk_item_category."name" AS category_name,
                    "public".atk_item."name" AS item_name,
                    "public".atk_stock_in.qty,
                    "public".atk_uom."name" AS uom
                    FROM
                    "public".atk_stock_in
                    LEFT JOIN "public".atk_transaction ON "public".atk_stock_in.transaction_id = "public".atk_transaction."id"
                    LEFT JOIN "public".atk_employee ON "public".atk_stock_in.employee_id = "public".atk_employee."id"
                    LEFT JOIN "public".atk_departement ON "public".atk_stock_in.departement_id = "public".atk_departement."id"
                    LEFT JOIN "public".atk_item_category ON "public".atk_stock_in.item_category_id = "public".atk_item_category."id"
                    INNER JOIN "public".atk_item ON "public".atk_stock_in.item_id = "public".atk_item."id"
                    LEFT JOIN "public".atk_uom ON "public".atk_stock_in.unit_measure_id = "public".atk_uom."id"
                    WHERE
                    "public".atk_stock_in.company_id = %d AND
                    EXTRACT(MONTH FROM "public".atk_transaction."name") = %s AND
                    EXTRACT(YEAR FROM "public".atk_transaction."name") = %s
                """ % (company_id, month, year)
        return query

    def query_harian_stock_in(self, company_id, date):
        query = """
                    SELECT
                    "public".atk_transaction."name" AS tanggal,
                    "public".atk_employee."name" AS employee_name,
                    "public".atk_departement."name" AS dept_name,
                    "public".atk_item_category."name" AS category_name,
                    "public".atk_item."name" AS item_name,
                    "public".atk_stock_in.qty,
                    "public".atk_uom."name" AS uom
                    FROM
                    "public".atk_stock_in
                    LEFT JOIN "public".atk_transaction ON "public".atk_stock_in.transaction_id = "public".atk_transaction."id"
                    LEFT JOIN "public".atk_employee ON "public".atk_stock_in.employee_id = "public".atk_employee."id"
                    LEFT JOIN "public".atk_departement ON "public".atk_stock_in.departement_id = "public".atk_departement."id"
                    LEFT JOIN "public".atk_item_category ON "public".atk_stock_in.item_category_id = "public".atk_item_category."id"
                    INNER JOIN "public".atk_item ON "public".atk_stock_in.item_id = "public".atk_item."id"
                    LEFT JOIN "public".atk_uom ON "public".atk_stock_in.unit_measure_id = "public".atk_uom."id"
                    WHERE
                    "public".atk_stock_in.company_id = %d AND
                    "public".atk_transaction."name" = '%s'
                """ % (company_id, date)
        return query

    def query_stock_remaining(self, condition, condition_request):
        query = """
    				SELECT
    				"public".atk_item."id" as item_id,
    				COALESCE("c".qty_in,0) - COALESCE("d".qty_out,0) - COALESCE("e".qty_approved,0) as stock_remaining
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
    				LEFT JOIN (
                        SELECT
                        "public".atk_stationary_request_line.item_id,
                        Sum("public".atk_stationary_request_line.qty_out) AS qty_approved
                        FROM
                        "public".atk_stationary_request_line
                        LEFT JOIN "public".atk_stationary_request ON "public".atk_stationary_request_line.stationary_request_id = "public".atk_stationary_request."id"
                        WHERE
                          %s
                        GROUP BY
                        "public".atk_stationary_request_line.item_id
    				) AS e ON "public".atk_item."id" = "e".item_id
    				LEFT JOIN "public".atk_item_category ON
    				"public".atk_item.item_category_id = "public".atk_item_category."id"
    				WHERE
    				"d".qty_out IS NOT NULL OR
    				"c".qty_in IS NOT NULL
    			""" % (condition, condition, condition_request)
        return query

    def query_tahunan_sisa_stock(self, year):
        stock_remaining_condition = """
                                    "public".atk_transaction."name" <= '%s'
                                    """ % (str(year) + "-12-31")

        stock_remaining_condition_request = """
                                            "public".atk_stationary_request.date_request <= '%s' AND
                                            "public".atk_stationary_request."state" = 'done'
                                            """ % (str(year) + "-12-31")
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
        						EXTRACT(YEAR FROM "public".atk_transaction."name") = """ + str(
            year) + """
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
        						EXTRACT(YEAR FROM "public".atk_transaction."name") = """ + str(
            year) + """
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
        				""" % (self.query_stock_remaining(stock_remaining_condition, stock_remaining_condition_request))
        return query

    def query_bulanan_sisa_stock(self, year, month):
        month_converter = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

        month_vals = 0
        if month:
            if month == 2:
                month_vals = 29 if (year % 4 == 0) else 28
            else:
                month_vals = month_converter[month]

        stock_remaining_condition = """
        									"public".atk_transaction."name" <= '%s'
        									""" % (
        str(year) + "-" + str(month) + "-" + str(month_vals))

        stock_remaining_condition_request = """
                                    "public".atk_stationary_request.date_request <= '%s' AND
                                    "public".atk_stationary_request."state" = 'done'
                                    """ % (str(year) + "-" + str(month) + "-" + str(month_vals))

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
        						EXTRACT(MONTH FROM "public".atk_transaction."name") = """ + str(
            month) + """ AND
        						EXTRACT(YEAR FROM "public".atk_transaction."name") = """ + str(
            year) + """
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
        						EXTRACT(MONTH FROM "public".atk_transaction."name") = """ + str(
            month) + """ AND
        						EXTRACT(YEAR FROM "public".atk_transaction."name") = """ + str(
            year) + """
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
        				""" % (self.query_stock_remaining(stock_remaining_condition, stock_remaining_condition_request))
        return query

    def query_harian_sisa_stock(self, date):
        stock_remaining_condition = """
                                    "public".atk_transaction."name" <= '%s'
                                    """ % (str(date))

        stock_remaining_condition_request = """
                                    "public".atk_stationary_request.date_request <= '%s' AND
                                    "public".atk_stationary_request."state" = 'done'
                                    """ % (str(date))

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
        						"public".atk_transaction."name" = '""" + str(date) + """'
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
        						"public".atk_transaction."name" = '""" + str(date) + """'
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
        				""" % (self.query_stock_remaining(stock_remaining_condition, stock_remaining_condition_request))
        return query

    def _process_report(self, data):
        lines = []

        process_report_choice = {
            'Tahunan': self.query_tahunan(data['form']['company_id'], data['form']['year_filter']),
            'Harian': self.query_harian(data['form']['company_id'], data['form']['date_filter']),
            'Bulanan': self.query_bulanan(data['form']['company_id'], data['form']['year_filter'],
                                          data['form']['month_filter'])
        }

        query = process_report_choice[data.get('form').get('report_type')]
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            lines.append(r)
        return lines

    def _process_report_stock_in(self, data):
        lines = []
        process_report_choice = {
            'Tahunan': self.query_tahunan_stock_in(data['form']['company_id'], data['form']['year_filter']),
            'Harian': self.query_harian_stock_in(data['form']['company_id'], data['form']['date_filter']),
            'Bulanan': self.query_bulanan_stock_in(data['form']['company_id'], data['form']['year_filter'],
                                          data['form']['month_filter'])
        }
        query = process_report_choice[data.get('form').get('report_type')]
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            lines.append(r)
        return lines

    def _process_report_sisa_stock(self, data):
        lines = []
        process_report_choice = {
            'Tahunan': self.query_tahunan_sisa_stock(data['form']['year_filter']),
            'Harian': self.query_harian_sisa_stock(data['form']['date_filter']),
            'Bulanan': self.query_bulanan_sisa_stock(data['form']['year_filter'],
                                                   data['form']['month_filter'])
        }
        query = process_report_choice[data.get('form').get('report_type')]
        print(query)
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            lines.append(r)
        return lines

    def _get_month_name(self, month):
        month_name = {
            1: 'Januari',
            2: 'Februari',
            3: 'Maret',
            4: 'April',
            5: 'Mei',
            6: 'Juni',
            7: 'Juli',
            8: 'Agustus',
            9: 'September',
            10: 'Oktober',
            11: 'November',
            12: 'Desember'
        }
        if month is None:
            return None
        return month_name[month]

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Rekap Stok Keluar')
        sheet2 = workbook.add_worksheet('Rekap Stok Masuk')
        sheet3 = workbook.add_worksheet('Rekap Sisa Stok')

        self.format_prasetia_header_table_center = workbook.add_format({'font_size': 11, 'font': 'Calibri',
                                                                   'align': 'center', 'border': 1})
        self.format_prasetia_data_table = workbook.add_format({'font_size': 11, 'font': 'Calibri',
                                                          'align': 'left', 'border': 1})
        self.format_prasetia_1 = workbook.add_format({'font_size': 11, 'bold': True, 'bg_color': '#D3D3D3',
                                                 'font': 'Calibri', 'align': 'center'})

        self.detail_sheet1(data, sheet)
        self.detail_sheet2(data, sheet2)
        self.detail_sheet3(data, sheet3)

    def detail_sheet1(self, data, sheet):

        sheet.set_column(0, 0, 3)
        sheet.set_column(1, 1, 12)
        sheet.set_column(2, 2, 8)
        sheet.set_column(3, 3, 14)
        sheet.set_column(4, 4, 13)
        sheet.set_column(5, 5, 13)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 8)
        sheet.set_column(8, 8, 8)
        sheet.merge_range('A1:I1', 'REKAP STOK KELUAR PERLENGKAPAN KANTOR(ATK)', self.format_prasetia_1)
        sheet.merge_range('A2:I2', data['company_name'], self.format_prasetia_1)
        if data.get('form').get('report_type') == 'Harian':
            sheet.merge_range('A3:I3', 'TANGGAL : ' + data['form']['date_filter'], self.format_prasetia_1)
        elif data.get('form').get('report_type') == 'Bulanan':
            sheet.merge_range('A3:I3', 'PERIODE : ' + self._get_month_name(data['form']['month_filter'])
                              + '-' + str(data['form']['year_filter']), self.format_prasetia_1)
        elif data.get('form').get('report_type') == 'Tahunan':
            sheet.merge_range('A3:I3', 'PERIODE : ' + str(data['form']['year_filter']), self.format_prasetia_1)
        sheet.merge_range('A5:A6', 'NO', self.format_prasetia_header_table_center)
        sheet.merge_range('B5:B6', 'TANGGAL', self.format_prasetia_header_table_center)
        sheet.merge_range('C5:C6', 'NOREG', self.format_prasetia_header_table_center)
        sheet.merge_range('D5:D6', 'NAMA', self.format_prasetia_header_table_center)
        sheet.merge_range('E5:E6', 'DEPARTEMEN', self.format_prasetia_header_table_center)
        sheet.merge_range('F5:I5', 'STOK KELUAR', self.format_prasetia_header_table_center)
        sheet.write('F6', 'KATEGORI', self.format_prasetia_header_table_center)
        sheet.write('G6', 'NAMA BARANG', self.format_prasetia_header_table_center)
        sheet.write('H6', 'JUMLAH', self.format_prasetia_header_table_center)
        sheet.write('I6', 'SATUAN', self.format_prasetia_header_table_center)
        lines = self._process_report(data)
        row_number = 5
        rec_number = 0
        for line in lines:
            row_number += 1
            rec_number += 1
            sheet.write(row_number, 0, rec_number, self.format_prasetia_data_table)
            sheet.write(row_number, 1, line['date_request'], self.format_prasetia_data_table)
            sheet.write(row_number, 2, line['nik'], self.format_prasetia_data_table)
            sheet.write(row_number, 3, line['name'], self.format_prasetia_data_table)
            sheet.write(row_number, 4, line['departement_name'], self.format_prasetia_data_table)
            sheet.write(row_number, 5, line['category_name'], self.format_prasetia_data_table)
            sheet.write(row_number, 6, line['item_name'], self.format_prasetia_data_table)
            sheet.write(row_number, 7, line['qty_out'], self.format_prasetia_data_table)
            sheet.write(row_number, 8, line['uom'], self.format_prasetia_data_table)

    def detail_sheet2(self, data, sheet):
        sheet.set_column(0, 0, 3)
        sheet.set_column(1, 1, 12)
        sheet.set_column(2, 2, 8)
        sheet.set_column(3, 3, 14)
        sheet.set_column(4, 4, 13)
        sheet.set_column(5, 5, 13)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 8)
        sheet.set_column(8, 8, 8)
        sheet.merge_range('A1:I1', 'REKAP STOK MASUK PERLENGKAPAN KANTOR(ATK)', self.format_prasetia_1)
        sheet.merge_range('A2:I2', data['company_name'], self.format_prasetia_1)
        if data.get('form').get('report_type') == 'Harian':
            sheet.merge_range('A3:I3', 'TANGGAL : ' + data['form']['date_filter'], self.format_prasetia_1)
        elif data.get('form').get('report_type') == 'Bulanan':
            sheet.merge_range('A3:I3', 'PERIODE : ' + self._get_month_name(data['form']['month_filter'])
                              + '-' + str(data['form']['year_filter']), self.format_prasetia_1)
        elif data.get('form').get('report_type') == 'Tahunan':
            sheet.merge_range('A3:I3', 'PERIODE : ' + str(data['form']['year_filter']), self.format_prasetia_1)

        sheet.merge_range('A5:A6', 'NO', self.format_prasetia_header_table_center)
        sheet.merge_range('B5:B6', 'TANGGAL', self.format_prasetia_header_table_center)
        sheet.merge_range('C5:C6', 'NOREG', self.format_prasetia_header_table_center)
        sheet.merge_range('D5:D6', 'NAMA', self.format_prasetia_header_table_center)
        sheet.merge_range('E5:E6', 'DEPARTEMEN', self.format_prasetia_header_table_center)
        sheet.merge_range('F5:I5', 'STOK KELUAR', self.format_prasetia_header_table_center)
        sheet.write('F6', 'KATEGORI', self.format_prasetia_header_table_center)
        sheet.write('G6', 'NAMA BARANG', self.format_prasetia_header_table_center)
        sheet.write('H6', 'JUMLAH', self.format_prasetia_header_table_center)
        sheet.write('I6', 'SATUAN', self.format_prasetia_header_table_center)

        lines = self._process_report_stock_in(data)
        row_number = 5
        rec_number = 0
        for line in lines:
            row_number += 1
            rec_number += 1
            sheet.write(row_number, 0, rec_number, self.format_prasetia_data_table)
            sheet.write(row_number, 1, line['tanggal'], self.format_prasetia_data_table)
            sheet.write(row_number, 2, '-', self.format_prasetia_data_table)
            sheet.write(row_number, 3, line['employee_name'], self.format_prasetia_data_table)
            sheet.write(row_number, 4, line['dept_name'], self.format_prasetia_data_table)
            sheet.write(row_number, 5, line['category_name'], self.format_prasetia_data_table)
            sheet.write(row_number, 6, line['item_name'], self.format_prasetia_data_table)
            sheet.write(row_number, 7, line['qty'], self.format_prasetia_data_table)
            sheet.write(row_number, 8, line['uom'], self.format_prasetia_data_table)

    def detail_sheet3(self, data, sheet):
        sheet.set_column(0, 0, 3)
        sheet.set_column(1, 1, 13)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 8)
        sheet.set_column(4, 4, 8)
        sheet.merge_range('A1:D1', 'REKAP SISA STOK PERLENGKAPAN KANTOR(ATK)', self.format_prasetia_1)
        if data.get('form').get('report_type') == 'Harian':
            sheet.merge_range('A2:D2', 'TANGGAL : ' + data['form']['date_filter'], self.format_prasetia_1)
        elif data.get('form').get('report_type') == 'Bulanan':
            sheet.merge_range('A2:D2', 'PERIODE : ' + self._get_month_name(data['form']['month_filter'])
                              + '-' + str(data['form']['year_filter']), self.format_prasetia_1)
        elif data.get('form').get('report_type') == 'Tahunan':
            sheet.merge_range('A2:D2', 'PERIODE : ' + str(data['form']['year_filter']), self.format_prasetia_1)

        sheet.write('A5', 'NO', self.format_prasetia_header_table_center)
        sheet.write('B5', 'KATEGORI', self.format_prasetia_header_table_center)
        sheet.write('C5', 'NAMA BARANG', self.format_prasetia_header_table_center)
        sheet.write('D5', 'JUMLAH', self.format_prasetia_header_table_center)

        lines = self._process_report_sisa_stock(data)
        row_number = 4
        rec_number = 0
        for line in lines:
            row_number += 1
            rec_number += 1
            sheet.write(row_number, 0, rec_number, self.format_prasetia_data_table)
            sheet.write(row_number, 1, line['category_name'], self.format_prasetia_data_table)
            sheet.write(row_number, 2, line['name'], self.format_prasetia_data_table)
            sheet.write(row_number, 3, line['stock_remaining'], self.format_prasetia_data_table)

report_atk_xls('report.prasetia.atk.xls.xlsx', 'atk.stationary.request')