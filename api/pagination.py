import json


class PhraseTmsPagination:
    def __init__(self, api_client):
        self._api_client = api_client

    def _get_content_on_single_page(self, url, page):
        content_on_single_page = self._api_client.get_request(
            url=url,
            params={"pageNumber": str(page)}
        )
        return {
            "totalPages": content_on_single_page["totalPages"],
            "content": content_on_single_page["content"]
        }

    def _get_content_on_all_pages(self, url, total_pages):
        all_jobs_on_all_pages = []
        page = 0
        while page < total_pages:
            content_per_page = self._get_content_on_single_page(url, page)[
                "content"]
            all_jobs_on_all_pages.extend(content_per_page)
            page += 1
        return all_jobs_on_all_pages

    def get_all_content_on_all_pages(self, url):
        content = self._get_content_on_single_page(url, 0)
        if content["totalPages"] > 1:
            return self._get_content_on_all_pages(url, content["totalPages"])
        else:
            return content["content"]

    def save_paginated_content_into_file(self, url, file):
        content = self._get_content_on_single_page(url, 0)
        with open(file, "w") as o:
            if content["totalPages"] > 1:
                for page in range(content["totalPages"]):
                    content_per_page = self._get_content_on_single_page(url, page)[
                        "content"]
                    for i in content_per_page:
                        o.write(json.dumps(i))
                        o.write("\n")
            else:
                for i in content["content"]:
                    o.write(json.dumps(i))
                    o.write("\n")


class PaginationViaHeaders:
    def __init__(self, api_client, page_count_header, starting_page=1, page_limit=100, limit_name="per_page",
                 headers_json=False, content_field=None):
        self._api_client = api_client
        self._page_count_header = page_count_header
        self._page_limit = page_limit
        self._limit_name = limit_name
        self._starting_page = starting_page
        self._headers_json = headers_json
        self._content_field = content_field

    def _get_content_on_single_page(self, url, params):
        content_on_single_page = self._api_client.get_request(
            url=url,
            params={**params, f"{self._limit_name}": self._page_limit},
            return_json=False
        )
        response_headers = json.loads(
            content_on_single_page.headers[self._page_count_header]) if self._headers_json else content_on_single_page.headers
        total_pages = response_headers["total_count"] / response_headers[
            "current_per_page"] if self._headers_json else int(response_headers[self._page_count_header])
        return {
            "total_pages": total_pages,
            "content": content_on_single_page.json()[self._content_field] if self._content_field else content_on_single_page.json()
        }

    def _get_content_on_all_pages(self, url, params, total_pages):
        all_content_on_all_pages = []
        page = self._starting_page

        while page <= total_pages:
            content_per_page = self._get_content_on_single_page(url, params)["content"]
            all_content_on_all_pages.extend(content_per_page)
            page += 1
        return all_content_on_all_pages

    def get_all_content_on_all_pages(self, url, params={}):
        params = {**params, "page": self._starting_page}
        first_page = self._get_content_on_single_page(url, params)
        if first_page["total_pages"] > 1:
            return self._get_content_on_all_pages(url, params, first_page["total_pages"])
        else:
            return first_page["content"]
