;; What follows is a "manifest" equivalent to the command line you gave.
;; You can store it in a file that you may then pass to any 'guix' command
;; that accepts a '--manifest' (or '-m') option.

(specifications->manifest
  (list "zstd:lib" "zlib" "gcc-toolchain" ; general dev libs
        "uv"                              ; python dev tools
        "make"                            ; general dev tools
        "texlive-scheme-basic"            ; base latex
        "texlive-luatex"                  ; luatex 
        "texlive-lualibs"                 ; utility libraries like lfs
        "texlive-latexmk"                 ; build system for examples
        "texlive-alegreya"))              ; font for docs
