import collections
import datetime
import hashlib
import itertools
import json
import pathlib
import re
import requests
import time
import zipfile

from typing import Iterable


class Appannie:
    def __init__(self, api_key, cache_dir, meta_file, proxies=None, encoding='utf-8'):
        self._api_key = api_key
        self._cache_dir = pathlib.Path(cache_dir)
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._meta_path = self._cache_dir / meta_file
        self._proxies = proxies
        self._encoding = encoding

    def countries(self) -> dict:
        '''
        Reference:
            - https://helpcenter.appannie.com/community/s/article/1-Country-List
        '''
        url = 'https://api.appannie.com/v1.3/meta/countries'
        return self._get(url)

    def categories(self, market:str) -> dict:
        '''
        Argument:
            - market: str, in {'ios', 'mac', 'appletv', 'google-play', 'amazon-appstore'}

        Reference:
            - https://helpcenter.appannie.com/community/s/article/2-Category-List
        '''
        url = f'https://api.appannie.com/v1.3/meta/apps/{market}/categories'
        return self._get(url)

    def app_detail(self, market:str, product_id:[str, int]) -> dict:
        '''
        Argument:
            - market, str, in {'ios', 'mac', 'appletv', 'google-play', 'amazon-appstore'}
            - product_id, str or int

        Reference:
            - https://helpcenter.appannie.com/community/s/article/1-App-Details
        '''
        url = f'https://api.appannie.com/v1.3/apps/{market}/app/{product_id}/details'
        return self._get(url)

    def company_detail(self,
            company_id:[str, int], detail_type:str, page_size:[str, int]=1000, page_index:[str, int]=0
        ) -> dict:
        '''
        Argument:
            - company_id: str or int
            - product_id: str, in {'subsidiaries_and_publishers', 'apps'}
            - page_size: str or int, specifies the response page size, accept integer from 0 to 1000
                (Only applies if detail_type is 'apps')
            - page_index: str or int, current page index, count starts from 0, default is 0

        Reference:
            - https://helpcenter.appannie.com/community/s/article/Company-Publisher-Details-APIs
        '''
        url = f'https://api.appannie.com/v1.3/company/{company_id}/{detail_type}'
        params = None
        if detail_type == 'apps':
            params = {'page_size': page_size, 'page_index': page_index}
        return self._get(url, params)

    def download_revenue(self,
            market:str, countries:str, categories:str, device:str, start_date:str,
            feeds:str='all feeds', ranks:int=1000, granularity:str='weekly'
        ) -> dict:
        '''
        Argument:
            - market: str, in {'ios', 'google-play'}
            - countries: str, two digit country code (refer to `self.countries`)
            - categories: str, refer to `self.categories`
            - device: str, in {'ios', 'iphone', 'ipad', 'android'}
            - start_date: str, yyyy-mm-dd format
            - feeds: str, in {'free', 'paid', 'grossing'}, default is 'all feeds'
            - ranks: int, in range(1, 1001), default is 1000
            - granularity: str, in {'daily', 'weekly', 'monthly'}, default is 'weekly'

        Reference:
            - https://helpcenter.appannie.com/community/s/article/Downloads-Revenue-APIs
        '''
        url = f'https://api.appannie.com/v1.3/intelligence/apps/{market}/ranking'
        params = {
            'countries': countries, 'categories': categories, 'feeds': feeds, 'ranks': ranks,
            'granularity': granularity, 'device': device, 'start_date': start_date,
        }
        feeds=='all feeds' and params.pop('feeds')
        return self._get(url, params)

    def _get(self, url, params=None):
        kwargs = {
            'url': url,
            'params': params,
            'proxies': self._proxies,
            'headers': {
                'Authorization': f'Bearer {self._api_key}',
                'Accept': 'application/json',
            },
        }
        text, md5 = self._hash(**kwargs)
        path = self._cache_dir / md5
        if path.exists():
            return json.loads(path.read_text(encoding=self._encoding))
        else:
            data = requests.get(**kwargs).json()
            assert data.get('code', None)==200, str(data)
            path.write_text(json.dumps(data), encoding=self._encoding)
            with open(self._meta_path, 'a+') as f:
                f.write(f'{md5}\t{text}\n')
            return data

    def _hash(self, **kwargs):
        text = repr('\n'.join(f'{key}\t{value}' for key, value in kwargs.items()))
        md5 = hashlib.md5(text.encode(encoding=self._encoding)).hexdigest()
        return text, md5

    def _months_between(self, start_date, end_date, pattern_1='%Y-%m', pattern_2='%Y-%m-%d'):
        f = lambda x: datetime.datetime.strptime(x, pattern_1)
        start, end = f(start_date), f(end_date)
        start_ym = 12*start.year + start.month - 1
        end_ym = 12*end.year + end.month
        for y, m in map(lambda x: divmod(x, 12), range(start_ym, end_ym)):
            yield datetime.datetime(y, m+1, 1).strftime(pattern_2)


