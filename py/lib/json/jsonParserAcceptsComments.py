#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

description = '''
    Pársuje json včetně komentářů.
    (podle http://www.lifl.fr/~riquetd/parse-a-json-file-with-comments.html)
'''

import json
import re

class JsonParserAcceptsComments:

    # Regular expression for comments
    comment_re = re.compile(
        '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
    )

    def parse(self, filename):
        """ Parse a JSON file
            First remove comments and then use the json module package
            Comments look like :
                // ...
            or
                /*
                ...
                */
        """
        with open(filename) as f:
            content = ''.join(f.readlines())

            ## Looking for comments
            match = self.comment_re.search(content)
            while match:
                # single line comment
                content = content[:match.start()] + content[match.end():]
                match = self.comment_re.search(content)

            # Return json file
            return json.loads(content)
