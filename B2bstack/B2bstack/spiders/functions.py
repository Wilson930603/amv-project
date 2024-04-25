import hashlib,re,requests
def get_unit(text):
    p = re.compile('(?<!\d|\.)\d+(?:\.\d+)?\s*?(?:mg|kg|ml|gm|q\.s\.|ui|m|g|µg|l|bottles|bottle|Sheets|packs|pack)(?!\w)')
    z = p.findall(text.lower())
    z = list(dict.fromkeys(z))
    return z
def get_type(text):
    p = re.compile('(?<!\d|\.)\d+(?:\.\d+)?\s*?(?:Taped|taped|Diaper|diaper|Insert|insert|Pants|pants)(?!\w)')
    z = p.findall(text)
    z = list(dict.fromkeys(z))
    return z
def get_size(text):
    p = re.compile('(?<!\d|\.)\d+(?:\.\d+)?\s*?(?:Pcs|pcs)(?!\w)')
    z = p.findall(text)
    z = list(dict.fromkeys(z))
    return z
def translate(text,fromlag,tolang):
    data = {'text': text,'gfrom': fromlag,'gto': tolang}
    response = requests.post('https://www.webtran.eu/gtranslate/', data=data)
    return(response.text)
def Get_Number(xau):
    KQ=re.sub(r"([^0-9.])","", str(xau).strip())
    return KQ
def Get_String(xau):
    KQ=re.sub(r"([^A-Za-z])","-", str(xau).strip())
    return KQ
def Get_Input_Str(xau):
    KQ=re.sub(r"([^a-z])","", (str(xau).lower()).strip())
    return KQ
def cleanhtml(raw_html):
    if raw_html:
        raw_html=str(raw_html).replace('</',' ^</')
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext=(' '.join(cleantext.split())).strip()
        cleantext=str(cleantext).replace(' ^','^').replace('^ ','^')
        while '^^' in cleantext:
            cleantext=str(cleantext).replace('^^','^')
        cleantext=str(cleantext).replace('^','\n')
        return cleantext.strip()
    else:
        return ''
def cleanhtml_body(raw_html):
    KQ=''
    if raw_html:
        regex =re.compile(' style="(.*?)"')
        KQ=re.sub(regex, '', raw_html)
        regex =re.compile('<img .*?>')
        KQ=re.sub(regex, '', KQ)
        RUN=True
        while RUN==True:
            CHK=False
            STR=['<div></div>','<span></span>','<p></p>','<ul></ul>']
            for Str in STR:
                if Str in KQ:
                    CHK=True
                    KQ=KQ.replace(Str, '')
            if CHK==False:
                RUN=False
    return KQ
def kill_space(xau):
    xau=str(xau).replace('\t','').replace('\r','').replace('\n',', ')
    xau=(' '.join(xau.split())).strip()
    return xau
def key_MD5(xau):
    xau=(xau.upper()).strip()
    KQ=hashlib.md5(xau.encode('utf-8')).hexdigest()
    return KQ
def get_data_from_sql(conn,sql):
    DATASET=[]
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    column_names = [i[0] for i in cur.description]
    for row in rows:
        item={}
        for i in range(len(column_names)):
            item[column_names[i]]=row[i]
        DATASET.append(item)
    return DATASET
def get_item_from_json(result,item,space):
    if isinstance(item,dict):
        for k,v in item.items():
            if isinstance(v,dict) or isinstance(v,list):
                if space=='':
                    get_item_from_json(result,v,k)
                else:
                    get_item_from_json(result,v,space+'.'+k)
            else:
                if space=='':
                    result[k]=v
                else:
                    result[space+'.'+k]=v
    else:
        for i in range(len(item)):
            k=str(i)
            v=item[i]
            if isinstance(v,dict) or isinstance(v,list):
                if space=='':
                    get_item_from_json(result,v,k)
                else:
                    get_item_from_json(result,v,space+'.'+k)
            else:
                if space=='':
                    result[k]=v
                else:
                    result[space+'.'+k]=v
    return result
