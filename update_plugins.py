try:
    import concurrent.futures as futures
except ImportError:
    try:
        import futures
    except ImportError:
        futures = None

import re
import zipfile
import shutil
import tempfile
import requests

from os import path

# --- Globals ----------------------------------------------
PLUGINS = """
ale https://github.com/dense-analysis/ale
vim-yankstack https://github.com/maxbrunsfeld/vim-yankstack
ctrlp.vim https://github.com/ctrlpvim/ctrlp.vim
nerdtree https://github.com/preservim/nerdtree
nginx.vim https://github.com/chr4/nginx.vim
tlib https://github.com/tomtom/tlib_vim
vim-addon-mw-utils https://github.com/MarcWeber/vim-addon-mw-utils
vim-coffee-script https://github.com/kchmck/vim-coffee-script
vim-pyte https://github.com/therubymug/vim-pyte
vim-snipmate https://github.com/garbas/vim-snipmate
vim-snippets https://github.com/honza/vim-snippets
vim-surround https://github.com/tpope/vim-surround
vim-fugitive https://github.com/tpope/vim-fugitive
vim-zenroom2 https://github.com/amix/vim-zenroom2
vim-commentary https://github.com/tpope/vim-commentary
vim-gitgutter https://github.com/airblade/vim-gitgutter
lightline.vim https://github.com/itchyny/lightline.vim
lightline-ale https://github.com/maximbaz/lightline-ale
rust.vim https://github.com/rust-lang/rust.vim
vim-markdown https://github.com/plasticboy/vim-markdown
vim-javascript https://github.com/pangloss/vim-javascript
vim-python-pep8-indent https://github.com/Vimjas/vim-python-pep8-indent
vim-indent-guides https://github.com/nathanaelkane/vim-indent-guides
elm-vim https://github.com/ElmCast/elm-vim
vim-nix https://github.com/LnL7/vim-nix
vim-pandoc https://github.com/vim-pandoc/vim-pandoc
vim-pandoc-syntax https://github.com/vim-pandoc/vim-pandoc-syntax
vim-stylish-haskell https://github.com/haskell/stylish-haskell
vimtex https://github.com/lervag/vimtex
dracula https://github.com/dracula/vim
mayansmoke https://github.com/vim-scripts/mayansmoke
gruvbox https://github.com/morhetz/gruvbox
peaksea https://github.com/calincru/peaksea.vim
vim-colors-solarized https://github.com/altercation/vim-colors-solarized
true-zen https://github.com/Pocco81/true-zen.nvim
sonokai https://github.com/sainnhe/sonokai
edge https://github.com/sainnhe/edge
onedark https://github.com/joshdick/onedark.vim
verilog_systemverilog https://github.com/vhda/verilog_systemverilog.vim
fzf.vim https://github.com/junegunn/fzf.vim
""".strip()

GITHUB_ZIP = "%s/archive/master.zip"

SOURCE_DIR = path.join(path.dirname(__file__), "sources_non_forked")


def download_extract_replace(plugin_name, zip_path, temp_dir, source_dir):
    temp_zip_path = path.join(temp_dir, plugin_name)

    # Download and extract file in temp dir
    req = requests.get(zip_path)
    open(temp_zip_path, "wb").write(req.content)

    zip_f = zipfile.ZipFile(temp_zip_path)
    zip_f.extractall(temp_dir)

    content_disp = req.headers.get("Content-Disposition")
    filename = re.findall("filename=(.+).zip", content_disp)[0]
    plugin_temp_path = path.join(temp_dir, path.join(temp_dir, filename))

    # Remove the current plugin and replace it with the extracted
    plugin_dest_path = path.join(source_dir, plugin_name)

    try:
        shutil.rmtree(plugin_dest_path)
    except OSError:
        pass

    shutil.move(plugin_temp_path, plugin_dest_path)
    print("Updated {0}".format(plugin_name))


def update(plugin):
    name, github_url = plugin.split(" ")
    zip_path = GITHUB_ZIP % github_url
    try:
        download_extract_replace(name, zip_path, temp_directory, SOURCE_DIR)
    except Exception as exp:
        print("Could not update {}. Error was: {}".format(name, str(exp)))


if __name__ == "__main__":
    temp_directory = tempfile.mkdtemp()

    try:
        if futures:
            with futures.ThreadPoolExecutor(16) as executor:
                executor.map(update, PLUGINS.splitlines())
        else:
            [update(x) for x in PLUGINS.splitlines()]
    finally:
        shutil.rmtree(temp_directory)
