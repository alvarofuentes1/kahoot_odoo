"""from odoo import models, fields, api

class QuizUserInput(models.Model):
    _inherit = "survey.user_input"


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


class QuizUserInputLine(models.Model):
    _inherit="survey.user_input.line"

    time_taken = fields.Integer("Time Taken for Question")"""