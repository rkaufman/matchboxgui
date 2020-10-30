import requests
import urllib3
import server.db.db
import server.util.mlUtil as mlUtil


class MxAuth(object):

    @staticmethod
    def login():

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        mx_host = db.get_setting('mx-host').setting
        mx_username = db.get_setting('mx-username').setting
        mx_pass = db.get_setting('mx-pass').setting
        mx_use_tls = mlUtil.to_bool(db.get_setting('mx-use-tls').setting)

        # Note: We're not using this. We'll only need this if the device complains
        #   about connecting to self-signed certs.
        bypass_cert_validation = mlUtil.to_bool(db.get_setting('bypass-cert-validation').setting)

        path = "/handlers/AjaxHandler.asmx/AjaxInvocation"
        protocol = "https://" if mx_use_tls else "http://"
        url = protocol + mx_host + path

        payload = {
            "request": {
                "method": "Authentication.Authenticate",
                "parameters": {
                    "UserName": mx_username,
                    "Password": mx_pass,
                    "RememberPassword ": "true"
                }
            }
        }

        # TODO - handle exception
        success = False
        try:
            response = requests.post(url, json=payload, verify=False, timeout=5)
            response.raise_for_status()
            success = True
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Other login error:", err)
        except urllib3.exceptions.NewConnectionError as errnc:
            print("Could not connect to MXSERVER instance at: {}".format(mx_host))

        if success:
            # Extract auth token
            hdrs = response.headers
            if 'Set-Cookie' in hdrs:
                cookies = hdrs['Set-Cookie']
                cookieList = cookies.split("=")
                authLabel = cookieList[0]
                (authToken, _) = cookieList[1].split(";")
            else:
                success = False
                hdrs = None
                cookies = None
                cookieList = None
                authLabel = None
                authToken = None
        else:
            hdrs = None
            cookies = None
            cookieList = None
            authLabel = None
            authToken = None

        return(success, hdrs, cookies, cookieList, authLabel, authToken)