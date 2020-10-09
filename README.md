# Github Trends to Telegram channel

![](https://github.com/alex-bormotov/github-telegram/workflows/Github-CICD/badge.svg)   [![Codacy Badge](https://app.codacy.com/project/badge/Grade/c1c1c58f3a1e488091aac12ae1d7127e)](https://www.codacy.com/manual/alex-bormotov/github-telegram?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alex-bormotov/github-telegram&amp;utm_campaign=Badge_Grade)

## Install (Ubuntu + Docker)

```bash
git clone https://github.com/alex-bormotov/github-telegram
```

```bash
cd github-telegram
```

```bash
cp config/config.json.sample config/config.json
```

> Edit config/config.json

```bash
sudo chmod +x docker_ubuntu_install.sh && sudo ./docker_ubuntu_install.sh
```

```bash
sudo docker run -d --rm --mount src=`pwd`/config,target=/github-telegram/config,type=bind skilfulll1/github-telegram:latest
```
