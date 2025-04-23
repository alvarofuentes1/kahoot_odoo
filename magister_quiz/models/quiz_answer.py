from odoo import fields, models, api

class QuizAnswer(models.Model):
    _inherit = "survey.question.answer"
    
    is_conditional_answer = fields.Boolean(
        "Is Conditional Answer", 
        help="If true, this answer will redirect to another question linked to this one.")
    
    @api.model
    def create_conditional_question():
        for record in self:
            if record.is_conditional_answer:
                # Create a new question linked to this answer
                new_question = self.env['survey.question'].create({
                    'title': "Conditional Question",
                    'question_type': 'simple_choice',
                    'survey_id': record.survey_id.id,
                })
                
                # Link the new question to the answer
                record.write({'conditional_question_id': new_question.id})