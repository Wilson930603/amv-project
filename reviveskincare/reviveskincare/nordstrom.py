import json
from time import sleep
from random import randint
import os
import pandas as pd
import requests
#Save to file
def saveCsv_second(User,Rating,Date,Title, Review,HelpFul,file_name):
    items = {'User':[],'Rating':[],'Date':[],'Title':[],'Review':[], 'HelpFul':[]}
    items['User'].append(User)
    items['Rating'].append(Rating)
    items['Date'].append(Date)
    items['Title'].append(Title)
    items['Review'].append(Review)
    items['HelpFul'].append(HelpFul)
    
    if not os.path.exists(file_name):
        pd.DataFrame(items).to_csv(file_name,index=False)
    else:
        pd.DataFrame(items).to_csv(file_name,index=False,header=False,mode='a')

URL = "https://www.nordstrom.com/s/moisturizing-renewal-cream-nightly-retexturizer/3081652?origin=category-personalizedsort&breadcrumb=Home%2FBeauty%2FSkin%20Care&color=000"
PRODUCT_ID = URL.split('?')[0].split('/')[-1]
cookies = {
    'FPLC': 'SIntIFAsLuFLKHWRg5FG%2BKjKc82Z3Il2A2sluaGsCc2RrkxYtc0VagZWLu00s1d5NWsyIzn%2BXhLpRfHKyINnrhh%2FJX8RlVlsxg1bl48ACqXKl6sxCCj%2FR9F7csX70Q%3D%3D',
    'FPID': 'FPID2.2.AyW6%2BAv8j5AiXnnraZ637GW7yck6nlyxBSkpLX6E4Pc%3D.1689901743',
    'audience': 'audiences=',
    'internationalshippref': 'preferredcountry=PK&preferredcurrency=PKR&preferredcountryname=Pakistan',
    'no-track': 'ccpa=false',
    'nordstrom': 'bagcount=0&firstname=&ispinned=False&isSocial=False&shopperattr=||0|False|-1&shopperid=8e25540ae2f8479e9cfd6378e949a246&USERNAME=',
    'nui': 'firstVisit=2023-07-21T02%3A48%3A11.628Z&geoLocation=&isModified=false&lme=false',
    'usersession': 'CookieDomain=nordstrom.com&SessionId=e1029ed1-1a0b-49c9-a689-4b48bf839e6a',
    'experiments': 'ExperimentId=8f817e0c-9ac0-4c13-bb3b-c40e08dbf2a6',
    'Bd34bsY56': 'AwEAWXaJAQAARVUgHhCgvQFB_vpk4sQ5_NeYLNp1hzxMISMZRaBCP33_EjgYATtneJqucirJwH8AAEB3AAAAAA==',
    'Ad34bsY56': 'A6j8WHaJAQAAMvT-C7ZHmvIwsq3gRdLjuNfun7AuhloRkMH5t8sg5RddnnQ7ATtneJqucirJwH8AAEB3AAAAAA|1|1|20dc0d51a5ff73bd098941d8ab6d88e88c192cc4',
    'wlcme': 'true',
    '_gcl_au': '1.1.100505614.1689907692',
    'n.com_shopperId': '8e25540ae2f8479e9cfd6378e949a246',
    '_gid': 'GA1.2.884775700.1689907693',
    'trx': '4783350576129312907',
    '_scid': '54eda7e2-1b1d-450b-899e-2d242d3dd470',
    '_tt_enable_cookie': '1',
    '_ttp': 'Fxt8O9dnbQyiE3lCTTZoSnilqk9',
    'storemode': 'version=4&postalCode=&selectedStoreIds=&storesById=&localMarketId=&localMarketsById=',
    'session': 'FILTERSTATE=&RESULTBACK=&RETURNURL=http%3A%2F%2Fshop.nordstrom.com&SEARCHRETURNURL=http%3A%2F%2Fshop.nordstrom.com&FLSEmployeeNumber=&FLSRegisterNumber=&FLSStoreNumber=&FLSPOSType=&gctoken=&CookieDomain=&IsStoreModeActive=0&',
    '_sctr': '1%7C1689879600000',
    'mdLogger': 'false',
    'kampyle_userid': 'e957-d34d-5b08-2875-7b8c-f201-6f4b-07ae',
    'bluecoreNV': 'false',
    '_pin_unauth': 'dWlkPU9ETm1PRFV3TmpNdE1EQmpZaTAwTWpaaUxXSTVObUl0TlRZMFpUTTVZelExT1dJeg',
    'bc_invalidateUrlCache_targeting': '1689911848491',
    'storeprefs': '|100|||2023-07-21T03:58:42.871Z',
    '_imp_apg_r_': '%7B%22c%22%3A%22SjM5dXBjMG4wd2ZwWm5YRg%3D%3D7JqnigIVqbagtcUK3Uv0vliezPz_ogd5sSwZIbVcejbVQc90W_J6neFur_aFdcVlKVX8X2alqsaSqTIIamQ_H9vEk85XgbFG-HyDFhdE40j6bN331Q%3D%3D%22%2C%22dc%22%3A0%2C%22mf%22%3A0%7D',
    '_scid_r': '54eda7e2-1b1d-450b-899e-2d242d3dd470',
    '_ga_XWLT9WQ1YB': 'GS1.1.1689901744.1.1.1689911924.50.0.0',
    'mp_nordstrom_com_mixpanel': '%7B%22distinct_id%22%3A%20%2218976590527305-0ec8813d3c7768-26031c51-144000-189765905288ef%22%2C%22bc_persist_updated%22%3A%201689907692842%7D',
    '_ga_11111111': 'GS1.1.1689901744.1.1.1689911924.0.0.0',
    '_uetsid': '08e8e7c0277111ee9b07f9c04570f711',
    '_uetvid': '08e934a0277111ee8da379a5cf913833',
    '_ga': 'GA1.2.711252923.1689907693',
    'Tld-kampyleUserSession': '1689911928194',
    'Tld-kampyleUserSessionsCount': '15',
    'Tld-kampyleSessionPageCounter': '1',
    'Tld-kampyleUserPercentile': '17.211904111360354',
    'forterToken': '09ca24c14bb74d74af2ac58b8867df58_1689911922504__UDF43-m4_17ck',
    'rfx-forex-rate': 'currencyCode=PKR&exchangeRate=309.98&quoteId=84453432',
    'shoppertoken': 'shopperToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTI1NTQwYWUyZjg0NzllOWNmZDYzNzhlOTQ5YTI0NiIsImF1ZCI6Imd1ZXN0IiwiaXNzIjoibm9yZHN0cm9tLWd1ZXN0LWF1dGgiLCJleHAiOjIwMDU1MzEyMDksInJlZnJlc2giOjE2ODk5MjY0MDksImp0aSI6ImFhYTc3NjlhLWFkNTEtNDBkZC04YTM1LThhOWNhNmNmMWUwZSIsImlhdCI6MTY4OTkxMjAwOX0.IIGrGQyCzWnHAxhrqrej48Is9ZM3W5UZlvqv7VBrDXMGIp8p5nRJb27SCzeP987vy4yCvNybSr_kZK029OTKb_MdYfmoIgRyrvNVuJzEHdvfqNK984cAZm3I7H7dPJq9Q3q3eGEcZNlh_eJbVYJUumoAbuJJrql-ICgHof1GaafK3sYR9q_JynbdwybSZe9mw26YEpcsbIC3BW9zs4aeVDaalsTihHDfgWrMwro-v8uVvpyH98e-_UH_sXbORJNPD3FRHDcMuLrazA0ZBJ4M8ALohy8qAATOk8GBTmmvpwx8TWGwvQWOm8AQUWj_tqJDMRHRXtjoENeJz3JwLXLet86hDD4pFqOuM6o-2264RYWPZ91Nhlx2zjN9Fw0jMqtblQAczDOeQlf1m8ltjII1mlrC3S3lo6U_bOXr-0wcrufePPJd4wWu-zOdGdJN4gPPQ18nh_yh6qE0HPKv2jSvgHMn5lOOcnEbPKXsKrJSx8tzBLDFCXq1soNsFjt4a84ZHmWVZgpcjT5n9Y5QNYaMn73YjvX7xOKI8OADDq_xeLLOgRcFIA5AsdeHEOwP6-BmqYXHiEwXJAstXW1TMayUTGbBEfNBrtQgNTCsjsaA42wrfyG5Nnuas_up78S5l1iKdg64PAtQG5JS4_alHi76vCejD-9CH_U84WBMpYr6Zg0',
}

