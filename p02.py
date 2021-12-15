import  requests
import parsel
import xlwt
import  time

url="https://search.jd.com/Search?"
#url地址
headers={
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
# ua伪装

params={
   'keyword':'手机'
}
#搜索的参数
res=requests.get(url=url,headers=headers,params=params)
# 请求
se=parsel.Selector(res.text)
#格式化结构
tt=se.xpath('//div[@class="gl-i-wrap"]')
print(tt.extract()[0])
# 这里为所有数据的
wb=xlwt.Workbook()
# # 打开excel
#
sheet=wb.add_sheet('sh')
# # 创建名为sh的工作簿
#
#
#
i=1  #行
l=1  # 列
for txt in tt.extract():


    l=0
    # time.sleep(3)
    se02 = parsel.Selector(txt)


    sname=''.join(se02.xpath("/html/body/div/div/a/em/text()").extract())
    sheet.write(i, l, sname)
    l = l + 1

    price = se02.xpath('//div[@class="p-price"]/strong/i/text()').extract()[0]
    # 如果不加[0]会出现['2011']


    sheet.write(i, l, price)
    l = l + 1

    data = se02.xpath('//div[@class="p-img"]/a/img/@data-lazy-img')
    imgurl = "https:" + data.extract()[0]
    sheet.write(i, l, imgurl)
    l=l+1

#     #sid  txt
    sid=se02.xpath('//div[@class="p-commit"]/strong/a/@id').extract()[0][10:]

#     #获取评价数据
    url02="https://club.jd.com/comment/productCommentSummaries.action?"
    params02={
        'referenceIds' :sid
    }
    pj=requests.get(url=url02,headers=headers,params=params02)

    rj=pj.json()

    pjdic=rj.get('CommentsCount')[0]

    sheet.write(i,l,pjdic.get('GoodCountStr'))
    l=l+1
    sheet.write(i, l, pjdic.get('PoorCountStr'))
    l = l + 1
    sheet.write(i, l, pjdic.get('GoodRate'))
    l = l + 1

    i = i + 1
    #本次循环结束进入下一个循环 同样的下次的内容写入下一行写入下一行

wb.save('手机商品11.xls')
print('爬取成功')


# print(res.text)

