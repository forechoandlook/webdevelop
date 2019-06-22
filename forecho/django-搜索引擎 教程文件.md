# 安装教程

1 安装包

> pip install django-haystack

2 配置

`INSTALL_APPS`中添加



3 搜索引擎
- Solr

setting 设置
```python
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}
```
Solr建立索引时候，搜索效率下降，实时搜索效率不高
Solr利用Zookeeper进行分布式管理
Solr支持更多格式的数据，比如JSON、XML、CSV
Solr官方提供的功能更多
Solr在传统的搜索应用中表现好于Elasticsearch，但在处理实时搜索应用时效率明显低于Elasticsearch。
Solr是传统搜索应用的有力解决方案



Solr有一个更大、更成熟的用户、开发和贡献者社区
Solr搜索海量历史数据，速度非常快，毫秒级返回数据
solr一般要部署到web服务器上，比如tomcat，启动tomcat，配置solr和tomcat的关联

Elasticsearch

```python
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
```
es实时搜索效率高
Elasticsearch自身带有分布式协调管理功能
Elasticsearch仅支持json文件格式
Elasticsearch本身更注重于核心功能，高级功能多有第三方插件提供
Elasticsearch处理实时搜索应用时效率明显
Elasticsearch更适用于新兴的实时搜索应用
es支持分布式，节点对外表现对等，加入节点自动均衡
es完全支持Apache Lucene的接近实时的搜索
es处理多租户multitenancy不需要特殊配置，而Solr需要更多的高级设置
es采用Gateway的概念，使得数据持久化更简单
es各节点组成对等的网络结构，某些节点出现故障时会自动分配其他节点代替其进行工作
es一般可以单独启动，然后es和spring整合，调用SpringDataElasticSearch里面提供的方法



主要特性 
敏捷的API（Pythonic API）。
纯python实现，无二进制包。程序不会莫名其妙的崩溃。
按字段进行索引。
索引和搜索都非常的快 -- 是目前最快的纯python全文搜索引擎。
良好的构架，评分模块/分词模块/存储模块等各个模块都是可插拔的。
功能强大的查询语言（通过pyparsing实现功能）。
纯python实现的拼写检查（目前唯一的纯python拼写检查实现）