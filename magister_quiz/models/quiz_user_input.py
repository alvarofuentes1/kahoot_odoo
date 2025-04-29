
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class QuizUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    response_time = fields.Float("Response Time", help="Time taken to answer the question in seconds")
    score = fields.Float("Puntuación", default=0.0)

    def calculate_score(self):
        """
        Calculate the score based on the user's response and the correct answer.
        """
        for record in self:
            
                if(record.question_id.question_type != 'multiple_choice'):
                    if(record.survey_id.is_time_limited):
                        if(record.response_time > 0):
                            record.score = (1 - (record.response_time / record.survey_id.time_per_question)/2) * 1000
                        else:
                            record.score = 1000
                    else:
                        record.score = 1000
                else:          
                    correct_answers = record.survey_id.question_ids.filtered(lambda answer: answer.is_correct)
                    num_answers = len(correct_answers)
                    for line in record:
                        if line.answer_is_correct:
                            user_correct_answers += 1
                    
                    if(record.survey_id.is_time_limited):
                        if(record.response_time > 0):
                            record.score = (1 - (record.response_time / record.survey_id.time_per_question)/2) * 1000 / (user_correct_answers/num_answers)
                        else:
                            record.score = 1000 / (user_correct_answers/num_answers)
                    else:
                        if(num_answers > 0):
                            record.score = 1000 / (user_correct_answers/num_answers)
                        else:
                            record.score = 0
                            
                            
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