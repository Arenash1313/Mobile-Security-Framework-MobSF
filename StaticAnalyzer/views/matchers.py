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
        return bool(re.findall(rule['match'], content))


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
                return False
        return True


class RegexOr(MatchStrategy):
    def perform_search(self, content, rule, perms):
        if isinstance(rule['match'], str):
            logger.debug('wrong regex type, switching to single regex')
            return SingleRegex().perform_search(content, rule, perms)
        for regex in rule['match']:
            if re.findall(regex, content):
                return True
        return False


class SingleString(MatchStrategy):
    def perform_search(self, content, rule, perms):
        return rule['match'] in content


class StringAnd(MatchStrategy):
    def perform_search(self, content, rule, perms):
        for match in rule['match']:
            if not match in content:
                return False
        return True


class StringAndOr(MatchStrategy):
    def perform_search(self, content, rule, perms):
        string_or_stat = False
        or_list = rule['match'][1]
        for match in or_list:
            if match in content:
                string_or_stat = True
                break
        return string_or_stat and rule['match'][0] in content


class StringOrAndPerm(MatchStrategy):
    def perform_search(self, content, rule, perms):
        string_or_ps = False
        for match in rule['match']:
            if match in content:
                string_or_ps = True
                break
        return rule['perm'] in perms and string_or_ps


class StringAndPerm(MatchStrategy):
    def perform_search(self, content, rule, perms):
        return rule['perm'] in perms and rule['match'] in content


class StringOr(MatchStrategy):
    def perform_search(self, content, rule, perms):
        for match in rule['match']:
            if match in content:
                return True
        return False


class StringAndNot(MatchStrategy):
    def perform_search(self, content, rule, perms):
        return rule['match'][0] in content and rule['match'][1] not in content