def fixEncoding(st):
    arr1 = ['&#192;','&#193;','&#194;','&#195;','&#200;','&#201;','&#202;','&#204;','&#205;','&#210;','&#211;','&#212;','&#213;','&#217;','&#218;','&#221;','&#224;','&#225;','&#226;','&#227;','&#232;','&#233;','&#234;','&#236;','&#237;','&#242;','&#243;','&#244;','&#245;','&#249;','&#250;','&#253;','&#7922;','&#7928;','&#7923;','&#7929;','&#7926;','&#7927;','&#7924;','&#7925;','&#7921;','&#7920;','&#7917;','&#7916;','&#7919;','&#7918;','&#7915;','&#7914;','&#7913;','&#7912;','&#432;','&#431;','&#7909;','&#7908;','&#7911;','&#7910;','&#361;','&#360;','&#7907;','&#7906;','&#7903;','&#7902;','&#7905;','&#7904;','&#7901;','&#7900;','&#7899;','&#7898;','&#417;','&#416;','&#7897;','&#7896;','&#7893;','&#7892;','&#7895;','&#7894;','&#7891;','&#7890;','&#7889;','&#7888;','&#7885;','&#7884;','&#7887;','&#7886;','&#7883;','&#7882;','&#7881;','&#7880;','&#297;','&#296;','&#7879;','&#7878;','&#7875;','&#7874;','&#7877;','&#7876;','&#7873;','&#7872;','&#7871;','&#7870;','&#7865;','&#7864;','&#7867;','&#7866;','&#7869;','&#7868;','&#7863;','&#7862;','&#7859;','&#7858;','&#7861;','&#7860;','&#7857;','&#7856;','&#7855;','&#7854;','&#259;','&#258;','&#7853;','&#7852;','&#7849;','&#7848;','&#7851;','&#7850;','&#7847;','&#7846;','&#7845;','&#7844;','&#7841;','&#7840;','&#7843;','&#7842;','&#273;','&#272;','&#65;','&#66;','&#67;','&#68;','&#69;','&#71;','&#72;','&#73;','&#75;','&#76;','&#77;','&#78;','&#79;','&#80;','&#81;','&#82;','&#83;','&#84;','&#85;','&#86;','&#88;','&#89;','&#97;','&#98;','&#99;','&#100;','&#101;','&#103;','&#104;','&#105;','&#107;','&#108;','&#109;','&#110;','&#111;','&#112;','&#113;','&#114;','&#115;','&#116;','&#117;','&#118;','&#120;','&#121;','&nbsp;','&quot;','&amp;','&#39;']
    arr2 = ['À','Á','Â','Ã','È','É','Ê','Ì','Í','Ò','Ó','Ô','Õ','Ù','Ú','Ý','à','á','â','ã','è','é','ê','ì','í','ò','ó','ô','õ','ù','ú','ý','Ỳ','Ỹ','ỳ','ỹ','Ỷ','ỷ','Ỵ','ỵ','ự','Ự','ử','Ử','ữ','Ữ','ừ','Ừ','ứ','Ứ','ư','Ư','ụ','Ụ','ủ','Ủ','ũ','Ũ','ợ','Ợ','ở','Ở','ỡ','Ỡ','ờ','Ờ','ớ','Ớ','ơ','Ơ','ộ','Ộ','ổ','Ổ','ỗ','Ỗ','ồ','Ồ','ố','Ố','ọ','Ọ','ỏ','Ỏ','ị','Ị','ỉ','Ỉ','ĩ','Ĩ','ệ','Ệ','ể','Ể','ễ','Ễ','ề','Ề','ế','Ế','ẹ','Ẹ','ẻ','Ẻ','ẽ','Ẽ','ặ','Ặ','ẳ','Ẳ','ẵ','Ẵ','ằ','Ằ','ắ','Ắ','ă','Ă','ậ','Ậ','ẩ','Ẩ','ẫ','Ẫ','ầ','Ầ','ấ','Ấ','ạ','Ạ','ả','Ả','đ','Đ','A','B','C','D','E','G','H','I','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y','a','b','c','d','e','g','h','i','k','l','m','n','o','p','q','r','s','t','u','v','x','y','','','&',"'"]
    for x, y in zip(arr1, arr2):
        st = st.replace(x, y)
    return st
def remove_accent(st):
    arr1 = ['"','ấ', 'ầ', 'ẩ', 'ẫ', 'ậ', 'Ấ', 'Ầ', 'Ẩ', 'Ẫ', 'Ậ', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ', 'Ắ', 'Ằ', 'Ẳ', 'Ẵ', 'Ặ', 'á', 'à', 'ả', 'ã', 'ạ', 'â', 'ă', 'Á', 'À', 'Ả', 'Ã', 'Ạ', 'Â', 'Ă', 'ế', 'ề', 'ể', 'ễ', 'ệ', 'Ế', 'Ề', 'Ể', 'Ễ', 'Ệ', 'é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ê', 'É', 'È', 'Ẻ', 'Ẽ', 'Ẹ', 'Ê', 'í', 'ì', 'ỉ', 'ĩ', 'ị', 'Í', 'Ì', 'Ỉ', 'Ĩ', 'Ị', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'Ố', 'Ồ', 'Ổ', 'Ô', 'Ộ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ', 'Ớ', 'Ờ', 'Ở', 'Ỡ', 'Ợ', 'ứ', 'ừ', 'ử', 'ữ', 'ự', 'Ứ', 'Ừ', 'Ử', 'Ữ', 'Ự', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ', 'Ý', 'Ỳ', 'Ỷ', 'Ỹ', 'Ỵ', 'Đ', 'đ', 'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ơ', 'Ó', 'Ò', 'Ỏ', 'Õ', 'Ọ', 'Ô', 'Ơ', 'ú', 'ù', 'ủ', 'ũ', 'ụ', 'ư', 'Ú', 'Ù', 'Ủ', 'Ũ', 'Ụ', 'Ư']
    arr2 = ['', 'a', 'a', 'a', 'a', 'a', 'A', 'A', 'A', 'A', 'A', 'a', 'a', 'a', 'a', 'a', 'A', 'A', 'A', 'A', 'A', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'e', 'e', 'e', 'e', 'e', 'E', 'E', 'E', 'E', 'E', 'e', 'e', 'e', 'e', 'e', 'e', 'E', 'E', 'E', 'E', 'E', 'E', 'i', 'i', 'i', 'i', 'i', 'I', 'I', 'I', 'I', 'I', 'o', 'o', 'o', 'o', 'o', 'O', 'O', 'O', 'O', 'O', 'o', 'o', 'o', 'o', 'o', 'O', 'O', 'O', 'O', 'O', 'u', 'u', 'u', 'u', 'u', 'U', 'U', 'U', 'U', 'U', 'y', 'y', 'y', 'y', 'y', 'Y', 'Y', 'Y', 'Y', 'Y', 'D', 'd', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'u', 'u', 'u', 'u', 'u', 'u', 'U', 'U', 'U', 'U', 'U', 'U']
    for x, y in zip(arr1, arr2):
        st = st.replace(x, y)
    return st
def post_slug(st):
    st = remove_accent(st)
    st = st.strip()
    st=re.sub(r"[^a-zA-Z0-9 -]","", st)
    st=re.sub(r"[ -]+","-", st)
    st=re.sub(r"^-|-$","", st)
    return st.lower()