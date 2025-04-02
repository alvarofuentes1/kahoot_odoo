from odoo import fields, models, api


class QuizQuestion(models.Model):
    _inherit = "survey.question"
    _name="quiz.question"

    question_type = fields.Selection(
        selection_add = [
            ('true_false', 'True or False')
        ]
    )

    points = fields.Integer("Points for Correct Answer")