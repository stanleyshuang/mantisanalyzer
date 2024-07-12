# -*- coding: utf-8 -*-
#
# Auther:   Stanley Huang
# Project:  vulnrep 2.0
# Date:     2023-02-13
#
import re
from . import permanent_obj


class vglobalconfig(permanent_obj):
    """{
        "last_analyst_index": 0,
        "analyst_list": ["KevinLiao@qnap.com", "MyronSu@qnap.com"],
    }"""

    def __init__(
        self, data, downloads, filename="global_config.json", service="common"
    ):
        super(vglobalconfig, self).__init__(data, downloads, filename, service)
        whole = self.load("global")
        if whole == None:
            whole = {
                "last_analyst_index": 0,
                "analyst_list": ["KevinLiao@qnap.com", "MyronSu@qnap.com"],
                "latest_qsaid_idx": "QSA-24-01",
            }
            self.update("global", whole)

    def select_analyst(self, model, email=None):
        whole = self.json_obj
        analyst_list = whole["analyst_list"]
        ### init whole['analyst_job_count']
        if "analyst_job_count" not in whole:
            whole["analyst_job_count"] = {}
        ### pick the one who's counts are smallest
        candidate = None
        min_count = 1000000.0
        if email:
            idx = self.find_index(email)
            if idx:
                if idx % 2 == 0:
                    candidate = "KevinLiao@qnap.com"
                else:
                    candidate = "MyronSu@qnap.com"
                min_count = whole["analyst_job_count"][candidate]
                print(
                    "分析師： "
                    + candidate
                    + "，已處理"
                    + str(min_count)
                    + "件工作。專責負責研究員 ("
                    + email
                    + ") 的弱點報告"
                )
        if candidate is None:
            if model in [
                "qts",
                "quts hero",
                "qutscloud",
                "qpkg",
                "qne",
                "qvp",
                "qvr",
                "qes",
                "main",
            ]:
                for analyst in analyst_list:
                    # init whole['analyst_job_count'][analyst]
                    if analyst not in whole["analyst_job_count"]:
                        whole["analyst_job_count"][analyst] = 0.0
                    # compare with min_count
                    if whole["analyst_job_count"][analyst] < min_count:
                        candidate = analyst
                        min_count = whole["analyst_job_count"][analyst]
                self.flush("global")
                print(
                    "分析師： " + candidate + "，已處理" + str(min_count) + "件工作。"
                )
            else:
                candidate = "KevinLiao@qnap.com"
                print("分析師： " + candidate + "，model: " + model + "。")

        return candidate

    def assign_analyst(self, assignee, weight=1.0):
        whole = self.json_obj
        analyst_list = whole["analyst_list"]
        ### init whole['analyst_job_count']
        if "analyst_job_count" not in whole:
            whole["analyst_job_count"] = {}
        ### init whole['analyst_job_count'][analyst]
        if assignee not in whole["analyst_job_count"]:
            whole["analyst_job_count"][assignee] = 0.0
        # job counts increased
        whole["analyst_job_count"][assignee] += weight
        self.flush("global")

    def find_index(self, email):
        self.researcher_email = [
            "h4lo2w1nn3r@gmail.com",  # k
            "sa@proczero.com",  # m
            "pwn2own@trendmicro.com",
            "alan.li.tw@gmail.com",  # m
            "jwdong2000@qq.com",  # k
            "fahimhusain.raydurg@gmail.com",
            "huasheng_mangguo@163.com",  # k
            "w181496@gmail.com",  # m
            "chinanuke@nuke666.cn",  # k
            "a2209799148@gmail.com",
            "agarwajrojk1234@gmail.com",  # k
            "tyaookk@gmail.com",
            "sachinkalkumbe28@gmail.com",
            "dabdurakhmanova@ptsecurity.com",
            "foysal1197@gmail.com",
            "bugfinder0@outlook.com",  # m
            "yc_m1qlin@139.com",
            "domen.puncerkugler@nccgroup.com",
            "13175460559@139.com",
            "chumen77sec@gmail.com",  # m
            "vyasp979@gmail.com",
            "fazalurrahman2005@gmail.com",
            "erikdejong@gmail.com",
            "zhaorunzi0@gmail.com",
            "shaikh.shahnawaz003@gmail.com",
            "thomas.fady@gmail.com",
            "ratneshmishra239@gmail.com",
            "shripadraccha5512v1@gmail.com",
            "muhammadtanvirahmed82@gmail.com",
            "thomas@bugscale.ch",
            "patrick.schramboeck@gmail.com",
            "theanupamsingh01@gmail.com",
            "amit@sternumiot.com",
            "edwardso@outlook.com",
            "rajyaguruvirang@gmail.com",
            "y.abe0808@gmail.com",
            "deepakdas288@gmail.com",
            "krishnajaiswal.2208@gmail.com",
            "qnap@noci.work",
            "simon.slater65@gmail.com",
            "christoph@kretz.link",
            "pwning.me@gmail.com",
            "ibrahimayadhi6@gmail.com",
            "joehuang@qnap.com",
            "dcs_security@protonmail.com",
            "fredoun@gmail.com",
            "noamr@ssd-disclosure.com",
            "ibnqamar10@gmail.com",
            "bugbountyhunter37@gmail.com",
            "yassfree@outlook.com",
            "tinutomy003@protonmail.com",
            "meljith6355484@gmail.com",
            "engineer.aayush1234@gmail.com",
            "suziyanakulsum26@gmail.com",
            "salvo.b18@live.it",
            "nikunj.chandak123@gmail.com",
            "azdrodowski@uniqal.pl",
            "attacker200301@gmail.com",
            "nakshraja2015@gmail.com",
            "mohdhaji24@gmail.com",
            "johnproto69@gmail.com",
            "amitpathak.ap786@gmail.com",
            "osama.eldosoky@proton.me",
            "anees.ethical@gmail.com",
            "tanunt1122@gmail.com",
            "shubhamsohi3@gmail.com",
            "ravindradagale2@gmail.com",
            "khadijamemon057@gmail.com",
            "nobodynobody@tutanota.com",
            "cynthia_wyre@rapid7.com",
            "scream.khaled2010@gmail.com",
            "lambardarrofficial@gmail.com",
            "cybarriersolutions509@gmail.com",
            "1160307775a@gmail.com",
            "wl03452329@gmail.com",
            "nemar.nil.0@gmail.com",
            "huangstan1215@gmail.com",  # k
            "hussain@utusec.com",
            "xuanninhho1412@gmail.com",
            'bd.abdullah.net@gmail.com',
        ]
        if email in self.researcher_email:
            return self.researcher_email.index(email)
        else:
            return None
