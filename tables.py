from flask_table import Table, Col, LinkCol
 
class Results(Table):
    user_id = Col('Index no')
    user_name = Col('Name')
    user_email = Col('Email')
    user_password = Col('Password', show=False)
    edit = LinkCol('Edit', 'edit_view', url_kwargs=dict(id='user_id'))
    delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='user_id'))


class Experiments(Table):
    experiment_id = Col('Experiment no')
    name = Col('Experiment Name')
    calculated_value = Col('Calculated Value')
    experiment_date = Col('Date')    
    created_date = Col('Created Date',show=False)
    updated_date = Col('Updated Date',show=False)
    is_deleted = Col('Is Deleted',show=False)
    is_edited = Col('Is Edited',show=False)
    edit = LinkCol('Edit', 'edit_experiment_view', url_kwargs=dict(id='experiment_id'))
    delete = LinkCol('Delete', 'delete_experiment', url_kwargs=dict(id='experiment_id'))