#!/usr/bin/env python3
import subprocess
import time
import random
import argparse
import os
import sys
import signal

class FixedSpammer:
    def __init__(self, target, sms=10, calls=5, delay=2):
        self.target = target.lstrip('+')
        self.sms_count = sms
        self.call_count = calls
        self.delay = delay
        self.stats = {'sms': 0, 'calls': 0, 'errors': []}
        
    def debug(self, msg):
        print(f"[DEBUG] {msg}")
        
    def test_permissions(self):
        """Test all required permissions"""
        tests = {
            'SMS': 'termux-sms-list',
            'Phone': 'termux-telephony-deviceinfo',
            'API': 'termux-api-version'
        }
        
        for name, cmd in tests.items():
            try:
                result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ {name} permission OK")
                else:
                    print(f"❌ {name} failed: {result.stderr}")
                    return False
            except:
                print(f"❌ {name} command not found")
                return False
        return True
    
    def send_sms(self, msg="Test"):
        """Robust SMS sending"""
        cmd = ['termux-sms-send', '-n', self.target, msg[:160]]  # SMS limit
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                self.stats['sms'] += 1
                print(f"✅ SMS #{self.stats['sms']}")
                return True
            else:
                print(f"❌ SMS: {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            print("❌ SMS timeout")
        except Exception as e:
            print(f"❌ SMS error: {e}")
        return False
    
    def make_call(self):
        """Robust calling"""
        cmd = ['termux-telephony-call', self.target]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"📞 Call #{self.stats['calls']+1}")
                self.stats['calls'] += 1
                time.sleep(5)  # Hold call 5s
                return True
            else:
                print(f"❌ Call: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ Call error: {e}")
        return False
    
    def run(self):
        if not self.test_permissions():
            print("❌ Fix permissions first!")
            return
        
        print(f"\n🎯 Target: +63{self.target}")
        print(f"📊 Plan: {self.sms_count} SMS, {self.call_count} calls\n")
        
        # SMS spam
        print("🚀 SMS PHASE")
        for i in range(self.sms_count):
            self.send_sms(f"Pentest {i+1}/{self.sms_count}")
            time.sleep(self.delay)
        
        # Call spam  
        print("\n📞 CALL PHASE")
        for i in range(self.call_count):
            self.make_call()
            time.sleep(self.delay * 2)
        
        print(f"\n✅ COMPLETE: {self.stats['sms']} SMS, {self.stats['calls']} calls")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Phone number")
    parser.add_argument("-s", "--sms", type=int, default=10)
    parser.add_argument("-c", "--calls", type=int, default=5) 
    parser.add_argument("-d", "--delay", type=float, default=2.0)
    
    args = parser.parse_args()
    spammer = FixedSpammer(args.target, args.sms, args.calls, args.delay)
    spammer.run()
