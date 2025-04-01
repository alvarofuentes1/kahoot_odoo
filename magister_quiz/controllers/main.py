from odoo import http
from odoo.http import request

class MagisterQuizController(http.Controller):

    @http.route('/play', auth='public', website=True)
    def play_quiz(self, survey_id=None, **kwargs):
        survey = request.env['survey.survey'].browse(int(survey_id))
        if not survey or not survey.is_quiz:
            return request.render('website.404')

        questions = survey.questions
        return request.render('magister_quiz.play_quiz', {
            'survey': survey,
            'questions': questions,
        })
