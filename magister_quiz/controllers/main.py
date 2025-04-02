from odoo import http
from odoo.http import request

class MagisterQuizController(http.Controller):

    @http.route('/play', auth='public', website=True)
    def play_quiz(self, **kw):
        return request.render('magister_quiz.template')

