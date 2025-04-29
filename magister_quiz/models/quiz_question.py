
from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class QuizQuestion(models.Model):
    _inherit = "survey.question"
    
    points = fields.Float("Puntos por pregunta", compute="_compute_points")
    bonus_per_second = fields.Float("Bonus en base a timepo de respuesta")
    question_type = fields.Selection(selection_add=[('true_false', 'True or False')])
    answer_boolean = fields.Boolean(
        string="Correct Answer (True/False)",
        help="Mark for True, leave unmarked for False"
    )
    
    @api.model
    def create(self, vals):
        if vals.get('question_type') == 'true_false':
            answer_boolean = vals.get('answer_boolean')
            answer_score = vals.get('answer_score', 0)

            _logger.info(f"La pregunta es: {answer_boolean}")
            _logger.info(f"La puntuación es: {answer_score}")

            # Cambiamos a 'simple_choice' para que use la lógica existente de Odoo
            vals['question_type'] = 'simple_choice'
            question = super(QuizQuestion, self).create(vals)

            # Creamos las respuestas con score solo en la que sea correcta
            answers = []
            for value in ['True', 'False']:
                is_correct = (value == 'True') if answer_boolean else (value == 'False')
                score = answer_score if is_correct else 0
                answers.append({
                    'question_id': question.id,
                    'value': value,
                    'is_correct': is_correct,
                    'answer_score': score,
                })

            self.env['survey.question.answer'].create(answers)
            return question

        return super(QuizQuestion, self).create(vals)

    def depends_on_conditional_answer(self):
        """Check if this question is targeted by any conditional answer."""
        self.ensure_one()
        return bool(self.env['survey.question.answer'].search([
            ('next_conditional_question_id', '=', self.id),
            ('is_conditional_answer', '=', True)
        ], limit=1))