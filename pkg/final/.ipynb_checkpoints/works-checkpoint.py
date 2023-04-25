"""works.py commit"""
import time
import base64
import requests
import matplotlib.pyplot as plt
from IPython.display import HTML
from IPython.core.pylabtools import print_figure


class Works:
    """Works commit"""

    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
        self.data = self.req.json()

    def __str__(self):
        return "str"

    def __repr__(self):
        _authors = [au["author"]["display_name"] for au in self.data["authorships"]]
        if len(_authors) == 0:
            authors = "none"
        elif len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and" + _authors[-1]

        title = self.data["title"]

        volume = self.data["biblio"]["volume"]

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [
                self.data["biblio"].get("first_page", "") or "",
                self.data["biblio"].get("last_page", "") or "",
            ]
        )
        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]

        oa_id = self.data["id"]
        s_sum = f'{authors}, {title}, {volume}{issue}{pages}, ({year}), \
            {self.data["doi"]}. cited by: {citedby}. {oa_id}'
        return s_sum

    def _repr_markdown_(self):
        _authors = [
            f'[{au["author"]["display_name"]}]({au["author"]["id"]})'
            for au in self.data["authorships"]
        ]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and " + _authors[-1]

        title = self.data["title"]

        journal = f"[{self.data['host_venue']['display_name']}]({self.data['host_venue']['id']})"

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [
                self.data["biblio"].get("first_page", "") or "",
                self.data["biblio"].get("last_page", "") or "",
            ]
        )

        # Citation counts by year
        years = [e["year"] for e in self.data["counts_by_year"]]
        counts = [e["cited_by_count"] for e in self.data["counts_by_year"]]

        fig, at_x = plt.subplots()
        at_x.bar(years, counts)
        at_x.set_xlabel("year")
        at_x.set_ylabel("citation count")
        data = print_figure(fig, "png")  # save figure in string
        plt.close(fig)

        b64 = base64.b64encode(data).decode("utf8")
        citefig = f"![img](data:image/png;base64,{b64})"

        s_sum = f'{authors}, *{title}*, **{journal}**, \
            {self.data["biblio"]["volume"]}{issue}{pages}, ({self.data["publication_year"]}),\
            {self.data["doi"]}. cited by: {self.data["cited_by_count"]}. \
            [Open Alex]({self.data["id"]})'

        s_sum += "<br>" + citefig
        return s_sum

    @property
    def ris(self):
        """ris commit"""
        fields = []
        if self.data["type"] == "journal-article":
            fields += ["TY  - JOUR"]
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data["authorships"]:
            fields += [f'AU  - {author["author"]["display_name"]}']

        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']

        if self.data["biblio"]["issue"]:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']

        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ["ER  -"]

        ris = "\n".join(fields)
        ris64 = base64.b64encode(ris.encode("utf-8")).decode("utf8")
        uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64,\
            {ris64}" download="ris">Download RIS</a>'

        return HTML(uri)

    def related_works(self):
        """related_works commit"""
        rworks = []
        for rw_url in self.data["related_works"]:
            r_w = Works(rw_url)
            rworks += [r_w]
            time.sleep(0.101)
        return rworks

    def bibtex(self):
        """bibtex commit"""
        fields = []
        if self.data["type"] == "journal-article":
            fields += [
                f'@Article{{{self.data["authorships"][0]["author"]["display_name"]}\
                    {self.data["publication_year"]}'
            ]
        else:
            raise Exception("Unsupported type {self.data['type']}")
        for author in self.data["authorships"]:
            fields += [f'author = {{{author["author"]["display_name"]}}}']
        fields += [f'year = {{{self.data["publication_year"]}}}']
        fields += [f'title = {{{self.data["title"]}}}']
        fields += [f'journal = {{{self.data["host_venue"]["display_name"]}}}']
        fields += [f'volume = {{{self.data["biblio"]["volume"]}}}']
        if self.data["biblio"]["issue"]:
            fields += [f'number = {{{self.data["biblio"]["issue"]}}}']
        fields += [
            f'pages = {{{self.data["biblio"]["first_page"]}-{self.data["biblio"]["last_page"]}}}'
        ]
        fields += [f'doi = {{{self.data["doi"]}}}']
        fields += ["}"]
        bibtex = ",\n".join(fields)
        print(bibtex)

    def references(self):
        """references commit"""
        re_works = []
        for re_w_url in self.data["referenced_works"]:
            re_w = Works(re_w_url)
            re_works += [re_w]
            time.sleep(0.101)
        return re_works

    def citing_works(self):
        """citing_works commit"""
        cited_works = requests.get(self.data["cited_by_api_url"]).json()
        cites_works = []
        for result in cited_works["results"]:
            url = result["id"]
            works = Works(url)
            cites_works += [works]
            time.sleep(0.101)
        return cites_works
