from odoo import fields, models, api


class QuizSurvey(models.Model):
    _inherit="survey.survey"

    is_quiz = fields.Boolean("Is Quiz", default=False)
    time_per_question = fields.Integer("Time per Question (seconds)", default=30)
    show_ranking = fields.Boolean("Show Ranking", default=True)
    bonus_points = fields.Boolean("Bonus Points for Speed", default=True)