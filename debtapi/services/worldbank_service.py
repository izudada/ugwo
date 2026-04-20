import requests
from datetime import datetime


class WorldBankService:

    @classmethod
    def get_base_url(cls, country):
        return f"https://api.worldbank.org/v2/country/{country}/indicator"

    @classmethod
    def _build_url(cls, indicator, country_code, counterpart='', date_param=None):
        """Build URL with proper parameter handling"""
        base = cls.get_base_url(country_code.upper())
        
        params = ['format=json']
        
        if date_param:
            params.append(f"date={date_param}")
        else:
            params.append("mrv=1")   # default to most recent
        
        if counterpart:
            params.append(f"counterpartArea={counterpart}")
        
        query_string = "&".join(params)
        return f"{base}/{indicator}?{query_string}"

    @classmethod
    def _fetch_single(cls, indicator, country_code, counterpart='', date_param=None):
        """Fetch one specific data point or most recent"""
        url = cls._build_url(indicator, country_code, counterpart, date_param)
        
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            
            if len(data) > 1 and data[1]:
                val = data[1][0]
                if val.get('value') is not None:
                    return {
                        'value': float(val['value']),
                        'year': val['date'],
                    }
            return {'value': 0, 'year': 'N/A'}
        except Exception:
            return {'value': 0, 'year': 'N/A'}

    @classmethod
    def fetch_range(cls, indicator, country_code, start_year, end_year=None, counterpart=''):
        """Fetch data for a range of years in ONE API call (best practice)"""
        if end_year is None:
            end_year = datetime.now().year + 1
        
        date_param = f"{start_year}:{end_year}"
        url = cls._build_url(indicator, country_code, counterpart, date_param)
        
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            
            if len(data) > 1:
                result = {}
                for item in data[1]:
                    if item.get('value') is not None:
                        result[int(item['date'])] = {
                            'value': float(item['value']),
                            'year': item['date']
                        }
                return result
            return {}
        except Exception:
            return {}

    # Keep fetch_for_year if needed for single year
    @classmethod
    def fetch_for_year(cls, indicator, year, country_code, counterpart=''):
        return cls._fetch_single(indicator, country_code, counterpart, date_param=str(year))
