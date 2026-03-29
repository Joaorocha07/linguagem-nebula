from pathlib import Path
import importlib.util

BASE_DIR = Path(__file__).resolve().parent     
ROOT_DIR = BASE_DIR.parent         
TESTS_DIR = ROOT_DIR / "examples" / "tests"

ROOT_EXAMPLE = ROOT_DIR / "examples" 
NEBULA_PATH = BASE_DIR / "nebula.py"

spec = importlib.util.spec_from_file_location("nebula", NEBULA_PATH)
nebula = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nebula)

print("\n" + "=" * 70)
print("TESTE 1: PRECEDÊNCIA")
print("=" * 70)
nebula.executar_arquivo(str(TESTS_DIR / "teste_precedencia.neb"))

print("\n" + "=" * 70)
print("TESTE 2: CONDICIONAL")
print("=" * 70)
nebula.executar_arquivo(str(TESTS_DIR / "teste_condicional.neb"))

print("\n" + "=" * 70)
print("TESTE 3: ERROS RECUPERÁVEIS")
print("=" * 70)
nebula.executar_arquivo(str(TESTS_DIR / "teste_erros_recuperaveis.neb"))

print("\n" + "=" * 70)
print("TESTE 4: INVÁLIDO")
print("=" * 70)
nebula.executar_arquivo(str(TESTS_DIR / "teste_invalido.neb"))

print("\n" + "=" * 70)
print("TESTE 5: PROGRAMA EXEMPLO")
print("=" * 70)
nebula.executar_arquivo(str(ROOT_EXAMPLE / "programa_exemplo.neb"))
