;; What follows is a "manifest" equivalent to the command line you gave.
;; You can store it in a file that you may then pass to any 'guix' command
;; that accepts a '--manifest' (or '-m') option.

(specifications->manifest
  (list "zstd:lib" "zlib" "gcc-toolchain"
        "libglvnd" "glib" ; general dev libs
        "uv"                              ; python dev tools
        "make"                            ; general dev tools
        "texlive-scheme-basic"            ; base latex
        "texlive-luatex"                  ; luatex 
        "texlive-lualibs"                 ; utility libraries like lfs
        "texlive-latexmk"                 ; build system for examples
        "texlive-fontspec"
        "texlive-babel-ukrainian"
        "texlive-xkeyval"
        "texlive-setspace"
        "texlive-float"
        "texlive-alegreya"                ; font for reports
        "texlive-listings"
        "texlive-xcolor"
        "ncurses"                         ; tput
        "fontconfig"
        "font-0xproto"))
