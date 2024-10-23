cd "$(dirname "$0")"

OS=$(uname)

run_on_linux() {
    gnome-terminal -- bash -c "./sh/api.sh; exec bash"
    gnome-terminal -- bash -c "./sh/auto_fetch.sh; exec bash"
    gnome-terminal -- bash -c "./sh/discord_chat_bot.sh; exec bash"
}

run_on_macos_terminal() {
    current_dir=$(pwd)
    osascript -e "tell application \"Terminal\" to do script \"cd '$current_dir' && sh ./sh/api.sh\""
    osascript -e "tell application \"Terminal\" to do script \"cd '$current_dir' && sh ./sh/auto_fetch.sh\""
    osascript -e "tell application \"Terminal\" to do script \"cd '$current_dir' && sh ./sh/discord_chat_bot.sh\""
}

echo "$(pwd)"

if [ "$OS" == "Linux" ]; then
    run_on_linux
elif [ "$OS" == "Darwin" ]; then
    run_on_macos_terminal
else
    echo "OS not supported."
    exit 1
fi