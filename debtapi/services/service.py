from helpers import CacheManager
from .imf_service import IMFService
from .worldbank_service import WorldBankService
from debtapi.enums import DataSource


class DebtAPIService: 

    @classmethod
    def fetch_debt(cls, param):
        country = param.get('country').upper()
        year = param.get('year')          
        start_year = param.get('start_year')
        end_year = param.get('end_year')

        date_param = str(year.year) if year else None

        source = DataSource.WORLD_BANK 
        result = WorldBankService._fetch_single(
            'DT.DOD.DECT.CD', country, date_param=date_param
        ).get('value', 0)

        if result == 0:
            result = IMFService.compute_actual_debt([country], date_param)[country]
            source = DataSource.IMF

        # multilateral_total = fetch_func["func"]('DT.DOD.MLAT.CD', country, date_param=date_param)
        # bilateral_total = fetch_func["func"]('DT.DOD.BLAT.CD', country, date_param=date_param)
        # private_total = fetch_func["func"]('DT.DOD.PRVT.CD', country, date_param=date_param)

        # # Specific multilaterals (most recent or specific year)
        # imf = fetch_func('DT.DOD.DECT.CD', country, '1MF', date_param=date_param)
        # world_bank = fetch_func('DT.DOD.DECT.CD', country, '1WB', date_param=date_param)

        # # Bilateral breakdown (most recent by default)
        # major_bilaterals = ['CHN', 'JPN', 'FRA', 'DEU', 'IND', 'SAU', 'TUR', 'GBR', 'USA', 'RUS']
        # bilateral_details = {}
        # for code in major_bilaterals:
        #     debt = fetch_func('DT.DOD.DECT.CD', country, code, date_param=date_param)
        #     print(100, debt)
        #     if debt.get('value', 0) > 0:
        #         bilateral_details[code] = debt

        # known_bilateral = sum(d.get('value', 0) for d in bilateral_details.values())
  
        return {
            'country': country,
            'requested_year': year or (f"{start_year}-{end_year}" if start_year else 'latest'),
            'total_external_debt_usd': f"{result:,.0f}",
            # 'breakdown': {
            #     'multilateral_total_usd': multilateral_total,
            #     'bilateral_total_usd': bilateral_total,
            #     'private_creditors_total_usd': private_total,
            # },
            # 'multilateral_details': {
            #     'imf_usd': imf,
            #     'world_bank_usd': world_bank,
            # },
            # 'bilateral_details': bilateral_details,
            'notes': [
                f"Data source: {source} International Debt Statistics API.",
                f"sum: ${result:,.0f} USD",
                # 'Use ?year=2023 or ?start_year=2018&end_year=2024 for historical data.'
            ]
        }
    
    @classmethod
    def fetch_from_imf(cls, param):
        country = param.get('country').upper()
        year = param.get('year')          
        # start_year = param.get('start_year')
        # end_year = param.get('end_year')

        date_param = str(year.year) if year else None

        country = [country]  # IMFService expects a list of countries
        return IMFService.compute_actual_debt(country, date_param)[country[0]]
    
    @classmethod
    def fetch_from_worldbank(cls, param):
        country = param.get('country').upper()
        year = param.get('year')          
        # start_year = param.get('start_year')
        # end_year = param.get('end_year')

        date_param = str(year.year) if year else None

        return WorldBankService._fetch_single('DT.DOD.DECT.CD', country, date_param=date_param)
