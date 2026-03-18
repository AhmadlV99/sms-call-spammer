#!/usr/bin/env python3
import subprocess
import time
import random
import argparse
import os
import sys
from datetime import datetime

class SMSCallSpammer:
    def __init__(self, target_number, sms_count=10, call_count=5, delay=2):
        self.target = target_number
        self.sms_count = sms_count
        self.call_count = call_count
        self.delay = delay
        self.log_file = f"logs/spam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        print(log_entry.strip())
        os.makedirs("logs", exist_ok=True)
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
    
    def send_sms(self, message="Test SMS"):
        """Send SMS using Termux API"""
        try:
            cmd = f'termux-sms-send -n {self.target} "{message}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"✅ SMS sent: {message[:30]}...")
                return True
            else:
                self.log(f"❌ SMS failed: {result.stderr}")
                return False
        except Exception as e:
            self.log(f"❌ SMS error: {str(e)}")
            return False
    
    def make_call(self, duration=5):
        """Make call using Termux API"""
        try:
            cmd = f'termux-telephony-call {self.target}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"📞 Call initiated to {self.target}")
                time.sleep(duration)
                subprocess.run('termux-telephony-deviceinfo', shell=True)
                return True
            else:
                self.log(f"❌ Call failed: {result.stderr}")
                return False
        except Exception as e:
            self.log(f"❌ Call error: {str(e)}")
            return False
    
    def spam_sms(self):
        """Spam SMS with random messages"""
        messages = [
            "Test message",
            "Security test",
            "Pentest notification",
            f"#{random.randint(1000,9999)}",
            "Automated test"
        ]
        
        self.log(f"🚀 Starting SMS spam: {self.sms_count} messages")
        success = 0
        
        for i in range(self.sms_count):
            msg = random.choice(messages)
            if self.send_sms(msg):
                success += 1
            time.sleep(self.delay + random.uniform(0, 1))
        
        self.log(f"📊 SMS spam complete: {success}/{self.sms_count} successful")
        return success
    
    def spam_calls(self):
        """Spam calls"""
        self.log(f"📞 Starting call spam: {self.call_count} calls")
        success = 0
        
        for i in range(self.call_count):
            if self.make_call(duration=3):
                success += 1
            time.sleep(self.delay * 2 + random.uniform(1, 3))
        
        self.log(f"📊 Call spam complete: {success}/{self.call_count} successful")
        return success
    
    def run_attack(self):
        """Execute combined SMS + Call attack"""
        self.log(f"🎯 Target: {self.target}")
        self.log(f"📋 Config: SMS={self.sms_count}, Calls={self.call_count}, Delay={self.delay}s")
        
        total_sms = self.spam_sms()
        time.sleep(2)
        total_calls = self.spam_calls()
        
        self.log(f"✅ Attack completed!")
        self.log(f"📈 Summary: {total_sms} SMS + {total_calls} Calls")

def main():
    parser = argparse.ArgumentParser(description="Termux SMS/Call Spammer")
    parser.add_argument("target", help="Target phone number (e.g., +639123456789)")
    parser.add_argument("-s", "--sms", type=int, default=10, help="Number of SMS (default: 10)")
    parser.add_argument("-c", "--calls", type=int, default=5, help="Number of calls (default: 5)")
    parser.add_argument("-d", "--delay", type=float, default=2.0, help="Delay between messages (default: 2s)")
    
    args = parser.parse_args()
    
    # Check Termux API
    try:
        subprocess.run('termux-sms-list', capture_output=True, check=True)
    except:
        print("❌ Install Termux:API from F-Droid and grant SMS/Call permissions!")
        sys.exit(1)
    
    spammer = SMSCallSpammer(args.target, args.sms, args.calls, args.delay)
    spammer.run_attack()

if __name__ == "__main__":
    main()
