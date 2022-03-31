<h1 align='center'> boya-backend </h1>

<h5 align='center'> Design by LXH, ZX, HTH | Direct by Prof Wu</h5>

博雅学院老师的项目的后端，采用mysql+FastAPI。
# 1 首页

<img src="img/image-20220331091935329.png" alt="image-20220331091935329" style="zoom: 15%;" /><img src="img/image-20220331092120937.png" alt="image-20220331092120937" style="zoom:15%;" />

## 1.1 发送用户数据

### 1.1.1 数据库设计

### 1.1.2 后端API实现

```
登录 post

{
	name:微信名
	avator:微信头像
	id:唯一id
}
```

# 2 诗情画意（诗经百科）

## 2.1 诗歌的展示
<img src="img/image-20220331092223984.png" alt="image-20220331092223984" style="zoom:15%;" /><img src="img/fengyasong.jpg" alt="img" style="zoom:15%;" />

### 2.1.1 数据库设计

### 2.1.2 后端API实现

```
返回300首诗的题目
{
	"feng":[
		{
			poem_id
			name
		}
	]
}

给id
{
	poem_id
	audio_url:http
	title
	content
	jieshuo
	zhushi
	picture_id (-1)
	
}
```
## 2.2 配图的展示

<img src="img/duck_picture.jpg" alt="img" style="zoom:15%;" /><img src="img/image-20220331093323826.png" alt="image-20220331093323826" style="zoom:15%;" />


### 2.2.1 数据库设计

### 2.2.2 后端API实现

```
给picture_id
{
	picture_url
	pinying_url
	原文
    出处
}

了解更多
给picture_id
{
	picture_url
	pinying_url
	原文
    出处
    图解
}
```

# 2 渐入佳境（单机，无飞花令）

<img src="img/image-20220331094906735.png" alt="image-20220331094906735" style="zoom:15%;" />

## 2.1 文海磨砺（诗经题库）

<img src="img/image-20220331095112762.png" alt="image-20220331095112762" style="zoom:15%;" />

### 2.1.1 数据库设计

使用mysql，数据库名为`boya`，题目表名为`question_bank`，存放题目相关信息：information_schema

|    字段     |       数据类型        |                       描述                       |
| :---------: | :-------------------: | :----------------------------------------------: |
|     id      | int unsigned NOT NULL |                   自增逻辑主键                   |
|    type     | varchar(10) NOT NULL  |        题目类型（单选、多选、填空、简答）        |
|    theme     | varchar(10) NOT NULL  |        题目主题        |
| description | varchar(255) NOT NULL |                       题干                       |
|   option    |     varchar(255)      | 题目选项（题目为选择题的情况下有效），以换行分隔 |
|   answer    | varchar(255) NOT NULL |         题目答案，若有多个答案以换行分隔         |
| explanation |     varchar(255)      |                     答案解析                     |



可以直接使用Navicat等可视化工具新建查询，然后运行如下sql命令增加题目（注意字符串最好不要换行，会引入`\n`、`\t`啥的）：

```mysql
INSERT INTO question_bank (`type`, `theme`, `description`, `option`, `answer`, `explanation`)
		VALUES ("单选",
				"诗句填空",
				"关关雎鸠，在河之洲。窈窕淑女，君子好逑。参差荇菜，_______。窈窕淑女，________。",
				"A 左右采之；琴瑟友之 \n B 左右流之；寤寐求之 \n C 左右采之；寤寐求之 \n D 左右流之；求之不得",
			    "C",
				"略"
			);
```

### 2.1.2 后端API实现

题目的查询，暂不支持修改、增加等操作（除非到时候要做一个教师端）。

之前已经实现了：

- `get-all`：返回所有题目的信息（包括诗歌内容等关于问题的所有信息）
- `get/{id}`：根据题目id来返回对应的题目。

考虑加一个：

- `get-all-id`：返回所有题目的id，因为`get-all`可能返回的内容太多了。

## 2.2 补字成诗（生僻字）

<img src="img/image-20220331095035069.png" alt="image-20220331095035069" style="zoom:15%;" />

### 2.2.1 数据库设计

### 2.2.2 后端API设计

```
题目
{
	题目列表{题目id，题目内容，题目答案}
}
手写识别
{
	题目id
	图片base4
}

{
	是否正确
}
```

# 3 与诗会友（双人对战，目前就只有飞花令）

## 3.1 对战匹配

<img src="img/image-20220331095232518.png" alt="image-20220331095232518" style="zoom:15%;" />

### 3.1.1 数据库设计

### 3.1.2 后端API实现

```
pk创建房间 websocket
{
	user_id
	房间号
}

加入房间
{
	user_id
	房间号
}
```

## 3.2 飞花令

<img src="img/image-20220331095211307.png" alt="image-20220331095211307" style="zoom:15%;" />

### 3.2.1 数据库设计

### 3.2.2 后端API实现

```
进去就返回 user_id 房间号
{
	player_1_avator_url
	player_2_avator_url
	飞花令题目
}

调百度api

给字符串
{
	是否正确
}
```