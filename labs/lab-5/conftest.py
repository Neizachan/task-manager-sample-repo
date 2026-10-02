import importlib.util, pathlib, sys, types
# expose labs/lab-5/pages/login_page.py as module `labs_lab5_pages` (folder name has a hyphen)
spec = importlib.util.spec_from_file_location("labs_lab5_pages", pathlib.Path(__file__).parent / "pages" / "login_page.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); sys.modules["labs_lab5_pages"] = mod
