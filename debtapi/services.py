import requests


class DebtAPIService:

    @classmethod
    def get_base_url(cls, country):
        return f"https://api.worldbank.org/v2/country/{country}/indicator"

    @classmethod
    def _fetch_debt_from_third_party(
        cls, 
        indicator, 
        counterpart='', 
        country=None,
    ):
        mrv = 'mrv=1'
        base_url = cls.get_base_url(country.upper() if country else 'NGA')

        if not base_url:
            base_url = cls.get_base_url('NGA')  # Default to NGA if no country is passed
        params = f"?{mrv}&format=json"

        if counterpart:
            params += f"&counterpartArea={counterpart}"
        url = f"{base_url}/{indicator}{params}"

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if len(data) > 1 and data[1]:
                val = data[1][0]
                if val.get('value') is not None:
                    return {
                        'value': float(val['value']),
                        'year': val['date'],
                        'note': val.get('decimal')  # optional
                    }
            return {'value': 0, 'year': 'N/A'}
        except:
            return {'value': 0, 'year': 'N/A'}

    @classmethod
    def fetch_agg(cls, indicator):
        """ Helper to fetch aggregate indicators (no counterpart)"""

        return cls._fetch_debt_from_third_party(indicator)
    
    
    @classmethod
    def fetch_debt(cls,  param=None):
        country = param.get('country', 'NGA').upper() if param else 'NGA'
        total_external = cls.fetch_agg('DT.DOD.DECT.CD')
        multilateral_total = cls.fetch_agg('DT.DOD.MLAT.CD')
        bilateral_total = cls.fetch_agg('DT.DOD.BLAT.CD')
        private_total = cls.fetch_agg('DT.DOD.PRVT.CD')  # Or DT.DOD.PPNG.CD for PPG private

        # Specific multilaterals
        imf = cls._fetch_debt_from_third_party(
            'DT.DOD.DECT.CD',  # Or use DT.DOD.DIMF.CD if available
            '1MF',
            country=country,
        )    
        world_bank = cls._fetch_debt_from_third_party(
            'DT.DOD.DECT.CD', 
            '1WB', 
            country=country
        )
        # Major bilateral (expand as needed; filter non-zero)
        major_bilaterals = ['CHN', 'JPN', 'FRA', 'DEU', 'IND', 'SAU', 'TUR', 'GBR', 'USA', 'RUS']
        bilateral_details = {}
        for code in major_bilaterals:
            debt = cls._fetch_debt_from_third_party(
                'DT.DOD.DECT.CD', 
                code, 
                country=country
            )
            if debt['value'] > 0:
                bilateral_details[code] = debt

        # "sum of known" for validation
        # known_multilateral = imf['value'] + world_bank['value']  
        known_bilateral = sum(d['value'] for d in bilateral_details.values())

        return {
            'country': country,
            'latest_year': total_external.get('year', 'N/A'),
            'grand_total_external_debt_usd': total_external,
            'breakdown': {
                'multilateral_total_usd': multilateral_total,
                'bilateral_total_usd': bilateral_total,
                'private_creditors_total_usd': private_total,
                #short_term_usd = fetch_agg('DT.DOD.DSTC.CD'),
            },
            'multilateral_details': {
                'imf_usd': imf,
                'world_bank_usd': world_bank,
                # TODO: Add AfDB ('counterpartArea=AFDB') 
            },
            'bilateral_details': bilateral_details,  # Country code → amount
            'notes': [
                'Amounts in current USD, latest available year from World Bank IDS.',
                f"Grand total should ≈ multilateral + bilateral + private (known bilateral sum: ${known_bilateral:,.0f}).",
                'Bilateral details show major reported creditors only; full list via counterpart-area API.'
            ]
        }
