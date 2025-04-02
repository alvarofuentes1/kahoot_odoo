{
    'name': 'Magister Quiz',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Enhances the Survey module with Kahoot! like functionality.',
    'depends': ['survey'],
    'data': [
        #Views
        'views/quiz_survey_views.xml',
        'views/quiz_question_views.xml',
        'views/quiz_menus.xml',

        #Security
        'security/ir.model.access.csv'
    ],
    'controllers': [
        'controllers.main',
    ],
    'application': 'true',
    'installable': 'true',
}
