from youtubesearchpython import CustomSearch, Transcript
from datetime import datetime
import csv
import os
import gc


class ExtractTranscripts():
    def __init__(self,
                 query: str,
                 pages_limit=10,
                 search_limit=100,
                 search_language='en',
                 search_region='US',
                 search_filter='EgQYAygB'):

        """
        Walk through video links of single query and extract containing transcripts
        Commonly (hard)tuned for English

        :param query: str
            Query used for youtube search bar
        :param pages_limit: int
            Num of iterations (searches) that call next page
        :param search_limit: int
            Max number of links returned per search
        :param search_language: str
            Search language. Parameter for youtube engine
        :param search_region: str
            Reginal parameter for youtube engine
        :param search_filter: str
            Text code that follows youtube query filtering pattern and also seen as 'sp' parameter
            (ex. https://www.youtube.com/results?search_query=science&sp=EgQYAygB)
        """

        self.links = []
        self.titles = []
        self.transcripts = []
        self.lang_types = []

        self.query = query
        self.p_lim = pages_limit
        self.s_lim = search_limit
        self.s_lang = search_language
        self.s_region = search_region
        self.s_pref = search_filter

    def create_search(self):
        self.search = CustomSearch(self.query,
                                   limit=self.s_lim,
                                   searchPreferences=self.s_pref,
                                   language=self.s_lang,
                                   region=self.s_region)

    def process_query(self):
        processed_cnt = 0
        print("Processed pages:...", end='')
        while True:

            # process page
            self.process_page()
            processed_cnt += 1
            print(f"{processed_cnt}...", end='')
            try:
                self.search.next()
            except:
                break
            if processed_cnt >= self.p_lim:
                break
        print("Done")

    def check_en_lang(self, transcripts: list) -> tuple:
        for elem in transcripts:
            if elem['selected']:
                if 'English' in elem['title']:
                    return (True, elem['title'])
        return (False, None)

    def process_page(self):
        page_result = self.search.result()['result']
        for i in range(len(page_result)):
            title = page_result[i]['title']
            url = page_result[i]['link']
            try:
                ts = Transcript.get(url)
                is_valid_language, language_type = self.check_en_lang(ts['languages'])
                if not is_valid_language:
                    continue
                ts_list = [elem['text'] for elem in ts['segments']]
                ts_text = ' '.join(ts_list)
                text = ts_text.replace('\n', ' ').replace('\xa0', ' ').replace(';', '.').replace('  ', ' ')
            except:
                continue
            self.links.append(url)
            self.titles.append(title)
            self.transcripts.append(text)
            self.lang_types.append(language_type)

    def store_data(self):
        fn = datetime.now().strftime('%Y%m%d%H%M%S')
        dest_path = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        with open(f"{dest_path}/{fn}.csv", 'a', newline='', encoding='utf-16') as f:
            fieldnames = ['Link', 'Title', 'Language_type', 'Transcript']
            writer = csv.writer(f)
            for i in range(len(self.titles)):
                writer.writerow([self.links[i],
                                 self.titles[i],
                                 self.lang_types[i],
                                 self.transcripts[i]])

    def run(self):
        self.create_search()
        self.process_query()
        self.store_data()



if __name__ == "__main__":

    # search phrases to process
    queries = ['vr technologies', 'robotics', 'science', 'quantum mechanics', 'dvc python', 'ml ops']

    for query in queries:
        print(f"Extracting subtitles for query: '{query}'")
        ext = ExtractTranscripts(query=query)
        ext.run()

        del ext
        gc.collect()