from openerp.osv import osv, fields


class course (osv.Model):
    _name = 'openacademy.course'
    
    _columns = {
        'name':             fields.char(string="Name", size=128, required=True),
        'description':      fields.text(string="Description"),
        'responsible_id':   fields.many2one('res.users', string="Responsible", required=True),
        'session_ids':      fields.one2many('openacademy.session', 'course_id', string="Sessions"),
    }

class session (osv.Model):
    _name = 'openacademy.session'
    
    _columns = {
        'name':         fields.char(string="Name", size=128, required=True),
        'start_date':   fields.date(string="Start date"),
        'duration':     fields.float(string="Duration", digits=(6,2), help="Session durantion in days"),
        'seats':        fields.integer(string="Number of seats"),
        'instructor_id':fields.many2one('res.partner', string="Instructor", ondelete="set null",
                                        domain="['|',('instructor','=',True),('category_id.name','in',['Teacher level 1', 'Teacher level 2'])]"),
        'course_id':    fields.many2one('openacademy.course', string="Course", ondelete="cascade"),
        'attendee_ids': fields.one2many('openacademy.attendee', 'session_id', string="Attendees"),
    }

class attendee (osv.Model):
    _name = 'openacademy.attendee'
    
    _rec_name = 'partner_id'
    _order = 'partner_id'
    
    _columns = {
        'partner_id':   fields.many2one('res.partner', string="Partner"),
        'session_id':   fields.many2one('openacademy.session', string="Attended session", ondelete="cascade"),
    }

class resPartner (osv.Model):
    #_name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'instructor':    fields.boolean(string="Instructor"),
        'attendee_ids':     fields.one2many('openacademy.attendee', 'partner_id', string="Sessions"),
    }











