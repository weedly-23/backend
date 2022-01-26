import re

import requests
from bs4 import BeautifulSoup


class YoutubService:
    '''
    the function gets youtube urls, channel ids, playlist ids and converts them into the proper
    standard ID form:
    "UC...." or "UU...." (24 characters string); or "PL...." (34 character string)

    :param input_string:
    :return:

    '''

    def extract_channel_id(self, input: str) -> str:
        patterns = [
            re.compile('U[UC][^&=]{22}'),
            re.compile('PL[^&=]{32}'),
            re.compile('RD[^&=]{41}'),
        ]
        for patern in patterns:
            my_search = patern.search(input)
            if my_search:
                break
        if my_search:
            proper_yt_id = my_search.group()
            return re.sub('^UU', 'UC', proper_yt_id)
        try:
            yt_content = requests.get(input.strip()).content
            soup = BeautifulSoup(yt_content, 'html.parser')
            channel_url = soup.select_one("link[rel='canonical']").get('href')
            channel_id = channel_url.split('/')[-1]
            if channel_id != 'null' and channel_url != input:
                return channel_id
            channel_tag = soup.select_one("meta[itemprop='channelId']")
            return channel_tag.get('content')
        except ValueError:
            return f'Problem with INPUT: {input}'


if __name__ == '__main__':
    yt = YoutubService()
    inputs = [
        'https://www.youtube.com/watch?v=pwbD-yva2Cg',
        'https://www.youtube.com/channel/UCFNfeiYmTZ0f9oFj13_Re3g',
        'https://www.youtube.com/c/NavalnyLiveChannel',
        'https://www.youtube.com/c/ntvru',
        'https://www.youtube.com/c/tvrain',
        'https://www.youtube.com/watch?v=PlBrgFe5Fhg&list=PLUh4W61bt_K78f3sc1iM3NMN0_RM0f9Cv',
    ]
    for input in inputs:
        channel_id = yt.extract_channel_id(input)
        print(channel_id)
