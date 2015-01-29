from openerp.osv import osv, fields

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











