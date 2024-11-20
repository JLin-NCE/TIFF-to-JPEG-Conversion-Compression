import os
from PIL import Image
import shutil
from pathlib import Path
import warnings
from PIL import ImageFile
import time
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Disable decompression bomb check as we're handling very large files
Image.MAX_IMAGE_PIXELS = None

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def convert_and_compress(input_path, output_path, target_size_kb=15000):
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    # Create a log file for tracking progress
    log_file = output_path / "conversion_log.txt"
    completed_files = set()
    
    if log_file.exists():
        with open(log_file, 'r') as f:
            completed_files = set(line.strip() for line in f)
    
    def compress_with_dynamic_quality(img, output_path, target_size_kb):
        """Compress image with dynamic quality adjustment"""
        quality = 95  # Start with high quality
        target_size_bytes = target_size_kb * 1024
        
        while quality >= 5:  # Don't go below quality of 5
            try:
                img.save(output_path, 'JPEG', 
                        quality=quality, 
                        optimize=True,
                        progressive=True)  # Use progressive JPEG for large files
                
                current_size = os.path.getsize(output_path)
                if current_size <= target_size_bytes:
                    return True
                
                # Adjust quality based on how far we are from target size
                size_ratio = current_size / target_size_bytes
                if size_ratio > 10:
                    quality -= 20
                elif size_ratio > 5:
                    quality -= 10
                else:
                    quality -= 5
                
            except Exception as e:
                print(f"Compression error at quality {quality}: {e}")
                quality -= 10
                
        return False

    # Walk through the input directory
    for root, dirs, files in os.walk(input_path):
        root_path = Path(root)
        rel_path = root_path.relative_to(input_path)
        current_output_dir = output_path / rel_path
        current_output_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            if file.lower().endswith(('.tif', '.tiff')):
                input_file_path = root_path / file
                output_filename = Path(file).stem + '.jpg'
                output_file_path = current_output_dir / output_filename
                
                # Skip if already processed
                if str(output_file_path) in completed_files:
                    print(f"Skipping already converted: {input_file_path}")
                    continue
                
                try:
                    input_size_mb = get_file_size_mb(input_file_path)
                    print(f"\nProcessing: {input_file_path}")
                    print(f"Input file size: {input_size_mb:.2f} MB")
                    
                    start_time = time.time()
                    
                    with Image.open(input_file_path) as img:
                        # Get image dimensions
                        width, height = img.size
                        print(f"Image dimensions: {width}x{height}")
                        
                        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                            print("Converting to RGB...")
                            img = img.convert('RGB')
                        
                        print("Compressing image...")
                        success = compress_with_dynamic_quality(img, output_file_path, target_size_kb)
                        
                        if success:
                            output_size_mb = get_file_size_mb(output_file_path)
                            compression_ratio = input_size_mb / output_size_mb
                            elapsed_time = time.time() - start_time
                            
                            print(f"Converted: {input_file_path} -> {output_file_path}")
                            print(f"Output size: {output_size_mb:.2f} MB")
                            print(f"Compression ratio: {compression_ratio:.2f}x")
                            print(f"Processing time: {elapsed_time:.1f} seconds")
                            
                            # Log successful conversion
                            with open(log_file, 'a') as f:
                                f.write(str(output_file_path) + '\n')
                            completed_files.add(str(output_file_path))
                        else:
                            print(f"Failed to compress {input_file_path} to target size")
                            if output_file_path.exists():
                                output_file_path.unlink()
                
                except KeyboardInterrupt:
                    print("\nOperation interrupted by user. Progress has been saved.")
                    if output_file_path.exists():
                        output_file_path.unlink()  # Remove partial file
                    raise
                except Exception as e:
                    print(f"Error processing {input_file_path}: {str(e)}")
                    if output_file_path.exists():
                        output_file_path.unlink()

if __name__ == "__main__":
    input_path = r"S:\POelkers\Santa Maria Ortho Imagery"
    output_path = r"S:\POelkers\Santa Maria Resized Ortho Imagery"
    
    try:
        convert_and_compress(input_path, output_path)
        print("\nConversion completed successfully!")
    except KeyboardInterrupt:
        print("\nProgram stopped by user. You can restart it later to continue from where it left off.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
