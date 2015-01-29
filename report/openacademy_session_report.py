from report import report_sxw
import time

class SessionInformation (report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(SessionInformation, self).__init__(cr, uid, name, context=context)
        
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw(
    'report.openacademy_session_information',
    'openacademy.session',
    'addons/openacademy/report/openacademy_session_report.rml',
    parser=SessionInformation,
    header=False
)
report_sxw.report_sxw(
    'report.openacademy_session_information_webkit',
    'openacademy.session',
    'addons/openacademy/report/openacademy_session_report.mako',
    parser=SessionInformation,
    header=False
)


