import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets


class DebtViewSet(viewsets.ViewSet):
    def list(self, request):
        country = request.GET.get('country', 'NGA').upper()
        mrv = 'mrv=1'
        
        base_url = f"https://api.worldbank.org/v2/country/{country}/indicator"
        def fetch_debt(indicator, counterpart=''):
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

        # Helper to fetch aggregate indicators (no counterpart)
        def fetch_agg(indicator):
            return fetch_debt(indicator)  # Reuse your function

        # Main aggregates
        try:
            total_external = fetch_agg('DT.DOD.DECT.CD')
            multilateral_total = fetch_agg('DT.DOD.MLAT.CD')
            bilateral_total = fetch_agg('DT.DOD.BLAT.CD')
            private_total = fetch_agg('DT.DOD.PRVT.CD')  # Or DT.DOD.PPNG.CD for PPG private

            # Specific multilaterals
            imf = fetch_debt('DT.DOD.DECT.CD', '1MF')     # Or use DT.DOD.DIMF.CD if available
            world_bank = fetch_debt('DT.DOD.DECT.CD', '1WB')

            # Major bilateral (expand as needed; filter non-zero)
            major_bilaterals = ['CHN', 'JPN', 'FRA', 'DEU', 'IND', 'SAU', 'TUR', 'GBR', 'USA', 'RUS']
            bilateral_details = {}
            for code in major_bilaterals:
                debt = fetch_debt('DT.DOD.DECT.CD', code)
                if debt['value'] > 0:
                    bilateral_details[code] = debt

            # "sum of known" for validation
            known_multilateral = imf['value'] + world_bank['value']  
            known_bilateral = sum(d['value'] for d in bilateral_details.values())

            result = {
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
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Failed to fetch debt data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)