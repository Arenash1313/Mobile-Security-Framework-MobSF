from abc import ABC, abstractclassmethod
import re
import logging

logger = logging.getLogger(__name__)


class MatchCommand:

    def __init__(self):
        self.patterns = {}

    def find_match(self, pattern_name, content, rule, perms):
        if pattern_name not in self.patterns:
            logger.debug('adding %s in the pool of patterns', pattern_name)
            pattern_class = globals()[pattern_name]
            self.patterns[pattern_name] = pattern_class()
        return self.patterns[pattern_name].perform_search(content, rule, perms)


class MatchStrategy(ABC):

    @abstractclassmethod
    def perform_search(self, content, rule, perms):
        """Search for instance of match in content."""


class SingleRegex(MatchStrategy):

    def perform_search(self, content, rule, perms):
        found = False
        if re.findall(rule['match'], content):
            found = True
        return found


class RegexAnd(MatchStrategy):
    def perform_search(self, content, rule, perms):
        found = True
        # This check is used because if you only pass a str rather than a list,
        # Python will iterate through the str without raising an exception
        if isinstance(rule['match'], str):
            logger.debug('wrong regex type, switching to single regex')
            return SingleRegex().perform_search(content, rule, perms)
        for regex in rule['match']:
            if not bool(re.findall(regex, content)):
                found = False
                break
        return found


class RegexOr(MatchStrategy):
    def perform_search(self, content, rule, perms):
        found = False
        if isinstance(rule['match'], str):
            logger.debug('wrong regex type, switching to single regex')
            return SingleRegex().perform_search(content, rule, perms)
        for regex in rule['match']:
            if re.findall(regex, content):
                found = True
                break
        return found


class SingleString(MatchStrategy):
    def perform_search(self, content, rule, perms):
        found = False
        if rule['match'] in content:
            found = True
        return found


class StringAnd(MatchStrategy):
    def perform_search(self, content, rule, perms):
        and_match_str = True
        for match in rule['match']:
            if (match in content) is False:
                and_match_str = False
                break
        return and_match_str


class StringAndOr(MatchStrategy):
    def perform_search(self, content, rule, perms):
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


class StringOrAndPerm(MatchStrategy):
    def perform_search(self, content, rule, perms):
        found = False
        string_or_ps = False
        for match in rule['match']:
            if match in content:
                string_or_ps = True
                break
        if(rule['perm'] in perms) and string_or_ps:
            found = True
        return found


class StringAndPerm(MatchStrategy):
    def perform_search(self, content, rule, perms):
        found = False
        if(rule['perm'] in perms and rule['match'] in content):
            found = True
        return found


class StringOr(MatchStrategy):
    def perform_search(self, content, rule, perms):
        found = False
        for match in rule['match']:
            if match in content:
                found = True
                break
        return found


class StringAndNot(MatchStrategy):
    def perform_search(self, content, rule, perms):
        found = False
        if (rule['match'][0] in content and rule['match'][1] not in content):
            found = True
        return found