from odoo import models, fields, api

class SessionRanking(models.Model):
    _name = 'survey.session_ranking'
    _description = 'Ranking por sesión'

    user_input_id = fields.Many2one('survey.user_input', required=True)
    survey_id = fields.Many2one('survey.survey', required=True)
    user_id = fields.Many2one("res.partner", store=True)
    total_score = fields.Float("Puntuación total", compute='_compute_total_score', store=True)

    @api.depends('user_input_id.user_input_line_ids.score')
    def _compute_total_score(self):
        for record in self:
            scores = record.user_input_id.user_input_line_ids.mapped('score')
            record.total_score = round(sum(scores), 2)
