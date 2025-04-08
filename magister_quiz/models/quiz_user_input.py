
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class QuizUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    value_boolean = fields.Boolean("True/False Answer")


class QuizUserInput(models.Model):
    _inherit = "survey.user_input"

    value_boolean = fields.Boolean('Boolean Answer', help="Stores the response for True/False questions")

    def _save_lines(self, question, answer, comment=None, overwrite_existing=True, **kwargs):
        _logger.info(f"Answer received: {answer}")
        _logger.info(f"Correct answer: {question.answer_boolean}")

        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])

        if old_answers and not overwrite_existing:
            raise UserError(_("This answer cannot be overwritten."))

        # Manejo específico para preguntas tipo true_false
        if question.question_type == "true_false":
            answer_val = None

            if isinstance(answer, dict):
                answer_val = answer.get('value')

            _logger.info(f"Parsed boolean value: {answer_val}")

            # Convertir el valor recibido a booleano
            if answer_val in ['1', 'True', True]:
                answer_val = True
            elif answer_val in ['0', 'False', False]:
                answer_val = False
            else:
                answer_val = None

            return self._save_line_true_false_answer(question, old_answers, answer_val)

        return super(QuizUserInput, self)._save_lines(question, answer, comment, **kwargs)

    def _save_line_true_false_answer(self, question, old_answers, answer):
        
        # Guardar la respuesta booleana (True/False)
        vals = {
            'user_input_id': self.id,
            'question_id': question.id,
            'survey_id': question.survey_id.id,
            'page_id': question.page_id.id,
            'value_boolean': answer,  # Guardar el valor True/False
        }

        if old_answers:
            old_answers.write(vals)
            return old_answers
        else:
            _logger.info(f"New answer: {vals}")
            return self.env['survey.user_input.line'].create(vals)
        
        
    