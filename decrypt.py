import os
import sys
import hashlib

def xor_bytes(data, key):
    return bytes(a ^ b for a, b in zip(data, (key * (len(data) // len(key) + 1))[:len(data)]))

def main(input_file, key_file, output_dir):
    print("Decrypting file " + input_file)

    chunk_size = 10 * 1024 * 1024
    key_chunk_size = 10 * 1024 * 1024

    hasher = hashlib.sha256()

    # Get the checksum from the input file name
    input_file_basename = os.path.basename(input_file)
    checksum_hex = input_file_basename.split(".")[-2]

    with open(input_file, "rb") as in_file, open(key_file, "rb") as key_file:
        # Get the size of the input file
        file_size = os.path.getsize(input_file)

        # Minus the checksum size
        file_size -= hasher.digest_size

        # Read the checksum from the beginning of the input file
        expected_hash = in_file.read(hasher.digest_size)

        # Create the output file path without the checksum in the filename
        # remove .<checksum>.enc
        input_file_basename = input_file_basename[:-len(checksum_hex) - 5]
        output_file = os.path.join(output_dir, input_file_basename)

        with open(output_file, "wb") as out_file:
            bytes_read = 0
            while True:
                chunk = in_file.read(chunk_size)
                if not chunk:
                    break

                key_chunk = key_file.read(key_chunk_size)
                if not key_chunk:
                    key_file.seek(0)
                    key_chunk = key_file.read(key_chunk_size)

                decrypted_chunk = xor_bytes(chunk, key_chunk)
                out_file.write(decrypted_chunk)

                bytes_read += len(chunk)
                progress = bytes_read / file_size * 100
                sys.stdout.write(f"\rProgress: {progress:.2f}%")
                sys.stdout.flush()

        with open(output_file, "rb") as out_file:
            # Compute the checksum over the decrypted file
            out_file.seek(0)
            while True:
                chunk = out_file.read(chunk_size)
                if not chunk:
                    break

                hasher.update(chunk)

            computed_hash = hasher.digest()

            if computed_hash != expected_hash:
                print("\nError: Checksums do not match. The file may be corrupted.")
                sys.exit(1)

        print ("\nDecryption completed.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: decrypt.py input_file key_file output_dir")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
