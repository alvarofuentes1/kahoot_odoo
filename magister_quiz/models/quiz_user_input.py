from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QuizUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    value_boolean = fields.Boolean("True/False Answer")


class QuizUserInput(models.Model):
    _inherit = "survey.user_input"

    value_boolean = fields.Boolean('Boolean Answer', help="Stores the response for True/False questions")

    def _save_lines(self, question, answer, comment=None, overwrite_existing=True, **kwargs):

        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])
        if old_answers and not overwrite_existing:
            raise UserError(_("This answer cannot be overwritten."))

        if question.question_type == "true_false":
            self._save_line_true_false_answer(question, old_answers, answer)
        else:
            return super(QuizUserInput, self)._save_lines(question, answer, comment, **kwargs)

    def _save_line_true_false_answer(self, question, old_answers, answer):
        """Guarda la respuesta de una pregunta de tipo true_false"""

        # Convertimos el valor recibido en un booleano
        is_true = answer == '1'  # Odoo envía '1' para True, '0' para False

        vals = {
            'user_input_id': self.id,
            'question_id': question.id,
            'survey_id': question.survey_id.id,
            'page_id': question.page_id.id,
            'value_boolean': is_true,  # Guardamos el valor en el nuevo campo
        }

        # Si ya existe una respuesta previa, la actualizamos, si no, creamos una nueva
        if old_answers:
            old_answers.write(vals)
            return old_answers
        else:
            return self.env['survey.user_input.line'].create(vals)
