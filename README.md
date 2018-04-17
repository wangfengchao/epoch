## **背景**
基于Python2.7.13的Scrapy爬虫框架。

## **部署步骤**
### **.WIN部署**
 依赖安装好，修改settings.py文件中相关目录配置， 本地启动就可以。。。
 相关依赖请看Linux部署。
 
### **.LINUX部署**
#### **1. Python配置：**</br>
下载：https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz </br></br>
解压到服务器目录： tar -zxf Python-2.7.13.tgz</br></br>
进入Python-2.7.13目录： cd Python-2.7.13</br></br>
编译&安装：</br>
    ./configure --enable-shared --enable-loadable-sqlite-extensions --with-zlib   其中--enable-loadable-sqlite-extensions是sqlite的扩展</br></br>
    vi ./Modules/Setup</br>
    找到#zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz去掉注释并保存</br>
    make && make install</br>
</br>
验证：  </br>
    使用  python -V  命令 查看python版本。 </br></br>
       
#### **2. 安装scrapyd服务**
步骤：http://blog.csdn.net/xxwang6276/article/details/45745181
 
#### **3. phantomjs配置**
下载：https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2</br>
解压到服务器目录： tar jxvf phantomjs-2.1.1-linux-x86_64.tar.bz2 </br>
修改目录名称： mv phantomjs-2.1.1-linux-x86_64 phantomjs-2.1.1</br>

#### **4. 安装其他依赖**
 pip install scrapyd-client：部署Scrapy到Scrapyd-client中</br>
 pip install pymysql： python MySql</br>
 pip install sqlalchemy： Python Mysql 依赖注入框架</br>
 pip install Twisted   </br>
 pip install Scrapy： 爬虫框架</br>
  
#### **5. 运行**
  本地运行 scrapy  crawl  spiders名称

### PS:由于各公司大神各显神通，不断的修改&提高反爬虫策略，爬虫和反爬虫工程师之间一直处于进攻和防御状态；程序没有持续维护，可能后期无法爬取数据；需稍加修改爬虫策略。。。