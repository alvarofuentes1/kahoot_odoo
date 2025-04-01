from odoo import fields, models, api


class QuizQuestion(models.Model):
    _inherit="survey.question"

    time_limit = fields.Integer("Time Limit for Answer (seconds)", default=30)
    points = fields.Integer("Points for Correct Answer", default=10)
    is_bonus_question = fields.Boolean("Is Bonus Question", default=False)
    