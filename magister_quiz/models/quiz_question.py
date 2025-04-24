
from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class QuizQuestion(models.Model):
    _inherit = "survey.question"
    
    points = fields.Float("Puntos por pregunta", compute="_compute_points")
    bonus_per_second = fields.Float("Bonus en base a timepo de respuesta")
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
    answer_boolean = fields.Boolean(
        string="Correct Answer (True/False)",
        help="Mark for True, leave unmarked for False"
    )
    is_conditional_question = fields.Boolean("Pregunta condicional", 
        help="Indica si tras esta pregunta hay otra pregunta condicional")
    conditional_next_question_id = fields.Many2one(
        'survey.question', 
        string="Pregunta condicional siguiente", 
        help="Pregunta a la que se redirige si la pregunta es condicional"
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

