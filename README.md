## 介绍
此脚本用于监控关注的**github存储库**，只监控存在`Releases`版本更新的软件，如果不存在`Releases`不会被检测到。

## 依赖包
> pip install apscheduler
> 
> pip install requests
> 
> pip install datetime
> 
> pip install loguru

## 使用
使用python3运行Github-monitor.py
> python3 Github-monitor.py

输入要监控的存储库名称与周期性检测时间

## 接入其他平台
将脚本的输出函数删除，将return结果对接到微信机器人或其他平台机器人输出。具体修改内容请自行上网搜索。
