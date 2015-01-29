<html>
<head>
    <style type="text/css">${css}</style>
</head>
<body>
    <% setLang(user.lang) %>
    <h1>Session Information</h1>
    %for session in objects:
        <h2>${session.name} - ${session.course_id.name}</h2>
        <table class="list_table">
            <tr>
                <td>Responsible: ${session.instructor_id.name}</td>
            <tr>
            </tr>
                <td>Start date: ${session.start_date}</td>
            <tr>
            </tr>
                <td>Duration: ${session.duration} days</td>
            <tr>
            </tr>
                <td>Seats available: ${session.available_seats}%</td>
            </tr>
        </table>
        <table border="1">
            <tr>
                <th colspan="2">Attendants:</th>
            </tr>
            <tr>
                <td>ID</td>
                <td>Name</td>
            </tr>
            %for attendee in session.attendee_ids:
                <tr>
                    <td>${attendee.partner_id.ref}</td>
                    <td>${attendee.partner_id.name}</td>
                </tr>
            %endfor
        </table>
    %endfor
</body>
</html>
