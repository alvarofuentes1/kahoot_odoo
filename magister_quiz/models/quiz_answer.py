from odoo import fields, models, api

class QuizAnswer(models.Model):
    _inherit = "survey.question.answer"
    
    is_conditional_answer = fields.Boolean(
        "Is Conditional Answer", 
        help="If true, this answer will redirect to another question linked to this one.")
    next_conditional_question_id = fields.Many2one(
        'survey.question', 
        string="Conditional Question", 
        help="Pregunta a la que se redirige si la pregunta es condicional, IMPORTANTE: se saltarán las preguntas entre esta y la pregunta condicional, además, está deberá ser creada de antemano"
    )
    survey_id = fields.Many2one(related="question_id.survey_id", string="Survey", store=True)