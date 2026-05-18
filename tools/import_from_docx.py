#!/usr/bin/env python3
"""
import_from_docx.py - Import slide content from Visual_Library_Script.docx into library.json.

Usage:
    python3 tools/import_from_docx.py path/to/Visual_Library_Script.docx [path/to/images_folder]
"""

import json
import os
import re
import shutil
import string
import random
import sys

try:
    import docx
except ImportError:
    print("ERROR: python-docx not installed. Run: pip install python-docx")
    sys.exit(1)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY_PATH = os.path.join(REPO_ROOT, 'data', 'library.json')
MEDIA_IMAGES_DIR = os.path.join(REPO_ROOT, 'media', 'images')

MODULE_MAP = {
    '01 planning':                               'planning',
    '02 survey & existing conditions':           'm_iqodh',
    '03 grading & earthwork construction & ada': 'm_g0bg0',
    '04 roadway design':                         'm_j7ovf',
    '05 stormwater & storm drain':               'm_b68tp',
    '06 water & sewer':                          'm_qk8f3',
    '07 erosion & sediment control':             'm_8e8ua',
    '08 final as-built environment':             'm_r6pef',
}

def bid():
    return 'b_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def sid():
    return 's_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def norm(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip().lower()

def parse_docx(path):
    doc = docx.Document(path)
    from docx.oxml.ns import qn

    slides_by_module = {}
    current_module = None
    pending = {}

    def flush(pending, current_module, slides_by_module):
        if pending and current_module is not None:
            slides_by_module.setdefault(current_module, []).append(dict(pending))
            pending.clear()

    for block in doc.element.body:
        tag = block.tag.split('}')[-1]

        if tag == 'p':
            style_el = block.find('.//' + qn('w:pStyle'))
            style = style_el.get(qn('w:val')) if style_el is not None else 'Normal'
            text = ''.join(n.text or '' for n in block.iter() if n.tag.split('}')[-1] == 't').strip()

            if style == 'Heading1':
                flush(pending, current_module, slides_by_module)
                current_module = norm(text)
                continue

            if style == 'Heading2' and text.lower().startswith('image'):
                flush(pending, current_module, slides_by_module)
                pending = {'_heading': text}
                continue

            if not text:
                continue

            if text.lower().startswith('narration script'):
                script = re.sub(r'^narration script[^:]*:\s*', '', text, flags=re.IGNORECASE)
                pending['narration_script'] = script

            elif text.lower().startswith('intern takeaway'):
                takeaway = re.sub(r'^intern takeaway[:\s]*', '', text, flags=re.IGNORECASE)
                pending['key_lesson'] = takeaway

        elif tag == 'tbl':
            rows = {}
            for row in block.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr'):
                cells = []
                for cell in row.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc'):
                    cells.append(''.join(
                        n.text or '' for n in cell.iter() if n.tag.split('}')[-1] == 't'
                    ).strip())
                if len(cells) >= 2:
                    rows[cells[0]] = cells[1]
            pending['original_filename'] = rows.get('Original Filename', '')
            pending['suggested_title']   = rows.get('Suggested Title', '')
            pending['caption']           = rows.get('Caption', '')
            pending['suggested_filename']= rows.get('Suggested Filename', '')
            pending['alt_text']          = rows.get('Alt Text', '')

    flush(pending, current_module, slides_by_module)
    return slides_by_module

