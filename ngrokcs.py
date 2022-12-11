#! pip install pyngrok
from pyngrok import ngrok
import os

if __name__ == '__main__':
    ngrok.set_auth_token(os.getenv('NGROK_AUTH_TOKEN'))
    web_tunnel = ngrok.connect(8080, proto='http')
    mqtt_tunnel = ngrok.connect(1883, proto='tcp')
    print('WEB: ', web_tunnel.public_url)
    print('MQTT: ', mqtt_tunnel.public_url)
    ngrok_process = ngrok.get_ngrok_process()
    try:
        # Block until CTRL-C or some other terminating event
        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        print(" Shutting down server.")
        ngrok.kill()
