# change to utf8(BOM) CRLF
function convert_text_windows_style {
    
    nkf --overwrite --oc=UTF-8-BOM -Lw $1
}

# load .env file
function load_env {

    eval "$(cat $1 | sed 's/# .*$//' | xargs -I {} echo export {};)"
}
