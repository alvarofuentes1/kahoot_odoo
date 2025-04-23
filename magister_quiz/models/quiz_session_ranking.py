from odoo import fields, models, api

class QuizSessionRanking(models.Model):
    _name = "survey.session_ranking"
    _description = "User ranking for quiz sessions"
    _order = "score desc"
    
    user_id = fields.Many2one("res.users", string="User", required=True)
    survey_id = fields.Many2one("survey.survey", string="Survey", required=True)
    score = fields.Float(string="Score", required=True)
    rank = fields.Integer(string="Rank", compute="_compute_rank", store=True)
    
    @api.depends("score")
    def _compute_rank(self):
        for record in self:
            # Get all scores for the same survey
            scores = self.search([("survey_id", "=", record.survey_id.id)], order="score desc")
            # Find the rank of the current record
            record.rank = scores.ids.index(record.id) + 1 if record.id in scores.ids else 0