headers = {
    'authority': 'www.nordstrom.com',
    'accept': 'application/vnd.nord.review.default.v1+json',
    'accept-language': 'en-US',
    'clientplatform': 'undefined',
    'content-type': 'application/vnd.nord.review.default.v1+json',
    # 'cookie': 'FPLC=SIntIFAsLuFLKHWRg5FG%2BKjKc82Z3Il2A2sluaGsCc2RrkxYtc0VagZWLu00s1d5NWsyIzn%2BXhLpRfHKyINnrhh%2FJX8RlVlsxg1bl48ACqXKl6sxCCj%2FR9F7csX70Q%3D%3D; FPID=FPID2.2.AyW6%2BAv8j5AiXnnraZ637GW7yck6nlyxBSkpLX6E4Pc%3D.1689901743; audience=audiences=; internationalshippref=preferredcountry=PK&preferredcurrency=PKR&preferredcountryname=Pakistan; no-track=ccpa=false; nordstrom=bagcount=0&firstname=&ispinned=False&isSocial=False&shopperattr=||0|False|-1&shopperid=8e25540ae2f8479e9cfd6378e949a246&USERNAME=; nui=firstVisit=2023-07-21T02%3A48%3A11.628Z&geoLocation=&isModified=false&lme=false; usersession=CookieDomain=nordstrom.com&SessionId=e1029ed1-1a0b-49c9-a689-4b48bf839e6a; experiments=ExperimentId=8f817e0c-9ac0-4c13-bb3b-c40e08dbf2a6; Bd34bsY56=AwEAWXaJAQAARVUgHhCgvQFB_vpk4sQ5_NeYLNp1hzxMISMZRaBCP33_EjgYATtneJqucirJwH8AAEB3AAAAAA==; Ad34bsY56=A6j8WHaJAQAAMvT-C7ZHmvIwsq3gRdLjuNfun7AuhloRkMH5t8sg5RddnnQ7ATtneJqucirJwH8AAEB3AAAAAA|1|1|20dc0d51a5ff73bd098941d8ab6d88e88c192cc4; wlcme=true; _gcl_au=1.1.100505614.1689907692; n.com_shopperId=8e25540ae2f8479e9cfd6378e949a246; _gid=GA1.2.884775700.1689907693; trx=4783350576129312907; _scid=54eda7e2-1b1d-450b-899e-2d242d3dd470; _tt_enable_cookie=1; _ttp=Fxt8O9dnbQyiE3lCTTZoSnilqk9; storemode=version=4&postalCode=&selectedStoreIds=&storesById=&localMarketId=&localMarketsById=; session=FILTERSTATE=&RESULTBACK=&RETURNURL=http%3A%2F%2Fshop.nordstrom.com&SEARCHRETURNURL=http%3A%2F%2Fshop.nordstrom.com&FLSEmployeeNumber=&FLSRegisterNumber=&FLSStoreNumber=&FLSPOSType=&gctoken=&CookieDomain=&IsStoreModeActive=0&; _sctr=1%7C1689879600000; mdLogger=false; kampyle_userid=e957-d34d-5b08-2875-7b8c-f201-6f4b-07ae; bluecoreNV=false; _pin_unauth=dWlkPU9ETm1PRFV3TmpNdE1EQmpZaTAwTWpaaUxXSTVObUl0TlRZMFpUTTVZelExT1dJeg; bc_invalidateUrlCache_targeting=1689911848491; storeprefs=|100|||2023-07-21T03:58:42.871Z; _imp_apg_r_=%7B%22c%22%3A%22SjM5dXBjMG4wd2ZwWm5YRg%3D%3D7JqnigIVqbagtcUK3Uv0vliezPz_ogd5sSwZIbVcejbVQc90W_J6neFur_aFdcVlKVX8X2alqsaSqTIIamQ_H9vEk85XgbFG-HyDFhdE40j6bN331Q%3D%3D%22%2C%22dc%22%3A0%2C%22mf%22%3A0%7D; _scid_r=54eda7e2-1b1d-450b-899e-2d242d3dd470; _ga_XWLT9WQ1YB=GS1.1.1689901744.1.1.1689911924.50.0.0; mp_nordstrom_com_mixpanel=%7B%22distinct_id%22%3A%20%2218976590527305-0ec8813d3c7768-26031c51-144000-189765905288ef%22%2C%22bc_persist_updated%22%3A%201689907692842%7D; _ga_11111111=GS1.1.1689901744.1.1.1689911924.0.0.0; _uetsid=08e8e7c0277111ee9b07f9c04570f711; _uetvid=08e934a0277111ee8da379a5cf913833; _ga=GA1.2.711252923.1689907693; Tld-kampyleUserSession=1689911928194; Tld-kampyleUserSessionsCount=15; Tld-kampyleSessionPageCounter=1; Tld-kampyleUserPercentile=17.211904111360354; forterToken=09ca24c14bb74d74af2ac58b8867df58_1689911922504__UDF43-m4_17ck; rfx-forex-rate=currencyCode=PKR&exchangeRate=309.98&quoteId=84453432; shoppertoken=shopperToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTI1NTQwYWUyZjg0NzllOWNmZDYzNzhlOTQ5YTI0NiIsImF1ZCI6Imd1ZXN0IiwiaXNzIjoibm9yZHN0cm9tLWd1ZXN0LWF1dGgiLCJleHAiOjIwMDU1MzEyMDksInJlZnJlc2giOjE2ODk5MjY0MDksImp0aSI6ImFhYTc3NjlhLWFkNTEtNDBkZC04YTM1LThhOWNhNmNmMWUwZSIsImlhdCI6MTY4OTkxMjAwOX0.IIGrGQyCzWnHAxhrqrej48Is9ZM3W5UZlvqv7VBrDXMGIp8p5nRJb27SCzeP987vy4yCvNybSr_kZK029OTKb_MdYfmoIgRyrvNVuJzEHdvfqNK984cAZm3I7H7dPJq9Q3q3eGEcZNlh_eJbVYJUumoAbuJJrql-ICgHof1GaafK3sYR9q_JynbdwybSZe9mw26YEpcsbIC3BW9zs4aeVDaalsTihHDfgWrMwro-v8uVvpyH98e-_UH_sXbORJNPD3FRHDcMuLrazA0ZBJ4M8ALohy8qAATOk8GBTmmvpwx8TWGwvQWOm8AQUWj_tqJDMRHRXtjoENeJz3JwLXLet86hDD4pFqOuM6o-2264RYWPZ91Nhlx2zjN9Fw0jMqtblQAczDOeQlf1m8ltjII1mlrC3S3lo6U_bOXr-0wcrufePPJd4wWu-zOdGdJN4gPPQ18nh_yh6qE0HPKv2jSvgHMn5lOOcnEbPKXsKrJSx8tzBLDFCXq1soNsFjt4a84ZHmWVZgpcjT5n9Y5QNYaMn73YjvX7xOKI8OADDq_xeLLOgRcFIA5AsdeHEOwP6-BmqYXHiEwXJAstXW1TMayUTGbBEfNBrtQgNTCsjsaA42wrfyG5Nnuas_up78S5l1iKdg64PAtQG5JS4_alHi76vCejD-9CH_U84WBMpYr6Zg0',
    'experiments': '{"experiments":[],"optimizely":{"experiments":[{"n":"bannerpreferences_optoutpage","v":"treatment","p":"FULL_LINE_DESKTOP"},{"n":"checkout_ff_selection_in_bag","v":"ff_in_bag","p":"FULL_LINE_DESKTOP"},{"n":"sbn_expanded_seo_content_block","v":"Expanded","p":"FULL_LINE_DESKTOP"},{"n":"ids_test_experiment_v1","v":"variation_2","p":"FULL_LINE_DESKTOP"},{"n":"checkout_apple_pay","v":"apple_pay","p":"FULL_LINE_DESKTOP"},{"n":"sponsored_ads_sbn_nsk_rollout","v":"nsk","p":"FULL_LINE_DESKTOP"},{"n":"pdp_final_sale_in_buy_pack","v":"holdback","p":"FULL_LINE_DESKTOP"},{"n":"cam-recognized-user","v":"recognized-user","p":"FULL_LINE_DESKTOP"},{"n":"type_ramp_on_sbn","v":"SbnTypeRamp","p":"FULL_LINE_DESKTOP"},{"n":"cam-psi-sign-up","v":"enabled","p":"FULL_LINE_DESKTOP"},{"n":"checkout_shopping_bag_express_payments_paypal_and_payin4","v":"Default","p":"FULL_LINE_DESKTOP"},{"n":"nr_token_migration","v":"Default","p":"FULL_LINE_DESKTOP"},{"n":"global_ncom_email_footer","v":"email","p":"FULL_LINE_DESKTOP"},{"n":"fcx_dynamic_promise_desktop","v":"default","p":"FULL_LINE_DESKTOP"},{"n":"wl_anniversary_toggle","v":"variation_1","p":"FULL_LINE_DESKTOP"},{"n":"checkout_shopping_bag_express_payments_apple_pay","v":"Default","p":"FULL_LINE_DESKTOP"},{"n":"wl_anniversary_postaddtobagupdates","v":"variation_1","p":"FULL_LINE_DESKTOP"},{"n":"holiday_2021_egift_message_improve_info_-_n_com","v":"egift_ncom","p":"FULL_LINE_DESKTOP"},{"n":"pdp_beauty_highlights_poc","v":"default","p":"FULL_LINE_DESKTOP"},{"n":"pdp_beauty_virtual_tryon","v":"default","p":"FULL_LINE_DESKTOP"},{"n":"sbn_sort_designer_by_newest","v":"Default","p":"FULL_LINE_DESKTOP"},{"n":"pdp_ncom_green_atb_button_atwl","v":"atwlbutton","p":"FULL_LINE_DESKTOP"},{"n":"out_notitles_v1","v":"default","p":"FULL_LINE_DESKTOP"},{"n":"hp_perso_ctr_carousel","v":"CTR","p":"FULL_LINE_DESKTOP"},{"n":"unrecognized-cam-sign-in-message-checkout","v":"unrecognized-checkout-message","p":"FULL_LINE_DESKTOP"},{"n":"tiles_desktop","v":"tiles","p":"FULL_LINE_DESKTOP"},{"n":"reco_perso-hp_categories","v":"perso","p":"FULL_LINE_DESKTOP"},{"n":"checkout_shopping_bag_layout_shift","v":"bag_layout","p":"FULL_LINE_DESKTOP"},{"n":"auth_test_2","v":"variation_2","p":"FULL_LINE_DESKTOP"},{"n":"accountlandingrecognizeduser","v":"variation_2","p":"FULL_LINE_DESKTOP"},{"n":"perso_content_womens_denim","v":"Default","p":"FULL_LINE_DESKTOP"},{"n":"aaa-metric-uat","v":"Default-a","p":"FULL_LINE_DESKTOP"},{"n":"wish_list_add_filters_v1","v":"wl_filters","p":"FULL_LINE_DESKTOP"},{"n":"cam-recognized-user-checkout-wishlist-share","v":"default","p":"FULL_LINE_DESKTOP"},{"n":"gift_bags","v":"gift_bag","p":"FULL_LINE_DESKTOP"},{"n":"cam_recognized_user_sign_up_ncom_nca","v":"recognized_user_sign_up","p":"FULL_LINE_DESKTOP"},{"n":"left_nav_meta_data","v":"metadata","p":"FULL_LINE_DESKTOP"},{"n":"pdp_paypal_bnpl","v":"paypal","p":"FULL_LINE_DESKTOP"},{"n":"pdp_360_degree_videos_v3","v":"autoplaymain","p":"FULL_LINE_DESKTOP"},{"n":"legacy-credit-flow","v":"legacy","p":"FULL_LINE_DESKTOP"},{"n":"pdp_image_first","v":"default","p":"FULL_LINE_DESKTOP"},{"n":"wl_add_rec_tray_to_confirmation_modal","v":"variation_1","p":"FULL_LINE_DESKTOP"},{"n":"cam-sign-in-message-checkout","v":"checkout-message","p":"FULL_LINE_DESKTOP"},{"n":"urgency_messaging_order_of_display_with_pick_up","v":"variation_2","p":"FULL_LINE_DESKTOP"},{"n":"gv2f_test_experiment","v":"default","p":"FULL_LINE_DESKTOP"},{"n":"ocp_first_dual_write_enabled_prod","v":"ICON_ONLY","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"ph_display_today_for_estimated_arrival","v":"isToday","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"chx_qr_code_in_wallet_hp","v":"qrCodeEnabled","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"nav_filters_style","v":"TestStyleFilter","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"ocp_first_ab_first_dev","v":"ICON_FRIST","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"rec_tray_ab_test_tracking_page","v":"new_position","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"fomo_feeds","v":"variant1","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"ph_dr_fedex_carrier","v":"isFedex","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"nav_filters_occasion","v":"TestOccasionFilter","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"hp_dcapi_explore_more_tray","v":"exploreMoreTray","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"sbn_rec_swap","v":"switchOrder","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"ava","v":"rollout","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"nav_filters_applicationarea","v":"TestApplicationAreaFilter","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"ph_ss_npr_ab_test","v":"isnpr","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"ocp_first_ab_first_prod","v":"ICON_FRIST","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"phdr_ss_npr_abc_test","v":"reportOrderIssue","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"segmentation_test","v":"variation_1","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"hp_generic_seasonal_looks","v":"seasonalOn","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"cam_psi_ttl_ios","v":"extended","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"sbn_departmenttiles","v":"departmentTiles","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"ocp_first_dual_write_enabled_dev","v":"ICON_AND_OCP","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"cam_psi_ttl_ext","v":"default","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"phdr_returnmates_ab_test","v":"returnmates","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"nav_filters_material","v":"TestMaterialFilter","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"eccs_ocp_first","v":"rollout","p":"FULL_LINE_BACKEND_SERVICE"},{"n":"cam_kong_enabled","v":"rollout","p":"FULL_LINE_BACKEND_SERVICE"}],"id":"8f817e0c-9ac0-4c13-bb3b-c40e08dbf2a6"},"user_id":"8f817e0c-9ac0-4c13-bb3b-c40e08dbf2a6"}',
    'identified-bot': 'False',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjIzMDUxMjEiLCJhcCI6IjMwMjQ2MTM4NiIsImlkIjoiYzQzZjcxZmZiYWIxODJjMyIsInRyIjoiMWM1MDZjMzYxODRmYzkwMGExNTBjNDAzMGU2MDA0NDAiLCJ0aSI6MTY4OTkxMjAxMzgxOCwidGsiOiIyMjkxMTU0In19',
    'nord-channel-brand': 'NORDSTROM',
    'nord-country-code': 'US',
    'nord-customer-experience': 'DESKTOP_WEB',
    'nord-request-id': 'c2b82e22-6a9d-4c2a-9701-ae57c3b093a6',
    'referer': 'https://www.nordstrom.com/s/moisturizing-renewal-cream-nightly-retexturizer/3081652?origin=category-personalizedsort&breadcrumb=Home%2FBeauty%2FSkin%20Care&color=000',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'tracecontext': 'dcc03aa7-53a9-491e-9814-98417e9caaae',
    'traceparent': '00-1c506c36184fc900a150c4030e600440-c43f71ffbab182c3-01',
    'tracestate': '2291154@nr=0-1-2305121-302461386-c43f71ffbab182c3----1689912013818',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-y8s6k3db-a': 'eHSqk82=CU3sPrBLZwtVsXn=h9RjjnbKcS=Nsd-lKDjzAet2GK9hvVGty850AZs0bTrgtpwOwxHqa=371Rx2=y6ALKxLEIMBLoaFM9Sd=Cqcv2Kb33Rd7LtzZmtbGn3=wvNyeJ6DrWOSkHtMRmgONe69pnAtrsjq_SWSXCjNB1H4jviLTPmSDAhyiLVe70wr6F2vagqX_P6MpxpU8VgamgXFDskHGJdgAMwzgPchDwLezCZfwM-OqA4c50mp6f3tqKUXbwaRoZ9KiaAKDUOv51n684vDd2VF1Kqk-SeLknum5IxVfiBjpcOn19_plldZyrHch4Ia87i9lVh-OpZiroFeZvqNEU_XzB-d_=yTb50WPOWDVD8pfiSnFi93HPdkD8WYCOv8dIeucN2t_A6OcTn7LuR1pqVIntrXshgEGb6ymTwnSXTgFgn5TD20G4gzRM5f_g1BvL8unqV=DBl5KRtgNaPTqWqc6YL_r-f5kP4v9JVvFpBTN_L6jd6j0IfaM7a4oy8l2T0OqDb8pOR0u0h6LT74bMjMDClbH6r=bVFBghrl67UYSOqIhnc4uR=gl6x03St4i81nCEcCydzCRcpkLr4kljMsRn3=5qsgLOHqzbFoMyrJubFDKe1C5fSOmon-SKOc0Ou5gmexjD5eGxvf5BXfh58HqGwYzSq-Xe0CWREuLuOxkK2yuIen=Ol0Sr0StaKx8Rv4_dAFMz=w0xO=ZfOm_U9tFP6b-lnHeoPPjrmjYykcF_2vjHkhFVMdCD10-LiJV5-gXnhXo3iFXzE8uRXizWKdwnBzUFyK1aojm4fWSyMqn8YK5azl1hwXwvT4_D0sb_jAwW=5uoVg3dDOJNjkrvG1jcD95sT0Y9Dz2ckalhWFKsai7UL96SbxnaBhzA=uhFvxvxflbFHJj36NxCcMPMbB1zO1GdGucLDVx39LCcmpz2-TR=WqthG1uIEN-cfFxUlTjqZ=7vpHCp7nXtzXkaZfcExI2fRmaOA1gfcnI2hrdxKDDzkbEWgp28zSdP6cf-XABxgTkdAk1gnKTKT8uEZ0fZtht9Ycg8m7Z_V8Su8yS=01r7VgywVlpLturPte9jChOKe7zPMViH52igxgNsZsgGXbcfD85h5Rv21AZd00c0heBVuaoAFNBwkzWs-heI4eZG4CCv1Tbk7tk=-w_LxY9Ka3RXgWCpXzD4yEmd1iRHm-YK-0OSwdNyE08pHAZ3B14frnyWTYnAtS=4w_DAWhAmGwAq-R2Gi8DA3RehrYuDPez8gCFgd0iD3j3mV8NFV=h9f1pFwcom3uoLiZbsGaWIyg9yITRCMuAL437TZNAfcjVaYXdVZd44hOXvbGbJJkxOOkGJz2-v=X6m41SBmj00f4exY=fhBmieb1MpsB4SLE1EqIfCSP9bkG341Y5bAqlCcMYpnXe3tS5h9sdcNjPaDAVxNOVPLtmR5TkWlvM49tEyY2=0MYFfUBaaU460gBA8sGfed56NA0DDSZ8xCMXPtMF67ZafIcSuPINLO_XjxI_95XGeFIOUXAn=j2Phth7giqEyRG24xS=zmGfu4743pE5oPN3HF27M_RlAIC12Yv2k9bdpAp-=GXrqs4cdHemrNa=CkrF2j2W5NwLwuH2BeOWDfIyLtan0ojzDmTy44y8atzw4B2dXZ_yF4PAYqvrKaHRG8pSAGnGLzHlffh6lArJZuG8hXPjyI4KNpEIAl8nCVyzJnp4I9soo566Eynfo4BHN7aaFcy4S6seq0qtM2IcAvmIw_mbl2u-8jPi5SN8sDanci3e_JxwDMJjLeUBF5r93LhsErlejWrbytuhv35pc8UdREE2F6CO6r5cntt9TAJtPd6ffIN0aqj9H30lhI3GnllqAVW24MHlX-inAL4HBPeUN2PN777ww48T4XTACrnZ_nZKn--ifJOoOh9R_aNXxiw18f=c=5fNPzDP7UDZLdsVEL80UdNFEeS3Wnp1BffYAS6jOwEUGCHDRhr0BWhUzCaUB=Cq3epMBLs36ipJ_apOGzZAfC4xLaAGhjoGgT5dB3WaUodv4xfXKyStbekgPOCbPoTGrB3Ef=b4lL38xCPEOJsLRSpAR595kzZ0KFh-PX5h6dNCB=2=XidW8=TpbO_OTG4lr03hIvV99-OHvR2loKO6eh4o7Py4IvinnPFks6uoF0ULnjTVJfA=B0U3mAr8Sva0bnxitw2yIaP1mTEnvha8OlXwMwjmKjFBex0sEP8lr=iis9b_FlXh6miulE0jdFc8_W1tmgkYtBPgdlbuGcD96h_7gpT1zZPNMe-uyqJ2MF60L=LjSaxzOrsxaAvG=cBY0tRJGqgJ93Nzo4E0a5vhwoxJWxDtxiGiKmdRuAoXktP8W7CTM1_NEwNljPcvXj=7rP15B75eOaZg7qaB6=VqjSk38lWkCBtRulnOzNzWOozLBZ1JGu4jyhZDTBPnm_7ChGF1Fz=0fhDlZshZ6yBydEdiWPlxvnOb-cY3R3b9t3mNTvLWc_-91=ouggxc37OA5B=WDozoUUPlKw3UZb0enYDuXKfGM3aFmF9FoUM3lbSYEXurbBDREX4nJCPhnM6xmdoN_zBw1D9YXgTAmK9-8bm7TBd7BPRPnr9kjGIK0IE-eGMwSXAWs4nvButR6NhbZWl3nqZirPtdEAl9-gZktFJETB2Xo0R-ghHpm2YRdJhBPsPNW3Beo8n5hrZlmjOP6TnbzKI0MrZrkxruj6OMosBgJLLSgMgKf8cIGFuiWo8B0xLkNFO_pSSa_9_6goGbDMIPlLJv_bcpCcB4SdoyI40P-aWk3q5BzypDcTGnZASHx4yFya-mlpFNmGmhlKPfwwDzb8KMaFdcMW3SxVtntTJB3npCh7daPz-2nMt4fTBcqgM2UtrM3clj48=E4c97zhrVxIlaaXwLjBAO6=jjBttdCavEUfWy5pHt9Sr9-bdihYq2soSd66NBbHgRDZodmujAOzsxAfgCWuJVprcWUqzk9L_g44c2h811f-RGdJwhhIHLIwfqLSgqVebKx1IErs7GjEiH4=ROq3AEFNsjYMOz_dobvrxB4A8fG_mPpHunJ4R_5iH9w_Wznp4O32LCO2NXAmyfDPs5klxL0kuKrClrbJp7cuyDujzgdjbFDTjISvJWqncT4Iu9tfsYWTzEyHqKRtOgg7ylXVcCUi2UAcDyUB4Cs5rx6N-Cux2OpizNtRYrgmruVcx21xJA-onlsXXbd0x5t23RXG5Tr2r3Lc3pL8DbPl=8ZnvZ63pCsWVn=JP0ZnibdTxqEPPTP7Xhn0rY8O11IOsdtsafyJNd=9xPpwdvZ9bzsSoW9wFF2FcuvnXUE9hCpvj7RFTMOOHbA20MTYnk6ZlS1HuEYeZhYVFlvOVHjyd1cftuys8CsuWYI8FVDZJemyr--Z=55tlEPgZjKedCnPcITb1ia7_UcGF9Lamx5osYnv8W=lr7x3u5Z_wKTeN0nee8abYf1oCGxZ0nej6z=o-CTyPcpPgp2pKHF_96H5RIZKmSq-JNw9epx1ltDBgOaB8vjPWO==I6gsxnPBSH5eF6bBLmtWMBj2C4pAd5BDdarcofj2pUwCSFjLhdg3XIurHHsJIrUBymq3iwym7Wo7Wgb5Rr1IhDCMWwVnhV3FOJnAPOC7dLj9SP4m6zTBiBhq2O-U3hkfxt8eSr5gT3HhvGcH-oPghx1doc348W_EbaxKFbLWp9u4fNWOfpeE6mLH_0=erh8saI-dPvgJ3w3t0zGCwio5wxYArcSer5kWOM-id5C5HF7DgbjSp6bC2RN5x1kK1hf_WmCk6K8IZdAaLCDMYJNKmxm4-4oV3kEZBRf8-sqPEFa1DJuDsCVETGTWttJkAFgYb1FulV3pYHTFDMrj1jYbTmsJzNsLf7YcsRTPOm3yABd0slCHu1=sPyiIJafjYhUOyIurkLqiNGEYOB3M7tYyFgrdmhO=cRDhwlWEzdjRWk8P-==G8okwabuWFom9U_nU2f68GjR5zGN8DO1ARgKwsUnIx_NW97=UpKw09JzOR4BhpqFtxqmEXOBzhC0iFiADGl48GVl2A5ITPxn3RT6DylZSX7TOy33GZdI65i_nKNplsDJWTDGLPC1eegBGqV30-aWUn=GfMbeLv=Ze51OETee-Abr30-to25jkSS2mWXHM37FtADInpzgJKyspBi1XWRuNjV2JTJ=s1mZbp5PWz6yAXWa1W5VVN4os63wZ1KFAL0C8=sHaXXn7M-eEBSEejBE8a0xoiDHSIqtW7HjGWASz-wPBNhuRhEW7A2PaxLYN5AlYd7BuzpFuOz7nxq5lOITIu2xKl00byIFdkJRDnKmKF3d7XOwlGG9UR5FRcu92k4BH2txcqaO=zUPDz_G0XXoqp1UgJkLAt749o6bEoxgVnI8BRgS78FpL1IsjGavC9kUydges3gZ3uAiAJrInwMjdvmm=n1yMKFBMHs5zFFtywv1AVLOp8J53qJElTvWusqGNZfv5YdBxmHFTjB=4u9m21ZVa4fOnnHdcMAiJeMiowut55RNC8SKnwXmX3G6JUM_ijCX0LqgWwaDbwM2_S7bZ=ZZt0JvSyfMq6hdXhJAktMD7n5FfR3sCzmyiW8OoD-jp0F5ME-pLTSqd0nWmaGUS8GVRsPOjxl-aAwKyBkzMwRU2nhdBVOqNjd9Hpv63Pfgtq-Ge8mxxMWqeKnIEpDVkTWjYOZEDVVvctovF_Lgqdu1wRpKECITk3f1Z-8v7RXuHt5b6khvh_vVr_6xMZpC_-j_aMoHRvqKWZLaEm3LkgioWORsn2_P5d44lc9B8FXoomiVXHD5NoXWcqZOESoCxz16SO6=jKvXLNSALuX=7b=XF-zS=1dxoa8BCZfTHdrD4qUkdwGo_2F93m7D-DBk1XSenr6z7UM9GipM9uRu3HosF_fkqHgZTK_7MpC5pgqpLoofFBJ1vReyXi99yRLg1zb8=ytmvB54=IhZeAKDYZcrdT7xWWVB0Y5aujMmZgBL2XWxKztlGhkIeFF7jzls-r1Ooupy5ESBbPBAnxkW_oNVbdpDKmxWmOOSgxXlWfwJeDgUaZXegVWwJJi8ULon0NYk=TgDHTe0y1C_Nh_djlUYraYWA=Gtr75rdYcyEx-Itdq=hLcmn5s_X5VlLtCZ0HLVq7A16cX3qFfzdheH9J=OFbufdfLZcq61nHjnzo2WNio27S4DwhHjPq2=lNK9DOdZx1HjmULzZMXthZ5FxwwvU0PYlqDoB3HF8R0Ln0prwtkrliTdt8IOwIGEkB5C50_wGwIVd-gAd7E1WCc28DphcaiRUivEgiFHGH4viqxN5RGWCOH6EDcYG4JBdiux4_vXuq-EF9nAzBVbBiAmUJMi3daqi9EFB-NX292Jb8rd7hrb0UpwkiUFr6rhI0U9M7FZ2qCVExi9WVSP3=ppvEh3GWMYos_dESybe3FEDcu36bIa=w34i4Sjwug9C7u-JqAzU4W8LZ2t3iSafhPW1Jwi2DON9jBB_mL5hhmP=0VRq4pv-u_FyZU_Ycs9qbPmplRwYW8ZJa-bHCZ9ToeX50yGrKdAKVoTDPfJGLiSg68mjXW7u7sE1ouzc9OjEHZse5HMVCf3kHJODLXxCmPV=8oqMXnipckJcvcAIyCnk8_N0DzmospXinqKPNnRSTl6PN41SjfKX93dWcDW0j8El36sD9ZZoT4BU2jViwEm=y7kUC4WkjcedGyHp0gpOobZ=FvRtRjUMj_0l4W211kxaVBwlr24TFfJhhXTnksVayoGp0Ipp=K=-SB2c5KmTTmPHBJaMih4BXcsRNwMZsRv-ybZ9b09hEOKh1Y0CNqCmkkZdL9CiN8z6B2cNKpmthm1SKrR-n1zLvjqZNfpsBG=TXwENS_za4IbrC3RinZclJhajA7opjvlvVE8_7SRpDw_YJ8rv8N7f6BjAoSTLCb58z1VV5CWecFbSyH4-Em0SLOOI0OZbbTRCP__gq0JFti2644UVunrdmZZoC63tIblHNRO_T3YA',
    'x-y8s6k3db-b': '-pg69tb',
    'x-y8s6k3db-c': 'AMBGf3aJAQAA5QlK6Epk2ZN4YdHy0ZQH4SOB2d442IeO2ReiQJerDZbKm6Ar',
    'x-y8s6k3db-d': 'ABaAhIDBCKGFgQGAAYIQgISigaIAwBGAzvpCzi_33weXqw2WypugK_______WRq4AB8JWNqJVZ3L26Z82Tmp-Ww',
    'x-y8s6k3db-f': 'AwKSmXaJAQAAH_PvFR3DE_nzh9R44Wl4nDJI-4960MkQXtJoiGve9SxFufvrATtneJqucirJwH8AAEB3AAAAAA==',
    'x-y8s6k3db-z': 'q',
}

