from flask import render_template, redirect,url_for
from wtforms import StringField,DateField,IntegerField,SubmitField
from wtforms.validators import DataRequired
from lbrc_flask.forms import FlashingForm
from lbrc_flask.database import db
from coloprevent.model import Ordered
from .. import blueprint


#create sql tables 


#creating forms 

class RequestForm(FlashingForm):
    equipment = StringField('Equipment', validators=[DataRequired()])
    total_requested =IntegerField('Total requested', validators=[DataRequired()])
    date_requested =DateField('Date requested', validators=[DataRequired()])


class DeleteData(FlashingForm):
    submit = SubmitField('Delete')

class EditData(FlashingForm):
    equipment = StringField('Equipment', validators=[DataRequired()])
    total_requested =IntegerField('Total requested', validators=[DataRequired()])
    date_requested =DateField('Date requested', validators=[DataRequired()])
    submit = SubmitField('Edit')


#creating config for sql tables

#secret ket for wtforms 



@blueprint.route('/', methods=['GET', 'POST'])
def index():
    ordered = db.session.execute(db.select(Ordered).order_by(Ordered.id)).scalars()
    ordered_list=[]
    for queried in ordered:
        ordered_list.append(queried)

    return render_template("ui/home.html", ordered_list=ordered_list)

@blueprint.route('/add', methods=['GET', 'POST'])
def add():
    form = RequestForm()
    if form.validate_on_submit():
            new_order =Ordered (
                equipment= form.equipment.data,
                date_ordered = form.date_requested.data,
                total_requested = form.total_requested.data                
                )
            db.session.add(new_order)
            db.session.commit()
    
            return redirect(url_for("ui.index"))
        
            
            

    return render_template("ui/add.html", form=form)



@blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(Ordered).where(Ordered.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect("ui.submissions")
    return render_template('ui/delete.html', id=id)
    
        

    

@blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(Ordered).where(Ordered.id == edit_id)).scalar()
        prev_equip = query_edit.equipment
        prev_total_req = query_edit.total_requested
        prev_date_ordered= query_edit.date_ordered
        ed_form=EditData(equipment=prev_equip,total_requested=prev_total_req, date_requested=prev_date_ordered) 

    
    if ed_form.validate_on_submit():
        
            query_edit.equipment= ed_form.equipment.data
            query_edit.date_ordered = ed_form.date_requested.data
            query_edit.total_requested = ed_form.total_requested.data
            db.session.add(query_edit)
            db.session.commit()
            return redirect("ui.submissions")
        

    return render_template('ui/edit.html', ed_form = ed_form, id=id)
