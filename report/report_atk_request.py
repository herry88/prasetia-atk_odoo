from openerp import api, models

class ReportAtkRequest(models.AbstractModel):
    _name = 'report.prasetia.report_atk_request_prasetia'

    def query_tahunan(self, data):
        query = """
            SELECT
            "public".atk_company."name" AS "COMPANY_NAME",
            "public".atk_stationary_request.nik,
            "public".atk_stationary_request."name",
            "public".atk_stationary_request.date_request,
            "public".atk_item."name" AS "ITEM_NAME",
            "public".atk_item_category."name" AS "CATEGORY_NAME",
            "public".atk_stationary_request_line.qty,
            "public".atk_stationary_request_line.qty_out,
            "public".atk_uom."name" AS "UOM_OUT",
            A."name" AS "UOM_IN",
            "public".atk_stationary_request_line.item_category_id,
            "public".atk_stationary_request_line.item_id
            FROM
            "public".atk_stationary_request_line
            LEFT JOIN "public".atk_stationary_request ON "public".atk_stationary_request_line.stationary_request_id = "public".atk_stationary_request."id"
            LEFT JOIN "public".atk_company ON "public".atk_stationary_request.company_id = "public".atk_company."id"
            LEFT JOIN "public".atk_item ON "public".atk_stationary_request_line.item_id = "public".atk_item."id"
            LEFT JOIN "public".atk_item_category ON "public".atk_stationary_request_line.item_category_id = "public".atk_item_category."id"
            LEFT JOIN "public".atk_uom ON "public".atk_stationary_request_line.unit_measure_id_out = "public".atk_uom."id"
            LEFT JOIN "public".atk_uom AS A ON "public".atk_stationary_request_line.unit_measure_id = A."id"
            WHERE
            "public".atk_stationary_request.company_id = """ + str(data.get('company_id')[0]) + """ AND
            EXTRACT(YEAR FROM "public".atk_stationary_request.date_request) = """+ str(data.get('year_filter')) +"""
            ORDER BY
            "public".atk_stationary_request_line.item_category_id ASC,
            "public".atk_stationary_request_line.item_id ASC
        """
        return query

    def query_bulanan(self, data):
        print(str(data.get('month_filter')))
        query = """
            SELECT
            "public".atk_company."name" AS "COMPANY_NAME",
            "public".atk_stationary_request.nik,
            "public".atk_stationary_request."name",
            "public".atk_stationary_request.date_request,
            "public".atk_item."name" AS "ITEM_NAME",
            "public".atk_item_category."name" AS "CATEGORY_NAME",
            "public".atk_stationary_request_line.qty,
            "public".atk_stationary_request_line.qty_out,
            "public".atk_uom."name" AS "UOM_OUT",
            A."name" AS "UOM_IN",
            "public".atk_stationary_request_line.item_category_id,
            "public".atk_stationary_request_line.item_id
            FROM
            "public".atk_stationary_request_line
            LEFT JOIN "public".atk_stationary_request ON "public".atk_stationary_request_line.stationary_request_id = "public".atk_stationary_request."id"
            LEFT JOIN "public".atk_company ON "public".atk_stationary_request.company_id = "public".atk_company."id"
            LEFT JOIN "public".atk_item ON "public".atk_stationary_request_line.item_id = "public".atk_item."id"
            LEFT JOIN "public".atk_item_category ON "public".atk_stationary_request_line.item_category_id = "public".atk_item_category."id"
            LEFT JOIN "public".atk_uom ON "public".atk_stationary_request_line.unit_measure_id_out = "public".atk_uom."id"
            LEFT JOIN "public".atk_uom AS A ON "public".atk_stationary_request_line.unit_measure_id = A."id"
            WHERE
            "public".atk_stationary_request.company_id = """ + str(data.get('company_id')[0]) + """ AND
            EXTRACT(MONTH FROM "public".atk_stationary_request.date_request) = """+ str(data.get('month_filter')) +""" AND
            EXTRACT(YEAR FROM "public".atk_stationary_request.date_request) = """+ str(data.get('year_filter')) +"""
            ORDER BY
            "public".atk_stationary_request_line.item_category_id ASC,
            "public".atk_stationary_request_line.item_id ASC
        """
        return query

    def query_harian(self, data):
        query = """
            SELECT
            "public".atk_company."name" AS "COMPANY_NAME",
            "public".atk_stationary_request.nik,
            "public".atk_stationary_request."name",
            "public".atk_stationary_request.date_request,
            "public".atk_item."name" AS "ITEM_NAME",
            "public".atk_item_category."name" AS "CATEGORY_NAME",
            "public".atk_stationary_request_line.qty,
            "public".atk_stationary_request_line.qty_out,
            "public".atk_uom."name" AS "UOM_OUT",
            A."name" AS "UOM_IN",
            "public".atk_stationary_request_line.item_category_id,
            "public".atk_stationary_request_line.item_id
            FROM
            "public".atk_stationary_request_line
            LEFT JOIN "public".atk_stationary_request ON "public".atk_stationary_request_line.stationary_request_id = "public".atk_stationary_request."id"
            LEFT JOIN "public".atk_company ON "public".atk_stationary_request.company_id = "public".atk_company."id"
            LEFT JOIN "public".atk_item ON "public".atk_stationary_request_line.item_id = "public".atk_item."id"
            LEFT JOIN "public".atk_item_category ON "public".atk_stationary_request_line.item_category_id = "public".atk_item_category."id"
            LEFT JOIN "public".atk_uom ON "public".atk_stationary_request_line.unit_measure_id_out = "public".atk_uom."id"
            LEFT JOIN "public".atk_uom AS A ON "public".atk_stationary_request_line.unit_measure_id = A."id"
            WHERE
            "public".atk_stationary_request.company_id = %d AND
            "public".atk_stationary_request.date_request = '%s'
            ORDER BY
            "public".atk_stationary_request_line.item_category_id ASC,
            "public".atk_stationary_request_line.item_id ASC
        """ % (data.get('company_id')[0], data.get('date_filter'))
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
        for r in res:
            lines.append(r)
        return lines

    @api.multi
    def render_html(self, data):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'report_type': data.get('form').get('report_type'),
            'date_filter': data.get('form').get('date_filter'),
            'bulan_filter': data.get('form').get('month_filter'),
            'tahun_filter': data.get('form').get('year_filter'),
            'company': data.get('form').get('company_id')[1],
            'transactions': self._get_atk_list(data.get('form')),
            'transaction_details': self._get_atk_list(data.get('form'))
        }

        return self.env['report'].render('prasetia.report_atk_request_prasetia', docargs)