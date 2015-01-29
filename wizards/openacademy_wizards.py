from openerp.osv import osv, fields

class AttendeeWizard (osv.TransientModel):
    _name = 'openacademy.wizard.attendee'
    
    _columns = {
        'name':     fields.many2one('res.partner', 'Partner', required=True),
        'wizard_id':fields.many2one('openacademy.wizard.attendee.create','Wizard'),
    }

class CreateAttendeeWizard (osv.TransientModel):
    _name = 'openacademy.wizard.attendee.create'
    
    def _get_active_session(self, cr, uid, context={}):
        if context.get('active_model') == 'openacademy.session':
            return context.get('active_id', False)
        return False
    
    _columns = {
        'session_ids':   fields.many2many('openacademy.session', 'wizard_session_rel', 'wizard_id', 'session_id', 'Session', required=True),
        'attendee_ids': fields.one2many('openacademy.wizard.attendee','wizard_id','Attendees'),
    }
    
    _defaults = {
        #'session_id': _get_active_session,
    }
    
    """
    def action_add_attendee(self, cr, uid, ids, context={}):
        attendee_model = self.pool.get('openacademy.attendee')
        wizard = self.browse(cr, uid, ids[0], context=context)
        for attendee in wizard.attendee_ids:
            attendee_model.create(cr, uid, {
                'partner_id': attendee.name.id,
                'session_id': wizard.session_id.id,
            })
        return {}
    """
        
    def action_add_attendee(self, cr, uid, ids, context={}):
        session_model = self.pool.get('openacademy.session')
        wizard = self.browse(cr, uid, ids[0], context=context)
        session_ids = [sess.id for sess in wizard.session_ids]
        attendee_data = [{'partner_id': att.name.id} for att in wizard.attendee_ids]
        session_model.write(cr, uid, session_ids, {
            'attendee_ids': [(0,0,data) for data in attendee_data]
        }, context=context)
        return {}
        
    
