# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DocumentLegal(models.Model):
    _name = "document.legal.send.mail"

    name = fields.Char(required=True, string="Nama Dokument")

    @api.model
    def _send_email_reminder_document_expired(self):

        obj_mail_mail = self.env['mail.mail']

        body_message = """
            Dear, All

            Diinformasikan bahwa dokumen berikut akan habis masa berlakukan dalam <strong>7 hari lagi</strong>

            <h4>%s</h4>
        """
        query = """
                SELECT
                "public".x_document_legal."id",
                "public".x_document_legal.x_name,
                "public".x_document_legal.x_tanggal_expire
                FROM
                "public".x_document_legal
                WHERE
                 current_date - "public".x_document_legal.x_tanggal_terbit = 7
                """

        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            vals = {
                'email_from': 'admin@prasetiadwidharma.co.id',
                'email_to': 'Junifar@gmail.com',
                'state': 'outgoing',
                'subject': '[Prasetia Legal Document] - Document Expired Soon',
                'body_html': body_message % r['x_name']
            }
            msg_id = obj_mail_mail.create(vals)
            if msg_id:
                obj_mail_mail.send([msg_id])