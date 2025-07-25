# Video Generator API Workflow

## Complete Workflow (Use ALL Steps)

### Step 1: Upload PDF
```bash
POST /upload-pdf
# Returns: pdf_id, slide_files[], total_pages
```

### Step 2: Parse Script (DON'T SKIP!)
```bash
POST /parse-script
# Upload timestamped script file
# Returns: script_id, parsed_segments[], total_duration
```

### Step 3: Generate Video
```bash
POST /generate-video
# Use: slide_files from Step 1 + parsed_segments from Step 2
```

## ⚠️ Common Mistakes
- **DON'T** manually create script segments
- **DON'T** bypass the script parser
- **DO** use all three endpoints in sequence

## Example Integration
See `tests/test_pdf_upload.py` for complete workflow example. 