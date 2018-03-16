# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DocumentLegal(models.Model):
    _name = "document.legal.send.mail"

    name = fields.Char(required=True, string="Nama Dokument")

    @api.model
    def _send_email_reminder_document_expired(self):

        obj_mail_mail = self.env['mail.mail']

        body_message = """
            Dear, All<br/></br>

            Di informasikan bahwa dokumen berikut akan habis masa berlaku dalam <strong>21 hari</strong></br></br>

            <table>
                <tr>
                    <th>Document</th>
                    <th>:</th>
                    <th><h4>%s</h4></th>
                </tr>
                <tr>
                    <th>Expired</th>
                    <th>:</th>
                    <th><h4>%s</h4></th>
                </tr>
            </table>

        """
        query = """
                SELECT
                "public".x_document_legal."id",
                "public".x_document_legal.x_name,
                "public".x_document_legal.x_tanggal_expire
                FROM
                "public".x_document_legal
                WHERE
                 "public".x_document_legal.x_tanggal_expire - current_date = 21
                """

        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            vals = {
                'email_from': 'admin@prasetiadwidharma.co.id',
                'email_to': 'junifar.hidayat@prasetiadwidharma.co.id; yohanes.efrendi@prasetiadwidharma.co.id',
                'state': 'outgoing',
                'subject': '[Prasetia Legal Document] - Document Expired Soon',
                'body_html': body_message % (r['x_name'], r['x_tanggal_expire'])
            }
            msg_id = obj_mail_mail.create(vals)
            if msg_id:
                obj_mail_mail.send([msg_id])