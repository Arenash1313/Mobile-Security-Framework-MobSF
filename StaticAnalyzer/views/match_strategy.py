from abc import ABC, abstractclassmethod
import re
import logging

logger = logging.getLogger(__name__)


class MatchStrategy(ABC):

    @abstractclassmethod
    def perform_search(self, content, rule, perms):
        """
        Search for instance of match in content
        """


<<<<<<< HEAD
class SingleRegex(MatchStrategy):
=======
class single_regex(MatchStrategy):
>>>>>>> 2af7f1d8917636d7ef249d475e3fc8d6e588768e

    def perform_search(self, content, rule, perms):
        found = False
        if re.findall(rule['match'], content):
            found = True
        return found


<<<<<<< HEAD
class RegexAnd(MatchStrategy):
=======
class regex_and(MatchStrategy):
>>>>>>> 2af7f1d8917636d7ef249d475e3fc8d6e588768e
    def perform_search(self, content, rule, perms):
        found = True
        # This check is used because if you only pass a str rather than a list,
        # Python will iterate through the str without raising an exception
        if isinstance(rule['match'], str):
            logger.debug("wrong regex type, switching to single regex")
<<<<<<< HEAD
            return SingleRegex().perform_search(content, rule, perms)
=======
            return single_regex().perform_search(content, rule, perms)
>>>>>>> 2af7f1d8917636d7ef249d475e3fc8d6e588768e
        for regex in rule['match']:
            if bool(re.findall(regex, content)) is False:
                found = False
                break
        return found


<<<<<<< HEAD
class RegexOr(MatchStrategy):
=======
class regex_or(MatchStrategy):
>>>>>>> 2af7f1d8917636d7ef249d475e3fc8d6e588768e
    def perform_search(self, content, rule, perms):
        found = False
        if isinstance(rule['match'], str):
            logger.debug("wrong regex type, switching to single regex")
<<<<<<< HEAD
            return SingleRegex().perform_search(content, rule, perms)
=======
            return single_regex().perform_search(content, rule, perms)
>>>>>>> 2af7f1d8917636d7ef249d475e3fc8d6e588768e
        for regex in rule['match']:
            if re.findall(regex, content):
                found = True
                break
        return found

<<<<<<< HEAD
class SingleString(MatchStrategy):
    def perform_search(self, content, rule, perms):
        found = False
        if rule['match'] in content:
            found = True
        return found

class StringAnd(MatchStrategy):
=======

class string_and(MatchStrategy):
>>>>>>> 2af7f1d8917636d7ef249d475e3fc8d6e588768e
    def perform_search(self, content, rule, perms):
        and_match_str = True
        for match in rule['match']:
            if (match in content) is False:
                and_match_str = False
                break
        return and_match_str
<<<<<<< HEAD

class StringAndOr(MatchStrategy):
    def perform_search(self, content,rule, perms):
        found = False
        string_or_stat = False
        or_list = rule['match'][1]
        for match in or_list:
            if match in content:
                string_or_stat = True
                break
        if string_or_stat and rule['match'][0] in content:
            found = True
        return found
=======
>>>>>>> 2af7f1d8917636d7ef249d475e3fc8d6e588768e
