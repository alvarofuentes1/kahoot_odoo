
from odoo import fields, models, api


class QuizSurvey(models.Model):
    _inherit="survey.survey"

    survey_type = fields.Selection([
        ('survey', 'Survey'),
        ('live_session', 'Live session'),
        ('assessment', 'Assessment'),
        ('custom', 'Custom'),
        ('quiz', 'Quiz'),
        ],
    )
    is_question_timed = fields.Boolean("Question Time Limit")
    time_per_question = fields.Integer("Time per Question (seconds)", default=10)
    
    def finalizeSurvey(self):
        
        self.env['survey.session_ranking'].calculate_ranking(self.id)
        
    def _get_next_page_or_question(self, user_input, page_or_question_id, go_back=False):
        survey = user_input.survey_id
        pages_or_questions = survey._get_pages_or_questions(user_input)
        Question = self.env['survey.question']

        # --- ✅ INICIO: Lógica condicional personalizada estilo Kahoot ---
        if not go_back and survey.questions_layout == 'page_per_question':
            # Buscar la última línea respondida correspondiente a esta pregunta
            last_input_line = user_input.user_input_line_ids.filtered(
                lambda l: l.question_id.id == page_or_question_id
            )

            if last_input_line:
                # Si es selección única
                conditional_answer = last_input_line.suggested_answer_id
                # O si es selección múltiple (buscar la primera condicional)
                if not conditional_answer:
                    conditional_answer = last_input_line.answer_ids.filtered('is_conditional_answer')[:1]

                next_conditional = conditional_answer.next_conditional_question_id
                if (
                    conditional_answer and
                    conditional_answer.is_conditional_answer and
                    next_conditional and
                    next_conditional.id in pages_or_questions.ids
                ):
                    return next_conditional

        # --- ✅ FIN: Lógica condicional personalizada ---

        # Get Next
        if not go_back:
            if not pages_or_questions:
                return Question
            if page_or_question_id == 0:
                return pages_or_questions[0]

        current_page_index = pages_or_questions.ids.index(page_or_question_id)

        if (go_back and current_page_index == 0) or (not go_back and current_page_index == len(pages_or_questions) - 1):
            return Question



        # Conditional Questions Management (original de Odoo)
        triggering_answers_by_question, _, selected_answers = user_input._get_conditional_values()
        inactive_questions = user_input._get_inactive_conditional_questions()
        if survey.questions_layout == 'page_per_question':
            question_candidates = pages_or_questions[0:current_page_index] if go_back \
                else pages_or_questions[current_page_index + 1:]
            for question in question_candidates.sorted(reverse=go_back):
                if question.is_page:
                    contains_active_question = any(sub_question not in inactive_questions for sub_question in question.question_ids)
                    is_description_section = not question.question_ids and not is_html_empty(question.description)
                    if contains_active_question or is_description_section:
                        return question
                else:
                    triggering_answers = triggering_answers_by_question.get(question)
                    if not triggering_answers or triggering_answers & selected_answers:
                        return question
        elif survey.questions_layout == 'page_per_section':
            section_candidates = pages_or_questions[0:current_page_index] if go_back \
                else pages_or_questions[current_page_index + 1:]
            for section in section_candidates.sorted(reverse=go_back):
                contains_active_question = any(question not in inactive_questions for question in section.question_ids)
                is_description_section = not section.question_ids and not is_html_empty(section.description)
                if contains_active_question or is_description_section:
                    return section

        return Question
