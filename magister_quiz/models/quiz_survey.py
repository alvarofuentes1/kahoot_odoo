from email.policy import default

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

    #is_time_limited (boolean)
    #time_lmit (float) -> tiempo total
    is_question_timed = fields.Boolean("Question Time Limit")
    time_per_question = fields.Integer("Time per Question (seconds)", default=20)
    """
    session_show_leaderboard = fields.Boolean("Show Session Leaderboard", compute='_compute_session_show_leaderboard',
        help="Whether or not we want to show the attendees leaderboard for this survey.")
        
    @api.depends('scoring_type', 'question_and_page_ids.save_as_nickname')
    def _compute_session_show_leaderboard(self):
        for survey in self:
            survey.session_show_leaderboard = survey.scoring_type != 'no_scoring' and \
                any(question.save_as_nickname for question in survey.question_and_page_ids)
                
    """
    bonus_points = fields.Boolean("Bonus Points for Speed", default=True)