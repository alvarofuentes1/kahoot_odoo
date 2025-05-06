
from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)

class QuizUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    response_time = fields.Float("Response Time", help="Time taken to answer the question in seconds")
    score = fields.Float("Puntuación")
    
    def _compute_score(self):
        for line in self:
            question = line.question_id
            survey = line.survey_id

            if not question or not survey or line.response_time is None:
                continue
            
            points = question.points
            time_limit = survey.time_per_question
            response_time = line.response_time

            total_score = (1 - ((response_time/time_limit) / 2 )) * points
            total_score = round(total_score, 2)
            
            line.score = total_score
        
           
                            
                            
class QuizUserInput(models.Model):
    _inherit = "survey.user_input"

    def has_selected_the_trigger_answer_for(self, question):
        """Check if the user selected an answer that triggers this question."""
        self.ensure_one()
        for line in self.user_input_line_ids:
            # Revisamos si la respuesta marcada tiene como siguiente esta pregunta
            answer = line.suggested_answer_id
            if answer and answer.next_conditional_question_id == question:
                return True
        return False
    
    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        """ Sobrescribimos el método para capturar response_time desde el contexto """
        input_line = super()._save_lines(question, answer, comment, overwrite_existing)

        response_time_map = self._context.get('response_time_map') or {}
        response_time = response_time_map.get(str(question.id))  # viene como string desde el JS

        if response_time and input_line:
            input_line.write({'response_time': float(response_time)})

        return input_line