"""
The new Google ReCaptcha implementation for Flask without Flask-WTF
Can be used as standalone
"""

__NAME__ = "Flask-ReCaptcha"
__version__ = "0.5.0"
__license__ = "MIT"
__author__ = "Mardix"
__copyright__ = "(c) 2015 Mardix"

try:
    from flask import request, current_app
    try:
        from jinja2 import Markup
    except ImportError:
        from markupsafe import Markup
    import requests
except ImportError as ex:
    print(f"Missing dependencies: {ex}")


class DEFAULTS(object):
    IS_ENABLED = True
    # V3 doesn't have theme, type, size, tabindex. Keep them for compatibility or remove.
    # We'll set default score threshold for v3.
    SCORE_THRESHOLD = 0.5 # Default score threshold for v3
    ACTION = "homepage" # Default action for v3 if not specified

class ReCaptcha(object):

    VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
    site_key = None
    secret_key = None
    is_enabled = False
    score_threshold = DEFAULTS.SCORE_THRESHOLD # For v3
    action = DEFAULTS.ACTION # For v3

    def __init__(self, app=None, site_key=None, secret_key=None, is_enabled=True, **kwargs):
        if site_key:
            self.site_key = site_key
            self.secret_key = secret_key
            self.is_enabled = is_enabled
            self.score_threshold = kwargs.get('score_threshold', DEFAULTS.SCORE_THRESHOLD)
            self.action = kwargs.get('action', DEFAULTS.ACTION)
            # Remove v2 specific parameters if you wish, or keep them but they won't be used by v3
            self.theme = kwargs.get('theme', None) # V2 specific
            self.type = kwargs.get('type', None)   # V2 specific
            self.size = kwargs.get('size', None)   # V2 specific
            self.language = kwargs.get('language', 'en') # V2 specific, but useful for v3 script
            self.tabindex = kwargs.get('tabindex', None) # V2 specific

        elif app:
            self.init_app(app=app)

    def init_app(self, app=None):
        self.__init__(site_key=app.config.get("RECAPTCHA_SITE_KEY"),
                      secret_key=app.config.get("RECAPTCHA_SECRET_KEY"),
                      is_enabled=app.config.get("RECAPTCHA_ENABLED", DEFAULTS.IS_ENABLED),
                      score_threshold=app.config.get("RECAPTCHA_SCORE_THRESHOLD", DEFAULTS.SCORE_THRESHOLD),
                      action=app.config.get("RECAPTCHA_ACTION", DEFAULTS.ACTION),
                      language=app.config.get("RECAPTCHA_LANGUAGE", 'en') # Keep language
                      )

        @app.context_processor
        def get_code():
            return dict(recaptcha_v3=Markup(self.get_code()))

    def get_code(self):
        """
        Returns the new ReCaptcha v3 code for rendering and execution.
        :return:
        """
        if not self.is_enabled:
            return ""

        # V3 script with render parameter
        script_tag = f"<script src='https://www.google.com/recaptcha/api.js?render={self.site_key}&hl={self.language}'></script>"

        # JavaScript function to execute reCAPTCHA and get the token
        # This function should be called by your form submission or other events
        js_code = f"""
        <script>
            function getRecaptchaToken(action_name = '{self.action}') {{
                return new Promise((resolve, reject) => {{
                    grecaptcha.ready(function() {{
                        grecaptcha.execute('{self.site_key}', {{action: action_name}})
                            .then(function(token) {{
                                resolve(token);
                            }})
                            .catch(function(error) {{
                                reject(error);
                            }});
                    }});
                }});
            }}
        </script>
        """
        return script_tag + js_code

    def verify(self, response=None, remote_ip=None, action=None, score_threshold=None):
        if not self.is_enabled:
            return True

        if not response:
            response = request.form.get('g-recaptcha-response')
            if not response:
                # If g-recaptcha-response is missing, it's likely not a valid submission
                # or frontend didn't send it correctly.
                # In v3, frontend must explicitly call grecaptcha.execute and send the token.
                return False

        data = {
            "secret": self.secret_key,
            "response": response,
            "remoteip": remote_ip or request.environ.get('REMOTE_ADDR')
        }

        # Send request to Google for verification
        try:
            r = requests.post(self.VERIFY_URL, data=data)
            r.raise_for_status() # Raise an exception for HTTP errors
            result = r.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"reCAPTCHA verification request failed: {e}")
            return False # Network error or invalid URL
        except ValueError as e: # JSONDecodeError in newer versions of requests
            current_app.logger.error(f"reCAPTCHA verification response not valid JSON: {e}")
            return False # Malformed JSON from Google

        # Check success first
        if not result.get("success"):
            current_app.logger.warning(f"reCAPTCHA verification failed: {result.get('error-codes', 'No error codes provided')}")
            return False

        # For v3, check score and action
        # Use provided score_threshold if available, otherwise use instance default
        current_score_threshold = score_threshold if score_threshold is not None else self.score_threshold
        current_action = action if action is not None else self.action

        recaptcha_score = result.get("score")
        recaptcha_action = result.get("action")

        if recaptcha_score is None:
            current_app.logger.error("reCAPTCHA v3 response missing score.")
            return False

        if recaptcha_score < current_score_threshold:
            current_app.logger.warning(f"reCAPTCHA score {recaptcha_score} is below threshold {current_score_threshold}.")
            return False

        if recaptcha_action and recaptcha_action != current_action:
            current_app.logger.warning(f"reCAPTCHA action '{recaptcha_action}' does not match expected action '{current_action}'.")
            # You might choose to return False here, or just log a warning depending on strictness
            # For strict action matching, uncomment the next line:
            # return False

        return True