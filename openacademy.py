from openerp.osv import osv, fields


class course (osv.Model):
    _name = 'openacademy.course'
    
    _columns = {
        'name':         fields.char(string="Name", size=128, required=True),
        'description':  fields.text(string="Description"),
    }
