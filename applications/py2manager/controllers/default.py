# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

def tester():
    return locals()

@auth.requires_login()
def add():
    project_form = SQLFORM(db.project).process()
    return dict(project_form=project_form)

@auth.requires_login()
def company():
    company_form = SQLFORM(db.company).process()
    grid = SQLFORM.grid(db.company, create=False, deletable=False,
    editable=False, maxtextlength=50, orderby=db.company.company_name)
    return locals()


@auth.requires_login()
def employee():
    employee_form = SQLFORM(db.auth_user).process()
    grid = SQLFORM.grid(db.auth_user, create=False, fields=[db.auth_user.first_name,
    db.auth_user.last_name, db.auth_user.email], deletable=False, editable=False, maxtextlength=50)
    return locals()

# ---- example index page ----
@auth.requires_login()
def index():
    response.flash = T('Welcome!')
    notes = [lambda project: A('Notes', _href=URL("default", "note", args=[project.id]))]
    grid = SQLFORM.grid(db.project, create=False, links=notes,
    fields=[db.project.name, db.project.employee_name,
    db.project.company_name, db.project.start_date,
    db.project.due_date, db.project.completed],
    deletable=False, maxtextlength=50)
    return locals()

@auth.requires_login()
def note():
    project = db.project(request.args(0))
    db.note.post_id.default = project.id
    form = crud.create(db.note) if auth.user else "Login to Post to the Project"
    allnotes = db(db.note.post_id == project.id).select()
    return locals()


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
