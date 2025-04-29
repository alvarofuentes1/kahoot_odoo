from odoo import fields, models, api

class QuizSessionRanking(models.Model):
    _name = "survey.session_ranking"
    _description = "User ranking for quiz sessions"
    _order = "score desc"
    
    user_id = fields.Many2one("res.users", string="User", required=True)
    survey_id = fields.Many2one("survey.survey", string="Survey", required=True)
    score = fields.Float(string="Score", required=True)
    rank = fields.Integer(string="Rank", compute="_compute_rank", store=True)

    @api.model
    def calculate_ranking(self, survey_id):
        """
        Calcular el ranking al finalizar una encuesta
        """
        # Primero obtenemos todas las respuestas de los usuarios en la encuesta
        user_input_lines = self.env['survey.user_input.line'].search([
            ('survey_id', '=', survey_id)
        ])
        
        # Creamos un diccionario de puntuaciones por usuario
        user_scores = {}
        
        for line in user_input_lines:
            user_id = line.user_id
            score = line.calculate_score()  # Asumiendo que tienes un método para calcular la puntuación
            if user_id in user_scores:
                user_scores[user_id] += score
            else:
                user_scores[user_id] = score
        
        # Ordenamos a los usuarios por su puntuación total de manera descendente
        sorted_user_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Guardamos el ranking
        rank_position = 1
        for user_id, total_score in sorted_user_scores:
            # Si no existe el ranking del usuario, lo creamos
            self.create({
                'user_id': user_id,
                'survey_id': survey_id,
                'score': score,
                'rank_position': rank_position
            })
            rank_position += 1