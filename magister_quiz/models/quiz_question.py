from email.policy import default

from odoo import fields, models, api


class QuizQuestion(models.Model):
    _inherit = "survey.question"

    question_type = fields.Selection([
        ('simple_choice', 'Multiple choice: only one answer'),
        ('multiple_choice', 'Multiple choice: multiple answers allowed'),
        ('text_box', 'Multiple Lines Text Box'),
        ('char_box', 'Single Line Text Box'),
        ('numerical_box', 'Numerical Value'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('matrix', 'Matrix'),
        ('true_false', 'True or False'),
    ])

    answer_type = fields.Selection([
        ('text_box', 'Free Text'),
        ('char_box', 'Text'),
        ('numerical_box', 'Number'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('suggestion', 'Suggestion'),
        ('boolean', 'Boolean'),
    ])

    answer_boolean = fields.Selection([('1', 'True'), ('0', 'False')], string="Correct Answer")
    is_true_or_false = fields.Boolean("True or False", default=False)
