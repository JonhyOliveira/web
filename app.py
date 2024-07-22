from flask import Flask, render_template, make_response, redirect, request, jsonify
from urllib.parse import quote_plus
import pathlib
from database import AnalyticsDatabase

BASE_PATH = pathlib.Path(__file__).parent
RICK_ROLL = 'https://shattereddisk.github.io/rickroll/rickroll.mp4'

def create_app():
    app = Flask(__name__, static_url_path='/pub')
    app.jinja_env.filters['quote_plus'] = quote_plus

    @app.context_processor
    def inject_handles():
        return dict(
            linkedin_handle='joao-fv-oliveira',
            github_handle='JonhyOliveira'
        )

    @app.after_request
    def log_request(response):
        if app.static_url_path in request.path:
            return response

        AnalyticsDatabase.track_click(request)
        return response

    @app.get('/favicon.ico')
    def favicon():
        res = make_response(app.send_static_file('favicon.png'))
        res.content_type = 'image/png'
        return res

    @app.get('/')
    def home():
        return render_template('me.html', passion_mode=("p" in request.args.keys()))

    @app.get('/cookie')
    def cookie():
        return render_template('cookie.html', cookie_image=app.url_for('static', filename='give_cookie.jpg'),
                               cookie_redirect=app.url_for('rickroll'))

    @app.get('/index.html')
    def rickroll():
        return redirect(RICK_ROLL, code=302)

    @app.get('/stats')
    def stats():
        return jsonify(AnalyticsDatabase.get_stats())

    return app

if __name__ == '__main__':
    create_app().run(debug=True, extra_files=["descriptions.html"])
else:
    app = create_app()
    def application():
        return app
