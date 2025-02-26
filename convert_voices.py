def analyze_binary_file(file_path):
    with open(file_path, 'rb') as f:
        # Read all bytes
        data = f.read()
        print("File size:", len(data))
        print("\nFirst 50 bytes (hex):")
        print(data[:50].hex())
        print("\nFirst 50 bytes (ascii):")
        print(''.join(chr(b) if 32 <= b <= 126 else '.' for b in data[:50]))
        
        # Try to find any text strings
        possible_strings = []
        current_string = ""
        for byte in data:
            if 32 <= byte <= 126:  # printable ASCII
                current_string += chr(byte)
            elif current_string:
                if len(current_string) > 3:  # only keep strings longer than 3 chars
                    possible_strings.append(current_string)
                current_string = ""
                
        print("\nPossible text strings found:")
        for s in possible_strings:
            print(s)

print("Analyzing voices-v1.0.bin...")
analyze_binary_file('voices-v1.0.bin')