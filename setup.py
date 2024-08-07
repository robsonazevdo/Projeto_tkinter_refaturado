from cx_Freeze import setup, Executable
import os

base = None
if os.name == 'nt':
    base = 'Win32GUI'

executables = [
    Executable('app.py', base=base, icon='assets/Iconsmind-Outline-Cash-register-2.ico')
]

include_files = [
    ('assets/', 'assets'),
    ('agendamento/', 'agendamento'),
    ('atendimento/', 'atendimento'),
    ('cliente/', 'cliente'),
    ('fluxo_caixa/', 'fluxo_caixa'),
    ('backup/', 'backup'),
    ('servico/', 'servico'),
    ('funcionario/', 'funcionario'),
    'Banco.py',
    'calendario.py',
    'agenda.db'  # Certifique-se de incluir o banco de dados, se necessário
]

options = {
    'build_exe': {
        'packages': ['sqlite3'],  # Inclua sqlite3 explicitamente
        'include_files': include_files,
    },
}

setup(
    name='MinhaAplicacao',
    version='0.1',
    description='Minha Aplicação',
    options=options,
    executables=executables
)
