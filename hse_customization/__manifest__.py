{
  'name': 'HSE Customizations',
  'version': '16.0.1.0.1',
  'depends': ['mail'],
  'data': [
    'security/security.xml',
    # Keep rule file but we'll deactivate the specific rule inside
    'security/ir_rule.xml',
    'data/activity_types.xml',
    'views/hse_views.xml',
  ],
  'installable': True,
}