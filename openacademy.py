from openerp.osv import osv, fields
from datetime import datetime, timedelta


class course (osv.Model):
    _name = 'openacademy.course'
    
    _columns = {
        'name':             fields.char(string="Name", size=128, required=True),
        'description':      fields.text(string="Description"),
        'responsible_id':   fields.many2one('res.users', string="Responsible", required=True, select="True"),
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
    
    def copy(self, cr, uid, id, default=None, context={}):
        course_brw = self.browse(cr, uid, id, context=context)
        new_name = course_brw.name
        while self.search(cr, uid, [('name', '=ilike', new_name)], count=True, context=context) != 0:
            new_name = "%s (copy)" % new_name
        default['name'] = new_name
        return super(course, self).copy(cr, uid, id, default, context=context)

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
    
    def _compute_end_date(self, cr, uid, ids, fields, arg, context={}):
        res = {}
        for session in self.browse(cr, uid, ids, context=context):
            if session.start_date and session.duration:
                start_date = datetime.strptime(session.start_date, "%Y-%m-%d")
                duration = timedelta(days=(session.duration-1))
                end_date = start_date + duration
                res[session.id] = end_date.strftime('%Y-%m-%d')
            else:
                res[session.id] = session.start_date
        return res
    
    def _set_end_date(self, cr, uid, id, field, value, arg, context={}):
        session = self.browse(cr, uid, id, context=context)
        if session.start_date and value:
            start_date = datetime.strptime(session.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(value[:10], "%Y-%m-%d")
            duration = end_date - start_date
            self.write(cr, uid, id, {'duration': (duration.days + 1)}, context=context)
    
    def _compute_hours(self, cr, uid, ids, fields, arg, context={}):
        res = {}
        for session in self.browse(cr, uid, ids, context=context):
            res[session.id] = (session.duration * 24 if session.duration else 0)
            """
            if session.duration:
                res[session.id] = session.duration * 24
            else:
                res[session.id] = 0
                """
        return res
    
    def _compute_attendee_count(self, cr, uid, ids, fields, arg, context={}):
        res = {}
        for session in self.browse(cr, uid, ids, context=context):
            res[session.id] = len(session.attendee_ids)
        return res
    
    def _set_hours(self, cr, uid, id, field, value, arg, context={}):
        if value:
            self.write(cr, uid, id, {'duration':(value/24)}, context=context)
    
    def action_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        
    def action_confirmed(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'confirmed'}, context=context)
        
    def action_done(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)
    
    _columns = {
        'name':         fields.char(string="Name", size=128, required=True),
        'start_date':   fields.date(string="Start date"),
        'duration':     fields.float(string="Duration", digits=(6,2), help="Session durantion in days"),
        'seats':        fields.integer(string="Number of seats"),
        'instructor_id':fields.many2one('res.partner', string="Instructor", ondelete="set null",
                                        domain="['|',('instructor','=',True),('category_id.name','in',['Teacher level 1', 'Teacher level 2'])]"),
        'course_id':    fields.many2one('openacademy.course', string="Course", ondelete="cascade"),
        'attendee_ids': fields.one2many('openacademy.attendee', 'session_id', string="Attendees"),
        'available_seats':  fields.function(get_available_seats, type="float", string="Available Seats (%)", readonly=True),
        'active':       fields.boolean(string="Active", help="Uncheck this to deactivate this session. Beware, it will not appear anymore in the session list."),
        'end_date':     fields.function(_compute_end_date, fnct_inv=_set_end_date, type="date", string="End date"),
        'hours':        fields.function(_compute_hours, fnct_inv=_set_hours, type="float", string="Hours"),
        'attendee_count':   fields.function(_compute_attendee_count, type="integer", string="Attendee Count", store=True),
        'color':        fields.integer('Color'),
        'state':        fields.selection([('draft','Draft'),('confirmed','Confirmed'),('done','Done')], string="State"),
    }
    
    _defaults = {
        'start_date':   fields.date.today,
        'active':       True,
        'state':        'draft',
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











