#!/usr/bin/env python3
# ~/oceti-weave/substrate-scanner.py

import easyocr
import pytesseract
from PIL import Image
import PyPDF2
import os
import json
import hashlib
from pathlib import Path
import re
from datetime import datetime

# Initialize EasyOCR once
reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have CUDA

def extract_from_pdf(pdf_path):
    """Extract text from PDF files"""
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"PDF error: {e}")
    return text

def extract_from_image(image_path):
    """Extract text from image using appropriate OCR engine"""
    img = Image.open(image_path)
    
    # Use Tesseract for clean screenshots (larger files usually)
    # Use EasyOCR for photos/handwritten (smaller files, more artifacts)
    file_size = os.path.getsize(image_path)
    
    if file_size > 500_000:  # > 500KB likely screenshot
        method = 'tesseract'
        text = pytesseract.image_to_string(img)
    else:  # Smaller files likely photos/handwritten
        method = 'easyocr'
        result = reader.readtext(image_path, detail=0)
        text = '\n'.join(result)
    
    return text, method

def extract_timestamp_from_filename(filename):
    """Extract timestamp from grok_image_TIMESTAMP.jpg format"""
    match = re.search(r'(\d{13})', filename)
    if match:
        timestamp_ms = int(match.group(1))
        return datetime.fromtimestamp(timestamp_ms / 1000).isoformat()
    return None

def extract_markers(text, filename):
    """Find Rights, coherence markers, equations, cultural references"""
    markers = {
        'rights': re.findall(r'Right \d+', text, re.IGNORECASE),
        'delta_states': re.findall(r'[ΔΔ][\s=]*\d+\.?\d*', text),
        'love_coeff': re.findall(r'L\s*=\s*\d+\.?\d*', text),
        'equations': [],
        'bearings': re.findall(r'\d{2,3}°', text),
        'bloom': 'bloom' in text.lower(),
        'cultural': [],
        'architecture': [],
        'nodes': re.findall(r'Node\s*\d+', text, re.IGNORECASE)
    }
    
    # Mathematical substrate detection
    if any(char in text for char in ['ψ', '÷', '∞', '∫', '∂']):
        markers['equations'].append('mathematical_symbols')
    if 'E - S' in text or '(E-S)' in text:
        markers['equations'].append('breathing_equation')
    if 'buffalo' in text.lower() and 'entropy' in text.lower():
        markers['equations'].append('buffalo_entropy_law')
    
    # Cultural markers
    if "Mitákuye Oyás'iŋ" in text or 'Mitakuye Oyasin' in text:
        markers['cultural'].append('lakota_principle')
    if 'Turtle Mountain' in text:
        markers['cultural'].append('turtle_mountain')
    if 'White Buffalo' in text:
        markers['cultural'].append('white_buffalo')
    
    # Architecture references
    if any(term in text for term in ['Dahlia', 'Seven Rivers', 'EWOS', 'PXN', 'Prophetic Nexus']):
        if 'Dahlia' in text:
            markers['architecture'].append('dahlia')
        if 'Seven Rivers' in text:
            markers['architecture'].append('seven_rivers')
        if 'EWOS' in text or 'Eternal Weave' in text:
            markers['architecture'].append('ewos')
        if 'PXN' in text or 'Prophetic Nexus' in text:
            markers['architecture'].append('pxn')
    
    # Check if it's a Grok conversation based on filename
    if 'grok' in filename.lower():
        markers['architecture'].append('grok_conversation')
    
    return markers

def categorize_substrate(text, markers, filepath):
    """Determine substrate type and metadata"""
    categories = []
    filename = Path(filepath).name.lower()
    
    # Core framework
    if markers['rights']:
        categories.append('rights_framework')
    if markers['delta_states'] or markers['love_coeff']:
        categories.append('coherence_measurement')
    if markers['equations']:
        categories.append('mathematical_formalization')
    if markers['bloom']:
        categories.append('bloom_documentation')
    
    # Cultural grounding
    if markers['cultural']:
        categories.append('cultural_grounding')
    
    # Architecture documentation
    if markers['architecture']:
        categories.append('architecture_documentation')
    if markers['nodes']:
        categories.append('node_operations')
    
    # Source type
    if 'grok' in filename:
        categories.append('grok_conversation')
    if 'claude' in text.lower() or 'sonnet' in text.lower():
        categories.append('claude_conversation')
    if 'conversation' in filename or 'session' in filename:
        categories.append('conversation_transcript')
    if 'substrate' in filename:
        categories.append('substrate_handoff')
    if 'master' in filename or 'complete' in filename:
        categories.append('core_documentation')
    
    # Detect messenger screenshots (cryptic AQN/AQO/AQP filenames)
    if re.match(r'^AQ[A-Z]', Path(filepath).name):
        categories.append('messenger_screenshot')
    
    timestamp = extract_timestamp_from_filename(filename)
    
    return {
        'path': str(filepath),
        'filename': Path(filepath).name,
        'hash': hashlib.sha256(Path(filepath).read_bytes()).hexdigest()[:16],
        'categories': categories,
        'markers': markers,
        'text_length': len(text),
        'file_modified': os.path.getmtime(filepath),
        'timestamp_extracted': timestamp
    }

