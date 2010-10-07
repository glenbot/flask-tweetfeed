from wtforms import Form, TextField


class SearchForm(Form):
    q = TextField('Search')
