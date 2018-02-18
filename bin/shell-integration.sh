# sodalite shell integration

# source that behaves like in bash
function _source {
    alias shopt=':'
    alias _expand=_bash_expand
    alias _complete=_bash_comp
    emulate -L sh
    setopt kshglob noshglob braceexpand
    builtin source "$@"
}


function sodalite-emacs-widget {
    cd $(sodalite)
    zle reset-prompt
}

function sodalite-vim-widget {
    sodalite-emacs-widget
    zle -K viins
}

shell=$(ps -p $$ | tail -n1 | rev | cut -d" " -f1 | rev)
if [ $shell = 'zsh' ]; then
    zle     -N      sodalite-vim-widget
    zle     -N      sodalite-emacs-widget
    bindkey -M vicmd 'f'  sodalite-vim-widget
    bindkey -M emacs '^f' sodalite-emacs-widget
elif [ $shell = 'bash' ]; then
    bind -m vi-command '"f":"ddicd $(sodalite); tput cuu1; tput ed\n"'
    bind -m emacs '"\C-f":"\C-k\C-ucd $(sodalite); tput cuu1; tput ed\n"'
fi