params = {
    'apikey': 'sGJGRvnBEzn4qvQyGZe7prihKstgGXXT',
    'styleid': PRODUCT_ID,
    'page': '1',
    'pagesize': '10',
    'starrating': '',
    'sortby': '-positivefeedbackcount,-submissiontime',
    'searchTerm': '',
    'feature': '',
    'hasPhotos': 'false',
    'filterBySize': '',
    'filterByColor': '',
    'filterByWidth': '',
    'isVerifiedPurchase': 'false',
}

response = requests.get('https://www.nordstrom.com/review/review', params=params, cookies=cookies, headers=headers)
ret = json.loads(response.text)
max = int(ret['totalResults']/10)+1

#The above code is scraping the reviews from the Nordstrom website.
#Stop if 403 error is reached. In case it does reach 403, then update the above header and chanage the range to the number of page where 403 error was recieved.
#Then run again, keep this method repeating untill the entire reviews for an item are downloaded
params = {
    'apikey': 'sGJGRvnBEzn4qvQyGZe7prihKstgGXXT',
    'styleid': PRODUCT_ID,
    'page': '2',
    'pagesize': '10',
    'starrating': '',
    'sortby': '-positivefeedbackcount,-submissiontime',
    'searchTerm': '',
    'feature': '',
    'hasPhotos': 'false',
    'filterBySize': '',
    'filterByColor': '',
    'filterByWidth': '',
    'isVerifiedPurchase': 'false',
}


