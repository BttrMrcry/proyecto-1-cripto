import lorem

def generate_lorem_file(file_size):
    with open('lorem.txt', 'w') as f:
        while f.tell() < file_size:
            f.write(lorem.get_sentence() + '\n')
    print(f'File generated successfully with size {file_size} bytes.')

generate_lorem_file(1024 * 100 )
