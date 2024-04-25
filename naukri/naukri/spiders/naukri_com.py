from datetime import datetime

import pytz
from naukri.items import NaukriItem
import scrapy
import json

class NaukriComSpider(scrapy.Spider):
    name = 'naukri_com'
    allowed_domains = ['x']
    start_urls = ['https://resdex.naukri.com/v3/search?agentId=57537901']

    handle_httpstatus_list = [401, 302, 503,403,307]

    def start_requests(self):
        cookies = {
            '_t_ds': '689ecdf1684756884-132689ecdf-0689ecdf',
            'test': 'naukri.com',
            'persona': 'default',
            '_ga': 'GA1.2.537000230.1684756924',
            '_gid': 'GA1.2.466448074.1684756924',
            '_gcl_au': '1.1.119297570.1684756924',
            '_fbp': 'fb.1.1684756933145.460959847',
            '_ga_K2YBNZVRLL': 'GS1.1.1684756923.1.1.1684757158.0.0.0',
            '_did': 'cd600830be',
            '_odur': 'edaf7e3744',
            'page_visit': '1',
            'dfp': '27cb18f51c3d72c2b82645d0488e002d',
            'LPVID': 'YwNzViM2MxM2Y3YzU0OGNh',
            'kycEligibleCookie1360722': '0',
            'UNPC': '1360722',
            'UNCC': '123739023',
            'showDomainLB123739023': '1',
            'showPhotoUploadPage123739023': 'isSet',
            '_abck': 'B1D7AED7848850B22DD68954693A1BA2~0~YAAQD3s1F5DozjuIAQAAL1nDRAnyuSe4yLorJLnCPI1p/N8rsBrRr/Rq+XRns4dnAaQqVJfp4YLghsGKCPyltZ0awOe6sAP6s147vBcdOaalg9mOy54uoM7tRtOsHU+82HG7wdNzl5UzfOJoNrK3NZMmHjU5UnDudCYaHpt2m+uvUX6Cdgnu5AyRGNXluO6jtXFtrZ9rSgmjy7ow8WffJQSs4UNQDYPThPg69GvuIE+m2aCLgx+h7COELO1wwQYHM4g8v8SxpVZlV/2roPW7/ancXZoRdwEmJh/DZ/LTP5jmZrBSzaIRVkAsPXZ67E9pCm/M98NQ0m5BVXKlUoIISNuMuitwd1RvN0FrjEXEHk3DmvqKnkY001VsnCh9rLwhw6WLs5EW4U9NWSngZLTdZVhaHL884kYM~-1~-1~-1',
            'bm_sz': '9DB8C447CAFD715DAD520EADC760172D~YAAQD3s1F5LozjuIAQAAL1nDRBNTEad4FhaVlmj4JA1mQo87xZBdtMS7c4juDcmqr6OBRtLitOiRZmdP7KB/GaIe3tZ394a15ne9dMFB/dH4kqgTPFaxd8yl3fdtFQo8R2oVoiRKUN4NYxn7i4MbD0zEZ9RJFf1/7mLrtECjN4K5e/8iX5yVsJ+XYONsz3qb0Pr1ObHHJuPNAGlMYKefRup+I4zC2vvyJ2SSJOMqcFrRXhwKyOz0FKixtLIjKMj+25/7FqCYqPkw6KNWgw/+TKXKvOiEeKyOLr4UwF6mgtHwoKg=~3552313~3422516',
            'bs_rnd': 'O100157O',
            'bm_mi': '2895AFD3AE1767B0BDF44C7834200A47~YAAQD3s1F3jpzjuIAQAAy13DRBMagNVjZ87b0u3bKf5Ubki+1uKExYqZQ6CTFLpYzAcPc3Mk4Lpf2CpeUi+ODWpem9JxDV7MD0pktUxxW6M4DhxOFOAsIylv9UI/wl1FR+GwWy7REVYMYdgaD67z5jWjxmpjTJweKrav5cVLehlEQ/KetXpZZuxmeGSL4PwMTmmP7vR9LKupOGQhwcU1mChhCYBdYM9JFqdBOnwky90al2WxqrFyFzQ4ufdpRMQxBtarrTQbylKvRRPHngxKMbvbVIpmLo5kaYUuG3SZaoekZhUip9fr6h3+Reb4OWL1PO0i0yp0zluWzJQ=~1',
            '1377ae61ea78a27436703be2d8e9c7781s7': 'v0%7CAi5kxoPuVcPyJYbWni5BmI8%2BbV6ghrqnJgCMJcrRryz%2BnokQtbXRwt07DYwDV%2F2Tnk0N%2FK%2BVpFGSrByhZu7KzsY6J7ZCqc4KGewjc9sGw47fprCNnhjDnTgo4UlPXP%2B%2FVF0b451e1Uo4%2F%2FmT%2FNyKz9n6ZfTlDIWJ7azVS2kK3yQ%3D',
            'LPSID-77159344': 'Imssqi6OSuCXXwQA1oaAhw',
            'ak_bmsc': 'EC2149A05952F24455645FF273A23369~000000000000000000000000000000~YAAQD3s1F0X0zjuIAQAAR7vDRBP3RmgE2qeMx87iaDvZyrdLMzKRw5WwyuTGEmqxZtquraRig51VRJrvAxxtdLjObdCqtGEj2WPhGlk8ubolKUB5xnjzQtQ5vEbLbKQFLqT07M330Kw4/ENBWqOzlAIoIt7TzfptShDoBCwyqlYjBBWRmqgQcnBMrXMDS5NwQLD/N2vVScoPgDsM4/9K1F55ydr7ylqIDUXaBhioHrduXi+iyndtZo2F5+TCW1vViEXTSRw8cLd+0TYJXWYPeC4X5vjJJw3sr+iI2INUrz2TX0fhItglb5UbqdAXLGrqknSZq0yD8tZRTsqMVw1hIO3N+JkeOUiOLUp/Fly4fe/FUksxiXfZuBui4Jc1kuszCDA+LSwDijzZ2gO87alvuOorNW/UZ8k5Ch0j2DiM3+ojo1WqPhZq',
            'ACCESS': '1684780861',
            'UNID': 'XTEHGihEfT61qeLCXBVXpJJuO3FXJgc0EMaeFaXX',
            'pvId': '0',
            'isAddMobShown123739023': '1',
            'bm_sv': '3F65BDBA4092EFA9BBB8EA99E5F55FA4~YAAQD3s1Fyi/zzuIAQAAwevMRBM/F6PsGOICg621aBvQFiibrayPgu6Bzq2fcqrMAN4WivZXptXlZOzEy8orVigt2tx6aN/EM1nWcLlEylud3LFU/vqJ8EL1aphLLWhLy8VuSN1wIsARX4lXNZhMB+yul3/S+Oy/5XELK880t9J8NbwiO55OyS05WNAj4VafGnb9lIK4V6wKq+DQqubzfA9NqerUIfLnhnV1Nwicimo+sB+IAF/d2iclPSehbZlnxg==~1',
            'HOWTORT': 'cl=1684781367255&r=https%3A%2F%2Fresdex.naukri.com%2Fv3%2Fsearch%3FagentId%3D57537901%26activeIn%3D39%26resPerPage%3D40%26pageNo%3D1%26oneDaySearch%3Dfalse%26sid%3D6043908322%26sidGroupId%3D59bbdd9f7ed78f098feb0a24d5876673&nu=https%3A%2F%2Fresdex.naukri.com%2Fsearch%2FmodifySearchAgent%3FSRCHTYPE%3Dadv%26agentid%3D57537901%26modify_savedsearch%3Dfalse&ul=1684781486817&hd=1684781390378',
        }

        headers = {
            'authority': 'resdex.naukri.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': '_t_ds=689ecdf1684756884-132689ecdf-0689ecdf; test=naukri.com; persona=default; _ga=GA1.2.537000230.1684756924; _gid=GA1.2.466448074.1684756924; _gcl_au=1.1.119297570.1684756924; _fbp=fb.1.1684756933145.460959847; _ga_K2YBNZVRLL=GS1.1.1684756923.1.1.1684757158.0.0.0; _did=cd600830be; _odur=edaf7e3744; page_visit=1; dfp=27cb18f51c3d72c2b82645d0488e002d; LPVID=YwNzViM2MxM2Y3YzU0OGNh; kycEligibleCookie1360722=0; UNPC=1360722; UNCC=123739023; showDomainLB123739023=1; showPhotoUploadPage123739023=isSet; _abck=B1D7AED7848850B22DD68954693A1BA2~0~YAAQD3s1F5DozjuIAQAAL1nDRAnyuSe4yLorJLnCPI1p/N8rsBrRr/Rq+XRns4dnAaQqVJfp4YLghsGKCPyltZ0awOe6sAP6s147vBcdOaalg9mOy54uoM7tRtOsHU+82HG7wdNzl5UzfOJoNrK3NZMmHjU5UnDudCYaHpt2m+uvUX6Cdgnu5AyRGNXluO6jtXFtrZ9rSgmjy7ow8WffJQSs4UNQDYPThPg69GvuIE+m2aCLgx+h7COELO1wwQYHM4g8v8SxpVZlV/2roPW7/ancXZoRdwEmJh/DZ/LTP5jmZrBSzaIRVkAsPXZ67E9pCm/M98NQ0m5BVXKlUoIISNuMuitwd1RvN0FrjEXEHk3DmvqKnkY001VsnCh9rLwhw6WLs5EW4U9NWSngZLTdZVhaHL884kYM~-1~-1~-1; bm_sz=9DB8C447CAFD715DAD520EADC760172D~YAAQD3s1F5LozjuIAQAAL1nDRBNTEad4FhaVlmj4JA1mQo87xZBdtMS7c4juDcmqr6OBRtLitOiRZmdP7KB/GaIe3tZ394a15ne9dMFB/dH4kqgTPFaxd8yl3fdtFQo8R2oVoiRKUN4NYxn7i4MbD0zEZ9RJFf1/7mLrtECjN4K5e/8iX5yVsJ+XYONsz3qb0Pr1ObHHJuPNAGlMYKefRup+I4zC2vvyJ2SSJOMqcFrRXhwKyOz0FKixtLIjKMj+25/7FqCYqPkw6KNWgw/+TKXKvOiEeKyOLr4UwF6mgtHwoKg=~3552313~3422516; bs_rnd=O100157O; bm_mi=2895AFD3AE1767B0BDF44C7834200A47~YAAQD3s1F3jpzjuIAQAAy13DRBMagNVjZ87b0u3bKf5Ubki+1uKExYqZQ6CTFLpYzAcPc3Mk4Lpf2CpeUi+ODWpem9JxDV7MD0pktUxxW6M4DhxOFOAsIylv9UI/wl1FR+GwWy7REVYMYdgaD67z5jWjxmpjTJweKrav5cVLehlEQ/KetXpZZuxmeGSL4PwMTmmP7vR9LKupOGQhwcU1mChhCYBdYM9JFqdBOnwky90al2WxqrFyFzQ4ufdpRMQxBtarrTQbylKvRRPHngxKMbvbVIpmLo5kaYUuG3SZaoekZhUip9fr6h3+Reb4OWL1PO0i0yp0zluWzJQ=~1; 1377ae61ea78a27436703be2d8e9c7781s7=v0%7CAi5kxoPuVcPyJYbWni5BmI8%2BbV6ghrqnJgCMJcrRryz%2BnokQtbXRwt07DYwDV%2F2Tnk0N%2FK%2BVpFGSrByhZu7KzsY6J7ZCqc4KGewjc9sGw47fprCNnhjDnTgo4UlPXP%2B%2FVF0b451e1Uo4%2F%2FmT%2FNyKz9n6ZfTlDIWJ7azVS2kK3yQ%3D; LPSID-77159344=Imssqi6OSuCXXwQA1oaAhw; ak_bmsc=EC2149A05952F24455645FF273A23369~000000000000000000000000000000~YAAQD3s1F0X0zjuIAQAAR7vDRBP3RmgE2qeMx87iaDvZyrdLMzKRw5WwyuTGEmqxZtquraRig51VRJrvAxxtdLjObdCqtGEj2WPhGlk8ubolKUB5xnjzQtQ5vEbLbKQFLqT07M330Kw4/ENBWqOzlAIoIt7TzfptShDoBCwyqlYjBBWRmqgQcnBMrXMDS5NwQLD/N2vVScoPgDsM4/9K1F55ydr7ylqIDUXaBhioHrduXi+iyndtZo2F5+TCW1vViEXTSRw8cLd+0TYJXWYPeC4X5vjJJw3sr+iI2INUrz2TX0fhItglb5UbqdAXLGrqknSZq0yD8tZRTsqMVw1hIO3N+JkeOUiOLUp/Fly4fe/FUksxiXfZuBui4Jc1kuszCDA+LSwDijzZ2gO87alvuOorNW/UZ8k5Ch0j2DiM3+ojo1WqPhZq; ACCESS=1684780861; UNID=XTEHGihEfT61qeLCXBVXpJJuO3FXJgc0EMaeFaXX; pvId=0; isAddMobShown123739023=1; bm_sv=3F65BDBA4092EFA9BBB8EA99E5F55FA4~YAAQD3s1Fyi/zzuIAQAAwevMRBM/F6PsGOICg621aBvQFiibrayPgu6Bzq2fcqrMAN4WivZXptXlZOzEy8orVigt2tx6aN/EM1nWcLlEylud3LFU/vqJ8EL1aphLLWhLy8VuSN1wIsARX4lXNZhMB+yul3/S+Oy/5XELK880t9J8NbwiO55OyS05WNAj4VafGnb9lIK4V6wKq+DQqubzfA9NqerUIfLnhnV1Nwicimo+sB+IAF/d2iclPSehbZlnxg==~1; HOWTORT=cl=1684781367255&r=https%3A%2F%2Fresdex.naukri.com%2Fv3%2Fsearch%3FagentId%3D57537901%26activeIn%3D39%26resPerPage%3D40%26pageNo%3D1%26oneDaySearch%3Dfalse%26sid%3D6043908322%26sidGroupId%3D59bbdd9f7ed78f098feb0a24d5876673&nu=https%3A%2F%2Fresdex.naukri.com%2Fsearch%2FmodifySearchAgent%3FSRCHTYPE%3Dadv%26agentid%3D57537901%26modify_savedsearch%3Dfalse&ul=1684781486817&hd=1684781390378',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }

        params = {
            'agentId': '57537901',
            'activeIn': '39',
            'resPerPage': '40',
            'pageNo': '1',
            'oneDaySearch': 'false',
            'sid': '6043908322',
            'sidGroupId': '59bbdd9f7ed78f098feb0a24d5876673',
        }
        yield scrapy.Request(self.start_urls[0],callback = self.pagination,cookies=cookies,headers=headers,dont_filter=True)
    def pagination(self,response):
        for i in range(1,17):    
            url = "https://resdex.naukri.com/cloudgateway-resdex/recruiter-js-profile-listing-services/v0/search/results/pageChange"
            import requests
            payload = json.dumps({
            "pageNo": i,
            "miscellaneousInfo": {
                "companyId": 1360722,
                "rdxUserId": "123739023",
                "rdxUserName": "deepak.kinra@tredence.com",
                "sid": 6043908322,
                "sidGroupId": "59bbdd9f7ed78f098feb0a24d5876673",
                "flowId": "59bbdd9f7ed78f098feb0a24d5876673",
                "flowName": "search",
                "fetchClusters": False,
                "fetchResumeTuples": True,
                "s2jEnabled": False
            }
            })
            headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Appid': '112',
            'Content-Type': 'application/json',
            'Cookie': '_t_ds=689ecdf1684756884-132689ecdf-0689ecdf; test=naukri.com; persona=default; _ga=GA1.2.537000230.1684756924; _gid=GA1.2.466448074.1684756924; _gcl_au=1.1.119297570.1684756924; _fbp=fb.1.1684756933145.460959847; _ga_K2YBNZVRLL=GS1.1.1684756923.1.1.1684757158.0.0.0; _did=cd600830be; _odur=edaf7e3744; page_visit=1; dfp=27cb18f51c3d72c2b82645d0488e002d; LPVID=YwNzViM2MxM2Y3YzU0OGNh; kycEligibleCookie1360722=0; UNPC=1360722; UNCC=123739023; showDomainLB123739023=1; showPhotoUploadPage123739023=isSet; _abck=B1D7AED7848850B22DD68954693A1BA2~0~YAAQD3s1F5DozjuIAQAAL1nDRAnyuSe4yLorJLnCPI1p/N8rsBrRr/Rq+XRns4dnAaQqVJfp4YLghsGKCPyltZ0awOe6sAP6s147vBcdOaalg9mOy54uoM7tRtOsHU+82HG7wdNzl5UzfOJoNrK3NZMmHjU5UnDudCYaHpt2m+uvUX6Cdgnu5AyRGNXluO6jtXFtrZ9rSgmjy7ow8WffJQSs4UNQDYPThPg69GvuIE+m2aCLgx+h7COELO1wwQYHM4g8v8SxpVZlV/2roPW7/ancXZoRdwEmJh/DZ/LTP5jmZrBSzaIRVkAsPXZ67E9pCm/M98NQ0m5BVXKlUoIISNuMuitwd1RvN0FrjEXEHk3DmvqKnkY001VsnCh9rLwhw6WLs5EW4U9NWSngZLTdZVhaHL884kYM~-1~-1~-1; bm_sz=9DB8C447CAFD715DAD520EADC760172D~YAAQD3s1F5LozjuIAQAAL1nDRBNTEad4FhaVlmj4JA1mQo87xZBdtMS7c4juDcmqr6OBRtLitOiRZmdP7KB/GaIe3tZ394a15ne9dMFB/dH4kqgTPFaxd8yl3fdtFQo8R2oVoiRKUN4NYxn7i4MbD0zEZ9RJFf1/7mLrtECjN4K5e/8iX5yVsJ+XYONsz3qb0Pr1ObHHJuPNAGlMYKefRup+I4zC2vvyJ2SSJOMqcFrRXhwKyOz0FKixtLIjKMj+25/7FqCYqPkw6KNWgw/+TKXKvOiEeKyOLr4UwF6mgtHwoKg=~3552313~3422516; bs_rnd=O100157O; bm_mi=2895AFD3AE1767B0BDF44C7834200A47~YAAQD3s1F3jpzjuIAQAAy13DRBMagNVjZ87b0u3bKf5Ubki+1uKExYqZQ6CTFLpYzAcPc3Mk4Lpf2CpeUi+ODWpem9JxDV7MD0pktUxxW6M4DhxOFOAsIylv9UI/wl1FR+GwWy7REVYMYdgaD67z5jWjxmpjTJweKrav5cVLehlEQ/KetXpZZuxmeGSL4PwMTmmP7vR9LKupOGQhwcU1mChhCYBdYM9JFqdBOnwky90al2WxqrFyFzQ4ufdpRMQxBtarrTQbylKvRRPHngxKMbvbVIpmLo5kaYUuG3SZaoekZhUip9fr6h3+Reb4OWL1PO0i0yp0zluWzJQ=~1; 1377ae61ea78a27436703be2d8e9c7781s7=v0%7CAi5kxoPuVcPyJYbWni5BmI8%2BbV6ghrqnJgCMJcrRryz%2BnokQtbXRwt07DYwDV%2F2Tnk0N%2FK%2BVpFGSrByhZu7KzsY6J7ZCqc4KGewjc9sGw47fprCNnhjDnTgo4UlPXP%2B%2FVF0b451e1Uo4%2F%2FmT%2FNyKz9n6ZfTlDIWJ7azVS2kK3yQ%3D; LPSID-77159344=Imssqi6OSuCXXwQA1oaAhw; ak_bmsc=EC2149A05952F24455645FF273A23369~000000000000000000000000000000~YAAQD3s1F0X0zjuIAQAAR7vDRBP3RmgE2qeMx87iaDvZyrdLMzKRw5WwyuTGEmqxZtquraRig51VRJrvAxxtdLjObdCqtGEj2WPhGlk8ubolKUB5xnjzQtQ5vEbLbKQFLqT07M330Kw4/ENBWqOzlAIoIt7TzfptShDoBCwyqlYjBBWRmqgQcnBMrXMDS5NwQLD/N2vVScoPgDsM4/9K1F55ydr7ylqIDUXaBhioHrduXi+iyndtZo2F5+TCW1vViEXTSRw8cLd+0TYJXWYPeC4X5vjJJw3sr+iI2INUrz2TX0fhItglb5UbqdAXLGrqknSZq0yD8tZRTsqMVw1hIO3N+JkeOUiOLUp/Fly4fe/FUksxiXfZuBui4Jc1kuszCDA+LSwDijzZ2gO87alvuOorNW/UZ8k5Ch0j2DiM3+ojo1WqPhZq; ACCESS=1684780861; UNID=XTEHGihEfT61qeLCXBVXpJJuO3FXJgc0EMaeFaXX; pvId=0; isAddMobShown123739023=1; bm_sv=3F65BDBA4092EFA9BBB8EA99E5F55FA4~YAAQD3s1F97KzzuIAQAAGVjNRBMBozw3fDauSwTGDllj0SwlMaRBOP0u9Jc52G3TKwPWcVcJfCG/6V5zUsw+v/XgKlpXUdsrw9JjqNlfG9VCp5xL6gn1YlfFXPjurVqEWOodOKAKkCe585MBYKRnubl1Ahy63KhIAxMWvJKrnlSQONGwBGptYhhrpwA7EOo+DHDdJMT1LZw3s/mY01rcCxCJy3HYojdQJ0YbvphBQufdi/SUJvidQMacZkZ1Ua0RuQ==~1; HOWTORT=cl=1684781367255&r=https%3A%2F%2Fresdex.naukri.com%2Fv3%2Fsearch%3FagentId%3D57537901%26activeIn%3D39%26resPerPage%3D40%26pageNo%3D1%26oneDaySearch%3Dfalse%26sid%3D6043908322%26sidGroupId%3D59bbdd9f7ed78f098feb0a24d5876673&nu=https%3A%2F%2Fresdex.naukri.com%2Fsearch%2FmodifySearchAgent%3FSRCHTYPE%3Dadv%26agentid%3D57537901%26modify_savedsearch%3Dfalse&ul=1684781486817&hd=1684781488328; _abck=B1D7AED7848850B22DD68954693A1BA2~-1~YAAQE3s1Fw8HPDWIAQAAw+bkRAlXjiqvOFP1t2HLzD4e77n0L15yEiT+Z9qqxWr2ak+1jNs6n2Jcqz4lg79VFRlam9uLhireGg2JSdu6Eakv7PK+PsLMKd6YEv2KECxoFALDaojwGabGxniJVd4jnqQoXyTRDr5PhTlWKPJnXeWKg1r0URf1PWQ/zHFCT1EQJmENjlpDUBRTXvVakH/uw+uWCLeqp0f3iOFiwqfviahqUmrvhRmChgDe7hcXaaxgZJsKCKUd/9uHSYjy5EedKsCTHzTHqWbAOCtQnyrvAT4xAoSOLRpU6Go1nScKhI9dG4fHKfB6tzUb78q6PIJwhahQ9l/iinS3nRjK18YndEoeyQ+dGyxMUAdN9wfkffGtZXQFDEsRAh09Gzp3u/kCUXOZSbPUwJpK~0~-1~-1; _did=6ee0f791df; _odur=d44228b9e0; _t_ds=1c81f5c71684758906-01c81f5c7-01c81f5c7; bm_sv=3F65BDBA4092EFA9BBB8EA99E5F55FA4~YAAQE3s1FxAHPDWIAQAAw+bkRBPVCYimAp5g09F+Rs9THqIwZzy0556bGP9W5M0tsfyKBdDFM/7Uz84b55+U+LSzE0NXThmUvWt3of5DJVUNN8nnda0j4aEkjEWyFpFssfaRM0EnqoLhoKFidM7IGekM3A7B/2JmrPpW+zRweZSoWJTsWWE86qAWvFGdwutuy22RwvGoq2OGk4cAQdXNd/6L8Wlb9+XFP2KIkTjyiXNjLMlW+TcyzEzcq9RsLATYRg==~1; bs_rnd=Z347d5cZ',
            'Origin': 'https://resdex.naukri.com',
            'Referer': 'https://resdex.naukri.com/v3/search?agentId=57537901&activeIn=39&resPerPage=40&pageNo=1&oneDaySearch=false&sid=6043908322&sidGroupId=59bbdd9f7ed78f098feb0a24d5876673',
            'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24":',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Systemid': 'naukriIndia',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-Transaction-Id': 'srp326362479157311609310781488426~~544ceb'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            jo = json.loads(response.text)          

            for dic in jo['tuples']:
                name = dic['jsUserName']
                title = '{} at {}'.format(dic['employment']['current']['designation'],dic['employment']['current']['organization'])
                experience = '{}y {}m'.format(dic['experience']['years'],dic['experience']['months'])
                salary = '{}.{}'.format(dic['ctcInfo']['lacs'],dic['ctcInfo']['thousands'])
                if '+' in salary:
                    salary = salary.split('.')[0]
                location = dic['currentLocation']
                views = dic['numberOfViews']
                downloads = dic['numberOfDownloads']
                activedate = (datetime.utcfromtimestamp(dic['activeDateMillis']/1000).astimezone(pytz.timezone('Asia/Kolkata'))).strftime('%m/%d/%Y')
                modifieddate = (datetime.utcfromtimestamp(dic['modifyDateMillis']/1000).astimezone(pytz.timezone('Asia/Kolkata'))).strftime('%m/%d/%Y')

                items = NaukriItem()
                items["Name"] = name
                items["Experience"] = experience
                items["Salary"] = salary
                items["City"] = location
                items["Title"] = title
                items["Views"] = views
                items["Downloads"] = downloads
                items["ModifiedOn"] = modifieddate
                items["Active"] = activedate
                yield items