def build_library(slides_by_module, images_folder=None):
    with open(LIBRARY_PATH) as f:
        lib = json.load(f)

    existing_by_module = {}
    for mod in lib['modules']:
        by_title = {}
        for s in mod['slides']:
            key = norm(s.get('title', ''))
            if key and key not in ('first slide', 'new slide', ''):
                by_title[key] = s
        existing_by_module[mod['id']] = {'by_title': by_title}

    img_lookup = {}
    if images_folder and os.path.isdir(images_folder):
        for dirpath, _dirs, fnames in os.walk(images_folder):
            for fname in fnames:
                img_lookup[norm(fname)] = os.path.join(dirpath, fname)

    os.makedirs(MEDIA_IMAGES_DIR, exist_ok=True)
    stats = {'matched': 0, 'new': 0, 'images_copied': 0, 'images_missing': []}

    for mod in lib['modules']:
        mod_key = None
        for k, v in MODULE_MAP.items():
            if v == mod['id']:
                mod_key = k
                break
        if mod_key is None:
            continue

        doc_slides = slides_by_module.get(mod_key, [])
        if not doc_slides:
            continue

        by_title = existing_by_module.get(mod['id'], {}).get('by_title', {})
        new_slides = []

        for ds in doc_slides:
            title = ds.get('suggested_title') or ds.get('_heading', 'Untitled')
            title = re.sub(r'^image \d+ of \d+\s*', '', title, flags=re.IGNORECASE).strip()
            if not title:
                title = 'Untitled'

            existing = by_title.get(norm(title))
            if existing:
                slide_id = existing['id']
                stats['matched'] += 1
            else:
                slide_id = sid()
                stats['new'] += 1

            img_src = None
            orig_fn = ds.get('original_filename', '')
            dest_fn = slide_id + '-A' + os.path.splitext(orig_fn)[1] if orig_fn else slide_id + '-A.png'
            dest_path = os.path.join(MEDIA_IMAGES_DIR, dest_fn)

            if img_lookup:
                src_path = img_lookup.get(norm(orig_fn))
                if src_path:
                    shutil.copy2(src_path, dest_path)
                    img_src = 'media/images/' + dest_fn
                    stats['images_copied'] += 1
                else:
                    stats['images_missing'].append({'slide': title, 'looking_for': orig_fn})
            elif existing:
                pair_block = next((b for b in existing.get('blocks', []) if b['type'] == 'imagePair'), None)
                if pair_block and pair_block.get('images'):
                    img_src = pair_block['images'][0].get('src')

            narration = existing.get('narration') if existing else None
            if not narration:
                narration = {'audio': None, 'mime': None, 'duration': 0,
                             'script': ds.get('narration_script', '')}
            else:
                narration = dict(narration)
                narration['script'] = ds.get('narration_script', narration.get('script', ''))

            slide = {
                'id': slide_id,
                'title': title,
                'subtitle': '',
                'pairing': 'real-vs-cad',
                'level': 1,
                'status': 'draft',
                'tags': '',
                'narration': narration,
                'annotations': existing.get('annotations', []) if existing else [],
                'speakerNotes': existing.get('speakerNotes', '') if existing else '',
                'projectContext': existing.get('projectContext', '') if existing else '',
                'resources': existing.get('resources', '') if existing else '',
                'imageLayout': 'one',
                'blocks': [
                    {
                        'id': bid(),
                        'type': 'imagePair',
                        'layout': 'one',
                        'images': [
                            {'src': img_src, 'label': ds.get('alt_text', ''), 'type': 'Real-world photo'},
                            {'src': None, 'label': '', 'type': 'CAD plan view'},
                        ],
                    },
                    {'id': bid(), 'type': 'keyLesson', 'text': ds.get('key_lesson', '')},
                    {'id': bid(), 'type': 'teaching', 't1': '', 't2': '', 't3': '', 't4': '', 't5': ''},
                ],
            }
            new_slides.append(slide)

        mod['slides'] = new_slides

    lib['updated'] = '2026-05-18'
    return lib, stats

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/import_from_docx.py path/to/script.docx [path/to/images]")
        sys.exit(1)

    docx_path = sys.argv[1]
    images_folder = sys.argv[2] if len(sys.argv) > 2 else None

    print("Parsing " + docx_path + " ...")
    slides_by_module = parse_docx(docx_path)

    total = sum(len(v) for v in slides_by_module.values())
    print("Found " + str(total) + " slides across " + str(len(slides_by_module)) + " modules")
    for k, v in slides_by_module.items():
        print("  " + k + ": " + str(len(v)) + " slides")

    print("\nBuilding library ...")
    lib, stats = build_library(slides_by_module, images_folder)

    with open(LIBRARY_PATH, 'w') as f:
        json.dump(lib, f, indent=2, ensure_ascii=False)
        f.write('\n')

    print("\ndone - wrote " + LIBRARY_PATH)
    print("  " + str(stats['matched']) + " slides matched to existing IDs")
    print("  " + str(stats['new']) + " new slides created")
    print("  " + str(stats['images_copied']) + " images copied to media/images/")
    if stats['images_missing']:
        print("\n  " + str(len(stats['images_missing'])) + " images NOT found:")
        for m in stats['images_missing']:
            print("    [" + m['slide'] + "]  looking for: " + m['looking_for'])
    else:
        print("  All images resolved")

if __name__ == '__main__':
    main()