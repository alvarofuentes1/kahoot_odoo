
from odoo import fields, models, api


class QuizSurvey(models.Model):
    _inherit="survey.survey"

    survey_type = fields.Selection([
        ('survey', 'Survey'),
        ('live_session', 'Live session'),
        ('assessment', 'Assessment'),
        ('custom', 'Custom'),
        ('quiz', 'Quiz'),
        ],
    )
    is_question_timed = fields.Boolean("Question Time Limit")
    time_per_question = fields.Integer("Time per Question (seconds)", default=10)
    
    def finalizeSurvey(self):
        
        self.env['survey.session_ranking'].calculate_ranking(self.id)