import os
import sys
import hashlib

def xor_bytes(data, key):
    return bytes(a ^ b for a, b in zip(data, (key * (len(data) // len(key) + 1))[:len(data)]))

def main(input_file, key_file, output_dir):
    print("Encrypting file " + input_file)

    chunk_size = 10 * 1024 * 1024
    key_chunk_size = 10 * 1024 * 1024

    hasher = hashlib.sha256()

    # Get the size of the input file
    file_size = os.path.getsize(input_file)

    with open(input_file, "rb") as in_file, open(key_file, "rb") as key_file:
        # Compute the checksum over the input file
        while True:
            chunk = in_file.read(chunk_size)
            if not chunk:
                break

            hasher.update(chunk)

        # Get the checksum hex representation
        checksum_hex = hasher.hexdigest()

        # Rewind the input file and key file
        in_file.seek(0)
        key_file.seek(0)

        # Create the output file path with the checksum in the filename
        output_file = os.path.join(output_dir, f"{os.path.basename(input_file)}.{checksum_hex}.enc")

        with open(output_file, "wb") as out_file:
            # Write the checksum to the beginning of the output file
            out_file.write(hasher.digest())

            bytes_read = 0
            while True:
                chunk = in_file.read(chunk_size)
                if not chunk:
                    break

                key_chunk = key_file.read(key_chunk_size)
                if not key_chunk:
                    key_file.seek(0)
                    key_chunk = key_file.read(key_chunk_size)

                encrypted_chunk = xor_bytes(chunk, key_chunk)
                out_file.write(encrypted_chunk)

                bytes_read += len(chunk)
                progress = bytes_read / file_size * 100
                sys.stdout.write(f"\rProgress: {progress:.2f}%")
                sys.stdout.flush()

        print("\nEncryption completed.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: encrypt.py input_file key_file output_dir")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
