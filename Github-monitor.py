# coding=utf-8
# author:Life Bitterness

import datetime
import requests
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler


class GithubMon:
    def __init__(self, server, proxies):
        self.server = server
        self.proxies = None
        if proxies:
            self.proxies = {
                "http": proxies,
                "https": proxies
            }

# 获取软件主页信息
    def get_update(self, search_content):
        try:
            res = requests.get(self.server + f"/search/repositories?q=is:not-curated%20{search_content}", proxies=self.proxies, verify=False).json()
            full_name = res["items"][0]["full_name"]  # github用户和仓库名
            html_url = res["items"][0]["html_url"]  # 仓库主页
            stargazers_count = res["items"][0]["stargazers_count"]  # star数量
            releases_url = res["items"][0]["releases_url"][:-5] + "?id=" + str(res["items"][0]["id"])  # 发布历史
            pushed_at = res["items"][0]["pushed_at"]  # push时间
            return {"status": "0", "results": {"用户和仓库名": full_name, "仓库主页": html_url, "star数量": stargazers_count, "发布历史_url": releases_url, "push时间": pushed_at}}
        except Exception as f:
            return {"status": "1", "results": f}

# 获取发布版本信息
    def get_releases_update(self, res_url, day_number=1):
        try:
            res = requests.get(res_url, proxies=self.proxies, verify=False).json()

            html_url = res[0]["html_url"]  # 软件下载页面
            name = res[0]["name"]  # 发布的软件名称
            published_at = res[0]["published_at"]  # 软件版本发布时间

            today_time = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=day_number)  # 默认为当前时间减1天
            # logger.info(today_time)
            published_at_datetime = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(minutes=480)  # 软件版本的创建时间
            # logger.info(published_at_datetime)
            if today_time < published_at_datetime:
                return {"status": "0", "results": {"发布的软件名称": name, "软件下载页面": html_url, "软件版本发布时间": published_at}}

        except Exception as f:
            return {"status": "1", "results": f}


def main():
    version_res = github.get_releases_update(r["results"]["发布历史_url"], timing_time)
    if version_res:
        logger.info(version_res)


if __name__ == "__main__":
    search_theme = input("请输入定时监控的存储库名称：")
    timing_time = int(input("请输入循环监控的天数(数字)："))
    github = GithubMon("https://api.github.com", "")
    r = github.get_update(search_theme)
    logger.info(r)

    time_scheduling = BlockingScheduler()
    time_scheduling.add_job(main, trigger="interval", days=timing_time)
    time_scheduling.start()
