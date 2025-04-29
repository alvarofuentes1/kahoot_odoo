{
    'name': 'Magister Quiz',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Enhances the Survey module with Kahoot! like functionality.',
    'depends': ['base', 'survey'],
    'data': [
        # Views
        'views/quiz_survey_views.xml',
        'views/quiz_question_views.xml',
        'views/quiz_menus.xml',
        'views/quiz_template.xml',

        # Security
        'security/ir.model.access.csv'
    ],
    'controllers': [
        'controllers.main',
    ],
    'assets': {
        'web.assets_frontend': [
            'magister_quiz/static/src/css/*',
            'magister_quiz/static/src/js/*',
        ],    
    },
    'application': 'true',
    'installable': 'true',
}
