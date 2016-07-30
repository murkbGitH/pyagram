import os
import os.path
import pyparsing as pp
import hashlib
import json
import pprint

class Diagram(object):
    def __init__(self, in_file, out_path, image_type, process_line_by_line, fontname = None):
        self.in_file = in_file
        self.out_path = out_path
        self.image_type = image_type
        self.process_line_by_line = process_line_by_line
        self.fontname = fontname

    def lexical_analysis(self, src):
        raise NotImplementedError('lexical_analysis method must be overridden and implemented by a descendant class.') 

    def syntactic_analysis(self, src):
        raise NotImplementedError('lexical_analysis method must be overridden and implemented by a descendant class.') 

    def generate_dot(self, ast):
        raise NotImplementedError('lexical_analysis method must be overridden and implemented by a descendant class.') 

    def generate_image(self, dot):
        dot_file = hashlib.md5(bytes(json.dumps(dot), 'utf-8')).hexdigest()
        out_file = os.path.basename(self.in_file.replace('.txt', '.' + self.image_type))
        f_out = open(dot_file, 'w', encoding='utf-8')
        f_out.write(dot)
        f_out.flush()
        f_out.close()

        command = 'dot -T' + self.image_type + ' -o ' + self.out_path + '/' + out_file + ' ' + dot_file
        os.system(command)
        os.remove(dot_file)

    def compile(self):
        pprint.pprint(self.in_file)
        f_in = open(self.in_file, 'r', encoding = 'utf-8')
        if self.process_line_by_line:
            parsed_lines = []
            for line in f_in.readlines():
                replaced_line = str(line.replace('\n',''))
                if len(replaced_line) != 0:
                    parsed_line = lexical_analysis(replaced_line)
                    parsed_lines.append(parsed_line)
        else:
            lines = f_in.readlines()
            parsed_lines = lexical_analysis(lines)
        ast = syntactic_analysis(parsed_lines)
        dot = generate_dot(ast)
        generate_image(dot)
