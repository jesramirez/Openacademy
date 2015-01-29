from openerp.osv import osv, fields


class course (osv.Model):
    _name = 'openacademy.course'
    
    _columns = {
        'name':             fields.char(string="Name", size=128, required=True),
        'description':      fields.text(string="Description"),
        'responsible_id':   fields.many2one('res.users', string="Responsible", required=True),
        'session_ids':      fields.one2many('openacademy.session', 'course_id', string="Sessions"),
    }
    
    _sql_constraints = [
        ('name_description_check',
        'CHECK(name <> description)',
        'The course title must be different from its description.'),
        
        ('name_unique',
        'UNIQUE(name)',
        'The course title must be unique.')
    ]

class session (osv.Model):
    _name = 'openacademy.session'
    
    def compute_available_seats(self, seats, attendee_ids):
        if seats == 0 or len(attendee_ids) > seats:
            return 0.0
        else:
            return 100.0 - (float(len(attendee_ids)) / seats * 100)
    
    def get_available_seats(self, cr, uid, ids, field, arg, context={}):
        res = {}
        sessions = self.browse(cr, uid, ids, context=context)
        for session in sessions:
            res[session.id] = self.compute_available_seats(session.seats, session.attendee_ids)
        return res
    
    def onchange_seats(self, cr, uid, ids, seats, attendee_ids, context={}):
        res = {
            'value': {
                'available_seats': self.compute_available_seats(seats, attendee_ids)
                }
        }
        if seats < 0:
            res['warning'] = {
                'title':    'Warning: wrong value',
                'message':  'The seats number cannot be negative.'
            }
        elif seats < len(attendee_ids):
            res['warning'] = {
                'title':    'Warning: wrong value',
                'message':  'There is not enough seats for everyone.'
            }
        return res
    
    _columns = {
        'name':         fields.char(string="Name", size=128, required=True),
        'start_date':   fields.date(string="Start date"),
        'duration':     fields.float(string="Duration", digits=(6,2), help="Session durantion in days"),
        'seats':        fields.integer(string="Number of seats"),
        'instructor_id':fields.many2one('res.partner', string="Instructor", ondelete="set null",
                                        domain="['|',('instructor','=',True),('category_id.name','in',['Teacher level 1', 'Teacher level 2'])]"),
        'course_id':    fields.many2one('openacademy.course', string="Course", ondelete="cascade"),
        'attendee_ids': fields.one2many('openacademy.attendee', 'session_id', string="Attendees"),
        'available_seats':  fields.function(get_available_seats, type="float", string="Available Seats (%)", readonly=True)
    }
    
    def _check_instructor_not_in_attendees(self, cr, uid, ids, context={}):
        for session in self.browse(cr, uid, ids, context=context):
            #partners = []
            #for attendee in session.attendee_ids:
            #    partners.append(attendee.partner_id)
            partners = [attendee.partner_id for attendee in session.attendee_ids]
            if session.instructor_id and session.instructor_id in partners:
                return False
        return True
    
    _constraints = [
        (_check_instructor_not_in_attendees,
        "The instructor cannot be also an attendee.",
        ['instructor_id', 'attendee_ids'])
    ]

class attendee (osv.Model):
    _name = 'openacademy.attendee'
    
    _rec_name = 'partner_id'
    _order = 'partner_id'
    
    _columns = {
        'partner_id':   fields.many2one('res.partner', string="Partner"),
        'session_id':   fields.many2one('openacademy.session', string="Attended session", ondelete="cascade"),
        'partner_id_mobile':    fields.related('partner_id','mobile',string='Mobile',type="char",readonly=True),
        'partner_id_country':   fields.related('partner_id','country_id','name',string='Country',type="char",readonly=True),
    }
    
    _sql_constraints = [
        ('partner_session_unique',
        'UNIQUE(partner_id, session_id)',
        'You cannot add an attendee multiple times on the same session.')
    ]

class resPartner (osv.Model):
    #_name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'instructor':    fields.boolean(string="Instructor"),
        'attendee_ids':     fields.one2many('openacademy.attendee', 'partner_id', string="Sessions"),
    }











