import os
import json
import scrapy,requests
from urllib.parse import urlencode
from datetime import datetime


class LinkedinSpiderSpider(scrapy.Spider):
    name = 'linkedin_spider'    
    cookies={}
    txt=open('cookies.txt','r',encoding='utf-8').read()
    Data=str(txt).split('\n')
    for rows in Data:
        row=str(rows).split('\t')
        if len(row)>=7:
            cookies[row[-2]]=row[-1]
    CK=[]
    for k,v in cookies.items():
        CK.append(k+'='+v)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'en-US,en;q=0.5',
        'x-li-lang': 'en_US',
        'Connection': 'keep-alive',
        'csrf-token': str(cookies['JSESSIONID']).replace('"',''),
        'Cookie': ('; '.join(CK)),
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'x-restli-protocol-version': '2.0.0',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    LIMIT=[]
    def start_requests(self):
        start=0
        url='https://www.linkedin.com/voyager/api/graphql?variables=(start:'+str(start)+',origin:FACETED_SEARCH,query:(flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:currentCompany,value:List(1035)),(key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.9bdbc7f24aade2f88bd25cf81bf1f811'
        yield scrapy.Request(url=url, callback=self.parse_user, headers=self.headers, meta={'start': start}, dont_filter=True)
    def parse_user(self,response):
        start=response.meta['start']
        Data=json.loads(response.text)
        MEM=0
        for row in Data['included']:
            if 'navigationUrl' in row and 'https://www.linkedin.com/in/' in row['navigationUrl']:
                username=str(row['navigationUrl']).split('https://www.linkedin.com/in/')[1].split('?')[0]
                if not username in self.LIMIT and len(self.LIMIT)<800:
                    MEM+=1
                    self.LIMIT.append(username)
                    params = {
                        'q': 'memberIdentity',
                        'includeWebMetadata': 'false',
                        'memberIdentity': username,
                        'decorationId': 'com.linkedin.voyager.dash.deco.identity.profile.WebTopCardCore-20',
                    }
                    url = 'https://www.linkedin.com/voyager/api/identity/dash/profiles?' + urlencode(params)
                    yield scrapy.Request(url=url, callback=self.parse, headers=self.headers, meta={'username': username}, dont_filter=True)
        if MEM>0 and len(self.LIMIT)<800:
            start+=10
            url='https://www.linkedin.com/voyager/api/graphql?variables=(start:'+str(start)+',origin:FACETED_SEARCH,query:(flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:currentCompany,value:List(1035)),(key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.9bdbc7f24aade2f88bd25cf81bf1f811'
            yield scrapy.Request(url=url, callback=self.parse_user, headers=self.headers, meta={'start': start}, dont_filter=True)
    def parse(self, response):
        basic_data = {
            'ID': '',
            'Username': response.meta['username'],
            'First Name': '',
            'Last Name': '',
            'Profile URL': 'https://www.linkedin.com/in/' + response.meta['username'],
            'Title': '',
            'Contact Info': {
                'Email': '',
                'Twitter': [],
            },
            'Location': '',
            'Country': '',
            'About': '',
            'Total Followers': '',
        }
        rows = response.json()['included']
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.common.Geo':
                location = row.get('defaultLocalizedNameWithoutCountryName')
                if location:
                    basic_data['Location'] = location
                else:
                    basic_data['Country'] = row.get('defaultLocalizedName')
            elif row['$type'] == 'com.linkedin.voyager.dash.identity.profile.Profile':
                username = row.get('publicIdentifier','')
                if username != response.meta['username']:
                    continue
                basic_data['First Name'] = row['firstName']
                basic_data['Last Name'] = row['lastName']
                basic_data['Title'] = row['headline']
                basic_data['ID'] = row['entityUrn'].split(':')[-1]
        
        url_about = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(profileUrn:urn%3Ali%3Afsd_profile%3A{basic_data["ID"]})&&queryId=voyagerIdentityDashProfileCards.3c16e320676acb02602ae17c4556669d'
        yield scrapy.Request(url=url_about, callback=self.parse_about, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)

    def parse_about(self, response):
        basic_data = response.meta['basic_data']

        rows = response.json()['included']
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.identity.profile.tetris.Card':
                if ',ABOUT,' in row['entityUrn']:
                    top_components = row['topComponents']
                    if len(top_components) > 0:
                        basic_data['About'] = top_components[-1]['components']['textComponent']['text']['text']
                    break

        url_socials = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=false&variables=(memberIdentity:{basic_data["Username"]})&=&queryId=voyagerIdentityDashProfiles.84cab0be7183be5d0b8e79cd7d5ffb7b'
        yield scrapy.Request(url=url_socials, callback=self.parse_socials, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)

    def parse_socials(self, response):
        basic_data = response.meta['basic_data']
        rows = response.json()['included']
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.identity.profile.Profile':
                username = row.get('publicIdentifier','')
                if username != basic_data['Username']:
                    continue
                basic_data['Contact Info']['Twitter'] = [handle['name'] for handle in row['twitterHandles']]
                email = row['emailAddress']
                if email:
                    basic_data['Contact Info']['Email'] = email.get('emailAddress')
        url_followers = f'	https://www.linkedin.com/voyager/api/identity/dash/profiles?q=memberIdentity&memberIdentity={basic_data["Username"]}&decorationId=com.linkedin.voyager.dash.deco.identity.profile.TopCardSupplementary-129'
        yield scrapy.Request(url=url_followers, callback=self.parse_followers, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)
    
    def parse_followers(self, response):
        basic_data = response.meta['basic_data']
        rows = response.json()['included']
        companies = {}
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.organization.Company':
                username = row['universalName']
                entity = row['entityUrn'].split(':')[-1]
                companies[entity] = username
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.feed.FollowingState':
                basic_data['Total Followers'] = row['followerCount']
            elif '*company' in row: # row['$type'] == 'com.linkedin.voyager.dash.identity.profile.Position':
                company_id = row['*company'].split(':')[-1]
                company = {
                    'ID': company_id,
                    'Name': '',
                    'Username': companies.get(company_id)
                }
                for k,v in row.items():
                    if str(k).endswith('Name'):
                        company['Name']=v                    
                basic_data['Company Header'] = company
        url_awards = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(profileUrn:urn%3Ali%3Afsd_profile%3A{basic_data["ID"]},sectionType:honors)&&queryId=voyagerIdentityDashProfileComponents.b7202de42ed588155dbc50de3622b379'
        yield scrapy.Request(url=url_awards, callback=self.parse_awards, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)

    def parse_awards(self, response):
        basic_data = response.meta['basic_data']
        basic_data['Awards'] = []
        rows = response.json()['included']
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.identity.profile.tetris.PagedListComponent':
                for item in row['components']['elements']:
                    award = {
                        'Name': '',
                        'Date': '',
                        'Description': ''
                    }
                    details = item['components']['entityComponent']
                    if details:
                        award['Name'] = details['title']['text']
                        description = ''
                        if details['subComponents']:
                            sub_componenets = details['subComponents']['components']
                            for sub_component in sub_componenets:
                                fixed_list = sub_component['components']['fixedListComponent']
                                if fixed_list:
                                    description = fixed_list['components'][0]['components']['textComponent']['text']['text']
                                    break
                        award['Description'] = description
                        try:
                            award['Date'] = details['subtitle']['text'].split(' · ')[-1]
                        except:
                            pass
                        basic_data['Awards'].append(award)

        url_experience = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(profileUrn:urn%3Ali%3Afsd_profile%3A{basic_data["ID"]},sectionType:experience,locale:en_US)&&queryId=voyagerIdentityDashProfileComponents.b7202de42ed588155dbc50de3622b379'
        yield scrapy.Request(url=url_experience, callback=self.parse_experience, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)
    
    def parse_experience(self, response):
        basic_data = response.meta['basic_data']
        basic_data['Current Experience'] = []
        basic_data['Previous Experience'] = []

        companies = {}

        rows = response.json()['included']
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.identity.profile.tetris.PagedListComponent':
                for item in row['components']['elements']:
                    component = item['components']
                    if component['entityComponent']['subComponents']:
                        try:
                            dates, period = component['entityComponent']['caption']['text'].split(' · ')
                            continue
                        except:
                            pass
                        company_url = component['entityComponent']['textActionTarget']
                        company_name = component['entityComponent']['title']['text']
                        companies[company_url] = company_name

        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.identity.profile.tetris.PagedListComponent':
                for item in row['components']['elements']:
                    experience = {
                        'Role': '',
                        'Company': '',
                        'Company URL': '',
                        'Start Date': '',
                        'End Date': '',
                        'Period': '',
                        'Present': '',
                        'Description': '',
                        'Location': ''
                    }
                    component = item['components']
                    experience['Role'] = component['entityComponent']['title']['text']
                    try:
                        dates, period = component['entityComponent']['caption']['text'].split(' · ')
                    except:
                        continue
                    end_date=''
                    try:
                        start_date, end_date = dates.split(' - ')
                    except:
                        start_date = dates
                    company_url = component['entityComponent']['textActionTarget']
                    if not company_url:
                        company_url = component['entityComponent']['image']['actionTarget']
                    if component['entityComponent']['subtitle']:
                        company = component['entityComponent']['subtitle']['text'].split(' · ')[0]
                    else:
                        company = companies.get(company_url)
                    if 'Present' in end_date:
                        experience['Present'] = True
                        end_date = ''
                    else:
                        experience['Present'] = False
                    experience['Start Date'] = start_date
                    experience['End Date'] = end_date
                    experience['Period'] = period
                    experience['Company'] = company
                    experience['Company URL'] = company_url
                    try:
                        experience['Location']=component['entityComponent']['metadata']['text']
                    except:
                        pass
                    sub_components = component['entityComponent']['subComponents']
                    if sub_components:
                        try:
                            experience['Description'] = sub_components['components'][0]['components']['fixedListComponent']['components'][0]['components']['textComponent']['text']['text']
                        except:
                            experience['Description'] = ''
                    if experience['Present']:
                        basic_data['Current Experience'].append(experience)
                    else:
                        basic_data['Previous Experience'].append(experience)
        recommendations_url = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(profileUrn:urn%3Ali%3Afsd_profile%3A{basic_data["ID"]},sectionType:recommendations,tabIndex:0,locale:en_US)&&queryId=voyagerIdentityDashProfileComponents.b7202de42ed588155dbc50de3622b379'
        yield scrapy.Request(url=recommendations_url, callback=self.parse_recommendations, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)

    def parse_recommendations(self, response):
        basic_data = response.meta['basic_data']
        basic_data['Recommendations'] = []

        rows = response.json()['included']
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.identity.profile.tetris.PagedListComponent' and 'RECEIVED_RECOMMENDATIONS' in row['entityUrn']:
                items = row['components']['elements']
                for item in items:
                    recommendation = {
                        'Name': '',
                        'Role': '',
                        'Profile URL': '',
                        'Header': '',
                        'Details': '',
                    }
                    component = item['components']['entityComponent']
                    try:
                        recommendation['Header'] = component['caption']['text']
                    except:
                        recommendation['Header']=''
                    recommendation['Name'] = component['title']['text']
                    recommendation['Role'] = component['subtitle']['text']
                    recommendation['Profile URL'] = component['textActionTarget']
                    recommendation['Details'] = component['subComponents']['components'][0]['components']['fixedListComponent']['components'][0]['components']['textComponent']['text']['text']

                    basic_data['Recommendations'].append(recommendation)
        
        licences_url = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(profileUrn:urn%3Ali%3Afsd_profile%3A{basic_data["ID"]},sectionType:certifications,locale:en_US)&&queryId=voyagerIdentityDashProfileComponents.b7202de42ed588155dbc50de3622b379'
        yield scrapy.Request(url=licences_url, callback=self.parse_licences, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)
    
    def parse_licences(self, response):
        basic_data = response.meta['basic_data']
        basic_data['Licences'] = []

        rows = response.json()['included']
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.identity.profile.tetris.PagedListComponent':
                items = row['components']['elements']
                for item in items:
                    licence = {
                        'Name': '',
                        'Issuing Organization': '',
                        'Issue Date': '',
                        'Expiration Date': '',
                        'Credential ID': '',
                        'Credential URL': '',
                    }
                    component = item['components']['entityComponent']
                    if component:
                        licence['Name'] = component['title']['text']
                        if component['subtitle']:
                            licence['Issuing Organization'] = component['subtitle']['text']
                        if component['caption']:
                            dates = component['caption']['text'].replace('Issued ', '').replace('Expires ', '')
                            if ' · ' in dates:
                                licence['Issue Date'], licence['Expiration Date'] = dates.split(' · ')
                            else:
                                licence['Issue Date'] = dates
                        if component['metadata']:
                            licence['Credential ID'] = component['metadata']['text'].replace('Credential ID ', '')
                        licence['Credential URL'] = component['textActionTarget']

                        basic_data['Licences'].append(licence)

        posts_url = f'https://www.linkedin.com/voyager/api/identity/profileUpdatesV2?count=50&includeLongTermHistory=true&moduleKey=creator_profile_all_content_view%3Adesktop&numComments=0&profileUrn=urn%3Ali%3Afsd_profile%3A{basic_data["ID"]}&q=memberShareFeed&start=0'
        yield scrapy.Request(url=posts_url, callback=self.parse_posts, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)
    
    def parse_posts(self, response):
        basic_data = response.meta['basic_data']
        basic_data['Posts'] = []

        rows = response.json()['included']

        all_posts = self.posts_helper(basic_data['ID'], rows)
        
        for _, post in all_posts.items():
            if basic_data['ID'] == post['Owner ID']:
                if post['Time of post'].endswith('yr'):
                    number_years = int(post['Time of post'].replace('yr', ''))
                    if number_years > 1:
                        continue
                if post['Original Post ID']:
                    post['Original Post'] = all_posts.get(post['Original Post ID'], {})
                basic_data['Posts'].append(post)

        url_comments = f'https://www.linkedin.com/voyager/api/identity/profileUpdatesV2?count=20&includeLongTermHistory=true&moduleKey=creator_profile_comments_content_view%3Adesktop&numComments=0&profileUrn=urn%3Ali%3Afsd_profile%3A{basic_data["ID"]}&q=memberComments&start=0'
        yield scrapy.Request(url=url_comments, callback=self.parse_comments, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)
    
    def parse_comments(self, response):
        basic_data = response.meta['basic_data']
        basic_data['Comments'] = []
        rows = response.json()['included']

        original_posts = {}
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.feed.render.UpdateV2':
                post = {
                    'Name': '',
                    'Text': '',
                }
                activity_id = row['*socialDetail'].split(':')[-1]
                try:
                    post['Name'] = row['actor']['name']['text']
                except:
                    pass
                if row.get('commentary'):
                    post['Text'] = row['commentary']['text']['text']
                original_posts[activity_id] = post

        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.feed.Comment':
                if row['commenterProfileId'] == basic_data['ID']:
                    comment = {
                        'Post Contact Name': '',
                        'Post Description': '',
                        'Contact comment': '',
                        'Comment time': '',
                    }
                    comment['Contact comment'] = row['commentV2']['text']
                    timestamp_comment = row['createdTime']
                    how_long_in_months = (datetime.now() - datetime.fromtimestamp(timestamp_comment/1000)).days / 30
                    if how_long_in_months > 16:
                        continue
                    comment['Comment time'] = datetime.fromtimestamp(timestamp_comment/1000).strftime('%Y-%m-%d %H:%M:%S')
                    thread_id = row['threadId'].split(':')[-1]
                    comment['Post Contact Name'] = original_posts.get(thread_id, {}).get('Name')
                    comment['Post Description'] = original_posts.get(thread_id, {}).get('Text')
                    basic_data['Comments'].append(comment)
        
        url_reactions = f'https://www.linkedin.com/voyager/api/identity/profileUpdatesV2?count=50&includeLongTermHistory=true&moduleKey=creator_profile_reactions_content_view%3Adesktop&numComments=0&profileUrn=urn%3Ali%3Afsd_profile%3A{basic_data["ID"]}&q=memberReactions&start=0'
        yield scrapy.Request(url=url_reactions, callback=self.parse_reactions, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)
    
    def parse_reactions(self, response):
        basic_data = response.meta['basic_data']
        basic_data['Reactions'] = []

        rows = response.json()['included']

        links = {}
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.feed.render.UpdateActions':
                activity_id = row['entityUrn'].split('activity:')[1].split(',')[0]
                for action in row['actions']:
                    if action['actionType'] == 'SHARE_VIA':
                        links[activity_id] = action['url']
                        break

        details = {}
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.feed.SocialDetail':
                activity_id = row['entityUrn'].split(':')[-1]
                num_likes = row['likes']['paging']['total']
                num_comments = row['comments']['paging']['total']
                details[activity_id] = {
                    'Likes': num_likes,
                    'Comments': num_comments
                }

        articles = {}
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.feed.render.UpdateV2':
                article = {
                    'Text': '',
                    'Url': '',
                }
                activity_id = row['*socialDetail'].split(':')[-1]
                try:
                    article_link = row['content']['navigationContext']['accessibilityText']
                    if 'Open article: ' in article_link:
                        article_link = article_link.split(': ', 1)[1]
                        article['Url'] = article_link
                except:
                    pass
                if row.get('commentary'):
                    article['Text'] = row['commentary']['text']['text']
                articles[activity_id] = article

        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.feed.render.UpdateV2':
                reaction = {
                    'Name of Contact': '',
                    'Contact Role': '',
                    'Post Details': {}
                }
                activity_id = row['*socialDetail'].split(':')[-1]
                if not row['header']:
                    continue
                header_attributes = row['header']['text']['attributes']
                actor_id = None
                for attribute in header_attributes:
                    if attribute['type'] == 'PROFILE_FULLNAME':
                        actor_id = attribute['*miniProfile'].split(':')[-1]
                        break
                if basic_data['ID'] != actor_id:
                    continue

                post = {
                    'ID': '',
                    'Text': '',
                    'Article Name': '',
                    'Link': '',
                    'Time of post': '',
                    '# of Likes': '',
                    '# of Comments': '',
                }
                if row.get('actor'):
                    reaction['Name of Contact'] = row['actor']['name']['text']
                    if not row['actor']['urn'].startswith('urn:li:company:'):
                        try:
                            reaction['Contact Role'] = row['actor']['description']['text']
                        except:
                            pass
                    post['Time of post'] = row['actor']['subDescription']['text'].split(' • ')[0]
                
                entity_id = row['entityUrn'].split('activity:')[1].split(',')[0]
                post['ID'] = activity_id
                if row.get('commentary'):
                    post['Text'] = row['commentary']['text']['text']
                post['Link'] = links.get(entity_id)
                post['# of Likes'] = details.get(activity_id, {}).get('Likes')
                post['# of Comments'] = details.get(activity_id, {}).get('Comments')
                try:
                    article_link = row['content']['navigationContext']['accessibilityText']
                    if 'Open article: ' in article_link:
                        post['Article Name'] = article_link.replace('Open article: ', '')
                except:
                    pass

                activity_share = row.get('*resharedUpdate')
                if activity_share:
                    activity_share = activity_share.split('activity:')[1].split(',')[0]
                    post['Article Name'] = articles.get(activity_share, {}).get('Url')
                    # post['Original Text'] = articles.get(activity_share, {}).get('Text')
                if not articles.get(activity_share):
                    post['Article Name'] = articles.get(entity_id, {}).get('Url')
                    # post['Original Text'] = articles.get(entity_id, {}).get('Text')
                
                reaction['Post Details'] = post

                basic_data['Reactions'].append(reaction)
        
        url_company = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(universalName:{basic_data["Company Header"]["Username"]})&=&queryId=voyagerOrganizationDashCompanies.73e009f60a7d34240a3c0731d9856dd6'
        yield scrapy.Request(url=url_company, callback=self.parse_company, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)
    
    def parse_company(self, response):
        basic_data = response.meta['basic_data']

        company = {
            'ID': basic_data['Company Header']['ID'],
            'Name': basic_data['Company Header']['Name'],
            'Username': basic_data['Company Header']['Username']
        }
        about = {
            'Owerview': '',
            'Website': '',
            'Industries': '',
            'Company Size': '',
            'Headquarters': '',
            'Founded': '',
            'Specialties': ''
        }
        del basic_data['Company Header']


        rows = response.json()['included']

        industries = {}
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.common.Industry':
                entity = row['entityUrn'].split(':')[-1]
                industries[entity] = row['name']

        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.organization.Company':
                entity = row['entityUrn'].split(':')[-1]
                if entity != company['ID']:
                    continue
                about['Owerview'] = row['description']
                about['Website'] = row['websiteUrl']
                about['Industries'] = [industries.get(industry.split(':')[-1]) for industry in row['*industry']]
                start_size = row['employeeCountRange']['start']
                end_size = row['employeeCountRange']['end']
                if end_size:
                    about['Company Size'] = f'{start_size} - {end_size}'
                else:
                    about['Company Size'] = f'{start_size}+'
                linkedin_employees = row['employeeCount']
                if linkedin_employees:
                    about['Company Size'] += f' ({linkedin_employees} employees on LinkedIn)'
                if row['headquarter']:
                    if row['headquarter']['address']:
                        about['Headquarters'] = row['headquarter']['address']['city']
                        if row['headquarter']['address']['geographicArea']:
                            about['Headquarters'] += ', ' + row['headquarter']['address']['geographicArea']
                founded_on = row.get('foundedOn')
                if founded_on:
                    about['Founded'] = founded_on.get('year', '')
                about['Specialties'] = row['specialities']
                company['About'] = about
                break
        basic_data['Company'] = company

        url_posts = f'https://www.linkedin.com/voyager/api/organization/updatesV2?companyIdOrUniversalName={basic_data["Company"]["Username"]}&count=20&moduleKey=ORGANIZATION_MEMBER_FEED_DESKTOP&numComments=0&numLikes=0&q=companyRelevanceFeed'
        yield scrapy.Request(url=url_posts, callback=self.parse_company_posts, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)
    
    def parse_company_posts(self, response):
        basic_data = response.meta['basic_data']
        basic_data['Company']['Posts'] = []

        rows = response.json()['included']

        all_posts = self.posts_helper(basic_data['Company']['ID'], rows)
        for _, post in all_posts.items():
            basic_data['Company']['Posts'].append(post)

        url_jobs = f'https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-169&count=20&q=jobSearch&query=(origin:JOB_SEARCH_PAGE_JOB_FILTER,locationUnion:(geoId:92000000),selectedFilters:(company:List({basic_data["Company"]["ID"]})),spellCorrectionEnabled:true)&start=0'
        yield scrapy.Request(url=url_jobs, callback=self.parse_company_jobs, headers=self.headers, meta={'basic_data': basic_data}, dont_filter=True)
    
    def parse_company_jobs(self, response):
        basic_data = response.meta['basic_data']
        basic_data['Company']['Jobs'] = []

        rows = response.json()['included']

        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.dash.jobs.JobPostingCard':
                if row.get('*jobPosting'):
                    job = {
                        'ID': '',
                        'Title': '',
                        'Description': '',
                        'URL': '',
                    }
                    entity = row['*jobPosting'].split(':')[-1]
                    job['ID'] = entity
                    job['Title'] = row['jobPostingTitle']
                    job['URL'] = f'https://www.linkedin.com/jobs/view/{entity}/'

                    basic_data['Company']['Jobs'].append(job)
        if len(basic_data['Company']['Jobs']) > 0:
            current_job = basic_data['Company']['Jobs'][0]
            other_jobs = basic_data['Company']['Jobs'][1:]
            url_job = f'https://www.linkedin.com/voyager/api/jobs/jobPostings/{current_job["ID"]}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65&topN=1&topNRequestedFlavors=List(TOP_APPLICANT,IN_NETWORK,COMPANY_RECRUIT,SCHOOL_RECRUIT,HIDDEN_GEM,ACTIVELY_HIRING_COMPANY)'

            yield scrapy.Request(url=url_job.format(current_job['ID']), callback=self.parse_company_job, headers=self.headers, meta={'basic_data': basic_data, 'other_jobs': other_jobs}, dont_filter=True)
        else:
            username = basic_data['Username']
            file_name = os.path.join('results', username + '.json')
            open(file_name, 'w').write(json.dumps(basic_data, indent=4))
    
    def parse_company_job(self, response):
        basic_data = response.meta['basic_data']
        other_jobs = response.meta['other_jobs']

        data = response.json()['data']
        job_id = str(data['jobPostingId'])
        job_description = data['description']['text']
        for job in basic_data['Company']['Jobs']:
            if job['ID'] == job_id:
                job['Description'] = job_description
                break
        if len(other_jobs) > 0:
            current_job = other_jobs[0]
            other_jobs = other_jobs[1:]
            url_job = f'https://www.linkedin.com/voyager/api/jobs/jobPostings/{current_job["ID"]}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65&topN=1&topNRequestedFlavors=List(TOP_APPLICANT,IN_NETWORK,COMPANY_RECRUIT,SCHOOL_RECRUIT,HIDDEN_GEM,ACTIVELY_HIRING_COMPANY)'

            yield scrapy.Request(url=url_job.format(current_job['ID']), callback=self.parse_company_job, headers=self.headers, meta={'basic_data': basic_data, 'other_jobs': other_jobs}, dont_filter=True)
        else:
            username = basic_data['Username']
            file_name = os.path.join('results', username + '.json')
            open(file_name, 'w').write(json.dumps(basic_data, indent=4))

    def posts_helper(self, owner_id, rows):
        links = {}
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.feed.render.UpdateActions':
                activity_id = row['entityUrn'].split('activity:')[1].split(',')[0]
                for action in row['actions']:
                    if action['actionType'] == 'SHARE_VIA':
                        links[activity_id] = action['url']
                        break
        
        details = {}
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.feed.shared.SocialActivityCounts':
                activity_id = row['entityUrn'].split(':')[-1]
                num_likes = row['numLikes']
                num_comments = row['numComments']
                details[activity_id] = {
                    'Likes': num_likes,
                    'Comments': num_comments
                }

        articles = {}
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.feed.render.UpdateV2':
                article = {
                    'Text': '',
                    'Url': '',
                }
                activity_id = row['*socialDetail'].split(':')[-1]
                try:
                    article_link = row['content']['navigationContext']['accessibilityText']
                    if 'Open article: ' in article_link:
                        article_link = article_link.split(': ', 1)[1]
                        article['Url'] = article_link
                except:
                    pass
                if row.get('commentary'):
                    article['Text'] = row['commentary']['text']['text']
                articles[activity_id] = article

        all_posts = {}
        for row in rows:
            if row['$type'] == 'com.linkedin.voyager.feed.render.UpdateV2':
                actor_id = None
                actor_name = row['actor']['name']['text']
                if 'company' in row['actor']['urn']:
                    actor_id = row['actor']['urn'].split(':')[-1]
                else:
                    actor_attributes = row['actor']['name']['attributes']
                    actor_id = None
                    for attribute in actor_attributes:
                        if attribute['type'] == 'PROFILE_FULLNAME':
                            actor_id = attribute['*miniProfile'].split(':')[-1]
                            break
                post = {
                    'Owner ID': actor_id,
                    'Owner Name': actor_name,
                    'ID': '',
                    'Text': '',
                    'Article Name': '',
                    'Link': '',
                    'Time of post': '',
                    '# of Likes': '',
                    '# of Comments': '',
                    'Original Post ID': '',
                    'Original Post': {}
                }
                post['Time of post'] = row['actor']['subDescription']['text'].split(' • ')[0]
                if row.get('commentary'):
                    post['Text'] = row['commentary']['text']['text']
                post_id = row['*socialDetail'].split(':')[-1]
                activity_id = row['entityUrn'].split('activity:')[1].split(',')[0]
                post['ID'] = activity_id
                post['Link'] = links.get(activity_id)
                post['# of Likes'] = details.get(post_id, {}).get('Likes')
                post['# of Comments'] = details.get(post_id, {}).get('Comments')
                try:
                    article_link = row['content']['navigationContext']['accessibilityText']
                    if 'Open article: ' in article_link:
                        post['Article Name'] = article_link.replace('Open article: ', '')
                except:
                    pass
                
                activity_reshare = row.get('*resharedUpdate')
                if activity_reshare:
                    reshare_id = activity_reshare.split('activity:')[1].split(',')[0]
                    post['Original Post ID'] = reshare_id
                switch_post = False
                if row.get('header'):
                    header = row['header']['text']['text']
                    if header.endswith(' reposted this'):
                        new_post = {
                            'Owner ID': owner_id,
                            'Owner Name': header.replace(' reposted this', ''),
                            'ID': activity_id,
                            'Text': '',
                            'Article Name': '',
                            'Link': '',
                            'Time of post': '',
                            '# of Likes': details.get(post_id, {}).get('Likes'),
                            '# of Comments': details.get(post_id, {}).get('Comments'),
                            'Original Post ID': post_id,
                            'Original Post': {}
                        }
                        all_posts[activity_id] = new_post
                        switch_post = True
                if not switch_post:
                    all_posts[activity_id] = post
                else:
                    all_posts[post_id] = post
        return all_posts
