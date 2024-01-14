ebussiness   
This is the programe of ebusiness written by Django   
1）download these code  
2）install python 3.7+  
3）pip3 install Django==4.1.6  
4) run runserver.bat  
5) open brower,enter http://127.0.0.1:8000  
#转换为MySQL支持   
1.	修改ebusiness/ebusiness/settings.py  
…  
#Database  
#https://docs.djangoproject.com/en/1.11/ref/settings/#databases    
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'ebusiness',  
        'USER': 'root',  
        'PASSWORD': '123456',  
        'HOST': '127.0.0.1',  
        'PORT': '3306',  
    }  
}  
…  
这里root的密码为123456。  
2.	在MySQL数据库中建立ebusiness数据库。数据集为utf-8  
3.	下载python插件pymysql和mysqlcilent  
/ebusiness>pip3 install pymysql  
/ebusiness>pip3 install mysqlcilent
5. 删除ebusiness中所有pyc文件,主要集中在%ebusiness_home%\ebusiness和%ebusiness_home%\goods下
6. 删除 %ebusiness_home%\goods\migrations目录下所有py文件
7. 在ebusiness目录下运行如下命令：  
/ebusiness>python manage.py makemigrations goods  
/ebusiness>python manage.py migrate  
8.	查看数据库，应该出现表goods_user、goods_goods等表：  
9.	运行如下命令  
INSERT INTO `goods_user` VALUES (1, 'linda', '24c8f01350b011f4388a729d3d3c5fd9c0027bb95c3bb3a6f5b26636391a859f', 'cindy@126.com');  
INSERT INTO `goods_user` VALUES (2, 'cindy', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'cindy@126.com');  
INSERT INTO `goods_user` VALUES (3, 'jerry', '481f6cc0511143ccdd7e2d1b1b94faf0a700a8b49cd13922a70b5ae28acaa8c5', 'cindy@126.com');    
INSERT INTO `goods_user` VALUES (4, 'susan', '9e69e7e29351ad837503c44a5971edebc9b7e6d8601c89c284b1b59bf37afa80', 'cindy@126.com');  
INSERT INTO `goods_user` VALUES (5, 'peter', '87c3bbd5b9a829bef126aeeb3ba9949b4aa168b1320a4349afee66ea624a28f9', 'cindy@126.com');  
INSERT INTO `goods_goods` VALUES (1, '正山堂茶业 元正简雅正山小种红茶茶叶礼盒装礼品 武夷山茶叶送礼', 238, 'static/image/1.jpg', '生产许可证编号: SC11435078200021产品标准号: GB/T13738.2-2008厂名: 福建武夷山国家级自然保护区正山茶业有限公司厂址: 武夷山市星村镇桐木村庙湾厂家联系方式: 4000599567配料表: 正山小种红茶储藏方法: 干燥、防潮、防晒、避光、防异味保质期: 1095食品添加剂: 无产品名称: 元正正山堂 元正 正山小种 简雅礼盒净含量: 250g包装方式: 包装包装种类: 盒装品牌: 元正正山堂系列: 元正 正山小种 简雅礼盒茶种类: 正山小种级别: 特级生长季节: 春季产地: 中国大陆省份: 福建省城市: 武夷山市食品工艺: 小种红茶套餐份量: 1人套餐周期: 1周配送频次: 1周1次特产品类: 正山小种价格段: 200-299元');  
INSERT INTO `goods_goods` VALUES (2, '红茶茶叶 正山小种武夷山红茶170g 春茶袋装170g散装新茶', 250, 'static/image/2.jpg', '生产许可证编号: SC11435052401681产品标准号: GB/T19598厂名: 福建省安溪县西坪南驰茶叶加工厂厂址: 安溪县西坪镇西坪村厂家联系方式: 13645928990配料表: 正山小种储藏方法: 防潮保质期: 540食品添加剂: 无任何添加剂净含量: 170g包装方式: 包装包装种类: 袋装品牌: 琨璟系列: 正山小种茶种类: 正山小种级别: 一级生长季节: 春季产地: 中国大陆省份: 福建省城市: 武夷山市食品工艺: 小种红茶套餐份量: 3人套餐周期: 1周配送频次: 1周2次');  
INSERT INTO `goods_goods` VALUES (3, '晋袍 花蜜香正山小种红茶 300g牛皮纸袋装礼盒 武夷山桐木关包邮', 360, 'static/image/3.jpg', '生产许可证编号: QS350714012179厂名: 福建省洪顺翔茶业有限公司厂址: 松溪县茶平乡官路村厂家联系方式: 4000605134配料表: 正山小种储藏方法: 干燥、密封、恒温存储保质期: 365食品添加剂: 无食品添加剂净含量: 300g包装方式: 包装包装种类: 礼盒装茶种类: 正山小种级别: 特级生长季节: 春季产地: 中国大陆省份: 福建省城市: 武夷山市食品工艺: 小种红茶套餐份量: 3人套餐周期: 2周配送频次: 1周2次');  
INSERT INTO `goods_goods` VALUES (4, '正山小种红茶特级 新茶 礼盒装 桂圆香 送礼红茶暖养胃茶叶250g', 450, 'static/image/4.jpg', '生产许可证编号: QS350714010038产品标准号: GB/T 13738.2-2008厂名: 福建省政和建溪茶厂厂址: 政和县石屯镇西津村新厂3层厂家联系方式: 15060888409配料表: 正山小种红茶储藏方法: 常温、防潮、防异味、避光保质期: 720食品添加剂: 无净含量: 250g包装方式: 包装包装种类: 袋装品牌: 淘春秋系列: 30茶种类: 正山小种级别: 特级生长季节: 春季产地: 中国大陆省份: 福建省城市: 武夷山市食品工艺: 小种红茶套餐份量: 1人套餐周期: 1周配送频次: 1周2次特产品类: 正山小种红茶价格段: 500元以上，生产日期: 2017年04月12日 至 2017年04月13日');  
INSERT INTO `goods_goods` VALUES (5, '2016春茶 武夷红茶 桐木关 野生红茶 正山小种 包邮 办公室用茶', 769, 'static/image/5.jpg', '生产许可证编号: SC11435078202263产品标准号: GB/T13738.2-2008厂名: 武夷山市武杨茶业发展有限公司厂址: 武夷山市五夫镇五夫村寺前小组厂家联系方式: 0599--5237765配料表: 正山小种储藏方法: 密封、避光、防潮、防异味保质期: 1095食品添加剂: 无净含量: 200g包装方式: 包装包装种类: 盒装品牌: 茶庸系列: 红茶茶种类: 正山小种级别: 特级生长季节: 春季产地: 中国大陆省份: 福建省城市: 武夷山市食品工艺: 小种红茶套餐份量: 1人特产品类: 正山小种红茶价格段: 60-99元');  
INSERT INTO `goods_goods` VALUES (6, '安吉白茶', 890, 'static/image/6.jpg', '吉白茶，浙江省安吉县特产，国家地理标志产品。安吉白茶外形挺直略扁，形如兰蕙；色泽翠绿，白毫显露；叶芽如金镶碧鞘，内裹银箭，十分可人。冲泡后，清香高扬且持久。滋味鲜爽，饮毕，唇齿留香，回味甘而生津。叶底嫩绿明亮，芽叶朵朵可辨。2004年4月，原国家质检总局正式批准“安吉白茶”为原产地域保护产品（即地理标志保护产品）');  
INSERT INTO `goods_goods` VALUES (7, '普洱茶', 1067, 'static/image/1.jpg', '普洱茶主要产于云南省的西双版纳、临沧、普洱等地区。普洱茶讲究冲泡技巧和品饮艺术，其饮用方法丰富，既可清饮，也可混饮。普洱茶茶汤橙黄浓厚，香气高锐持久，香型独特，滋味浓醇，经久耐泡');  
INSERT INTO `goods_goods` VALUES (8, '火腿肠', 23, 'static/image/2.jpg', '火腿（英语：Ham），是腌制或熏制的动物的腿（如牛腿、羊腿、猪腿、鸡腿），是经过盐渍、烟熏、发酵和干燥处理的腌制动物后腿，又名“火肉”“兰熏”。中国传统特色美食。原产于浙江金华，现代以浙江金华和江苏如皋，江西安福与云南宣威出产的火腿最有名。');  
INSERT INTO `goods_goods` VALUES (9, '老城隍庙 奶油五香豆', 50, 'static/image/3.jpg', '五香豆又称奶油五香豆，是上海市的一种著名传统小吃，该食品由上海老城隍庙郭记兴隆五香豆店首创，故又称城隍庙奶油五香豆；早在1930年前，上海已有以桂皮、茴香等香料烧制的小青豆制食品，颇受各地市民欢迎。');  
INSERT INTO `goods_goods` VALUES (10, '花生', 3.4, 'static/image/4.jpg', '落花生（学名：Arachis hypogaea Linn.）：蔷薇目、豆科，落花生属的一年生草本植物。根部有丰富的根瘤；茎和分枝均有棱，叶纸质对生；叶柄基部抱茎，卵状长圆形至倒卵形，先端钝圆形，两面被毛，边缘具睫毛；叶脉边缘互相联结成网状；花长约8毫米；苞片披针形；花冠黄色或金黄色，旗瓣开展，翼瓣与龙骨瓣分离，长圆形或斜卵形，花柱延伸于萼管咽部之外，荚果膨胀，荚厚，6-8月花果期。');  
INSERT INTO `goods_goods` VALUES (11, '烤鸭', 50, 'static/image/5.jpg', '烤鸭是北京和南京的一道特色名菜，属于北京菜或金陵菜，该菜品以色泽红艳，肉质细嫩，味道醇厚，肥而不腻的特色，被誉为“天下美味”而驰名中外，其色泽略黄，柔软淡香，夹卷其他荤素食物食用，为宴席常用菜点，更是家常风味美食。');  
INSERT INTO `goods_goods` VALUES (12, '瓜子', 2.15, 'static/image/6.jpg', '瓜的种子，特指炒熟了的做食品的倭瓜子、西瓜子等。 又叫瓜子儿，俗名叫边果。它的种类较多，有葵花子、海瓜子、吊瓜子、西瓜子、南瓜子、黄瓜子、丝瓜子等。葵花子是向日葵的果实，不但可以作为零食，而且还可以作为制作糕点的原料，同时也是重要的榨油原料，是高档健康的油脂来源。');  
INSERT INTO `goods_goods` VALUES (13, '大排', 29, 'static/image/1.jpg', '大排是里脊肉与背脊肉连接的部位，又称为肉排，多用于油炸。以肉片为主，但带着排骨。');  
INSERT INTO `goods_goods` VALUES (14, '烤肉', 50, 'static/image/2.jpg', '烤肉（barbecues），是中国的一道菜品，制作原料有猪肉、牛肉、蔬菜、海鲜等。独具风味，历史悠久，有浓郁的香味和鲜美的味道，可大大提高食欲。值得一提的是，现代烤肉与刀耕火种时的烤肉并不相同。据《汉代画象全集》可知，早在两汉时期就有体系完备的烤肉烤食讲究');  
INSERT INTO `goods_goods` VALUES (15, '羊肉串', 10, 'static/image/3.jpg', '羊肉串是指新鲜的羊肉用竹签或钢签穿成串后烧烤制成的菜品，是一种比较常见的烧烤类菜品');  
INSERT INTO `goods_goods` VALUES (16, '辣子鸡丁', 30, 'static/image/4.jpg', '辣子鸡丁，特色传统菜肴，属川菜系， 一道家常菜，较辣，是重庆一道著名的江湖风味菜，起源于歌乐山。干辣椒不是主料胜似主料，充分体现了江湖厨师“下手重”的特点。经巴国布衣厨师精心改良后其口味更富有特色，成菜色泽棕红油亮，质地酥软，麻辣味浓。咸鲜醇香，略带回甜，是一款食者啖之难忘的美味佳肴。');  
10.	查看ebusiness数据库goods_goods和goods_user表中是否有相应的数据。
