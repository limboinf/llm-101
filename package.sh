#!/bin/bash
# 项目初始化或者每次拉取新代码时进行更新操作

cd $(dirname $0)

APP_HOME=$(pwd)
ENV_PATH=$APP_HOME/venv

if [ ! -d "$LOG_PATH" ]; then
    mkdir "$LOG_PATH"
fi

if [ ! -d "$ENV_PATH" ]; then
  echo "创建python虚拟环境 ..."
  python3 -m venv $ENV_PATH
fi

# 安装依赖
echo "pip安装 ..."
$ENV_PATH/bin/pip --default-timeout=1000 --retries=5 install --trusted-host=pypi.douban.com.cn -r $APP_HOME/requirements.txt

export PYTHONPATH="${PYTHONPATH}:$APP_HOME"

echo $PYTHONPATH

echo "------------ LLM-101 Init OK ------------"
