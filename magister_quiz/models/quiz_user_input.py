from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QuizUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    value_boolean = fields.Boolean("True/False Answer")


class QuizUserInput(models.Model):
    _inherit = "survey.user_input"

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
    time_taken = fields.Integer("Time Taken for Question")


"""
    @api.depends(
        "user_input_line_ids.answer_score",
        "user_input_line_ids.question_id",
        "user_input_line_ids.time_taken",
        "survey_id.bonus_points",
        "survey_id.time_per_question",
    )
    def _compute_scoring_values(self):
        for user_input in self:
            total_score = 0
            total_possible_score = 0

            for line in user_input.user_input_line_ids:
                question = line.question_id
                answer_score = line.answer_score
                time_taken = line.time_taken or user_input.survey_id.time_per_question  # Evita errores si es nulo

                if question.question_type in ["simple_choice", "multiple_choice"]:
                    total_possible_score += max(
                        question.suggested_answer_ids.mapped("answer_score"), default=0
                    )

                    base_score = answer_score  # Puntos base según la respuesta
                    if user_input.survey_id.bonus_points:
                        # Calcula el bono basado en la rapidez de respuesta
                        max_time = user_input.survey_id.time_per_question
                        bonus_factor = max(0, (max_time - time_taken) / max_time)  # Cuánto más rápido, más puntos
                        speed_bonus = round(base_score * bonus_factor)

                        base_score += speed_bonus

                    total_score += base_score

            # Asignar los valores finales
            user_input.scoring_total = total_score
"""