for page in range(1,max+2):
    res = 200
    counter = 0
    if page<0:
        continue
    while(True):
        # url = f"https://www.nordstrom.com/review/review?apikey=sGJGRvnBEzn4qvQyGZe7prihKstgGXXT&styleid={productKey[1]}&page={page}&pagesize=10&starrating=&sortby=-submissiontime&searchTerm=&feature=&hasPhotos=false&filterBySize=&filterByColor=&filterByWidth=&isVerifiedPurchase=false"
        params["page"] = str(page)
        response = requests.get('https://www.nordstrom.com/review/review', params=params, cookies=cookies, headers=headers)
        #response = requests.request("GET", url, headers=headers, data=payload)

        print(f'Page Num: {page}, Response Status{response.status_code}')
        if response.status_code==403:
            counter+=1
            if counter == 3:
                res = response.status_code
                break
            sleep(randint(20,60))
            continue
            # break
        ret = json.loads(response.text)
        print(f'Page Num: {page}, review count{len(ret["reviews"])}')
        for i in ret['reviews']:
            if i.get('userNickname'):
                user = i['userNickname']
            else:
                user = 'N/A'
            if i.get('syndicationSource'):
                syndicationSource ='Reposted from '+ i['syndicationSource']['name']
            saveCsv_second(user,i['starRating'],i['submissionDate'],i.get('title','NA'),i['comment'],i.get('positiveVoteCount',0),f'{PRODUCT_ID}.csv')
        break
    if res==403:
        break
    sleep(randint(10,15))