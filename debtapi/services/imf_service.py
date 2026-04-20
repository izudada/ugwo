import requests


class IMFService:
    BASE_URL = "https://www.imf.org/external/datamapper/api/v1"
    DEBT_UNIT_MULTIPLIER = 1_000_000_000  # Convert from billions to actual USD

    @classmethod
    def fetch_indicator(cls, indicator, countries):
        country_str = ";".join(countries)
        url = f"{cls.BASE_URL}/{indicator}/{country_str}"
        return requests.get(url).json()["values"][indicator]

    @classmethod
    def compute_actual_debt(cls, countries, year):
        debt_ratio = cls.fetch_indicator("GGXWDG_NGDP", countries)
        gdp = cls.fetch_indicator("NGDPD", countries)

        result = {}

        for country in countries:
            try:
                ratio = debt_ratio[country][str(year)]
                gdp_value = gdp[country][str(year)]

                # Convert to actual USD
                actual_debt = (ratio / 100) * gdp_value * cls.DEBT_UNIT_MULTIPLIER

                result[country] = round(actual_debt, 2)

            except KeyError:
                result[country] = None

        return result
