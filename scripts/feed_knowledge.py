#!/usr/bin/env python3
"""
Knowledge Feeding Script - Add new knowledge to the corpus
Supports URLs, files, directories, and direct text
"""

import os
import sys
import requests
import shutil
from pathlib import Path
from urllib.parse import urlparse
import argparse
from datetime import datetime

class KnowledgeFeeder:
    """
    Feed knowledge into the corpus for processing
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.raw_inputs = self.project_root / "knowledge-corpus" / "raw-inputs"
        
        # Ensure directories exist
        self.raw_inputs.mkdir(parents=True, exist_ok=True)
        (self.raw_inputs / "documentation").mkdir(exist_ok=True)
        (self.raw_inputs / "papers").mkdir(exist_ok=True)
        (self.raw_inputs / "examples").mkdir(exist_ok=True)
        (self.raw_inputs / "repositories").mkdir(exist_ok=True)
    
    def feed_url(self, url: str, category: str = "documentation"):
        """Download content from URL and add to corpus"""
        print(f"📥 Downloading from URL: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Determine filename from URL
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path) or "downloaded_content"
            
            # Ensure proper extension
            if not Path(filename).suffix:
                if 'pdf' in response.headers.get('content-type', ''):
                    filename += '.pdf'
                elif 'json' in response.headers.get('content-type', ''):
                    filename += '.json'
                else:
                    filename += '.html'
            
            # Save to appropriate category
            output_path = self.raw_inputs / category / filename
            output_path.write_bytes(response.content)
            
            print(f"✅ Downloaded: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")
            return None
    
    def feed_file(self, file_path: str, category: str = None):
        """Add a local file to the corpus"""
        source = Path(file_path)
        
        if not source.exists():
            print(f"❌ File not found: {file_path}")
            return None
        
        # Auto-detect category if not specified
        if category is None:
            if source.suffix.lower() in ['.pdf', '.tex', '.bib']:
                category = "papers"
            elif source.suffix.lower() in ['.py', '.js', '.ts', '.md']:
                category = "documentation"
            elif source.name.lower() in ['readme.md', 'changelog.md', 'license']:
                category = "documentation"
            else:
                category = "examples"
        
        # Copy to corpus
        destination = self.raw_inputs / category / source.name
        shutil.copy2(source, destination)
        
        print(f"✅ Added file: {destination}")
        return destination
    
    def feed_directory(self, dir_path: str, category: str = "documentation"):
        """Add all files from a directory to the corpus"""
        source_dir = Path(dir_path)
        
        if not source_dir.exists():
            print(f"❌ Directory not found: {dir_path}")
            return []
        
        added_files = []
        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                # Skip hidden files and common excludes
                if file_path.name.startswith('.'):
                    continue
                if file_path.suffix in ['.pyc', '.pyo', '.pyd']:
                    continue
                
                # Create relative directory structure
                rel_path = file_path.relative_to(source_dir)
                destination = self.raw_inputs / category / rel_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(file_path, destination)
                added_files.append(destination)
                print(f"✅ Added: {destination}")
        
        print(f"📁 Added {len(added_files)} files from {dir_path}")
        return added_files
    
    def feed_text(self, text: str, filename: str, category: str = "documentation"):
        """Add raw text content to the corpus"""
        destination = self.raw_inputs / category / filename
        destination.write_text(text, encoding='utf-8')
        
        print(f"✅ Added text content: {destination}")
        return destination
    
    def feed_github_repo(self, repo_url: str):
        """Clone a GitHub repository to the corpus"""
        print(f"📥 Cloning repository: {repo_url}")
        
        try:
            # Extract repo name from URL
            repo_name = repo_url.rstrip('/').split('/')[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
            
            # Clone to repositories directory
            destination = self.raw_inputs / "repositories" / repo_name
            
            if destination.exists():
                print(f"⚠️  Repository already exists: {destination}")
                return destination
            
            # Use git clone
            import subprocess
            result = subprocess.run([
                'git', 'clone', '--depth', '1', repo_url, str(destination)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Remove .git directory to save space
                shutil.rmtree(destination / '.git', ignore_errors=True)
                print(f"✅ Cloned repository: {destination}")
                return destination
            else:
                print(f"❌ Failed to clone: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error cloning repository: {e}")
            return None
    
    def list_corpus_contents(self):
        """List current contents of the knowledge corpus"""
        print("\n📚 Current Knowledge Corpus Contents:")
        print("=" * 40)
        
        for category in ['documentation', 'papers', 'examples', 'repositories']:
            category_path = self.raw_inputs / category
            if category_path.exists():
                files = list(category_path.rglob("*"))
                file_count = len([f for f in files if f.is_file()])
                print(f"{category.upper()}: {file_count} files")
                
                # Show recent additions
                recent = sorted([f for f in files if f.is_file()], 
                              key=lambda x: x.stat().st_mtime, reverse=True)[:3]
                for recent_file in recent:
                    rel_path = recent_file.relative_to(category_path)
                    print(f"  - {rel_path}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Feed knowledge into the corpus")
    parser.add_argument("--url", help="Download from URL")
    parser.add_argument("--file", help="Add local file")
    parser.add_argument("--directory", help="Add all files from directory")
    parser.add_argument("--text", help="Add raw text content")
    parser.add_argument("--filename", help="Filename for text content")
    parser.add_argument("--github", help="Clone GitHub repository")
    parser.add_argument("--category", 
                       choices=['documentation', 'papers', 'examples', 'repositories'],
                       default='documentation',
                       help="Category to add content to")
    parser.add_argument("--list", action="store_true", help="List corpus contents")
    parser.add_argument("--process", action="store_true", help="Process corpus after feeding")
    
    args = parser.parse_args()
    
    feeder = KnowledgeFeeder()
    
    if args.list:
        feeder.list_corpus_contents()
        return
    
    added_content = None
    
    if args.url:
        added_content = feeder.feed_url(args.url, args.category)
    elif args.file:
        added_content = feeder.feed_file(args.file, args.category)
    elif args.directory:
        added_content = feeder.feed_directory(args.directory, args.category)
    elif args.text and args.filename:
        added_content = feeder.feed_text(args.text, args.filename, args.category)
    elif args.github:
        added_content = feeder.feed_github_repo(args.github)
    else:
        parser.print_help()
        return
    
    if added_content and args.process:
        print("\n🔄 Processing knowledge corpus...")
        os.system("python3 agents/knowledge_harvester.py")
        os.system("python3 agents/bmad_knowledge_bridge.py")

if __name__ == "__main__":
    main()