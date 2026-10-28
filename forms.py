from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField


class CategoryForm(FlaskForm):
    search_type = SelectField(
        "Search By",
        choices=[
            ("category", "Search by Category"),
            ("name", "Search by Name")
        ]
    )
    submit = SubmitField("Continue")


class SearchForm(FlaskForm):
    search_text = StringField("Search")
    submit = SubmitField("Search")
