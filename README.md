<h1 align="center">Quartz</h1>

<p align="center"> A tool for turning Spotify songs into iPhone-ready alarms & ringtones. </p>
<p align="center">
  <a href="#usage">Usage</a> •
  <a href="#troubleshooting">Troubleshooting</a>
</p>

<div align="center">
<br />

[![license](https://img.shields.io/github/license/dec0dOS/amazing-github-template.svg?style=flat-square)](LICENSE)

</div>

<div align='center'>
<img src='https://github.com/gracewzhang/Quartz/assets/32557716/392c739d-da65-4865-9c51-0815f38841e9' width='700'/>
</div>

## Usage
1. Clone the repo
2. Store your [Spotify Client ID and Client Secret](https://developer.spotify.com/documentation/web-api/concepts/apps) as environment variables called `QUARTZ_CLIENT_ID` and `QUARTZ_CLIENT_SECRET`, respectively.
3. `cd` into the cloned repo and run `pip install -r requirements.txt`
4. Run Quartz
   1. Converting a song: `python src/main.py song [song Spotify URL]`
   2. Converting a playlist (must be public): `python src/main.py playlist [playlist Spotify URL]`
   3. Configure the output directory of the file by appending `--out-dir [output directory]` to the end of either of the above two commands
6. [Upload the downloaded file(s) to iTunes](https://support.apple.com/guide/itunes/import-items-already-on-your-computer-itns3081/windows#:~:text=In%20the%20iTunes%20app%20on,are%20added%20to%20your%20library.)
7. Connect your iPhone to your PC and [transfer the file(s)](https://support.apple.com/guide/itunes/transfer-files-itns32636/windows)

Note: For the audio file to be a valid ringtone, it must be at most 30 seconds long. This can easily be configured using the built-in file trimmer.

## Troubleshooting
```
Unexpected renderer encountered.
Renderer name: dict_keys(['reelShelfRenderer'])
```
This is a known issue with pytube that is caused by YouTube Shorts. Although the log doesn't impact Quartz's functionality, you can follow [this](https://github.com/pytube/pytube/issues/1270#issuecomment-1436041377) fix to suppress the message.
