#!/usr/bin/env python3
"""
Emergence Monitor - Real-time pattern discovery monitoring
Watch patterns emerge without prejudice
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List, Any
import requests
import argparse
from datetime import datetime
import signal
import sys

class EmergenceMonitor:
    """
    Real-time monitoring of pattern emergence
    Displays discoveries as they happen
    """
    
    def __init__(self, ml_bridge_url: str = "http://localhost:8000"):
        self.ml_bridge_url = ml_bridge_url
        self.running = True
        self.last_discovery_count = 0
        self.discovery_log = []
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print("\n🛑 Shutting down emergence monitor...")
        self.running = False
    
    async def monitor_realtime(self, refresh_rate: int = 5):
        """Monitor emergence in real-time"""
        print("🌟 SOLAR EMERGENCE - Real-time Discovery Monitor")
        print("=" * 50)
        print(f"Monitoring: {self.ml_bridge_url}")
        print(f"Refresh rate: {refresh_rate} seconds")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        while self.running:
            try:
                # Get current intelligence state
                response = requests.get(f"{self.ml_bridge_url}/intelligence/state", timeout=5)
                if response.status_code == 200:
                    state = response.json()
                    self._display_current_state(state)
                
                # Get recent discoveries
                discoveries_response = requests.get(f"{self.ml_bridge_url}/discoveries/recent?limit=5", timeout=5)
                if discoveries_response.status_code == 200:
                    discoveries = discoveries_response.json()
                    self._display_discoveries(discoveries)
                
                # Get pattern evolution
                evolution_response = requests.get(f"{self.ml_bridge_url}/patterns/evolution", timeout=5)
                if evolution_response.status_code == 200:
                    evolution = evolution_response.json()
                    self._display_pattern_evolution(evolution)
                
                await asyncio.sleep(refresh_rate)
                
            except requests.RequestException as e:
                print(f"⚠️  Connection error: {e}")
                await asyncio.sleep(refresh_rate * 2)
            except KeyboardInterrupt:
                break
    
    def _display_current_state(self, state: Dict):
        """Display current intelligence state"""
        # Clear screen and show header
        print("\033[2J\033[H")  # Clear screen, move cursor to top
        print("🌟 SOLAR EMERGENCE - LIVE DISCOVERY MONITOR")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Intelligence metrics
        print("📊 INTELLIGENCE STATE")
        print("-" * 20)
        print(f"Videos Processed: {state.get('videos_processed', 0)}")
        print(f"Total Patterns: {state.get('total_patterns', 0)}")
        print(f"Total Correlations: {state.get('total_correlations', 0)}")
        print(f"Unknown Space Used: {state.get('unknown_space_used', 0):.1%}")
        
        # Intelligence metrics
        metrics = state.get('intelligence_metrics', {})
        if metrics:
            print(f"Pattern Diversity: {metrics.get('pattern_diversity', 0)}")
            print(f"Correlation Density: {metrics.get('correlation_density', 0)}")
            print(f"Discovery Rate: {metrics.get('discovery_rate', 0):.2f} patterns/video")
        
        print()
    
    def _display_discoveries(self, discoveries_data: Dict):
        """Display recent discoveries"""
        discoveries = discoveries_data.get('discoveries', [])
        
        print("🔍 RECENT DISCOVERIES")
        print("-" * 20)
        
        if not discoveries:
            print("No recent discoveries")
        else:
            for discovery in discoveries[-3:]:  # Show last 3
                video_num = discovery.get('video', 'Unknown')
                patterns = discovery.get('patterns_found', 0)
                correlations = discovery.get('correlations_found', 0)
                unknown = discovery.get('unknown_signals', 0)
                timestamp = discovery.get('timestamp', '')
                
                print(f"Video {video_num}: {patterns}P, {correlations}C, {unknown}U [{timestamp[:19]}]")
        
        print()
    
    def _display_pattern_evolution(self, evolution: Dict):
        """Display pattern evolution"""
        print("📈 PATTERN EVOLUTION")
        print("-" * 20)
        
        timeline = evolution.get('evolution_timeline', [])
        if timeline:
            # Show trend
            if len(timeline) >= 2:
                recent = timeline[-2:]
                trend = "📈" if recent[-1].get('patterns_found', 0) > recent[-2].get('patterns_found', 0) else "📉"
                print(f"Trend: {trend}")
        
        # Show emergence events
        emergence = evolution.get('emergence_events', [])
        if emergence:
            print("🌟 Recent Emergence Events:")
            for event in emergence[-3:]:
                video = event.get('video', 'Unknown')
                pattern = event.get('pattern', 'Unknown pattern')
                strength = event.get('initial_strength', 0)
                print(f"  Video {video}: {pattern} (strength: {strength:.2f})")
        else:
            print("No emergence events detected")
        
        print()
    
    def monitor_file_based(self, discovery_dir: str = "./data/discoveries"):
        """Monitor discoveries through file system"""
        discovery_path = Path(discovery_dir)
        
        print("📁 FILE-BASED DISCOVERY MONITOR")
        print("-" * 30)
        print(f"Watching: {discovery_path}")
        
        if not discovery_path.exists():
            print("❌ Discovery directory not found")
            return
        
        last_modification = 0
        
        while self.running:
            try:
                # Check for new files
                json_files = list(discovery_path.rglob("*.json"))
                
                for file_path in json_files:
                    if file_path.stat().st_mtime > last_modification:
                        self._process_discovery_file(file_path)
                        last_modification = file_path.stat().st_mtime
                
                time.sleep(2)
                
            except KeyboardInterrupt:
                break
    
    def _process_discovery_file(self, file_path: Path):
        """Process a discovery file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            print(f"🔍 New discovery file: {file_path.name}")
            
            if "patterns_found" in data:
                print(f"  Patterns: {data['patterns_found']}")
            
            if "correlations_found" in data:
                print(f"  Correlations: {data['correlations_found']}")
            
            if "unknown_signals" in data:
                print(f"  Unknown signals: {data['unknown_signals']}")
            
            print(f"  Timestamp: {data.get('timestamp', 'Unknown')}")
            print()
            
        except Exception as e:
            print(f"⚠️  Error processing {file_path}: {e}")
    
    def display_summary(self):
        """Display final summary"""
        print("📊 EMERGENCE MONITORING SUMMARY")
        print("-" * 30)
        print(f"Total discoveries logged: {len(self.discovery_log)}")
        print(f"Monitoring duration: Session complete")
        print("✅ Monitor shutdown complete")

def main():
    parser = argparse.ArgumentParser(description="Monitor emergent pattern discovery")
    parser.add_argument("--realtime", action="store_true", help="Real-time monitoring via API")
    parser.add_argument("--file-based", action="store_true", help="File-based monitoring")
    parser.add_argument("--url", default="http://localhost:8000", help="ML Bridge URL")
    parser.add_argument("--refresh", type=int, default=5, help="Refresh rate in seconds")
    parser.add_argument("--discovery-dir", default="./data/discoveries", help="Discovery directory")
    
    args = parser.parse_args()
    
    monitor = EmergenceMonitor(ml_bridge_url=args.url)
    
    try:
        if args.realtime:
            asyncio.run(monitor.monitor_realtime(refresh_rate=args.refresh))
        elif args.file_based:
            monitor.monitor_file_based(discovery_dir=args.discovery_dir)
        else:
            print("Please specify --realtime or --file-based monitoring mode")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    
    finally:
        monitor.display_summary()

if __name__ == "__main__":
    main()