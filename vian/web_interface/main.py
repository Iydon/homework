from flask import Flask, jsonify, send_file

from api.appannie import API, Appannie
from api.cache import Cache
from models import APIHooker, Config, form


config = Config()
api = API(**config['appannie'])
cache = Cache(**config['cache'])
api_hooker = APIHooker(Flask(__name__, static_url_path='/static'))

(  # core
    api_hooker.add(lambda: config.data, 'core.config', 'Check the configuration file, remember to modify it locally.', dict(), jsonify),
)

(  # cache
    api_hooker.add(
        cache.getsize, 'cache.getsize', cache.getsize.__doc__, dict(),
        lambda x: f'缓存大小 {x/2**20:.3f} MB'
    ).add(
        cache.clear_zip_tsv, 'cache.clear_zip_tsv', cache.clear_zip_tsv.__doc__, dict(), str
    )
)

(  # appannie
    api_hooker.add(
        api.countries, 'appannie.countries', Appannie.countries.__doc__, dict(), str
    ).add(
        api.app_detail, 'appannie.app_detail', Appannie.app_detail.__doc__, {
            'market': (
                form.datalist, {
                    'options': ('ios', 'mac', 'appletv', 'google-play', 'amazon-appstore'),
                }
            ),
            'product_id': (form.text, dict()),
        }, str
    ).add(
        api.company_detail, 'appannie.company_detail', Appannie.company_detail.__doc__, {
            'company_id': (form.text, dict()),
        }, str
    ).add(
        api.categories, 'appannie.categories', Appannie.categories.__doc__, {
            'market': (
                form.datalist, {
                    'options': ('ios', 'mac', 'appletv', 'google-play', 'amazon-appstore'),
                }
            ),
        }, str
    ).add(
        api.download_revenue, 'appannie.download_revenue', Appannie.download_revenue.__doc__, {
            'market': (
                form.datalist, {
                    'options': ('ios', 'google-play'),
                }
            ),
            'countries': (
                form.datalist, {
                    'options': {
                        country['country_code']: country['country_name']
                        for country in api.appannie.countries()['country_list']
                    },
                }
            ),
            'categories': (
                form.group, {
                    'options': {
                        key: tuple(
                            category['category_path']
                            for category in api.appannie.categories(key)['category_list']
                        )
                        for key in ('ios', 'mac', 'appletv', 'google-play', 'amazon-appstore')
                    },
                }
            ),
            'device': (
                form.datalist, {
                    'options': ('ios', 'iphone', 'ipad', 'android'),
                }
            ),
            'start_date': (form.date, dict()),
            'feeds': (
                form.datalist, {
                    'options': ('all feeds', 'free', 'paid', 'grossing'),
                }
            ),
            'ranks': (
                form.range, {
                    'min': 1, 'max': 1000, 'step': 1, 'default': 1000,
                }
            ),
            'granularity': (
                form.datalist, {
                    'options': ('daily', 'weekly', 'monthly'),
                }
            ),
        }, jsonify
    ).add(
        api.convert_download_revenue_to_csv, 'appannie.convert_download_revenue_to_csv', api.convert_download_revenue_to_csv.__doc__, {
            'markets': (
                form.checkbox, {
                    'options': ('ios', 'google-play'),
                }
            ),
            'countries': (
                form.multiple, {
                    'options': {
                        country['country_code']: country['country_name']
                        for country in api.appannie.countries()['country_list']
                    },
                }
            ),
            'feeds': (
                form.checkbox, {
                    'options': ('free', 'paid', 'grossing'),
                }
            ),
            'devices': (
                form.checkbox, {
                    'options': ('ios', 'iphone', 'ipad', 'android'),
                }
            ),
            'category_ios': (
                form.datalist, {
                    'options': tuple(
                        category['category_path']
                        for category in api.appannie.categories('ios')['category_list']
                    ),
                }
            ),
            'category_google': (
                form.datalist, {
                    'options': tuple(
                        category['category_path']
                        for category in api.appannie.categories('google-play')['category_list']
                    ),
                }
            ),
            'start_date': (form.date, dict()),
            'rank': (
                form.range, {
                    'min': 1, 'max': 1000, 'step': 1, 'default': 50,
                }
            ),
            'granularity': (
                form.datalist, {
                    'options': ('daily', 'weekly', 'monthly'),
                }
            ),
        }, lambda x: send_file(x, as_attachment=True)
    ).add(
        api.convert_monthly_download_revenue_to_csv, 'appannie.convert_monthly_download_revenue_to_csv', api.convert_monthly_download_revenue_to_csv.__doc__, {
            'markets': (
                form.checkbox, {
                    'options': ('ios', 'google-play'),
                }
            ),
            'countries': (
                form.multiple, {
                    'options': {
                        country['country_code']: country['country_name']
                        for country in api.appannie.countries()['country_list']
                    },
                }
            ),
            'feeds': (
                form.checkbox, {
                    'options': ('free', 'paid', 'grossing'),
                }
            ),
            'devices': (
                form.checkbox, {
                    'options': ('ios', 'iphone', 'ipad', 'android'),
                }
            ),
            'category_ios': (
                form.datalist, {
                    'options': tuple(
                        category['category_path']
                        for category in api.appannie.categories('ios')['category_list']
                    ),
                }
            ),
            'category_google': (
                form.datalist, {
                    'options': tuple(
                        category['category_path']
                        for category in api.appannie.categories('google-play')['category_list']
                    ),
                }
            ),
            'start_month': (form.month, dict()),
            'end_month': (form.month, dict()),
            'rank': (
                form.range, {
                    'min': 1, 'max': 1000, 'step': 1, 'default': 50,
                }
            ),
        }, lambda x: send_file(x, as_attachment=True)
    )
)

api_hooker.run(debug=True)
