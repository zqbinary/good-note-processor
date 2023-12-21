from abc import ABC, abstractmethod

from service.WebProcessor import WebProcessor


class RuleStrategy(ABC):
    def __init__(self, soup):
        self.soup = soup

    @abstractmethod
    def apply_rule(self, location=None):
        pass


class StrategyFactory:

    def __init__(self):
        self.STRATEGY_MAP = {
            'learn.lianglianglee.com': Lianglianglee
        }

    def get_strategy(self, key, soup) -> RuleStrategy | None:
        try:
            if key not in self.STRATEGY_MAP:
                print('no rule for ' + key)
                return None
            return self.STRATEGY_MAP[key](soup)
        except Exception as e:
            print('strategy error', e)
            return None


class Lianglianglee(RuleStrategy):

    def apply_rule(self, location=None):
        remove_selector = [
            'div>div>a', 'div>div>hr',
            '.copyright'
        ]
        WebProcessor.remove_eles_by_selectors(remove_selector, self.soup)
        for tag in self.soup.find_all('h1'):
            new_tag = self.soup.new_tag('h2')
            new_tag.string = tag.get_text()
            tag.replace_with(new_tag)

        for img in self.soup.find_all('img'):
            img_url = img.get('src')
            if img_url.startswith('assets'):
                pieces = location['pathname'].split('/')
                img['src'] = location['origin'] + '' + '/'.join(pieces[0:-1]) + '/' + img_url
