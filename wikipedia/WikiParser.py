# -*- coding: utf-8 -*-
import re
from datetime import datetime, date


class WikiParser:
    def __init__(self, page):
        self.page = page
        self.text = page.text

    @staticmethod
    def remove_double_whitespaces(text: str) -> str:
        while "  " in text:
            text = text.replace("  ", " ")
        return text.strip()

    @staticmethod
    def remove_non_numbers(text: str) -> str:
        return re.sub("[^0-9 ]", "", text).strip()

    @staticmethod
    def remove_html_tags(text: str) -> str:
        return re.sub(r"<.*?>(.*)</.*?>", "", text).strip()

    @staticmethod
    def remove_parenthesis(text: str) -> str:
        return re.sub(r"[\(\)]", "", text).strip()

    @staticmethod
    def remove_parenthesis_content(text: str) -> str:
        return re.sub(r"\((.*)\)", "", text).strip()

    @staticmethod
    def remove_brackets(text: str) -> str:
        return re.sub(r"[\{\}]", "", text).strip()

    @staticmethod
    def remove_brackets_content(text: str) -> str:
        return re.sub(r"\{(.*)\}", "", text).strip()

    @staticmethod
    def remove_square_brackets(text: str) -> str:
        return re.sub(r"[\[\]]", "", text).strip()

    @staticmethod
    def remove_square_brackets_content(text: str) -> str:
        return re.sub(r"\[(.*)\]", "", text).strip()
