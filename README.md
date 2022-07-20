# Document Watermarker
The tool that watermarks all pictures in the docx document.

# How to use

### In terminal:
```
python3 docx_watermarker [path_to_document] [path_to_watermark] [(OPTIONAL) output_file_path]
```


### Using python:
```python
import docx_watermarker

docx_watermarker.watermark_document_images(
    "path/to/file.docx",
    "path/to/watermark.png",
    "path/to/output.docx"  # OPTIONAL
)
```
