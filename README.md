# TIFF to JPEG Image Converter

A Python script for batch converting and compressing large TIFF images to JPEG format while maintaining optimal quality within a specified file size limit.

## Features

- Converts TIFF images to compressed JPEG format
- Maintains directory structure during conversion
- Dynamic quality adjustment to meet target file size
- Progress tracking with resume capability
- Handles transparent and RGBA images
- Progressive JPEG compression for large files
- Detailed logging of conversion metrics

## Prerequisites

Required Python packages:
```
Pillow (PIL)
pathlib
```

## Installation

1. Install the required packages:
```bash
pip install Pillow
```

2. Clone or download this script to your local machine.

## Usage

1. Modify the input and output paths in the script:
```python
input_path = r"S:\POelkers\Santa Maria Ortho Imagery"
output_path = r"S:\POelkers\Santa Maria Resized Ortho Imagery"
```

2. Run the script:
```bash
python image_converter.py
```

## Configuration

The script includes several configurable parameters:

- `target_size_kb`: Maximum target file size in kilobytes (default: 15000)
- `quality`: Initial JPEG quality setting (default: 95)
- Initial quality adjustment thresholds:
  - Size ratio > 10: Reduce quality by 20
  - Size ratio > 5: Reduce quality by 10
  - Otherwise: Reduce quality by 5

## Features in Detail

### Progress Tracking
- Creates a `conversion_log.txt` file in the output directory
- Tracks completed conversions to allow resume after interruption
- Skips already processed files when restarted

### Error Handling
- Graceful handling of keyboard interrupts
- Cleanup of partial files on errors
- Detailed error logging
- Skips problematic files and continues processing

### Image Processing
- Converts RGBA/transparent images to RGB
- Uses progressive JPEG encoding for large files
- Dynamic quality adjustment to meet size constraints
- Preserves original directory structure

## Output Information

The script provides detailed information during conversion:
- Input file size
- Image dimensions
- Output file size
- Compression ratio
- Processing time

## Example Output
```
Processing: input/image.tif
Input file size: 100.50 MB
Image dimensions: 8000x6000
Converting to RGB...
Compressing image...
Converted: input/image.tif -> output/image.jpg
Output size: 14.50 MB
Compression ratio: 6.93x
Processing time: 3.2 seconds
```

## Limitations

- Minimum quality threshold of 5
- Maximum image dimensions determined by available system memory
- Target file size may not always be achievable while maintaining acceptable quality

## Error Recovery

If the script is interrupted:
1. The progress is automatically saved in the conversion log
2. Partial files are cleaned up
3. Simply rerun the script to continue from the last successful conversion

## Safety Features

- Disables PIL decompression bomb check for large files
- Handles truncated images
- Preserves original files
- Removes partial/failed conversion outputs

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open-source and available under the MIT License.
