from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective
from sphinx.locale import _

class SQLQueryDirective(SphinxDirective):
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        'host': str,
        'port': str,
        'user': str,
        'password': str,
        # Добавьте здесь другие необходимые параметры подключения
    }

    def run(self):
        code = '\n'.join(self.content)
        sql_code_block = nodes.literal_block(code, code)
        sql_code_block['language'] = 'sql'
        sql_code_block['classes'] = ['sql-query']

        execute_button = nodes.raw(
            '',
            '<button class="sql-execution-button">Execute</button>',
            format='html'
        )

        result_div = nodes.container('', classes=['sql-result'])

        return [sql_code_block, execute_button, result_div]

    def encode_param(self, name, value):
        return f'{name}={value}'

    def get_connection_params(self):
        params = {}

        for key, value in self.options.items():
            params[key] = value

        return '&'.join(self.encode_param(key, value) for key, value in params.items())

def process_sql_queries(app, doctree, fromdocname):
    for node in doctree.traverse(SQLQueryDirective):
        code_block = node.children[0].deepcopy()
        execute_button = node.children[1].deepcopy()
        result_div = node.children[2].deepcopy()

        connection_params = node.get_connection_params()
        execute_button.attributes['data-connection'] = connection_params

        container = nodes.container()
        container += code_block
        container += execute_button
        container += result_div

        node.replace_self(container)

def setup(app):
    app.add_directive('sqlquery', SQLQueryDirective)
    app.connect('doctree-resolved', process_sql_queries)
    app.add_js_file('sql_execution.js')
    app.add_css_file('custom.css')

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