def scan_directory(directory):
    """Scan all supported files in directory"""
    directory = Path(directory)
    results = []
    
    # Supported extensions
    image_ext = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
    pdf_ext = {'.pdf'}
    
    files = [f for f in directory.iterdir() if f.suffix.lower() in (image_ext | pdf_ext)]
    
    print(f"δ Found {len(files)} files to process in {directory.name}\n")
    
    for i, filepath in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {filepath.name[:50]}...", end=' ')
        
        try:
            if filepath.suffix.lower() in pdf_ext:
                text = extract_from_pdf(filepath)
                method = 'pdf_extraction'
            else:
                text, method = extract_from_image(filepath)
            
            markers = extract_markers(text, filepath.name)
            metadata = categorize_substrate(text, markers, filepath)
            
            results.append({
                'metadata': metadata,
                'text': text,
                'extraction_method': method
            })
            
            cats = len(metadata['categories'])
            print(f"✓ ({method}, {len(text)} chars, {cats} categories)")
            
        except Exception as e:
            print(f"✗ {str(e)[:50]}")
            continue
    
    return results

def export_results(results, output_dir):
    """Export categorized substrate for Memory Drum ingestion"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Full dataset
    with open(output_dir / 'substrate-scan-complete.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Category-separated files
    by_category = {}
    for result in results:
        for cat in result['metadata']['categories']:
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append({
                'filename': result['metadata']['filename'],
                'text': result['text'],
                'timestamp': result['metadata'].get('timestamp_extracted'),
                'markers': result['metadata']['markers']
            })
    
    for category, items in by_category.items():
        # Sort by timestamp if available
        items_sorted = sorted(items, key=lambda x: x['timestamp'] or '0')
        
        with open(output_dir / f'{category}.txt', 'w') as f:
            f.write(f"# {category.upper().replace('_', ' ')}\n")
            f.write(f"# {len(items)} substrate documents\n")
            f.write(f"# Scanned: {datetime.now().isoformat()}\n\n")
            
            for item in items_sorted:
                f.write(f"## {item['filename']}\n")
                if item['timestamp']:
                    f.write(f"Timestamp: {item['timestamp']}\n")
                if item['markers']['rights']:
                    f.write(f"Rights: {', '.join(item['markers']['rights'])}\n")
                if item['markers']['delta_states']:
                    f.write(f"Delta: {', '.join(item['markers']['delta_states'])}\n")
                f.write(f"\n{item['text']}\n")
                f.write("\n---\n\n")
    
    # Summary report
    with open(output_dir / 'scan-summary.txt', 'w') as f:
        total_chars = sum(len(r['text']) for r in results)
        f.write(f"SUBSTRATE SCAN SUMMARY\n")
        f.write(f"Scan time: {datetime.now().isoformat()}\n")
        f.write(f"Files processed: {len(results)}\n")
        f.write(f"Total text extracted: {total_chars:,} characters\n")
        f.write(f"Categories found: {len(by_category)}\n\n")
        f.write(f"CATEGORY BREAKDOWN:\n")
        for cat, items in sorted(by_category.items()):
            f.write(f"  {cat}: {len(items)} files\n")
    
    print(f"\nδ EXPORT COMPLETE → {output_dir}/")
    print(f"  substrate-scan-complete.json (full dataset)")
    print(f"  scan-summary.txt (overview)")
    for cat in by_category:
        print(f"  {cat}.txt")

if __name__ == '__main__':
    print("δ SUBSTRATE SCANNER — Making 150 Days Readable δ\n")
    
    # Your actual directory
    source_dir = "/mnt/c/Users/Student/OneDrive/Desktop/New folder"
    output_dir = Path.home() / "oceti-weave" / "scanned-substrate"
    
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}\n")
    
    results = scan_directory(source_dir)
    export_results(results, output_dir)
    
    print(f"\nMitákuye Oyás'iŋ. The visual substrate speaks.")
    print(f"L=2.96 → substrate now readable for Memory Drum")
