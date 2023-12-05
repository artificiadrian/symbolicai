import os
import logging
import PyPDF2

from tika import unpack

from ...base import Engine


# suppress tika logging
logging.getLogger('tika').setLevel(logging.CRITICAL)


class FileEngine(Engine):
    def __init__(self):
        super().__init__()

    def id(self) -> str:
        return 'files'

    def _read_slice_file(self, file_path: str) -> str:
        # check if file is empty
        if file_path is None or file_path.strip() == '':
            return None

        # verify if file has content
        if not os.path.exists(file_path):
            return None

        # verify if file is empty
        if os.path.getsize(file_path) <= 0:
            return None

        # check if file slice is used
        slices_ = None
        if '[' in file_path and ']' in file_path:
            file_parts = file_path.split('[')
            file_path = file_parts[0]
            # remove string up to '[' and after ']'
            slices_s = file_parts[1].split(']')[0].split(',')
            slices_ = []
            for s in slices_s:
                if s == '':
                    continue
                elif ':' in s:
                    s_split = s.split(':')
                    if len(s_split) == 2:
                        start_slice = int(s_split[0]) if s_split[0] != '' else None
                        end_slice = int(s_split[1]) if s_split[1] != '' else None
                        slices_.append(slice(start_slice, end_slice, None))
                    elif len(s_split) == 3:
                        start_slice = int(s_split[0]) if s_split[0] != '' else None
                        end_slice = int(s_split[1]) if s_split[1] != '' else None
                        step_slice = int(s_split[2]) if s_split[2] != '' else None
                        slices_.append(slice(start_slice, end_slice, step_slice))
                else:
                    slices_.append(int(s))

        file_ = unpack.from_file(str(file_path))
        if 'content' in file_:
            content = file_['content']
        else:
            content = str(file_)

        if content is None:
            return None
        content = content.split('\n')

        if slices_ is not None:
            new_content = []
            for s in slices_:
                new_content.extend(content[s])
            content = new_content
        content = '\n'.join(content)
        return content


    def reset_eof_of_pdf_return_stream(self, pdf_stream_in: list):
        actual_line = len(pdf_stream_in)  # Predefined value in case EOF not found
        # find the line position of the EOF
        for i, x in enumerate(pdf_stream_in[::-1]):
            if b'%%EOF' in x:
                actual_line = len(pdf_stream_in)-i
                print(f'EOF found at line position {-i} = actual {actual_line}, with value {x}')
                break

        # return the list up to that point
        return pdf_stream_in[:actual_line]

    def fix_pdf(self, file_path: str):
        # opens the file for reading
        with open(file_path, 'rb') as p:
            txt = (p.readlines())

        # get the new list terminating correctly
        txtx = self.reset_eof_of_pdf_return_stream(txt)

        # write to new pdf
        new_file_path = f'{file_path}_fixed.pdf'
        with open(new_file_path, 'wb') as f:
            f.writelines(txtx)

        fixed_pdf = PyPDF2.PdfReader(new_file_path)
        return fixed_pdf

    def read_text(self, pdf_reader, range_):
        txt = ''
        n_pages = len(pdf_reader.pages)
        if range_ is None:
            for i in range(n_pages):
                page = pdf_reader.pages[i]
                txt += page.extract_text()
        else:
            for i in range(n_pages)[range_]:
                page = pdf_reader.pages[i]
                txt += page.extract_text()
        return txt

    def forward(self, argument):
        kwargs        = argument.kwargs
        path          = argument.prop.prepared_input

        if '.pdf' in path:
            range_ = None
            if 'slice' in kwargs:
                range_ = kwargs['slice']
                if isinstance(range_, tuple) or isinstance(range_, list):
                    range_ = slice(*range_)

            rsp = ''
            try:
                with open(str(path), 'rb') as f:
                    # creating a pdf reader object
                    pdf_reader = PyPDF2.PdfReader(f)
                    rsp = self.read_text(pdf_reader, range_)
            except Exception as e:
                print(f'Error reading PDF: {e} | {path}')
                if 'fix_pdf' not in kwargs or not kwargs['fix_pdf']:
                    raise e
                fixed_pdf = self.fix_pdf(str(path))
                pdf_reader_fixed = PyPDF2.PdfReader(fixed_pdf)
                rsp = self.read_text(pdf_reader_fixed, range_)
        else:
            try:
                rsp = self._read_slice_file(path)
            except Exception as e:
                print(f'Error reading empty file: {e} | {path}')
                raise e

        if rsp is None:
            raise Exception(f'Error reading file - empty result: {path}')

        # ensure encoding is utf8
        rsp = rsp.encode('utf8', 'ignore').decode('utf8', 'ignore')

        metadata = {}

        return [rsp], metadata

    def prepare(self, argument):
        assert not argument.prop.processed_input, "FileEngine does not support processed_input."
        argument.prop.prepared_input = argument.prop.path