class API:
    def __init__(self, **kwargs):
        self._appannie = Appannie(**kwargs)

    @property
    def appannie(self):
        return self._appannie

    def countries(self):
        data = self._appannie.countries()['country_list']
        return self._table2d(data[0].keys(), data)

    def categories(self, market):
        data = self._appannie.categories(market)['category_list']
        return self._table2d(data[0].keys(), data)

    def app_detail(self, market, product_id):
        data = self._appannie.app_detail(market, product_id)['product']
        return self._table1d(data)

    def company_detail(self, company_id):
        data = self._appannie.company_detail(company_id, 'subsidiaries_and_publishers')
        return self._table1d(data)

    def download_revenue(self, market, countries, categories, device,
            start_date, feeds='all feeds', ranks=1000, granularity='weekly'
        ):
        return self._appannie.download_revenue(
            market, countries, categories, device, start_date, feeds, ranks, granularity
        )

    def convert_download_revenue_to_csv(self,
            markets:Iterable, countries:Iterable, feeds:Iterable, devices:Iterable,
            category_ios:str, category_google:str, start_date:str, rank:[str, int], granularity:str
        ):
        '''Convert Downloads&Revenue data to CSV

        Argument:
            - markets: Iterable, in {'ios', 'google-play'}
            - countries: Iterable
            - feeds: Iterable, in {'free', 'paid', 'grossing'}
            - devices: Iterable, in {'ios', 'iphone', 'ipad', 'android'}, (when market is ios, device=ios means all)
            - category_ios: str
            - category_google: str
            - start_date: str, yyyy-mm-dd format
            - rank: int, in range(1, 1001)
            - granularity: str, in {'daily', 'weekly', 'monthly'}, default is 'weekly'

        Return:
            - zip path

        Reference:
            - https://helpcenter.appannie.com/community/s/article/Downloads-Revenue-APIs
        '''
        zippath = self._appannie._cache_dir / f'{int(1000*time.time())}.zip'
        zipfolder = zipfile.ZipFile(zippath,'w', compression=zipfile.ZIP_STORED)
        market_device_mapper = {'ios': {'ios', 'iphone', 'ipad'}, 'google-play': {'android'}}
        market_category_mapper = {'ios': category_ios, 'google-play': category_google}
        headers = (
            'Rank', 'Estimate', 'Market', 'Device', 'Country', 'Unified Product ID', 'Unified Product Name',
            'Company Name', 'Parent Company Name', 'Publisher Name', 'Headquarter Country',
        )
        for feed in feeds:
            result = dict()
            for country, market, device in self._cmd(countries, markets, devices):
                print(
                    '[convert_download_revenue_to_csv]',
                    f'feed={feed} country={country} market={market} device={device}',
                )
                data = self._appannie.download_revenue(
                    market, country, market_category_mapper[market], device, start_date, feed, rank, granularity,
                )
                for item in data['list'][feed]:
                    data = self._appannie.app_detail(market, item['product_id'])['product']
                    if data['unified_product_id'] not in result:
                        result[data['unified_product_id']] = {
                            'estimate': 0, 'countries': set(), 'markets': set(), 'devices': set(), 'details': dict(),
                        }
                    result[data['unified_product_id']]['estimate'] += item['estimate']
                    result[data['unified_product_id']]['countries'].add(country)
                    result[data['unified_product_id']]['markets'].add(market)
                    result[data['unified_product_id']]['devices'].add(device)
                    result[data['unified_product_id']]['details'][market] = data
            # convert data to csv
            path = self._appannie._cache_dir / self._file(
                feed, ','.join(markets), ','.join(countries), ','.join(devices), category_ios,
                category_google, start_date, rank, granularity, sep='_', extension='.tsv',
            )
            with open(path, 'w', encoding=self._appannie._encoding) as f:
                f.write('\t'.join(headers) + '\n')
                for ith, product_id in enumerate(sorted(result, key=lambda x: result[x]['estimate'], reverse=True)):
                    value = result[product_id]
                    ios_or_google = value['details'].popitem()[1]
                    f.write(
                        '\t'.join(map(str, (
                            ith+1, value['estimate'], ' & '.join(value['markets']), ' & '.join(value['devices']),
                            ' & '.join(value['countries']), product_id, *(
                                ios_or_google.get(key, '') for key in (
                                    'unified_product_name', 'company_name', 'parent_company_name',
                                    'publisher_name', 'headquarter_country'
                                )
                            )
                        ))) + '\n'
                    )
            zipfolder.write(path, arcname=path.name)
        zipfolder.close()
        return zipfolder.filename

    def convert_monthly_download_revenue_to_csv(self,
            markets:Iterable, countries:Iterable, feeds:Iterable, devices:Iterable,
            category_ios:str, category_google:str, start_month:str, end_month:str, rank:[str, int]
        ):
        '''Convert monthly Downloads&Revenue data to CSV

        Argument:
            - markets: Iterable, in {'ios', 'google-play'}
            - countries: Iterable
            - feeds: Iterable, in {'free', 'paid', 'grossing'}
            - devices: Iterable, in {'ios', 'iphone', 'ipad', 'android'}, (when market is ios, device=ios means all)
            - category_ios: str
            - category_google: str
            - start_month: str, yyyy-mm format
            - end_month: str, yyyy-mm format
            - rank: int, in range(1, 1001)

        Return:
            - zip path

        Reference:
            - https://helpcenter.appannie.com/community/s/article/Downloads-Revenue-APIs
        '''
        zippath = self._appannie._cache_dir / f'{int(1000*time.time())}.zip'
        zipfolder = zipfile.ZipFile(zippath,'w', compression=zipfile.ZIP_STORED)
        market_device_mapper = {'ios': {'ios', 'iphone', 'ipad'}, 'google-play': {'android'}}
        market_category_mapper = {'ios': category_ios, 'google-play': category_google}
        headers = (
            'Rank', 'Estimate', 'Market', 'Device', 'Country', 'Unified Product ID', 'Unified Product Name',
            'Company Name', 'Parent Company Name', 'Publisher Name', 'Headquarter Country',
        )
        for feed in feeds:
            result = dict()
            for country, market, device in self._cmd(countries, markets, devices):
                for date in self._appannie._months_between(start_month, end_month):
                    print(
                        '[convert_download_revenue_to_csv]',
                        f'feed={feed} country={country} market={market} device={device} date={date}',
                    )
                    data = self._appannie.download_revenue(
                        market, country, market_category_mapper[market], device, date, feed, rank, 'monthly',
                    )
                    for item in data['list'][feed]:
                        data = self._appannie.app_detail(market, item['product_id'])['product']
                        if data['unified_product_id'] not in result:
                            result[data['unified_product_id']] = {
                                'estimate': 0, 'countries': set(), 'markets': set(), 'devices': set(), 'details': dict(),
                            }
                        result[data['unified_product_id']]['estimate'] += item['estimate']
                        result[data['unified_product_id']]['countries'].add(country)
                        result[data['unified_product_id']]['markets'].add(market)
                        result[data['unified_product_id']]['devices'].add(device)
                        result[data['unified_product_id']]['details'][market] = data
            # convert data to csv
            path = self._appannie._cache_dir / self._file(
                feed, ','.join(markets), ','.join(countries), ','.join(devices), category_ios,
                category_google, start_month, end_month, rank, 'monthly', sep='_', extension='.tsv',
            )
            with open(path, 'w', encoding=self._appannie._encoding) as f:
                f.write('\t'.join(headers) + '\n')
                for ith, product_id in enumerate(sorted(result, key=lambda x: result[x]['estimate'], reverse=True)):
                    value = result[product_id]
                    ios_or_google = value['details'].popitem()[1]
                    f.write(
                        '\t'.join(map(str, (
                            ith+1, value['estimate'], ' & '.join(value['markets']), ' & '.join(value['devices']),
                            ' & '.join(value['countries']), product_id, *(
                                ios_or_google.get(key, '') for key in (
                                    'unified_product_name', 'company_name', 'parent_company_name',
                                    'publisher_name', 'headquarter_country'
                                )
                            )
                        ))) + '\n'
                    )
            zipfolder.write(path, arcname=path.name)
        zipfolder.close()
        return zipfolder.filename

    def _file(self, *args, sep, extension):
        p = re.compile(r'[\/\\\:\*\?\"\<\>\|]')
        return p.sub('-', sep.join(map(str, args))).replace(' ', '') + extension

    def _cmd(self, countries, markets, devices):
        market_device_mapper = {
            'ios': {'ios', 'iphone', 'ipad'}, 'google-play': {'android'},
        }
        for country, market in itertools.product(countries, markets):
            for device in market_device_mapper[market].intersection(devices):
                yield country, market, device

    def _table1d(self, data):
        return '<table border="1">\n' + '\n'.join(
            f'<tr><th>{key}</th><td>{value}</td></tr>'
            for key, value in data.items()
            # if not isinstance(value, (dict, list, tuple))
        ) + '\n</table>'

    def _table2d(self, headers, data):
        columns = '<tr>{}</tr>'.format(''.join(f'<th>{h}</th>' for h in headers))
        body = '\n'.join(
                '<tr>{}</tr>'.format(
                    ''.join(f'<td>{country[header]}</td>' for header in headers)
                ) for country in data
            )
        return f'''
            <table border="1">
                <tr>{columns}</tr>
                {body}
            </table>
        '''
