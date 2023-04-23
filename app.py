import csv
import json
import uuid
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render
from pyramid.response import Response


@view_config(route_name="main")
def home(request):
    html = render('templates\home.html', {}, request=request)
    return Response(html)


@view_config(route_name="upload", request_method="POST")
def benford(request):
    csvfile = request.POST['csvfile'].file

    data_list = []
    reader = csv.reader(csvfile.read().decode('utf-8').splitlines())
    for row in reader:
        data_list.extend(row)

    results, conform = conform_benford_law(data_list)

    if conform == True:
        file_location = f"json/{uuid.uuid1()}file.json"
        with open(file_location, "w+") as f:
            json.dump(results, f)
        # return Response(json.dumps(results))
        # Format the results using json.dumps()
        formatted_results = json.dumps(results)

        # Return the formatted results in a rounded box
        return Response(f'''
            <html>
                <head>
                    <title>Results</title>
                    <style>
                        .container {{
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                        }}
                        
                        .success {{
                            font-size: 24px;
                            font-weight: bold;
                            color: green;
                            margin-bottom: 20px;
                        }}
                        
                        .box {{
                            border: 2px solid black;
                            border-radius: 10px;
                            padding: 20px;
                            text-align: center;
                            background-color: #f0f0f0;
                            width: 1000px;
                            height: auto;
                            overflow: auto;
                            overflow-wrap: break-word;
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="success">Input csv_data conforms to Benford's Law.</div>
                        <div class="box">
                            <pre>{formatted_results}</pre>
                        </div>
                    </div>
                </body>
            </html>
        ''')
    else:
        return Response('<html><head><title>Error</title><style>.container{display:flex;flex-direction:column;justify-content:center;align-items:center;height:100vh;}.error{font-size:24px;font-weight:bold;color:red;}</style></head><body><div class="container"><div class="error">Input csv_data does not conform to Benford\'s Law.</div></div></body></html>')


def conform_benford_law(data_list):
    BENFORD_PERCENTAGES = [0, 0.301, 0.176, 0.125,
                           0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

    first_digits = []
    for data in data_list[1:]:
        if data != '':
            int_data = int(float(data))
            first_digits.append(int_data)

    # Count the number of first digits in the list of numbers
    first_digit_counts = {str(i): 0 for i in range(10)}
    for number in first_digits:
        first_digit = str(number)[0]
        first_digit_counts[first_digit] += 1

    results = []
    for n in range(10):
        data_frequency = first_digit_counts[str(n)]
        data_frequency_percent = data_frequency / len(first_digits)
        benford_frequency = len(first_digits) * BENFORD_PERCENTAGES[n]
        benford_frequency_percent = BENFORD_PERCENTAGES[n]
        difference_frequency = data_frequency - benford_frequency
        difference_frequency_percent = data_frequency_percent - benford_frequency_percent

        results.append({"n": n,
                        "data_frequency": data_frequency,
                        "data_frequency_percent": data_frequency_percent,
                        "benford_frequency": benford_frequency,
                        "benford_frequency_percent": benford_frequency_percent,
                        "difference_frequency": difference_frequency,
                        "difference_frequency_percent": difference_frequency_percent})

    conform = all(results[i]["difference_frequency_percent"]
                  < 0.1 for i in range(1, 10))

    return results, conform


if __name__ == "__main__":
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.add_route('main', '/benford')
        config.add_route('upload', '/upload')
        config.scan()
        config.add_jinja2_renderer('.html')
        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 5050, app)
    server.serve_forever()
