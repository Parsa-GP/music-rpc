# RPC for CMUS

## Introduntion
first, the title explains everything and second,
you spelled intropunction wrong

## Client? what is this, a server?  
We need a server script that communicates with discord rpc
and a script to send info from cmus to the server. because
discord needs the script to run indefinitely but cmus runs
the script everytime it changes the status, so yeah.

### Which is which?
`rpc_server.py` is the server which it's the script that
sets the discord presence to the recieved data from client. \
`cmus-rpc.py` is the client which it sends the info to the
server. you can change this code to for example get from
mpv and sends it to the server.

## Run
> [!IMPORTANT]
> 1. You have to install tmux for it to work
> 2. it _might not_ work in windows/wsl

Execute this command in your cmus:
```
set status_display_program=/PATH/TO/display-hook.sh

```
## Specia Thanks
to TOBEFILLED for the miku art [pixiv](https://www.pixiv.net/en/artworks/126438958) | [gelbooru](https://gelbooru.com/index.php?page=post&s=view&id=11349050) \
to еще рекомендую for the pixelart of the music notes [apppng](https://apppng.vercel.app/posts/music-note-pixel-art/)
