from json import dumps
from httplib2 import Http
from jinja2 import Template

def webhook(user):
    
    url = "chat.google_api_is_req_here"
    msg = f"Hello {user},\nYou have not visited the library."
    app_message = {"text": msg}
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    print(f'Message sent to Google Chat to notify the {user} about the library visit.')




def generate_report_template(user_name, no_of_books, no_of_requests, req_deadlines):
    template_content = """
    <!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>User Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <style>
        .center {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }
        .container {
            margin: 0 auto;
            width: 60%;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        h4 {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ user }}'s Report</h1>
        <div class="card mb-4">
            <div class="card-header">
                <h4>Book Deadlines</h4>
            </div>
            <div class="card-body">
                <ul class="list-group">
                    {% for req in req_deadlines %}
                    <li class="list-group-item"><strong>Book:</strong> {{ req.book_name }} | <strong>Deadline:</strong> {{ req.book_deadline }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>

        <div class="card mb-4">
            <div class="card-header">
                <h4>Statistics</h4>
            </div>
            <div class="card-body">
                <p><strong>Number of Books Issued:</strong> {{ no_of_books }}</p>
                <p><strong>Number of Requests Made:</strong> {{ no_of_requests }}</p>
            </div>
        </div>
    </div>
</body>
</html>

"""

    template = Template(template_content)

    rendered_template = template.render(
        user=user_name,
        no_of_books=no_of_books,
        no_of_requests=no_of_requests,
        req_deadlines=req_deadlines,
    )
    return rendered_template
